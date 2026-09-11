import json
from openai import OpenAI
from dotenv import load_dotenv

from error import LoopError
from toolschema import call_tool
from metrices import new_stats, record, row, check_caps

load_dotenv()
client = OpenAI()

MODEL = "gpt-4.1-mini"
MAX_OUT = 1000


PLAN_SYSTEM = (
    "You are a planner. Given a task and a directory listing, produce the list of "
    "sum_column operations needed. Produce exactly one step per region CSV. "
    "You are NOT executing anything — only planning."
)


WRITE_SYSTEM = (
    "You write final reports from tool results. Use only the numbers given to you. "
    "Return ONLY the markdown content, with no commentary and no code fences."
)


PLAN_SCHEMA = {
    "name": "plan",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string"},
                        "path": {"type": "string"},
                        "filter_column": {"type": "string"},
                        "filter_value": {"type": "string"},
                        "amount_column": {"type": "string"},
                    },
                    "required": ["region", "path", "filter_column",
                                 "filter_value", "amount_column"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["steps"],
        "additionalProperties": False,
    },
}


def make_plan(task, listing, rates, stats, trace):
    messages = [
        {"role": "system", "content": PLAN_SYSTEM},
        {"role": "user", "content":
            f"TASK:\n{task}\n\nFiles in regions/:\n{listing}\n\nrates.json:\n{rates}"},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_completion_tokens=MAX_OUT,
        response_format={"type": "json_schema", "json_schema": PLAN_SCHEMA},
    )
    choice = response.choices[0]
    record(stats, response.usage, MODEL, 0)

    if choice.finish_reason != "stop":
        raise LoopError(f"plan call ended with finish_reason={choice.finish_reason}")

    steps = json.loads(choice.message.content)["steps"]
    trace.append({"turn": 1, "tool": "(plan)", "args": "",
                  "result": json.dumps(steps)[:300]})
    return steps



def execute(steps, trace):
    results = []
    for step in steps:
        args = {k: step[k] for k in
                ("path", "filter_column", "filter_value", "amount_column")}
        result = call_tool("sum_column", args)
        trace.append({"turn": 0, "tool": "sum_column",
                      "args": json.dumps(args), "result": result[:200]})
        results.append((step["region"], result))
    return results



def synthesise(task, results, rates, stats, trace):
    lines = "\n".join(f"{region}: {res}" for region, res in results)
    messages = [
        {"role": "system", "content": WRITE_SYSTEM},
        {"role": "user", "content":
            f"TASK:\n{task}\n\nrates.json:\n{rates}\n\nTool results:\n{lines}"},
    ]
    response = client.chat.completions.create(
        model=MODEL, messages=messages, max_completion_tokens=MAX_OUT,
    )
    choice = response.choices[0]
    record(stats, response.usage, MODEL, 0)

    if choice.finish_reason != "stop":
        raise LoopError(f"synthesis ended with finish_reason={choice.finish_reason}")

    content = choice.message.content
    result = call_tool("write_file", {"path": "report.md", "content": content})
    trace.append({"turn": 0, "tool": "write_file",
                  "args": '{"path": "report.md"}', "result": result[:200]})
    return content


def run(task: str, trace: list | None = None, stats: dict | None = None) -> str:
    if trace is None:
        trace = []
    if stats is None:
        stats = new_stats()

    listing = call_tool("list_files", {"directory": "regions"})
    rates = call_tool("read_file", {"path": "rates.json"})

    check_caps(stats)
    steps = make_plan(task, listing, rates, stats, trace)

    results = execute(steps, trace)

    check_caps(stats)
    return synthesise(task, results, rates, stats, trace)


if __name__ == "__main__":
    TASK = (
        "For each CSV file in the regions directory, total the 'amount' column for "
        "rows whose status is exactly 'paid'. Multiply each region's paid total by "
        "that region's rate from rates.json to get its commission. Write report.md "
        "with one line per region and a final grand total. Round all money to 2 decimals."
    )

    trace, stats, ok = [], new_stats(), True
    try:
        answer = run(TASK, trace=trace, stats=stats)
    except LoopError as e:
        answer, ok = f"ABORTED: {e}", False

    for s in trace:
        print(f"[t{s['turn']}] {s['tool']}({s['args'][:60]}) -> {s['result'][:80]}")
    print(row("Plan-Execute", stats, ok))

