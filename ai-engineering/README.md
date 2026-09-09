# AI Engineering Ladder

Target: be able to attack Harbour (Open Problem 01) as a senior engineer.

## The spine

An LLM is a **stateless, non-deterministic function from text to text, with no ability to act.**
Four consequences follow, and every topic below manages one of them. When you meet a new
AI-engineering idea, ask which row it belongs to. If it belongs to none, it is probably fashion.

## Phases

- [ ] **Phase 0 — The mental model** (½ day, no code)
- [ ] **Phase 1 — The model as a function** (1 day, ~80 lines)
- [ ] **Phase 2 — Observe–Think–Act: the minimum harness** (1–2 days, ~150 lines)
- [ ] **Phase 3 — The loop taxonomy, measured** (2–3 days) — OTA / ReAct / Plan-Execute / Ralph
- [ ] **Phase 4 — Observability** (2 days) — OpenTelemetry, OTLP, cost per case
- [ ] **Phase 5 — Evaluation, determinism, drift** (3 days) — record/replay, mutation testing
- [ ] **Phase 6 — Trust, authority, failure** (3 days) — injection, audit log, HITL, checkpointing
- [ ] **Phase 7 — System design capstone** (~1 week) — paper-to-code agent
- [ ] **Phase 8 — Harbour**

## The seven standing questions

Ask these of any AI system, including ones you didn't build.

1. Where does authority live? Which line of code decides an action actually happens?
2. What's the smallest amount of model I can use?
3. How would I know this broke?
4. What does one unit of work cost?
5. What's the failure path — designed, or accidental?
6. What here is untrusted?
7. Can my tests fail?

## Rules of the road

- No frameworks until Phase 7 at the earliest. Hand-roll everything.
- Every phase produces working code you keep and reuse in the next phase.
- Write down what you believed *before* you had evidence. The delta is the learning.
