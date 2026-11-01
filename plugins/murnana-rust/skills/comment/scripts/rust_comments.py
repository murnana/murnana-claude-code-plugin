#!/usr/bin/env python3
"""List the comments in Rust files, or check that only comments changed.

Usage:
  rust_comments.py list FILE...         Print every comment as `file:line: KIND: text`.
  rust_comments.py snapshot FILE...     Copy FILEs to a new temporary directory and
                                        print its path. Run before editing.
  rust_comments.py check --base DIR FILE...
                                        Exit 1 if any file's code (everything except
                                        comments and whitespace) differs from its copy
                                        in DIR (made by `snapshot`), if the license header
                                        changed, or if a `// SAFETY:` comment was removed.
  rust_comments.py check --rev REV FILE...
                                        Same, comparing against a git revision instead.

KIND is one of: DOC_OUTER (///), DOC_INNER (//!), SAFETY, TODO, FIXME, LINE (//), BLOCK (/* */).
The lexer understands string, raw string, byte string, char literals and lifetimes,
so `"//"` inside a string is not taken for a comment.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def lex(src):
    """Split Rust source into (code_tokens, comments).

    comments: list of (line, kind, text). code_tokens: whitespace-separated code
    with comments removed, used for comparison.
    """
    code = []
    comments = []
    i, n, line = 0, len(src), 1

    def emit_comment(start, end, start_line, block):
        text = src[start:end]
        if block:
            kind = "DOC_OUTER" if text.startswith("/**") and not text.startswith("/**/") else \
                   "DOC_INNER" if text.startswith("/*!") else "BLOCK"
        else:
            kind = "DOC_OUTER" if text.startswith("///") and not text.startswith("////") else \
                   "DOC_INNER" if text.startswith("//!") else "LINE"
        if kind in ("LINE", "BLOCK"):
            body = text.lstrip("/*! ").upper()
            for tag in ("SAFETY", "TODO", "FIXME"):
                if body.startswith(tag):
                    kind = tag
                    break
        comments.append((start_line, kind, " ".join(text.split())))

    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            code.append(" ")
            i += 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j == -1 else j
            emit_comment(i, j, line, False)
            code.append(" ")
            i = j
        elif src.startswith("/*", i):
            start, start_line, depth = i, line, 0
            while i < n:
                if src.startswith("/*", i):
                    depth += 1
                    i += 2
                elif src.startswith("*/", i):
                    depth -= 1
                    i += 2
                    if depth == 0:
                        break
                else:
                    if src[i] == "\n":
                        line += 1
                    i += 1
            emit_comment(start, i, start_line, True)
            code.append(" ")
        else:
            m = re.compile(r'(?:b|c)?r(#*)"').match(src, i)
            if m and (i == 0 or not (src[i - 1].isalnum() or src[i - 1] == "_")):
                close = '"' + m.group(1)
                j = src.find(close, m.end())
                j = n if j == -1 else j + len(close)
                line += src.count("\n", i, j)
                code.append(src[i:j])
                i = j
                continue
            if c == '"' or (c in "bc" and src.startswith('"', i + 1)
                            and (i == 0 or not (src[i - 1].isalnum() or src[i - 1] == "_"))):
                j = i + (2 if c != '"' else 1)
                while j < n and src[j] != '"':
                    j += 2 if src[j] == "\\" else 1
                j = min(j + 1, n)
                line += src.count("\n", i, j)
                code.append(src[i:j])
                i = j
                continue
            if c == "'" or (c == "b" and src.startswith("'", i + 1)):
                k = i + (2 if c == "b" else 1)
                m = re.compile(r"(\\(?:x[0-9a-fA-F]{2}|u\{[0-9a-fA-F_]+\}|.)|[^\\\n])'").match(src, k)
                if m:  # char literal
                    code.append(src[i:m.end()])
                    i = m.end()
                    continue
                code.append(c)  # lifetime or label: the identifier follows as code
                i += 1
                continue
            if c.isspace():
                code.append(" ")
            else:
                code.append(c)
            i += 1
    return "".join(code).split(), comments


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "snapshot", "check"):
        print(__doc__, file=sys.stderr)
        return 2
    mode, args = argv[1], argv[2:]
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
    files = [a for a in args if a.endswith(".rs")]
    if not files:
        print("no .rs files given", file=sys.stderr)
        return 2
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="rust-comment-")
        for path in files:
            dest = os.path.join(out, os.path.abspath(path).lstrip(os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    status = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        tokens, comments = lex(src)
        if mode == "list":
            for ln, kind, text in comments:
                print(f"{path}:{ln}: {kind}: {text}")
            continue
        if base is not None:
            copy = os.path.join(base, os.path.abspath(path).lstrip(os.sep))
            old = open(copy, encoding="utf-8").read() if os.path.exists(copy) else None
        else:
            old = git_show(rev, path)
        if old is None:
            print(f"SKIP {path}: no earlier copy")
            continue
        old_tokens, old_comments = lex(old)
        new_licenses = licenses(src, comments)
        lost = [("LICENSE", t) for t in licenses(old, old_comments) if t not in new_licenses]
        safety_before = sum(1 for _, kind, _ in old_comments if kind == "SAFETY")
        safety_after = sum(1 for _, kind, _ in comments if kind == "SAFETY")
        if safety_after < safety_before:
            lost.append(("SAFETY", f"{safety_before - safety_after} // SAFETY: comment(s) removed"))
        if old_tokens == tokens and not lost:
            print(f"OK   {path}: only comments/whitespace changed")
            continue
        status = 1
        if old_tokens != tokens:
            k = next((x for x in range(min(len(old_tokens), len(tokens)))
                      if old_tokens[x] != tokens[x]), min(len(old_tokens), len(tokens)))
            before = " ".join(old_tokens[max(0, k - 5):k + 5])
            after = " ".join(tokens[max(0, k - 5):k + 5])
            print(f"CODE {path}: code changed near\n     was: {before}\n     now: {after}")
        for kind, text in lost:
            print(f"{kind} {path}: changed or removed: {text[:120]}")
    return status


def licenses(src, comments):
    """Copyright or license comments in the header (before the first code), whitespace-normalized."""
    header = re.match(r"(?:\s|//[^\n]*|/\*.*?\*/)*", src, re.S)
    last_line = src.count("\n", 0, header.end()) + 1
    return [text for ln, _, text in comments if ln <= last_line
            and re.search(r"copyright|license|licence|SPDX-License-Identifier", text, re.IGNORECASE)]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
