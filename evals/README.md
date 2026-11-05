# Model evals

These evals measure what Claude Haiku and Claude Sonnet know about each framework with no docs, tools, or MCP. The results and limitations are in [results.md](results.md).

| Eval | Question | Calls |
| --- | --- | --- |
| E1a | Can a model write valid classes for a framework from its name alone? | 180 |
| E1b | Can a model read a page's classes and answer questions about them? | 18 |
| E1c | Given a short grammar summary, how much do class names vary across sessions? | 30 |

## Files

| Path | Contents |
| --- | --- |
| `PREREGISTRATION.md` | Predictions and file hashes, written before the first model call |
| `preregistered/scripts/` | The original `e1a_key.py` and `vocab.py`, matching their pre-registered hashes |
| `scripts/` | The scripts as used for the reported scores, including the revised keys |
| `fixtures/` | The three test pages and the three grammar summaries |
| `raw/` | Every model output, plus scores from both keys |

`PREREGISTRATION.md` is unedited, so "brief" in it refers to an unpublished planning document and "Mine" refers to the agent that ran the evals.

## What changed after pre-registration

- **The Lumos key.** After the runs, `e1a_key.py` and `vocab.py` were revised to match the class list on the live Lumos v2 Starter. This lowered Lumos's combined score from 0.70 to 0.53. A later review fixed two rules in that revision, for `u-alignment-center` and the secondary button, and no score changed. `results.md` lists what moved.
- **A parsing fix.** `score.py` was written after the hashes and later changed to score only the first line of each answer, so an unrequested explanation would not zero a correct answer. This moved Client-First from 0.98 to 1.07.
- **The bootstrap script.** `scripts/bootstrap.py` was added when this repo was assembled. It now prints two ranges for each gap. The first treats every answer as independent and matches the interval first reported. The second resamples the 10 tasks, and it is the one reported in `results.md`.
- **Extra tables.** `score.py` now also prints the same-task comparison and the drift row that ignores `u-` utilities. These use the same saved answers.

The vocabulary comments in `vocab.py` mention private reference notes and a local copy of the Lumos naming docs. Neither is published here. The files in `preregistered/scripts/` are kept as they ran, so their hashes still match.

## Check the results

These commands need only Python 3:

```bash
./verify-preregistration.sh
cd scripts
python3 score.py
python3 bootstrap.py
```

`verify-preregistration.sh` checks all 9 hashes. `score.py` prints the tables in `raw/score-output.md` and rewrites `raw/scores.json` with the same contents.

To score with the pre-registered key, run `python3 score.py --v1`. It prints the tables in `raw/score-output-v1.md` and rewrites `raw/scores-v1.json` with the same contents.

## Run the models again

`scripts/run.py` needs the [Claude Code CLI](https://claude.com/product/claude-code). Before running it:

1. Change `CWD` in `run.py` to an empty folder that exists on your machine.
2. Move or delete the outputs in `raw/e1a`, `raw/e1b`, and `raw/e1c`, because the script skips outputs that exist.
3. Check `MODELS`. Hosted models change, so a new run may not match these results.

```bash
cd scripts
python3 run.py e1a
python3 run.py e1b
python3 run.py e1c
python3 score.py
```
