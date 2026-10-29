"""pin-lag (49GAION/DR-0053): a report, never a gate. For each Library repository it shows the
Operating Protocol release its PROTOCOL-PIN names and how many releases it lags behind the latest;
and the version of each mother the Library register (library/README.md) pins against that mother's
latest release tag. It writes a Markdown table to $GITHUB_STEP_SUMMARY (or stdout) and opens nothing.
Reads public repositories only: git ls-remote for tags, the GitHub API for one file each.
Usage: pin_lag.py   (env GH_TOKEN for the API; run at the root of 49GAION-protocol)."""
import json, os, re, subprocess, urllib.request, base64

ORG = "49g-holding"
REPOS = ["charter", "source-lifecycle", "operations-event-register", "target-operating-model",
         "process-and-position-design", "delivery-and-implementation", "product-core",
         "organisation-design-and-delivery"]
def tags(repo):
    out = subprocess.run(["git", "ls-remote", "--tags", f"https://github.com/{ORG}/{repo}.git", "refs/tags/v*"],
                         capture_output=True, text=True).stdout
    t = {}
    for line in out.splitlines():
        sha, ref = line.split("\t")
        m = re.fullmatch(r"refs/tags/(v\d+\.\d+\.\d+)(\^\{\})?", ref)
        if m and (m.group(2) or m.group(1) not in t):
            t[m.group(1)] = sha
    return t
def ver(v): return tuple(int(x) for x in v[1:].split("."))
def file(repo, path):
    req = urllib.request.Request(f"https://api.github.com/repos/{ORG}/{repo}/contents/{path}")
    if os.environ.get("GH_TOKEN"): req.add_header("Authorization", "Bearer " + os.environ["GH_TOKEN"])
    try:
        return base64.b64decode(json.load(urllib.request.urlopen(req, timeout=30))["content"]).decode()
    except Exception:
        return None
ptags = tags("49GAION-protocol")
order = sorted(ptags, key=ver); latest = order[-1] if order else None
by_sha = {s: t for t, s in ptags.items()}
reg = open("library/README.md", encoding="utf-8").read()
rows = ["| Repository | Protocol pin | Its release | Releases behind | Register pins | Latest release |", "|---|---|---|---|---|---|"]
for r in REPOS:
    name = f"49GAION-{r}"
    pin = (file(name, "PROTOCOL-PIN") or "").strip()
    rel = by_sha.get(pin, "untagged")
    behind = (len(order) - 1 - order.index(rel)) if rel in order else "?"
    m = re.search(rf"github\.com/{ORG}/{re.escape(name)}`[^|]*?(v\d+\.\d+\.\d+)", reg)
    rt = tags(name); last = sorted(rt, key=ver)[-1] if rt else "none"
    rows.append(f"| {name} | `{pin[:7] or 'none'}` | {rel} | {behind} | {m.group(1) if m else 'not in the register'} | {last} |")
text = f"### pin-lag: the latest Operating Protocol release is {latest}\n\n" + "\n".join(rows) + "\n"
out = os.environ.get("GITHUB_STEP_SUMMARY")
if out:
    open(out, "a", encoding="utf-8").write(text)
print(text)
