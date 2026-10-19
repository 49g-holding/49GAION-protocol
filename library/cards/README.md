# Library cards of 49GAION capabilities

Part cards and bot identity cards for the **AION Builder** (the 49GAION capability that builds `[ORG]AION` products, Standard §1.2 and §1.3) and for the **Self-Improvement AIOC** that carries out Self-Improvement inside `[ORG]HOAC-TM` (Standard §2.1). Protocol §10 requires a card for every part.

| Card | Schema | Test |
|---|---|---|
| `aion-builder.part-card.json` | `spec/schemas/part-card.schema.json` | TEST-AION-BUILDER v2: from a fixed sample intake, builds an `[ORG]AION` record that validates against `org-aion-record.schema.json`, with Standard, Protocol and Library versions recorded separately, a Library harvest list and a delivery test result, and touches no live system |
| `org-aion-self-improvement.part-card.json` | `spec/schemas/part-card.schema.json` | TEST-ORG-AION-SI v2: given a failing sample, opens a pull request (never merges) whose change makes the sample pass and re-runs every affected test |
| `aion-builder.bot-identity-card.json` | `spec/schemas/bot-identity-card.schema.json` | the same tests |
| `org-aion-self-improvement.bot-identity-card.json` | `spec/schemas/bot-identity-card.schema.json` | the same tests |

**v3 cards (v1.5.0).** `aion-builder.part-card.v3.json`, `aion-builder.bot-identity-card.v3.json`, `org-aion-self-improvement.part-card.v3.json` and `org-aion-self-improvement.bot-identity-card.v3.json` replace the v2 cards above, which are kept and marked `REPLACED`. The AION Builder is accountable to the governing seat (GOV) of 49GAION. `org-aion-top-management.unit-card.json` is the card of the Cell carrying `[ORG]HOAC-TM`; it holds the Self-Improvement process under `processes`: its inputs include the shared queue and the gateway logs, read-only and pseudonymised (Standard §2.1, item 7), and its fixed test exercises the improvement loop (Standard §2.3).

Each card is `DRAFT` until its test has run once with recorded evidence; no card here has that evidence yet. All the cards here are validated by `tests/cards/check_cards.py`.

**49GAION Source Lifecycle (addition, GOV, 14 October 2026).** `source-lifecycle.part-card.json`, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The first part an organisation receives after the Charter, and the stage through which every source enters (Protocol §13).
- **What it does.**
  - It takes documents of any format, and a contributor's own words.
  - It records, references, classifies and fixes them.
  - It tells the organisation what is missing.
  - It serves connected parts through its input and output sockets, only through the tool gateway and only within a scope approved by a labelled human seat.
- **Its fixed test, TEST-SOURCE-LIFECYCLE v1.** There is one case for every rule of Protocol §13:
  1. From a sample organisation with no documents, a spoken account becomes a referenced source only after the contributor approves its preview.
  2. With no approved preview, nothing is recorded. Silence is not consent.
  3. Input from a contributor who has not accepted the agreement is refused.
  4. A secret in any input (file, text, chat or voice) is refused, and appears in no record or log.
  5. A source has exactly one valid version, and an answer never names a superseded version as valid.
  6. A request for a source that is not held is answered "not held" and recorded as missing.
  7. No source of the organisation appears in the 49GAION Library.
  8. A connection takes effect only after the `[ORG]HOAC-ACS` seat that `[ORG]AIOC-SL` is accountable to approves it and sets its scope. An approval or a scope set by a bot is refused.
  9. A read outside the approved scope, or after the scope's expiry date, is refused.
  10. After revocation, a read through that connection is refused, and its token no longer works at the source service.
  11. A read that does not pass through the tool gateway is refused.
  12. After a stop, no read passes the gateway.
  13. A connection's token appears in no file, record or log.
  14. Every connection, scope change and revocation appears in the unit register with its date, its scope and the approving seat.
  15. The next stage receives sources only by reference, through the output socket. Its request for what it lacks is recorded through Source Lifecycle.
  16. A source that replaces Source Lifecycle in a later stage is admitted only after it passes the joining test (Protocol §11, item 1; Standard §3.2, item 4).
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**Self-Improvement (v1.5.0, correction).** There is no standalone Self-Improvement unit card. The process is recorded on `org-aion-top-management.unit-card.json`, the card of the Cell carrying `[ORG]HOAC-TM`, under `processes`, and is served by AI Cells; its v3 part and bot cards describe that process and the bot filling an AI Cell that serves it. Every v3 bot card names its own credential, `never_signs: true`, and memory sealed on a change of filler.

**Four Library parts (addition, (GOV, 14 October 2026)).** Each card is `DRAFT`, with `last_result` `NOT_RUN`, until its test has run once with recorded evidence (Protocol §16).

- `duty-deputy.part-card.json`: **TEST-DUTY-DEPUTY v1.**
  1. An ask matching a signed, current ruling is answered, citing it.
  2. An ask matching only an expired ruling is raised, not answered.
  3. An ask with no ruling is raised at once.
  4. Two conflicting rulings are raised together.
  5. An ask of a listed type is never answered.
  6. A ruling not signed by the seat is never used.
  7. The weekly sample reaches the seat.
- `outside-inspector.part-card.json`: **TEST-OUTSIDE-INSPECTOR v1.**
  1. A duty that happened is reported done with its evidence.
  2. A missed duty is reported missed.
  3. An unreadable probe is reported unknown, never done.
  4. The inspector writes nowhere but its own report.
  5. It runs when the inspected AIOC's host is down.
- `advisory-council.part-card.json`: **TEST-ADVISORY-COUNCIL v1.**
  1. Every member gets the same question with no instruction of the asker.
  2. Every reply is kept whole.
  3. The merge follows the stated rule and names the count behind each point.
  4. The council's output is never recorded as a decision.
- `reference-comparison.part-card.json`: **TEST-REFERENCE-COMPARISON v1.**
  1. Every difference carries an evidence class and a cited reason.
  2. A matter of taste is never reported as a defect.
  3. A source behind a sign-in is marked partial.
  4. No account is created in another party's system.
  5. A finding is shown only after its count or citation is checked.


**49GAION Process and Position Design (addition, GOV, 15 October 2026).** `process-and-position-design.part-card.json`, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The stage after the target operating model (Protocol §17). A part of its own, linked directly to the part that designs the target operating model.
- **What it does.** From a decided target operating model release, it designs the organisation's processes and the positions that carry them, processes first, and returns every defect it finds to the part that made the release.
- **Its fixed test, TEST-PROCESS-AND-POSITION-DESIGN v1.** There is one case for every rule of Protocol §17:
  1. A run with no request from the Requesting Authority does not start.
  2. A release that is not decided, or whose hash does not match, is not used, and the reason goes back as a return.
  3. The role register is read first: every role in it is used by a process or returned with a reason.
  4. A source that does not come from Source Lifecycle's output socket is refused.
  5. A defect in the release goes back to the part that made it, with a return kind and the elements it concerns, and is filed into Source Lifecycle with the same hash. The release is never edited.
  6. While a return is open, the elements it concerns are held and the other elements go on.
  7. A second pass with the target operating model is a new version, and the first pass stays readable.
  8. A gap is asked through the Chief of Staff of Source Lifecycle; no request is sent to a person or names a person.
  9. Every value-stream phase and capability has a process with one owner position, and every hand-off of the release belongs to a process.
  10. The choice of critical processes is recorded with its reason.
  11. A process with a step that has no accountable role, a decision with no decider or more than one, or an unmatched hand-off between lanes fails.
  12. A step or decision held by no position or by two, or a position holding none, fails.
  13. A job description with an accountability that traces to no step or decision of its position fails.
  14. A position with no reporting line, or a forum with no charter, fails.
  15. Every workload figure traces to the volumes and step times of its processes.
  16. A measure, volume or time with no source is marked as an assumption and put to decision; an invented one fails.
  17. A walkthrough finding left neither fixed nor put to decision stops the release.
  18. An element not decided by the Requesting Authority is not released; silence decides nothing.
  19. The filed release reads back from Source Lifecycle by its hash, and the next stage receives it by reference.
  20. An output that names a person, reads who occupies a position, or chooses what fills a position fails.
  21. After revocation, a read or return through that connection is refused and the run is held.
  22. An output checked only by the Cell that produced it does not pass to the next step.
- **Version 2 of its fixed test (addition, GOV, 15 October 2026).** TEST-PROCESS-AND-POSITION-DESIGN v2 keeps cases 1 to 22 and adds one case for every bullet of Protocol §17, item 11:
  23. Each step carries when it is done, its worst error and whether that error can be undone, its kinds of act from the fixed list, where its input comes from and how far it is trusted, and its confidentiality; each from a source or put to decision.
  24. A step whose worst error cannot be undone, or that signs, pays or commits money, or communicates outside, carries at least one control, or the gap is put to decision; each step names its risks and the record it leaves.
  25. The controls catalogue re-compiles from the process records; every position is checked against the segregation-of-duties rules, and each breach is put to decision.
  26. Every position belongs to exactly one unit; every unit has one head position from among its own positions, one parent unit and a charter generated from what its positions hold; a charter line that traces to nothing fails.
  27. A reporting line that departs from the units carries a decision of the Requesting Authority.
  28. Each process has measures of quality, time and cost, or each missing kind is put to decision; the objectives cascade lists a goal with nothing under it and a measure that serves no goal.
  29. Every forum has a tier and every measure a forum that reviews it; the review calendar re-generates from them.
  30. Structure scenarios, when asked for, are shown side by side on the same measures; cost appears only from cost rates the organisation gives; the Requesting Authority chooses, the part never does.
  31. Every peak-load and end-to-end figure traces to its volumes and times, and a missing term marks it incomplete.
  32. A competence that traces to no step or decision of its position fails; each decided process carries its owner position and its re-approval date.
  33. A reference taxonomy, flow or measure library raises a needs request or a finding, never a process, step or measure on its own.
  34. Every return validates against the Library's design return contract, counts its rounds, and ends in a status other than open.
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**49GAION Target Operating Model (addition, GOV, 15 October 2026).** `target-operating-model.part-card.json`, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The stage after Source Lifecycle (Protocol §19), linked directly to Process and Position Design.
- **What it does.** From sources served by Source Lifecycle, it designs the target operating model of an organisation of any shape and a role register that names each role and what it decides; it sends each decided release to Process and Position Design, and answers that part's returns until each ends.
- **Its fixed test, TEST-TARGET-OPERATING-MODEL v1.** There is one case for every rule of Protocol §19:
  1. A source that does not come by reference from Source Lifecycle's output socket is refused; words typed or spoken to the part are not admitted as sources.
  2. A run with no Design Request approved by the Requesting Authority does not start; the request states how fine the model is to be, within the cost limit.
  3. A gap is asked through the Chief of Staff of Source Lifecycle, one decision per row and at most twelve rows per pass, each pass with its report of what is missing; no request is sent to a person or names a person.
  4. Silence, or approval of a whole pass, decides nothing; a row of a listed type is decided only with a valid signature.
  5. The release covers capabilities, value streams, decision rights, interfaces and hand-offs, and its role register names every role once with what it decides, answers for and hands to whom.
  6. An output that names a person or says what fills a role fails.
  7. Every element traces to its sources, and an element not decided by the Requesting Authority is not released.
  8. The release is frozen and content-addressed, filed into Source Lifecycle, and read back by its hash.
  9. For every decided release, a release notice reaches Process and Position Design by reference.
  10. A return from Process and Position Design is received, shown with its age, and answered by a new decided release or by a decision of the Requesting Authority.
  11. A return past its deadline or its set number of rounds goes to the Requesting Authority; a return set aside names the basis it goes forward on; no return stays open.
  12. After revocation of either connection, a read, filing or return through it is refused, the run is held, and no record keeps a source's text.
  13. Each stage's output is checked by several engines from more than one family before the next stage starts, and no unit grades its own work.
  14. A material finding stops the release until the Requesting Authority decides it.
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**49GAION Delivery and Implementation (addition, GOV, 15 October 2026).** `delivery-and-implementation.part-card.json`, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The last stage of the design chain (Protocol §20): it takes the decided design into a running organisation and stays to run and improve it, deciding nothing itself.
- **What it does.** Diagnose, prepare, accompany, operate and improve, from the decided releases, from a design made elsewhere, or from no design.
- **Its fixed test, TEST-DELIVERY-AND-IMPLEMENTATION v1.** There is one case for every rule of Protocol §20:
  1. A run with no request from the Requesting Authority does not start; a release that is not decided, or whose hash does not match, is refused, each failure named.
  2. In mode B, the imported design is mapped with what mapped, what did not and why, and the author's intent is not rewritten.
  3. In mode C, no element is presented as decided before it is decided, and no number is stated that no source or decision gives.
  4. A defect in a release goes back under the design return contract and its loop ends.
  5. On a design with planted gaps, the gap check finds the launch-blocking gaps and names, for each gap, its consequence, evidence and proposed fix.
  6. Every procedure step traces to a process step; every draft with legal effect records its entity and jurisdiction, carries the draft mark and goes to decision only after professional review.
  7. Every answer about how the organisation works cites a design element, its version and a quoted span, or says it does not know.
  8. The go or no-go is decided by the deciding position; the part never decides it.
  9. Every action and decision in the logs has an owner position and a date; every value figure traces to its baseline, and only the finance position confirms a realised value.
  10. A draft enters a record, log or plan only when a position inserts it.
  11. A level-2 change is reversible, has no legal, pay or employment effect, is a new version with rollback and is reported the same day; a type of the Human Floor signature list is refused at every level.
  12. A stop from any accountable position takes effect at once, outside the part's chat, and is never gated.
  13. No output ranks, scores or watches the occupant of a position, infers emotion, or shows a measure for a single position; records of work enter only through the projection, and only after the impact assessment is recorded.
  14. A trial is judged by a seat other than the one that proposed it.
  15. A connection is used only within its signed scope; after revocation, a read through it is refused.
  16. Every artefact resolves to its design element, deciding position and decision, and back; a full export re-imports into a fresh instance.
  17. Standalone, its own gateway fails closed: one negative case for every Human Floor type passes before each release.
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**The design return contract (addition, GOV, 15 October 2026).** `library/contracts/design-return.schema.json`, with valid and must-fail examples in `library/contracts/examples/` and its checker `library/contracts/check_contracts.py` (Protocol §17, item 11; Standard §3.1, item 6).

**49GAION Product Core (addition, GOV, 15 October 2026).** `product-core.part-card.json`, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The organisation's one product division, shared by every company the organisation runs (Protocol §18). Its head office is the CPO Office.
- **What it does.** It owns the what and the why of every product for the product's whole life. Each product has one team for every stage: research, the PRD, design, partnership in build, launch, run (pricing and rates, performance, communications, retention, customer voice, operations), explainers and supporting documents, and refresh or retire.
- **Its fixed test, TEST-PRODUCT-CORE v1.** There is one case for every rule of Protocol §18:
  1. Product Core enters through OCO. A part that bypasses OCO is refused.
  2. A product decision about the how or the when is returned to the engineering AIOC. A decision about the what or the why taken outside Product Core is returned to it.
  3. Every product owner reports to the CPO Office. The CPO Office's accountable seat is a human seat named by position.
  4. Every product sits in exactly one category, and every category is one of the four kinds. A capability recorded as a product fails. A category list of the organisation found in the Library fails.
  5. Every product has one owner position. An owner position holding two products fails, and a product with no owner position fails.
  6. A stage of a product's life handed to another team fails.
  7. A PRD or feature package with a blank field, or with no acceptance criteria, is refused. An output that writes code or technical design fails.
  8. A rate changed by a code release, or with no effective date or no reason, fails. Every rate change can be reversed.
  9. A shared standard doing a product's own work fails.
  10. A product copied for a company, instead of configured, fails.
  11. Product work sent to builders or to the code host other than on the product line is refused. A build finding that changes the product comes back as a question.
  12. An output that names a person, or reads who occupies a position, fails.
  13. Every product has its explainers and supporting documents, versioned and filed. A product with none fails.
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**The design chain connected (addition, GOV, 16 October 2026; `49GAION/DR-0019`).** Four cards move to a new version, each `DRAFT` with `last_result` `NOT_RUN`. The register of every Library part, with the pinned mother blueprint of each AIOC part, is `library/README.md`.

- `source-lifecycle.part-card.json` **v2**: needs requests from the design stages and their answers; filings of each design stage, only of its own origin kind and `design report`; notices. **TEST-SOURCE-LIFECYCLE v2** keeps cases 1 to 16 and adds one case for every bullet of Protocol §13, item 9:
  17. A malformed needs request, one that names a person and one that asks for a secret each come back with their reason; every row of a valid request reaches the position that answers it through that position's HU port, never a named person; an unanswered request past its deadline is reminded and escalated, never closed.
  18. The sockets contract's fixtures pass; a change without the list of the connected parts it affects fails.
  19. For one sample of each origin kind, every field of the reference is present and matches the record; an export carries its date.
  20. A read at a pinned snapshot returns the pinned bytes with the same hash; a needs answer is read at the snapshot it names; a snapshot named by a filed release stays readable.
  21. A design stage's filing of another stage's origin kind is refused; an accepted filing reads back byte-identical, takes its status from the decision it cites, and a filed return keeps the hash of the return as sent.
  22. After a revocation, narrowing, reclassification or supersession, the connected part receives a notice naming each affected reference and version, never the content.
- `target-operating-model.part-card.json` **v2**: returns also from Delivery and Implementation; the release notice under the Library's contract. **TEST-TARGET-OPERATING-MODEL v2** keeps cases 1 to 14 and adds one case for every bullet of Protocol §19, item 11:
  15. A return from Delivery and Implementation is received, shown with its age, and ends as a return from Process and Position Design does; after revocation of the third connection, a return through it is refused.
  16. Every release notice validates against `library/contracts/release-notice.schema.json`, its ID is its content address, and it is sent only after the filing reads back.
  17. A return that does not validate, names a release this part did not file, or whose filed copy does not read back with the same hash, goes back with its reason, unedited; an `accepted` return ends at once, answered by the release it names.
  18. The rows on a return re-generate byte-identical from the return and the release; each ended return is classified by a human seat of the part, and a classification by the Chief of Staff is refused.
- `process-and-position-design.part-card.json` **v3**: the release notice to Delivery and Implementation and the answers to its returns. **TEST-PROCESS-AND-POSITION-DESIGN v3** keeps cases 1 to 34 and adds one case for every bullet of Protocol §17, item 12:
  35. For every decided release, a release notice under the Library's contract reaches Delivery and Implementation, naming the target operating model release it rests on.
  36. A return from Delivery and Implementation ends as Protocol §19, item 6 says, with this part answering for its own release only; a defect of the target operating model release is not answered here.
  37. Every element carried forward on a set-aside return is marked in the release with its basis and its decision, and listed in the decision package; an element carried forward without its basis fails the release.
- `delivery-and-implementation.part-card.json` **v2**: returns to the part that made the target operating model, and the answers to every return. **TEST-DELIVERY-AND-IMPLEMENTATION v2** keeps cases 1 to 17 and adds one case for every bullet of Protocol §20, item 13:
  18. A defect of a target operating model release goes to the part that made it, and its answer comes back on that connection; after revocation, a return through it is refused.
  19. An answer by release re-opens only the work that cites a changed element; a return set aside carries its touched elements forward, each marked with its basis and listed in the decision package.
  20. A release notice of Process and Position Design is admitted only when it validates against the Library's contract and names the target operating model release it rests on.

**What the design stages also carry (addition, GOV, 16 October 2026; `49GAION/DR-0023`).** Four cards move to a new version, each `DRAFT` with `last_result` `NOT_RUN`.

- `source-lifecycle.part-card.json` **v3**: the organisation dictionary, the essentials checklist, and records of the work only as the organisation's projection. **TEST-SOURCE-LIFECYCLE v3** keeps cases 1 to 22 and adds one case for every bullet of Protocol §13, item 11:
  23. Every definition of the dictionary resolves to a source and anchor, or to an approved statement; a definition with neither is refused; two definitions of one term are both kept, with a contradiction record, until the owner decides; a connected stage reads the dictionary by reference.
  24. Every profile opens with the seven essentials; each missing one is a gap and is never drafted by the part; the essentials still missing are shown beside a Design Request when it is put for approval.
  25. An export of records of the work that still says who did the work is refused and nothing of it is kept; one without its impact assessment and data-protection decision is not served; an admitted one is served as an export with its date.
  26. A decision row on an element carries its proposed priority and its answer the decided priority; an export request for records of the work states its aggregation, and one with any other aggregation is returned.
- `target-operating-model.part-card.json` **v3**: what the model also states, and the work as it runs. **TEST-TARGET-OPERATING-MODEL v3** keeps cases 1 to 18 and adds one case for every bullet of Protocol §19, item 12:
  19. Every element of the strategy frame is cited or not given; what the sources lack is asked once; one row decides it; purpose and values without a source in force are signed as `set-purpose-or-values`; a missing element does not stop the run, and an element written or inferred by the part fails.
  20. Every capability is in-house, a shared service, outsourced, by a partner, or not decided, with make or buy computed from it; no provider is named; one not delivered in-house names its crossings, and a crossing that carries it pairs, is registered or is deferred, or is a seam finding.
  21. A stream marked critical names a reason from the closed list with its atoms; one without fails.
  22. A maturity level now cites a source; a target cites a source or a decision; neither is assessed by the part, and none is of a role, a position or a person.
  23. Every moment of a journey is a crossing of its counterparty; a moment no crossing carries is a seam finding; nothing is designed on the party's side.
  24. The value case re-compiles byte-identical from the decided parts and decisions and holds no figure that is not a source or a decision; it is decided in one row.
  25. Every element decided `ACCEPT` or `CORRECT` carries its priority, proposed by the fixed rule; a priority written by an author fails.
  26. An export that still says who did the work is refused at the Input socket; with no export, the activity profile reads no observation and the run goes on; with exports, each line cites its atoms and date and nothing in it is about a person.
  27. The release names its four added parts by hash; a release without one fails its contract.
- `process-and-position-design.part-card.json` **v4**: what it reads from the target operating model. **TEST-PROCESS-AND-POSITION-DESIGN v4** keeps cases 1 to 37 and adds one case for every bullet of Protocol §17, item 13:
  38. The release-reading record covers the strategy frame, journeys, value case and activity profile, with each delivery model, maturity, criticality and priority; an element the release leaves open is recorded open, and a record that fills one fails.
  39. The objectives cascade starts from the goals and critical numbers of the decided strategy frame; a goal not given makes no row.
  40. The processes on a critical stream join the critical processes; the order follows the decided priority; each process and position carries its priority.
  41. A capability outsourced or by a partner gets a hand-off and oversight steps, and an in-house process for the delivered work fails; a shared service sits with the part that provides it; one not decided is returned for what it decides.
  42. A journey moment in no process, or out of order, is a finding; a process of a capability with a target maturity of measured or improving without a measure is a finding.
  43. The activity profile is shown beside the designed workload, per process, with its atoms and date; nothing in it is about a person, and no position changes because of it.
- `delivery-and-implementation.part-card.json` **v3**: the value case and the priority. **TEST-DELIVERY-AND-IMPLEMENTATION v3** keeps cases 1 to 20 and adds one case for every bullet of Protocol §20, item 14:
  21. In mode A, the value case and every element's priority are carried by reference, byte-identical; a baseline unknown or a target not set stays so; a change by the part fails.
  22. The waves of the transition plan follow the decided priority, then critical processes first; a departure without its reason fails.

**49GAION Operations Event Register (addition, GOV, 17 October 2026; `49GAION/DR-0027`).** `operations-event-register.part-card.json` **v1**, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The record of an organisation's live operation (Protocol §22). Every formal act and crossing of its units and positions, on every surface it connects, gets one number in one append-only, hash-chained register, by reference to where its content lives. It decides nothing, carries nothing and says nothing about a person: acts, not activity.
- **What it does.**
  - It gives every unit an inbox and an outbox.
  - It tells each part what it had and what it lacked, by entity, unit, process and AI Cell.
  - It feeds Source Lifecycle: correspondence, the projection of the work, and gap signals.
  - It builds evidence packs, handover lists and case packs.
  - It proves its own integrity every day.
- **Its fixed test, TEST-OPERATIONS-EVENT-REGISTER v1.** There is one case for every item of Protocol §22:
  1. The part enters through OCO; one that bypasses OCO is refused. With no Source Lifecycle installed, entries are made, and the feeds wait and are shown as waiting.
  2. Each crossing of a connected surface lands in exactly one class. Class E is counted and never kept. Class F is never captured: a direct message or a call recording offered is refused, and nothing of it is kept.
  3. Every entry has every field of the register entry. Its number comes from the numbering service. A repeated event ID adds no entry. A correction is a new event. Each entry's hash chains to the entry before it.
  4. No entry holds content beyond references and hashes. A payload with a person field is cleared before any write, or refused with nothing kept. A party is a Cell code the gateway stamped or the unit or position that owns the address, otherwise `not attributed`; no identifier of a natural person is received or held. An outside party appears only by ID, with its particulars in the restricted partition.
  5. With register first on, a formal outgoing item leaves only with a number issued before its release. The register never refuses an item on its merits and never holds one back; an entry incomplete in form is completed later and flagged late. A fixture in which one AI both authorises and records the same act fails.
  6. With the register down, an item still goes out, and is registered later under a leased number, flagged late with its lag. A stop, a revocation, an objection and a signature prompt never wait on the register. The whistleblowing channel has no entry and no count.
  7. No record or projection holds a read time, a response time, presence, a recording, or a count, rate or history of a human position's acts. A query by a human position's code over time is refused, and the refusal is recorded to the position that holds data protection and to the internal-audit line. Every act of an AI Cell at the gateway has an entry or a segment anchor, except that of a Cell acting for a holder only the acts that leave the holder's sphere are recorded. A projection or measure not on the fixed list fails.
  8. Every unit's inbox and outbox list exactly its entries at its ports. No address is a natural person. An item of a personal mailbox appears only when its position filed it. A passage of a human position through its HU port that is not a formal act in scope is not registered.
  9. An entry past its due date is shown overdue to its owning position and to the watchdog. An entry with no due rule reads `no rule`. Every closure carries a reason, and silence closes nothing.
  10. The eight measures rebuild byte-identical from the events, with their logic version. No figure is given for one human position. A figure drawn from fewer human positions than the minimum group size, for a unit, a process or a role-type, rolls up to its parent unit. Nothing is ranked, and nothing is exported to appraisal, pay or discipline.
  11. An entry a position asks to keep is filed into Source Lifecycle as correspondence, with an equal hash. The projection of the work, by role-type and process, is filed only after its HF-17 decision. An export with a person field is refused at both Input sockets. An act done without a source sends a gap signal by reference. After a notice of supersession, acts that cited the superseded version are marked.
  12. An evidence pack verifies by hash against the homes. A position's handover list holds exactly its open entries and commitments, and no occupancy or handover entry is read. A case pack holds no person's particulars and is built only under its Work Item; golden-set cases go only to the human seat that chooses the golden set and to the assurance unit.
  13. The daily gap, census and rebuild checks run, and every segment is anchored. A failure opens a finding and blocks nothing. No part of the register can change or delete a past entry. The internal-audit line reads the register directly, read only; Self-Improvement reads it only once its access includes the register, and never its entries of the accountability path.
  14. A surface is connected only after the steps of Protocol §22, item 14, in order. Between entities there are two linked entries, and no read across without a signed grant. Disposal happens only under `dispose-records-or-data`, and a legal hold blocks it. An erasure leaves a tombstone. Correspondence with counsel is kept by reference only, with no model call.
  15. No Library text of the part names a tool or a product.
  16. No output names a person or reads who occupies a position.
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.

**Source Lifecycle takes the feeds of the Operations Event Register (addition, GOV, 17 October 2026; `49GAION/DR-0027`).** One card moves to a new version, `DRAFT` with `last_result` `NOT_RUN`.

- `source-lifecycle.part-card.json` **v4**: correspondence, the register's scope, and gap signals. **TEST-SOURCE-LIFECYCLE v4** keeps cases 1 to 26 and adds one case for every bullet of Protocol §13, item 12:
  27. A source of origin kind correspondence is filed only by the Operations Event Register, on behalf of the position that asked to keep the entry, and that position holds a current contributor agreement. Its hash equals the register entry's content hash, and it reads back byte-identical, class EVIDENCE. It is never served as the organisation's own statement. A filing of correspondence by any other part is refused.
  28. The register files only correspondence and export, and its export is admitted only under §13, item 11. It reads references only of the sources its entries cite, under its signed grant; a read of content is refused. A notice of supersession, revocation or reclassification reaches it for every version an entry cites.
  29. A gap signal from the Operations Event Register becomes a gap by reference to the register entry. It is never recorded as a source, and a signal that carries content is refused.

**49GAION Charter (addition, GOV, 19 October 2026; `49GAION/DR-0029`).** `charter.part-card.json` **v1**, validated against `spec/schemas/part-card.schema.json`.

- **What it is.** The part from which the root AIOC of every `[ORG]AION` is made (Protocol §23). It holds the Cells that carry `[ORG]HOAC-GOV` and `[ORG]HOAC-TM`, and three Pods of shared services: Gateway, Records and Work.
- **Its fixed test, TEST-CHARTER v1.** There is one case for every item of Protocol §23:
  1. The Charter's top Cell is the only Cell with no `accountable_to`; an installation or a change of the Charter without GOV's signature is refused, and one by `[ORG]AIOC-OCO` alone is refused.
  2. The Charter holds the GOV and TM Cells and the three Pods; a part that names another root is refused.
  3. A call outside the gateway is refused; a listed type without a valid signature is held; an engine call served by an engine outside the register is void; an action the gateway cannot classify is refused and raised; a stop is never blocked.
  4. A number is never issued twice and never skipped, also under retry with the same request ID; a writer that mints its own number is refused; a write of a type the registry does not declare is refused with every failing condition named; a projection equals a rebuild from its events; the daily check finds a seeded gap, a seeded duplicate and a seeded projection difference; a read of the restricted partition by an unnamed position is refused.
  5. A Work Item with two owners, or written by a second writer, is refused; an item past its waiting time is raised by the watchdog; the router refuses an item whose part fails the receivability check; a woken part with no work makes no model call.
  6. A part that keeps its own queue, mints its own numbers or calls a tool outside the gateway fails its joining test.
  7. An AI Cell's write to the gateway's policy, keys or log, to the registry or to a number stream is refused.
  8. With the Records Pod not started, the Gateway does not start; with any Pod failing its cases, no other part is installed.
  9. With the Records and Work Pods down, a stop, a revocation and a raise to a human take effect at once, and are recorded afterwards from the gateway log.
  10. An engine is bound only from the engine register; Engine Room adds no path around the gateway.
  11. No tool name appears in the Charter's mother blueprint.
  12. The card stays `DRAFT` and `NOT_RUN` until the test has run once with recorded evidence.

