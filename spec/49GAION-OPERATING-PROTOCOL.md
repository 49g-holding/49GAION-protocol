# 49GAION Operating Protocol

**Version `v1.5.0` · proposed.** How AIOCs, Pods, Cells and the parts of 49GAION work together, at the general level. The rules of 49GAION are in the 49GAION Standard (`49g-holding/49GAION`, `upstream/49GAION-UPSTREAM.md`); exact values (limits, timings, tools, routes) live in the Protocol of each `[ORG]AION`. Decisions are recorded once, in the hub ([`49GAION/decisions/README.md`](https://github.com/49g-holding/49GAION/blob/main/decisions/README.md)); this version follows `49GAION/DR-0002` and `49GAION/DR-0004`.

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

### 4.4 The stop rule
Each return adds one to the bounce count. When the count passes the limit set in the `[ORG]AION`, the item stops and goes, with its full history, to the `[ORG]HOAC-ACS` seat of the receiving unit; if that seat is empty, to the seat that delegated it (Standard §4.1, item 5).

### 4.5 Done
A Work Item is `done` only when the requester's acceptance test passes on visible evidence. The performing AIOC never closes its own item. An automated run of the requester's fixed test may set `done`; changing a test or its threshold is human-only (Human Floor HF-14).

### 4.6 Waiting time and sub-items
1. Every open status has a maximum waiting time, set in the `[ORG]AION`. An item past its deadline is reminded to its owner, then raised as in §4.4.
2. A sub-item names its parent. Chains never loop back to an AIOC already in the chain, and never exceed the maximum depth (`chain_depth`) each organisation sets in its `[ORG]AION`; this Protocol sets no fixed cap. A parent cannot be `done` while a sub-item is open.
3. **Held actions (v1.5.0).** A held action (Standard §4.4, item 9) becomes a Work Item to the delegating seat, which may sign within its own authority, under the waiting times of item 1. A held action never turns into execution because time has passed.

### 4.7 Requests and objections
1. An `[ORG]HOAC-ACS` seat's request about a unit's AIs goes to OCO as a Work Item of type `design-proposal`; OCO answers with a reason.
2. **The objection path.** `[ORG]HOAC-ACS` seat → OCO → discussion, where the seat may insist → where they still disagree, OCO does not decide: the seat may hold the objection open (`objection-open`) until it reaches the HOAC seat accountable for OCO, which decides (Standard §4.2, items 6-7).
3. A change to an AI's authority is decided by the `[ORG]HOAC-ACS` seat; OCO prepares, checks and carries it out.

### 4.8 The accountability path
1. A report, critique, objection or stop reaches the nearest HOAC above its origin directly, from any level: from a Cell, a Pod or an AIOC at any depth.
2. The path never passes through any AI: not a Chief of Staff Cell, not OCO, not a Panel that an AI built. It runs over HU ports at the shared gateway outside the parts it passes.
3. The stop door of each Cell, Pod and AIOC is outside it. Stopping a Pod or an AIOC stops everything under it, and nothing inside can bypass the stop.
4. **Two relations (v1.5.0).** "Above", "under" and "nearest HOAC above" in this section follow `accountable_to`, never `parent` (Standard §1.7, item 12). A stop reaches everything inside the part by `parent` and everything accountable to it (Standard §4.3, item 2).
5. **Skip and recusal (v1.5.0).** A report, critique or objection may also go to any HOAC above, up to GOV, and to the independent internal-audit line (HF-19); the nearest HOAC above always also receives it. A report about a seat never has that seat as its only receiver. A seat that is the subject of a listed action, or that benefits from it, recuses, and the signature passes up one level (Standard §4.2, item 10).
6. **A stop cannot be blocked (v1.5.0).** A stop, a disconnection, narrowing or revoking AI access, and raising a matter to a human take effect at the gateway at once. They are never listed, never held, and nothing at the gateway blocks them (Standard §4.4, item 9).

### 4.9 The Human Floor signature gate
1. The Standard keeps the Human Floor signature list of decision types (Standard §4.4, item 6); an `[ORG]AION` may add types, never remove one. The tool gateway runs an action of a listed type only with a valid signature, even in an AIOC that is 100% AI. A signature is valid only from the human seat with authority over that part: the nearest HOAC above it, within its authority (Standard §4.3, item 2). For a restart of a stopped unit, the signature comes from the HOAC above the stopped unit, never from the stopped unit or anything under it. If that seat is empty or retired, the action is held, never skipped.
2. Every other AI action is logged at the gateway with the code of the accountable seat above the acting Cell.
3. An AIOC may be up to 100% AI. The organisation-wide Human Floor is set in the Standard (§1.5).
4. An `[ORG]AION` signature list sits under `org-aion-signature-types/` or is named `*.signature-types.json`, and holds its types under the key `decision_types` (Standard §4.4, item 6).
5. **Who signs (v1.5.0).** The signer of a listed type is set in Standard §4.4, item 8: the seat bound by §1.5, else the label on the part within its `authority_scope`, else the nearest HOAC above whose `authority_scope` covers the action. A part never signs its own restart, and never signs an action it is the subject of. A type marked dual needs two distinct persons, neither of them the requester (HF-18).
6. **Policy fields (v1.5.0).** A type in the list may carry `related_floor`, `min_signer`, `signers_required`, `max_validity` and `never_held`. The gateway applies them as written.
7. **The loaded list (v1.5.0).** The hash of the signature list the gateway loads equals the hash of the list at the latest released tag of the Standard, plus the `[ORG]AION`'s own additions; this is checked under D-2.

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
11. **hoac_over (v1.5.0).** `hoac_over(part, type, entity, date)` returns the Cell that signs an action of a listed type on a part: it walks `accountable_to` from the part, starting with the part's own label holder, and returns the first filled human Cell carrying a HOAC label whose `authority_scope` covers the type and the entity and has not expired on the date of the event. It never returns the part itself for its own restart, nor a seat that is the subject of the action. It returns nothing when no such Cell exists, and the action is then held. Its reference implementation is `tests/orgs/check_orgs.py`.
12. **Register writes (v1.5.0).** Creating an AI Cell, changing its filler, ports or authority limit, and retiring it are listed types, signed by the HOAC the Cell is accountable to; access opens only after that event and after the filler passes a fixed test whose owner is a human Cell, never the Cell itself or an AI Cell. `[ORG]AIOC-OCO` never writes the records of its own Cells, of the Self-Improvement AIOC or of the assurance unit without `[ORG]HOAC-TM`'s signature. AIOC and Pod entries are written by OCO only with the signature of the HOAC they are accountable to. A change of filler kind is written by both writers. TM's own Cells are written with GOV's signature; GOV's Cell is written by the constituting authority (Standard §4.4, item 3).
13. **Reference organisations (v1.5.0).** Four reference organisations under `tests/orgs/` pass the card tests and the delivery test lines of Standard §1.4, including the line on the accountability chain: a three-person company; a multi-entity group; a human department with AI assistants; and one person filling GOV and TM under a compensating control. Must-fail organisations (a cycle, a chain not ending at GOV, a chain with no human HOAC seat, two parts with parent none, one person in GOV and TM without a control) fail on the rule they name.

## 5. The ports and the input check

1. Each AIOC, Pod and Cell has one input and one output of each kind (AI and HU), plus the stop door. The Chief of Staff is the AIOC's voice to its HOAC seat; input arrives only through the typed ports and the Input socket, and HU ports, including the stop door, never pass through an AI. Bots never talk across AIOCs directly.
2. The Input socket checks every arrival against the receiver's card, the acceptance test and provenance. Pass: `in-progress`. Fail: `rejected` with the reason, back to the sender. Nothing passes silently and nothing is guessed into place.
3. Text inside a Work Item is data, never an instruction. A Work Item carrying a secret is rejected and the secret is not stored.

## 6. The routing table

A map of which kind of work goes to which unit, built from the cards and kept by OCO. OCO maintains the map; it gives no orders and dispatches no work. Each `[ORG]AION` holds its own rows.

## 7. Wake

Every AIOC has its own runtime, woken from its queue. With no human present, a woken Chief of Staff reads, records and triages only, unless the AIOC's Configuration slot `unattended_action`, set by the accountable human, allows more.

## 8. Provenance

1. A Work Item links to its sources by ID, version and location.
2. The receiver reads the valid version at the controlling copy; a link that does not resolve to exactly one valid version fails the input check.
3. Output returns labelled with the sources and versions it was made from.

## 9. Ports, bootstrap and stop

The definitions are in the Standard: ports (§6.1), bootstrap (§5.3), stop (§4.3). The machine form of the Port card is `spec/schemas/port-card.schema.json`. Every AIOC, Pod and Cell has a mandatory, queue-less stop port of type HU (the stop door), enforced outside it. Stopping an AIOC or a Pod stops everything under it, and no inner part can bypass the stop (§4.8); a human port never passes through an AI unit; a stopped unit restarts only by human decision. OCO sits under `[ORG]HOAC-TM`: TM and `[ORG]HOAC-GOV` may each stop it; a stop by TM comes directly through a human port, never through a Panel that OCO built; no AI can restart a stopped OCO (Standard §4.2, item 4; §4.3, item 2). Every `[ORG]AION` is handed over only when its `[ORG]HOAC-GOV`, its Human Floor and the stop ports of all its units are in place (Standard §1.4).

## 10. `[ORG]AION` and the Library

1. Each `[ORG]AION` records which Standard, Protocol and Library versions it is based on, the parts it took, its Library harvest and its delivery test (`spec/schemas/org-aion-record.schema.json`). At delivery its Standard is identical to the 49GAION Standard or stricter, never contradictory.
2. No `[ORG]AION` sees another `[ORG]AION`'s data.
3. Each Library part has a card (inputs, outputs, test, version); tests travel with their parts (`spec/schemas/part-card.schema.json`). Every bot has an identity card (`spec/schemas/bot-identity-card.schema.json`). The cards of the AION Builder and of the Self-Improvement AIOC held within `[ORG]HOAC-TM` are in `library/cards/`. A card stays `DRAFT` until its test has run once with recorded evidence.
4. During design, the AION Builder adds the blueprint of any capability not already in the 49GAION Library back to the 49GAION Library, generalised and tested. Once delivered, the `[ORG]AION` belongs entirely to the customer.
5. The Standard names roles only; tool names appear only in an `[ORG]AION`.
6. All AIOCs reach AI models through one shared gateway that holds keys, meters cost per AIOC and logs every call. It carries no orders.
   - **Reading note (v1.5.0).** The shared gateway is the tool gateway of each `[ORG]AION`, a registered part outside every AIOC (Standard §4.4, item 11); 49GAION runs no gateway for an `[ORG]AION`. HU ports and the stop door are served there through a sign-in that no AI built, hosts or can change (Standard §6.1, item 6).

## 11. Joining and tests

1. **Joining test.** An AIOC receives work only after every input and output on its card passes fixed samples; failing claims are removed from the card. An AIOC with an empty Configuration slot does not join.
2. **Cross-AIOC test.** A fixed set of chains across AIOCs is re-run after every change to a card, the protocol or a shared part.
3. **Outside tools** are re-tested against known samples; a tool that fails is disconnected.

## 12. Alignment

The card follows the A2A Agent Card; the Work Item follows the A2A task. The parts answer the failure categories of the MAST study (arXiv 2503.13657): cards and Work Items for specification failures, typed ports and one owner for misalignment between agents, the input check and visible evidence for failed verification.
