# Phase 1 — The model as a function

**1 day. ~80 lines of code total. Four experiments.**

Goal: replace every intuition you have about LLM cost and determinism with a number
you measured yourself. When you later argue "the retry loop is what's spiking the
bill," you want to be reasoning from measurement, not from vibes.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

Python 3.11+ recommended (you're on 3.9 — upgrade first).

Total spend for this whole phase: well under $1.

## Model facts you need

| Model | ID | Input $/1M | Output $/1M |
|---|---|---|---|
| Claude Opus 5 (default) | `claude-opus-5` | $5.00 | $25.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | $1.00 | $5.00 |

**Two things that will confuse you if nobody warns you:**

1. **Opus 5 thinks by default.** Omitting the `thinking` parameter runs adaptive
   thinking. Those thinking tokens are billed as output tokens and count against
   `max_tokens`, but the raw reasoning is never returned to you. So your first cost
   measurement will include output you cannot see. This is not a bug — note it.

2. **Opus 5 rejects `temperature`, `top_p`, and `top_k` with a 400.** The sampling
   knobs are gone on this generation; depth is controlled by
   `output_config={"effort": ...}` instead. This is why Experiment 2 uses
   Haiku 4.5 — not because it's cheaper, but because it's the model that still
   *has* the parameter you need to probe.

---

## Experiment 1 — One call, one cost

Send one message to `claude-opus-5`. Print:
- the response text
- `response.usage.input_tokens`
- `response.usage.output_tokens`
- `response.stop_reason`
- the computed dollar cost

Write a `cost(usage, model)` helper. **You will reuse this function in every
remaining phase of the ladder** — it's the first brick of your library.

**Done when:** you have a cost function you trust.

---

## Experiment 2 — How non-deterministic is it, really?

Use `claude-haiku-4-5` (it accepts `temperature`; Opus 5 does not).

Send the *same* prompt 20 times at `temperature=0`. Count how many distinct
outputs you get. Then repeat at `temperature=1`.

Pick a prompt with room to vary — "Name a programming language and say one
sentence about it" beats "What is 2+2?".

**Done when:** you can state, from your own data, how much variance you observed
at temperature 0. Do not assume it will be zero.

**Then:** send a request to `claude-opus-5` with `temperature=0.5`. Catch the
error. Read what it says. That 400 is the API telling you something about how
this generation of models is meant to be steered.

---

## Experiment 3 — What does context actually cost?

Ask the same question twice:
- once with ~200 tokens of context
- once with ~20,000 tokens of context (paste a long file in)

For each, record: input tokens, output tokens, cost, wall-clock latency.

**Done when:** you have a small table of your own numbers, and you can say what
the marginal cost of 20k tokens of context is in dollars and seconds.

This is Row 1 of the table becoming a number. Every turn of an agent loop pays
this again.

---

## Experiment 4 — Structured output, and what happens when it can't comply

Force a JSON schema with `output_config={"format": {"type": "json_schema",
"schema": {...}}}`. Extract a name and email from a sentence.

Then **break it deliberately**: ask it to extract a name and email from a sentence
that contains neither. Observe what comes back and what `stop_reason` is.

**Done when:** you have seen the failure and handled it, rather than assuming it
won't happen. Every tool call in Phase 2 is this same problem.

---

## Also: keep a stop_reason census

Print `stop_reason` on every call in every experiment. By the end, list every
value you saw and what you would do about each in a real system.

You will need `tool_use` in Phase 2, and `refusal` and `max_tokens` are both
things a production loop must handle.

---

## Deliverable

- `probe.py` — all four experiments, runnable
- `findings.md` — your numbers, filled in from the template
