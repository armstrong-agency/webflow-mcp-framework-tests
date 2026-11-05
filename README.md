# Webflow MCP framework tests

These are the tests behind my video [Why Client-First Is the Best Framework for Webflow MCP](ADD-VIDEO-LINK). They compare Client-First, Mast, and Lumos on two questions: what an AI agent can do with each framework through the Webflow MCP, and what AI models already know about each one.

The video argues a position. This repo does not. It reports what happened, including the results that favor Mast and Lumos, so you can check the data and reach your own conclusion.

All tests ran on 2026-11-02 against Webflow MCP beta v2.2.0. The MCP changes often, so treat every result as a snapshot of that version.

## Disclosures

- **My position.** I have used Client-First for years, I contributed to the Client-First V3 docs with the Finsweet team, and my video argues for Client-First.
- **Who ran the tests.** Claude Code agents ran the tests under my direction. I checked the conditionals result in the Webflow Designer. First person in the result files ("I", "Mine") usually means the agent that ran that test.
- **Who wrote the scoring.** The same agents wrote the fixtures, scoring keys, and test intents, and they knew I expected Client-First to win. A Mast or Lumos expert might choose different tests.
- **Which models.** The model evals used Claude Haiku and Claude Sonnet only. They say nothing about other model families.

## How the tests were set up

| Framework | Site used | Note |
| --- | --- | --- |
| Client-First | Blank Relume style guide | This is a v2-era Client-First site, not a v3 site |
| Mast | Clone of the Mast Starter (v2.4) | Component-first, with Section, Grid Row, and Grid Column components |
| Lumos | Clone of the Lumos v2 Starter | Component-first |

The agent used only the MCP's headless data tools, with no Designer open. Each mechanic was run once and read back through the MCP. Round 4 then published test pages to `webflow.io` and measured them in Chrome.

## MCP results

"Not measured" means the test was not run on that framework.

| Measure | Client-First | Mast | Lumos | Source |
| --- | --- | --- | --- | --- |
| Make a section dark | 5 writes, 1 failed call | Not measured | 1 write | [Round 2](probes/round-2.md) |
| Add an icon and text row, knowing the slot names | 3 writes, 1 read | Not measured | 3 writes, 1 read | [Round 2](probes/round-2.md) |
| Same row, first attempt as observed | 4 calls, 0 failures | Not measured | 9 calls, with a slot-name miss and a leftover element | [Round 2](probes/round-2.md) |
| Apply a new class stack | 3 calls (2 utilities) | 6 calls (4 classes) | 3 attempts (2 classes) | [Mast and Client-First](probes/mast-and-client-first.md), [Lumos](probes/lumos.md) |
| Reorder an existing stack | Fails until the new chain is created | Fails until the new chain is created | Not measured | [Round 2](probes/round-2.md) |
| Build a hero and 3 cards | 6 calls, 0 failures | 1 build and 2 prop calls, 0 failures | About 8 calls, 0 failures, then 2 fix rounds found after publishing | [Round 4](probes/round-4-rendered.md) |
| Visible overflow at 200% text | 307px at 1440 with a v2-style grid, none with v3's `grid-autofit` | None | None | [Round 4](probes/round-4-rendered.md), [v3](probes/client-first-v3.md) |
| H1 survives an agent text edit | Yes | Yes | No, the heading published as `<p>` | [Round 4](probes/round-4-rendered.md) |
| Style values the MCP misreports on read-back | 0 | 7, all core grid gutters | 3 | [Round 3](probes/round-3.md), [Round 4](probes/round-4-rendered.md) |
| Formula variables, which the MCP cannot write | 0 of 37 | 17 of 144 | About 46 of 128 | [Round 3](probes/round-3.md) |
| Type and spacing scale retunable through the MCP | Yes | Yes, through static min and max number variables | No | [Round 3](probes/round-3.md) |

Client-First's one-call section probe depended on combos that the Relume style guide already ships. Mast or Lumos could be warmed up in the same way, so that probe is not a like-for-like comparison.

These behaviors belong to the MCP rather than to a framework, but they affect frameworks differently depending on how much each one relies on components:

- Slots accepted only component instances, and a plain element was refused by both routes tried on Lumos.
- A slot nested inside a slot could not be reached through 3 routes on Lumos.
- All 5 failed component builds left an orphan behind, across Mast and Lumos.
- Slot names shown by the MCP differed from the names it accepts, on both Mast and Lumos.
- Class-string props accepted nonexistent classes without an error, on both Mast and Lumos. Style tools cannot see those classes.
- A conditional authored in the Designer read back as an opaque marker, and a routine visibility write removed it with no warning. This was tested on a Lumos component. See [Conditionals](probes/conditionals.md).
- Custom-property style writes and formula variable writes were rejected.

### A correction inside the data

Rounds 2 and 3 reported a `calc()` bug as silent corruption. Round 4 showed that this was wrong. Webflow stores and publishes the original `calc()`, and it computed correctly in the browser. Only the MCP's read-back reports the wrong value. The earlier files keep their original text with a correction at the top.

## Model evals

These 228 calls ran in isolation, with no docs, tools, or MCP. The predictions, fixtures, and original keys were hashed before the first call. See [the full write-up](evals/results.md).

**Zero-shot class writing** (mean score from 0 to 2, higher is better):

| Model | Client-First | Mast | Lumos | Lumos on the pre-registered key |
| --- | --- | --- | --- | --- |
| Haiku | 0.77 | 0.00 | 0.00 | 0.07 |
| Sonnet | 1.37 | 0.33 | 1.07 | 1.33 |
| Both | 1.07 | 0.17 | 0.53 | 0.70 |

The Sonnet gap between Client-First and Lumos is not statistically significant, with a 95% interval of −0.17 to +0.77. Models often wrote Client-First classes when asked for Lumos or Mast.

The Lumos key was revised after the runs to match the class list on the live Lumos starter. The Client-First and Mast vocabularies were not checked against live starters in the same way. Both versions of the key and both sets of scores are published. The custom-class scoring rule also helps Client-First more than the others. With those intents excluded, the scores are 1.47, 0.19, and 0.53.

**Naming drift** (distinct class strings per role over 10 Sonnet samples, lower is better):

| Metric | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| All classes | 1.41 | 2.29 | 2.29 |
| Ignoring `u-` utilities, the fairer comparison | 1.41 | 1.71 | 1.53 |

**Same-page comprehension** (percent correct): Client-First scored 97%, Mast 99%, and Lumos 100%. The fixture was too easy to separate them. The one discriminating question was "make only the card titles bigger", where Lumos got 6 of 6, Mast 5 of 6, and Client-First 4 of 6.

## Limits

- **One run per probe.** The probe plan called for 3 runs, but each probe ran once. The orphan, slot-name, order-sensitivity, and `calc` read-back findings were repeated. The rest were not. See [the replication list](probes/README.md#what-was-repeated).
- **Client-First v3 was mostly not tested.** The sandbox is v2-era. Only the `grid-autofit` pattern was tested live, with a literal `20rem` in place of v3's variable. Everything else in the [v3 notes](probes/client-first-v3.md) comes from Finsweet's documentation.
- **The 200% text test is a stand-in.** It sets the root font size inside an iframe rather than changing a real browser preference.
- **Raw MCP call logs are not published.** The probe files are written summaries of those calls. The model evals are the exception, because their raw outputs are all here.
- **Some comparisons cover only two frameworks.** The theme and icon-row tests did not run on Mast.

## What could change these results

Re-test if Webflow ships any of these in the MCP: plain-element slot insertion or atomic component builds, a read and write API for conditionals, or verbatim round-trips for `calc()` and custom properties. The same applies to any full Client-First v3 test on a v3 site.

## What's in this repo

| Path | Contents |
| --- | --- |
| [`probes/`](probes/README.md) | The MCP tests: the plan, then a result file for each round |
| [`evals/`](evals/README.md) | The model evals: pre-registration, fixtures, scripts, raw outputs, and scores |
| [`advocate-reports/`](advocate-reports/README.md) | Three adversarial reports, each making the best case for one framework |

To check the eval numbers yourself:

```bash
./evals/verify-preregistration.sh
cd evals/scripts && python3 score.py
```

The first command checks the pre-registered hashes. The second rebuilds the score tables from the raw model outputs, and needs only Python 3.

## Test pages

Round 4's published pages were live when this repo was written, but they sit on sandbox sites and may be reset or removed:

- [Client-First](https://relume-test-2-c16648.webflow.io/mcp-probes)
- [Mast](https://mast-starter-5ed4eb.webflow.io/mcp-probes)
- [Lumos](https://lumos-v2-starter-636f55.webflow.io/mcp-probes)

## Framework links

- [Client-First](https://finsweet.com/client-first) by Finsweet
- [Mast](https://mast-framework.webflow.io) by No-Code Supply Co.
- Lumos by Timothy Ricks

If you run these tests and get different results, please open an issue.
