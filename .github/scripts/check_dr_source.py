"""dr-source (DR-0053): a decision record added by a change names where it comes from.
For every decisions/DR-*.md file added between the base and the head:
  DR-SOURCE-MISSING   it has no "Source" field ("- **Source:**").
  DR-SOURCE-NO-WORDS  its Source quotes no words of the deciding seat (a quotation in straight or
                      curly double quotes, however short: "Confirmed." is a source) and cites no list it approves
                      by path and commit (a path followed by @ and a commit of 7 to 40 hex digits).
  DR-SOURCE-NO-DATE   neither its Source nor its Date field holds a date (YYYY-MM-DD, or a day,
                      a month name and a year).
Records already on the base are frozen and never judged again (dr-frozen).
Usage: check_dr_source.py <base-rev> [<head-rev>]."""
import re, subprocess, sys

base = sys.argv[1]; head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
r = subprocess.run(["git", "diff", "--name-only", "--diff-filter=A", base, head, "--", "decisions/"], capture_output=True, text=True)
if r.returncode:
    print(f"::error::DR-SOURCE-UNREADABLE: git diff {base}..{head} failed; failing closed"); sys.exit(1)
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = re.compile(rf"\b\d{{4}}-\d{{2}}-\d{{2}}\b|\b\d{{1,2}} ({MONTHS}) \d{{4}}\b")
QUOTE = re.compile("[\"\u201c][^\"\u201d\\n]*\\w[^\"\u201d\\n]*[\"\u201d]")
PATHSHA = re.compile(r"[\w./-]+@[0-9a-f]{7,40}\b")
errs = []
for path in [p for p in r.stdout.splitlines() if re.fullmatch(r"decisions/DR-\d{4}-[^/]+\.md", p)]:
    text = subprocess.run(["git", "show", f"{head}:{path}"], capture_output=True, text=True).stdout
    m = re.search(r"^- \*\*Source:\*\*(.*?)(?=^- \*\*[A-Z][^*]*:\*\*|^## |\Z)", text, re.M | re.S)
    if not m:
        errs.append(f"DR-SOURCE-MISSING {path}: no Source field"); continue
    src = m.group(1)
    datef = re.search(r"^- \*\*Date:\*\*(.*)$", text, re.M)
    if not QUOTE.search(src) and not PATHSHA.search(src):
        errs.append(f"DR-SOURCE-NO-WORDS {path}: the Source quotes no words and cites no list by path@commit")
    if not DATE.search(src) and not (datef and DATE.search(datef.group(1))):
        errs.append(f"DR-SOURCE-NO-DATE {path}: no date in Source or Date")
for e in errs:
    print(f"::error::{e}")
if errs:
    sys.exit(1)
print("dr-source: every added decision record names its source and a date")
