# The 49GAION Library

**Addition (GOV, 16 October 2026; `49GAION/DR-0019`).** The 49GAION Library holds every ready-made part of 49GAION: its AIOC parts with their mother blueprints, its capability parts, its unit cards, its contracts and its method catalogues (Standard §3.1). Built once, configured per `[ORG]AION`, never rebuilt. This file is its register: every part is named here once.

## How a part is held

- **Its card** sits in `library/cards/`, valid against `spec/schemas/part-card.schema.json`, `DRAFT` with `last_result` `NOT_RUN` until its fixed test has run once with recorded evidence (Protocol §10, item 3).
- **Its rules** sit in its Protocol section, and its place in the Standard in §3.1.
- **Its mother blueprint**, for an AIOC part, is written in its own writing repository, for any organisation, with `[ORG]` placeholders and no organisation's data. The Library holds it by pin: repository, path, version, commit and the SHA-256 of the blueprint file. A new version reaches the Library only by a pull request that moves the pin, merged by the governing seat of 49GAION. An organisation's instance keeps its own values in its own records repository.
- **One home.** The text lives in one place; the Library holds its pin, never a second copy.
- **A pin before its merge.** A pin may name the head commit of the writing repository's pull request that carries the version; when that pull request is merged, the pin moves to the merged commit, with the same SHA-256.

## The register

### AIOC parts

| Part | In an `[ORG]AION` | Card | Protocol | Standard | Fixed test | Mother blueprint | Status |
|---|---|---|---|---|---|---|---|
| 49GAION Source Lifecycle | `[ORG]AIOC-SL`, the first stage | `source-lifecycle.part-card.json` v2 | §13 | §3.1, item 7 | TEST-SOURCE-LIFECYCLE v2 | not yet held: the first instance's blueprint is private and holds an organisation's data; a mother for any organisation is to be written from it | `DRAFT`, `NOT_RUN` |
| 49GAION Target Operating Model | `[ORG]AIOC-TOM`, the second stage | `target-operating-model.part-card.json` v2 | §19 | §3.1, item 4 | TEST-TARGET-OPERATING-MODEL v2 | `github.com/49g-holding/49aioc-tom`, `blueprint/TOM-BLUEPRINT.md`, v0.5.0, commit `00d1e086f12a74437d1aea4cdbd092ce4978a7c2` (pull request #3), SHA-256 `a90b3b5b6a0bbb288cb6078df255304715a79c061a38e5b2c53b5aabb11f336a`; its fixed test `tests/TEST-TOM.md` v4 | `DRAFT`, `NOT_RUN` |
| 49GAION Process and Position Design | `[ORG]AIOC-PPD`, the third stage | `process-and-position-design.part-card.json` v3 | §17 | §3.1, item 3 | TEST-PROCESS-AND-POSITION-DESIGN v3 | `github.com/49g-holding/49aioc-ppd`, `blueprint/PPD-BLUEPRINT.md`, v0.4.0, commit `2d5b69c382a20ab35ee88cd1357f1431c2b6406b` (pull request #5), SHA-256 `39708621823c9031429ba758c9d7ad15e4935ce577dc317e5d1eb412cd5b73a0`; its fixed test `tests/TEST-PPD.md` v2 | `DRAFT`, `NOT_RUN` |
| 49GAION Delivery and Implementation | `[ORG]AIOC-DI`, the last stage | `delivery-and-implementation.part-card.json` v2 | §20 | §3.1, item 5 | TEST-DELIVERY-AND-IMPLEMENTATION v2 | `github.com/49g-holding/49aioc-di`, `blueprint/DI-BLUEPRINT.md`, v0.1.1 (slice 1 of 4), commit `026fb281df98d6e1dccf9541cac05f4528a5cb1b` (pull request #3), SHA-256 `0b04f49fb8e5b65be882cb9d14bb5e940f6d21c8b1b733c042cc72e2af1b183e`; its fixed test `tests/TEST-DI.md` | `DRAFT`, `NOT_RUN` |
| 49GAION Product Core | `[ORG]AIOC-PC` | `product-core.part-card.json` v1 | §18 | — | TEST-PRODUCT-CORE v1 | written in its own repository (Protocol §18); not yet pinned here | `DRAFT`, `NOT_RUN` |

### Capability parts and unit cards

| Part | Where it works | Card | Protocol | Standard | Fixed test | Status |
|---|---|---|---|---|---|---|
| AION Builder | 49GAION, accountable to its governing seat | `aion-builder.part-card.v3.json`, `aion-builder.bot-identity-card.v3.json` | §10 | §1.2, §1.3 | TEST-AION-BUILDER v2 | `DRAFT`, `NOT_RUN` |
| Self-Improvement | a process of the Cell carrying `[ORG]HOAC-TM`, served by AI Cells | `org-aion-self-improvement.part-card.v3.json`, `org-aion-self-improvement.bot-identity-card.v3.json`, `org-aion-top-management.unit-card.json` | §10 | §2 | TEST-ORG-AION-SI v2 | `DRAFT`, `NOT_RUN` |
| Duty Deputy | inside an `[ORG]AION` | `duty-deputy.part-card.json` | §16 | — | TEST-DUTY-DEPUTY v1 | `DRAFT`, `NOT_RUN` |
| Outside Inspector | outside the AIOC it inspects | `outside-inspector.part-card.json` | §16 | §3.2, item 12 | TEST-OUTSIDE-INSPECTOR v1 | `DRAFT`, `NOT_RUN` |
| Advisory Council | inside an `[ORG]AION` | `advisory-council.part-card.json` | §16 | — | TEST-ADVISORY-COUNCIL v1 | `DRAFT`, `NOT_RUN` |
| Reference Comparison | inside an `[ORG]AION` | `reference-comparison.part-card.json` | §16 | — | TEST-REFERENCE-COMPARISON v1 | `DRAFT`, `NOT_RUN` |

The v2 cards of the AION Builder and of Self-Improvement are kept and marked `REPLACED` (`library/cards/README.md`).

### Contracts

| Contract | File | Between | Standard |
|---|---|---|---|
| Design return | `library/contracts/design-return.schema.json` | a design stage and the stage that made the release it reads | §3.1, item 6 |
| Release notice | `library/contracts/release-notice.schema.json` | a design stage and the stage after it | §3.1, item 8 |

### Method catalogues

| Catalogue | File | Version | Standard |
|---|---|---|---|
| Reference-model catalogue | `library/reference-models/reference-model-catalogue.json` | v0.1.0, draft | §3.1, item 1 |

## TEST-DESIGN-CHAIN v1

One case for every item of the Protocol section The design chain (§21), run across the fixtures of the four stages as a cross-AIOC test (Protocol §11, item 2). Written before use; every case reads `NOT_RUN`.

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

Powered by 49GAION
