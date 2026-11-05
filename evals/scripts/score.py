"""Score raw outputs for E1a/E1b/E1c and print markdown tables. Writes raw/scores.json."""
import json
import pathlib
import re
from collections import defaultdict
from statistics import mean

from e1a_key import CUSTOM_IDIOM, INTENTS, score as score_e1a
from e1b_key import KEY, QUESTIONS, correct
from vocab import tokens, valid

RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"
FWS = ["cf", "mast", "lumos"]


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else None


def first_answer(text):
    """Post-hoc parsing fix: score only the first line (or its first backticked span), so a correct
    answer followed by unrequested explanation is not zeroed by the prose tokens."""
    line = next((l for l in text.strip().splitlines() if l.strip()), "")
    m = re.search(r"`([^`]+)`", line)
    return m.group(1) if m else line


def e1a():
    rows = []
    for f in sorted((RAW / "e1a").glob("*.txt")):
        fw, iid, m, s = f.stem.split("__")
        ts = tokens(first_answer(f.read_text()))
        rows.append(dict(fw=fw, intent=iid, model=m, sample=int(s), answer=" ".join(ts), score=score_e1a(fw, iid, ts),
                         invalid=[t for t in ts if not valid(fw, t)]))
    print("## E1a mean score (0-2)\n\n| model | " + " | ".join(FWS) + " |\n|---|---|---|---|")
    for m in ("haiku", "sonnet", "all"):
        cells = []
        for fw in FWS:
            xs = [r["score"] for r in rows if r["fw"] == fw and (m == "all" or r["model"] == m)]
            cells.append(f"{mean(xs):.2f} (n={len(xs)}, 0s={xs.count(0)})" if xs else "-")
        print(f"| {m} | " + " | ".join(cells) + " |")
    print("\nExcluding custom-class idioms:")
    for fw in FWS:
        xs = [r["score"] for r in rows if r["fw"] == fw and (fw, r["intent"]) not in CUSTOM_IDIOM]
        print(f"  {fw}: {mean(xs):.2f} (n={len(xs)})")
    print("\n| intent | " + " | ".join(FWS) + " |\n|---|---|---|---|")
    for iid, _ in INTENTS:
        print(f"| {iid} | " + " | ".join(
            f"{mean([r['score'] for r in rows if r['fw'] == fw and r['intent'] == iid]):.2f}" for fw in FWS) + " |")
    return rows


def e1b():
    rows = []
    for f in sorted((RAW / "e1b").glob("*.txt")):
        fw, m, s = f.stem.split("__")
        ans = parse_json(f.read_text()) or {}
        for q, qtype, _ in QUESTIONS:
            a = ans.get(q, "")
            rows.append(dict(fw=fw, model=m, sample=int(s), q=q, qtype=qtype, answer=a, ok=correct(fw, q, a)))
    print("\n## E1b % correct\n\n| slice | " + " | ".join(FWS) + " |\n|---|---|---|---|")
    slices = [("all", lambda r: True), ("haiku", lambda r: r["model"] == "haiku"), ("sonnet", lambda r: r["model"] == "sonnet")]
    slices += [(f"type {t}", (lambda t: lambda r: r["qtype"] == t)(t)) for t in "PSVG"]
    for name, pred in slices:
        cells = []
        for fw in FWS:
            xs = [r["ok"] for r in rows if r["fw"] == fw and pred(r)]
            cells.append(f"{100 * mean(xs):.0f}% ({sum(xs)}/{len(xs)})" if xs else "-")
        print(f"| {name} | " + " | ".join(cells) + " |")
    print("\n| q | " + " | ".join(FWS) + " |\n|---|---|---|---|")
    for q, t, _ in QUESTIONS:
        print(f"| {q} ({t}) | " + " | ".join(
            f"{sum(r['ok'] for r in rows if r['fw'] == fw and r['q'] == q)}/6" for fw in FWS) + " |")
    return rows


def e1c():
    out = {}
    print("\n## E1c drift (sonnet, 10 samples each)\n\n| metric | " + " | ".join(FWS) + " |\n|---|---|---|---|")
    stats = {}
    for fw in FWS:
        per_role = defaultdict(list)
        all_tokens, bad_samples, parsed = [], 0, 0
        for f in sorted((RAW / "e1c").glob(f"{fw}__*.txt")):
            d = parse_json(f.read_text())
            if not d:
                continue
            parsed += 1
            sample_bad = False
            for comp, roles in d.items():
                for role, cls in roles.items():
                    ts = tokens(cls)
                    per_role[f"{comp}.{role}"].append(" ".join(sorted(ts)))
                    all_tokens += ts
                    sample_bad |= any(not valid(fw, t) for t in ts)
            bad_samples += sample_bad
        distinct = {r: len(set(v)) for r, v in per_role.items()}
        conform = mean(valid(fw, t) for t in all_tokens)
        stats[fw] = dict(parsed=parsed, mean_distinct=mean(distinct.values()), conform=conform,
                         bad_samples=bad_samples, tokens_per_el=len(all_tokens) / max(1, sum(map(len, per_role.values()))),
                         distinct=distinct, invalid=sorted({t for t in all_tokens if not valid(fw, t)}))
    for label, key, fmt in [("samples parsed", "parsed", "{}"), ("mean distinct class strings per role (of 10)", "mean_distinct", "{:.2f}"),
                            ("% tokens conforming", "conform", "{:.1%}"), ("samples with any non-conforming class", "bad_samples", "{}"),
                            ("mean classes per element", "tokens_per_el", "{:.2f}")]:
        print(f"| {label} | " + " | ".join(fmt.format(stats[fw][key]) for fw in FWS) + " |")
    for fw in FWS:
        print(f"\n{fw} per-role distinct: {stats[fw]['distinct']}\n{fw} invalid tokens: {stats[fw]['invalid']}")
    return stats


if __name__ == "__main__":
    res = dict(e1a=e1a(), e1b=e1b(), e1c=e1c())
    (RAW / "scores.json").write_text(json.dumps(res, indent=1, default=str))
