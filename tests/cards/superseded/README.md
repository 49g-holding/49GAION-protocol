# Superseded card fixtures

These four cards were the must-pass set up to v1.4.0. They are superseded by the corrected cards of v1.5.0 (Standard §1.7, items 12 and 13) and kept unchanged for the record. They are no longer in the must-pass set, and `tests/cards/check_cards.py` reports them only for reading.

| Superseded card | Why | Corrected copy |
|---|---|---|
| `valid-card.json` | An AIOC with a Cell as `parent` (`TenCELL-TMS`); a Cell is never a parent | `../valid-aioc-card.json`, `../valid-charter-card.json` |
| `valid-ai-cell-card.json` | An attached AI Cell with its person's Cell as `parent`; it sits in the same Blueprint as that Cell | `../valid-ai-cell-card.v15.json` |
| `valid-cell-card.json` | A Cell with `parent: none`; only the Charter has no parent | `../valid-human-cell-card.json`, `../valid-gov-cell-card.json` |
| `valid-pod-card.json` | A Pod with a HOAC label and no `label_holder`; no ports or fixed test | `../valid-pod-card.v15.json`, `../valid-board-pod-card.json` |

Powered by 49GAION
