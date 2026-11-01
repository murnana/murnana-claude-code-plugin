#!/usr/bin/env python3
"""Check C++ doc comments with Doxygen (and clang, when available).

Usage: check_comments.py [--doxyfile PATH | --no-doxyfile] FILE...

Run from the repository root. Prints one line per finding,
"path:line: [check] message", then a summary line.
"[advisory]" lines (a documented function without @param/@return) don't
count as findings. Exit status: 0 = no findings, 1 = findings,
2 = Doxygen is not installed or a file doesn't exist.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

DOXYFILE_CANDIDATES = ["Doxyfile", "docs/Doxyfile", "doc/Doxyfile"]
SOURCE_EXTS = {".c", ".cc", ".cpp", ".cxx", ".c++"}
HEADER_EXTS = {".h", ".hh", ".hpp", ".hxx", ".h++", ".ipp", ".inl"}
ADVISORY = re.compile(r"(parameters|return type) of member .* (is|are) not documented$")


def rel(path):
    try:
        return os.path.relpath(path)
    except ValueError:
        return path


def text_of(elem):
    return "".join(elem.itertext()).strip() if elem is not None else ""


def run_doxygen(files, doxyfile, outdir):
    """Run Doxygen on the files and return its warning lines."""
    logfile = os.path.join(outdir, "warnings.log")
    lines = []
    if doxyfile:
        lines.append("@INCLUDE = " + os.path.abspath(doxyfile))
    lines += [
        "INPUT = " + " ".join('"%s"' % os.path.abspath(f) for f in files),
        "EXCLUDE =",
        "RECURSIVE = NO",
        "OUTPUT_DIRECTORY = " + outdir,
        "FULL_PATH_NAMES = YES",
        "STRIP_FROM_PATH = " + os.getcwd(),
        # HTML must be generated: with XML alone, Doxygen 1.9.8 reports false
        # "parameters ... are not documented" warnings.
        "GENERATE_HTML = YES",
        "GENERATE_XML = YES",
        "GENERATE_LATEX = NO",
        "GENERATE_RTF = NO",
        "GENERATE_MAN = NO",
        "HAVE_DOT = NO",
        "QUIET = YES",
        "WARNINGS = YES",
        # EXTRACT_ALL = YES would silence the undocumented-member warnings.
        "EXTRACT_ALL = NO",
        "WARN_IF_UNDOCUMENTED = YES",
        "WARN_IF_DOC_ERROR = YES",
        "WARN_IF_INCOMPLETE_DOC = YES",
        "WARN_NO_PARAMDOC = YES",
        "WARN_AS_ERROR = NO",
        'WARN_FORMAT = "$file:$line: $text"',
        "WARN_LOGFILE = " + logfile,
    ]
    subprocess.run(["doxygen", "-"], input="\n".join(lines) + "\n", text=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if not os.path.exists(logfile):
        return []
    with open(logfile, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    # Continuation lines ("  parameter 'x'") belong to the previous warning.
    merged = []
    for line in raw.splitlines():
        if line.startswith((" ", "\t")) and merged:
            merged[-1] += " " + line.strip()
        elif line.strip():
            merged.append(line.strip())
    return merged


def doxygen_findings(warnings, targets):
    findings = []
    for w in warnings:
        m = re.match(r"(.+?):(\d+): (?:warning|error): (.*)", w)
        if not m:
            continue
        path = os.path.abspath(m.group(1))
        if path in targets:
            msg = m.group(3)
            # WARN_NO_PARAMDOC: may be acceptable for a trivial accessor whose
            # @brief already says everything, so it doesn't fail the check.
            check = "advisory" if ADVISORY.match(msg) else "doxygen"
            findings.append((rel(path), int(m.group(2)), check, msg))
    return findings


def location(elem):
    loc = elem.find("location")
    if loc is None:
        return None, 0
    return os.path.abspath(loc.get("file", "")), int(loc.get("line", "0") or 0)


def member_key(member):
    return member.get("id", "").rsplit("_1", 1)[-1]


def is_documented(elem):
    return bool(text_of(elem.find("briefdescription")) or text_of(elem.find("detaileddescription")))


def structure_findings(xmldir, targets):
    """Find what Doxygen accepts silently but renders wrongly or not at all."""
    findings = []
    if not os.path.isdir(xmldir):
        return findings
    compounds = []
    for name in sorted(os.listdir(xmldir)):
        if not name.endswith(".xml") or name == "index.xml":
            continue
        try:
            compounds += ET.parse(os.path.join(xmldir, name)).getroot().iter("compounddef")
        except ET.ParseError:
            continue
    # A function declared in a header and defined in a .cpp is listed in both
    # file compounds, with ids that differ only in the file prefix. It is
    # visible if any documented file lists it.
    visible = {member_key(m) for c in compounds
               if c.get("kind") == "file" and is_documented(c) for m in c.iter("memberdef")}
    for compound in compounds:
        kind = compound.get("kind")
        cname = compound.findtext("compoundname", "")
        members = list(compound.iter("memberdef"))
        documented_in_targets = [
            m for m in members if is_documented(m) and location(m)[0] in targets
        ]
        if kind == "file":
            path, _ = location(compound)
            # Only entities declared in this file: a .cpp also lists the
            # definitions of functions declared (and documented) in a header.
            declared_here = [m for m in documented_in_targets
                             if location(m)[0] == path and member_key(m) not in visible]
            if path in targets and declared_here and not is_documented(compound):
                findings.append((rel(path), 1, "structure",
                                 "no @file block: %d documented file-scope entities (%s) are left out of the generated pages"
                                 % (len(declared_here),
                                    ", ".join(sorted({m.findtext("name") for m in declared_here})[:5]))))
        if kind == "namespace" and documented_in_targets and not is_documented(compound):
            path, line = location(documented_in_targets[0])
            findings.append((rel(path), line, "structure",
                             "namespace %s is not documented anywhere: its documented members are left out of the generated pages" % cname))
        if kind in ("class", "struct", "union") and not text_of(compound.find("briefdescription")) \
                and text_of(compound.find("detaileddescription")):
            path, line = location(compound)
            if path in targets:
                findings.append((rel(path), line, "structure",
                                 "%s has a detailed description but an empty brief: start the block with @brief" % cname))
        for m in members:
            path, line = location(m)
            if path not in targets:
                continue
            mname = m.findtext("name")
            brief = text_of(m.find("briefdescription"))
            detail_elem = m.find("detaileddescription")
            if not brief and text_of(detail_elem):
                findings.append((rel(path), line, "structure",
                                 "%s %s has a detailed description but an empty brief: start the block with @brief" % (m.get("kind"), mname)))
            if text_of(m.find("inbodydescription")):
                findings.append((rel(path), line, "structure",
                                 "%s has a /// or /** */ comment inside its body; use // there" % mname))
            if m.get("kind") == "function" and detail_elem is not None:
                has_return = any(s.get("kind") == "return" for s in detail_elem.iter("simplesect"))
                rtype = text_of(m.find("type"))
                if has_return and (rtype in ("", "void") or rtype.endswith(" void")):
                    findings.append((rel(path), line, "structure",
                                     "@return on %s, which returns nothing (void or constructor)" % mname))
    return findings


def compile_flags(compdb, path):
    """Flags for clang from compile_commands.json: the file's own entry, or the first entry for a header."""
    if not compdb:
        return None
    for entry in compdb:
        f = os.path.abspath(os.path.join(entry.get("directory", "."), entry.get("file", "")))
        if f == path:
            return entry
    return compdb[0] if os.path.splitext(path)[1] in HEADER_EXTS else None


def useful_args(entry):
    args = entry.get("arguments") or shlex.split(entry.get("command", ""))
    keep, i = [], 1
    while i < len(args):
        a = args[i]
        if a in ("-I", "-D", "-isystem", "-include", "-iquote") and i + 1 < len(args):
            val = args[i + 1]
            if a != "-D" and not os.path.isabs(val):
                val = os.path.join(entry.get("directory", "."), val)
            keep += [a, val]
            i += 2
            continue
        if a.startswith(("-I", "-isystem", "-iquote")) and len(a) > 2:
            prefix = "-I" if a.startswith("-I") else ("-isystem" if a.startswith("-isystem") else "-iquote")
            val = a[len(prefix):]
            if not os.path.isabs(val):
                val = os.path.join(entry.get("directory", "."), val)
            keep.append(prefix + val)
        elif a.startswith(("-D", "-std=")):
            keep.append(a)
        i += 1
    return keep


def clang_findings(files, targets):
    clang = shutil.which("clang++")
    if not clang:
        return [], "clang++ not found: skipped the -Wdocumentation check"
    compdb = None
    for candidate in ("compile_commands.json", "build/compile_commands.json"):
        if os.path.exists(candidate):
            with open(candidate, encoding="utf-8") as fh:
                compdb = json.load(fh)
            break
    findings, notes = [], []
    for f in files:
        path = os.path.abspath(f)
        entry = compile_flags(compdb, path)
        if entry:
            extra = useful_args(entry)
        else:
            extra = ["-I" + d for d in ("include", "src", os.path.dirname(f) or ".") if os.path.isdir(d)]
        if not any(a.startswith("-std=") for a in extra):
            extra.append("-std=c++20")
        lang = ["-x", "c++-header"] if os.path.splitext(f)[1] in HEADER_EXTS else []
        cmd = [clang, "-fsyntax-only", "-Wdocumentation", "-Wdocumentation-unknown-command"] + extra + lang + [f]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        errors = 0
        for line in proc.stderr.splitlines():
            m = re.match(r"(.+?):(\d+):\d+: (warning|error): (.*)", line)
            if not m:
                continue
            if m.group(3) == "error":
                errors += 1
                continue
            if "-Wdocumentation" in m.group(4) and os.path.abspath(m.group(1)) in targets:
                findings.append((rel(m.group(1)), int(m.group(2)), "clang", m.group(4)))
        if errors:
            notes.append("clang: %s did not compile standalone (%d errors); its clang check may be incomplete" % (f, errors))
    return findings, "; ".join(notes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--doxyfile", help="project Doxyfile to include (default: auto-detect)")
    group.add_argument("--no-doxyfile", action="store_true", help="use Doxygen's defaults")
    args = parser.parse_args()

    missing = [f for f in args.files if not os.path.isfile(f)]
    if missing:
        print("not found: " + ", ".join(missing))
        return 2
    targets = {os.path.abspath(f) for f in args.files}

    doxyfile = None
    if args.doxyfile:
        doxyfile = args.doxyfile
    elif not args.no_doxyfile:
        doxyfile = next((c for c in DOXYFILE_CANDIDATES if os.path.isfile(c)), None)

    findings, notes = [], []
    status = 0
    if shutil.which("doxygen"):
        outdir = tempfile.mkdtemp(prefix="check-comments-")
        try:
            findings += doxygen_findings(run_doxygen(args.files, doxyfile, outdir), targets)
            findings += structure_findings(os.path.join(outdir, "xml"), targets)
        finally:
            shutil.rmtree(outdir, ignore_errors=True)
        notes.append("Doxyfile: " + (doxyfile or "none (Doxygen defaults)"))
    else:
        notes.append("doxygen not found: install it (e.g. `apt install doxygen`, `brew install doxygen`) for the main check")
        status = 2

    clang_result, clang_note = clang_findings(args.files, targets)
    findings += clang_result
    if clang_note:
        notes.append(clang_note)

    seen = set()
    for path, line, check, msg in sorted(findings):
        key = (path, line, check, msg)
        if key in seen:
            continue
        seen.add(key)
        print("%s:%d: [%s] %s" % (path, line, check, msg))
    for note in notes:
        print("note: " + note)
    blocking = [k for k in seen if k[2] != "advisory"]
    print("%d finding(s), %d advisory" % (len(blocking), len(seen) - len(blocking)))
    if status:
        return status
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
