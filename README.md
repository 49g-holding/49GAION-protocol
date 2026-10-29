# 49GAION Operating Protocol

**Version `v2.2.0` · approved by the governing seat (GOV) of 49GAION.**

49GAION is an organisation design framework: a framework for building organisations from interchangeable AI and human parts. This repository holds its Operating Protocol: how AIOCs, Pods, Cells and the parts work together (the unit card, the Work Item, the shared queue, the ports (one input and one output of each kind, AI and HU, plus the stop door) per unit, the input check, routing, wake, provenance and the stop rule). General level only; exact values and tools live in the Protocol of each `[ORG]AION`.

**The product: `[ORG]AION`**, the AI Operating Nexus of one organisation; its one definition is in the 49GAION Standard, §1.3, item 1 ([`49GAION/upstream/49GAION-UPSTREAM.md`](https://github.com/49g-holding/49GAION/blob/main/upstream/49GAION-UPSTREAM.md)).

**The complete definition (DR-0041).** The complete definition of 49GAION, approved by its governing seat on 25 October 2026, is [`49GAION-FRAMEWORK.md`](https://github.com/49g-holding/49GAION/blob/main/49GAION-FRAMEWORK.md) in the hub. Where this repository, or the Standard, differs from it, the complete definition governs, and the text is read with it until it is brought into line. The additions marked DR-0041 in this repository bring it into line; nothing is removed.

## What is here

| Path | Holds |
|---|---|
| [`spec/49GAION-OPERATING-PROTOCOL.md`](spec/49GAION-OPERATING-PROTOCOL.md) | The protocol |
| [`spec/schemas/`](spec/schemas/) | Machine schemas: unit card (AIOC, Pod and Cell, with the HOAC label as a field), Work Item, shared status list, part card, bot identity card, `[ORG]AION` record, Port card; since v1.5.0 also the signature record and the process record |
| [`library/README.md`](library/README.md) | **The Library register** (GOV, 16 October 2026): every Library part named once, with its card, Protocol section, Standard item, fixed test and, for an AIOC part, its mother blueprint pinned by repository, path, version, commit and SHA-256; and TEST-DESIGN-CHAIN v2 |
| [`library/cards/`](library/cards/) | Library cards of the Self-Improvement AIOC (read, v1.5.0: of the Self-Improvement process in TM and the bots serving it), and of every part added since |
| [`library/contracts/`](library/contracts/) | The Library's contracts: the design return and the release notice, with their examples and their check |
| [`library/reference-models/`](library/reference-models/) | The reference-model catalogue, a method catalogue of the Library (GOV, 16 October 2026) |
| [`tests/`](tests/) | Schema tests |
| [`tests/cards/`](tests/cards/), [`tests/signatures/`](tests/signatures/), [`tests/work-items/`](tests/work-items/) | Must-pass and must-fail fixtures of the machine forms; superseded fixtures kept in `tests/cards/superseded/` (v1.5.0) and `tests/signatures/sets/superseded/` (GOV, 15 October 2026) |
| [`tests/orgs/`](tests/orgs/) | Reference organisations, checked against the rules on the GOV seat, the Human Floor, the stop door and the accountability chain (GOV, 21 October 2026) |
| [`tests/verdicts/`](tests/verdicts/), [`tests/action-classes/`](tests/action-classes/) | Must-pass and must-fail fixtures of the verdict record and the standing action class (GOV, 14 October 2026) |
| [`decisions/`](decisions/) | Links to the decision records, kept once in the hub |

## Related repositories

| Repository | Holds |
|---|---|
| [`49GAION`](https://github.com/49g-holding/49GAION) | The hub: the 49GAION Standard, the master definition, the Naming Standard |
| [`49GAION-aioc`](https://github.com/49g-holding/49GAION-aioc) | What an AIOC is and the blueprint template |

## Rules

- Changes by pull request with green checks; `main` is protected.
- No secret in any file, commit, issue or pull request.

## Owner and licence

- **Owner and licence.** The copyright holder, and the licences of the texts (CC BY 4.0, credit "Powered by 49GAION") and of the code (Apache-2.0), are in [`LICENSE.md`](LICENSE.md).

Powered by 49GAION
