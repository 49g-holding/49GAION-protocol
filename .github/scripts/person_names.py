#!/usr/bin/env python3
"""person-names: lines added or changed by a change must not name a person on the list.
The list is read from the environment variable PERSON_NAMES (one full name per line), set from
the repository secret of the same name. The list is never written to the log, and a hit is
reported by path and line number only, never by the matched text.
Fail closed: a missing or empty list fails (a fork pull request gets no secrets and fails).
Each listed name matches only as a full name: its parts in order or reversed, joined by
spaces, dots, commas, hyphens or underscores, case-insensitive. One part on its own never matches.
Usage: person_names.py BASE HEAD   (judges the lines HEAD adds or changes against BASE)"""
import os, re, subprocess, sys

def fail(msg):
    print(f"::error::PERSON-NAMES {msg}"); sys.exit(1)

def patterns(raw):
    pats = []
    for line in raw.splitlines():
        parts = [p for p in re.split(r"[\s.,_-]+", line.strip()) if p]
        if len(parts) < 2:
            continue
        for seq in (parts, parts[::-1]):
            pats.append(r"(?<![^\W_])" + r"[\s.,_-]*".join(map(re.escape, seq)) + r"(?![^\W_])")
    return re.compile("|".join(pats), re.I) if pats else None

def added_lines(base, head):
    out = subprocess.run(["git", "diff", "--no-color", "--no-ext-diff", "-U0", "--src-prefix=a/", "--dst-prefix=b/",
                          f"{base}...{head}"], capture_output=True, text=True, errors="replace")
    if out.returncode:
        fail("cannot read the change (git diff failed): failing closed.")
    path, n = None, 0
    for l in out.stdout.splitlines():
        if l.startswith("+++ "):
            path = None if l[4:] == "/dev/null" else l[6:]
        elif l.startswith("@@"):
            m = re.match(r"@@ -\S+ \+(\d+)", l); n = int(m.group(1))
        elif l.startswith("+") and path is not None:
            yield path, n, l[1:]; n += 1

def main():
    if len(sys.argv) != 3:
        fail("usage: person_names.py BASE HEAD")
    pat = patterns(os.environ.get("PERSON_NAMES", ""))
    if pat is None:
        fail("the PERSON_NAMES secret is missing or empty (a fork pull request gets no secrets): failing closed.")
    hits, count = [], 0
    for path, n, text in added_lines(*sys.argv[1:]):
        count += 1
        if pat.search(text):
            hits.append(f"{path}:{n}")
    for h in hits:
        print(f"::error::PERSON-NAMES a person name is on an added or changed line: {h}")
    if hits:
        print(f"PERSON-NAMES: {len(hits)} line(s) name a person. Name the seat instead, e.g. the governing seat (GOV) of 49GAION; fillers go in the private holders register.")
        sys.exit(1)
    print(f"person-names: {count} added or changed line(s) checked, none names a listed person.")

main()
