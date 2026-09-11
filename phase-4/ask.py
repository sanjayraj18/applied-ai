import json
from pathlib import Path

RUNS = Path(__file__).parent / "runs.jsonl"

def load():
    runs = []
    for line in RUNS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            runs.append(json.loads(line))
    return runs


if __name__ == "__main__":
    runs = load()

    print(f"{'when':<21}{'loop':<14}{'ok':<7}{'turns':>6}{'in':>7}{'usd':>11}{'secs':>7}")
    for r in runs:
        print(f"{r['ts']:<21}{r['loop']:<14}{str(r['ok']):<7}"
              f"{r['turns']:>6}{r['in']:>7}{r['usd']:>11.6f}{r['secs']:>7.1f}")

    total = sum(r["usd"] for r in runs)
    print(f"\n{len(runs)} runs, ${total:.6f} total")