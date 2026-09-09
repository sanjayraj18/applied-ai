
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

REASONING_MODEL = "gpt-5.4"    
CHEAP_MODEL = "gpt-4.1-mini"  


PRICES = {
    REASONING_MODEL: (2.50, 0.25, 15.00),
    CHEAP_MODEL: (0.40, 0.10, 1.60),
}

STOP_REASONS = []


def cost(usage, model):
    """Dollar cost of one response. The brick you reuse in every phase."""
    price_in, price_cached, price_out = PRICES[model]

    details = getattr(usage, "prompt_tokens_details", None)
    cached = getattr(details, "cached_tokens", 0) or 0 if details else 0
    uncached = usage.prompt_tokens - cached

    return (
        uncached * price_in
        + cached * price_cached
        + usage.completion_tokens * price_out
    ) / 1_000_000


def reasoning_tokens(usage):
    """Billed as output, never shown to you."""
    details = getattr(usage, "completion_tokens_details", None)
    return getattr(details, "reasoning_tokens", 0) or 0 if details else 0


def experiment_1():
    print("=== Experiment 1 — one call, one cost ===")
    model = REASONING_MODEL

    response = client.chat.completions.create(
        model=model,
        max_completion_tokens=2048,
        messages=[{"role": "user", "content": "In two sentences, what is a token?"}],
    )

    choice = response.choices[0]
    usage = response.usage
    STOP_REASONS.append((model, choice.finish_reason))

    print(choice.message.content)
    print()
    print("response",response)
    print("prompt_tokens:    ", usage.prompt_tokens)
    print("completion_tokens:", usage.completion_tokens)
    print("  of which reasoning:", reasoning_tokens(usage))
    print("finish_reason:    ", choice.finish_reason)
    print(f"cost:              ${cost(usage, model):.6f}")


if __name__ == "__main__":
    experiment_1()