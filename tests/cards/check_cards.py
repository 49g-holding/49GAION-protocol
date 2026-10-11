"""Fixed test for unit cards (AIOC and HOAC): complete cards must pass, an incomplete card and bad codes must fail; Library cards validate."""
import json, pathlib, sys
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
root = pathlib.Path(__file__).resolve().parents[2] / "spec" / "schemas"
schemas = {p.name: json.loads(p.read_text()) for p in root.glob("*.schema.json")}
reg = Registry().with_resources([(n, Resource.from_contents(s)) for n, s in schemas.items()] +
                                [(s["$id"], Resource.from_contents(s)) for s in schemas.values() if "$id" in s])
for n, s in schemas.items():
    Draft202012Validator.check_schema(s)
val = Draft202012Validator(schemas["unit-card.schema.json"], registry=reg)
here = pathlib.Path(__file__).parent
ok = all(not list(val.iter_errors(json.loads((here / n).read_text())))
         for n in ("valid-card.json", "valid-hoac-card.json"))
for n in ("valid-card.json", "valid-hoac-card.json"):
    print(n, [e.message for e in val.iter_errors(json.loads((here / n).read_text()))][:3] or "valid")
code_schema = schemas["unit-card.schema.json"]["properties"]["code"]
good_codes = ["[ORG]AIOC-SL", "TenAIOC-SL", "[ORG]AIOC-OCO", "[ORG]HOAC-GOV", "TenHOAC-GOV", "[ORG]HOAC-ACS-SL"]
bad_codes = ["49GAION-SL", "[ORG]AIOC-", "TenHOAC-CEO", "Ten AIOC-SL", "[ORG]AIOC-sl"]
cv = Draft202012Validator(code_schema)
codes_ok = all(cv.is_valid(c) for c in good_codes) and not any(cv.is_valid(c) for c in bad_codes)
print("code pattern accepts examples and rejects bad codes:", codes_ok)
ok = ok and codes_ok
bad = list(val.iter_errors(json.loads((here / "incomplete-card.json").read_text())))
print("valid card passes:", ok); print("incomplete card rejected:", bool(bad), [e.message for e in bad][:5])
lib = pathlib.Path(__file__).resolve().parents[2] / "library" / "cards"
okcards = True
for f in sorted(lib.glob("*.json")):
    sch = "part-card.schema.json" if "part-card" in f.name else "bot-identity-card.schema.json"
    errs = list(Draft202012Validator(schemas[sch], registry=reg).iter_errors(json.loads(f.read_text())))
    print(f.name, "valid" if not errs else [e.message for e in errs][:3]); okcards &= not errs
wi = schemas["work-item.schema.json"]
def find_enum(o):
    if isinstance(o, dict):
        if "received" in o.get("enum", []): return o["enum"]
        for v in o.values():
            r = find_enum(v)
            if r: return r
same = find_enum(wi) == schemas["status.schema.json"]["enum"]
print("work-item status list equals the shared list:", same)
sys.exit(0 if ok and bad and okcards and same else 1)
