"""Check the Library design return contract (49GAION Standard §3.1, item 6).

Every valid-*.json example in contracts/examples must validate against its schema, and every
must-fail-*.json example must be refused and have its reason in MUST-FAIL-REASONS.json.
Usage: python3 library/contracts/check_contracts.py   (exit 1 on any failure)
"""
import json, pathlib, sys
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "design-return.schema.json").read_text(encoding="utf-8"))
EX = ROOT / "examples"


def main():
    v = jsonschema.Draft202012Validator(SCHEMA)
    jsonschema.Draft202012Validator.check_schema(SCHEMA)
    reasons = json.loads((EX / "MUST-FAIL-REASONS.json").read_text(encoding="utf-8"))
    failures = []
    for f in sorted(EX.glob("*.json")):
        if f.name == "MUST-FAIL-REASONS.json":
            continue
        errs = list(v.iter_errors(json.loads(f.read_text(encoding="utf-8"))))
        if f.name.startswith("valid-") and errs:
            failures.append(f"{f.name}: expected valid, got {errs[0].message}")
        elif f.name.startswith("must-fail-"):
            if not errs:
                failures.append(f"{f.name}: expected refused, was valid")
            if f.name not in reasons:
                failures.append(f"{f.name}: no reason in MUST-FAIL-REASONS.json")
        print(f"{f.name}: {'valid' if not errs else 'refused'}")
    for name in reasons:
        if not (EX / name).exists():
            failures.append(f"MUST-FAIL-REASONS.json names a missing file: {name}")
    for x in failures:
        print("FAIL", x)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
