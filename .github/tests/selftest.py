#!/usr/bin/env python3
"""ci-selftest (companion): must-fail and must-pass cases for the checks of this repository.
A must-fail case counts only when it fails on its own rule with the named error in the log."""
import os, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
S = ROOT / ".github/scripts"
DEPS = os.environ.get("REF_DEPS", "")
results = []

def run(cwd, *a, env=None):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env={**os.environ, **(env or {})})

def expect(name, r, code=None):
    out = r.stdout + r.stderr
    ok = r.returncode == 0 if code is None else (r.returncode != 0 and code in out)
    results.append((name, ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}: expected {'exit 0' if code is None else 'failure with ' + code}")
    if not ok:
        print("    " + out.replace("\n", "\n    "))

# ref-check reads the escaped section sign \u00a7 in schema text
dirs = {"HUB_DIR": f"{DEPS}/hub", "PROTOCOL_DIR": f"{DEPS}/protocol", "AIOC_DIR": f"{DEPS}/aioc"}
for name, body, code in (("a valid escaped reference passes", "see Standard \\u00a74.4", None),
                         ("a broken escaped reference fails", "see Standard \\u00a799.9", "§99.9 does not exist")):
    d = pathlib.Path(tempfile.mkdtemp()) / "repo"
    shutil.copytree(ROOT, d, ignore=shutil.ignore_patterns(".git", ".deps"))
    run(d, "git", "init", "-q")
    (d / "probe.schema.json").write_text('{"description": "%s"}\n' % body)
    run(d, "git", "add", "-A")
    env = dict(dirs, BASE_SHA="")
    env[os.environ["SELF_DIR_VAR"]] = "."
    expect("ref-check: " + name, run(d, sys.executable, str(S / "check_refs.py"), env=env), code)

# template-fill (AIOC repository only)
if (S / "check_template_fill.py").exists():
    schema = f"{DEPS}/protocol/spec/schemas/unit-card.schema.json"
    fx = ROOT / ".github/tests/template-fill/complete.md"
    expect("template-fill: a complete card block passes", run(ROOT, sys.executable, str(S / "check_template_fill.py"), str(fx), schema))
    for key in ("lifecycle_state", "full_name", "lineage"):
        t = pathlib.Path(tempfile.mkdtemp()) / "missing.md"
        t.write_text("\n".join(l for l in fx.read_text().splitlines() if not l.strip().startswith(key + ":")) + "\n")
        expect(f"template-fill: removing the required key {key} fails",
               run(ROOT, sys.executable, str(S / "check_template_fill.py"), str(t), schema), f"'{key}' is a required property")

# ---------- no-persian, no-org-names variants, links (49GAION/DR-0051) ----------
def tmp_repo(files, msg="c"):
    d = pathlib.Path(tempfile.mkdtemp())
    run(d, "git", "init", "-q"); run(d, "git", "config", "user.email", "ci@example.invalid"); run(d, "git", "config", "user.name", "ci")
    (d / "a.md").write_text("clean\n"); run(d, "git", "add", "-A"); run(d, "git", "commit", "-q", "-m", "base")
    base = run(d, "git", "rev-parse", "HEAD").stdout.strip()
    for p, body in files.items():
        (d / p).parent.mkdir(parents=True, exist_ok=True); (d / p).write_text(body, encoding="utf-8")
    run(d, "git", "add", "-A"); run(d, "git", "commit", "-q", "--allow-empty", "-m", msg)
    return d, base
for name, files, code, msg, env in (
        ("a clean change passes", {"b.md": "plain\n"}, None, "c", {}),
        ("one letter of the Arabic block fails", {"b.md": "x \u0627\n"}, "PERSIAN-SCRIPT file: b.md:1", "c", {}),
        ("one presentation-form letter fails", {"b.md": "x \ufb50\n"}, "PERSIAN-SCRIPT file: b.md:1", "c", {}),
        ("one letter of Arabic Supplement fails", {"b.md": "x \u0750\n"}, "PERSIAN-SCRIPT file: b.md:1", "c", {}),
        ("a file name with one letter fails", {"\u0627.md": "plain\n"}, "PERSIAN-SCRIPT file name", "c", {}),
        ("a new commit message with one letter fails", {"b.md": "plain\n"}, "PERSIAN-SCRIPT commit", "note \u0627", {}),
        ("a pull request body with one letter fails", {"b.md": "plain\n"}, "PERSIAN-SCRIPT pull request body", "c", {"PR_BODY": "b \u0627"}),
        ("a branch name with one letter fails", {"b.md": "plain\n"}, "PERSIAN-SCRIPT branch name", "c", {"HEAD_REF": "x/\u0627"})):
    d, base = tmp_repo(files, msg)
    expect("no-persian: " + name, run(d, sys.executable, str(S / "no_persian.py"), env={"BASE": base, **env}), code)
_v = pathlib.Path(tempfile.mkdtemp()) / "variants.md"
_v.write_text("a 49 G b\nFO\u200b49G\nForty Nine Group\nthe Founder\u2019s Office\nF049G\n49-G\n", encoding="utf-8")
_n = len(run(ROOT, "bash", str(S / "no-org-names.sh"), "--lines", str(_v)).stdout.splitlines())
results.append(("no-org-names: six written variants are flagged", _n == 6))
print(f"{'ok  ' if _n == 6 else 'FAIL'} no-org-names: six written variants are flagged ({_n})")
for name, files, code in (("a link to a file of the repository passes", {"x.md": "see [b](docs/b.md#x)\n", "docs/b.md": "b\n"}, None),
                          ("a link to a missing file fails", {"x.md": "see [g](guide/OLD.md)\n"}, "LINK-DEAD guide/OLD.md"),
                          ("a link in the list of superseded wording is not followed",
                           {"x.md": "body\n\n## Superseded wording, by version\n\n- [old](guide/OLD.md)\n"}, None)):
    d, _ = tmp_repo(files)
    expect("links: " + name, run(d, sys.executable, str(S / "check_links.py")), code)

# ---------- person-names (fictional name; the real list is never used here) ----------
expect("person-names: selftest cases", subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve().parent / "person_names_selftest.py")], capture_output=True, text=True))

bad = [n for n, ok in results if not ok]
print(f"\nci-selftest: {len(results) - len(bad)}/{len(results)} cases as expected")
if bad:
    print("::error::ci-selftest: cases not as expected: " + "; ".join(bad)); sys.exit(1)
