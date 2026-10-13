"""Fixed test for the protocol's machine forms (v1.5.0).
- Every schema is valid JSON Schema.
- Must-pass: every tests/cards/valid-*.json unit card, tests/signatures/valid-*.json and
  tests/work-items/valid-*.json validates; Library cards validate against their schema.
- Must-fail: every must-fail-*.json fails, and counts only if it fails on its own rule: the rule
  named in its "$expect" key (or in LEGACY for fixtures older than v1.5.0) appears among its
  errors (the "$comment" RULE-... of the schema rule, or the path of the failing property).
- Superseded fixtures under tests/cards/superseded/ are reported for reading only.
- Code and version patterns accept the examples and reject malformed values."""
import json, pathlib, sys
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCH = ROOT / "spec" / "schemas"
schemas = {p.name: json.loads(p.read_text()) for p in SCH.glob("*.schema.json")}
reg = Registry().with_resources([(n, Resource.from_contents(s)) for n, s in schemas.items()] +
                                [(s["$id"], Resource.from_contents(s)) for s in schemas.values() if "$id" in s])
for n, s in schemas.items():
    Draft202012Validator.check_schema(s)
V = {n: Draft202012Validator(s, registry=reg) for n, s in schemas.items()}
LEGACY = {"must-fail-pod-in-pod.json": "RULE-POD-HOLDS-CELLS", "must-fail-hoac-unit.json": "unit_kind",
          "must-fail-cell-suffix.json": "code", "must-fail-human-cell-attached-to.json": "RULE-ATTACHED-AI",
          "must-fail-pod-attached-to.json": "RULE-ATTACHED-AI"}
ok = True

def signatures(schema_name, err):
    """Rule names and property paths an error (and its sub-errors) points at."""
    out = set()
    stack = [err]
    while stack:
        e = stack.pop()
        out.add("/".join(str(x) for x in e.absolute_path))
        out.add(e.message)
        node, name = schemas[schema_name], schema_name
        for key in e.absolute_schema_path:
            if isinstance(node, dict) and "$comment" in node and str(node["$comment"]).startswith("RULE-"):
                out.add(node["$comment"].split(":")[0])
            if isinstance(node, dict) and key not in node and "$ref" in node:
                node = schemas.get(node["$ref"].split("/")[-1], {})
            try:
                node = node[key]
            except (KeyError, IndexError, TypeError):
                break
        if isinstance(node, dict) and str(node.get("$comment", "")).startswith("RULE-"):
            out.add(node["$comment"].split(":")[0])
        stack.extend(e.context or [])
    return out

def code_rules(card):
    """Rules JSON Schema cannot state: a fixed test is never owned by the part itself."""
    errs = []
    ft = card.get("fixed_test") or {}
    if card.get("unit_kind") and ft.get("owner") == card.get("code"):
        errs.append("RULE-TEST-OWNER")
    return errs

def run(folder, schema_name, extra=lambda c: []):
    global ok
    d = ROOT / folder
    for f in sorted(d.glob("valid-*.json")):
        c = json.loads(f.read_text())
        errs = [e.message for e in V[schema_name].iter_errors(c)] + extra(c)
        print(f"{folder}/{f.name}:", "valid" if not errs else f"NOT VALID {errs[:3]}"); ok &= not errs
    for f in sorted(d.glob("must-fail-*.json")):
        c = json.loads(f.read_text()); want = c.pop("$expect", None) or LEGACY.get(f.name)
        errs = list(V[schema_name].iter_errors(c)); sigs = set().union(*[signatures(schema_name, e) for e in errs]) | set(extra(c))
        hit = want is not None and any(want == s or s.startswith(want) or want in s for s in sigs)
        print(f"{folder}/{f.name}:", f"rejected on {want}" if hit else f"NOT REJECTED ON {want} (got {sorted(sigs)[:6]})"); ok &= hit

run("tests/cards", "unit-card.schema.json", code_rules)
run("tests/signatures", "signature.schema.json")
run("tests/work-items", "work-item.schema.json")
for f in sorted((ROOT / "tests/cards/superseded").glob("*.json")):
    errs = list(V["unit-card.schema.json"].iter_errors(json.loads(f.read_text())))
    print(f"superseded (reading only) {f.name}: {len(errs)} finding(s) under v1.5.0")
bad = list(V["unit-card.schema.json"].iter_errors(json.loads((ROOT / "tests/cards/incomplete-card.json").read_text())))
print("incomplete card rejected:", bool(bad)); ok &= bool(bad)

def pat(schema, prop):
    return Draft202012Validator(schemas[schema]["properties"][prop])
uc = pat("unit-card.schema.json", "code")
good = ["[ORG]AIOC-SL", "TenAIOC-SL", "[ORG]AIOC-OCO", "[ORG]POD-RV", "TenPOD-RV", "[ORG]CELL-SLCS", "TenCELL-TMS"]
badc = ["49GAION-SL", "[ORG]AIOC-", "[ORG]HOAC-GOV", "TenCELL-TMS-SL", "Ten AIOC-SL", "[ORG]AIOC-sl", "[ORG]POD-rv"]
r = all(uc.is_valid(c) for c in good) and not any(uc.is_valid(c) for c in badc); print("unit code pattern:", r); ok &= r
h = pat("unit-card.schema.json", "hoac")
r = all(h.is_valid(c) for c in ["[ORG]HOAC-GOV", "TenHOAC-TM", "[ORG]HOAC-ACS"]) and not h.is_valid("[ORG]HOAC-CEO"); print("hoac label pattern:", r); ok &= r
b = pat("bot-identity-card.schema.json", "aioc")
r = all(b.is_valid(c) for c in ["TenAIOC-SL", "[ORG]AIOC-SL", "TENAIOC-SL"]) and not any(b.is_valid(c) for c in ["TenAIOC-sl", "AIOC-SL", "Ten AIOC-SL"]); print("bot-identity aioc pattern (R13):", r); ok &= r
pv = pat("part-card.schema.json", "version")
r = all(pv.is_valid(v) for v in ["v2", "v1.3", "v1.3.0", "v1.3.0-rc1"]) and not any(pv.is_valid(v) for v in ["1.3.0", "v1.3.0.1", "v1..3", "vX"]); print("part-card version pattern (R7):", r); ok &= r

lib = ROOT / "library" / "cards"
for f in sorted(lib.glob("*.json")):
    sch = "unit-card.schema.json" if ".unit-card" in f.name else "part-card.schema.json" if "part-card" in f.name else "bot-identity-card.schema.json"
    c = json.loads(f.read_text()); errs = [e.message for e in V[sch].iter_errors(c)] + (code_rules(c) if sch.startswith("unit") else [])
    print(f"library/cards/{f.name}:", "valid" if not errs else errs[:3]); ok &= not errs

def find_enum(o):
    if isinstance(o, dict):
        if "received" in o.get("enum", []): return o["enum"]
        for v in o.values():
            r = find_enum(v)
            if r: return r
same = find_enum(schemas["work-item.schema.json"]) == schemas["status.schema.json"]["enum"]
print("work-item status list equals the shared list:", same); ok &= same
print("card-schema-test:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
