"""Bootstrap the E1a score gaps from raw/scores.json.

Added after the evals. The answer-level method treats all 30 answers as independent and reproduces
the interval first reported. The intent-level method resamples the 10 intents first, because the 3
samples of one intent are not independent. It is the fairer estimate, though 10 intents is few.
"""
import json
import pathlib
import random
from statistics import mean

RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"
ROWS = json.loads((RAW / "scores.json").read_text())["e1a"]
INTENTS = sorted({r["intent"] for r in ROWS})
N = 100_000


def scores(fw, model):
    return {i: [r["score"] for r in ROWS if r["fw"] == fw and r["intent"] == i and model in ("both", r["model"])]
            for i in INTENTS}


def answer_level(a, b, rng):
    xs, ys = sum(a.values(), []), sum(b.values(), [])
    return mean(rng.choices(xs, k=len(xs))) - mean(rng.choices(ys, k=len(ys)))


def intent_level(a, b, rng):
    return mean(mean(rng.choices(a[i], k=len(a[i]))) - mean(rng.choices(b[i], k=len(b[i])))
                for i in rng.choices(INTENTS, k=len(INTENTS)))


def report(label, method, a, b):
    rng = random.Random(0)
    gaps = sorted(method(a, b, rng) for _ in range(N))
    print(f"  {label}: 95% interval {gaps[N // 40]:+.2f} to {gaps[N - N // 40]:+.2f}, "
          f"second framework ties or wins in {sum(g <= 0 for g in gaps) / N:.1%} of resamples")


for model, first, second in [("sonnet", "cf", "lumos"), ("both", "cf", "lumos"), ("both", "cf", "mast")]:
    a, b = scores(first, model), scores(second, model)
    print(f"{first} minus {second}, {model}: gap {mean(sum(a.values(), [])) - mean(sum(b.values(), [])):+.2f}")
    report("answer level", answer_level, a, b)
    report("intent level", intent_level, a, b)
