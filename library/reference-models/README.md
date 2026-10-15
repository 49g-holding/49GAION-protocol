# The reference-model catalogue

**Addition (GOV, 16 October 2026; `49GAION/DR-0022`).** `reference-model-catalogue.json`, version `v0.1.0`, status `draft`, valid against `reference-model-catalogue.schema.json` in this folder. A method catalogue of the 49GAION Library (Standard §3.1, item 1).

## What it is

A catalogue of operating-model patterns: widely known ways to organise, each with its typical capabilities, its decision rights by role-type, its typical hand-offs, when it fits and when it does not, and its known risks. A design part may read it as a method, never as evidence about an organisation. It is read by version and SHA-256, and it changes only by a new version. It holds no organisation's data and no text copied from any source.

## The rules every reader keeps

1. A pattern is a method. It may suggest a structure; it never states a fact about an organisation.
2. Every element a pattern suggests still needs the organisation's own evidence. Without it, the element is an assumption, with what breaks if it is false.
3. A pattern never raises the label of a statement, never closes an unknown and never settles a contradiction.
4. A pattern names role-types only: never a person or a position.
5. This catalogue holds no organisation's data and no copied text. Each pattern is a plain description of a widely known way to organise.

## The patterns of `v0.1.0`

| ID | Name | In one paragraph |
|---|---|---|
| `RMP-FUNCTIONAL` | Functional organisation | Work is grouped by kind of expertise, such as sales, operations, finance and people. Each function has one accountable lead, and the top role joins the functions together. |
| `RMP-DIVISIONAL` | Divisional organisation | The organisation is split into divisions by product, market, customer group or region. Each division holds most of the functions it needs and answers for its own results, under a small centre. |
| `RMP-MATRIX` | Matrix organisation | Two lines of accountability cross: one by function or expertise, one by product, project, market or region. Many roles answer to both, so the decision rights must say which line decides what. |
| `RMP-SHARED-SERVICE` | Shared-service centre | Common support work, such as finance processing, people administration, purchasing or information services, is done once, in one centre, for several units, under agreed service terms. |
| `RMP-HOLDING` | Holding with independent subsidiaries | A parent owns several subsidiaries. Each runs as an independent entity, with its own management and its own governing body. The parent acts as owner, not as operator. |
| `RMP-PLATFORM` | Platform with business units | A central platform provides common capabilities, such as customer access, technology, data, payments or brand, and several business units build their own offers on it. The units own their markets and results; the platform owns the shared capabilities. |
| `RMP-SOLO` | Single-position practice | One position, the practitioner, does or directs all the work, with clients, suppliers, advisers and authorities at the boundary. The roles are hats the one position wears, so the model names each role-type that position carries and what each decides. |

## How a part takes it into use

A part pins one version of the catalogue by its version, the commit of this repository and the SHA-256 of `reference-model-catalogue.json`, as a tested change of that part. Until it is pinned, the part declares the catalogue unavailable and cites no pattern. The mother blueprint of the Target Operating Model reads it at its design stage (its §5.5 and Annex E.19).

## How it changes

A new pattern, or a change to one, is a new version of the catalogue, made by pull request and merged by the governing seat of 49GAION. A pattern ID is never reused. `python3 library/contracts/check_contracts.py` validates the catalogue against its schema, checks that every pattern carries the sentence "This pattern is never evidence for an organisation.", and refuses a pattern that names a person.

Powered by 49GAION
