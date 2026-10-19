# The 49GAION Library

**Addition (GOV, 16 October 2026; `49GAION/DR-0019`).** The 49GAION Library holds every ready-made part of 49GAION: its AIOC parts with their mother blueprints, its capability parts, its unit cards, its contracts and its method catalogues (Standard §3.1). Built once, configured per `[ORG]AION`, never rebuilt. This file is its register: every part is named here once.

## How a part is held

- **Its card** sits in `library/cards/`, valid against `spec/schemas/part-card.schema.json`, `DRAFT` with `last_result` `NOT_RUN` until its fixed test has run once with recorded evidence (Protocol §10, item 3).
- **Its rules** sit in its Protocol section, and its place in the Standard in §3.1.
- **Its mother blueprint**, for an AIOC part, is written in its own writing repository, for any organisation, with `[ORG]` placeholders and no organisation's data. The Library holds it by pin: repository, path, version, commit and the SHA-256 of the blueprint file. A new version reaches the Library only by a pull request that moves the pin, merged by the governing seat of 49GAION. An organisation's instance keeps its own values in its own records repository.
- **One home.** The text lives in one place; the Library holds its pin, never a second copy.
- **A pin before its merge.** A pin may name the head commit of the writing repository's pull request that carries the version; when that pull request is merged, the pin moves to the merged commit, with the same SHA-256.
- **A mother repository (addition, GOV, 16 October 2026; `49GAION/DR-0024`).** Where the writing repository of a part's first instance holds an organisation's data, the mother is written in the part's own public mother repository, `49GAION-<part>`, laid out and checked as a writing repository, and pinned here like any mother. Source Lifecycle and Product Core are the first two.

## The register

**Two sections (addition, GOV, 16 October 2026; `49GAION/DR-0025`).** The Library is the one store of everything 49GAION has built and knows. **Parts**: everything 49GAION builds, from a Cell to an AIOC, with its blueprint, card, fixed test, contracts and method catalogues, and its whole history (versions, lineage, decisions, lessons, test results), held in its own home and named here. **Products**: what the Library offers, a single part offered alone or an assembly of parts placed side by side and connected; an assembly's blueprint lists its parts by pin, their connections, what it sets and one shared test, and its features are its parts' features (Standard §3.1, items 11 and 12).

### Parts

#### AIOC parts

| Part | In an `[ORG]AION` | Card | Protocol | Standard | Fixed test | Mother blueprint | Status |
|---|---|---|---|---|---|---|---|
| 49GAION Source Lifecycle | `[ORG]AIOC-SL`, the first stage | `source-lifecycle.part-card.json` v4 | §13 | §3.1, item 7 | TEST-SOURCE-LIFECYCLE v4 | `github.com/49g-holding/49GAION-source-lifecycle` (its mother repository, `49GAION/DR-0024`), `blueprint/SL-BLUEPRINT.md`, v0.1.3, commit `af5e98876d2a8740c8ac1dd3caf16db62eec0fe9`, SHA-256 `a487397ffb65a72dce19f173322a3bfed1a9a404c2f9575bdf49b9b95f7bf71d`; its fixed test `tests/TEST-SL.md` v1 | `DRAFT`, `NOT_RUN` |
| 49GAION Target Operating Model | `[ORG]AIOC-TOM`, the second stage | `target-operating-model.part-card.json` v3 | §19 | §3.1, item 4 | TEST-TARGET-OPERATING-MODEL v3 | `github.com/49g-holding/49aioc-tom`, `blueprint/TOM-BLUEPRINT.md`, v0.6.0, commit `a8445cb006e6f2378b7694543fb65c5da48af41f`, SHA-256 `ea11cd76a3343b926c452dbbd887cfad075702af933fc06e6b32cb16640f4c50`; its fixed test `tests/TEST-TOM.md` v5 | `DRAFT`, `NOT_RUN` |
| 49GAION Process and Position Design | `[ORG]AIOC-PPD`, the third stage | `process-and-position-design.part-card.json` v4 | §17 | §3.1, item 3 | TEST-PROCESS-AND-POSITION-DESIGN v4 | `github.com/49g-holding/49aioc-ppd`, `blueprint/PPD-BLUEPRINT.md`, v0.5.0, commit `b69997973181d15d356bccea49dd6ea0da3174bb`, SHA-256 `707f9dc374aeef2df17880584f2985a9a57d6d298bbd8233fdc18a7d5d5f5ce7`; its fixed test `tests/TEST-PPD.md` v3 | `DRAFT`, `NOT_RUN` |
| 49GAION Delivery and Implementation | `[ORG]AIOC-DI`, the last stage | `delivery-and-implementation.part-card.json` v3 | §20 | §3.1, item 5 | TEST-DELIVERY-AND-IMPLEMENTATION v3 | `github.com/49g-holding/49aioc-di`, `blueprint/DI-BLUEPRINT.md`, v0.2.0 (complete, slices 1 to 4), commit `3d7ca4397cf3b8fd3757fba9ec4e97a450aeeb64`, SHA-256 `de4d9c9683a12a1a690e5c20c18c428d49e219d5da3c8fbf3386e1bcbd8b5cc9`; its fixed test `tests/TEST-DI.md` | `DRAFT`, `NOT_RUN` |
| 49GAION Product Core | `[ORG]AIOC-PC` | `product-core.part-card.json` v1 | §18 | — | TEST-PRODUCT-CORE v1 | `github.com/49g-holding/49GAION-product-core` (its mother repository, `49GAION/DR-0024`), `blueprint/PC-BLUEPRINT.md`, v0.1.0, commit `eddd73a55c1f3c2160b369b0e6b6bd079017fa05`, SHA-256 `3c965404460429f3db7bc04c5c99131fa4c96d50b40e8003dc1780501f9db780`; its fixed test `tests/TEST-PC.md` v1 | `DRAFT`, `NOT_RUN` |
| 49GAION Operations Event Register | `[ORG]AIOC-OER`, the record of the live operation, beside Source Lifecycle | `operations-event-register.part-card.json` v1 | §22 | §3.1, item 13 | TEST-OPERATIONS-EVENT-REGISTER v1 | `github.com/49g-holding/49GAION-operations-event-register` (its mother repository, `49GAION/DR-0024`, `DR-0027`), `blueprint/OER-BLUEPRINT.md`, v0.1.0, commit `31a7ad8214c8a839276febfe4638d7d32983781f`, SHA-256 `f4eec569abde23d517355e4927c5ffe04f17da7ad26688bdcc20522cbfb6fed1`; its fixed test `tests/TEST-OER.md` v1 | `DRAFT`, `NOT_RUN` |
| 49GAION Engine Room | `[ORG]AIOC-ER`, the one hub for every AI engine and every paid external service; each unit draws from it with its own quota, and it never decides a unit's need | not yet written | — | — | not yet written | not yet written | named only, built later (`49GAION/DR-0026`) |

#### Capability parts and unit cards

| Part | Where it works | Card | Protocol | Standard | Fixed test | Status |
|---|---|---|---|---|---|---|
| AION Builder | 49GAION, accountable to its governing seat | `aion-builder.part-card.v3.json`, `aion-builder.bot-identity-card.v3.json` | §10 | §1.2, §1.3 | TEST-AION-BUILDER v2 | `DRAFT`, `NOT_RUN` |
| Self-Improvement | a process of the Cell carrying `[ORG]HOAC-TM`, served by AI Cells | `org-aion-self-improvement.part-card.v3.json`, `org-aion-self-improvement.bot-identity-card.v3.json`, `org-aion-top-management.unit-card.json` | §10 | §2 | TEST-ORG-AION-SI v2 | `DRAFT`, `NOT_RUN` |
| Duty Deputy | inside an `[ORG]AION` | `duty-deputy.part-card.json` | §16 | — | TEST-DUTY-DEPUTY v1 | `DRAFT`, `NOT_RUN` |
| Outside Inspector | outside the AIOC it inspects | `outside-inspector.part-card.json` | §16 | §3.2, item 12 | TEST-OUTSIDE-INSPECTOR v1 | `DRAFT`, `NOT_RUN` |
| Advisory Council | inside an `[ORG]AION` | `advisory-council.part-card.json` | §16 | — | TEST-ADVISORY-COUNCIL v1 | `DRAFT`, `NOT_RUN` |
| Reference Comparison | inside an `[ORG]AION` | `reference-comparison.part-card.json` | §16 | — | TEST-REFERENCE-COMPARISON v1 | `DRAFT`, `NOT_RUN` |

The v2 cards of the AION Builder and of Self-Improvement are kept and marked `REPLACED` (`library/cards/README.md`).

#### Contracts

| Contract | File | Between | Standard |
|---|---|---|---|
| Design return | `library/contracts/design-return.schema.json` | a design stage and the stage that made the release it reads | §3.1, item 6 |
| Release notice | `library/contracts/release-notice.schema.json` | a design stage and the stage after it | §3.1, item 8 |

#### Method catalogues

| Catalogue | File | Version | Standard |
|---|---|---|---|
| Reference-model catalogue | `library/reference-models/reference-model-catalogue.json` | v0.1.0, draft | §3.1, item 1 |

### Products

| Product | Kind | Parts (pinned under Parts) | Connections | Shared test | Status |
|---|---|---|---|---|---|
| 49GAION Source Lifecycle | a single part, offered alone; it runs on its own | 49GAION Source Lifecycle | none | TEST-SOURCE-LIFECYCLE v4 | `DRAFT`, `NOT_RUN` |
| 49GAION Organisation Design and Delivery | assembly | 49GAION Source Lifecycle, Target Operating Model, Process and Position Design, Delivery and Implementation | the release notice contract, from each stage to the next; the design return contract, from each later stage to the stage whose release it reads (Protocol §21) | TEST-DESIGN-CHAIN v2 (below) | named and defined, built later (`49GAION/DR-0025`); its parts `DRAFT`, `NOT_RUN`; Delivery and Implementation written in full (v0.2.0) |
| 49GAION Operations Event Register | a single part, offered alone; it runs on its own | 49GAION Operations Event Register | none | TEST-OPERATIONS-EVENT-REGISTER v1 | `DRAFT`, `NOT_RUN` |
| 49GAION Organisation Memory | assembly | 49GAION Source Lifecycle, Operations Event Register | the register's scope in Source Lifecycle (it writes origin kinds `correspondence` and `export`, and reads references only) and its gap signals (Protocol §13, item 12; §22, item 11); Source Lifecycle's notices back to the register | TEST-ORGANISATION-MEMORY v1 (below) | named and defined, built later (`49GAION/DR-0027`); its parts `DRAFT`, `NOT_RUN` |

An organisation of human positions is its output; it does not decide which positions an AI fills. The next product, for an `[ORG]AION`, may use all or some of its parts.

Organisation Memory keeps what the organisation knows beside what it did. Placed beside Organisation Design and Delivery, it closes the loop of an AI-native operation: the design runs, the register records it, and the next design starts from the record (Standard §3.1, item 14).

## TEST-DESIGN-CHAIN v2

One case for every item of the Protocol section The design chain (§21), run across the fixtures of the four stages as a cross-AIOC test (Protocol §11, item 2). Written before use; every case reads `NOT_RUN`. Version 2 (`49GAION/DR-0023`) adds cases 12 to 15, one for every bullet of §21, item 12.

1. On fixture organisations, each stage runs alone with no later stage installed, and no stage waits for a later one.
2. Every decided release is filed into Source Lifecycle under its stage's own origin kind and reads back by hash; no stage holds or edits another stage's release.
3. Every notice validates against the Library's release notice contract, its ID is its content address, it is sent only after the filing reads back, and it carries no release text and no name of a person.
4. A defect is returned to the stage that made the release, under the design return contract, with a filed copy of the same hash; Delivery and Implementation returns a defect of a target operating model release to that part, not to Process and Position Design.
5. With the fixtures run to the end, every return has ended in one of the contract's four ends; past a deadline or a set number of rounds a return reaches the Requesting Authority and the Cell carrying `[ORG]HOAC-TM`; an element carried forward on a set-aside return is marked with its basis and its decision.
6. No stage opens a new Work Item back to the stage that sent it a return.
7. After a revocation, a notice or a return through that link is refused at the gateway, and each stage still runs alone.
8. In every stage after Source Lifecycle, a seeded defect at each step is caught by the engines that did not produce it; no count, family majority, Chief of Staff or code removes a finding that has a verified quote.
9. No output of any stage names a person or reads who occupies a position.
10. Every AIOC part's mother blueprint pinned in this register reads back from its repository at the pinned commit with the pinned SHA-256.
11. The cases above run across the four stages together, each with its own fixed test passing first.
12. Where Source Lifecycle holds a dictionary, every stage reads it, and a term used in another meaning raises a contradiction.
13. What a stage leaves open (not given, not decided, not set, unknown, no observation) reaches every later stage open; a later stage that fills it fails.
14. The priority and the value case of the target operating model reach Process and Position Design and Delivery and Implementation byte-identical, by reference.
15. No record of the work about a person enters any stage, and no output of any stage says anything about a person from records of the work.

## TEST-ORGANISATION-MEMORY v1

The shared test of 49GAION Organisation Memory (`49GAION/DR-0027`), run across the fixtures of its two parts as a cross-AIOC test (Protocol §11, item 2). Written before use; every case reads `NOT_RUN`.

1. Each part's own fixed test passes first: TEST-SOURCE-LIFECYCLE v4 and TEST-OPERATIONS-EVENT-REGISTER v1.
2. Each part runs alone with the other absent: Source Lifecycle with no register, and the register with no Source Lifecycle, its feeds shown as waiting.
3. A formal outgoing letter through the gateway takes its number before it leaves. When its position asks to keep it, Source Lifecycle files it as `correspondence`, and its hash equals the entry's content hash. The reply moves the entry to answered and links its Work Item.
4. The period's projection of the work enters Source Lifecycle as an `export` by role-type and process, only after its HF-17 decision. A person field injected into it is refused at both Input sockets, and nothing of it is kept.
5. A rebuild of the register's projections equals the export Source Lifecycle serves.
6. An act done without a source raises a gap in Source Lifecycle's gap list, by reference, never as a source.
7. A source superseded in Source Lifecycle marks, in the register, the acts that cited it after its supersession.
8. Over the fixture run, no number stream has a gap or a duplicate.
9. Nothing in either part names a person or reads who occupies a position, and nothing gives a figure for one human position.

Powered by 49GAION
