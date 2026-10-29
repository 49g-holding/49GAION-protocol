#!/usr/bin/env python3
"""no-persian: no character of the Arabic script anywhere the public 49GAION repositories carry
text (DR-0051). Every text is in English; originals in another language stay outside the
repositories, and a translation is marked "translated from Persian".
Surfaces scanned:
  - every tracked text file: its contents and its path;
  - on a pull request: its title and body (PR_TITLE, PR_BODY) and its head branch (HEAD_REF);
  - the commits new to the change (BASE..HEAD, when BASE is a commit): their messages and their
    author and committer names and e-mail addresses. Earlier commits stay as history.
Every text is read as written and after NFKC normalisation. The script blocks: Arabic, Arabic
Supplement, Arabic Extended-A, -B and -C, Arabic Presentation Forms-A and -B, Rumi Numeral
Symbols, Arabic Mathematical Alphabetic Symbols.
Rule: PERSIAN-SCRIPT <surface>: <where>.
Usage: no_persian.py   (at the root of the repository under test; env BASE, PR_TITLE, PR_BODY, HEAD_REF)."""
import os, re, subprocess, sys, unicodedata

RANGES = [(0x0600, 0x06FF), (0x0750, 0x077F), (0x0870, 0x089F), (0x08A0, 0x08FF),
          (0xFB50, 0xFDFF), (0xFE70, 0xFEFF), (0x10E60, 0x10E7F), (0x10EC0, 0x10EFF),
          (0x1EE00, 0x1EEFF)]
PAT = re.compile("[" + "".join(f"\\U{a:08x}-\\U{b:08x}" for a, b in RANGES) + "]")

def hit(s):
    return bool(s) and (PAT.search(s) is not None or PAT.search(unicodedata.normalize("NFKC", s)) is not None)

def git(*a, check=True):
    r = subprocess.run(["git", *a], capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        print(f"::error::PERSIAN-SCRIPT unreadable: git {' '.join(a)} failed; failing closed"); sys.exit(1)
    return r

found = []
for path in git("ls-files", "-z").stdout.split("\0"):
    if not path:
        continue
    if hit(path):
        found.append(f"file name: {path}")
    try:
        data = open(path, "rb").read()
    except (IsADirectoryError, FileNotFoundError):
        continue
    if b"\0" in data:
        continue  # a binary file; no-binaries keeps them out
    text = data.decode("utf-8", errors="replace")
    for n, line in enumerate(text.splitlines(), 1):
        if hit(line):
            found.append(f"file: {path}:{n}")

for name, label in (("PR_TITLE", "pull request title"), ("PR_BODY", "pull request body"), ("HEAD_REF", "branch name")):
    if hit(os.environ.get(name, "")):
        found.append(label)

base = os.environ.get("BASE", "").strip()
if base and set(base) != {"0"} and git("cat-file", "-e", f"{base}^{{commit}}", check=False).returncode == 0:
    log = git("log", "--format=%H%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e", f"{base}..HEAD").stdout
    for rec in log.split("\x1e"):
        parts = rec.strip("\n").split("\x1f")
        if len(parts) < 6:
            continue
        sha, an, ae, cn, ce, msg = parts[:6]
        for label, value in (("author", an + " " + ae), ("committer", cn + " " + ce), ("message", msg)):
            if hit(value):
                found.append(f"commit {sha[:7]} {label}")

for f in found:
    print(f"::error::PERSIAN-SCRIPT {f}")
if found:
    sys.exit(1)
print("no-persian: no Arabic-script character in files, names, the pull request or its new commits")
