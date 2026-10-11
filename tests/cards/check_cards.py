"""Fixed test for AIOC cards (v1 B-27): a complete card must pass, an incomplete card must fail."""
import json, pathlib, sys
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
root = pathlib.Path(__file__).resolve().parents[2] / "spec" / "schemas"
schemas = {p.name: json.loads(p.read_text()) for p in root.glob("*.schema.json")}
reg = Registry().with_resources([(n, Resource.from_contents(s)) for n, s in schemas.items()] +
                                [(s["$id"], Resource.from_contents(s)) for s in schemas.values() if "$id" in s])
for n, s in schemas.items():
    Draft202012Validator.check_schema(s)
val = Draft202012Validator(schemas["aioc-card.schema.json"], registry=reg)
here = pathlib.Path(__file__).parent
ok = not list(val.iter_errors(json.loads((here / "valid-card.json").read_text())))
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
