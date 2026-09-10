from openai import OpenAI
from error import LoopError
from toolschema import TOOL_SCHEMAS, dispatch
from dotenv import load_dotenv
from metrices import new_stats, record, row

load_dotenv()

client = OpenAI()

max_iterations=10
MAX_CHUNKS = 8000


SYSTEM = (
    "You are a file assistant working inside a sandbox directory. "
    "Use the tools to inspect files before you answer — do not guess at contents. "
    "When the task is complete, reply with a short plain-text answer."
    "If a file named in the task does not exist, say so and stop. "
    "Never substitute a different file for the one you were asked about."
)


def run(task : str , iteration = max_iterations, system : str = SYSTEM , trace: list | None = None, stats: dict | None = None):
    if trace is None:
        trace = []

    if stats is None:
        stats = new_stats()

    messages = [
        {"role" : "system", "content" : system},
        {"role" : "user", "content" : task}
    ]


    for turn in range (1, iteration+1):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                tools=TOOL_SCHEMAS,
                max_completion_tokens=MAX_CHUNKS,
            )

            choice = response.choices[0]
            msg = choice.message
            usage = response.usage

            record(stats, usage, "gpt-4.1-mini", len(msg.tool_calls or []))

            messages.append(msg.model_dump(exclude_none=True))
            calls = msg.tool_calls or []

            match choice.finish_reason:
                case "tool_calls":
                    for call in calls:
                        try:
                            result = dispatch(call)
                        except Exception as e:
                            result = f"ERROR: {type(e).__name__}: {e}"

                        trace.append({
                            "turn" : turn,
                            "tool" : call.function.name,
                            "args": call.function.arguments,
                            "result" : result[:200]
                        })
                        messages.append({
                            "role" : "tool",
                            "tool_call_id" : call.id,
                            "content" : result
                        })
                    continue

                case "stop":
                    return msg.content

                case "length":
                    raise LoopError(
                        f"turn {turn}: truncated at max_completion_tokens={MAX_OUT}. "
                        f"{len(calls)} tool call(s) in flight — arguments may be invalid JSON."
                    )

                case "content_filter":
                    raise LoopError(f"turn {turn}: content filtered. Escalate; do not retry the same input.")
                
                case other:
                    raise LoopError(f"turn {turn}: unhandled finish_reason {other!r}")

    raise LoopError(f"exhausted {iteration} turns without finishing")
   


if __name__ == "__main__":
    TASK = (
        "For each CSV file in the regions directory, total the amounts of rows "
        "with status 'paid'. Apply that region's commission rate from rates.json. "
        "Write report.md with one line per region and a grand total."
    )

    trace = []
    stats = new_stats()
    ok = True
    try:
        answer = run(task=TASK, trace=trace, stats=stats)
    except LoopError as e:
        answer, ok = f"ABORTED: {e}", False

    print(row("OTA", stats, ok))