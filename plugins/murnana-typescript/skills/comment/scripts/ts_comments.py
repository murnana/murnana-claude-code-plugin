#!/usr/bin/env python3
"""List, lint and guard comments in TypeScript files.

Usage:
  ts_comments.py list [--internal] FILE...
        Print every comment as `file:line: KIND: text`, then every API declaration
        without a doc comment as `file:line: UNDOCUMENTED: <kind> <name>`.
        API = exported declarations (all top-level ones in a .d.ts without exports),
        and the non-private members of exported classes and interfaces.
        --internal also counts non-exported top-level declarations as API.
  ts_comments.py lint [--internal] [--tags a,b] FILE...
        Check TSDoc comments. Prints `file:line: ERROR|WARN CODE: message`, or
        `OK file`. Exit 1 if any ERROR. Custom tags come from --tags and from the
        nearest tsdoc.json; TypeDoc tags are allowed when the nearest package.json
        depends on typedoc. When the project has @microsoft/tsdoc installed and
        `node` is on PATH, its parser also runs (lines tagged TSDOC).
  ts_comments.py snapshot FILE...
        Copy FILEs to a new temporary directory and print its path. Run before editing.
  ts_comments.py check --base DIR FILE...   (or --rev REV)
        Exit 1 if any file's code (everything except comments and whitespace)
        differs from its copy in DIR (or in git revision REV).

Comment KIND: DOC (/** */ attached to a declaration), ORPHAN_DOC (/** */ attached to
nothing), DIRECTIVE (tool directive: @ts-*, eslint-*, prettier-ignore, triple-slash,
#__PURE__, ...), LICENSE (/*! ... */, @license, copyright header), TODO, FIXME,
LINE (//), BLOCK (/* */). The lexer understands strings, template literals (with
${} nesting) and regex literals, so "//" inside them is not taken for a comment.
Declarations are found line by line, so code formatted one declaration per line
(Prettier, Biome, dprint output) is parsed best.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

EXTS = (".ts", ".tsx", ".mts", ".cts")

# ---------------------------------------------------------------- lexer

REGEX_AFTER_WORDS = {"return", "typeof", "case", "do", "else", "in", "of", "new", "delete",
                     "void", "throw", "instanceof", "yield", "await", "extends", "keyof"}
IDENT = r"[A-Za-z_$\u0080-\uffff][\w$\u0080-\uffff]*"
TOKEN_RE = re.compile(IDENT + r"|\d[\w.]*|\S")


def lex(src, tsx=False):
    """Return (tokens, comments, masked).

    tokens: code tokens with comments removed; each string, template or regex
            literal is one exact token.
    comments: list of (start, end, line, text).
    masked: src with comments and literal bodies replaced by spaces (newlines and
            the quote characters kept).
    """
    n = len(src)
    masked = list(src)
    comments = []
    tokens = []
    prev = ""  # previous significant token, for the regex-or-division decision
    tmpl = []  # brace depth inside each open ${ ... }

    def blank(a, b):
        for k in range(a, b):
            if masked[k] != "\n":
                masked[k] = " "

    def line_at(p):
        return src.count("\n", 0, p) + 1

    def scan_template(i):
        """i is just after ` or after the } closing ${...}. Return (end, opened_expr)."""
        k = i
        while k < n:
            c = src[k]
            if c == "\\":
                k += 2
                continue
            if c == "`":
                return k + 1, False
            if src.startswith("${", k):
                return k + 2, True
            k += 1
        return n, False

    i = 0
    if src.startswith("#!"):
        j = src.find("\n")
        j = n if j == -1 else j
        comments.append((0, j, 1, src[:j]))
        blank(0, j)
        i = j
    while i < n:
        c = src[i]
        if c in " \t\r\n\f\v\ufeff":
            i += 1
            continue
        if src.startswith("//", i) and not (tsx and i > 0 and src[i - 1] == ":"):
            j = src.find("\n", i)
            j = n if j == -1 else j
            comments.append((i, j, line_at(i), src[i:j]))
            blank(i, j)
            i = j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            comments.append((i, j, line_at(i), src[i:j]))
            blank(i, j)
            i = j
            continue
        if c in "'\"" and not (i > 0 and (src[i - 1].isalnum())):
            k = i + 1
            while k < n and src[k] != c and src[k] != "\n":
                k += 2 if src[k] == "\\" else 1
            k = min(k + 1, n)
            tokens.append(src[i:k])
            blank(i + 1, k - 1)
            prev = "lit"
            i = k
            continue
        if c == "`":
            k, opened = scan_template(i + 1)
            tokens.append(src[i:k])
            blank(i + 1, k - (2 if opened else 1))
            if opened:
                tmpl.append(0)
            prev = "lit"
            i = k
            continue
        if c == "}" and tmpl and tmpl[-1] == 0:
            tmpl.pop()
            k, opened = scan_template(i + 1)
            tokens.append(src[i:k])
            blank(i + 1, k - (2 if opened else 1))
            if opened:
                tmpl.append(0)
            prev = "lit"
            i = k
            continue
        if c == "/":
            regex_ok = prev == "" or (not re.match(r"[\w$)\]}]", prev[-1]) and prev != "lit") \
                or prev in REGEX_AFTER_WORDS
            if regex_ok:
                k, in_class = i + 1, False
                while k < n and src[k] != "\n":
                    if src[k] == "\\":
                        k += 2
                        continue
                    if src[k] == "[":
                        in_class = True
                    elif src[k] == "]":
                        in_class = False
                    elif src[k] == "/" and not in_class:
                        break
                    k += 1
                if k < n and src[k] == "/":
                    k += 1
                    while k < n and (src[k].isalnum()):
                        k += 1
                    tokens.append(src[i:k])
                    blank(i + 1, k)
                    prev = "lit"
                    i = k
                    continue
        m = TOKEN_RE.match(src, i)
        tok = m.group(0)
        if tmpl:
            if tok == "{":
                tmpl[-1] += 1
            elif tok == "}":
                tmpl[-1] -= 1
        tokens.append(tok)
        prev = tok
        i = m.end()
    return tokens, comments, "".join(masked)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def line_of(src, pos):
    return src.count("\n", 0, pos) + 1


def short(text, limit=100):
    t = " ".join(text.split())
    return t if len(t) <= limit else t[:limit - 3] + "..."


# ---------------------------------------------------------------- declarations

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def match_close(s, i):
    """Index just after the bracket that closes s[i] (masked text), or len(s)."""
    open_c, close_c = s[i], PAIRS[s[i]]
    depth, k = 0, i
    while k < len(s):
        ch = s[k]
        if ch == open_c:
            depth += 1
        elif ch == close_c and not (close_c == ">" and k > 0 and s[k - 1] == "="):
            depth -= 1
            if depth == 0:
                return k + 1
        elif open_c == "<" and ch in ";{":
            return k
        k += 1
    return len(s)


def split_top(text, sep=","):
    parts, depth, buf = [], 0, []
    for k, ch in enumerate(text):
        if ch in "([{<":
            depth += 1
        elif ch in ")]}" or (ch == ">" and not (k > 0 and text[k - 1] == "=")):
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf))
    return parts


def parse_params(text):
    names = []
    for p in split_top(text):
        p = re.sub(r"@\w+(\([^)]*\))?\s*", "", p).strip()
        p = re.sub(r"^((public|private|protected|readonly|override)\s+)+", "", p)
        p = p.lstrip(".").strip()
        m = re.match(IDENT, p)
        if m:
            if m.group(0) != "this":
                names.append(m.group(0))
        elif p:
            names.append("")  # destructured: any @param name is accepted
    return names


def parse_type_params(text):
    out = []
    for p in split_top(text):
        p = re.sub(r"^\s*(const|in|out)\s+", "", p.strip())
        m = re.match(IDENT, p)
        if m:
            out.append(m.group(0))
    return out


class Decl:
    def __init__(self, **kw):
        self.__dict__.update(kw)


TOP_RE = re.compile(
    r"^([ \t]*)((?:export\s+(?:default\s+)?)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?)"
    r"(function\s*\*?|class|interface|type|const\s+enum|enum|const|let|var|namespace|module)"
    r"\s*(" + IDENT + r")?", re.M)
MEMBER_RE = re.compile(
    r"^([ \t]*)((?:(?:public|protected|private|static|readonly|abstract|override|declare|"
    r"async|accessor|get|set)\s+)*)(\*?\s*)(#?" + IDENT + r"|\[[^\]\n]*\]|'[^'\n]*'|\"[^\"\n]*\")"
    r"\s*([?!])?\s*(<|\(|:|=|;|,|$)", re.M)
SIG_RE = re.compile(r"^([ \t]*)(new\s*)?(<[^\n]*?>\s*)?\(", re.M)
KEYWORDS = {"if", "for", "while", "switch", "return", "throw", "case", "default", "else",
            "do", "try", "catch", "finally", "break", "continue", "import", "export",
            "await", "yield", "delete", "typeof", "void", "super", "this", "new"}


def blocks_of(masked):
    """Map each '{' index to its matching '}' index, and depth at each index."""
    stack, pairs = [], {}
    depth = [0] * (len(masked) + 1)
    d = 0
    for k, ch in enumerate(masked):
        if ch == "{":
            stack.append(k)
            d += 1
        elif ch == "}":
            if stack:
                pairs[stack.pop()] = k
            d = max(0, d - 1)
        depth[k + 1] = d
    return pairs, depth


def signature_after(masked, k):
    """From k (just after a name), parse optional <T>, (params) and return type.
    Return (tparams, params or None, return_type or None, end_index)."""
    n = len(masked)

    def skip_ws(p):
        while p < n and masked[p] in " \t\r\n":
            p += 1
        return p

    k = skip_ws(k)
    tparams = []
    if k < n and masked[k] == "<":
        e = match_close(masked, k)
        tparams = parse_type_params(masked[k + 1:e - 1])
        k = skip_ws(e)
    if k >= n or masked[k] != "(":
        return tparams, None, None, k
    e = match_close(masked, k)
    params = parse_params(masked[k + 1:e - 1])
    k = skip_ws(e)
    ret = None
    if k < n and masked[k] == ":":
        p = skip_ws(k + 1)
        start, depth = p, 0
        while p < n:
            ch = masked[p]
            if ch in "([<" or (ch == "{" and (depth > 0 or p == start)):
                depth += 1
            elif ch in ")]" or (ch == ">" and masked[p - 1] != "=") or (ch == "}" and depth > 0):
                depth -= 1
            elif depth == 0 and (ch in "{;" or masked.startswith("=>", p) or ch == "\n" and
                                 masked[start:p].strip() and not masked[start:p].rstrip().endswith(("|", "&", ",", "<", "=>"))):
                break
            p += 1
        ret = " ".join(masked[start:p].split())
        k = p
    return tparams, params, ret, k


def declarations(path, src, masked, internal=False):
    """Return a list of Decl for top-level declarations and class/interface members."""
    pairs, depth = blocks_of(masked)
    dts = path.endswith((".d.ts", ".d.mts", ".d.cts"))
    has_export = re.search(r"^\s*export\b", masked, re.M) is not None
    decls = []
    containers = []  # (open, close, decl)
    namespaces = []  # (open, close, visible)

    def ns_visible(pos):
        vis = True
        for o, c, v in namespaces:
            if o < pos < c:
                vis = vis and v
        return vis

    def in_ns(pos):
        return any(o < pos < c for o, c, _ in namespaces)

    # top-level and namespace-level declarations
    for m in TOP_RE.finditer(masked):
        pos = m.start(2) if m.group(2) else m.start(3)
        d_here = depth[pos]
        ns_depth = sum(1 for o, c, _ in namespaces if o < pos < c)
        if d_here != ns_depth:
            continue
        mods, kw, name = m.group(2), " ".join(m.group(3).split()), m.group(4) or ""
        if kw.startswith("function"):
            kw = "function"
        exported = "export" in mods
        if not name and "default" in mods:
            name = "default"
        if not name:
            continue
        visible = exported or internal or (dts and not has_export) or (in_ns(pos) and exported)
        if in_ns(pos):
            visible = (exported or internal) and ns_visible(pos)
        after = m.end(4) if m.group(4) else m.end(3)
        tparams, params, ret, end = [], None, None, after
        kind = kw
        if kw == "function":
            tparams, params, ret, end = signature_after(masked, after)
        elif kw in ("const", "let", "var"):
            # arrow function or function expression assigned to a variable
            mm = re.compile(r"\s*(?::[^=\n]*)?=\s*(?:async\s+)?(?:function\b\s*\*?\s*(?:" + IDENT +
                            r")?\s*)?(?=[<(])").match(masked, after)
            if mm:
                tparams, params, ret, end = signature_after(masked, mm.end())
                if params is not None:
                    kind = "function"
            if kind != "function":
                kind = "variable"
        elif kw in ("class", "interface"):
            tparams, _, _, _ = signature_after(masked, after)
        elif kw == "type":
            tparams, _, _, _ = signature_after(masked, after)
        decl = Decl(kind=kind, name=name, line=line_of(src, pos), start=pos, visible=visible,
                    params=params, tparams=tparams, returns=ret, static=False, override=False,
                    private=False, container=None, has_body=False, doc=None, exported=exported)
        # find the body block for containers
        if kw in ("class", "interface", "namespace", "module", "enum", "const enum"):
            b = masked.find("{", after)
            if b != -1 and b in pairs:
                if kw in ("namespace", "module"):
                    namespaces.append((b, pairs[b], visible))
                elif kw in ("class", "interface"):
                    containers.append((b, pairs[b], decl))
                else:
                    containers.append((b, pairs[b], decl))
        if kind == "function":
            nxt = masked[end:end + 3].lstrip()[:1]
            decl.has_body = nxt in ("{", "=") or kw in ("const", "let", "var")
        decls.append(decl)

    # members of classes, interfaces and enums
    for o, c, owner in containers:
        body_depth = depth[o + 1]
        region = masked[o + 1:c]
        member_vis = owner.visible
        if "enum" in owner.kind:
            off = 0
            for part in split_top(region):
                mm = re.match(r"\s*(" + IDENT + r"|'[^'\n]*'|\"[^\"\n]*\")", part)
                if mm:
                    pos = o + 1 + off + mm.start(1)
                else:
                    pos = None
                off += len(part) + 1
                if pos is None:
                    continue
                decls.append(Decl(kind="enum member", name=mm.group(1).strip("'\""), line=line_of(src, pos),
                                  start=pos, visible=member_vis, params=None, tparams=[], returns=None,
                                  static=True, override=False, private=False, container=owner,
                                  has_body=False, doc=None, exported=False))
            continue
        seen_names = set()
        for mm in MEMBER_RE.finditer(region):
            pos = o + 1 + mm.start(2) if mm.group(2) else o + 1 + mm.start(4)
            if depth[pos] != body_depth:
                continue
            mods = mm.group(2).split()
            name = mm.group(4)
            if name in KEYWORDS and not mods:
                continue
            # a modifier word alone followed by ( or : is the member name itself
            private = "private" in mods or name.startswith("#")
            is_ctor = name == "constructor"
            nxt = mm.group(6)
            after = o + 1 + mm.end(5) if mm.group(5) else o + 1 + mm.start(6)
            kind = "property"
            tparams, params, ret, end = [], None, None, after
            if nxt in ("<", "("):
                tparams, params, ret, end = signature_after(masked, after)
                if params is not None:
                    kind = "constructor" if is_ctor else "method"
                    if "get" in mods:
                        kind = "getter"
                    elif "set" in mods:
                        kind = "setter"
            elif nxt == ":":
                # property whose type is a function type stays a property
                kind = "property"
            key = (name, "static" in mods)
            accessor_pair = kind in ("getter", "setter") and key in seen_names
            has_body = masked[end:end + 2].lstrip()[:1] == "{"
            overload_follow = kind == "method" and key in seen_names and has_body
            seen_names.add(key)
            d = Decl(kind=kind, name=name, line=line_of(src, pos), start=pos,
                     visible=member_vis and not private and not accessor_pair and not overload_follow,
                     params=params, tparams=tparams, returns=ret, static="static" in mods,
                     override="override" in mods, private=private, container=owner,
                     has_body=masked[end:end + 2].lstrip()[:1] == "{", doc=None, exported=False)
            if is_ctor and params is not None:
                d.kind = "constructor"
                d.name = "constructor"
            decls.append(d)
        if owner.kind == "interface":
            for mm in SIG_RE.finditer(region):
                pos = o + 1 + mm.start(0) + len(mm.group(1))
                if depth[pos] != body_depth:
                    continue
                k = o + 1 + mm.end(0) - 1
                tparams, params, ret, _ = signature_after(masked, k)
                decls.append(Decl(kind="construct signature" if mm.group(2) else "call signature",
                                  name="new" if mm.group(2) else "call", line=line_of(src, pos),
                                  start=pos, visible=member_vis, params=params, tparams=tparams,
                                  returns=ret, static=False, override=False, private=False,
                                  container=owner, has_body=False, doc=None, exported=False))
    # top-level function overloads: the implementation signature gets no doc comment
    seen = {}
    for d in decls:
        if d.kind == "function" and d.container is None:
            key = d.name
            if key in seen and d.has_body:
                d.visible = False
                d.overload_of = seen[key]
            seen.setdefault(key, d)
    decls.sort(key=lambda d: d.start)
    return decls


DIRECTIVE_RE = re.compile(
    r"^(//\s*@ts-|/\*\s*@ts-|//\s*(eslint|tslint|jshint|biome-ignore|prettier-ignore|deno-lint|"
    r"deno-fmt|dprint-ignore|noinspection|istanbul|c8|v8|cspell|spell-checker|stylelint|global\b|"
    r"#region|#endregion|region\b|endregion\b|@ts-|@jsx|@vitest-|@jest-)|/\*\s*(eslint|tslint|jshint|"
    r"istanbul|c8|v8|global\b|prettier-ignore|biome-ignore|webpack|@vite-ignore|@__PURE__|#__PURE__|"
    r"@__NO_SIDE_EFFECTS__|#__NO_SIDE_EFFECTS__|@jsx|@ts-|cspell)|///\s*<(reference|amd)|#!)", re.I)


def attach_docs(src, masked, comments, decls):
    """Set decl.doc for each declaration; return the set of attached comment starts
    and the start of a @packageDocumentation comment (or None)."""
    by_start = {d.start: d for d in decls}
    attached, pkg = set(), None
    n = len(masked)
    for idx, c in enumerate(comments):
        text = c[3]
        if not text.startswith("/**") or text.startswith("/**/"):
            continue
        if "@packageDocumentation" in text or "@module" in text and idx == 0:
            attached.add(c[0])
            pkg = c[0]
            continue
        k = c[1]
        # skip whitespace and decorators
        while True:
            while k < n and masked[k] in " \t\r\n":
                k += 1
            if k < n and masked[k] == "@":
                mm = re.compile(r"@" + IDENT + r"(\." + IDENT + r")*").match(masked, k)
                if not mm:
                    break
                k = mm.end()
                if k < n and masked[k] == "(":
                    k = match_close(masked, k)
                continue
            break
        # another doc comment in between means this one is not the attached one
        nxt = comments[idx + 1] if idx + 1 < len(comments) else None
        if nxt and nxt[0] < k and nxt[3].startswith("/**"):
            continue
        d = by_start.get(k)
        if d is None:
            # declaration starting later on the same token run, e.g. `export` handled by TOP_RE
            for dd in decls:
                if dd.start >= k and masked[k:dd.start].strip() == "":
                    d = dd
                    break
        if d is not None:
            d.doc = c
            attached.add(c[0])
        elif re.match(r"\s*(export\s|declare\s|abstract\s|async\s|function\b|class\b|interface\b|type\b|"
                      r"enum\b|const\b|let\b|var\b|namespace\b|module\b|public\b|protected\b|"
                      r"private\b|static\b|readonly\b|get\b|set\b|constructor\b|#" + IDENT + r"|" + IDENT + r"\s*[?!]?\s*:)",
                      masked[k:k + 200]):
            attached.add(c[0])  # documents something not tracked as API (locals, private members)
    return attached, pkg


def kind_of(text, first_code):
    if DIRECTIVE_RE.match(text):
        return "DIRECTIVE"
    if text.startswith("/*!") or "@license" in text or "@preserve" in text or \
            (first_code and re.search(r"copyright|\(c\)|©|spdx-license", text, re.I)):
        return "LICENSE"
    body = text.lstrip("/*! ").upper()
    if body.startswith("TODO") or re.match(r"(//|/\*)\s*TODO\b", text):
        return "TODO"
    if body.startswith(("FIXME", "XXX", "HACK")):
        return "FIXME"
    return "LINE" if text.startswith("//") else "BLOCK"


# ---------------------------------------------------------------- list


def is_tsx(path):
    return path.endswith(".tsx")


def cmd_list(files, internal):
    for path in files:
        src = read(path)
        _, comments, masked = lex(src, is_tsx(path))
        decls = declarations(path, src, masked, internal)
        attached, pkg = attach_docs(src, masked, comments, decls)
        first_code = len(masked) - len(masked.lstrip())
        for c in comments:
            text = c[3]
            if text.startswith("/**") and not text.startswith("/**/"):
                kind = "DOC" if c[0] in attached else "ORPHAN_DOC"
                if "@license" in text or "@preserve" in text:
                    kind = "LICENSE"
            else:
                kind = kind_of(text, c[0] <= first_code)
            print(f"{path}:{c[2]}: {kind}: {short(text)}")
        for d in decls:
            if not d.visible or d.doc or d.override:
                continue
            owner = f"{d.container.name}." if d.container is not None else ""
            print(f"{path}:{d.line}: UNDOCUMENTED: {d.kind} {owner}{d.name}")
    return 0


# ---------------------------------------------------------------- lint

TSDOC_TAGS = {
    # block tags
    "param", "typeParam", "returns", "remarks", "example", "throws", "see", "deprecated",
    "defaultValue", "privateRemarks", "decorator", "jsx", "jsxRuntime", "jsxFrag",
    "jsxImportSource",
    # modifier tags
    "alpha", "beta", "experimental", "internal", "public", "readonly", "sealed", "virtual",
    "override", "eventProperty", "packageDocumentation",
    # inline tags
    "link", "inheritDoc", "label",
}
TYPEDOC_TAGS = {"category", "categoryDescription", "group", "groupDescription", "module",
                "hidden", "ignore", "since", "author", "document", "enum", "event", "expand",
                "hideconstructor", "import", "inline", "interface", "namespace", "overload",
                "primaryExport", "private", "protected", "showCategories", "showGroups",
                "hideCategories", "hideGroups", "sortStrategy", "summary", "useDeclaredType",
                "class", "function", "linkcode", "linkplain", "include", "includeCode",
                "mergeModuleWith", "disableGroups", "abstract", "license", "preventExpand",
                "preventInline", "property", "prop", "satisfies", "this", "type", "typedef",
                "template", "callback", "categoryDescription"}
JSDOC_SUGGEST = {
    "return": "@returns", "arg": "@param", "argument": "@param", "exception": "@throws",
    "template": "@typeParam", "default": "@defaultValue", "desc": "the summary",
    "description": "the summary", "summary": "the summary paragraph", "type": "the TypeScript type",
    "typedef": "a TypeScript `type`", "callback": "a TypeScript function type",
    "function": "nothing (TypeScript knows)", "func": "nothing (TypeScript knows)",
    "method": "nothing (TypeScript knows)", "class": "nothing (TypeScript knows)",
    "constructor": "nothing (TypeScript knows)", "extends": "nothing (TypeScript knows)",
    "augments": "nothing (TypeScript knows)", "implements": "nothing (TypeScript knows)",
    "memberof": "nothing (TypeScript knows)", "private": "the `private` modifier or @internal",
    "protected": "the `protected` modifier", "access": "a TypeScript modifier or @internal",
    "const": "nothing (TypeScript knows)", "constant": "nothing (TypeScript knows)",
    "enum": "nothing (TypeScript knows)", "async": "nothing (TypeScript knows)",
    "static": "nothing (TypeScript knows)", "abstract": "the `abstract` modifier",
    "property": "a doc comment on the property itself", "prop": "a doc comment on the property itself",
    "since": "@remarks text, or register the tag in tsdoc.json", "author": "the commit log",
    "version": "package.json", "todo": "a `// TODO(#issue): ...` comment", "fires": "@eventProperty",
    "throw": "@throws", "returns": None, "yields": "@returns", "yield": "@returns",
    "module": "@packageDocumentation", "file": "@packageDocumentation",
    "fileoverview": "@packageDocumentation", "overview": "@packageDocumentation",
    "ignore": "@internal", "hidden": "@internal", "inheritdoc": "{@inheritDoc}",
    "link": "{@link ...} (inline, inside braces)", "linkcode": "{@link ...}", "linkplain": "{@link ...}",
}
NON_REPEATABLE = {"remarks", "returns", "deprecated", "defaultValue", "privateRemarks", "example_none"}
MEANINGS = {"class", "interface", "type", "enum", "namespace", "function", "var", "constructor",
            "member", "event", "call", "new", "index", "complex"}
GLOBALS = {"Array", "ArrayBuffer", "AsyncIterable", "AsyncIterableIterator", "AsyncIterator",
           "AsyncGenerator", "BigInt", "Boolean", "DataView", "Date", "Error", "EvalError",
           "Function", "Generator", "Infinity", "Intl", "Iterable", "IterableIterator", "Iterator",
           "JSON", "Map", "Math", "NaN", "Number", "Object", "Promise", "PromiseLike", "Proxy",
           "RangeError", "ReadonlyArray", "ReadonlyMap", "ReadonlySet", "ReferenceError", "Reflect",
           "RegExp", "Set", "SharedArrayBuffer", "String", "Symbol", "SyntaxError", "TypeError",
           "URIError", "Uint8Array", "Int8Array", "Uint16Array", "Int16Array", "Uint32Array",
           "Int32Array", "Float32Array", "Float64Array", "BigInt64Array", "BigUint64Array",
           "WeakMap", "WeakSet", "WeakRef", "AggregateError", "Record", "Partial", "Required",
           "Readonly", "Pick", "Omit", "Exclude", "Extract", "NonNullable", "Parameters",
           "ReturnType", "InstanceType", "Awaited", "AbortController", "AbortSignal", "URL",
           "URLSearchParams", "Request", "Response", "Headers", "fetch", "console", "globalThis",
           "Event", "EventTarget", "Element", "HTMLElement", "Document", "Window", "Node", "Buffer",
           "TextEncoder", "TextDecoder", "Blob", "File", "FormData", "ReadableStream",
           "WritableStream", "structuredClone", "setTimeout", "setInterval", "queueMicrotask"}
STOP = {"the", "a", "an", "this", "of", "returns", "return", "gets", "get", "sets", "set", "is",
        "checks", "whether", "if", "value", "for", "to", "function", "method", "class", "property",
        "interface", "type", "given", "specified", "new", "creates", "create"}


def find_up(start, names):
    d = os.path.dirname(os.path.abspath(start))
    while True:
        for nm in names:
            p = os.path.join(d, nm)
            if os.path.isfile(p):
                return p
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def project_tags(path):
    """Return (extra tag names, notes) from tsdoc.json and package.json near path."""
    extra, notes = set(), []
    tj = find_up(path, ["tsdoc.json"])
    if tj:
        try:
            data = json.loads(read(tj))
            for t in data.get("tagDefinitions", []):
                extra.add(t.get("tagName", "").lstrip("@"))
            for k, v in (data.get("supportForTags") or {}).items():
                if v:
                    extra.add(k.lstrip("@"))
            notes.append(f"tsdoc.json ({os.path.relpath(tj)})")
        except (ValueError, OSError):
            notes.append(f"tsdoc.json unreadable ({os.path.relpath(tj)})")
    pj = find_up(path, ["package.json"])
    if pj:
        try:
            data = json.loads(read(pj))
            deps = {}
            for key in ("dependencies", "devDependencies", "peerDependencies"):
                deps.update(data.get(key) or {})
            if "typedoc" in deps or find_up(path, ["typedoc.json", "typedoc.jsonc"]):
                extra |= TYPEDOC_TAGS
                notes.append("typedoc tags")
        except (ValueError, OSError):
            pass
    return extra, notes


def doc_lines(text):
    body = text[3:-2] if text.endswith("*/") else text[3:]
    out = []
    for ln in body.split("\n"):
        s = ln.strip()
        out.append(re.sub(r"^\s*\* ?", "", ln, count=1) if s.startswith("*") else s)
    return out


def mask_code(lines):
    """Return lines with fenced code blocks and `code spans` blanked out."""
    out, fence = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            fence = not fence
            out.append(" " * len(ln))
            continue
        if fence:
            out.append(" " * len(ln))
            continue
        out.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), ln))
    return out


def camel_words(name):
    return {w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)}


def check_reference(ref, src_names, classes, emit, line):
    """Validate a declaration reference (the part of {@link} before |)."""
    ref = ref.strip()
    if not ref or re.match(r"[a-z][a-z0-9+.-]*://", ref, re.I):
        return
    # split off module source at the first ! outside quotes/brackets
    k, q, depth, bang = 0, False, 0, -1
    while k < len(ref):
        ch = ref[k]
        if ch == "\\" and q:
            k += 2
            continue
        if ch == '"':
            q = not q
        elif not q and ch == "[":
            depth += 1
        elif not q and ch == "]":
            depth -= 1
        elif not q and depth == 0 and ch == "!" and bang == -1:
            bang = k
        k += 1
    if q or depth != 0:
        emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: unbalanced quotes or brackets")
        return
    module, path = (ref[:bang], ref[bang + 1:]) if bang != -1 else (None, ref)
    if module is not None and module.startswith('"') and not module.endswith('"'):
        emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: unterminated module source")
        return
    local = path.startswith("~")
    if local:
        path = path[1:]
    meaning = None
    mm = re.search(r":(\w+(\(\d+\))?|\(\d+\)|\d+)$", path)
    if mm:
        meaning = mm.group(1)
        path = path[:mm.start()]
        kw = re.match(r"[a-z]+", meaning)
        if kw and kw.group(0) not in MEANINGS:
            emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: unknown meaning `:{kw.group(0)}` "
                 f"(use one of {', '.join(sorted(MEANINGS))})")
    elif ":" in re.sub(r'"[^"]*"|\[[^\]]*\]', "", path):
        emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: `:` must be followed by a meaning keyword or overload index")
        return
    # components
    comps, k, cur, sep = [], 0, "", ""
    q, depth = False, 0
    while k < len(path):
        ch = path[k]
        if ch == "\\" and q:
            cur += path[k:k + 2]
            k += 2
            continue
        if ch == '"':
            q = not q
        elif not q and ch == "[":
            depth += 1
        elif not q and ch == "]":
            depth -= 1
        if not q and depth == 0 and ch in ".#~":
            comps.append((sep, cur))
            sep, cur = ch, ""
        else:
            cur += ch
        k += 1
    comps.append((sep, cur))
    for s, comp in comps:
        if comp.startswith('"') or comp.startswith("["):
            continue
        if not comp and (path or module is None):
            emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: empty component (doubled or trailing `.`, `#` or `~`)")
            return
        bad = re.search(r"[\s\"{}()\[\]!.#~:,@]", comp)
        if bad:
            emit(line, "ERROR", "LINK_SYNTAX", f"`{ref}`: `{comp}` contains `{bad.group(0)}`; "
                 f"quote the name (\"...\")")
            return
    if module is not None or not comps or not comps[0][1]:
        return
    head = comps[0][1].strip('"')
    if head not in src_names and head not in GLOBALS:
        emit(line, "WARN", "LINK_UNRESOLVED", f"`{ref}`: `{head}` is not declared or imported in this "
             "file; confirm it exists (LSP workspaceSymbol or Grep), or add a module source (`pkg!Name`)")
        return
    if len(comps) >= 2 and head in classes:
        sep, member = comps[1][0], comps[1][1].strip('"')
        info = classes[head]
        if member in info["instance"] and sep == ".":
            emit(line, "WARN", "LINK_NAVIGATION", f"`{ref}`: `{member}` is an instance member; use `{head}#{member}`")
        elif member in info["static"] and sep == "#":
            emit(line, "WARN", "LINK_NAVIGATION", f"`{ref}`: `{member}` is static; use `{head}.{member}`")
        elif info["kind"] in ("enum", "namespace") and sep == "#":
            emit(line, "WARN", "LINK_NAVIGATION", f"`{ref}`: members of {info['kind']} `{head}` use `.`")
        elif member not in info["instance"] and member not in info["static"] and not member.startswith("["):
            emit(line, "WARN", "LINK_UNRESOLVED", f"`{ref}`: `{head}` has no member `{member}` in this file")


def names_in_file(masked, decls):
    names = {d.name for d in decls if d.container is None}
    for m in TOP_RE.finditer(masked):
        if m.group(4):
            names.add(m.group(4))
    for m in re.finditer(r"\bimport\s+(type\s+)?([^;]*?)\s+from\b", masked, re.S):
        clause = m.group(2)
        for nm in re.findall(r"(?:\bas\s+)?(" + IDENT + r")", re.sub(r"\b\w+\s+as\s+", "", clause)):
            if nm not in ("type", "as"):
                names.add(nm)
    for m in re.finditer(r"\bimport\s+(" + IDENT + r")\s*=", masked):
        names.add(m.group(1))
    return names


def class_members(decls):
    out = {}
    for d in decls:
        if d.container is None and d.kind in ("class", "interface", "enum", "const enum"):
            out.setdefault(d.name, {"kind": "enum" if "enum" in d.kind else d.kind,
                                    "instance": set(), "static": set()})
        if d.container is not None and d.container.name in out:
            info = out[d.container.name]
            if d.kind == "constructor":
                continue
            (info["static"] if d.static else info["instance"]).add(d.name.lstrip("#"))
    return out


def own_checks(decl, emit, allowed, src_names, classes, legacy=False):
    c = decl.doc
    text = c[3]
    base = c[2]
    raw = doc_lines(text)
    lines = mask_code(raw)
    # block tags and summary
    tags = []  # (tag, rest, line_offset)
    summary_lines = []
    for k, ln in enumerate(lines):
        m = re.match(r"\s*@(\w+)\b(.*)", ln)
        if m:
            tags.append([m.group(1), raw[k].strip()[len(m.group(1)) + 1:].strip(), k])
        elif tags:
            tags[-1][1] += "\n" + raw[k]
        else:
            summary_lines.append(raw[k])
    summary = "\n".join(summary_lines).strip()
    whole = "\n".join(lines)
    inherit_only = bool(re.fullmatch(r"\s*\{@inheritDoc[^}]*\}\s*", summary)) and not \
        [t for t in tags if t[0] not in ("override", "public", "beta", "alpha", "internal")]
    # unknown and JSDoc-style tags, anywhere outside code
    for k, ln in enumerate(lines):
        ln = re.sub(r"(\{@\w+)[^}]*\}", r"\1}", ln)  # inline tag bodies are not tags
        for m in re.finditer(r"(?<![\w\\{])@(\w+)|\{@(\w+)", ln):
            tag = m.group(1) or m.group(2)
            if tag in TSDOC_TAGS or tag in allowed:
                continue
            sug = JSDOC_SUGGEST.get(tag) or JSDOC_SUGGEST.get(tag.lower())
            if sug:
                emit(base + k, "WARN", "JSDOC_TAG", f"`@{tag}` is JSDoc, not TSDoc; use {sug}")
            else:
                emit(base + k, "WARN", "TAG_UNKNOWN", f"`@{tag}` is not a TSDoc tag; remove it, write it as "
                     "text (`\\@` or a code span), or register it in tsdoc.json")
    # inline tags: closed, and their references
    for k, ln in enumerate(lines):
        for m in re.finditer(r"\{@(\w+)", ln):
            close = ln.find("}", m.end())
            if close == -1:
                emit(base + k, "ERROR", "INLINE_UNCLOSED", f"`{{@{m.group(1)}` is not closed with `}}` on the same line")
                continue
            if m.group(1) in ("link", "linkcode", "linkplain", "inheritDoc"):
                body = ln[m.end():close].strip()
                target = body.split("|", 1)[0].strip()
                if m.group(1) == "inheritDoc" and not target:
                    continue
                if not target:
                    emit(base + k, "ERROR", "LINK_SYNTAX", f"`{{@{m.group(1)}}}` has no target")
                    continue
                if legacy:
                    head = re.match(IDENT + r"$", target.split(".")[0])
                    if "#" not in target and head and head.group(0) not in src_names \
                            and head.group(0) not in GLOBALS:
                        emit(base + k, "WARN", "LINK_UNRESOLVED", f"`{target}`: `{head.group(0)}` is not "
                             "declared or imported in this file; confirm it exists")
                else:
                    check_reference(target, src_names, classes, emit, base + k)
        stripped = re.sub(r"\{@\w+[^}]*\}|^\s*@\w+\s*\{[^}]*\}", "", ln)
        if re.search(r"(?<!\\)[{}]", stripped):
            emit(base + k, "WARN", "ESCAPE", "a bare `{` or `}` in text; put code in backticks or escape it as `\\{` `\\}`")
    # summary
    if not summary and not inherit_only and decl is not None:
        emit(base, "WARN", "SUMMARY_MISSING", "no summary paragraph before the first block tag")
    first = re.split(r"(?<=[.。])\s", summary, maxsplit=1)[0] if summary else ""
    if first and decl.kind not in ("constructor",):
        words = {re.sub(r"(?<=[a-z]{3})(es|s)$", "", w.lower())
                 for w in re.findall(r"[A-Za-z]+", re.sub(r"\{@\w+\s*([^}|]*)[^}]*\}", r"\1", first))}
        nw = camel_words(decl.name.lstrip("#"))
        if words and nw and words - STOP <= nw and len(words) <= len(nw) + 3:
            emit(base, "WARN", "SUMMARY_RESTATES", f"summary only restates the name `{decl.name}`; say what the name can't")
    names = [t[0] for t in tags]
    for t in set(names):
        if t in NON_REPEATABLE and names.count(t) > 1:
            emit(base, "WARN", "DUPLICATE_TAG", f"`@{t}` appears {names.count(t)} times")
    # per-tag checks
    documented, tdocumented = [], []
    for tag, rest, off in tags:
        line = base + off
        first_line = rest.split("\n", 1)[0]
        if tag in ("param", "typeParam"):
            m = re.match(r"(\{[^}]*\}\s*)?(\[?[\w$.\[\]]+\]?)?\s*(-)?\s*(.*)", first_line)
            if m.group(1):
                emit(line, "ERROR", "JSDOC_TYPE", f"`@{tag} {{...}}`: drop the JSDoc type; TypeScript already has it")
            name = (m.group(2) or "").strip("[]")
            if not name:
                emit(line, "ERROR", "PARAM_NAME", f"`@{tag}` without a name")
                continue
            if (m.group(2) or "").startswith("["):
                emit(line, "WARN", "JSDOC_OPTIONAL", f"`@{tag} [{name}]`: brackets are JSDoc; write `@{tag} {name} - ...`")
            if not m.group(3):
                emit(line, "ERROR", "PARAM_HYPHEN", f"`@{tag} {name}` needs ` - ` between the name and the description")
            elif not m.group(4).strip() and len(rest.split("\n")) == 1:
                emit(line, "WARN", "PARAM_EMPTY", f"`@{tag} {name} -` has no description")
            (documented if tag == "param" else tdocumented).append(name)
        elif tag == "returns":
            if first_line.startswith("{"):
                emit(line, "ERROR", "JSDOC_TYPE", "`@returns {...}`: drop the JSDoc type; TypeScript already has it")
            if decl.kind in ("constructor", "setter") or (decl.returns and re.fullmatch(
                    r"void|never|Promise<void>|PromiseLike<void>|undefined", decl.returns)):
                emit(line, "WARN", "RETURNS_VOID", f"`@returns` on a {decl.kind} that returns {decl.returns or 'nothing'}")
            elif not rest.strip():
                emit(line, "WARN", "RETURNS_EMPTY", "`@returns` has no description")
        elif tag == "throws":
            if re.match(r"\{(?!@)[^}]*\}", first_line):
                emit(line, "WARN", "JSDOC_TYPE", "`@throws {Type}` is JSDoc; write `@throws {@link Type} if ...` or plain text")
        elif tag == "deprecated" and not rest.strip():
            emit(line, "WARN", "DEPRECATED_EMPTY", "`@deprecated` must say what to use instead")
        elif tag == "example" and "```" not in rest:
            emit(line, "WARN", "EXAMPLE_NO_FENCE", "put the `@example` code in a ```ts fenced block")
    if inherit_only or decl.params is None:
        return
    expected = [p for p in decl.params]
    named = [p for p in expected if p]
    if "" not in expected:
        for d in documented:
            if d.split(".")[0] not in named:
                emit(base, "ERROR", "PARAM_UNKNOWN", f"`@param {d}` names no parameter of `{decl.name}`")
    for p in named:
        if p not in [d.split(".")[0] for d in documented]:
            emit(base, "WARN", "PARAM_MISSING", f"no `@param {p} - ...`")
    order = [d for d in documented if d in named]
    if order != [p for p in named if p in order]:
        emit(base, "WARN", "PARAM_ORDER", "`@param` tags are not in declaration order")
    for t in decl.tparams:
        if t not in tdocumented:
            emit(base, "WARN", "TYPEPARAM_MISSING", f"no `@typeParam {t} - ...`")
    for t in tdocumented:
        if t not in decl.tparams:
            emit(base, "ERROR", "TYPEPARAM_UNKNOWN", f"`@typeParam {t}` names no type parameter of `{decl.name}`")
    if decl.kind in ("function", "method", "call signature") and decl.returns and \
            not re.fullmatch(r"void|never|Promise<void>|PromiseLike<void>|undefined|asserts .*", decl.returns) \
            and "returns" not in names:
        emit(base, "WARN", "RETURNS_MISSING", f"no `@returns` (returns `{short(decl.returns, 40)}`)")


TSDOC_JS = r"""
const path = require('path');
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
let tsdoc;
try {
  tsdoc = require(require.resolve('@microsoft/tsdoc', { paths: [input.root] }));
} catch (e) { console.log('NOTFOUND'); process.exit(0); }
const config = new tsdoc.TSDocConfiguration();
for (const name of input.tags) {
  if (!config.tryGetTagDefinition('@' + name)) {
    config.addTagDefinition(new tsdoc.TSDocTagDefinition({
      tagName: '@' + name, syntaxKind: tsdoc.TSDocTagSyntaxKind.BlockTag, allowMultiple: true }));
  }
}
config.setSupportForTags(config.tagDefinitions, true);
const parser = new tsdoc.TSDocParser(config);
const out = [];
for (const c of input.comments) {
  const ctx = parser.parseString(c.text);
  for (const m of ctx.log.messages) {
    const before = c.text.slice(0, m.textRange.pos + (m.tokenSequence ? 0 : 0));
    let line = c.line;
    if (m.textRange && m.textRange.buffer) {
      const pos = m.textRange.pos;
      line = c.line + (m.textRange.buffer.slice(0, pos).match(/\n/g) || []).length;
    }
    out.push([c.file, line, m.messageId, m.unformattedText]);
  }
}
console.log(JSON.stringify(out));
"""

COVERED_BY_OWN = {"tsdoc-undefined-tag", "tsdoc-param-tag-with-invalid-type", "tsdoc-param-tag-missing-hyphen", "tsdoc-unsupported-tag",
                  "tsdoc-malformed-inline-tag", "tsdoc-inline-tag-missing-right-brace",
                  "tsdoc-escape-right-brace", "tsdoc-escape-greater-than", "tsdoc-reference-missing-dot"}


def run_tsdoc_parser(files_comments, tags, root):
    """Return (ran, {file: [(line, level, code, msg)]})."""
    node = shutil.which("node")
    if not node or not files_comments:
        return False, {}
    payload = json.dumps({"root": root, "tags": sorted(tags), "comments": files_comments})
    try:
        r = subprocess.run([node, "-e", TSDOC_JS], input=payload, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False, {}
    out = r.stdout.strip()
    if r.returncode != 0 or not out or out == "NOTFOUND":
        return False, {}
    found = {}
    for f, line, mid, msg in json.loads(out.splitlines()[-1]):
        if mid in COVERED_BY_OWN:
            continue
        found.setdefault(f, []).append((line, "WARN", f"TSDOC({mid})", msg))
    return True, found


def cmd_lint(files, internal, custom):
    errors = 0
    results = {}
    parser_input = []
    all_tags = set(custom)
    notes = set()
    for path in files:
        src = read(path)
        _, comments, masked = lex(src, is_tsx(path))
        decls = declarations(path, src, masked, internal)
        attached, pkg = attach_docs(src, masked, comments, decls)
        extra, nts = project_tags(path)
        legacy = find_up(path, ["api-extractor.json"]) is not None
        if legacy:
            nts = list(nts) + ["api-extractor.json found: links checked as legacy TSDoc syntax"]
        notes |= set(nts)
        allowed = custom | extra
        all_tags |= allowed
        src_names = names_in_file(masked, decls)
        classes = class_members(decls)
        found = []

        def emit(line, level, code, msg):
            found.append((line, level, code, msg))

        for d in decls:
            if d.doc:
                own_checks(d, emit, allowed, src_names, classes, legacy)
        for d in decls:
            ov = getattr(d, "overload_of", None)
            if d.doc and ov is not None and d.has_body and not ov.doc:
                emit(d.doc[2], "WARN", "OVERLOAD_DOC", f"doc comment is on the implementation of overloaded "
                     f"`{d.name}`; move it to the first overload signature (line {ov.line})")
        for c in comments:
            text = c[3]
            if text.startswith("/**") and not text.startswith("/**/"):
                parser_input.append({"file": path, "line": c[2], "text": text})
                if c[0] not in attached and "@license" not in text:
                    emit(c[2], "WARN", "ORPHAN_DOC", "this /** */ comment documents nothing (it is not directly "
                         "before a declaration); move it or make it `//`")
        results[path] = found
    root = os.path.dirname(find_up(files[0], ["package.json"]) or os.path.abspath(files[0]))
    ran, extra_found = run_tsdoc_parser(parser_input, all_tags, root)
    print(f"NOTE tags: TSDoc standard" + "".join(f" + {n}" for n in sorted(notes)) + (f" + --tags" if custom else ""))
    if not ran:
        print("SKIP tsdoc-parser: @microsoft/tsdoc not installed in the project (or node missing); "
              "only this script's checks ran")
    for path in files:
        found = results[path] + extra_found.get(path, [])
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
        la, lb = lex(old, is_tsx(path)), lex(read(path), is_tsx(path))
        a, b = la[0], lb[0]
        problems = []
        if a != b:
            i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            problems.append(f"CODE changed near token {i}: before `{' '.join(a[max(0, i - 3):i + 4])}` "
                            f"/ after `{' '.join(b[max(0, i - 3):i + 4])}`")
        da, db = guarded(old, la), guarded(read(path), lb)
        for kind in ("DIRECTIVE", "LICENSE"):
            before = [x for x in da if x[0] == kind]
            after = [x for x in db if x[0] == kind]
            if kind == "DIRECTIVE" and before != after:
                lost = [x for x in before if x not in after]
                problems.append(f"DIRECTIVE moved, changed or removed: {short(lost[0][2] if lost else after[0][2], 70)} "
                                "(a directive must keep its exact text and stay before the same code)")
            if kind == "LICENSE" and not {x[2] for x in before} <= {x[2] for x in after}:
                problems.append("LICENSE comment changed or removed")
        if not problems:
            print(f"{path}: OK")
            continue
        status = 1
        for msg in problems:
            print(f"{path}: {msg}")
    return status


def guarded(src, lexed):
    """Directive and license comments as (kind, code tokens before it, text)."""
    _, comments, masked = lexed
    first_code = len(masked) - len(masked.lstrip())
    out = []
    for c in comments:
        text = c[3]
        kind = kind_of(text, c[0] <= first_code)
        if text.startswith("/**") and ("@license" in text or "@preserve" in text):
            kind = "LICENSE"
        if kind in ("DIRECTIVE", "LICENSE"):
            before = len(TOKEN_RE.findall(masked[:c[0]]))
            out.append((kind, before, " ".join(text.split())))
    return out


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "lint", "snapshot", "check"):
        print(__doc__, file=sys.stderr)
        return 2
    mode, args = argv[1], argv[2:]
    internal = "--internal" in args
    args = [a for a in args if a != "--internal"]
    custom, base, rev = set(), None, None
    rest = []
    k = 0
    while k < len(args):
        a = args[k]
        if a in ("--tags", "--base", "--rev") and k + 1 < len(args):
            v = args[k + 1]
            if a == "--tags":
                custom = {t.strip().lstrip("@") for t in v.split(",") if t.strip()}
            elif a == "--base":
                base = v
            else:
                rev = v
            k += 2
            continue
        rest.append(a)
        k += 1
    files = [a for a in rest if a.endswith(EXTS)]
    if not files:
        print("no .ts/.tsx/.mts/.cts files given", file=sys.stderr)
        return 2
    missing = [f for f in files if not os.path.isfile(f)]
    if missing and mode != "check":
        print(f"not found: {' '.join(missing)}", file=sys.stderr)
        return 2
    if mode == "list":
        return cmd_list(files, internal)
    if mode == "lint":
        return cmd_lint(files, internal, custom)
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="ts-comment-")
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
