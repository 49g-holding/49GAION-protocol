# Reviews of the governing seat's model for Edition Maker's output (raw)

Asked on 22 October 2026, about 23:10 UTC on 21 October, through a reviewer server, on the governing seat's direction to challenge his model from the building side (GOV, 22 October 2026). Each reviewer got the same prompt, below. The answers are kept as received. Claude's answer was cut off after its four points, before "what is missing".

## The prompt

An owner proposes how a framework should start an AI-native organisation. Challenge it from the side of actually building and running it. In at most 250 words, plain English, no praise: the 4 weakest points, each with one concrete fix; then anything important that is missing.

The model:
1. A starter ("Edition Maker") takes in the organisation's outputs, inputs, limits, owner, money and time. It hands over only what the organisation's core needs to start: the framework's rules and definitions (naming, musts and must-nots, which work always stays human, what a unit, a cell and a human accountability seat are), the spirit of the framework (start from outputs, AI first, humans cover AI's gaps and are accountable), the framework's library of ready-made unit designs, and the organisation's own first rule sheet and blueprint. The core may amend these as it builds, with the owner's approval.
2. The core is itself one AI unit, delivered as one project in an AI assistant: an instruction plus these files.
3. The core first writes its own target AI operation (what AI-native operation the organisation needs), then asks the human owner, by proposal, how to divide the organisation and how human each part should be.
4. From the answers it decides how many AI units there are and their scope, writes each one as its own project, and lets each one improve itself as far as the owner wants.
5. Each unit joins: for operation, it reports to the top management unit; for decisions and installation, to the human owner.
6. The core then monitors: where there is a gap it defines a new unit; where units are idle it merges them.
7. Each unit's core is a project. It grows its capabilities until it reaches the best quality; then it builds its own panel (a web console where humans read reports, use it and decide), and the project becomes the panel's back office.
8. The core governs and builds; it never runs operation.


---

## OpenAI (gpt-6-astra)

1. **An assistant project is not a running unit.** Instructions and files do not provide reliable scheduling, shared records, permissions or recovery when work fails. **Fix:** Build one working unit around a controlled workflow, with durable task records, approved tools, retries and a human escalation route. Treat the project as its interface, not its operating machinery.

2. **The organisation is divided before its work is proven.** Asking the owner how many parts should exist, and how human they should be, risks designing boxes around guesses. **Fix:** Run one real output from request to delivery; measure quality, cost, delay and human intervention, then define unit boundaries from the evidence.

3. **Authority is split, while operational responsibility is unclear.** Reporting to management for work and the owner for decisions creates competing instructions and an approval bottleneck. The non-operating core cannot fill that gap. **Fix:** Name an operational lead and give every unit a written decision boundary, spending limit and escalation path; reserve only specified decisions for the owner.

4. **Self-improvement and restructuring lack safe triggers.** "Best quality" is undefined; a gap may need a process repair, not another unit, and idle capacity may be intentional. **Fix:** Require measured benefits, tests and rollback for changes; provide a basic human control screen from day one.

**Missing:** Data ownership and access rules; security and legal checks; acceptance standards for outputs; incident response and service continuity; full costs, including human review; and a funded, named human accountable for each live service.

---

## Gemini (gemini-4-argon)

**4 Weakest Points and Fixes**

1. **AI assistant projects are passive.** A project (like a Custom GPT or Claude Project) is just a chat window with text files. It cannot monitor units, merge them, or run operations on its own.
*Fix:* Build the core on an agent orchestration backend (e.g., LangGraph) with database access, cron jobs, and API triggers.

2. **Units cannot talk to each other.** Separate projects are isolated silos. A unit cannot report to a "top management unit" without a human manually copying and pasting text between chats.
*Fix:* Create a shared message bus and central database so units exchange structured JSON data automatically.

3. **Unchecked self-improvement breaks systems.** Letting units "improve" their own prompts and rules leads to prompt drift, hallucinations, and broken workflows.
*Fix:* Lock unit instructions in version control (Git). Require automated testing against a fixed benchmark before the owner approves any change.

4. **Custom web panels create maintenance chaos.** Having every unit code and host its own web console creates a tangled mess of frontends, broken code, and security holes.
*Fix:* Build one unified human dashboard that reads standard schemas from all units.

**What Is Missing**

* **Tool and API access:** How units actually act on the world (sending emails, charging cards, reading databases).
* **Memory management:** How the organisation stores long-term state once chat context windows fill up.
* **Cost and loop circuit-breakers:** Hard limits to stop two units from triggering each other infinitely and draining the bank account.

---

## Grok (grok-4.7)

The core is a chat project, not a system that can run anything. An instruction plus files cannot install units, keep state, enforce rules, or tell when a unit stalls or lies. Chat context forgets, and there is no audit trail. Fix: give the core a persistent record, a scheduler, and an append-only log before it creates any unit.

Self-improvement has no hard stop. Money and time enter the starter, then vanish. Units may "improve as far as the owner wants," with no spend cap, deadline, or definition of done. Fix: every unit charter must state a budget, a deadline, and a stop rule the core checks before any change.

Humans cannot see or stop work until a panel exists. "Best quality" is undefined, and the console comes only after growth—the riskiest phase. Fix: set a written pass/fail test and require human sign-off before a unit widens scope; show live status from day one.

Nobody owns live operation. The core builds and never runs. Units report to a top management unit that is never created, and to the owner only for "decisions." A bad action in production has no named stopper. Fix: name one human operating owner, separate from the builder, with the right to halt any unit immediately.

Missing: a kill switch and rollback; rules for secrets, customer data, and money movement; how units call real systems and each other; what happens if the owner is away; how promised outputs are measured and fed back; who is legally liable when a unit acts.

---

## Claude (claude-opus-5-5)

**1. A chat project can't run or watch anything.**
An assistant project has no memory between sessions, no scheduler and no live data. So "the core monitors" and "units report" have nothing underneath them.
*Fix:* Keep all state, logs and unit specs in a shared repository and database. Run the core and units on scheduled jobs that read and write there. The project is only the editor.

**2. Self-amendment and self-improvement will drift.**
Rules, blueprints and units changing themselves, approved one by one, become untraceable within weeks.
*Fix:* Treat every change as a versioned diff. Each diff comes with test cases, and none goes live without passing them and having a rollback ready.

**3. "Best quality" is undefined, and every unit builds its own panel.**
Units will never stop improving, or will stop at random. You also end up with dozens of inconsistent, insecure consoles.
*Fix:* Set measurable acceptance targets per unit at creation. Generate all panels from one shared, centrally maintained template.

**4. The owner is a bottleneck, and split reporting causes conflict.**
Every decision and installation goes to one person. Meanwhile, operations answer to a management unit that may disagree with the owner.
*Fix:* Define decision classes with limits. Routine changes are pre-approved, and only items above set cost or risk thresholds reach the owner. Set one rule for which line wins in a conflict.

*(cut off here)*

---

Powered by 49GAION
