#!/usr/bin/env python3
"""List, lint and guard comments in Swift files.

Usage:
  swift_comments.py list FILE...        Print every comment as `file:line: KIND: text`, then
                                        every public/open declaration without a doc comment
                                        as `file:line: UNDOCUMENTED: <declaration>`.
                                        Add --internal to also flag internal/package ones.
  swift_comments.py lint FILE...        Check each documentation comment against DocC rules and
                                        its declaration (parameters, return value, throws).
                                        Prints `file:line: ERROR|WARN CODE: message`, or
                                        `OK file`. Exit 1 if any ERROR.
  swift_comments.py snapshot FILE...    Copy FILEs to a new temporary directory and print its
                                        path. Run before editing.
  swift_comments.py check --base DIR FILE...
                                        Exit 1 if any file's code (everything except comments
                                        and whitespace) differs from its copy in DIR, or if a
                                        `// swiftlint:` directive or the license header was
                                        changed or removed.
  swift_comments.py check --rev REV FILE...
                                        Same, comparing against a git revision instead.

Comment KIND is one of: DOC (/// or /** */), MARK, TODO, FIXME, LINE (//), BLOCK (/* */).
The lexer understands string literals (including multi-line, raw `#"..."#` and
interpolation), so `"//"` inside a string is not taken for a comment.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


# ---------------------------------------------------------------- lexer

def lex(src):
    """Return (code_tokens, comments, masked).

    comments: list of (start_offset, end_offset, line, text).
    masked: src with every comment and string body replaced by spaces (newlines kept),
    so declarations can be parsed by position without being fooled by literals.
    """
    n = len(src)
    masked = list(src)
    code = []
    comments = []

    def blank(a, b):
        for k in range(a, b):
            if masked[k] != "\n":
                masked[k] = " "

    def line_of(pos):
        return src.count("\n", 0, pos) + 1

    def skip_string(i):
        """i points at the opening quote run (after any '#'). Return end offset."""
        hashes = 0
        j = i
        while j > 0 and src[j - 1] == "#":
            j -= 1
            hashes += 1
        multi = src.startswith('"""', i)
        close = ('"""' if multi else '"') + "#" * hashes
        k = i + (3 if multi else 1)
        esc = "\\" + "#" * hashes
        while k < n:
            if src.startswith(esc, k):
                after = k + len(esc)
                if after < n and src[after] == "(":
                    k = lex_code(after + 1, until_paren=True)
                    continue
                k = after + 1
                continue
            if src.startswith(close, k):
                return k + len(close)
            if not multi and src[k] == "\n":
                return k
            k += 1
        return n

    def lex_code(i, until_paren=False):
        depth = 0
        while i < n:
            c = src[i]
            if src.startswith("//", i):
                j = src.find("\n", i)
                j = n if j == -1 else j
                comments.append((i, j, line_of(i), src[i:j]))
                blank(i, j)
                code.append(" ")
                i = j
            elif src.startswith("/*", i):
                start, d = i, 0
                while i < n:
                    if src.startswith("/*", i):
                        d += 1
                        i += 2
                    elif src.startswith("*/", i):
                        d -= 1
                        i += 2
                        if d == 0:
                            break
                    else:
                        i += 1
                comments.append((start, i, line_of(start), src[start:i]))
                blank(start, i)
                code.append(" ")
            elif c == '"':
                j = skip_string(i)
                code.append(src[i:j])
                blank(i + 1, max(i + 1, j - 1))
                i = j
            elif until_paren and c == "(":
                depth += 1
                code.append(c)
                i += 1
            elif until_paren and c == ")":
                if depth == 0:
                    code.append(c)
                    return i + 1
                depth -= 1
                code.append(c)
                i += 1
            else:
                code.append(" " if c.isspace() else c)
                i += 1
        return n

    lex_code(0)
    return "".join(code).split(), comments, "".join(masked)


def kind_of(text):
    if (text.startswith("///") and not text.startswith("////")) or \
            (text.startswith("/**") and not text.startswith("/**/") and not text.startswith("/***")):
        return "DOC"
    body = text.lstrip("/*! ").upper()
    for tag in ("MARK", "TODO", "FIXME"):
        if body.startswith(tag):
            return tag
    return "BLOCK" if text.startswith("/*") else "LINE"


# ---------------------------------------------------------------- declarations

MODIFIERS = (r"public|open|internal|fileprivate|private|package|static|class|final|override|"
             r"mutating|nonmutating|convenience|required|lazy|weak|unowned|dynamic|optional|"
             r"nonisolated|isolated|indirect|prefix|postfix|infix|consuming|borrowing|distributed")
KEYWORDS = (r"func|init|subscript|var|let|case|class|struct|enum|protocol|actor|extension|"
            r"typealias|associatedtype|macro|deinit|operator|precedencegroup")
ATTR = r"@[\w.]+(?:\([^()]*(?:\([^()]*\)[^()]*)*\))?"
DECL_RE = re.compile(
    rf"[ \t]*(?P<attrs>(?:{ATTR}\s+)*)(?P<mods>(?:(?:{MODIFIERS})(?:\([^)]*\))?\s+)*)"
    rf"(?P<kw>{KEYWORDS})\b")
ATTR_ONLY_RE = re.compile(rf"[ \t]*(?:{ATTR}\s*)+$")
TYPE_KEYWORDS = ("class", "struct", "enum", "protocol", "actor", "extension")
ACCESS = ("public", "open", "internal", "fileprivate", "private", "package")


def match_decl(masked, pos):
    """Match a declaration starting at pos (start of a line). Return match or None."""
    m = DECL_RE.match(masked, pos)
    # `case` inside a `switch` is not a declaration
    if m and m.group("kw") == "case" and not re.match(r"\s+[A-Za-z_]\w*\s*(\(|=|,|$)", masked[m.end():m.end() + 80].split("\n")[0] + "\n"):
        return None
    return m


def matching(masked, i):
    """masked[i] is an opening bracket. Return the index just after its match."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack = []
    for k in range(i, len(masked)):
        c = masked[k]
        if c in pairs:
            stack.append(pairs[c])
        elif stack and c == stack[-1]:
            stack.pop()
            if not stack:
                return k + 1
    return len(masked)


def split_top(text, sep=","):
    parts, depth, cur, k = [], 0, [], 0
    while k < len(text):
        c = text[k]
        if text.startswith("->", k):
            cur.append("->")
            k += 2
            continue
        if c in "([{<":
            depth += 1
        elif c in ")]}>":
            depth -= 1
        if c == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        k += 1
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


def parse_signature(masked, m):
    """Return dict(kind, name, params[(label, name)], returns(bool|None), throws(bool), text)."""
    kw = m.group("kw")
    k = m.end()
    info = {"kind": kw, "params": [], "returns": None, "throws": False}
    end_line = masked.find("\n", m.start())
    end_line = len(masked) if end_line == -1 else end_line
    info["text"] = " ".join(masked[m.start():end_line].split())
    if kw not in ("func", "init", "subscript", "macro"):
        return info
    paren = masked.find("(", k)
    if paren == -1:
        return info
    # generic clause between name and '(' is allowed; anything else means no param list
    between = masked[k:paren]
    if "{" in between or "\n\n" in between:
        return info
    close = matching(masked, paren)
    for p in split_top(masked[paren + 1:close - 1]):
        head = p.split(":", 1)[0].split()
        if not head:
            continue
        label, name = (head[0], head[1]) if len(head) >= 2 else (head[0], head[0])
        info["params"].append((label, name))
    # effects and return clause, up to '{', 'where' or the next declaration line
    rest_end = len(masked)
    for stop in ("{", "\n\n"):
        s = masked.find(stop, close)
        if s != -1:
            rest_end = min(rest_end, s)
    rest = masked[close:rest_end]
    nxt = DECL_RE.search(rest)
    if nxt and nxt.start() > 0:
        rest = rest[:nxt.start()]
    rest = re.split(r"\bwhere\b", rest)[0]
    info["throws"] = bool(re.search(r"\b(throws|rethrows)\b", rest.split("->")[0]))
    if kw in ("init",):
        info["returns"] = None
    elif "->" in rest:
        rtype = rest.split("->", 1)[1].strip()
        info["returns"] = rtype not in ("Void", "()", "Never", "Swift.Void")
    else:
        info["returns"] = False
    return info


# ---------------------------------------------------------------- doc comments

def doc_blocks(src, comments):
    """Group adjacent DOC comments into blocks: (start_line, end_offset, lines[])."""
    blocks = []
    cur = None
    for start, end, line, text in comments:
        if kind_of(text) != "DOC":
            cur = None
            continue
        if text.startswith("///"):
            body = [text[3:]]
        else:
            inner = text[3:-2] if text.endswith("*/") else text[3:]
            body = inner.split("\n")
            out = []
            for b in body:
                b2 = re.sub(r"^\s*\* ?", "", b) if re.match(r"^\s*\*(?!/)", b) else b
                out.append(b2)
            body = out
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
        gap = src[cur["end"]:start] if cur else None
        if cur and text.startswith("///") and gap is not None and gap.strip() == "" and gap.count("\n") == 1:
            cur["lines"].extend(body)
            cur["end"] = end
        else:
            cur = {"line": line, "end": end, "lines": body}
            blocks.append(cur)
    for b in blocks:
        # one leading space after /// is markup-neutral
        if all(not l or l.startswith(" ") for l in b["lines"]):
            b["lines"] = [l[1:] if l.startswith(" ") else l for l in b["lines"]]
    return blocks


def next_decl(masked, pos):
    """Skip blank and attribute-only lines after pos; return (decl match, line start) or None."""
    k = masked.find("\n", pos)
    if k == -1:
        return None
    k += 1
    while k < len(masked):
        e = masked.find("\n", k)
        e = len(masked) if e == -1 else e
        line = masked[k:e]
        if ATTR_ONLY_RE.match(line):
            k = e + 1
            continue
        if not line.strip():
            return None
        m = match_decl(masked, k)
        return (m, k) if m else None
    return None


TAG_RE = re.compile(r"^[-*+] +(?P<kw>[A-Za-z]+)(?: +(?P<arg>[^:]+?))?\s*:(?P<rest>.*)$")
NESTED_RE = re.compile(r"^(?P<indent> +)[-*+] +(?P<name>[^:\s]+)\s*:")


def lint_block(path, block, info, emit):
    lines = block["lines"]
    line0 = block["line"]
    if any("\t" in l for l in lines):
        emit(line0, "WARN", "TAB", "tab in doc comment; indent with spaces")
    paras = []
    cur = []
    for l in lines:
        if l.strip():
            cur.append(l)
        elif cur:
            paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    if not paras or TAG_RE.match(paras[0][0].strip()):
        emit(line0, "ERROR", "NO_SUMMARY", "first paragraph must be a one-sentence summary")
    else:
        summary = " ".join(x.strip() for x in paras[0])
        if len(summary) > 150:
            emit(line0, "WARN", "LONG_SUMMARY", f"summary is {len(summary)} characters; aim for 150 or fewer")
        if "](" in summary or "``" in summary or "<doc:" in summary:
            emit(line0, "WARN", "SUMMARY_LINK", "keep the summary plain text: no links or symbol links")
    tags = []  # (kw, arg, line_index)
    section_names = []
    in_params = False
    for idx, l in enumerate(lines):
        t = TAG_RE.match(l)
        if t and not l.startswith(" "):
            kw = t.group("kw").lower()
            tags.append((kw, (t.group("arg") or "").strip(), idx))
            in_params = kw == "parameters"
            continue
        if in_params:
            nm = NESTED_RE.match(l)
            if nm and len(nm.group("indent")) < 4:  # deeper items belong to a description
                if len(nm.group("indent")) != 2:
                    emit(line0 + idx, "ERROR", "INDENT",
                         f"nested parameter '{nm.group('name')}' must be indented exactly 2 spaces")
                else:
                    section_names.append(nm.group("name"))
            elif l.strip() and not l.startswith(" "):
                in_params = False
    kws = [t[0] for t in tags]
    field_names = [t[1] for t in tags if t[0] == "parameter"]
    if "parameters" in kws and "parameter" in kws:
        emit(line0, "WARN", "MIXED_PARAMS", "use either a '- Parameters:' section or '- Parameter x:' fields, not both")
    for kw in ("returns", "throws", "parameters"):
        if kws.count(kw) > 1:
            emit(line0, "ERROR", "DUPLICATE", f"more than one '- {kw.capitalize()}:' item")
    order = [k for k in kws if k in ("parameter", "parameters", "returns", "throws")]
    rank = {"parameter": 0, "parameters": 0, "returns": 1, "throws": 2}
    if [rank[k] for k in order] != sorted(rank[k] for k in order):
        emit(line0, "WARN", "ORDER", "put Parameters, then Returns, then Throws")
    if info is None:
        if tags and any(k in ("parameter", "parameters", "returns", "throws") for k in kws):
            emit(line0, "WARN", "NO_DECL", "doc comment has tags but no declaration was recognized below it")
        return
    documented = section_names + field_names
    if info["kind"] in ("func", "init", "subscript", "macro"):
        names = [n for _, n in info["params"] if n != "_"]
        labels = {lab: n for lab, n in info["params"] if lab != n}
        for d in documented:
            if d not in names:
                if d in labels:
                    emit(line0, "ERROR", "LABEL_NOT_NAME",
                         f"'{d}' is an argument label; document the parameter name '{labels[d]}'")
                else:
                    emit(line0, "ERROR", "EXTRA_PARAM", f"'{d}' is not a parameter of this declaration")
        for nme in names:
            if nme not in documented:
                emit(line0, "ERROR", "MISSING_PARAM", f"parameter '{nme}' is not documented")
        if info["returns"] and "returns" not in kws:
            emit(line0, "ERROR", "MISSING_RETURNS", "returns a value but has no '- Returns:'")
        if info["returns"] is False and "returns" in kws:
            emit(line0, "ERROR", "EXTRA_RETURNS", "has '- Returns:' but returns nothing")
        if info["throws"] and "throws" not in kws:
            emit(line0, "ERROR", "MISSING_THROWS", "can throw but has no '- Throws:'")
        if not info["throws"] and "throws" in kws and info["kind"] != "subscript":
            emit(line0, "ERROR", "EXTRA_THROWS", "has '- Throws:' but does not throw")
    elif documented or "returns" in kws:
        emit(line0, "WARN", "TAG_ON_NON_FUNCTION",
             f"Parameters/Returns on a '{info['kind']}' declaration")


# ---------------------------------------------------------------- commands

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def cmd_list(files, internal):
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        for _, _, line, text in comments:
            kind = kind_of(text)
            first = " ".join(text.split("\n")[0].split())
            print(f"{path}:{line}: {kind}: {first[:120]}")
        documented_lines = set()
        for b in doc_blocks(src, comments):
            nd = next_decl(masked, b["end"])
            if nd:
                documented_lines.add(nd[1])
        # Frames for open braces: ("type", keyword, access) for a type or extension body,
        # ("code", None, None) for anything else (function bodies, closures, accessors).
        # Only declarations at file level or directly in a type body are API.
        frames = []
        pending = None  # a type declaration whose `{` is on a later line
        pos = 0
        while pos < len(masked):
            e = masked.find("\n", pos)
            e = len(masked) if e == -1 else e
            line_text = masked[pos:e]
            top = frames[-1] if frames else None
            # attribute-only lines belong to the declaration on a following line
            m = None if ATTR_ONLY_RE.match(line_text) else match_decl(masked, pos)
            kw = access = None
            if m and (top is None or top[0] == "type"):
                mods = m.group("mods").split()
                kw = m.group("kw")
                access = next((x.split("(")[0] for x in mods if x.split("(")[0] in ACCESS), None)
                if access is None and top is not None:
                    _, parent_kw, parent_access = top
                    inherits = parent_kw in ("protocol", "extension") or (parent_kw == "enum" and kw == "case")
                    if inherits and parent_access in ("public", "open"):
                        access = "public"
                wanted = access in ("public", "open") or (internal and access in (None, "internal", "package"))
                if kw == "case" and (top is None or top[1] != "enum"):
                    wanted = False
                if wanted and kw not in ("extension", "deinit") and "override" not in mods \
                        and pos not in documented_lines:
                    info = parse_signature(masked, m)
                    print(f"{path}:{masked.count(chr(10), 0, pos) + 1}: UNDOCUMENTED: {info['text'][:120]}")
            elif m:
                m = None
            if m:
                pending = ("type", kw, access) if kw in TYPE_KEYWORDS else None
            for c in line_text:
                if c == "{":
                    frames.append(pending or ("code", None, None))
                    pending = None
                elif c == "}" and frames:
                    frames.pop()
            pos = e + 1
    return 0


def cmd_lint(files):
    errors = 0
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        found = []

        def emit(line, level, code, msg):
            found.append((line, level, code, msg))

        for b in doc_blocks(src, comments):
            nd = next_decl(masked, b["end"])
            info = parse_signature(masked, nd[0]) if nd else None
            lint_block(path, b, info, emit)
        for line, level, code, msg in sorted(found):
            print(f"{path}:{line}: {level} {code}: {msg}")
            errors += level == "ERROR"
        if not found:
            print(f"OK {path}")
    return 1 if errors else 0


def snapshot_path(base, path):
    """Where `snapshot` keeps the copy of path inside base (works for any path)."""
    return os.path.join(base, os.path.abspath(path).lstrip(os.sep))


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "lint", "snapshot", "check"):
        print(__doc__, file=sys.stderr)
        return 2
    mode, args = argv[1], argv[2:]
    internal = "--internal" in args
    args = [a for a in args if a != "--internal"]
    rev = base = None
    if mode == "check":
        if args[:1] == ["--rev"]:
            rev, args = args[1], args[2:]
        elif args[:1] == ["--base"]:
            base, args = args[1], args[2:]
        else:
            print("check needs --base DIR or --rev REV", file=sys.stderr)
            return 2
    files = [a for a in args if a.endswith(".swift")]
    if not files:
        print("no .swift files given", file=sys.stderr)
        return 2
    if mode == "list":
        return cmd_list(files, internal)
    if mode == "lint":
        return cmd_lint(files)
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="swift-comment-")
        for path in files:
            dest = snapshot_path(out, path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    status = 0
    for path in files:
        if base is not None:
            old_path = snapshot_path(base, path)
            old = read(old_path) if os.path.exists(old_path) else None
        else:
            old = git_show(rev, path)
        if old is None:
            print(f"{path}: NEW (no earlier copy to compare)")
            continue
        new = read(path)
        a, b = lex(old)[0], lex(new)[0]
        new_guarded = guarded(new)
        lost = [g for g in guarded(old) if g not in new_guarded]
        if a == b and not lost:
            print(f"{path}: OK")
            continue
        status = 1
        if a != b:
            i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            print(f"{path}: CODE changed near token {i}: "
                  f"before `{' '.join(a[max(0, i - 3):i + 4])}` / after `{' '.join(b[max(0, i - 3):i + 4])}`")
        for kind, text in lost:
            print(f"{path}: {kind} changed or removed: {text[:120]}")
    return status


GUARD = re.compile(r"^(?://|/\*)\s*(?:swiftlint:|swift-format-ignore|sourcery:|periphery:ignore)", re.IGNORECASE)


def guarded(src):
    """DIRECTIVE and LICENSE comments (license = before the first code), whitespace-normalized."""
    _, comments, masked = lex(src)
    first_code = len(masked) - len(masked.lstrip())
    out = []
    for start, _, _, text in comments:
        if GUARD.match(text):
            out.append(("DIRECTIVE", " ".join(text.split())))
        elif start < first_code and re.search(r"copyright|license|licence|SPDX-License-Identifier", text, re.IGNORECASE):
            out.append(("LICENSE", " ".join(text.split())))
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv))
