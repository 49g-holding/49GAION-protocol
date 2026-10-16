# Library contracts

**Addition (GOV, 15 October 2026).**

| File | What it is |
|---|---|
| `design-return.schema.json` | The design return: a notice from a design stage to the stage that made the release it reads. Five kinds; elements and evidence by reference, never a person; never new release text; a round count; and an end for every return: answered by release, answered by decision, set aside by decision and carried forward on a stated basis, or withdrawn (Protocol §17, item 11; Standard §3.1, item 6) |
| `examples/` | Valid and must-fail examples of the design return; the reason for each must-fail example is in `examples/MUST-FAIL-REASONS.json` |
| `release-notice.schema.json` | **Addition (GOV, 16 October 2026; `49GAION/DR-0019`).** The release notice: a notice from a design stage to the stage after it, sent on every filing of a decided release. It points to the filed release by reference (ID, version and manifest hash), names the releases it rests on, the filed copy, the final-status decision and the returns it answers; it never carries release text or the name of a person. Its ID is its content address. A stage's own notice contract may narrow a field; it never adds or removes one (Protocol, the section The design chain; Standard §3.1, item 8) |
| `examples/release-notice/` | Valid and must-fail examples of the release notice, with their reasons |
| `check_contracts.py` | `python3 library/contracts/check_contracts.py`: every valid example of each contract validates, every must-fail example is refused and has its reason, every notice ID is its content address, and the reference-model catalogue (`library/reference-models/`) validates and names no person; exit 1 on any failure. Run in CI by `card-schema-test` |

Powered by 49GAION
