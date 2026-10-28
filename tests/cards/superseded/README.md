# Superseded card fixtures

These four cards were the must-pass set up to v1.4.0. They are superseded by the corrected cards of v1.5.0 (Standard §1.7, items 12 and 13) and kept unchanged for the record. They are no longer in the must-pass set, and `tests/cards/check_cards.py` reports them only for reading.

`valid-board-pod-card.json` was in the must-pass set up to `49GAION/DR-0049`. A HOAC label is held by one position, its `label_holder`; a board behind a position is the organisation's own mechanism, outside the system (the complete definition, §6), so a card with a `decision_rule` is refused (`../must-fail-decision-rule-withdrawn.json`). It is kept unchanged for the record.

| Superseded card | Why | Corrected copy |
|---|---|---|
| `valid-card.json` | An AIOC with a Cell as `parent` (`TenCELL-TMS`); a Cell is never a parent | `../valid-aioc-card.json`, `../valid-charter-card.json` |
| `valid-ai-cell-card.json` | An attached AI Cell with its position's Cell as `parent`; it sits in the same Blueprint as that Cell | `../valid-ai-cell-card.v15.json` |
| `valid-cell-card.json` | A Cell with `parent: none`; only the Charter has no parent | `../valid-human-cell-card.json`, `../valid-gov-cell-card.json` |
| `valid-pod-card.json` | A Pod with a HOAC label and no `label_holder`; no ports or fixed test | `../valid-pod-card.v15.json` |
| `valid-board-pod-card.json` | A Pod carrying a HOAC label through a `decision_rule` (a board behind the label); withdrawn by `49GAION/DR-0049` | `../valid-pod-card.v15.json` |

Powered by 49GAION
