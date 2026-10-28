# Superseded signature sets

These sets are kept unchanged for the record. They are no longer in the must-pass or must-fail sets, and `tests/cards/check_cards.py` reports them only for reading.

- `must-fail-dual-one-person-two-cells.json` was a must-fail case up to the direction of GOV of 15 October 2026. Two positions are two parties, even when one natural person occupies both (Standard §1.1, item 10; Protocol §4.10, item 13), so the case it tested no longer fails.
- `valid-dual-two-persons.json` and `valid-dual-one-occupant-two-positions.json` passed up to `49GAION/DR-0049`. They recorded references to persons (a pseudonymous identity reference, a signer role and a credential bound to one person), which the system no longer holds (the complete definition, §6).

| Superseded set | Why | Current case |
|---|---|---|
| `must-fail-dual-one-person-two-cells.json` | It failed dual signature because one occupant signed under two Cells; two Cells are two parties and count as two | `../valid-dual-two-positions.json` |
| `valid-dual-two-persons.json` | It carried references to persons; the system records no person and no reference to one (`49GAION/DR-0049`) | `../valid-dual-two-positions.json` |
| `valid-dual-one-occupant-two-positions.json` | It carried one identity reference under two positions; with no person recorded, the case is two signing positions (`49GAION/DR-0049`) | `../valid-dual-two-positions.json` |

Powered by 49GAION
