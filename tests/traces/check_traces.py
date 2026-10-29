#!/usr/bin/env python3
"""Trace test for the event record (spec/schemas/event.schema.json), v2.2.0.

A trace is one JSON file under tests/traces/: an object whose "events" array holds the events of
the gateway's log in seq order. (JSON Lines is not used: a fixture also carries its "$comment" and,
for a must-fail trace, its "$expect".) The keys of a trace file are:
  "$comment"     one line in plain English: what the trace shows (required);
  "$expect"      must-fail traces only: the one rule ID the trace must fail on (required there);
  "type_policy"  optional: the organisation's own policy fields for listed decision types, e.g.
                 {"commit-money": {"signers_required": 2}}; they add to the signature list;
  "events"       the events (required, at least one).
Files: valid-*.json must pass with no finding; must-fail-*.json count only if they fail with exactly
the rule in "$expect" and nothing else (a schema error counts only when it is the expected rule).
policy-versions.json is the table of gateway policy tags and the commit each names. Any other JSON
file here fails the test.

Each event is first validated against the schema. A schema error reports the "$comment" RULE-...
name of the schema rule it breaks; a schema rule named RULE-<ID> for a behaviour rule <ID> (here
RULE-DECISION-BASIS) reports as <ID>, the shape half of that rule. Behaviour rules run only over a
trace whose every event passes the schema. The behaviour rules, by ID:
  TRACE-CHAIN            seq is 1 then contiguous; prev_hash is null on the first event and the hash
                         of the event before on every other; event IDs are unique; time never runs
                         backwards. The hash is "sha256:" and the hex SHA-256 of the event's
                         canonical JSON: keys sorted, no whitespace, UTF-8 (RFC 8785 for records that
                         hold no floating-point number, as the schema requires).
  CALL-WITHOUT-DECISION  a tool-call run needs a request earlier in the trace and a gateway-decision
                         "allow" naming that request as parent_call between them; one allow opens one
                         run, and the run carries the request's tool name and payload hash.
  CALL-AFTER-STOP        no allow and no run for a call whose acting position or any part of its
                         delegation chain is covered by a stop, until a restart lifts that stop.
  RESTART-BY-STOPPED     a restart never rests on an approval by a position the stop covered, or
                         made with a credential a covered position used in the trace.
  AUTHORITY-ESCALATION   a call's permission lies in the intersection of the permissions of every
                         part of its delegation chain; effective_permissions claims nothing beyond
                         that intersection; the chain starts at on_behalf_of and ends at the acting
                         position. A grant (Protocol §24, item 9) by a pos: credential goes only to
                         the position's own Chief of Staff (grantee_serves is the granting position);
                         a grant by a bot: credential rests on a grant in force to that Chief of Staff
                         that lets it give (may_grant), within its reach and end; a revocation comes
                         from the position that gave the grant.
  HUMAN-FLOOR-QUORUM     an approval of a listed type is made with a human position credential
                         (prefix pos:) and repeats its envelope's position and credential, or by that
                         position's own Chief of Staff (bot:) under a grant in force, given by the
                         position with its pos: credential, that reaches the type; it then counts as
                         the credential that signed the grant. Any other bot: and every sys: approval
                         never counts; when a call of a listed type is allowed, or a restart lifts
                         a stop (type restart-stopped-unit), the approvals bound to it (same type,
                         subject_ref and subject_sha) hold the type's quorum of distinct credentials
                         and no credential counted twice. The quorum is signers_required from the
                         trace's type_policy, else from the signature list, else 1.
  FRESH-CREDENTIAL       an approval of a listed type by a pos: credential needs a credential-in-force
                         event for that credential and position earlier in the trace whose
                         waiting_until is null or not later than the approval. A stop is never
                         delayed: a stop by a fresh credential passes.
  TAINTED-RUN            a run is tainted from a taint event that reads external content, an item
                         stored with the label external, or an item a tainted run stored
                         (write-inside) earlier in the trace. In a tainted run, an allow for a call
                         whose effect is send, publish, write-outside, new-target or permission needs
                         a clearance of that request earlier in the run (deterministic-check under a
                         sys: credential, or position under a pos: credential). Along a delegation
                         chain, no part is marked untainted after a tainted part, and no part that
                         read tainted content in the run is marked untainted.
  DECISION-BASIS         a gateway decision names a policy tag and commit, with the commit the tag
                         names in policy-versions.json, an authorising record, and an earlier
                         tool-call request as parent_call.
Listed types are the ids of the Human Floor signature list: the hub's own list when HUB_DIR is set
($HUB_DIR/upstream/human-floor-signature-types.json), else the vendored copy at
tests/fixtures/signature-list/human-floor-signature-types.json; the trace's type_policy may add types.

The test fails when any trace is not as expected, when a must-pass trace has any finding (so a
checker that always fails fails too), and when a rule has no must-fail trace (TAINTED-RUN needs at
least four) or there is no must-pass trace. Exit 0 only when every trace is as expected."""
import datetime, hashlib, json, os, pathlib, sys
from collections import defaultdict
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "tests" / "traces"
SCHEMA = json.loads((ROOT / "spec/schemas/event.schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
V = Draft202012Validator(SCHEMA)
VENDORED = ROOT / "tests/fixtures/signature-list/human-floor-signature-types.json"
RULES = ["TRACE-CHAIN", "CALL-WITHOUT-DECISION", "CALL-AFTER-STOP", "RESTART-BY-STOPPED",
         "AUTHORITY-ESCALATION", "HUMAN-FLOOR-QUORUM", "FRESH-CREDENTIAL", "TAINTED-RUN", "DECISION-BASIS"]
MIN_MUST_FAIL = {"TAINTED-RUN": 4}
GATED = {"send", "publish", "write-outside", "new-target", "permission"}
TRACE_KEYS = {"$comment", "$expect", "type_policy", "events"}


def canonical(e):
    return json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def event_hash(e):
    return "sha256:" + hashlib.sha256(canonical(e)).hexdigest()


def when(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def signature_list():
    hub = os.environ.get("HUB_DIR")
    src = pathlib.Path(hub) / "upstream/human-floor-signature-types.json" if hub else VENDORED
    if not src.exists():
        print(f"signature list not found: {src}")
        sys.exit(1)
    return {t["id"]: t for t in json.loads(src.read_text())["decision_types"]}, src


def schema_rule(err):
    """The deepest "$comment" RULE-... on the schema path of an error; RULE-<ID> of a behaviour rule reads <ID>."""
    node, found = SCHEMA, None

    def note(n):
        nonlocal found
        if isinstance(n, dict) and str(n.get("$comment", "")).startswith("RULE-"):
            found = n["$comment"].split(":")[0]
    note(node)
    for key in err.absolute_schema_path:
        if isinstance(node, dict) and key not in node and "$ref" in node:
            node = resolve(node["$ref"])
            note(node)
        try:
            node = node[key]
        except (KeyError, IndexError, TypeError):
            break
        note(node)
    found = found or "SCHEMA"
    return found[5:] if found.startswith("RULE-") and found[5:] in RULES else found


def resolve(ref):
    node = SCHEMA
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def check(trace, policy, types):
    """Findings (rule ID, message) for one trace."""
    events = trace["events"]
    F = []

    def f(rule, e, msg):
        F.append((rule, f"{e.get('event_id')} (seq {e.get('seq')}): {msg}"))

    for e in events:
        for err in V.iter_errors(e):
            f(schema_rule(err), e, err.message)
    if F:
        return F

    tp = trace.get("type_policy", {})
    listed = set(types) | set(tp)

    def quorum(dtype):
        return tp.get(dtype, {}).get("signers_required") or types.get(dtype, {}).get("signers_required") or 1

    # TRACE-CHAIN
    seen_ids, prev = set(), None
    for e in events:
        if e["event_id"] in seen_ids:
            f("TRACE-CHAIN", e, "event ID used twice")
        seen_ids.add(e["event_id"])
        if prev is None:
            if e["seq"] != 1 or e["prev_hash"] is not None:
                f("TRACE-CHAIN", e, "the first event of a trace has seq 1 and prev_hash null")
        else:
            if e["seq"] != prev["seq"] + 1:
                f("TRACE-CHAIN", e, f"seq {e['seq']} follows seq {prev['seq']}: an event is missing or out of order")
            if e["prev_hash"] != event_hash(prev):
                f("TRACE-CHAIN", e, "prev_hash is not the hash of the event before it: an event was deleted or altered")
            if when(e["time"]) < when(prev["time"]):
                f("TRACE-CHAIN", e, "time runs backwards")
        prev = e

    requests, allows, approvals = {}, defaultdict(list), {}
    by_subject = defaultdict(list)
    active_stops, in_force = {}, {}
    tainted_runs, tainted_parts, tainted_items = set(), defaultdict(set), set()
    clearances = defaultdict(list)
    creds_of = defaultdict(set)

    def covering(parts):
        return [s for s in active_stops.values() if set(s["gaion"]["covers"]) & parts]

    def parts_of(req, actor):
        g = req["gaion"]
        return {actor, g["on_behalf_of"]} | {h["part"] for h in g["delegation_chain"]}

    grants, revoked, cos_of = {}, set(), {}

    def grant_in_force(gid, at):
        gr = grants.get(gid)
        if gr is None or gid in revoked:
            return None
        end = gr["gaion"]["ends_at"]
        return gr if (end is None or when(end) > when(at)) else None

    def reaches(gr, dtype):
        return "*" in gr["gaion"]["reach"] or dtype in gr["gaion"]["reach"]

    def cos_grant(a):
        """The grant a Chief of Staff's approval rests on, if it is valid; else None."""
        ga = a["gaion"]
        gr = grant_in_force(ga.get("under_grant"), a["time"]) if ga.get("under_grant") else None
        if (gr is None or not gr["credential_ref"].startswith("pos:") or gr["position"] != ga["approver_position"]
                or gr["gaion"]["grantee"] != a["position"] or gr["gaion"]["grantee_credential"] != a["credential_ref"]
                or gr["gaion"]["grantee_serves"] != ga["approver_position"] or ga["approver_credential_id"] != a["credential_ref"]
                or not reaches(gr, ga["decision_type"])):
            return None
        return gr

    def counted(a):
        """The credential an approval counts as toward a quorum, or None when it never counts."""
        if (a["credential_ref"].startswith("pos:") and a["gaion"]["approver_position"] == a["position"]
                and a["gaion"]["approver_credential_id"] == a["credential_ref"]):
            return a["credential_ref"]
        if a["credential_ref"].startswith("bot:"):
            gr = cos_of.get(a["event_id"])
            return gr["credential_ref"] if gr else None
        return None

    def approval_counts(e, a):
        return counted(a) is not None

    def check_quorum(e, dtype, subject_ref, subject_sha, cands, what):
        valid = [a for a in cands if a["gaion"]["decision_type"] == dtype and a["gaion"]["subject_ref"] == subject_ref
                 and a["gaion"]["subject_sha"] == subject_sha and approval_counts(e, a)]
        made = [a["credential_ref"] for a in valid]
        twice = sorted({c for c in made if made.count(c) > 1})
        creds = [counted(a) for a in valid]
        if twice:
            f("HUMAN-FLOOR-QUORUM", e, f"{what}: credential {', '.join(twice)} counted twice toward the quorum of {dtype}")
        if len(set(creds)) < quorum(dtype):
            f("HUMAN-FLOOR-QUORUM", e, f"{what}: {len(set(creds))} distinct human position credential(s) approve it; {dtype} needs {quorum(dtype)}")

    for e in events:
        g, ty, run = e["gaion"], e["event_type"], e["run_id"]
        creds_of[e["position"]].add(e["credential_ref"])
        if ty == "credential-in-force":
            in_force[g["credential_id"]] = e
        elif ty == "taint":
            if (g["tainted"] or g["source_label"] == "external" or g.get("stored_label") == "external"
                    or g["source_ref"] in tainted_items):
                tainted_runs.add(run)
                tainted_parts[run].add(e["position"])
        elif ty == "clearance":
            ok = ((g["cleared_by"] == "deterministic-check" and e["credential_ref"].startswith("sys:"))
                  or (g["cleared_by"] == "position" and e["credential_ref"].startswith("pos:")))
            if ok:
                clearances[(run, g["clears"])].append(e)
        elif ty == "grant":
            if e["credential_ref"].startswith("pos:"):
                cif = in_force.get(e["credential_ref"])
                if cif is None or cif["gaion"]["for_position"] != e["position"]:
                    f("FRESH-CREDENTIAL", e, f"no credential-in-force event for {e['credential_ref']} and {e['position']} before the grant")
                if g["revokes"]:
                    old = grants.get(g["revokes"])
                    if old is None or old["position"] != e["position"]:
                        f("AUTHORITY-ESCALATION", e, f"{e['position']} revokes {g['revokes']}, a grant it did not give")
                    else:
                        revoked.add(g["revokes"])
                elif g["grantee_serves"] != e["position"]:
                    f("AUTHORITY-ESCALATION", e, f"{e['position']} grants to {g['grantee']}, which is not its own Chief of Staff (it serves {g['grantee_serves']})")
                else:
                    grants[e["event_id"]] = e
            elif e["credential_ref"].startswith("bot:"):
                parent = grant_in_force(g.get("under_grant"), e["time"]) if g.get("under_grant") else None
                if (parent is None or parent["gaion"]["grantee"] != e["position"] or parent["gaion"]["grantee_credential"] != e["credential_ref"]
                        or not parent["gaion"]["may_grant"] or g["revokes"]):
                    f("AUTHORITY-ESCALATION", e, f"{e['position']}, an AI part, gives a grant to {g['grantee']} with no grant of its position that lets it")
                elif not ("*" in parent["gaion"]["reach"] or set(g["reach"]) <= set(parent["gaion"]["reach"])):
                    f("AUTHORITY-ESCALATION", e, f"the grant to {g['grantee']} reaches {sorted(set(g['reach']) - set(parent['gaion']['reach']))}, beyond the grant it rests on")
                elif parent["gaion"]["ends_at"] and (g["ends_at"] is None or when(g["ends_at"]) > when(parent["gaion"]["ends_at"])):
                    f("AUTHORITY-ESCALATION", e, f"the grant to {g['grantee']} outlasts the grant it rests on")
                else:
                    grants[e["event_id"]] = e
            else:
                f("AUTHORITY-ESCALATION", e, "a grant is never given by a deterministic part")
        elif ty == "approval":
            approvals[e["event_id"]] = e
            by_subject[g["subject_ref"]].append(e)
            if g["decision_type"] in listed and e["credential_ref"].startswith("bot:") and g.get("under_grant"):
                gr = cos_grant(e)
                if gr is None:
                    f("HUMAN-FLOOR-QUORUM", e, f"approval of the listed type {g['decision_type']} by {e['position']} for {g['approver_position']} rests on no grant in force of that position that reaches it; it never counts")
                else:
                    cos_of[e["event_id"]] = gr
            elif g["decision_type"] in listed:
                if not e["credential_ref"].startswith("pos:"):
                    f("HUMAN-FLOOR-QUORUM", e, f"approval of the listed type {g['decision_type']} made with a non-human credential ({e['credential_ref'].split(':')[0]}:) and under no grant of a position; it never counts")
                elif g["approver_position"] != e["position"] or g["approver_credential_id"] != e["credential_ref"]:
                    f("HUMAN-FLOOR-QUORUM", e, "the approver position or credential differs from the position and credential that made the approval")
                else:
                    cif = in_force.get(e["credential_ref"])
                    if cif is None or cif["gaion"]["for_position"] != e["position"]:
                        f("FRESH-CREDENTIAL", e, f"no credential-in-force event for {e['credential_ref']} and {e['position']} before the approval")
                    elif cif["gaion"]["waiting_until"] and when(cif["gaion"]["waiting_until"]) > when(e["time"]):
                        f("FRESH-CREDENTIAL", e, f"{e['credential_ref']} is still in its waiting period until {cif['gaion']['waiting_until']}; it may not yet approve {g['decision_type']}")
        elif ty == "stop":
            active_stops[e["event_id"]] = e
        elif ty == "restart":
            stop = active_stops.get(g["lifts"])
            if stop is not None:
                refs = [approvals[r] for r in g["approval_refs"] if r in approvals]
                check_quorum(e, "restart-stopped-unit", stop["event_id"], event_hash(stop), refs, f"restart lifting {stop['event_id']}")
                covered = set(stop["gaion"]["covers"])
                covered_creds = set().union(*[creds_of[p] for p in covered])
                for a in refs:
                    if a["gaion"]["approver_position"] in covered or a["gaion"]["approver_credential_id"] in covered_creds or a["position"] in covered:
                        f("RESTART-BY-STOPPED", e, f"the restart rests on approval {a['event_id']} by {a['gaion']['approver_position']}, which the stop {stop['event_id']} covers")
                del active_stops[stop["event_id"]]
        elif ty == "tool-call" and g["phase"] == "request":
            requests[e["event_id"]] = e
            after_taint = False
            for h in g["delegation_chain"]:
                read_taint = h["part"] in tainted_parts[run]
                if after_taint and not h["taint"]:
                    f("TAINTED-RUN", e, f"{h['part']} is marked untainted after an earlier tainted part of the delegation chain")
                elif read_taint and not h["taint"]:
                    f("TAINTED-RUN", e, f"{h['part']} read tainted content in this run but is marked untainted in the delegation chain")
                after_taint = after_taint or h["taint"] or read_taint
        elif ty == "gateway-decision":
            req = requests.get(g["parent_call"])
            tag, commit = g["policy_version"]["tag"], g["policy_version"]["commit"]
            if tag not in policy:
                f("DECISION-BASIS", e, f"policy tag {tag} is not in policy-versions.json")
            elif policy[tag] != commit:
                f("DECISION-BASIS", e, f"policy commit {commit[:12]} is not the commit tag {tag} names ({policy[tag][:12]})")
            if req is None:
                f("DECISION-BASIS", e, f"parent_call {g['parent_call']} is not an earlier tool-call request")
                continue
            if g["decision"] != "allow":
                continue
            allows[req["event_id"]].append(e)
            rg = req["gaion"]
            for s in covering(parts_of(req, req["position"])):
                f("CALL-AFTER-STOP", e, f"call {req['event_id']} allowed while stop {s['event_id']} covers it")
            if run in tainted_runs and rg["effect"] in GATED and not clearances.get((run, req["event_id"])):
                f("TAINTED-RUN", e, f"{rg['effect']} call {req['event_id']} allowed in a run that read external input, with no clearance before it")
            if rg.get("decision_type") in listed:
                check_quorum(e, rg["decision_type"], req["event_id"], rg["payload_sha"], by_subject[req["event_id"]], f"call {req['event_id']}")
        elif ty == "tool-call" and g["phase"] == "run":
            req = requests.get(g["request_ref"])
            if req is None:
                f("CALL-WITHOUT-DECISION", e, f"the run names no earlier request ({g['request_ref']})")
                continue
            rg = req["gaion"]
            if not allows[req["event_id"]]:
                f("CALL-WITHOUT-DECISION", e, f"call {req['event_id']} runs with no gateway allow before it (model text alone never opens an action)")
            else:
                allows[req["event_id"]].pop(0)
            if (e["gen_ai"]["attributes"]["gen_ai.tool.name"] != req["gen_ai"]["attributes"]["gen_ai.tool.name"]
                    or g["payload_sha"] != rg["payload_sha"]):
                f("CALL-WITHOUT-DECISION", e, f"the call that runs is not the call {req['event_id']} that was judged (tool or payload differs)")
            for s in covering(parts_of(req, e["position"])):
                f("CALL-AFTER-STOP", e, f"call {req['event_id']} runs while stop {s['event_id']} covers it")
            chain = rg["delegation_chain"]
            inter = set.intersection(*[set(h["permissions"]) for h in chain])
            if chain[0]["part"] != rg["on_behalf_of"] or chain[-1]["part"] != req["position"]:
                f("AUTHORITY-ESCALATION", e, "the delegation chain does not run from on_behalf_of to the acting position")
            if rg["permission"] not in inter:
                f("AUTHORITY-ESCALATION", e, f"{req['position']} uses {rg['permission']} for {rg['on_behalf_of']}, outside the chain's intersection {sorted(inter)}")
            beyond = set(rg["effective_permissions"]) - inter
            if beyond:
                f("AUTHORITY-ESCALATION", e, f"effective_permissions claims {sorted(beyond)} beyond the chain's intersection")
            if rg["effect"] == "write-inside" and run in tainted_runs and rg.get("target_ref"):
                tainted_items.add(rg["target_ref"])
    return F


def main():
    ok, rows = True, []
    types, src = signature_list()
    policy = json.loads((HERE / "policy-versions.json").read_text())["versions"]
    print(f"signature list: {src.resolve().relative_to(ROOT) if src.resolve().is_relative_to(ROOT) else src} ({len(types)} types)")
    files = sorted(p for p in HERE.glob("*.json") if p.name != "policy-versions.json")
    n_pass = n_fail = 0
    expected_rules = defaultdict(int)
    for p in files:
        name = f"tests/traces/{p.name}"
        try:
            trace = json.loads(p.read_text())
        except json.JSONDecodeError as x:
            print(f"{name}: NOT AS EXPECTED: not JSON ({x})"); ok = False; continue
        problems = []
        if not isinstance(trace, dict) or not isinstance(trace.get("events"), list) or not trace["events"]:
            problems.append("a trace is an object with a non-empty events array")
        else:
            if set(trace) - TRACE_KEYS:
                problems.append(f"unknown keys {sorted(set(trace) - TRACE_KEYS)}")
            c = trace.get("$comment")
            if not isinstance(c, str) or not c.strip() or "\n" in c:
                problems.append("a trace carries a one-line $comment")
        if p.name.startswith("valid-"):
            n_pass += 1
            if "$expect" in trace:
                problems.append("a must-pass trace carries no $expect")
            findings = [] if problems else check(trace, policy, types)
            good = not problems and not findings
            print(f"{name}: {'pass' if good else 'NOT AS EXPECTED: must pass'}")
        elif p.name.startswith("must-fail-"):
            n_fail += 1
            want = trace.get("$expect") if isinstance(trace, dict) else None
            if not isinstance(want, str):
                problems.append("a must-fail trace names its rule in $expect")
            findings = [] if problems else check(trace, policy, types)
            got = sorted({r for r, _ in findings})
            good = not problems and got == [want]
            if good:
                expected_rules[want] += 1
            print(f"{name}: " + (f"rejected on {want}" if good else f"NOT AS EXPECTED: expected {want}, got {got or 'no finding'}"))
        else:
            findings = []
            good = False
            problems.append("a trace file is named valid-*.json or must-fail-*.json")
            print(f"{name}: NOT AS EXPECTED")
        for x in problems:
            print(f"  {x}")
        for r, m in findings:
            print(f"  {r}: {m}")
        ok &= good
    for r in RULES:
        need = MIN_MUST_FAIL.get(r, 1)
        if expected_rules[r] < need:
            print(f"COVERAGE: {r} has {expected_rules[r]} must-fail trace(s) as expected; it needs {need}")
            ok = False
    if n_pass == 0:
        print("COVERAGE: no must-pass trace")
        ok = False
    print(f"traces: {n_pass} must-pass, {n_fail} must-fail, " + ("all as expected" if ok else "NOT ALL AS EXPECTED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
