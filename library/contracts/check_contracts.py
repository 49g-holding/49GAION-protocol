"""Check the Library contracts and method catalogues (49GAION Standard §3.1, items 1, 6 and 8).

1. The design return contract: every valid-*.json in contracts/examples validates against
   design-return.schema.json, and every must-fail-*.json is refused and has its reason in
   contracts/examples/MUST-FAIL-REASONS.json.
2. The release notice contract: the same for contracts/examples/release-notice/, against
   release-notice.schema.json; and the notice_id of every example is its content address: the
   sending stage's prefix and 'N-', then the SHA-256 of the canonical notice without notice_id
   (keys sorted, separators ',' and ':', UTF-8, non-ASCII kept). A must-fail example is otherwise
   valid, so its notice_id is its content address too.
3. The reference-model catalogue: library/reference-models/reference-model-catalogue.json
   validates against its schema; every pattern carries the never-evidence sentence; no string
   names a person.
Usage: python3 library/contracts/check_contracts.py   (exit 1 on any failure)
"""
import hashlib, json, pathlib, re, sys
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent
LIB = ROOT.parent
EX = ROOT / "examples"
NEVER = "This pattern is never evidence for an organisation."
PERSON = re.compile(r"\b(person|persons|headcount)\b", re.I)


def content_ok(doc):
    nid = doc.get("notice_id", "")
    m = re.match(r"^([A-Z]{2,8}N-)", nid)
    if not m:
        return False
    body = {k: v for k, v in doc.items() if k != "notice_id"}
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return nid == m.group(1) + hashlib.sha256(canon.encode("utf-8")).hexdigest()


def check_folder(schema_file, folder, addressed):
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    v = jsonschema.Draft202012Validator(schema)
    reasons = json.loads((folder / "MUST-FAIL-REASONS.json").read_text(encoding="utf-8"))
    failures = []
    for f in sorted(folder.glob("*.json")):
        if f.name == "MUST-FAIL-REASONS.json":
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        errs = list(v.iter_errors(doc))
        if addressed and not content_ok(doc):
            failures.append(f"{folder.name}/{f.name}: notice_id is not the content address")
        if f.name.startswith("valid-") and errs:
            failures.append(f"{folder.name}/{f.name}: expected valid, got {errs[0].message}")
        elif f.name.startswith("must-fail-"):
            if not errs:
                failures.append(f"{folder.name}/{f.name}: expected refused, was valid")
            if f.name not in reasons:
                failures.append(f"{folder.name}/{f.name}: no reason in MUST-FAIL-REASONS.json")
        print(f"{schema_file}: {f.name}: {'valid' if not errs else 'refused'}")
    for name in reasons:
        if not (folder / name).exists():
            failures.append(f"{folder.name}/MUST-FAIL-REASONS.json names a missing file: {name}")
    return failures


def check_catalogue():
    d = LIB / "reference-models"
    schema = json.loads((d / "reference-model-catalogue.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    cat = json.loads((d / "reference-model-catalogue.json").read_text(encoding="utf-8"))
    failures = [f"catalogue: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(cat)]
    for p in cat.get("patterns", []):
        if p.get("never_evidence") != NEVER:
            failures.append(f"catalogue: {p.get('pattern_id')} lacks the never-evidence sentence")
        for s in json.dumps(p, ensure_ascii=False).split('"'):
            if PERSON.search(s):
                failures.append(f"catalogue: {p.get('pattern_id')} names a person: {s[:60]}")
    print(f"reference-model catalogue {cat.get('version')}: {len(cat.get('patterns', []))} patterns")
    return failures


def main():
    failures = check_folder("design-return.schema.json", EX, False)
    failures += check_folder("release-notice.schema.json", EX / "release-notice", True)
    failures += check_catalogue()
    for x in failures:
        print("FAIL", x)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
