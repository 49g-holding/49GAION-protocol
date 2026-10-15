# 49GAION Operating Protocol

**Version `v1.5.0` · approved by the governing seat (GOV) of 49GAION.** How AIOCs, Pods, Cells and the parts of 49GAION work together, at the general level. The rules of 49GAION are in the 49GAION Standard (`49g-holding/49GAION`, `upstream/49GAION-UPSTREAM.md`); exact values (limits, timings, tools, routes) live in the Protocol of each `[ORG]AION`. Decisions are recorded once, in the hub ([`49GAION/decisions/README.md`](https://github.com/49g-holding/49GAION/blob/main/decisions/README.md)); this version follows `49GAION/DR-0002` and `49GAION/DR-0004`.

49GAION is an organisation design framework: a framework for building organisations from interchangeable AI and human parts.

**The product: `[ORG]AION`**, the AI Operating Nexus of one organisation; its one definition is in the 49GAION Standard, §1.3, item 1 ([`49GAION/upstream/49GAION-UPSTREAM.md`](https://github.com/49g-holding/49GAION/blob/main/upstream/49GAION-UPSTREAM.md)). The Protocol of each `[ORG]AION` is derived from this one: identical to it or stricter, never contradictory.

## 1. Purpose

Units exchange work automatically and with the fewest errors:
- every hand-off is a recorded **Work Item** with one owner;
- every AIOC, Pod and Cell declares, on a **card**, what it takes and what it gives; a HOAC label, where one sits on it, is a field of that card;
- every receiver **checks** what arrives and returns failures with a reason;
- every piece of work points to the **valid version** of its sources.

The protocol decides **how** work moves. **What** work happens is decided by humans: management decisions by Top Management (`[ORG]HOAC-TM`), final authority by the Governing Body (`[ORG]HOAC-GOV`) (Standard §4.2). `[ORG]HOAC-TM` is the human hub: it decides and orders. `[ORG]AIOC-OCO` (Organization Core Office) is the AI hub, under TM: every AIOC, at any depth, joins, is fixed, maintained and upgraded through it, and it gives no orders on what work is done.

## 2. The parts

| # | Part | Definition |
|---|---|---|
| 1 | **Card** | Each AIOC, Pod and Cell declares its code, its kind, its type, its HOAC label if any, its parent, its inner parts, what it receives, what it delivers and in what format. An AIOC's card lives in its blueprint. |
| 2 | **Work Item** | One hand-off: sender, receiver, requested output, the requester's acceptance test, status, exactly one owner. |
| 3 | **Shared queue** | One queue that holds every Work Item. |
| 4 | **Ports** | One input and one output of each kind (AI and HU), plus the stop door, per unit, each with a Port card (Standard §6.1); the Chief of Staff is the AIOC's voice to its HOAC seat. |
| 5 | **Input check** | The receiver's Input socket checks each arrival; failures return with a reason. |
| 6 | **Routing table** | Which kind of work goes to which AIOC. It is a map, not a table of decision rights. |
| 7 | **Wake** | Every AIOC has a runtime woken from its queue (§7). |
| 8 | **Provenance** | A Work Item links to its sources by ID and version; it never carries copied text as the source. |
| 9 | **Stop rule** | A Work Item that bounces past the limit stops (§4.4). |

**Built like a puzzle.** Every part declares a card and connects to others only through it. A process is a versioned composition of parts; replacing a part re-runs the tests of every process that uses it.

## 3. The card

1. Every AIOC, Pod and Cell, at every depth, has one card. An AIOC's card, and the cards of its Pods and Cells, are in its Blueprint. The card declares: its **code** (fixed, never changed when the part moves or its filler changes) and **kind** (`AIOC`, `POD` or `CELL`); its **type**; its **HOAC label** (`hoac`), where one sits on it; for a Cell, the **filler kind** it allows; its **parent** (the part that holds it, or `none`) and its **inner parts**, by link; what it **receives** (kind, format, acceptance test); what it **delivers** (kind, format, usual receiver); its **ports** (one input and one output of each kind, plus the stop door); for an AIOC, its **voice** (Chief of Staff), its **wake method** and its **Configuration**, including `unattended_action`; its **versions**.
2. An AIOC or a Pod is one piece from outside: one card, its ports and its stop door, of the same shape as a Cell's (Standard §1.7). A change of `parent` needs the approval of the human seat over the unit; OCO cannot make it alone (Naming Standard R14).
3. Capabilities on the card carry plain English names; the part is given by the card's own `code` field.
4. The machine form is `spec/schemas/unit-card.schema.json`, aligned with the A2A Agent Card. It accepts `unit_kind` `AIOC`, `POD` and `CELL`; a card with `unit_kind` `HOAC` is not valid, because HOAC is a label (`hoac`), not a unit.
5. A card changes only by a tested change to the blueprint. A change to what an AIOC receives or delivers names every AIOC it affects, and the cross-AIOC test is re-run.

## 4. The Work Item

### 4.1 Fields
ID; sender; receiver; requested output; acceptance test (written by the requester); status; owner; sources (ID + version + location); bounce count; parent Work Item and chain depth (for sub-items); status entered at. Machine form: `spec/schemas/work-item.schema.json`.

**Addition (GOV, 14 October 2026).** A Work Item may also carry these optional fields (`spec/schemas/work-item.schema.json`):
- `move_on`, the move-on taken while the item waits (§4.6, item 4);
- `assumptions`, each marked UNCONFIRMED, CONFIRMED or REFUTED;
- `scope`, the parts and records the item expects to change, compared with the actual change at hand-off;
- `claims`, each figure the worker wants believed, with how to reproduce it and the re-run result;
- `verdict_ref`, the verdict record it moved on (§8, item 5);
- `labels`, for example `disputed` (§4.4);
- for the type `decision-request` (§4.7, item 4): `recommendation`, `dissent`, `reversible`, `meanwhile` and `answer`.

### 4.2 Statuses
One shared list, held once in `spec/schemas/status.schema.json`:

| Status | Meaning |
|---|---|
| `received` | Arrived at the receiver's typed input port; not yet checked |
| `in-progress` | Passed the input check; being worked |
| `needs-input` | The holder cannot continue without something from another node; the reason is written |
| `objection-open` | The responsible HOAC seat holds an objection open (§4.7); no AI can close or act on it |
| `stopped` | Stopped by the stop rule or a stop door; no node may work it until a human decides |
| `done` | Delivered with visible evidence; the requester's acceptance test passed |
| `rejected` | Failed the input check, or cannot be done; the reason is written |

### 4.3 One owner, one writer
A Work Item has exactly one owner at a time, and only the owner writes to it. Ownership moves only by an explicit hand-over.

**Coordination log and leases (GOV, 14 October 2026).** Parts that share records other than Work Items keep one append-only coordination log of typed acts (open, take, done, note, ask, answer, close), each line carrying the time, the part's code, the type, what was done and a link. The first part to write "take" for an item owns it. A write that touches several records holds a lease with an expiry and a fencing token, and a stale writer is refused by the token. A part that cannot write the log leaves one immutable run file, which the next writer folds in once, by name. A lease expiry never moves a held action into execution (§4.6, item 3).

### 4.4 The stop rule

**Reading note (v1.5.0).** Where this section or §5 names the ACS or HOAC seat "of" a part that carries no label, it means the nearest HOAC above that part along `accountable_to` (§4.8).

Each return adds one to the bounce count. When the count passes the limit set in the `[ORG]AION`, the item stops and goes, with its full history, to the `[ORG]HOAC-ACS` seat of the receiving unit; if that seat is empty, to the seat that delegated it (Standard §4.1, item 5).

**Addition (GOV, 14 October 2026).**
1. **Loop breaker.** A Cell that runs the same item more than a set number of times in a set window stops on that item; the item goes to another Cell, of another engine where one exists, or is raised. In-loop fix rounds are capped. This counts runs by one Cell; the bounce count counts returns between parts.
2. **Repair tripwire.** When automated recovery acts on the same target more than a set number of times or for longer than a set time, or when the first anomaly appears on work of the highest sensitivity class, automated action on it stops and the matter is raised at once to the nearest HOAC above (Standard §4.4, item 9: raising is never held).
3. **Dispute exit.** When the bounce count of a disagreement between a producer and a verifier passes the limit, a dispute in a class the `[ORG]AION` names as sensitive goes to the nearest HOAC above with the verifier's recommendation; any other dispute may proceed with the label `disputed`, which later review samples. An objection held by a human seat (`objection-open`) is never passed this way.

### 4.5 Done
A Work Item is `done` only when the requester's acceptance test passes on visible evidence. The performing AIOC never closes its own item. An automated run of the requester's fixed test may set `done`; changing a test or its threshold is human-only (Human Floor HF-14).

**Addition (GOV, 14 October 2026).**
1. **Honest exit.** A worker that cannot meet a protected acceptance test without changing it raises a typed spec-conflict to the test's owner (a `needs-input` reason) and moves on to other work. Tests it did not write are closed to it, and changing a test stays human-only (HF-14).
2. **Unconfirmed assumption.** On an ambiguous request with no answer, a worker proceeds on reversible matters with each assumption marked UNCONFIRMED on the item and its evidence. It ships an irreversible matter only as a fail-closed stub that is switched off, and opens a new Work Item if a later answer differs.

### 4.6 Waiting time and sub-items
1. Every open status has a maximum waiting time, set in the `[ORG]AION`. An item past its deadline is reminded to its owner, then raised as in §4.4.
2. A sub-item names its parent. Chains never loop back to an AIOC already in the chain, and never exceed the maximum depth (`chain_depth`) each organisation sets in its `[ORG]AION`; this Protocol sets no fixed cap. A parent cannot be `done` while a sub-item is open.
3. **Held actions (v1.5.0).** A held action (Standard §4.4, item 9) becomes a Work Item to the delegating seat, which may sign within its own authority, under the waiting times of item 1. A held action never turns into execution because time has passed.
4. **Move-on and stub debt (GOV, 14 October 2026).** Every item that waits gets at once an owner, a due time and a move-on: a fail-closed stub, a default marked UNCONFIRMED, a mock, or the next item. Each stub or default is a debt record with an owner and an age cap; the wait clears only when the real thing replaces it; nothing stubbed reaches the outside world; the waiter may refuse an unsafe move-on. A move-on never covers a listed type or an irreversible act (item 3).
5. **Stuck-item watchdog (GOV, 14 October 2026).** A sweep with no model keeps, for every open item, the time it became ready for its next step. Past a threshold it reads the cause from the system, not from the item, and repairs from a fixed menu inside its own authority: re-queue, send to the next verifier, post the missing ask, cut the missing item. It logs one line per repair and reports every repair and every still-stuck item afterwards; one failed repair, or an unclear cause, escalates. A repair is never an approval, a merge, a release or any listed type, and never restarts a part a human stopped (Standard §4.3, item 4). Its measure is "found by a person first: zero".
6. **Stale work (GOV, 14 October 2026).** Open work past a set age is finished by a named owner within a set time, restarted from a one-page outcome, or dropped when it has no owner, under a cap on work in flight. Dropping an item a human requested is that human's decision.
7. **Human seats (GOV, 14 October 2026).** Each human seat's answer time is part of its contract (Standard §4.1); the waiting time of an item held for a human seat counts from it. A request for a personal signature that passes its time is referred to the seat's deputy, who obtains the seat's own signature and never signs in its place (Standard §4.1).

### 4.7 Requests and objections
1. An `[ORG]HOAC-ACS` seat's request about a unit's AIs goes to OCO as a Work Item of type `design-proposal`; OCO answers with a reason.
2. **The objection path.** `[ORG]HOAC-ACS` seat → OCO → discussion, where the seat may insist → where they still disagree, OCO does not decide: the seat may hold the objection open (`objection-open`) until it reaches the HOAC seat accountable for OCO, which decides (Standard §4.2, items 6-7).
3. A change to an AI's authority is decided by the `[ORG]HOAC-ACS` seat; OCO prepares, checks and carries it out.
4. **Decision request (GOV, 14 October 2026).** A matter for a human decision is a Work Item of type `decision-request` holding one recommendation, its reason, risks, whether it can be reversed, the dissent of the preparing office and what the waiting party does meanwhile. The seat answers `yes`, `veto` or `change-this-part`, which opens a new request. A veto closes the subject; only that seat or its acting filler (Standard §4.1, item 12) reopens it. For a decision of a listed type or of the highest sensitivity class, no pick or score sits on the item (Standard §5.2).

### 4.8 The accountability path
1. A report, critique, objection or stop reaches the nearest HOAC above its origin directly, from any level: from a Cell, a Pod or an AIOC at any depth.
2. The path never passes through any AI: not a Chief of Staff Cell, not OCO, not a Panel that an AI built. It runs over HU ports at the shared gateway outside the parts it passes.
3. The stop door of each Cell, Pod and AIOC is outside it. Stopping a Pod or an AIOC stops everything under it, and nothing inside can bypass the stop.
4. **Two relations (v1.5.0).** "Above", "under" and "nearest HOAC above" in this section follow `accountable_to`, never `parent` (Standard §1.7, item 12). A stop reaches everything inside the part by `parent` and everything accountable to it (Standard §4.3, items 2 and 8).
5. **Skip and recusal (v1.5.0).** A report, critique or objection may also go to any HOAC above, up to GOV, and to the independent internal-audit line (HF-19); the nearest HOAC above always also receives it. A report about a seat never has that seat as its only receiver. A seat that is the subject of a listed action, or that benefits from it, recuses, and the signature passes up one level (Standard §4.2, item 10).
6. **A stop cannot be blocked (v1.5.0).** A stop, a disconnection, narrowing or revoking AI access, and raising a matter to a human take effect at the gateway at once. They are never listed, never held, and nothing at the gateway blocks them (Standard §4.4, item 9).

### 4.9 The Human Floor signature gate
1. The Standard keeps the Human Floor signature list of decision types (Standard §4.4, item 6); an `[ORG]AION` may add types, never remove one. The tool gateway runs an action of a listed type only with a valid signature, even in an AIOC that is 100% AI. A signature is valid only from the human seat with authority over that part: the nearest HOAC above it, within its authority (Standard §4.3, item 2). For a restart of a stopped unit, the signature comes from the HOAC above the stopped unit, never from the stopped unit or anything under it. If that seat is empty or retired, the action is held, never skipped.
2. Every other AI action is logged at the gateway with the code of the accountable seat above the acting Cell.
3. An AIOC may be up to 100% AI. The organisation-wide Human Floor is set in the Standard (§1.5).
4. An `[ORG]AION` signature list sits under `org-aion-signature-types/` or is named `*.signature-types.json`, and holds its types under the key `decision_types` (Standard §4.4, item 6).
5. **Who signs (v1.5.0).** The signer of a listed type is set in Standard §4.4, item 8: the seat bound by §1.5 or a Cell to which it has delegated the type through `authority_scope`, else the label on the part within its `authority_scope`, else the nearest HOAC above whose `authority_scope` covers the action. A part never signs its own restart, and never signs an action it is the subject of. A type marked dual needs two distinct persons, neither of them the requester (HF-18).
6. **Policy fields (v1.5.0).** A type in the list may carry `related_floor`, `min_signer`, `signers_required`, `max_validity` and `never_held`. The gateway applies them as written.
7. **The loaded list (v1.5.0).** The hash of the signature list the gateway loads equals the hash of the list at the latest released tag of the Standard, plus the `[ORG]AION`'s own additions; this is checked under D-2.
8. **Signers by label (GOV, 14 October 2026).** Where an `[ORG]AION` labels items by risk (Standard §4.4), the gateway reads the label from the item's recorded flags, never from the requester, and requires the signer pair the label selects, one signature record each (§4.10, item 9).
9. **Class signature (GOV, 14 October 2026).** A standing action class (Standard §4.4) is recorded in `spec/schemas/action-class.schema.json` and signed once as `sign-standing-action-class`, its signature bound to the class version's digest. The gateway runs an action under a class only when the actor and target are in the class, the trigger is read from its own record and never from the actor's evidence, the envelope holds counted across actors and retries, and the class is neither narrowed past the action, expired nor revoked. Each use is logged with its before and after state. A narrowing applies at once as an overlay; a widening is a new version, signed again. A class whose actions map to `commit-money`, `grant-or-widen-access` or a type bound to HF-01, HF-02 or HF-15, or that is not reversible, is refused.

### 4.10 The unit register at work
1. The unit register is append-only (Standard §4.4). `[ORG]AIOC-OCO` writes AI Cell records; `[ORG]HOAC-TM` writes human Cell records. An event whose decision type is on the Human Floor signature list (for example granting or widening access, or changing a parent) is written only with that seat's valid signature (§4.9); `[ORG]AIOC-OCO` cannot write it alone. A filler change, a parent change, a retirement, and each external port's `connected` and `disconnected` events are recorded events on the existing entry.
2. The gateway opens access only for an active, filled Cell whose filler has passed the seat's fixed test, and closes it automatically on a filler change or retirement. Access never pools within a Pod.
3. A signature is recorded with the code of the Cell it is given for. Two approvals by one person under two Cells, where two people are required, are flagged and do not count as dual approval.
4. Work moves from human to AI, or from one version to the next, only when the fixed test owned by the seat passes; it moves back when the score drops below the recorded threshold.
5. **External attachments.** An external service, API or tool is not a Cell. Each connection is a port on the card of the Cell that receives (input) or sends (output), and passes only through the tool gateway. The intake Cell normalises what arrives to the AIOC's standard and has its own fixed test. Stopping or retiring the owning Cell cuts the connection automatically. An external AI agent that acts directly in the work is registered as an AI Cell whose access the organisation grants and whose stop door it holds.
6. An AI Cell attached to a person, including that person's Chief of Staff, never provides that person's signature.
7. A listed action counts as signed only when the signature is made with the human seat holder's own identity. A signature from any AI Cell's credentials, including an attached assistant, is rejected.
8. The signature is the human seat's own decision; once it is given, an AI Cell may carry out the signed action. The AI Cell's call carries a reference to that signature, and the gateway runs it only if the signature matches the exact action and is still valid.

9. **The signature record (v1.5.0).** A signature is a record holding: the decision type and the target code; the hash of the canonical action payload; the signer's Cell code and identity; the executor's Cell code; the Work Item ID; a single-use nonce; issue and expiry times; evidence of the fresh live sign-in (HF-10). The gateway runs the action only when all of these hold: the hash of the call equals the signed hash; the caller is the named executor; the nonce has not been used; the time is before expiry; the signer's Cell has not changed filler, been retired or been stopped; the signature has not been revoked. Every check is logged, including the signature's expiry against the time of execution. The record and the gateway log hold only the payload hash, Cell codes and a pseudonymous identity reference; personal data is kept in the `[ORG]AION`'s private store. A purge of personal data (HF-17) removes it from that store and never touches the log. The machine form is `spec/schemas/signature.schema.json`; its fixtures prove shape only. Replay, revocation, expiry, a wrong executor, an altered payload, and a signer Cell changed, retired or stopped are required cases of each `[ORG]AION`'s D-3 gateway delivery test, with one valid signature that passes.
10. **Signer identity (v1.5.0).** A signature carries a live sign-in, made at signing, with a phishing-resistant authenticator bound to one person. Human accounts are never shared. A deputy signs under their own identity and the Cell's code, by a recorded delegation with a scope and an end date. No AI administers the identity issuer of human seats.
11. **hoac_over (v1.5.0).** `hoac_over(part, type, entity, date)` returns the Cell that signs an action of a listed type on a part: it walks `accountable_to` from the part, starting with the part's own label holder, and returns the first filled human Cell carrying a HOAC label whose `authority_scope` covers the type and the entity and has not expired on the date of the event. It never returns the part itself for its own restart, nor a seat that is the subject of the action. It returns nothing when no such Cell exists, and the action is then held. For a restart of a stopped part it skips the part and every Cell inside it or accountable to it, and returns the first such Cell above it (Standard §4.4, item 6). A Cell's `authority_scope` covers a type whose Human Floor item the Standard binds to another seat (Standard §1.5) only by that seat's recorded delegation (Standard §4.4, item 8). Its reference implementation is `tests/orgs/check_orgs.py`.
12. **Register writes (v1.5.0).** Creating an AI Cell, changing its filler, ports or authority limit, and retiring it are listed types, signed by the HOAC the Cell is accountable to; access opens only after that event and after the filler passes a fixed test whose owner is a human Cell, never the Cell itself or an AI Cell. `[ORG]AIOC-OCO` never writes the records of its own Cells, of the AI Cells serving the Self-Improvement process in TM or of the assurance unit without `[ORG]HOAC-TM`'s signature. AIOC and Pod entries are written by OCO only with the signature of the HOAC they are accountable to. A change of filler kind is written by both writers. TM's own Cells are written with GOV's signature; GOV's Cell is written by the constituting authority (Standard §4.4, item 3).
13. **Reference organisations (v1.5.0).** Four reference organisations under `tests/orgs/` pass the card tests and the delivery test lines of Standard §1.4, including the line on the accountability chain: a three-person company; a multi-entity group; a human department with AI assistants; and one person filling GOV and TM under a compensating control. Must-fail organisations (a cycle, a chain not ending at GOV, a chain with no human HOAC seat, two parts with parent none, one person in GOV and TM without a control, a binding to a Human Floor item that does not exist, an `accountable_to` naming a part that is not a human Cell carrying a HOAC label) fail on the rule they name. Signature sets under `tests/signatures/sets/` check dual signature by distinct persons other than the requester, types that are never held, self-signing and the entity of the signer; `tests/cards/check_cards.py` prints a fixture log of every fixture with its expected and actual result.
14. **Intent before effect (GOV, 14 October 2026).** Before any side effect, the gateway writes the intent of the action (actor, version, target, digest, trigger reference, action ID) to its append-only log; if the intent cannot be written, nothing runs. A stop, a cut-off, a revocation, a narrowing or a raise to a human is never held by a failed intent write: it runs at once, and its record is written as soon as the log is back (Standard §4.4, item 9). After the effect it writes the verified outcome with the before and after state. A lost acknowledgement marks the action Unknown and starts reconciliation against the real state, never a blind replay. Every executed action records its inverse for the recovery path (§15).
15. **Correction fence (GOV, 14 October 2026).** A correction never changes the decision fields of a signed event (answer, words, slot, version, amount, class); a changed decision is a new event, and the corrected record keeps its original visible.

16. **Position codes only (GOV, 15 October 2026).** Every HOAC reference and every field that points to a human seat (for example `accountable_to`, `label_holder`, `attached_to`, a signer's seat) takes a position code only, never a person. The Position Principle and the HOAC Arrangement Models are in Standard §5.2. The models are three (GOV, 15 October 2026): Solo, Team and Overseen; a model stays only if it changes who decides or the result of a decision, and a future model is admitted only under that test. No other model name is accepted, and no withdrawn name maps to a new one. A temporary, backup or rotating occupant is an occupancy rule, not a model: each change is an occupancy entry (item 17).
17. **What the register follows (GOV, 15 October 2026).** The unit register follows (a) who held each position at each moment, as occupancy entries with a valid time and a recorded time, corrected only by new entries; and (b) the full transfer of everything the position carries (effects, achievements, losses, commitments and open work) on a change of occupant, as a handover entry listing what passed. Occupancy and handover entries carry internal person IDs and stay in the organisation's private register copy; position and arrangement entries carry no people.
18. **Occupants resolved at action time (GOV, 15 October 2026).** The gateway resolves a position's occupant or occupants at the moment of the action, and stamps each signed decision with the position code and the occupant ID or IDs at that moment.
   - **Team signing (GOV, 15 October 2026).** A position held by more than one holder carries a recorded signing rule (any one, majority or all), and the gateway applies it. Every decision stamp carries one named accountable member, filled at signing, who must be a current occupant of the position; a stamp without one, or naming someone who is not a current occupant, is rejected.
   - **Overseen, pre (GOV, 15 October 2026).** The action waits at the gateway until the overseeing position clears it, or until the recorded hold window lapses with no stop. A clearance is a stamped decision (overseeing position, occupant IDs, time). A lapse writes a "window lapsed, no stop" entry and counts only if the overseeing position has a holder at that moment and a window is recorded.
   - **Overseen, post (GOV, 15 October 2026).** The action runs; it is reversed only by a new signed decision that references the identifier of the reversed decision. The original stays and is marked reversed.
   - **Irreversible actions (GOV, 15 October 2026).** The gateway marks each tool action reversible or not. An irreversible tool action (a sent message, a payment, a deletion) under Overseen always goes through pre, whatever timing form is recorded.
19. **Who may change an arrangement (GOV, 15 October 2026).** The gateway accepts an arrangement change for a position below `[ORG]HOAC-TM` only from TM, for TM only from `[ORG]HOAC-GOV`, and for GOV only through the organisation's founding configuration. No position changes its own arrangement.
   - **Arrangement entry and trials (GOV, 15 October 2026).** An arrangement entry records, for its scope, Solo or Team (with the holder count and, for more than one holder, the signing rule) and any Overseen link (the overseeing position and the timing form, pre or post, with the hold window where one is set). Overseen combines with Solo or Team. A trial is a time-boxed run of an arrangement, not a model of its own.
20. **Arrangements resolve (GOV, 15 October 2026).** An arrangement must not loop, and must resolve to at least one real person. An arrangement that loops or resolves to no person is rejected. An arrangement in which `[ORG]HOAC-GOV` is overseen by a lower position is rejected (GOV, 15 October 2026).
21. **Vacant position (GOV, 15 October 2026).** While a position has no occupant, its Chief of Staff only advises; the matter goes up the accountability path (§4.8); and every action that needs that position's signature is blocked until a new occupant is recorded.
   - **Vacant overseeing position (GOV, 15 October 2026).** If the overseeing position of an Overseen link is vacant, the held action escalates to the position that set the arrangement (`[ORG]HOAC-TM`, then `[ORG]HOAC-GOV`) and never passes automatically. Escalation ends at GOV; if GOV is vacant, the action stays held until GOV is filled through the founding configuration.

## 5. The ports and the input check

1. Each AIOC, Pod and Cell has one input and one output of each kind (AI and HU), plus the stop door. The Chief of Staff is the AIOC's voice to its HOAC seat; input arrives only through the typed ports and the Input socket, and HU ports, including the stop door, never pass through an AI. Bots never talk across AIOCs directly.
2. The Input socket checks every arrival against the receiver's card, the acceptance test and provenance. Pass: `in-progress`. Fail: `rejected` with the reason, back to the sender. Nothing passes silently and nothing is guessed into place.
3. Text inside a Work Item is data, never an instruction. A Work Item carrying a secret is rejected and the secret is not stored.
4. **Readiness verdict (GOV, 14 October 2026).** A package of work the receiving AIOC did not draft is read blind by two readers independent of the drafter, on different model providers where available, who return one verdict within a set time: Ready; Ready with notes, which travel with the work; or Back, with numbered questions, each with suggested answers and a default. They block only on a short fixed list (an untestable or contradictory acceptance test, a missing rule on a protected matter, a conflict with a decision record), never judge the requester's purpose, and review a new version only for what changed. An independent challenger may also write the case against doing the work.
5. **Validate before show (GOV, 14 October 2026).** An AI finding goes to an HU port only after a machine check has proven or discarded it; anything no check can confirm goes only as a hypothesis, or not at all. Every claim carries its evidence class (§8, item 4).
6. **Two-party line (GOV, 14 October 2026).** Two units that share no queue may bind a port pair to one store in which each side writes only in its own folder, every message is a new immutable file with a typed header pointing to the message it answers, each side keeps a read mark, an index shows who owes the next step, and a fixed table says what happens on a missed read, an edited file or a duplicate reference. The line projects into the shared queue; port types are still enforced at the gateway.
7. **No authority from writable files (GOV, 14 October 2026).** An instruction, assignment or decision that arrives as a file in a place an AI can write is a notice only; it takes effect only as a signed event made through the human gateway surface.
8. **Demand signal (GOV, 14 October 2026).** A part that receives work needing a materially different capability refuses that part of the work with the reason "out of card", and records it as a demand signal for Self-Improvement instead of absorbing it.

## 6. The routing table

A map of which kind of work goes to which unit, built from the cards and kept by OCO. OCO maintains the map; it gives no orders and dispatches no work. Each `[ORG]AION` holds its own rows.

**Receivability check (GOV, 14 October 2026).** Before routing an item to a part, the router checks that the part's installed version equals the approved version, that it has the access the item needs, that it is awake on this route, and that nobody has taken the item; a mismatch is a refusal with its reason.

## 7. Wake

Every AIOC has its own runtime, woken from its queue. With no human present, a woken Chief of Staff reads, records and triages only, unless the AIOC's Configuration slot `unattended_action`, set by the accountable human, allows more.

**Addition (GOV, 14 October 2026).**
1. **Zero-cost wake.** A woken Cell first checks for work with no model call and holds a single-run lock; a model runs only when there is work. Every unattended Cell declares its cadence and is flagged when its newest output is older than twice it.
2. **Delegation ladder.** Beyond `read-record-triage` and `act-within-limits`, the `unattended_action` slot may hold a ladder: for each class of act, decides alone, decides and reports, only prepares, or never. The level covering an act is read from the act itself; every listed type is "never" (Standard §5.2).

## 8. Provenance

1. A Work Item links to its sources by ID, version and location.
2. The receiver reads the valid version at the controlling copy; a link that does not resolve to exactly one valid version fails the input check.
3. Output returns labelled with the sources and versions it was made from.
4. **Evidence class (GOV, 14 October 2026).** Every claim in an output carries one evidence class: proven, measured, cited, hypothesis or not established; a fact that could not be extracted is "not extracted", never guessed.
5. **Verdict record (GOV, 14 October 2026).** A verification is a record written by the verifier's own step, bound to the full content hash of the exact version read (`spec/schemas/verdict-record.schema.json`); a new version voids it; queues and tools act only on such records, never on the text of a note; a blocking verdict names a failing check the verifier wrote and returns the item to its producer; an advice-only verdict never counts as an approval; the verifier is never the producer.
6. **Completion ladder (GOV, 14 October 2026).** Drafted, adopted, executed and implemented are separate states, each reached only by its own recorded event; a register row is not evidence.
7. **Staleness and precedence (GOV, 14 October 2026).** A derived artefact (a knowledge pack, an installed instruction, a summary) is stale as soon as a source it depends on is newer, and is not relied on until regenerated. When sources disagree, the `[ORG]AION`'s fixed precedence applies, and a conflict it cannot resolve goes to a human.
8. **Generated values (GOV, 14 October 2026).** Every figure, hash, count or identifier in a record is read from what produced it, never retyped.
9. **Request package (GOV, 14 October 2026).** A request between units may travel as an immutable, versioned package holding:
   - a machine-checkable header;
   - the requester's words verbatim, with the interpretation beside them;
   - numbered acceptance criteria;
   - numbered rules, each with its source;
   - a declared scope;
   - a hash manifest of every attached file.

   A change is a new version. Work tied to a superseded version pauses by itself, and a verifier fails a result built on it.
10. **Known-failure register (GOV, 14 October 2026).** A register of past failures, vendor behaviour and never-again decisions, each with its source, is attached by area to every new Work Item at planning. It holds what cannot yet be a test, and it is never the only holder of a relationship or of tacit knowledge (HF-13).

## 9. Ports, bootstrap and stop

The definitions are in the Standard: ports (§6.1), bootstrap (§5.3), stop (§4.3). The machine form of the Port card is `spec/schemas/port-card.schema.json`. Every AIOC, Pod and Cell has a mandatory, queue-less stop port of type HU (the stop door), enforced outside it. Stopping an AIOC or a Pod stops everything under it, and no inner part can bypass the stop (§4.8); a human port never passes through an AI unit; a stopped unit restarts only by human decision. OCO sits under `[ORG]HOAC-TM`: TM and `[ORG]HOAC-GOV` may each stop it; a stop by TM comes directly through a human port, never through a Panel that OCO built; no AI can restart a stopped OCO (Standard §4.2, item 4; §4.3, item 2). Every `[ORG]AION` is handed over only when its `[ORG]HOAC-GOV`, its Human Floor and the stop ports of all its units are in place (Standard §1.4).

## 10. `[ORG]AION` and the Library

1. Each `[ORG]AION` records which Standard, Protocol and Library versions it is based on, the parts it took, its Library harvest and its delivery test (`spec/schemas/org-aion-record.schema.json`). At delivery its Standard is identical to the 49GAION Standard or stricter, never contradictory.
2. No `[ORG]AION` sees another `[ORG]AION`'s data.
3. Each Library part has a card (inputs, outputs, test, version); tests travel with their parts (`spec/schemas/part-card.schema.json`). Every bot has an identity card (`spec/schemas/bot-identity-card.schema.json`). The cards of the AION Builder and of the Self-Improvement AIOC held within `[ORG]HOAC-TM` are in `library/cards/`. A card stays `DRAFT` until its test has run once with recorded evidence.
   - **Addition (v1.5.0).** Every bot has its own credential, issued to it alone, held by the one Cell it fills, and never shared or reused (`credential` on its v3 identity card). A bot never signs: this covers every bot, in an AI Cell, an attached AI Cell or a Chief of Staff Cell (`never_signs: true`); no signature record (§4.10) names a bot as signer. Stopping a part under the stop rule (§4.4) is not a signature. When the filler of a Cell changes, the bot's memory of the previous filler is sealed, never purged.
   - **Correction (v1.5.0).** There is no standalone Self-Improvement unit or unit card. Self-Improvement is a process held inside `[ORG]HOAC-TM` (Standard §2.1, item 6): its fields are recorded only on the card of the Cell carrying `[ORG]HOAC-TM`, under `processes`, and it is served by AI Cells, read as "AI Cells serving the Self-Improvement process in TM" wherever a text says "the Self-Improvement AIOC". Its access to records is an access rule, not a signature type: read-only, pseudonymised, with no private store, and changed only as a Work Item (`processes[].access`).
   - **Addition (GOV, 14 October 2026).** The card of 49GAION Source Lifecycle, `source-lifecycle.part-card.json`, is also in `library/cards/` (§13).
   - **Addition (GOV, 15 October 2026).** The card of 49GAION Process and Position Design, `process-and-position-design.part-card.json`, is also in `library/cards/` (§17).
4. During design, the AION Builder adds the blueprint of any capability not already in the 49GAION Library back to the 49GAION Library, generalised and tested. Once delivered, the `[ORG]AION` belongs entirely to the customer.
5. The Standard names roles only; tool names appear only in an `[ORG]AION`.
6. All AIOCs reach AI models through one shared gateway that holds keys, meters cost per AIOC and logs every call. It carries no orders.
   - **Reading note (v1.5.0).** The shared gateway is the tool gateway of each `[ORG]AION`, a registered part held in the Charter and outside every other AIOC (Standard §4.4, item 11); 49GAION runs no gateway for an `[ORG]AION`. HU ports and the stop door are served there through a sign-in that no AI built, hosts or can change (Standard §6.1, item 6).
   - **Reading note (DR-0007).** 'outside every AIOC' (DR-0007 item 8) is read with the root rule (Standard §1.7, item 13): the gateway is held in the Charter and sits outside every other AIOC.
7. **Runtime contract and engine binding (GOV, 14 October 2026).** One versioned runner performs the common duties of every AI Cell in a clean workspace per run; each Cell pins its runner version. A Cell's engine binding (tier, floor, model) is versioned on its card (`engine_binding`) and switches at the next run, never mid-task. Engines are re-scored on a schedule against a frozen set of past cases; a regression demotes an engine at once (Standard §5.1).
8. **Spend (GOV, 14 October 2026).** The gateway keeps decided spend, standing commitments and metered usage as separate numbers, billed and notional apart; applies the soft hold at a set fraction of a cap; pauses a Cell past its cap alone; at the global cap holds only new non-critical starts; and keeps the last caps when its meter fails. Each capability's degradation order is read from its blueprint.

## 11. Joining and tests

1. **Joining test.** An AIOC receives work only after every input and output on its card passes fixed samples; failing claims are removed from the card. An AIOC with an empty Configuration slot does not join.
2. **Cross-AIOC test.** A fixed set of chains across AIOCs is re-run after every change to a card, the protocol or a shared part.
3. **Outside tools** are re-tested against known samples; a tool that fails is disconnected.
4. **Verification by a non-author (GOV, 14 October 2026).** Work is verified by a Cell that did not produce it, on another model provider where one exists, in a fresh context, with the producer's description withheld; it restates the acceptance test and writes its own checks first; one non-author pass suffices; when a verifier is unavailable the next in a fixed list verifies; a fixed share of closed items is re-verified at random.
5. **Fresh-instance and duty-carriage tests (GOV, 14 October 2026).** On every change to a definition, a fresh instance is built from the definition alone and run against the fixed tests; every duty a role card gives a position is traced to a process step, an event or a setting, and a duty with no carrier fails the unit's fixed test.
6. **Deterministic executor (GOV, 14 October 2026).** A routine, consequential action that is not a listed type is carried out only by a program with no model, on machine-readable preconditions (verified at the exact version, all checks green on the combined result, not held, not stopped), with one kill switch. Only a deterministic re-run of a registered check opens an action; a model's words are evidence, never authority.
7. **Check placement (GOV, 14 October 2026).** Every automated check that is not a fixed test declares its placement, its budget per item and its degradation order, and is advisory unless it shows a real defect (Standard §3.2).

## 12. Alignment

The card follows the A2A Agent Card; the Work Item follows the A2A task. The parts answer the failure categories of the MAST study (arXiv 2503.13657): cards and Work Items for specification failures, typed ports and one owner for misalignment between agents, the input check and visible evidence for failed verification.

## 13. Source Lifecycle: the first stage

**Addition (GOV, 14 October 2026).** 49GAION Source Lifecycle is a Library part (`library/cards/source-lifecycle.part-card.json`). In an `[ORG]AION` it is the AIOC `[ORG]AIOC-SL` (Naming Standard R2).

1. **The first part.** It is the first part an organisation receives after the Charter, with the GOV, TM and OCO installed in it (Standard §1.7, item 13; §5.3). Like every other part, it enters through OCO. It is the stage through which every source enters.
   - It works for any organisation, from a single person to a group of entities.
   - Every later part builds on it.
   - **Reading note (GOV, 14 October 2026).** "with the GOV, TM and OCO installed in it" reads as "with `[ORG]HOAC-GOV`, `[ORG]HOAC-TM` and `[ORG]AIOC-OCO` installed in it".
2. **What it takes.** Documents and files of any format, and a contributor's own words, by text, chat or voice.
   - Each contributor accepts an agreement before their first input. An input made before that is refused.
   - Words become a record only after the contributor approves a preview of the exact text. With no approval, nothing is recorded. Human silence is never consent.
   - A secret in any input is refused and appears in no record or log (§5, item 3).
3. **What it does.**
   - It registers every input, gives it a reference and classifies it.
   - It fixes each input through its own stages, so that each source has one valid version (§8).
   - It tells the organisation what is missing for that kind of organisation.
   - The sources are the organisation's own data and never enter the 49GAION Library (Standard §1.3, item 9).
4. **Its sockets.**
   - **Input socket.** It checks everything that arrives (§5; STANDARD-CAPABILITIES §4.3).
   - **Output socket.** It answers a connected part by reference (ID, version and hash). The answer is "held" or "not held", and covers only the scope approved under item 5.
5. **Connections.**
   - **Approval and scope.** A part connects only by request.
     - The `[ORG]HOAC-ACS` seat that `[ORG]AIOC-SL` is accountable to approves the request and sets its scope, as the listed type `connect-external-port` (§4.9).
     - A wider scope is the listed type `grant-or-widen-access`.
     - No bot approves a request or sets a scope; a bot never signs (§10, item 3).
   - **Revocation.** That seat, or any seat above it, may revoke a connection at any time.
     - Revocation takes effect at the tool gateway first, and is never held or blocked (§4.8, item 6).
     - It invalidates the connection's token at the source service.
     - A read through a revoked connection is refused.
   - **Gateway.** Every source connection runs through the tool gateway, held in the Charter (Standard §4.4, item 11). No AIOC calls a source service directly.
     - A stop takes effect at the gateway first, and is never blocked.
     - The expiry of a scope is checked against the date of each read.
   - **Token.** A connection's token is held only in the platform's secret store or behind the tool gateway. Each connection has its own token, with least privilege. A token is never written to any file, record or log.
   - **Register.** Every connection, scope change and revocation is recorded as an event in the unit register, which is append-only (Standard §4.4, items 2 and 7). Each event carries its date, its scope and the approving seat.
6. **Then the next stage starts.**
   - The next stage takes its sources through its own input socket, from Source Lifecycle's output socket. A document store the organisation already keeps may be connected the same way.
   - What the next stage lacks, it asks for through Source Lifecycle, which records the answer as a source.
   - What reaches the next stage is therefore documented, versioned and traceable to its source.
7. **Replaceable in later stages.** Source Lifecycle is a part like any other (§2). In the stages after the first, another source of documents or knowledge may replace it or stand beside it. Examples:
   - a document management system the organisation already uses;
   - a version-controlled repository of its texts;
   - a knowledge base;
   - a records or archive system the organisation already keeps.

   Such a source qualifies only when it uses the same sockets, follows item 5, and passes the joining test (§11). It must:
   - answer by reference (ID, version and hash);
   - answer "held" or "not held";
   - serve only the approved scope.

   Tool names appear only in an `[ORG]AION` (§10, item 5).
   - **Reading note (GOV, 14 October 2026).** The joining test is defined in §11, item 1 (Standard §3.2, item 4).
8. **The fixed test.** Every rule of this section has a case in TEST-SOURCE-LIFECYCLE (`library/cards/README.md`). The card stays `DRAFT`, with `last_result` `NOT_RUN`, until the test has run once with recorded evidence (§10, item 3).

## 14. Records

**Addition (GOV, 14 October 2026).**
1. **One home.** An AIOC's records live in one home as immutable events. Each event carries a time-sortable ID, which is also its idempotency key, the actor's Cell code and the expected revision. Two writes on the same revision are both kept: the first applies and the later becomes a question to its author.
2. **Portals and projections.** Every register, board and number is a projection rebuilt from the events, carrying the version of the logic that built it. Every surface is a portal and keeps no copy. A write shows first as "not yet joined" and, if it fails the rules at join, as "refused at join" with the rule's ID. A change made in a projection is a request, checked before it becomes an event.
3. **Registry.** One machine-readable registry declares every record type, field, state, event, emitter and condition; a write it does not allow is refused, and the refusal names every condition that fails.
4. **Numbering.** One numbering service issues every readable number, a stream per type, atomically and safe to retry; no writer mints its own.
5. **Daily check.** A daily job proves that projections equal a rebuild from the events, that no number stream has gaps or duplicates, that every act is attributed to a part, and that every reported number traces to its events. A failure opens a defect and stays flagged.
6. **Restricted partition.** Records that name a person or carry the particulars of a corporate act live in a separate store read by named positions; every other record refers to them by ID only (Standard §4.4).
7. **State snapshot and rules in force.** On every change the unit publishes one human-readable and one machine-readable snapshot from its registers, keeping one line in its accountable human's own words, and stops publication if a personal name or contact would appear. For every position, a generator builds the rules in force today with a fixed precedence and marks superseded and lapsed items.
8. **Mechanism register and Reserve.** The unit's register of mechanisms and its Reserve of ideas not adopted are records like any other (Standard §2.1, §3.2).

## 15. Halt, pause and cut-off at work

**Addition (GOV, 14 October 2026).**
1. **The control record.** One control record per scope holds the state (running, draining, paused, resuming), the grace time and the reason. Every runtime reads it before every start and every step. On draining, new work stops at once, and running work stops at its first safe point within the grace time and writes a structured hand-off (status, item, version, what is done, the next steps in order, open questions, where the evidence is). After the grace time, work stops with a forced hand-off. Resume follows the declared order from the hand-offs, and the next run reads its hand-off first. A halt never delays a stop (§9).
2. **Flags and holds.** A flag or hold placed by a human seat is an event on the part or item. Every effect already queued for held work is held at the system that would run it. Work is released only when no pause, stop or superseded version still holds it. A hold placed by a human is lifted only by a human seat. Lifting a hold on a part or its work is `restart-stopped-unit`; lifting a containment hold that holds only a resource, a flow or an outside effect is `restore-or-rollback` (item 5; Standard §4.3, item 9).
3. **Cut-off.** A stop of AI authority raises a cut-off epoch that every executor checks before every mutation, refusing within seconds any credential issued before it. Delegated AI authority holds only while its witnesses renew a short lease from a fresh heartbeat; the `[ORG]AION` sets how many witnesses there are, on at least one host other than the AI's own (Standard §4.3, item 11). Human seats' own actions are never fenced. Re-arming, and any return of authority on a restored heartbeat, is signed.
4. **Recovery path.** The inverse of an executed action runs through a recovery-only path that needs no model, broker or Panel and grants no forward authority. It journals itself when the central log is down, and writes "reverted" only after the restoration is verified. Running it is `restore-or-rollback`, unless the action was taken under a standing action class whose envelope names the automatic revert.
5. **Soft containment.** On a deterministic breach, a containment part (never the detector) applies at once the narrowest reversible hold for the highest good in play; a human seat confirms or lifts it. A containment hold that stops a part or its work is lifted as in item 2 with `restart-stopped-unit`; one that holds only a resource, a flow or an outside effect is lifted with `restore-or-rollback` (Standard §4.4, item 19).

## 16. Library parts added on 14 October 2026

**Addition (GOV, 14 October 2026).** Four Library parts, each with its card in `library/cards/` (`DRAFT`, `last_result` `NOT_RUN`) and its fixed test in `library/cards/README.md`:
1. **49GAION Duty Deputy:** answers members' recurring asks for a human seat only from signed, unexpired rulings, cites the ruling, and raises every ask no ruling covers and every conflict between rulings (Standard §5.2).
2. **49GAION Outside Inspector:** checks from infrastructure that shares no failure with the inspected AIOC that its duties happened; builds nothing, directs no one, writes only its own report; never the internal-audit line (Standard §3.2).
3. **49GAION Advisory Council:** asks several model providers independently, without the asker's instruction or a leading frame, keeps every reply whole and merges by a stated rule; decides nothing (Standard §2.4).
4. **49GAION Reference Comparison:** compares an organisation's output with recognised references of the same kind; perception by a model, judgement by rules and cited evidence, decision by a human; facts counted, never taste; public sources only, and no account created in another party's system.

## 17. Process and Position Design: the stage after the target operating model

**Addition (GOV, 15 October 2026).** 49GAION Process and Position Design is a Library part (`library/cards/process-and-position-design.part-card.json`). In an `[ORG]AION` it is the AIOC `[ORG]AIOC-PPD` (Naming Standard R2). It is a part of its own, never merged with the part that designs the target operating model or with the stage after it (Standard §3.1, item 3; `49GAION/DR-0014`).

1. **Its place.** It follows the part that designs the organisation's target operating model. Like every other part, it enters through OCO.
2. **What it takes.**
   - **The release, directly.** A decided target operating model release with its role register, handed over by the part that made it: by reference (ID, version and hash of its manifest), through its Input socket and the tool gateway. It reads the role register first. A release that is not decided, or whose hash does not match, is not used.
   - **Other sources.** The organisation's other sources (its existing processes, procedures, policies, volumes and times) come only by reference from Source Lifecycle's output socket (§13, item 4).
   - **The request.** A run starts only from a request of the Requesting Authority: the Cell carrying `[ORG]HOAC-GOV`, or a human Cell to which it has delegated the design decisions (Standard §4.2, items 5 and 8).
3. **Back to the target operating model.**
   - It never edits the release. A defect it finds goes back to the part that made the release as a return, one of: accepted; cannot use, missing what; contradiction found; assumption invalid; request kind unsupported. Each return cites the elements it concerns.
   - The elements a return concerns are held until a new decided release, or a decision of the Requesting Authority, answers it. Work on the other elements goes on.
   - The two parts may go back and forth as often as needed. Each pass is a new version; nothing is overwritten.
   - Each return is also filed into Source Lifecycle as a design report, with the same hash, so that a revised request to the part that made the release can cite it.
4. **What it asks.** What the release and the sources do not answer, it asks of the Chief of Staff of Source Lifecycle as a needs request, and the answer is recorded there as a source (§13, item 6). It never asks a person, and a request never names a person.
5. **What it does.** One stage, processes first; each step has one output and a done-test.
   1. **Process architecture.** The processes under each value-stream phase and capability of the release, in levels, each with one owner position. Every phase and capability has a process, and every hand-off of the release belongs to one.
   2. **Critical processes first.** The processes that cross parts of the model are chosen, with the reason recorded, and designed first.
   3. **Process design.** For each process: its purpose and trigger; its ordered steps in role lanes; the inputs and outputs of each step; the decision at each step and who decides it; exceptions and escalation; measures, volumes and step times. Each step has one accountable role, each decision one decider, and each hand-off between lanes is matched at both ends.
   4. **Positions.** The steps and decisions of each role are grouped into positions. Every step and decision sits in exactly one position, and every position holds at least one. Each job description is generated from what the position holds: its purpose, accountabilities, decisions and their limits, the positions it works with, its measures and its reporting line. A job description is never written free-hand.
   5. **Structure.** Reporting lines inside each part, with spans and layers checked; standing forums, each with a charter. Every position has one reporting line.
   6. **Workload.** The work each position carries, from the volumes and step times of its processes.
   7. **Walkthrough.** The design is walked through realistic situations. Every finding is fixed or put to decision.
   8. **Decision and release.**
6. **What it gives.**
   - **The release.** A Process and Position Design release with these parts: process architecture; process book; decision-rights register and authority matrix; policy register; position register with job descriptions; organisation charts; forums with charters; workload; crosswalk from the current organisation to the target; walkthrough report and quality checks; decision package.
   - **Traced, never invented.** Every element traces to an element of the release or to a source. A measure, volume or time that no source gives is marked as an assumption and put to decision.
   - **Decided.** Every element is decided by the Requesting Authority. Silence, or approval of a whole pass, decides nothing.
   - **Filed.** The release is frozen and content-addressed, filed into Source Lifecycle as a source, and handed to the next stage by reference.
7. **Positions only.** It designs positions, never people (Standard §1.1, item 9). No output names a person or reads who occupies a position. It makes no choice of what fills a position; that belongs to a later stage.
8. **Its connections.** Two connections, each approved and scoped as in §13, item 5: to the part that made the target operating model release (read its releases; send returns), and to Source Lifecycle (read; needs requests; write only its own filed releases and returns). Revocation cuts a connection at the gateway at once and holds the run.
9. **Assurance.** The output of each step is checked by Cells that did not produce it before the next step starts (Standard §3.2, item 14). Critical outputs are written twice, separately, and their differences are settled on the sources or put to the Requesting Authority.
10. **The fixed test.** Every rule of this section has a case in TEST-PROCESS-AND-POSITION-DESIGN v1 (`library/cards/README.md`). The card stays `DRAFT`, with `last_result` `NOT_RUN`, until the test has run once with recorded evidence (§10, item 3).
