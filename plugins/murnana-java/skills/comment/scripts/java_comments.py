#!/usr/bin/env python3
"""List, lint and guard comments in Java files.

Usage:
  java_comments.py list [--package] FILE...
        Print every comment as `file:line: KIND: text`, then every API declaration
        without a doc comment as `file:line: UNDOCUMENTED: <kind> <declaration>`.
        API = public/protected (and interface members) inside visible types.
        --package also counts package-private declarations as API.
  java_comments.py lint [--package] [--tags a,b] [--classpath CP] FILE...
        Run javac doclint (if javac is on PATH) and this script's own checks.
        Prints `file:line: ERROR|WARN CODE: message`, or `OK file`. Exit 1 if any ERROR.
        --tags names custom block tags the build registers (apiNote,implSpec,...).
        --classpath lets doclint resolve references to dependencies.
  java_comments.py snapshot FILE...
        Copy FILEs to a new temporary directory and print its path. Run before editing.
  java_comments.py check --base DIR FILE...   (or --rev REV)
        Exit 1 if any file's code (everything except comments and whitespace)
        differs from its copy in DIR (or in git revision REV), or if a tool directive
        (//CHECKSTYLE:, NOSONAR, //noinspection, @formatter:) or the license header
        was changed or removed.

Comment KIND: DOC (/** */ attached to a declaration), ORPHAN_DOC (/** */ that javadoc
ignores), TODO, FIXME, LINE (//), BLOCK (/* */). The lexer understands string, char
and text-block literals, so "//" inside a string is not taken for a comment.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------- lexer


def lex(src):
    """Return (tokens, comments, masked).

    tokens: code tokens with comments removed; each literal is one exact token.
    comments: list of (start, end, line, text).
    masked: src with comments and literal bodies replaced by spaces (newlines kept).
    """
    n = len(src)
    masked = list(src)
    comments = []
    parts = []  # code text chunks and ("LIT", text)
    buf = []

    def blank(a, b):
        for k in range(a, b):
            if masked[k] != "\n":
                masked[k] = " "

    def flush():
        if buf:
            parts.append("".join(buf))
            buf.clear()

    def scan_quoted(i, close):
        k = i
        while k < n:
            if src[k] == "\\":
                k += 2
                continue
            if src.startswith(close, k):
                return k + len(close)
            if close != '"""' and src[k] == "\n":
                return k
            k += 1
        return n

    i = 0
    while i < n:
        if src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j == -1 else j
            comments.append((i, j, src.count("\n", 0, i) + 1, src[i:j]))
            blank(i, j)
            buf.append(" ")
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            comments.append((i, j, src.count("\n", 0, i) + 1, src[i:j]))
            blank(i, j)
            buf.append(" ")
            i = j
        elif src.startswith('"""', i):
            j = scan_quoted(i + 3, '"""')
            flush()
            parts.append(("LIT", src[i:j]))
            blank(i + 3, max(i + 3, j - 3))
            i = j
        elif src[i] in "\"'":
            j = scan_quoted(i + 1, src[i])
            flush()
            parts.append(("LIT", src[i:j]))
            blank(i + 1, max(i + 1, j - 1))
            i = j
        else:
            buf.append(src[i])
            i += 1
    flush()
    tokens = []
    for p in parts:
        if isinstance(p, tuple):
            tokens.append(p[1])
        else:
            tokens.extend(re.findall(r"[\w$.]+|\S", p))
    return tokens, comments, "".join(masked)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def line_of(src, pos):
    return src.count("\n", 0, pos) + 1


# ---------------------------------------------------------------- declarations

MODIFIERS = {"public", "protected", "private", "static", "final", "abstract", "sealed",
             "non-sealed", "strictfp", "default", "synchronized", "native", "transient",
             "volatile"}
TYPE_KW = {"class", "interface", "enum", "record", "@interface"}
ANNOT_RE = re.compile(r"@(?!interface\b)[\w$.]+")
OPEN = {"(": ")", "[": "]", "{": "}"}


def match_close(s, i):
    """s[i] is an opening bracket. Return the index just after its match."""
    stack = []
    for k in range(i, len(s)):
        c = s[k]
        if c in OPEN:
            stack.append(OPEN[c])
        elif stack and c == stack[-1]:
            stack.pop()
            if not stack:
                return k + 1
    return len(s)


def skip_annotations(head):
    """Return (annotation names, rest of head) for a declaration head."""
    names = []
    i = 0
    while True:
        while i < len(head) and head[i].isspace():
            i += 1
        m = ANNOT_RE.match(head, i)
        if not m:
            return names, head[i:]
        names.append(m.group(0)[1:].split(".")[-1])
        i = m.end()
        j = i
        while j < len(head) and head[j].isspace():
            j += 1
        if j < len(head) and head[j] == "(":
            i = match_close(head, j)


def split_top(text, sep=","):
    out, depth, cur = [], 0, []
    for c in text:
        if c in "([{<":
            depth += 1
        elif c in ")]}>":
            depth -= 1
        if c == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    if "".join(cur).strip():
        out.append("".join(cur))
    return out


def parse_params(text):
    names = []
    for p in split_top(text):
        _, p = skip_annotations(p.strip())
        ids = re.findall(r"[A-Za-z_$][\w$]*", p.replace("...", " "))
        ids = [x for x in ids if x != "final"]
        if ids:
            names.append(ids[-1])
    return names


def parse_type_params(text):
    """text starts with '<'. Return (names, rest)."""
    depth = 0
    for k, c in enumerate(text):
        if c == "<":
            depth += 1
        elif c == ">":
            depth -= 1
            if depth == 0:
                inner = text[1:k]
                names = [re.match(r"\s*(?:@[\w.]+\s*)*([A-Za-z_$][\w$]*)", p).group(1)
                         for p in split_top(inner) if p.strip()]
                return names, text[k + 1:]
    return [], text


class Decl:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def classify(head, parent):
    """Classify a member head (text before `;`, `{` or `=`). Return Decl or None."""
    annots, rest = skip_annotations(head)
    words = rest.split()
    mods = []
    while words and words[0] in MODIFIERS:
        mods.append(words.pop(0))
    rest = " ".join(words)
    if not rest or rest.split()[0] in ("package", "import", "module", "open"):
        return None
    first = rest.split()[0]
    if first in TYPE_KW or rest.startswith("@interface"):
        kind = "@interface" if rest.startswith("@interface") else first
        m = re.match(r"(?:@interface|class|interface|enum|record)\s+([A-Za-z_$][\w$]*)", rest)
        if not m:
            return None
        after = rest[m.end():]
        tparams, after = parse_type_params(after.lstrip()) if after.lstrip().startswith("<") else ([], after)
        params = []
        if kind == "record" and "(" in after:
            p = after.index("(")
            params = parse_params(after[p + 1:match_close(after, p) - 1])
        return Decl(kind=kind, name=m.group(1), mods=mods, annots=annots, params=params,
                    tparams=tparams, throws=[], returns=None, text=rest)
    tparams = []
    if rest.startswith("<"):
        tparams, rest = parse_type_params(rest)
        rest = rest.strip()
    if "(" in rest:
        p = rest.index("(")
        before = rest[:p].split()
        if not before:
            return None
        name = before[-1]
        rtype = " ".join(before[:-1])
        close = match_close(rest, p)
        params = parse_params(rest[p + 1:close - 1])
        tail = rest[close:]
        throws = []
        m = re.search(r"\bthrows\b(.*)", tail)
        if m:
            throws = [t.strip().split(".")[-1] for t in split_top(m.group(1)) if t.strip()]
        kind = "constructor" if not rtype else "method"
        return Decl(kind=kind, name=name, mods=mods, annots=annots, params=params,
                    tparams=tparams, throws=throws,
                    returns=None if kind == "constructor" else rtype, text=rest)
    if parent and parent.kind == "record" and rest.split() == [parent.name]:
        return Decl(kind="constructor", name=parent.name, mods=mods, annots=annots,
                    params=[], tparams=[], throws=[], returns=None, text=rest)
    names = []
    for d in split_top(rest):
        ids = re.findall(r"[A-Za-z_$][\w$]*", d.split("=")[0])
        if ids:
            names.append(ids[-1])
    if not names or len(rest.split()) < 2:
        return None
    return Decl(kind="field", name=", ".join(names), mods=mods, annots=annots, params=[],
                tparams=[], throws=[], returns=None, text=rest, count=len(names))


def visible(decl, parent, package_level):
    if "private" in decl.mods:
        return False
    if parent is not None and not parent.visible:
        return False
    if parent is not None and parent.kind in ("interface", "@interface"):
        return True
    if decl.kind == "enum constant":
        return True
    if "public" in decl.mods or "protected" in decl.mods:
        return True
    return package_level


def declarations(src, masked, comments, package_level=False):
    """Return a list of Decl with .line, .doc (comment tuple or None), .parent."""
    by_end = {}
    for c in comments:
        by_end[c[1]] = c
    out = []

    def doc_before(pos):
        k = pos
        while k > 0 and src[k - 1].isspace():
            k -= 1
        c = by_end.get(k)
        if c and c[3].startswith("/**") and not c[3].startswith("/**/"):
            return c
        return None

    def add(decl, start, parent):
        decl.line = line_of(src, start)
        decl.start = start
        decl.doc = doc_before(start)
        decl.parent = parent
        decl.visible = visible(decl, parent, package_level)
        out.append(decl)

    def enum_constants(i, end, parent):
        """Parse enum constants from i; return index after the terminating ';' (or end)."""
        while i < end:
            while i < end and (masked[i].isspace() or masked[i] == ","):
                i += 1
            if i >= end or masked[i] in ";}":
                return i + 1 if i < end and masked[i] == ";" else i
            start = i
            annots, _ = skip_annotations(masked[i:end])
            j = i
            # skip annotations
            while True:
                while j < end and masked[j].isspace():
                    j += 1
                m = ANNOT_RE.match(masked, j)
                if not m:
                    break
                j = m.end()
                while j < end and masked[j].isspace():
                    j += 1
                if masked[j] == "(":
                    j = match_close(masked, j)
            m = re.compile(r"[A-Za-z_$][\w$]*").match(masked, j)
            if not m:
                return i + 1
            j = m.end()
            while j < end and masked[j].isspace():
                j += 1
            if j < end and masked[j] == "(":
                j = match_close(masked, j)
                while j < end and masked[j].isspace():
                    j += 1
            if j < end and masked[j] == "{":
                j = match_close(masked, j)
            add(Decl(kind="enum constant", name=m.group(0), mods=[], annots=annots, params=[],
                     tparams=[], throws=[], returns=None, text=m.group(0)), start, parent)
            i = j
        return i

    def body(i, end, parent):
        if parent is not None and parent.kind == "enum":
            i = enum_constants(i, end, parent)
        while i < end:
            while i < end and masked[i].isspace():
                i += 1
            if i >= end:
                return
            if masked[i] == ";":
                i += 1
                continue
            start = i
            depth = 0
            k = i
            stop = None
            while k < end:
                c = masked[k]
                if c in "([":
                    depth += 1
                elif c in ")]":
                    depth -= 1
                elif depth == 0 and c in ";{=":
                    stop = c
                    break
                elif c == "@" and depth == 0:
                    # annotation arguments may contain '=' and '{'
                    m = ANNOT_RE.match(masked, k)
                    if m and not masked.startswith("@interface", k):
                        k = m.end()
                        while k < end and masked[k].isspace():
                            k += 1
                        if k < end and masked[k] == "(":
                            k = match_close(masked, k)
                        continue
                k += 1
            if stop is None:
                return
            head = masked[start:k]
            decl = classify(head, parent)
            if stop == "=":
                # skip initializer to the ';' at brace depth 0
                d = 0
                while k < end:
                    c = masked[k]
                    if c in "([{":
                        d += 1
                    elif c in ")]}":
                        d -= 1
                    elif c == ";" and d == 0:
                        break
                    k += 1
                nxt = k + 1
            elif stop == "{":
                nxt = match_close(masked, k)
            else:
                nxt = k + 1
            if decl:
                add(decl, start, parent)
                if decl.kind in TYPE_KW and stop == "{":
                    body(k + 1, nxt - 1, decl)
            i = nxt

    body(0, len(masked), None)
    return out


def package_doc(src, masked, comments, path):
    """For package-info.java: the doc comment before `package`, if any."""
    if os.path.basename(path) != "package-info.java":
        return None
    m = re.search(r"^\s*(?:@[\w.]+(?:\([^)]*\))?\s*)*package\b", masked, re.M)
    if not m:
        return None
    k = m.start()
    while k < len(masked) and masked[k].isspace():
        k += 1
    for c in comments:
        if c[1] <= k and src[c[1]:k].strip() == "" and c[3].startswith("/**"):
            return c
    return None


def kind_of(text):
    body = text.lstrip("/*! ").upper()
    for tag in ("TODO", "FIXME"):
        if body.startswith(tag):
            return tag
    return "BLOCK" if text.startswith("/*") else "LINE"


def short(text, limit=100):
    t = " ".join(text.split())
    return t if len(t) <= limit else t[:limit - 3] + "..."


# ---------------------------------------------------------------- list


def cmd_list(files, package_level):
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        decls = declarations(src, masked, comments, package_level)
        attached = {d.doc[0] for d in decls if d.doc}
        pd = package_doc(src, masked, comments, path)
        if pd:
            attached.add(pd[0])
        for c in comments:
            text = c[3]
            if text.startswith("/**") and not text.startswith("/**/"):
                kind = "DOC" if c[0] in attached else "ORPHAN_DOC"
            else:
                kind = kind_of(text)
            print(f"{path}:{c[2]}: {kind}: {short(text)}")
        for d in decls:
            if not d.visible or d.doc:
                continue
            if d.kind in ("method",) and "Override" in d.annots:
                continue
            print(f"{path}:{d.line}: UNDOCUMENTED: {d.kind} {short(d.text)}")
    return 0


# ---------------------------------------------------------------- lint

STANDARD_BLOCK = ["param", "return", "throws", "exception", "author", "version", "see",
                  "since", "serial", "serialField", "serialData", "deprecated",
                  "hidden", "provides", "uses", "spec"]
ORDER = {t: k for k, t in enumerate(["param", "return", "throws", "exception", "author",
                                     "version", "see", "since", "serial", "serialField",
                                     "serialData", "deprecated"])}
STOP = {"the", "a", "an", "this", "of", "returns", "return", "gets", "get", "sets", "set",
        "is", "checks", "whether", "if", "value", "for", "to"}


def doc_lines(text):
    body = text[3:-2] if text.endswith("*/") else text[3:]
    lines = []
    for ln in body.split("\n"):
        lines.append(re.sub(r"^\s*\*?", "", ln, count=1) if ln.strip().startswith("*") else ln.strip())
    return lines


def split_doc(text):
    """Return (main description, [(tag, arg, rest, line_offset)])."""
    lines = doc_lines(text)
    main, tags, in_pre = [], [], False
    for k, ln in enumerate(lines):
        s = ln.strip()
        if "<pre" in s:
            in_pre = True
        m = None if in_pre else re.match(r"@([A-Za-z]+)\b\s*(.*)", s)
        if m:
            rest = m.group(2)
            arg = rest.split()[0] if rest.split() else ""
            tags.append([m.group(1), arg, rest, k])
        elif tags:
            tags[-1][2] += " " + s
        else:
            main.append(ln)
        if "</pre>" in s:
            in_pre = False
    return "\n".join(main).strip(), tags


def first_sentence(main):
    m = re.search(r"\.(\s|$)", main)
    return main[:m.end()].strip() if m else main.strip()


def camel_words(name):
    return {w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)}


def own_checks(path, src, decl, emit, custom, javac_ok):
    c = decl.doc
    text = c[3]
    main, tags = split_doc(text)
    base = c[2]
    inherit_only = main.strip() == "{@inheritDoc}" and not tags
    # summary
    summary = first_sentence(main)
    raw_first = main.split("\n\n")[0]
    if re.search(r"\b(e\.g|i\.e|vs)\.$", summary):
        emit(base, "WARN", "SUMMARY_ABBREV",
             f"summary is cut at the abbreviation: `{short(summary, 60)}`; write `e.g.&nbsp;` or rephrase")
    for ln in raw_first.split("\n"):
        if re.search(r"。(?=[^\s。」』）)])", ln):
            emit(base, "WARN", "SUMMARY_JA_BREAK",
                 "text follows `。` on the same line, so the summary runs past the first sentence; "
                 "end the line after the first `。`")
            break
    if summary and decl.kind in ("method", "field", "constructor"):
        words = {w.lower() for w in re.findall(r"[A-Za-z]+", re.sub(r"\{@\w+\s*([^}]*)\}", r"\1", summary))}
        nw = set()
        for nm in decl.name.split(", "):
            nw |= camel_words(nm)
        if words and words - STOP <= nw and len(words) <= len(nw) + 3 and decl.kind != "constructor":
            emit(base, "WARN", "SUMMARY_RESTATES",
                 f"summary only restates the name `{decl.name}`; say what the name can't")
    # tags
    last = -1
    order_reported = False
    names = [t[0] for t in tags]
    for tag, arg, rest, off in tags:
        line = base + off
        if tag not in STANDARD_BLOCK and tag not in custom:
            if not javac_ok:
                emit(line, "ERROR", "UNKNOWN_TAG", f"`@{tag}` is not a standard block tag; register it with -tag or remove it")
            continue
        if tag in ORDER:
            if ORDER[tag] < last and not order_reported:
                order_reported = True
                emit(line, "WARN", "TAG_ORDER", f"`@{tag}` is out of the recommended order "
                     "(@param, @return, @throws, @author, @version, @see, @since, @serial*, @deprecated)")
            last = max(last, ORDER[tag])
    has_dep_tag = "deprecated" in names
    has_dep_ann = "Deprecated" in decl.annots
    if has_dep_tag and not has_dep_ann:
        emit(base, "WARN", "DEPRECATED_ANNOTATION", "`@deprecated` tag without the `@Deprecated` annotation (code change: propose it, don't add it)")
    if has_dep_ann and not has_dep_tag:
        emit(base, "WARN", "DEPRECATED_TAG", "`@Deprecated` element without a `@deprecated` tag saying what to use instead")
    if "{@inheritDoc}" in text and decl.kind != "method":
        emit(base, "ERROR", "INHERITDOC_PLACE", "`{@inheritDoc}` only works in method comments")
    if javac_ok or inherit_only:
        return
    # fallback structural checks when javac doclint is not available
    documented = [t[1] for t in tags if t[0] == "param"]
    expected = list(decl.params) + [f"<{t}>" for t in decl.tparams]
    for d in documented:
        if d not in expected:
            emit(base, "ERROR", "PARAM_UNKNOWN", f"`@param {d}` names no parameter of `{decl.name}`")
    for e in expected:
        if e not in documented:
            emit(base, "WARN", "PARAM_MISSING", f"no `@param {e}`")
    if decl.kind == "method":
        void = decl.returns.split()[-1] == "void" if decl.returns else True
        if void and "return" in names:
            emit(base, "ERROR", "RETURN_VOID", "`@return` on a void method")
        if not void and "return" not in names and "{@return" not in main:
            emit(base, "WARN", "RETURN_MISSING", "no `@return`")
    thrown = {t[1].split(".")[-1] for t in tags if t[0] in ("throws", "exception")}
    for t in decl.throws:
        if t not in thrown:
            emit(base, "WARN", "THROWS_MISSING", f"no `@throws {t}`")


def source_root(path, src):
    m = re.search(r"^\s*package\s+([\w.]+)\s*;", src, re.M)
    d = os.path.dirname(os.path.abspath(path))
    if not m:
        return d
    parts = m.group(1).split(".")
    for p in reversed(parts):
        if os.path.basename(d) != p:
            return os.path.dirname(os.path.abspath(path))
        d = os.path.dirname(d)
    return d


def run_doclint(files, package_level, classpath, custom):
    """Return (ran, {abspath: [(line, level, code, msg)]}, env_count)."""
    javac = shutil.which("javac")
    if not javac:
        return False, {}, 0
    roots = []
    for p in files:
        r = source_root(p, read(p))
        if r not in roots:
            roots.append(r)
    out = tempfile.mkdtemp(prefix="java-comment-cls-")
    level = "package" if package_level else "protected"
    cmd = [javac, f"-Xdoclint:all/{level}", "-Xmaxerrs", "100000", "-Xmaxwarns", "100000",
           "-proc:none", "-implicit:none", "-encoding", "UTF-8", "-d", out,
           "-sourcepath", os.pathsep.join(roots)]
    if classpath:
        cmd += ["-cp", classpath]
    cmd += [p for p in files if os.path.basename(p) != "module-info.java"]
    def diags(lint):
        c = list(cmd)
        c[1] = lint
        r = subprocess.run(c, capture_output=True, text=True)
        res = []
        for ln in (r.stdout + r.stderr).splitlines():
            m = re.match(r"(.+?\.java):(\d+): (error|warning): (.*)", ln)
            if m:
                res.append((os.path.abspath(m.group(1)), int(m.group(2)), m.group(3), m.group(4)))
        return res

    # Diagnostics that also appear without doclint come from the compiler (missing
    # dependencies, code errors), not from comments.
    compiler = set(diags("-Xdoclint:none"))
    shutil.rmtree(out, ignore_errors=True)
    found, env = {}, 0
    targets = {os.path.abspath(p) for p in files}
    for d in diags(cmd[1]):
        fp, line, sev, msg = d
        if fp not in targets:
            continue
        if d in compiler:
            env += 1
            continue
        tm = re.match(r"unknown tag: (\w+)", msg)
        if tm and tm.group(1) in custom:
            continue
        if msg.startswith("use of default constructor"):
            msg += " (fixing it needs a code change: propose it, don't add it)"
        level_name = "ERROR" if sev == "error" else "WARN"
        found.setdefault(fp, []).append((line, level_name, "DOCLINT", msg))
    return True, found, env


def cmd_lint(files, package_level, custom, classpath):
    ran, dl, env = run_doclint(files, package_level, classpath, custom)
    if not ran:
        print("SKIP doclint: javac not found; only this script's checks ran")
    elif env:
        print(f"NOTE doclint: {env} compiler diagnostic(s) not about comments were ignored "
              "(usually dependencies missing from the classpath); if `reference not found` "
              "points at a dependency type, pass --classpath")
    errors = 0
    for path in files:
        src = read(path)
        _, comments, masked = lex(src)
        decls = declarations(src, masked, comments, package_level)
        found = list(dl.get(os.path.abspath(path), []))

        def emit(line, level, code, msg):
            found.append((line, level, code, msg))

        attached = set()
        for d in decls:
            if d.doc:
                attached.add(d.doc[0])
                own_checks(path, src, d, emit, custom, ran)
        pd = package_doc(src, masked, comments, path)
        if pd:
            attached.add(pd[0])
        for c in comments:
            if c[3].startswith("/**") and not c[3].startswith("/**/") and c[0] not in attached:
                emit(c[2], "WARN", "ORPHAN_DOC", "javadoc ignores this doc comment: it is not directly "
                     "before a declaration (before its annotations); move it or make it `//`/`/* */`")
        for line, level, code, msg in sorted(set(found)):
            print(f"{path}:{line}: {level} {code}: {msg}")
            errors += level == "ERROR"
        if not found:
            print(f"OK {path}")
    return 1 if errors else 0


# ---------------------------------------------------------------- snapshot / check


def snapshot_path(base, path):
    return os.path.join(base, os.path.abspath(path).lstrip(os.sep))


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def cmd_check(files, base, rev):
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


GUARD = re.compile(r"^(?://|/\*)\s*(?:CHECKSTYLE:|NOSONAR|noinspection|@formatter:|\$NON-NLS|spotless:|CPD-)",
                   re.IGNORECASE)


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


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "lint", "snapshot", "check"):
        print(__doc__, file=sys.stderr)
        return 2
    mode, args = argv[1], argv[2:]
    package_level = "--package" in args
    args = [a for a in args if a != "--package"]
    custom, classpath, base, rev = set(), None, None, None
    rest = []
    k = 0
    while k < len(args):
        a = args[k]
        if a in ("--tags", "--classpath", "--base", "--rev") and k + 1 < len(args):
            v = args[k + 1]
            if a == "--tags":
                custom = {t.strip().lstrip("@") for t in v.split(",") if t.strip()}
            elif a == "--classpath":
                classpath = v
            elif a == "--base":
                base = v
            else:
                rev = v
            k += 2
            continue
        rest.append(a)
        k += 1
    files = [a for a in rest if a.endswith(".java")]
    if not files:
        print("no .java files given", file=sys.stderr)
        return 2
    missing = [f for f in files if not os.path.isfile(f)]
    if missing and mode != "check":
        print(f"not found: {' '.join(missing)}", file=sys.stderr)
        return 2
    if mode == "list":
        return cmd_list(files, package_level)
    if mode == "lint":
        return cmd_lint(files, package_level, custom, classpath)
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="java-comment-")
        for path in files:
            dest = snapshot_path(out, path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    if base is None and rev is None:
        print("check needs --base DIR or --rev REV", file=sys.stderr)
        return 2
    return cmd_check(files, base, rev)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
