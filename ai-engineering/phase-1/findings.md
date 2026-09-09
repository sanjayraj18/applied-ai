# Phase 1 findings — my own measurements

Date:

## Experiment 1 — Cost of one call

| | |
|---|---|
| Model | |
| Prompt used | |
| Input tokens | |
| Output tokens | |
| Cost | |
| stop_reason | |

Did the output-token count look higher than the visible text warranted? Why?

>

## Experiment 2 — Determinism

| Setting | Model | Distinct outputs / 20 |
|---|---|---|
| temperature=0 | claude-haiku-4-5 | |
| temperature=1 | claude-haiku-4-5 | |

What exactly did the Opus 5 request with `temperature` return? Paste the error.

>

**In one sentence: can you write `assert output == expected` against this system?**

>

## Experiment 3 — The cost of context

| Context size | Input tokens | Output tokens | Cost | Latency |
|---|---|---|---|---|
| ~200 tokens | | | | |
| ~20,000 tokens | | | | |

Marginal cost of 20k tokens of context: $______ and ______ seconds.

**A 10-turn agent loop carrying that context re-pays this how many times?**

>

## Experiment 4 — Structured output under failure

What came back when the requested fields weren't in the text?

>

What was `stop_reason`?

>

How would you handle this in a system that must not crash?

>

## stop_reason census

Values I actually saw, and what a production loop should do about each:

| stop_reason | What it means | What my loop should do |
|---|---|---|
| | | |

## The one thing that surprised me

>
