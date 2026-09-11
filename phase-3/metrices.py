import time
from error import CapExceeded

PRICES = {"gpt-4.1-mini": (0.40, 0.10, 1.60)}   


CAPS = {"turns": 10, "tokens": 40_000, "seconds": 120, "usd": 0.05}


def cost(usage, model):
    price_in, price_cached, price_out = PRICES[model]
    details = getattr(usage, "prompt_tokens_details", None)
    cached = (getattr(details, "cached_tokens", 0) or 0) if details else 0
    uncached = usage.prompt_tokens - cached
    return (
        uncached * price_in
        + cached * price_cached
        + usage.completion_tokens * price_out
    ) / 1_000_000

def new_stats():
    return {"turns": 0, "calls": 0, "in": 0, "out": 0,
            "spend": 0.0, "first_in": 0, "t0": time.time()}


def record(s, usage, model, n_calls=0):
    """Call once per API response, whatever the loop shape."""
    s["turns"] += 1
    s["calls"] += n_calls
    s["in"] += usage.prompt_tokens
    s["out"] += usage.completion_tokens
    s["spend"] += cost(usage, model)
    s["first_in"] = s["first_in"] or usage.prompt_tokens


def row(label, s, ok):
    naive = s["turns"] * s["first_in"]
    return {
        "loop": label,
        "turns": s["turns"],
        "calls": s["calls"],
        "in": s["in"],
        "out": s["out"],
        "ratio": round(s["in"] / naive, 2) if naive else 0,
        "usd": round(s["spend"], 6),
        "secs": round(time.time() - s["t0"], 1),
        "ok": ok,
    }

def check_caps(s, caps=CAPS):
    if s["turns"] >= caps["turns"]:
        raise CapExceeded(f"turn cap: {s['turns']} >= {caps['turns']}")
    if s["in"] + s["out"] >= caps["tokens"]:
        raise CapExceeded(f"token cap: {s['in'] + s['out']} >= {caps['tokens']}")
    
    elapsed = time.time() - s["t0"]
    
    if elapsed >= caps["seconds"]:
        raise CapExceeded(f"wall-clock cap: {elapsed:.1f}s >= {caps['seconds']}s")
    if s["spend"] >= caps["usd"]:
        raise CapExceeded(f"dollar cap: ${s['spend']:.6f} >= ${caps['usd']:.2f}")
