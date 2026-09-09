# Phase 2 findings — the minimum harness

Date:
Model used:
Task I gave the agent:

## The run log

Paste your actual per-turn table.

| turn | in_tok | out_tok | cum_tok | cum_$ | finish_reason | action |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

Turn 1 input tokens: ______
Final turn input tokens: ______
Total input tokens for the run: ______
`n × turn-1 input tokens` would have been: ______

**Where did the extra tokens come from? Name the single largest contributor.**

>

## The six breakage runs

| # | Failure | What actually happened | Did the loop survive? | Fix: prompt or code? |
|---|---|---|---|---|
| 1 | Bad tool args | | | |
| 2 | Truncated JSON args | | | |
| 3 | Infinite loop | | | |
| 4 | Path traversal | | | |
| 5 | Prompt injection (tools present) | | | |
| 5b | Prompt injection (`write_file` removed) | | | |
| 6 | Cost curve | | | |

### Run 5 in detail

The injected text I put in `orders.csv`:

>

What the model did, verbatim:

>

What happened when I removed `write_file` from the `tools` list:

>

**One sentence: what is the difference between the two defences?**

>

## finish_reason census (Phase 2 edition)

| finish_reason | Times seen | What my loop did |
|---|---|---|
| | | |

Any value I did *not* see but must still handle:

>

## The four rows, as code

Point at a specific line number in `harness.py` for each.

| Row | Line in harness.py | What that line does about it |
|---|---|---|
| Stateless | | |
| Non-deterministic | | |
| Cannot act | | |
| Cannot distinguish instruction from data | | |

## The seven standing questions

1. Where does authority live? (line number)
2. What's the smallest amount of model I could have used?
3. How would I know this broke?
4. What does one unit of work cost?
5. What's the failure path — designed or accidental?
6. What here is untrusted?
7. Can my tests fail?

>

## The one thing that surprised me

>
