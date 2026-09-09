from openai import OpenAI, BadRequestError
from collections import Counter
from dotenv import load_dotenv

STOP_REASONS=[]

load_dotenv()
client = OpenAI()

REASONING_MODEL = "gpt-5.4"    
CHEAP_MODEL = "gpt-4.1-mini"  


PRICES = {
    REASONING_MODEL: (2.50, 0.25, 15.00),
    CHEAP_MODEL: (0.40, 0.10, 1.60),
}


def cost(usage, model):
    price_in, price_cached, price_out = PRICES[model]

    details = getattr(usage, "prompt_tokens_details", None)
    cached = getattr(details, "cached_tokens", 0) or 0 if details else 0
    uncached = usage.prompt_tokens - cached

    return (
        uncached * price_in
        + cached * price_cached
        + usage.completion_tokens * price_out
    ) / 1_000_000


def sample_many(model, prompt, temperature,n=20):
    outputs = []
    spend = 0.0
    for _ in range(n):
        response = client.chat.completions.create(
            model=model,
            max_completion_tokens=100,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        choice = response.choices[0]
        STOP_REASONS.append((model, choice.finish_reason))
        outputs.append(choice.message.content.strip())
        spend += cost(response.usage, model)
    return outputs, spend


def report(label, outputs, spend):
    counts = Counter(outputs)
    print(f"\n{label}: {len(counts)} distinct / {len(outputs)} calls  (${spend:.6f})")
    for text, n in counts.most_common():
        print(f"  {n:>2}x  {text[:90]}")

def experiment_2():
    print("\n=== Experiment 2 — how non-deterministic is it, really? ===")
    prompt = "Name a programming language and say one sentence about it."

    outputs, spend = sample_many(CHEAP_MODEL, prompt, temperature=0)
    report("temperature=0", outputs, spend)

    outputs, spend = sample_many(CHEAP_MODEL, prompt, temperature=1)
    report("temperature=1", outputs, spend)

    print(f"\n--- now send temperature to {REASONING_MODEL} ---")
    try:
        client.chat.completions.create(
            model=REASONING_MODEL,
            max_completion_tokens=100,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}],
        )
        print("no error — it accepted temperature")
    except BadRequestError as e:
        print(f"{type(e).__name__}  status={e.status_code}")
        print(e.message)



if __name__ == "__main__":
    experiment_2()