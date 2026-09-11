import json, time
from pathlib import Path

RUNS = Path(__file__).parent / "runs.jsonl"

def save_run(label, task, stats, trace, answer, ok):
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "loop": label,
        "ok": ok,
        "turns": stats["turns"],
        "in": stats["in"],
        "out": stats["out"],
        "usd": round(stats["spend"], 6),
        "secs": round(time.time() - stats["t0"], 1),
        "task": task,
        "answer": answer,
        "trace": trace,
    }
    
    with RUNS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record