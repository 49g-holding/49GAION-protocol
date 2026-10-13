#!/usr/bin/env python3
"""Must-fail and must-pass cases for person_names.py. Uses a fictional name, never the real list."""
import os, pathlib, subprocess, sys, tempfile
S = pathlib.Path(__file__).resolve().parents[1] / "scripts/person_names.py"
NAME = "Jane Fictional\nFictional\nFictionel\n\u0698\u0627\u0646 \u0641\u0631\u0636\u06cc\n\u0641\u0631\u0636\u06cc"
res = []
def git(d, *a): subprocess.run(["git", *a], cwd=d, check=True, capture_output=True)
def case(name, line, code=None, names=NAME, unset=False):
    d = tempfile.mkdtemp(); git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "ci@example.invalid"); git(d, "config", "user.name", "ci")
    p = pathlib.Path(d, "registers/R.md"); p.parent.mkdir(); p.write_text("| seat | GOV |\n")
    git(d, "add", "-A"); git(d, "commit", "-qm", "base")
    p.write_text(p.read_text() + line + "\n"); git(d, "add", "-A"); git(d, "commit", "-qm", "head")
    env = {k: v for k, v in os.environ.items() if k != "PERSON_NAMES"}
    if not unset: env["PERSON_NAMES"] = names
    r = subprocess.run([sys.executable, str(S), "HEAD~1", "HEAD"], cwd=d, capture_output=True, text=True, env=env)
    out = r.stdout + r.stderr
    ok = (r.returncode == 0) if code is None else (r.returncode != 0 and code in out)
    if ok and code and any(w in out.lower() for w in ("fictional", "fictionel", "\u0641\u0631\u0636")): ok = False  # the matched text must never be printed
    res.append(ok); print(f"{'ok  ' if ok else 'FAIL'} person-names: {name}")
    if not ok: print("    " + out.replace("\n", "\n    "))
case("a register row naming the person fails", "| GOV | Jane Fictional |", "registers/R.md:2")
case("reversed order with a comma fails", "| GOV | FICTIONAL, Jane |", "PERSON-NAMES")
case("the given name alone passes", "| GOV | Jane |")
case("the surname alone (a listed form) fails", "| GOV | fictional |", "PERSON-NAMES")
case("a listed Latin variant fails", "| GOV | FICTIONEL |", "PERSON-NAMES")
case("a listed Persian full name fails", "| GOV | \u0698\u0627\u0646 \u0641\u0631\u0636\u06cc |", "PERSON-NAMES")
case("Persian with Arabic letter variants and a zero-width joiner fails (NFKC and folding)", "| GOV | \u0641\u0631\u0636\u200c\u064a |", "PERSON-NAMES")
case("a Persian word containing the surname passes", "| x | \u0641\u0631\u0636\u06cc\u0633\u062a\u0627\u0646 |")
case("an ordinary word containing the surname passes", "| x | Fictionalistan |")
case("a line without the name passes", "| GOV | the governing seat (GOV) of 49GAION |")
case("a name inside a longer word does not match", "| x | Janet Fictionality |")
case("an unset list fails closed", "| GOV | x |", "failing closed", unset=True)
case("an empty list fails closed", "| GOV | x |", "failing closed", names="\n  \n")
bad = res.count(False); print(f"person-names selftest: {len(res) - bad}/{len(res)} cases as expected"); sys.exit(1 if bad else 0)
