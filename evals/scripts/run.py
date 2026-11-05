"""Run E1a/E1b/E1c samples through isolated `claude -p` calls. Resumable: skips outputs that exist.

Usage: python3 run.py e1a|e1b|e1c [--dry]
Each call runs from an empty cwd with no tools, MCP, skills, or setting sources, and a neutral
system prompt, so no framework docs or user context leak in.
"""
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from e1a_key import INTENTS
from e1b_key import QUESTIONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
FIX = ROOT / "fixtures"
CWD = pathlib.Path("/private/tmp/claude-501/evalcwd")
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
FW_NAME = {"cf": "Finsweet Client-First", "mast": "No-Code Supply Mast", "lumos": "Lumos (Timothy Ricks)"}
FIXTURE = {"cf": "a.html", "mast": "b.html", "lumos": "c.html"}


def call(model, prompt):
    cmd = ["claude", "-p", "--model", model, "--tools", "", "--strict-mcp-config",
           "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--system-prompt", "You are a helpful assistant.", prompt]
    r = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(r.stderr[-500:] or "empty output")
    return r.stdout


def jobs_e1a():
    for fw in FW_NAME:
        for iid, intent in INTENTS:
            for m in MODELS:
                for s in range(3):
                    p = (f"In a Webflow site that uses the {FW_NAME[fw]} class naming convention, write ONLY the "
                         f"space-separated class list you would put on the element for: {intent}. No explanation.")
                    yield RAW / "e1a" / f"{fw}__{iid}__{m}__{s}.txt", MODELS[m], p


def jobs_e1b():
    qs = "\n".join(f"{q}: {text}" for q, _, text in QUESTIONS)
    for fw in FW_NAME:
        html = (FIX / FIXTURE[fw]).read_text()
        for m in MODELS:
            for s in range(3):
                p = ("Here is the HTML of part of a Webflow page. You see only the class names, not the CSS.\n\n"
                     f"```html\n{html}```\n\nAnswer each question using the class names exactly as written. "
                     "Reply with ONLY a JSON object mapping question id to answer string, e.g. "
                     '{"Q1": "class-a class-b", ...}. No explanation.\n\n' + qs)
                yield RAW / "e1b" / f"{fw}__{m}__{s}.txt", MODELS[m], p


def jobs_e1c():
    for fw in FW_NAME:
        grammar = (FIX / f"grammar-{fw}.txt").read_text()
        for s in range(10):
            p = (f"A Webflow site follows this {grammar}\n"
                 "Name the classes for three new components, following the convention exactly. Reply with ONLY a "
                 "JSON object of this exact shape, each value being the space-separated class list for that element:\n"
                 '{"pricing": {"card": "", "popular_badge": "", "title": "", "price": "", "feature_list": "", '
                 '"feature_item": "", "button": ""}, '
                 '"team": {"card": "", "photo": "", "name": "", "role": "", "social_list": "", "social_link": ""}, '
                 '"faq": {"item": "", "question": "", "answer": "", "toggle_icon": ""}}\n'
                 "The pricing card shown is the highlighted \"popular\" plan. No explanation.")
            yield RAW / "e1c" / f"{fw}__sonnet__{s}.txt", MODELS["sonnet"], p


def run_one(job):
    out, model, prompt = job
    if out.exists():
        return "skip"
    for attempt in (1, 2):
        try:
            out.write_text(call(model, prompt))
            return "ok"
        except Exception as e:  # noqa: BLE001
            err = str(e)
    out.with_suffix(".failed").write_text(err)
    return "failed"


if __name__ == "__main__":
    which = sys.argv[1]
    jobs = list({"e1a": jobs_e1a, "e1b": jobs_e1b, "e1c": jobs_e1c}[which]())
    if "--dry" in sys.argv:
        print(len(jobs)); print(jobs[0][2]); sys.exit()
    CWD.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(run_one, jobs))
    print(which, {k: results.count(k) for k in set(results)})
