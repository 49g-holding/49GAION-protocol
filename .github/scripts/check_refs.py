#!/usr/bin/env python3
"""ref-check (on a pull request, the files it changes; on main, every file): every reference to a decision record (DR-####), a section (§N.N or
"section N.N"), a Naming Standard rule (R#), a Human Floor item (HF-##) or a delivery
test line (D-#) must point to something that exists. References to decision IDs that
exist nowhere (for example A13 or B-12) fail.
Repositories are found through HUB_DIR, PROTOCOL_DIR and AIOC_DIR (default: siblings
checked out by the workflow; the repository under test is ".")."""
import os, re, subprocess, sys, pathlib

HUB = pathlib.Path(os.environ.get("HUB_DIR", "."))
PRO = pathlib.Path(os.environ.get("PROTOCOL_DIR", "."))
AIO = pathlib.Path(os.environ.get("AIOC_DIR", "."))
DOCS = {
    "Naming Standard": HUB / "standards/49GAION-NAMING-STANDARD.md",
    "Standard": HUB / "upstream/49GAION-UPSTREAM.md",
    "Protocol": PRO / "spec/49GAION-OPERATING-PROTOCOL.md",
    "template": AIO / "template/AIOC-BLUEPRINT-TEMPLATE.md",
    "WHAT-IS-AN-AIOC": AIO / "docs/WHAT-IS-AN-AIOC.md",
    "STANDARD-CAPABILITIES": AIO / "docs/STANDARD-CAPABILITIES.md",
    "spec ": PRO / "spec/49GAION-OPERATING-PROTOCOL.md",
}
HEAD = re.compile(r"^#{1,6}\s+(?:Annex\s+)?([0-9]+(?:\.[0-9]+)*)\.?\s")

def sections(path):
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(line)
        if m:
            out.add(m.group(1))
    return out

def fail_missing(p):
    print(f"::error::reference target not found: {p}"); sys.exit(1)

secs = {}
for k, p in DOCS.items():
    if not p.exists():
        fail_missing(p)
    secs[k] = sections(p)
std_text = DOCS["Standard"].read_text(encoding="utf-8")
hf_ids = set(re.findall(r"\*\*(HF-\d\d)\*\*", std_text))
d_ids = set(re.findall(r"\|\s*(D-\d+)\s*\|", std_text))
r_ids = set(re.findall(r"^### (R\d+)\.", DOCS["Naming Standard"].read_text(encoding="utf-8"), re.M))
dr_ids = {m.group(1) for f in (HUB / "decisions").glob("DR-*.md") if (m := re.match(r"(DR-\d{4})", f.name))}

own_key = {}
for k, p in DOCS.items():
    if k == "spec ":
        continue
    try:
        own_key[str(p.resolve().relative_to(pathlib.Path(".").resolve()))] = k
    except ValueError:
        pass

files = subprocess.run(["git", "ls-files", "*.md", "*.json"], capture_output=True, text=True, check=True).stdout.split()
base = os.environ.get("BASE_SHA")
if base:  # pull request: check the files it changes; push to main checks every file
    changed = set(subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD"],
                                 capture_output=True, text=True, check=True).stdout.split())
    files = [f for f in files if f in changed]
files = [f for f in files if not re.match(r"(\.github|tests/fixtures|references)/", f)]
KEYS = sorted(DOCS, key=len, reverse=True)
SEC = re.compile(r"(?:§\s?|\bsection )([0-9]+(?:\.[0-9]+)*)")
errors = []
for f in files:
    for n, line in enumerate(pathlib.Path(f).read_text(encoding="utf-8").splitlines(), 1):
        for m in SEC.finditer(line):
            before = line[max(0, m.start() - 80):m.start()]
            best, pos = None, -1
            for k in KEYS:
                i = before.rfind(k)
                if i > pos or (i == pos and i >= 0 and best and len(k) > len(best)):
                    best, pos = k, i
            if best == "Standard" and before.rfind("Naming Standard") >= 0 and before.rfind("Naming Standard") + 7 == pos:
                best = "Naming Standard"
            key = best if pos >= 0 else own_key.get(f)
            if key is None:
                continue
            if m.group(1) not in secs[key]:
                errors.append(f"{f}:{n}: {key} §{m.group(1)} does not exist")
        for m in re.finditer(r"\bDR-\d{4}\b", line):
            if m.group(0) not in dr_ids:
                errors.append(f"{f}:{n}: decision record {m.group(0)} does not exist")
        for m in re.finditer(r"\bHF-\d\d\b", line):
            if m.group(0) not in hf_ids:
                errors.append(f"{f}:{n}: Human Floor item {m.group(0)} does not exist")
        for m in re.finditer(r"\bD-\d+\b", line):
            if m.group(0) not in d_ids:
                errors.append(f"{f}:{n}: delivery test line {m.group(0)} does not exist")
        for m in re.finditer(r"(?<![\w\[-])R\d{1,2}\b", line):
            if m.group(0) not in r_ids:
                errors.append(f"{f}:{n}: Naming Standard rule {m.group(0)} does not exist")
        for m in re.finditer(r"\b(?:decision\s+)?(?:A\d{2}|B-\d{1,3})\b", line):
            errors.append(f"{f}:{n}: reference to a decision ID that does not exist: {m.group(0)}")
if errors:
    print("\n".join(errors))
    print("::error::References to sections, rules, items or decisions that do not exist (listed above).")
    sys.exit(1)
print(f"ref-check: {len(files)} files clean; DR {sorted(dr_ids)}")
