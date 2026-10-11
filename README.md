# 49GAION Operating Protocol

**Version `v1.0.0` · approved by Iman Tajik (Founder).**

49GAION is an organisation design framework: a framework for building organisations from interchangeable AI and human parts. This repository holds its Operating Protocol: how AIOCs and the parts work together (the card, the Work Item, the shared queue, typed ports (two inputs, two outputs, AI/HU) plus a stop door per unit, the input check, routing, wake, provenance, the stop rule and ports). General level only; exact values and tools live in the Protocol of each `[ORG]AION`.

**The product: `[ORG]AION`.** 49GAION's product is `[ORG]AION`, the AI Operating Nexus of one organisation (for example "Nike AION, Powered by 49GAION"). Each `[ORG]AION` is built for one organisation and is not public. It is a complete organisation design: it contains its own Standard, Protocol, Library, Self-Improvement, AIOCs and HOACs, and the organisation is built from it. It has its own `[ORG]HOAC-GOV` from day one, so its top authority is that organisation, not 49GAION, and it stands on its own Human Floor. Every AIOC in an `[ORG]AION` has its own runtime, woken from its queue. The AION Builder builds each `[ORG]AION` over a design period; once delivered, the `[ORG]AION` belongs entirely to the customer.

## What is here

| Path | Holds |
|---|---|
| [`spec/49GAION-OPERATING-PROTOCOL.md`](spec/49GAION-OPERATING-PROTOCOL.md) | The protocol |
| [`spec/schemas/`](spec/schemas/) | Machine schemas: AIOC card, Work Item, shared status list, part card, bot identity card, `[ORG]AION` record, Port card |
| [`library/cards/`](library/cards/) | Library cards of the AION Builder and `[ORG]AION` Self-Improvement |
| [`tests/`](tests/) | Schema tests |
| [`decisions/`](decisions/) | Decision records of this repository |

## Related repositories

| Repository | Holds |
|---|---|
| [`49GAION`](https://github.com/49g-holding/49GAION) | The hub: the 49GAION Standard, the master definition, the Naming Standard |
| [`49GAION-aioc`](https://github.com/49g-holding/49GAION-aioc) | What an AIOC is and the blueprint template |

## Rules

- Changes by pull request with green checks; `main` is protected.
- No secret in any file, commit, issue or pull request.

Powered by 49GAION
