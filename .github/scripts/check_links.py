#!/usr/bin/env python3
"""links (a step of ref-check): every relative link in a tracked Markdown file resolves to a file
or folder of this repository at this commit (DR-0051). Links to the web, mail addresses and
anchors in the same file are not followed. Links inside a text's list of superseded wording (from
its heading "## Superseded wording" to the end of the file) are verbatim history and are not
followed. Code spans and fenced code blocks are skipped.
Records that are never edited are not followed either, so that a later move of a file never
leaves the check red on history: decision records and their index (decisions/), raw records
(references/), release notes, change logs, and the Edition Maker's raw reviews and trials.
Rule: LINK-DEAD  a relative link names a path that is not in this repository.
Usage: check_links.py   (run at the root of the repository under test)."""
import posixpath, re, subprocess, sys, urllib.parse

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout

tracked = set(git("ls-files").splitlines())
dirs = {""}
for p in tracked:
    d = posixpath.dirname(p)
    while d and d not in dirs:
        dirs.add(d); d = posixpath.dirname(d)

INLINE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
CODE = re.compile(r"`+[^`]*`+")

def targets(line):
    line = CODE.sub("", line)
    out = [m.group(1) for m in INLINE.finditer(line)]
    m = REFDEF.match(line)
    if m: out.append(m.group(1))
    return out

errs = []
SKIP = ("decisions/", "references/", "RELEASE-NOTES/", "library/edition-maker/reviews/", "library/edition-maker/trials/")
for f in sorted(p for p in tracked if p.endswith(".md") and not p.startswith(SKIP) and posixpath.basename(p) != "CHANGELOG.md"):
    try:
        text = open(f, encoding="utf-8").read()
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        continue
    fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence; continue
        if fence: continue
        if re.match(r"^##\s+Superseded wording", line):
            break
        for t in targets(line):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", t) or t.startswith("#") or t.startswith("//"):
                continue
            path = urllib.parse.unquote(t.split("#", 1)[0].split("?", 1)[0])
            if not path:
                continue
            base = "" if path.startswith("/") else posixpath.dirname(f)
            norm = posixpath.normpath(posixpath.join(base, path.lstrip("/")))
            if norm == ".": norm = ""
            if norm.startswith(".."):
                errs.append((f, n, t, "points outside the repository")); continue
            if norm.rstrip("/") not in tracked and norm.rstrip("/") not in dirs:
                errs.append((f, n, t, "not in this repository"))
for f, n, t, why in errs:
    print(f"::error file={f},line={n}::LINK-DEAD {t}: {why}")
if errs:
    sys.exit(1)
print("links: every relative link resolves")
