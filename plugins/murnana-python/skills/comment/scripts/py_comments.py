#!/usr/bin/env python3
"""List the comments in Python files, or check that only comments and docstrings changed.

Usage:
  py_comments.py list FILE...           Print every comment as `file:line: KIND: text`, then
                                        every public module, class or function without a
                                        docstring as `file:line: UNDOCUMENTED: <name>`.
  py_comments.py snapshot FILE...       Copy FILEs to a new temporary directory and print
                                        its path. Run before editing.
  py_comments.py check --base DIR FILE...
                                        Exit 1 if any file's code (its syntax tree with the
                                        docstrings removed) differs from its copy in DIR
                                        (made by `snapshot`), or if a DIRECTIVE or LICENSE
                                        comment was changed or removed.
  py_comments.py check --rev REV FILE...
                                        Same, comparing against a git revision instead.

KIND is one of: DIRECTIVE (# noqa, # type:, # pragma:, # pylint:, # fmt:, # isort:,
# ruff:, # mypy:, # pyright:), LICENSE (a copyright or license comment before the
first line of code), SHEBANG (#! and coding lines), TODO, FIXME, LINE.
`check` compares syntax trees, so pure formatting changes are not reported.
Public means: not starting with `_`, except `__init__` with parameters besides self;
nested functions, members of private classes and `test_*` functions are skipped.
"""
import ast
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize

DIRECTIVE = re.compile(r"#\s*(?:noqa\b|type:|pragma:|pylint:|fmt:|isort:|ruff:|mypy:|pyright:)",
                       re.IGNORECASE)


def comments_of(src):
    """Return [(line, kind, text)] for every `#` comment."""
    out = []
    seen_code = False
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError):
        return out
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            text = tok.string
            if DIRECTIVE.search(text):
                kind = "DIRECTIVE"
            elif tok.start[0] <= 2 and (text.startswith("#!") or re.search(r"coding[:=]", text)):
                kind = "SHEBANG"
            elif not seen_code and re.search(r"copyright|license|licence|SPDX-License-Identifier",
                                             text, re.IGNORECASE):
                kind = "LICENSE"
            else:
                body = text.lstrip("# ").upper()
                kind = next((t for t in ("TODO", "FIXME") if body.startswith(t)), "LINE")
            out.append((tok.start[0], kind, text))
        elif tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                              tokenize.ENCODING, tokenize.ENDMARKER):
            seen_code = True
    return out


def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return tree


def code_of(src, path):
    return ast.dump(strip_docstrings(ast.parse(src, path)), include_attributes=False)


def undocumented(src, path):
    """Yield (line, name) for public objects without a docstring."""
    tree = ast.parse(src, path)
    if ast.get_docstring(tree) is None and src.strip():
        yield 1, "module"

    def visit(body, prefix, in_class):
        for node in body:
            if isinstance(node, ast.ClassDef):
                if node.name.startswith("_"):
                    continue
                if ast.get_docstring(node) is None:
                    yield node.lineno, f"class {prefix}{node.name}"
                yield from visit(node.body, f"{prefix}{node.name}.", True)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name == "__init__":
                    params = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                    if not in_class or len(params) <= 1 and not node.args.vararg and not node.args.kwarg:
                        continue
                elif name.startswith("_") or name.startswith("test_"):
                    continue
                if ast.get_docstring(node) is None:
                    yield node.lineno, f"def {prefix}{name}"

    yield from visit(tree.body, "", False)


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:./{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def read(path):
    with open(path, encoding="utf-8") as f:
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
    files = [a for a in args if a.endswith((".py", ".pyi"))]
    if not files:
        print("no .py files given", file=sys.stderr)
        return 2
    if mode == "snapshot":
        out = tempfile.mkdtemp(prefix="py-comment-")
        for path in files:
            dest = os.path.join(out, os.path.abspath(path).lstrip(os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
        print(out)
        return 0
    status = 0
    for path in files:
        src = read(path)
        if mode == "list":
            for ln, kind, text in comments_of(src):
                print(f"{path}:{ln}: {kind}: {text[:160]}")
            try:
                for ln, name in undocumented(src, path):
                    print(f"{path}:{ln}: UNDOCUMENTED: {name}")
            except SyntaxError as e:
                print(f"{path}:{e.lineno}: ERROR: cannot parse: {e.msg}")
                status = 1
            continue
        if base is not None:
            copy = os.path.join(base, os.path.abspath(path).lstrip(os.sep))
            old = read(copy) if os.path.exists(copy) else None
        else:
            old = git_show(rev, path)
        if old is None:
            print(f"SKIP {path}: no earlier copy")
            continue
        ok = True
        try:
            if code_of(old, path) != code_of(src, path):
                ok = False
                print(f"CODE {path}: code changed (syntax tree differs outside docstrings)")
        except SyntaxError as e:
            ok = False
            print(f"CODE {path}:{e.lineno}: cannot parse: {e.msg}")
        new_guarded = [(k, t.strip()) for _, k, t in comments_of(src) if k in ("DIRECTIVE", "LICENSE")]
        for _, kind, text in comments_of(old):
            if kind in ("DIRECTIVE", "LICENSE") and (kind, text.strip()) not in new_guarded:
                ok = False
                print(f"{kind} {path}: changed or removed: {text.strip()[:120]}")
        if ok:
            print(f"OK   {path}: only comments/docstrings changed")
        else:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
