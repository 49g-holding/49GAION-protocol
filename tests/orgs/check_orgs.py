"""Reference organisations (Protocol §4.10, items 11 and 13).

Each folder under tests/orgs/ holds one organisation's register (register.json): its parts,
the Human Floor bindings and its register events. No register records a person: who holds a
position is the organisation's own mechanism, outside the system (49GAION/DR-0049). The check expands every entry into a unit card and
validates it against spec/schemas/unit-card.schema.json, then checks the rules in force
that can be read from a register (GOV, 21 October 2026):
  GOV-SEAT       exactly one filled, unscoped Cell carrying [ORG]HOAC-GOV, seat kind human
                 (Standard §1.3, item 2)
  FLOOR-BINDING  every Human Floor item HF-01..HF-19 is bound to a filled human Cell carrying a
                 HOAC label (Standard §1.5). Two positions are two parties (GOV, 15 October 2026):
                 no check compares the persons behind positions, and none reads a compensating
                 control, which is the organisation's own (49GAION/DR-0049)
  STOP-DOOR      every part has exactly one stop door, from its card (Standard §4.3)
  CHAIN-*        every accountable_to chain is acyclic, ends at the GOV Cell, and passes at least
                 one Cell of seat kind human carrying a HOAC label; the Charter is the only part
                 with parent none; every accountable_to names a human Cell carrying a HOAC label
                 (CHAIN-TARGET) (Standard §1.7, items 12 and 13)
A reference organisation passes every check. A must-fail organisation (folder name
must-fail-*) names in "expect" the code it must fail with, and counts only if it fails with
that code. The Protocol function hoac_over(part, type, entity, date) is implemented here and
exercised by each organisation's "queries"."""
import json, pathlib, sys
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCH = ROOT / "spec/schemas"
schemas = {p.name: json.loads(p.read_text()) for p in SCH.glob("*.schema.json")}
reg = Registry().with_resources([(n, Resource.from_contents(s)) for n, s in schemas.items()])
UNIT = Draft202012Validator(schemas["unit-card.schema.json"], registry=reg)
CONFIG = json.loads((ROOT / "tests/cards/valid-aioc-card.json").read_text())["configuration"]
HF = [f"HF-{i:02d}" for i in range(1, 20)]

def ports(code, stops=1):
    b = {"unit": code, "accepted_content": ["Work Item"], "authority_limit": "as on the card", "audit_trail": "gateway log",
         "required_tests": ["TEST-PORT v1"], "enforcement": "shared-gateway-outside-unit"}
    out = [dict(b, port=n, direction=d, type=t, identification="technical-key" if t == "AI" else "live-human-sign-in-at-gateway")
           for n, d, t in (("ai-in", "input", "AI"), ("ai-out", "output", "AI"), ("hu-in", "input", "HU"), ("hu-out", "output", "HU"))]
    out += [dict(b, port=f"stop-{i}", direction="input", type="HU", identification="live-human-sign-in-at-gateway", stop_door=True) for i in range(stops)]
    return out

def card(e):
    k = e["kind"]; code = e["code"]
    c = {"unit_kind": k, "code": code, "parent": e["parent"], "full_name": e.get("name", code), "card_version": "v1", "version": "1.0.0",
         "lineage": {"id": code, "version": "1.0.0", "relation": "original"}, "lifecycle_state": "live",
         "fixed_test": {"id": "TEST-" + code.split("-")[1], "version": "v1", "owner": e.get("test_owner", e.get("accountable_to"))},
         "ports": ports(code, e.get("stop_doors", 1))}
    for f in ("accountable_to", "hoac", "top_cell", "label_holder", "decision_rule", "authority_scope", "entity", "attached_to"):
        if f in e: c[f] = e[f]
    if k == "CELL":
        c["type"] = "Human Seat" if e["seat_kind"] == "human" else "AI Agent"; c["filler_kind"] = e["seat_kind"]
    elif k == "POD":
        c["type"] = "Board"; c["inner_units"] = e.get("inner_units", [])
    else:
        c.update(type=e.get("type", "structural"), blueprint_version="v1", template_version="v1.5.0", input_door="Chief of Staff",
                 wake={"method": "queue"}, receives=[{"kind": "request", "format": "Work Item", "acceptance_test": "TEST-IN v1"}],
                 delivers=[{"kind": "result", "format": "Work Item"}], skills=[{"id": "run", "name": "Run", "tags": ["core"]}],
                 configuration=CONFIG)
    return c

CHARTER_CHANGE = {"create-or-install-unit", "retire-unit", "change-parent", "set-or-move-hoac-label",
                  "approve-change-or-promote-challenger", "restore-or-rollback"}

def hoac_over(parts, part, dtype, entity, date):
    """The Cell that signs a listed type for a part (Standard §4.4, item 8): the nearest Cell,
    along accountable_to and starting with the part's own label, whose authority_scope covers
    the type and the entity and has not expired on the event's date; never the part itself
    for its own restart, never a seat that is the subject of the action (recusal passes it up).
    For a restart it also skips every Cell inside the stopped part (by parent) or under it (by
    accountable_to), so the signer is above the stopped part (Standard §4.4, item 6)."""
    skip = {part}
    if dtype == "restart-stopped-unit":
        for c in parts:
            a, s = parts[c].get("parent"), set()
            while a and a not in s:
                if a == part: skip.add(c); break
                s.add(a); a = parts.get(a, {}).get("parent")
            a, s = parts[c].get("accountable_to"), set()
            while a and a not in s:
                if a == part: skip.add(c); break
                s.add(a); a = parts.get(a, {}).get("accountable_to")
    # Addition (49GAION/DR-0030): a change of a Pod or Cell of the Charter is GOV's (Standard §1.7, item 13)
    root = next((c for c, e in parts.items() if e["kind"] == "AIOC" and e.get("parent") == "none"), None)
    par = parts[part].get("parent")
    if dtype in CHARTER_CHANGE and parts[part]["kind"] in ("POD", "CELL") and root and (par == root or parts.get(par, {}).get("kind") == "POD" and parts[par].get("parent") == root):
        gov = next((c for c, e in parts.items() if e.get("hoac", "").endswith("HOAC-GOV") and "entity" not in (e.get("authority_scope") or {})), None)
        e = parts.get(gov, {}); sc = e.get("authority_scope")
        ok = gov and gov not in skip and e.get("seat_kind") == "human" and e.get("filled") and sc and dtype in sc["decision_types"] and sc["expires"] >= date
        return gov if ok else None
    seen, cur = set(), parts[part].get("accountable_to") if parts[part]["kind"] == "CELL" else parts[part].get("label_holder", parts[part].get("accountable_to"))
    while cur and cur not in seen:
        seen.add(cur); e = parts.get(cur)
        if e is None: return None
        sc = e.get("authority_scope")
        if e.get("hoac") and e.get("seat_kind") == "human" and e.get("filled") and cur not in skip and sc and dtype in sc["decision_types"] \
           and sc.get("entity", entity) in (entity, None) and sc["expires"] >= date:
            return cur
        cur = e.get("accountable_to")
    return None

def check(org):
    R = json.loads((org / "register.json").read_text())
    parts = {e["code"]: e for e in R["parts"]}
    errs = []
    for e in R["parts"]:
        c = card(e)
        if c["unit_kind"] == "CELL" and e.get("seat_kind") == "ai" and "fixed_test" in c:
            pass
        for x in UNIT.iter_errors(c):
            errs.append(("CARD", f"{e['code']}: {x.message[:120]}"))
        if c["fixed_test"]["owner"] in (e["code"], None) or parts.get(c["fixed_test"]["owner"], {}).get("seat_kind") == "ai":
            errs.append(("CARD-TEST-OWNER", f"{e['code']}: fixed test owner must be another human Cell"))
        if sum(1 for p in c["ports"] if p.get("stop_door")) != 1:
            errs.append(("STOP-DOOR", f"{e['code']}: needs exactly one stop door"))
    govs = [e for e in R["parts"] if e.get("hoac", "").endswith("HOAC-GOV") and not e.get("scoped_entity")]
    if len(govs) != 1 or govs[0].get("seat_kind") != "human" or not govs[0].get("filled"):
        errs.append(("GOV-SEAT", "exactly one filled, unscoped human Cell carrying [ORG]HOAC-GOV"))
    gov = govs[0]["code"] if govs else None
    for hf in HF:
        b = R["floor_bindings"].get(hf); e = parts.get(b)
        if not e or e.get("seat_kind") != "human" or not e.get("hoac") or not e.get("filled"):
            errs.append(("FLOOR-BINDING", f"{hf}: not bound to a filled human Cell carrying a HOAC label"))
    for hf in R["floor_bindings"]:
        if hf not in HF:
            errs.append(("FLOOR-BINDING", f"{hf}: cited Human Floor item does not exist in Standard §1.5 (HF-01..HF-19)"))
    # Two positions are two parties (GOV, 15 October 2026): GOV and TM are two parties whoever holds
    # them, and no compensating control is read (49GAION/DR-0049). No register records a person.
    roots = [e["code"] for e in R["parts"] if e["parent"] == "none"]
    if len(roots) != 1:
        errs.append(("CHAIN-TWO-ROOTS", f"parts with parent none: {roots}; only the Charter has none"))
    for e in R["parts"]:
        a = e.get("accountable_to"); t = parts.get(a, {})
        if a and not (t.get("kind") == "CELL" and t.get("seat_kind") == "human" and t.get("hoac")):
            errs.append(("CHAIN-TARGET", f"{e['code']}: accountable_to {a} is not a human Cell carrying a HOAC label"))
    for e in R["parts"]:
        if e["code"] == gov: continue
        path, cur, human = [e["code"]], e.get("accountable_to"), False
        while cur and cur not in path:
            path.append(cur); p = parts.get(cur)
            if p is None: break
            if p.get("hoac") and p.get("seat_kind") == "human": human = True
            if cur == gov: break
            cur = p.get("accountable_to")
        if cur in path[:-1] or (cur and cur == path[0]):
            errs.append(("CHAIN-CYCLE", f"{e['code']}: accountable_to cycle {' -> '.join(path + [cur])}")); continue
        if path[-1] != gov:
            errs.append(("CHAIN-NOT-ENDING-AT-GOV", f"{e['code']}: chain {' -> '.join(path)} does not end at the GOV Cell")); continue
        if not human:
            errs.append(("CHAIN-NO-HUMAN-HOAC", f"{e['code']}: chain passes no human Cell carrying a HOAC label"))
    for q in R.get("queries", []):
        got = hoac_over(parts, q["part"], q["type"], q.get("entity"), q["date"])
        if got != q["expect"]:
            errs.append(("HOAC-OVER", f"hoac_over({q['part']}, {q['type']}, {q.get('entity')}, {q['date']}) = {got}, expected {q['expect']}"))
    return R, errs

import os
def LOG(n, e, a, g):
    if os.environ.get("FIXTURE_LOG"): print("LOGROW\t" + "\t".join([n, e, a, "1" if g else "0"]))
ok = True
# The reference set is fixed: all four must be present and non-empty, and the cycle case
# must be present. Since 49GAION/DR-0049 the four are three-position-company, multi-entity-group,
# human-department-with-assistants and gov-and-tm-only (GOV and TM as the only human positions).
# A missing or empty folder fails (FIXTURE-ORGS-REFERENCE-MISSING).
REQUIRED = ["three-position-company", "multi-entity-group", "human-department-with-assistants",
            "gov-and-tm-only", "must-fail-cycle"]
HERE = pathlib.Path(__file__).parent
for name in REQUIRED:
    f = HERE / name / "register.json"
    try:
        good = bool(json.loads(f.read_text()).get("parts"))
    except Exception:
        good = False
    if not good:
        print(f"FIXTURE-ORGS-REFERENCE-MISSING {name}: folder missing or register empty"); ok = False
CHAIN = {"CHAIN-CYCLE", "CHAIN-NOT-ENDING-AT-GOV", "CHAIN-NO-HUMAN-HOAC", "CHAIN-TWO-ROOTS", "CHAIN-TARGET"}
orgs = sorted(p for p in HERE.iterdir() if p.is_dir())
for org in orgs:
    R, errs = check(org)
    codes = {c for c, _ in errs}
    if org.name.startswith("must-fail-"):
        hit = R["expect"] in codes
        line = " (accountability chain)" if R["expect"] in CHAIN else ""
        print(f"{org.name}: {'rejected on ' + R['expect'] + line if hit else 'NOT REJECTED ON ' + R['expect']} {[m for _, m in errs][:2]}")
        ok &= hit
        LOG(f"tests/orgs/{org.name}", f"fail {R['expect']}", "fail " + ",".join(sorted(codes)) if codes else "pass", hit)
    else:
        print(f"{org.name}: {'passes every check' if not errs else 'FAILS'}")
        for c, m in errs: print(f"   {c}: {m}")
        ok &= not errs
        LOG(f"tests/orgs/{org.name}", "pass every check", "pass" if not errs else "fail " + ",".join(sorted(codes)), not errs)
if not orgs:
    print("no reference organisations"); ok = False
print("fixture-orgs:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
