# Library contracts

**Addition (GOV, 15 October 2026).**

| File | What it is |
|---|---|
| `design-return.schema.json` | The design return: a notice from a design stage to the stage that made the release it reads. Five kinds; elements and evidence by reference, never a person; never new release text; a round count; and an end for every return: answered by release, answered by decision, set aside by decision and carried forward on a stated basis, or withdrawn (Protocol §17, item 11; Standard §3.1, item 6) |
| `examples/` | Valid and must-fail examples; the reason for each must-fail example is in `examples/MUST-FAIL-REASONS.json` |
| `check_contracts.py` | `python3 library/contracts/check_contracts.py`: every valid example validates, every must-fail example is refused and has its reason; exit 1 on any failure |

Powered by 49GAION
