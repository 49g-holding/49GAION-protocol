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

- **What it is.** The first part an organisation receives, and the stage through which every source enters (Protocol §13).
- **What it does.**
  - It takes documents of any format and the owner's own words.
  - It records, references, classifies and fixes them.
  - It tells the owner what is missing.
  - It serves connected parts through its input and output sockets.
- **Its fixed test, TEST-SOURCE-LIFECYCLE v1.**
  1. From a sample owner with no documents, a spoken account becomes a referenced source only after the speaker approves its preview.
  2. A connected part reading outside the scope it was granted is refused.
  3. A request for a source that is not held is answered "not held" and recorded as missing.
- **Status.** `DRAFT`. Its test has not run.

**Self-Improvement (v1.5.0, correction).** There is no standalone Self-Improvement unit card. The process is recorded on `org-aion-top-management.unit-card.json`, the card of the Cell carrying `[ORG]HOAC-TM`, under `processes`, and is served by AI Cells; its v3 part and bot cards describe that process and the bot filling an AI Cell that serves it. Every v3 bot card names its own credential, `never_signs: true`, and memory sealed on a change of filler.
