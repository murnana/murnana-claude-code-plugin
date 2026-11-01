#!/usr/bin/env python3
"""List the comments in C++ files, or check that only comments changed.

Usage:
  cpp_comments.py list FILE...          Print every comment as `file:line: KIND: text`.
  cpp_comments.py snapshot FILE...      Copy FILEs to a new temporary directory and
                                        print its path. Run before editing.
  cpp_comments.py check --base DIR FILE...
                                        Exit 1 if any file's code (everything except
                                        comments and whitespace) differs from its copy
                                        in DIR (made by `snapshot`), or if a DIRECTIVE or
                                        LICENSE comment was changed or removed.
  cpp_comments.py check --rev REV FILE...
                                        Same, comparing against a git revision instead.

KIND is one of: DOC (///, //!, /** */, /*! */), LICENSE (a copyright or license
comment before the first line of code), DIRECTIVE (NOLINT, clang-format, IWYU,
cppcheck-suppress, ...), TODO, FIXME, LINE (//), BLOCK (/* */).
The lexer understands string, raw string (R"x(...)x") and character literals and
digit separators (1'000), so `"//"` inside a string is not taken for a comment.
Undocumented declarations are reported by check_comments.py (Doxygen), not here.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

EXTS = (".h", ".hh", ".hpp", ".hxx", ".h++", ".ipp", ".inl", ".tpp",
        ".c", ".cc", ".cpp", ".cxx", ".c++", ".cppm", ".ixx")
DIRECTIVE = re.compile(
    r"^(?://|/\*)\s*(?:NOLINT|NOLINTNEXTLINE|NOLINTBEGIN|NOLINTEND|clang-format\s+(?:off|on)"
    r"|IWYU\s+pragma|cppcheck-suppress|coverity\[|LCOV_EXCL|GCOVR_EXCL|NOSONAR|lint\b|fallthrough\b)",
    re.IGNORECASE)
RAW_PREFIX = re.compile(r'(?:u8|u|U|L)?R"([^()\\\s]{0,16})\(')
NUMBER_TAIL = re.compile(r"(?<![A-Za-z_0-9'])\d[0-9A-Za-z']*$")


def is_digit_separator(src, i):
    """True if the quote at i sits inside a number literal (1'000'000, 0xFF'FF)."""
    return bool(NUMBER_TAIL.search(src[max(0, i - 64):i])) and src[i + 1:i + 2].isalnum()


def lex(src):
    """Split C++ source into (code_tokens, comments).

    comments: list of (line, text, before_code). code_tokens: whitespace-separated
    code with comments removed, used for comparison.
    """
    code = []
    comments = []
    i, n, line = 0, len(src), 1
    seen_code = False

    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            code.append(" ")
            i += 1
        elif src.startswith("//", i):
            j = i
            while True:  # a backslash at the end of the line continues the comment
                k = src.find("\n", j)
                k = n if k == -1 else k
                if k < n and src[j:k].rstrip("\r").endswith("\\"):
                    j = k + 1
                    continue
                break
            comments.append((line, src[i:k], not seen_code))
            line += src.count("\n", i, k)
            code.append(" ")
            i = k
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            comments.append((line, src[i:j], not seen_code))
            line += src.count("\n", i, j)
            code.append(" ")
            i = j
        else:
            prev = src[i - 1] if i else ""
            m = RAW_PREFIX.match(src, i)
            if m and not (prev.isalnum() or prev == "_"):
                close = ")" + m.group(1) + '"'
                j = src.find(close, m.end())
                j = n if j == -1 else j + len(close)
            elif c == '"' or (c == "'" and not is_digit_separator(src, i)):
                j = i + 1
                while j < n and src[j] != c and src[j] != "\n":
                    j += 2 if src[j] == "\\" else 1
                j = min(j + 1, n)
            else:
                code.append(" " if c.isspace() else c)
                if not c.isspace():
                    seen_code = True
                i += 1
                continue
            seen_code = True
            line += src.count("\n", i, j)
            code.append(src[i:j])
            i = j
    return "".join(code).split(), comments


def kind_of(text, before_code):
    if DIRECTIVE.match(text):
        return "DIRECTIVE"
    if before_code and re.search(r"copyright|license|licence|SPDX-License-Identifier", text, re.IGNORECASE):
        return "LICENSE"
    if text.startswith(("///", "//!")) and not text.startswith("////"):
        return "DOC"
    if text.startswith(("/**", "/*!")) and not text.startswith(("/**/", "/***")):
        return "DOC"
    body = text.lstrip("/*! ").upper()
    for tag in ("TODO", "FIXME"):
        if body.startswith(tag):
            return tag
    return "BLOCK" if text.startswith("/*") else "LINE"


def guarded(comments):
    """The DIRECTIVE and LICENSE comments, in order, whitespace-normalized."""
    return [(kind, " ".join(text.split())) for _, text, bc in comments
            for kind in [kind_of(text, bc)] if kind in ("DIRECTIVE", "LICENSE")]


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


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
    files = [a for a in args if a.lower().endswith(EXTS)]
    if not files:
        print("no C++ files given", file=sys.stderr)
        return 2
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="cpp-comment-")
        for path in files:
            dest = os.path.join(out, os.path.abspath(path).lstrip(os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    status = 0
    for path in files:
        tokens, comments = lex(read(path))
        if mode == "list":
            for ln, text, bc in comments:
                print(f"{path}:{ln}: {kind_of(text, bc)}: {' '.join(text.split())[:160]}")
            continue
        if base is not None:
            copy = os.path.join(base, os.path.abspath(path).lstrip(os.sep))
            old = read(copy) if os.path.exists(copy) else None
        else:
            old = git_show(rev, path)
        if old is None:
            print(f"SKIP {path}: no earlier copy")
            continue
        old_tokens, old_comments = lex(old)
        ok = True
        if old_tokens != tokens:
            ok = False
            k = next((x for x in range(min(len(old_tokens), len(tokens)))
                      if old_tokens[x] != tokens[x]), min(len(old_tokens), len(tokens)))
            before = " ".join(old_tokens[max(0, k - 5):k + 5])
            after = " ".join(tokens[max(0, k - 5):k + 5])
            print(f"CODE {path}: code changed near\n     was: {before}\n     now: {after}")
        old_guarded, new_guarded = guarded(old_comments), guarded(comments)
        for kind, text in old_guarded:
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
