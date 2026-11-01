#!/usr/bin/env python3
"""List, lint and guard comments in Kotlin files.

Usage:
  kt_comments.py list FILE...           Print every comment as `file:line: KIND: text`, then
                                        every public/protected declaration without KDoc as
                                        `file:line: UNDOCUMENTED: <declaration>`.
                                        Add --internal to also flag internal ones.
  kt_comments.py lint FILE...           Check each KDoc against its declaration. Prints
                                        `file:line: ERROR|WARN CODE: message`, or `OK file`.
                                        Exit 1 if any ERROR.
  kt_comments.py snapshot FILE...       Copy FILEs to a new temporary directory and print its
                                        path. Run before editing.
  kt_comments.py check --base DIR FILE...
                                        Exit 1 if any file's code (everything except comments
                                        and whitespace) differs from its copy in DIR, or if a
                                        DIRECTIVE or LICENSE comment was changed or removed.
  kt_comments.py check --rev REV FILE...
                                        Same, comparing against a git revision instead.

Comment KIND is one of: DOC (/** */), LICENSE (a copyright or license comment before the
first line of code), DIRECTIVE (ktlint-disable, noinspection, @formatter:, NOSONAR,
language=, region/endregion), TODO, FIXME, LINE (//), BLOCK (/* */).
The lexer understands nested block comments, string templates, raw strings and char
literals, so `"//"` inside a string is not taken for a comment.
Declarations inside function bodies, override members, members of private types and
primary-constructor properties (documented with @property) are not listed.

Lint codes: SUMMARY_MISSING, UNKNOWN_TAG, DEPRECATED_TAG (use the @Deprecated
annotation), PARAM_UNKNOWN (@param/@property names nothing in the signature),
RETURN_ON_UNIT, ORPHAN_DOC (KDoc not followed by a declaration).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

DIRECTIVE = re.compile(
    r"^(?://|/\*)\s*(?:ktlint-disable|ktlint-enable|noinspection|@formatter:|NOSONAR|language=|region\b|endregion\b"
    r"|detekt\b|suppress\b)", re.IGNORECASE)
MODIFIERS = (r"public|private|internal|protected|open|abstract|final|sealed|data|enum|annotation|inner|value"
             r"|inline|override|suspend|tailrec|operator|infix|external|const|lateinit|companion|expect|actual|fun")
DECL = re.compile(r"\b(class|interface|object|fun|val|var|typealias|constructor)\b")
HEAD_OK = re.compile(r"^\s*(?:(?:@[\w.:]+(?:\([^()]*\))?|" + MODIFIERS + r")\s+)*$")
TYPE_KW = {"class", "interface", "object"}
KNOWN_TAGS = {"param", "return", "constructor", "receiver", "property", "throws", "exception",
              "sample", "see", "author", "since", "suppress"}


# ---------------------------------------------------------------- lexer

def lex(src):
    """Return (code_tokens, comments, masked).

    comments: list of (start, end, line, text, before_code).
    masked: src with every comment and string body replaced by spaces (newlines kept).
    """
    n = len(src)
    masked = list(src)
    code = []
    comments = []
    seen_code = [False]

    def blank(a, b):
        for k in range(a, b):
            if masked[k] != "\n":
                masked[k] = " "

    def skip_string(i):
        """i at an opening quote; return the index after the closing quote."""
        raw = src.startswith('"""', i)
        j = i + (3 if raw else 1)
        while j < n:
            if raw and src.startswith('"""', j):
                j += 3
                while j < n and src[j] == '"':  # """...""""" ends at the last quote
                    j += 1
                return j
            if not raw and src[j] == '"':
                return j + 1
            if not raw and src[j] == "\\":
                j += 2
                continue
            if src.startswith("${", j):
                j = skip_template(j + 2)
                continue
            j += 1
        return n

    def skip_template(j):
        depth = 1
        while j < n and depth:
            if src[j] == '"':
                j = skip_string(j)
                continue
            if src[j] == "'":
                j = skip_char(j)
                continue
            depth += {"{": 1, "}": -1}.get(src[j], 0)
            j += 1
        return j

    def skip_char(j):
        m = re.compile(r"'(?:\\u[0-9a-fA-F]{4}|\\.|[^\\'\n])'").match(src, j)
        return m.end() if m else j + 1

    i, line = 0, 1
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j == -1 else j
        elif src.startswith("/*", i):
            j, depth = i, 0
            while j < n:
                if src.startswith("/*", j):
                    depth += 1
                    j += 2
                elif src.startswith("*/", j):
                    depth -= 1
                    j += 2
                    if depth == 0:
                        break
                else:
                    j += 1
        else:
            j = None
        if j is not None:
            comments.append((i, j, line, src[i:j], not seen_code[0]))
            blank(i, j)
            line += src.count("\n", i, j)
            code.append(" ")
            i = j
            continue
        if c in "\"'":
            j = skip_string(i) if c == '"' else skip_char(i)
            blank(i + 1, j - 1)
            code.append(src[i:j])
            line += src.count("\n", i, j)
            seen_code[0] = True
            i = j
            continue
        if c == "\n":
            line += 1
        if c.isspace():
            code.append(" ")
        else:
            code.append(c)
            seen_code[0] = True
        i += 1
    return "".join(code).split(), comments, "".join(masked)


def kind_of(text, before_code):
    if DIRECTIVE.match(text):
        return "DIRECTIVE"
    if before_code and re.search(r"copyright|license|licence|SPDX-License-Identifier", text, re.IGNORECASE):
        return "LICENSE"
    if text.startswith("/**") and not text.startswith(("/**/", "/***")):
        return "DOC"
    body = text.lstrip("/*! ").upper()
    for tag in ("TODO", "FIXME"):
        if body.startswith(tag):
            return tag
    return "BLOCK" if text.startswith("/*") else "LINE"


# ---------------------------------------------------------------- declarations

def matching(masked, i, open_ch="(", close_ch=")"):
    depth = 0
    for j in range(i, len(masked)):
        if masked[j] == open_ch:
            depth += 1
        elif masked[j] == close_ch:
            depth -= 1
            if depth == 0:
                return j
    return len(masked) - 1


def split_top(text):
    parts, depth, cur = [], 0, ""
    for ch in text:
        if ch in "(<[{":
            depth += 1
        elif ch in ")>]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def param_names(text):
    names = []
    for p in split_top(text):
        p = re.sub(r"@[\w.:]+(?:\([^()]*\))?", " ", p)
        m = re.match(r"\s*(?:(?:vararg|noinline|crossinline|val|var|" + MODIFIERS + r")\s+)*(\w+)\s*:", p)
        if m:
            names.append(m.group(1))
    return names


def declarations(src, masked):
    """Yield dicts for member-level declarations (not inside function bodies)."""
    stack = [{"type": True, "vis": "public"}]
    paren = 0
    pending = None
    for m in re.finditer(r"[{}()]|" + DECL.pattern, masked):
        tok = m.group(0)
        if tok == "(":
            paren += 1
        elif tok == ")":
            paren = max(0, paren - 1)
        elif tok == "{":
            if paren == 0 and pending is not None:
                stack.append({"type": True, "vis": pending})
            else:
                stack.append({"type": False, "vis": None})
            pending = None
        elif tok == "}":
            if len(stack) > 1:
                stack.pop()
            pending = None
        elif paren == 0 and stack[-1]["type"]:
            line_start = masked.rfind("\n", 0, m.start()) + 1
            head = masked[line_start:m.start()]
            if not HEAD_OK.match(head):
                continue
            kw = m.group(1)
            if kw == "object" and not re.match(r"\s+\w", masked[m.end():]) and "companion" not in head:
                continue  # an object expression, not a declaration
            words = set(re.findall(r"\w+", head))
            vis = next((v for v in ("private", "internal", "protected", "public") if v in words), "public")
            pending = vis if kw in TYPE_KW else None
            eol = masked.find("\n", m.end())
            eol = len(masked) if eol == -1 else eol
            yield {"kw": kw, "pos": m.start(), "line_start": line_start, "vis": vis,
                   "override": "override" in words, "parents": [s["vis"] for s in stack],
                   "text": " ".join(src[line_start:eol].split())}


def doc_for(decl, comments, masked):
    """The DOC comment directly above the declaration (annotations may sit between)."""
    before = [c for c in comments if c[1] <= decl["line_start"]]
    if not before:
        return None
    c = before[-1]
    gap = masked[c[1]:decl["line_start"]]
    if not re.fullmatch(r"(?:\s|@[\w.:]+(?:\([^()]*\))?)*", gap):
        return None
    return c if kind_of(c[3], c[4]) == "DOC" else None


def signature(masked, decl):
    """Return (params, type_params, return_type or None, has_block_body)."""
    rest = masked[decl["pos"]:]

    def type_params(at):
        end = matching(rest, at, "<", ">")
        names = [re.sub(r"^\s*(?:reified|in|out)\s+", "", t).split(":")[0].strip()
                 for t in split_top(rest[at + 1:end])]
        return names, end + 1

    tparams = []
    if decl["kw"] == "class":
        m = re.match(r"class\s+\w+\s*", rest)
        if not m:
            return [], [], None, False
        at = m.end()
        if rest.startswith("<", at):
            tparams, at = type_params(at)
        m = re.compile(r"\s*(?:(?:@[\w.:]+|public|private|internal|protected)\s+)*(?:constructor\s*)?\(").match(rest, at)
        if not m:
            return [], tparams, None, False
        open_paren = m.end() - 1
    else:
        m = re.match(r"(?:fun|constructor)\s*", rest)
        at = m.end() if m else 0
        if rest.startswith("<", at):
            tparams, at = type_params(at)
        open_paren = rest.find("(", at)
        stop = re.compile(r"[{=]").search(rest, at)
        if open_paren == -1 or (stop and stop.start() < open_paren):
            return [], tparams, None, False
    close = matching(rest, open_paren)
    params = param_names(rest[open_paren + 1:close])
    after = rest[close + 1:]
    rm = re.match(r"\s*:\s*([^{=\n]+)", after)
    ret = rm.group(1).strip() if rm else None
    body = re.match(r"\s*(?::\s*[^{=\n]+)?\s*\{", after) is not None
    return params, tparams, ret, body


# ---------------------------------------------------------------- commands

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def cmd_list(files, internal):
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        for _, _, line, text, bc in comments:
            print(f"{path}:{line}: {kind_of(text, bc)}: {' '.join(text.split())[:120]}")
        allowed = ("public", "protected", "internal") if internal else ("public", "protected")
        for d in declarations(src, masked):
            if d["override"] or "companion object" in d["text"] \
                    or any(v not in allowed for v in d["parents"] + [d["vis"]]):
                continue
            if doc_for(d, comments, masked) is None:
                print(f"{path}:{masked.count(chr(10), 0, d['pos']) + 1}: UNDOCUMENTED: {d['text'][:120]}")
    return 0


def cmd_lint(files):
    status = 0
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        decls = list(declarations(src, masked))
        attached = {}
        for d in decls:
            c = doc_for(d, comments, masked)
            if c is not None:
                attached[c[0]] = d
        found = []

        def emit(line, level, code, msg):
            found.append((line, level, code, msg))

        for start, end, line, text, bc in comments:
            if kind_of(text, bc) != "DOC":
                continue
            d = attached.get(start)
            if d is None:
                emit(line, "WARN", "ORPHAN_DOC", "KDoc is not directly above a declaration")
                continue
            body = re.sub(r"^\s*\*(?!/) ?", "", text[3:-2], flags=re.M)
            summary = re.split(r"^\s*@", body, maxsplit=1, flags=re.M)[0]
            if not summary.strip():
                emit(line, "WARN", "SUMMARY_MISSING", "no summary before the block tags")
            params, tparams, ret, block = signature(masked, d) if d["kw"] in ("fun", "class", "constructor") \
                else ([], [], None, False)
            for tm in re.finditer(r"^\s*@(\w+)(?:\s+\[?([\w.]+)\]?)?", body, flags=re.M):
                tag, name = tm.group(1), tm.group(2)
                tline = line + body.count("\n", 0, tm.start())
                if tag == "deprecated":
                    emit(tline, "ERROR", "DEPRECATED_TAG", "KDoc has no @deprecated; propose the @Deprecated annotation")
                elif tag not in KNOWN_TAGS:
                    emit(tline, "WARN", "UNKNOWN_TAG", f"@{tag} is not a KDoc block tag")
                elif tag in ("param", "property") and d["kw"] in ("fun", "class", "constructor") \
                        and name and name not in params + tparams:
                    emit(tline, "ERROR", "PARAM_UNKNOWN", f"@{tag} {name}: no such parameter in the signature")
                elif tag == "return" and d["kw"] == "fun" and (ret == "Unit" or (ret is None and block)):
                    emit(tline, "WARN", "RETURN_ON_UNIT", "@return on a function that returns Unit")
        for line, level, code, msg in sorted(found):
            print(f"{path}:{line}: {level} {code}: {msg}")
            if level == "ERROR":
                status = 1
        if not found:
            print(f"OK {path}")
    return status


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def guarded(comments):
    return [(k, " ".join(t.split())) for _, _, _, t, bc in comments
            for k in [kind_of(t, bc)] if k in ("DIRECTIVE", "LICENSE")]


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
    if base is not None and not os.path.isdir(base):
        print(f"snapshot directory not found: {base!r}", file=sys.stderr)
        return 2
    files = [a for a in args if a.endswith((".kt", ".kts"))]
    if not files:
        print("no .kt files given", file=sys.stderr)
        return 2
    if mode == "list":
        return cmd_list(files, internal)
    if mode == "lint":
        return cmd_lint(files)
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="kotlin-comment-")
        for path in files:
            dest = os.path.join(out, os.path.abspath(path).lstrip(os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    status = 0
    for path in files:
        tokens, comments, _ = lex(read(path))
        if base is not None:
            copy = os.path.join(base, os.path.abspath(path).lstrip(os.sep))
            old = read(copy) if os.path.exists(copy) else None
        else:
            old = git_show(rev, path)
        if old is None:
            print(f"SKIP {path}: no earlier copy")
            continue
        old_tokens, old_comments, _ = lex(old)
        ok = True
        if old_tokens != tokens:
            ok = False
            k = next((x for x in range(min(len(old_tokens), len(tokens)))
                      if old_tokens[x] != tokens[x]), min(len(old_tokens), len(tokens)))
            print(f"CODE {path}: code changed near\n     was: {' '.join(old_tokens[max(0, k - 5):k + 5])}"
                  f"\n     now: {' '.join(tokens[max(0, k - 5):k + 5])}")
        new_guarded = guarded(comments)
        for kind, text in guarded(old_comments):
            if (kind, text) not in new_guarded:
                ok = False
                print(f"{kind} {path}: changed or removed: {text[:120]}")
        if ok:
            print(f"OK   {path}: only comments/whitespace changed")
        else:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
