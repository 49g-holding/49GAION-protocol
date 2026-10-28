"""Fixed test for the protocol's machine forms (v1.5.0).
- Since (GOV, 14 October 2026): verdict records (tests/verdicts) and standing action classes (tests/action-classes),
  must-pass and must-fail like the others.
- Every schema is valid JSON Schema.
- Must-pass: every tests/cards/valid-*.json unit card, tests/signatures/valid-*.json and
  tests/work-items/valid-*.json validates; Library cards validate against their schema.
- Must-fail: every must-fail-*.json fails, and counts only if it fails on its own rule: the rule
  named in its "$expect" key (or in LEGACY for fixtures older than v1.5.0) appears among its
  errors (the "$comment" RULE-... of the schema rule, or the path of the failing property).
- Superseded fixtures under tests/cards/superseded/ and tests/signatures/sets/superseded/ are reported for reading only.
- Since (GOV, 15 October 2026): two positions are two parties; signature sets count distinct signing
  positions other than the requesting position (SIG-DUAL), never the persons behind them.
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
ROWS = []  # (fixture, expected, actual, as expected) for the fixture log
def row(name, expected, actual, good):
    ROWS.append((name, expected, actual, good))

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
        raw = list(V[schema_name].iter_errors(c))
        errs = [e.message for e in raw] + extra(c)
        rules = sorted({s for e in raw for s in signatures(schema_name, e) if s.startswith("RULE-")} | {x for x in extra(c) if x.startswith("RULE-")})
        print(f"{folder}/{f.name}:", "valid" if not errs else f"NOT VALID {rules} {errs[:3]}"); ok &= not errs
        row(f"{folder}/{f.name}", "pass", "pass" if not errs else "fail " + ",".join(rules or ["schema"]), not errs)
    for f in sorted(d.glob("must-fail-*.json")):
        c = json.loads(f.read_text()); want = c.pop("$expect", None) or LEGACY.get(f.name)
        errs = list(V[schema_name].iter_errors(c)); sigs = set().union(*[signatures(schema_name, e) for e in errs]) | set(extra(c))
        hit = want is not None and any(want == s or s.startswith(want) or want in s for s in sigs)
        print(f"{folder}/{f.name}:", f"rejected on {want}" if hit else f"NOT REJECTED ON {want} (got {sorted(sigs)[:6]})"); ok &= hit
        got = sorted(s for s in sigs if s.startswith("RULE-") or s == want) or sorted(sigs)[:2]
        row(f"{folder}/{f.name}", f"fail {want}", ("fail " + ",".join(got)) if errs or extra(c) else "pass", hit)

run("tests/cards", "unit-card.schema.json", code_rules)
import re
def bot_rules(card):
    """A bot never signs: no allowed action may grant it a signature (RULE-BOT-NEVER-SIGNS)."""
    return ["RULE-BOT-NEVER-SIGNS"] if any(re.search(r"\bsign", a, re.I) for a in card.get("allowed_actions", [])) else []

def shared_credentials(cards):
    """RULE-CREDENTIAL-SHARED: one credential id held by more than one Cell or card."""
    seen, errs = {}, []
    for name, c in cards:
        cid = (c.get("credential") or {}).get("id")
        if cid is None: continue
        if cid in seen: errs.append(f"RULE-CREDENTIAL-SHARED {cid}: {seen[cid]} and {name}")
        else: seen[cid] = name
    return errs

run("tests/cards/bots", "bot-identity-card.schema.json", bot_rules)
_b = ROOT / "tests/cards/bots"
r = not shared_credentials([(f.name, json.loads(f.read_text())) for f in sorted(_b.glob("valid-*.json"))])
print("tests/cards/bots valid cards hold distinct credentials:", r); ok &= r
for g in sorted(p for p in _b.glob("must-fail-*") if p.is_dir()):
    cards = [(f.name, json.loads(f.read_text())) for f in sorted(g.glob("*.json"))]
    errs = [e.message for _, c in cards for e in V["bot-identity-card.schema.json"].iter_errors(c)]
    hit = bool(shared_credentials(cards)) and not errs
    print(f"tests/cards/bots/{g.name}/:", "rejected on RULE-CREDENTIAL-SHARED" if hit else "NOT REJECTED ON RULE-CREDENTIAL-SHARED"); ok &= hit
run("tests/signatures", "signature.schema.json")
run("tests/work-items", "work-item.schema.json")
def verdict_rules(v):
    """RULE-VERDICT-NON-AUTHOR: the verifier is never the producer (Protocol §8, item 5)."""
    return ["RULE-VERDICT-NON-AUTHOR"] if v.get("verifier_cell") and v.get("verifier_cell") == v.get("producer_cell") else []
run("tests/verdicts", "verdict-record.schema.json", verdict_rules)
run("tests/action-classes", "action-class.schema.json")
# Signature sets (Protocol §4.9 items 5 and 6, §4.10 item 3): rules over one action's signatures.
NEVER_HELD = re.compile(r"(^|-)(stop|disconnect|disconnection|narrow|revoke|raise)(-|$)")
def set_rules(S):
    errs = []
    ty, tgt, sigs = S["type"], S["target"], S["signatures"]
    for s in sigs:
        errs += ["SIG-SCHEMA " + e.message for e in V["signature.schema.json"].iter_errors(s)]
    if NEVER_HELD.search(ty["id"]) or ty.get("never_held"):
        errs.append("SIG-NEVER-HELD: a stop, disconnection, narrowing or revoking of AI access or raising to a human is never listed or held")
    for s in sigs:
        if s["signer_cell"] == tgt["code"]:
            errs.append(f"SIG-SELF: {s['signer_cell']} signs an action on itself")
        ent = S.get("signer_entities", {}).get(s["signer_cell"])
        if tgt.get("entity") and ent != tgt["entity"]:
            errs.append(f"SIG-ENTITY: {s['signer_cell']} (entity {ent}) signs for entity {tgt['entity']}")
    # Two positions are two parties (GOV, 15 October 2026): dual signature counts distinct signing
    # positions (signer_cell) other than the requesting position (requester_cell). The persons behind
    # positions are never compared, and no record holds a reference to one (49GAION/DR-0049).
    need = ty.get("signers_required", 1)
    if need > 1 and not S.get("requester_cell"):
        errs.append("SIG-DUAL: the requesting position (requester_cell) is not recorded")
    positions = {s["signer_cell"] for s in sigs} - {S.get("requester_cell")}
    if len(positions) < need:
        errs.append(f"SIG-DUAL: {need} distinct positions other than the requesting position needed, {len(positions)} found")
    return errs
for f in sorted((ROOT / "tests/signatures/sets").glob("*.json")):
    S = json.loads(f.read_text()); want = S.get("$expect", "pass"); errs = set_rules(S)
    codes = sorted({e.split(":")[0].split(" ")[0] for e in errs})
    good = (not errs) if want == "pass" else want in codes
    print(f"tests/signatures/sets/{f.name}:", ("valid" if not errs else errs) if want == "pass" else (f"rejected on {want}" if good else f"NOT REJECTED ON {want} {codes}"))
    row(f"tests/signatures/sets/{f.name}", want if want == "pass" else f"fail {want}", "pass" if not errs else "fail " + ",".join(codes), good); ok &= good

for f in sorted((ROOT / "tests/signatures/sets/superseded").glob("*.json")):
    errs = set_rules(json.loads(f.read_text()))
    print(f"superseded (reading only) tests/signatures/sets/superseded/{f.name}: {len(errs)} finding(s) under the rule of 15 October 2026")
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
def prow(label, v, vals, want):
    for x in vals:
        got = v.is_valid(x); row(f"pattern {label}: {x}", "accept" if want else "reject", "accept" if got else "reject", got == want)
prow("unit code", uc, good, True); prow("unit code", uc, badc, False)
h = pat("unit-card.schema.json", "hoac")
r = all(h.is_valid(c) for c in ["[ORG]HOAC-GOV", "TenHOAC-TM", "[ORG]HOAC-ACS"]) and not h.is_valid("[ORG]HOAC-CEO"); print("hoac label pattern:", r); ok &= r
b = pat("bot-identity-card.schema.json", "aioc")
r = all(b.is_valid(c) for c in ["TenAIOC-SL", "[ORG]AIOC-SL", "TENAIOC-SL"]) and not any(b.is_valid(c) for c in ["TenAIOC-sl", "AIOC-SL", "Ten AIOC-SL"]); print("bot-identity aioc pattern (R13):", r); ok &= r
prow("bot-identity aioc (widened, R13)", b, ["TenAIOC-SL", "[ORG]AIOC-SL", "TENAIOC-SL"], True); prow("bot-identity aioc (widened, R13)", b, ["TenAIOC-sl", "AIOC-SL", "Ten AIOC-SL"], False)
pv = pat("part-card.schema.json", "version")
r = all(pv.is_valid(v) for v in ["v2", "v1.3", "v1.3.0", "v1.3.0-rc1"]) and not any(pv.is_valid(v) for v in ["1.3.0", "v1.3.0.1", "v1..3", "vX"]); print("part-card version pattern (R7):", r); ok &= r
prow("part-card version (widened, R7)", pv, ["v2", "v1.3", "v1.3.0", "v1.3.0-rc1"], True); prow("part-card version (widened, R7)", pv, ["1.3.0", "v1.3.0.1", "v1..3", "vX"], False)

lib = ROOT / "library" / "cards"
for f in sorted(lib.glob("*.json")):
    sch = "unit-card.schema.json" if ".unit-card" in f.name else "part-card.schema.json" if "part-card" in f.name else "bot-identity-card.schema.json"
    c = json.loads(f.read_text()); raw = list(V[sch].iter_errors(c))
    extra_l = (code_rules(c) if sch.startswith("unit") else bot_rules(c) if "bot-identity" in sch else [])
    errs = [e.message for e in raw] + extra_l
    rules = sorted({s for e in raw for s in signatures(sch, e) if s.startswith("RULE-")} | set(extra_l))
    print(f"library/cards/{f.name}:", "valid" if not errs else f"NOT VALID {rules} {errs[:3]}"); ok &= not errs
_lib_bots = [(f.name, json.loads(f.read_text())) for f in sorted(lib.glob("*.bot-identity-card*.json"))]
r = not shared_credentials(_lib_bots); print("library bot cards hold distinct credentials:", r); ok &= r
r = not any(bot_rules(c) for _, c in _lib_bots); print("no library bot card is allowed to sign:", r); ok &= r
r = not list(lib.glob("*self-improvement*.unit-card*.json")); print("no standalone Self-Improvement unit card:", r); ok &= r

def find_enum(o):
    if isinstance(o, dict):
        if "received" in o.get("enum", []): return o["enum"]
        for v in o.values():
            r = find_enum(v)
            if r: return r
same = find_enum(schemas["work-item.schema.json"]) == schemas["status.schema.json"]["enum"]
print("work-item status list equals the shared list:", same); ok &= same

# Fixture log: every fixture of this test and of the reference organisations, expected against actual.
import subprocess
orgs = subprocess.run([sys.executable, str(ROOT / "tests/orgs/check_orgs.py")], capture_output=True, text=True, env={**__import__("os").environ, "FIXTURE_LOG": "1"})
for line in orgs.stdout.splitlines():
    if line.startswith("LOGROW\t"):
        _, n, e, a_, g = line.split("\t"); row(n, e, a_, g == "1")
print("\n===== FIXTURE LOG (fixture | expected | actual | result) =====")
for n, e, a_, g in ROWS:
    print(f"{n} | {e} | {a_} | {'as expected' if g else 'NOT AS EXPECTED'}")
print(f"===== {sum(1 for r in ROWS if r[3])}/{len(ROWS)} as expected =====\n")
ok &= all(r[3] for r in ROWS)
print("card-schema-test:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
