# Task 2 — Read the tool-use docs, actively

**Time: ~2 hours.** Reading without questions is passive and evaporates. Answer these
*while* reading, in your own words. Copy-pasting from the docs defeats the purpose.

## Read, in this order

1. Tool use overview — https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
2. Implement tool use — https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
3. Skim: Models overview — https://platform.claude.com/docs/en/about-claude/models/overview
4. Skim: Pricing — https://platform.claude.com/docs/en/pricing

## Questions you must be able to answer

**Q1.** What exactly is in the API response when Claude "uses a tool"?
Name the block type and its fields.

>

**Q2.** Who executes the tool? Trace the sequence: request → response → ??? → next request.

>

**Q3.** What is `tool_use_id` and what breaks if you get it wrong?

>

**Q4.** What is `stop_reason`, and which values must your loop handle?
List them and say what you'd do for each.

>

**Q5.** Claude asks for three tools in one response. What must you send back,
and in how many messages? What goes wrong if you split them?

>

**Q6.** A tool throws an exception. What do you send back to Claude?
(There is a specific field for this.)

>

**Q7.** In `input_schema`, what is `required` for, and why does a good
`description` on each property matter so much?

>

**Q8.** Where does the conversation history live between turns — on Anthropic's
server, or in your process? What does that imply about cost as the loop runs?

>

---

## Facts to write down (you'll need these in Phase 1)

- Model ID you'll use:
- Its input price per 1M tokens:
- Its output price per 1M tokens:
- Where token counts appear in the response object:
