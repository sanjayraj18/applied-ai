# Task 1 — The four-row table, from memory

**Time: 30 minutes. Close the chat window. Do not look at my earlier message.**

Fill this in yourself. The property column is given; you derive the other two.

| Property of the model | Direct consequence | The discipline it generates |
|---|---|---|
| **Stateless** — remembers nothing between calls | | |
| **Non-deterministic** — same input, different output | | |
| **Cannot act** — it can only emit text that *asks* for an action | | |
| **Cannot distinguish instruction from data** — it's all one string | | |

---

## Then derive these, in your own words (2–3 sentences each)

Do not look anything up. If you can't derive it, write "can't derive yet" — that's a
real answer and it tells us what Phase 1 needs to fix.

**Q1.** Why can't prompt injection be fixed by writing a better prompt?
(Which row does this come from?)

>

**Q2.** Why does a 10-step agent loop cost far more than 10 single calls?
(Which row?)

>

**Q3.** Why can't you test an LLM system with `assert output == expected`?
What would you assert on instead?

>

**Q4.** An agent "deleted a file." Which component actually deleted it — the model
or your code? Why does the answer matter for security?

>

---

## Self-check

Only after you've written all of the above, compare against the version in the chat.
Write below what you got wrong or missed. **This is the point of the exercise** — the
gaps are the curriculum.

>
