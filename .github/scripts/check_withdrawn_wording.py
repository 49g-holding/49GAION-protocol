#!/usr/bin/env python3
"""withdrawn-wording (49GAION/DR-0054): wording that the governing seat has withdrawn never comes back
into a text. The list (.github/withdrawn-wording.tsv) names, one per row: an id, a regular expression
(read case-insensitive and multi-line), the record that withdrew it and what it was. Every tracked
Markdown file is read whole, code spans included, except the records that keep history verbatim and
are never edited: decision records and their index (decisions/), raw records (references/), release
notes, change logs, and raw reviews and trials. The list itself is read from the base branch.
Rule: WITHDRAWN-WORDING <id>  a text carries wording that the list names.
Usage: check_withdrawn_wording.py <list>   (run at the root of the repository under test)."""
import re, subprocess, sys

if len(sys.argv) != 2:
    print("::error::WITHDRAWN-WORDING-USAGE: check_withdrawn_wording.py <list>"); sys.exit(2)
rules = []
try:
    for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) != 4:
            print(f"::error::WITHDRAWN-WORDING-LIST row {n}: four tab-separated columns expected"); sys.exit(1)
        rules.append((cols[0], re.compile(cols[1], re.I | re.M), cols[2], cols[3]))
except (OSError, re.error) as e:
    print(f"::error::WITHDRAWN-WORDING-LIST unreadable: {e}; failing closed"); sys.exit(1)
if not rules:
    print("::error::WITHDRAWN-WORDING-LIST is empty; failing closed"); sys.exit(1)

SKIP = ("decisions/", "references/", "RELEASE-NOTES/", "reviews/", ".github/",
        "library/edition-maker/reviews/", "library/edition-maker/trials/")
files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.splitlines()
errs = 0
for f in sorted(files):
    if f.startswith(SKIP) or f.split("/")[-1] == "CHANGELOG.md":
        continue
    try:
        text = open(f, encoding="utf-8").read()
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        continue
    for rid, rx, rec, what in rules:
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            print(f"::error file={f},line={line}::WITHDRAWN-WORDING {rid}: \"{m.group(0)}\" was withdrawn by {rec} ({what})")
            errs += 1
if errs:
    sys.exit(1)
print(f"withdrawn-wording: no withdrawn wording in the texts ({len(rules)} rules)")
