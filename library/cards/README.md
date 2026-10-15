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
  5. A defect in the release goes back to the part that made it, with a return kind and the elements it concerns. The release is never edited.
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
- **Status.** `DRAFT`, with `last_result` `NOT_RUN`. It stays so until the test has run once with recorded evidence.
