# The starting setup

You may change all of it.

1. A versioned record for the Standard, the Blueprint, the decisions and each unit's spec.
2. A durable workflow engine: the shared queue of work.
3. A shared state store and an append-only log of who did what.
4. One connector, with a separate identity for each unit.
5. Units that run as code, from their spec in the record.
6. A trace of every step, visible to the human seats.
7. A stop outside the AI: it revokes the unit's credential and cancels its work.

**Phase one.** A small organisation may start with the record, one state store and the stop.

Each unit carries a fixed test, a spending cap and a stop rule, versioned improvements with a restore point, and a stop door with an accountability chain that ends at the governing seat. A human seat signs each listed signature type; the workspace holds no keys.
