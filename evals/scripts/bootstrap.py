"""Bootstrap the Sonnet CF-minus-Lumos E1a gap from raw/scores.json.

Added after the evals, so the interval reported in results.md could be checked. The original
one-off calculation was not saved, so the last digit can differ from that report.
"""
import json
import pathlib
import random
from statistics import mean

RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"
rows = json.loads((RAW / "scores.json").read_text())["e1a"]
cf = [r["score"] for r in rows if r["fw"] == "cf" and r["model"] == "sonnet"]
lumos = [r["score"] for r in rows if r["fw"] == "lumos" and r["model"] == "sonnet"]

rng = random.Random(0)
gaps = sorted(mean(rng.choices(cf, k=len(cf))) - mean(rng.choices(lumos, k=len(lumos))) for _ in range(100_000))
print(f"gap {mean(cf) - mean(lumos):+.2f}, n={len(cf)}/{len(lumos)}")
print(f"95% interval {gaps[2_500]:+.2f} to {gaps[97_500]:+.2f}")
print(f"Lumos ties or wins in {sum(g <= 0 for g in gaps) / len(gaps):.1%} of resamples")
