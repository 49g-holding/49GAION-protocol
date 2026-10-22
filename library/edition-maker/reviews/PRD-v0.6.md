# Reviews of the Edition Maker PRD v0.6, the rule "no step on one engine" (raw)

Asked on 22 October 2026, about 17:15 UTC, through a reviewer server. The PRD was written by one engine (Claude). Two other engines challenged it, each given the same extracts of the rule and the parts it touches. The answers are kept as received, except that a bare requirement number is written with its "EM-" prefix, so that it reads as a requirement of the PRD.

## Gemini (gemini-4-argon)

(1) Contradictions and errors: Chicken-and-egg: allowed engines are gathered in "gather", yet EM-R0 requires multiple engines in the preceding "open" step before the owner has consented. Redundancy: in "check", two engines critique the pack (EM-R17); under EM-R0 those must themselves be critiqued. Obsolete test: EM-R18 is pointless if every step already runs on two or three engines. Role confusion: "approve" is listed in EM-R0 as an AI step, but Principle 6 says a human seat decides. Test mismatch: TC 18 requires two challenging engines, breaking when an owner allows only two engines. UX bottleneck: challenging every question before asking the owner will grind "complete" to a halt.
(2) Missing: tie-breaking (who decides when worker and challengers deadlock; how critique loops stop); privacy (raw sources with personal data sent to three suppliers); single-engine fallback; cost (caps, cheaper challengers).
(3) First changes: exempt early and human steps; define the resolution loop (one round; the worker engine has the final word before human review, logging unresolved dissent); delete EM-R17 and EM-R18, folding their intent into the compose step's critique.

## OpenAI (gpt-6-astra)

(1) Principle 8 says "two or three" engines but requires three roles; EM-R0 permits two; EM-R17, core instruction 5, setup 9.1 and test 18 still require three. "Every step", including approval, assigns the work to an engine; Principle 6 reserves decisions to a human. The rule is not permanently binding: Principle 2 permits amendment after handover; state whether that is intended. EM-R16 bans personal data in the pack, not processing; EM-R22's private store does not prevent disclosure to external engines; EM-R17's "never with personal data" needs a defined scope. EM-R18's portability test is distinct from critique. Test 18 verifies only four activities, not every step.
(2) Define: what counts as a step and a distinct engine; whether critics review independently; how findings are answered, disagreements resolved, serious objections escalated, retries stopped; who accepts residual risk (engines must not approve their own disputes); per-engine data permissions, redaction, retention, logging, consent withdrawal; cost, latency and retry limits; outage handling; what happens when only one engine is authorised; whether critique records belong in the pack and how they satisfy EM-R16.
(3) Unify the rule (three normally, an explicit two-engine exception, pause when only one is authorised; clarify post-handover amendment); specify the workflow (independent critiques, recorded responses, bounded retries, human resolution of material disagreements); add enforceable gates (data permissions, spending limits, tests covering every named step).

## What was applied, and what was not

Applied in v0.6: EM-R0 rewritten (distinct engine; independent critiques; one round; the writer answers each finding; a material dispute goes to the owner with both views; no engine settles its own dispute; human acts never done by an engine; no personal data in the records; three by default, two recorded, one means the step waits; no owner data to any engine before consent; per-engine data; cost and time within the edition's limits); EM-R2a (consent and engines first); EM-R9 (questions challenged as one set); EM-R17 (the compose step's challenge round, not challenged again); intake items 9 and 10; principle 8 (the organisation may amend it after the handover); core instruction item 5; test case 18 (every step where an engine worked).

Not applied:
1. "Delete EM-R17 and EM-R18" (Gemini). EM-R18 is the exit-plan test, that the pack runs on another engine; it is not a critique, as OpenAI also says. EM-R17 is kept as the compose step's challenge round.
2. "The worker engine has the final word before human review" (Gemini). A finding that matters and is still in dispute goes to the owner with both views; no engine settles a dispute about its own work.
