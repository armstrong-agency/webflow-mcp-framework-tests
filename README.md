# Webflow MCP framework tests

This repository contains tests comparing Client-First, Mast, and Lumos on two questions:

1. What can an AI agent actually do with each framework through the Webflow MCP?
2. What do AI models already know about each framework?

Results are reported as observed, including where each framework did well or badly. The raw model outputs and scoring scripts are included so the eval numbers can be checked.

All tests ran on 2026-11-02 against Webflow MCP beta v2.2.0. The MCP changes often, so treat every result as a snapshot of that version.

## Summary of findings

- **Model knowledge.** With no docs, Client-First scored highest on both models. Its lead over Mast is solid, and its lead over Lumos is within the margin of error. Models often used Client-First names when asked for Mast or Lumos.
- **Classes.** New class stacks failed on all three frameworks until the chain was created.
- **Components.** Failed component builds left orphans on Mast and Lumos, and the slot names the MCP shows differ from the names it accepts. Client-First was not tested with components.
- **Theming.** A dark section took 1 write on Lumos and 5 on Client-First. Mast was not measured.
- **Page builds.** Mast built the hero test in the fewest calls. Lumos lost its H1 after an agent text edit. Client-First's first grid overflowed at 200% text, and v3's `grid-autofit` removed the overflow.
- **Formula variables.** The MCP cannot write them. Client-First has none, Mast has 17 of 144, and Lumos has about 46 of 128.
- **Confidence.** Most results are single runs, so treat them as observations, not measurements. See [Limits](#limits).

## Disclosures

- **Author.** These tests were directed by Emmett Armstrong, a Client-First certified expert and a contributor to the Client-First docs. Emmett has also published a video arguing for Client-First.
- **Who ran the tests.** Claude Code agents ran the tests under Emmett's direction. Emmett checked the conditionals result in the Webflow Designer. First person in the result files ("I", "Mine") usually means the agent that ran that test.
- **Who wrote the scoring.** The same agents wrote the fixtures, scoring keys, and test tasks, and they knew Emmett expected Client-First to win. A Mast or Lumos expert might choose different tests.
- **Which models.** The model evals used Claude Haiku and Claude Sonnet only. They say nothing about other model families.

## Terms used here

| Term | Meaning |
| --- | --- |
| MCP | The tool connection an AI agent uses to read and change a Webflow site |
| Read-back | Asking the MCP what a value is after writing it |
| Class stack | Several classes on one element. Webflow stores each stack as an ordered chain, and the MCP makes you create that chain before you can apply it |
| Slot | A place inside a component where other content goes |
| Orphan | A leftover element that a failed build leaves on the page |
| Formula variable | A variable whose value is a CSS expression such as `clamp()`, not a plain number or color |
| Key | The rules that decide whether a model's answer is right |

## How the tests were set up

| Framework | Site used | Note |
| --- | --- | --- |
| Client-First | Blank Relume style guide | This is a v2-era Client-First site, not a v3 site |
| Mast | Clone of the Mast Starter (v2.4) | Built around components: Section, Grid Row, and Grid Column |
| Lumos | Clone of the Lumos v2 Starter | Built around components |

The agent used only the MCP's headless data tools, with no Designer open. Each test ran once and was read back through the MCP. Round 4 then published test pages to `webflow.io` and measured them in Chrome.

## MCP results

"Not measured" means the test was not run on that framework.

| What was tested | Client-First | Mast | Lumos | Source |
| --- | --- | --- | --- | --- |
| Make a section dark | 5 writes, 1 failed call | Not measured | 1 write | [Round 2](probes/round-2.md) |
| Add an icon and text row, knowing the slot names | 3 writes, 1 read | Not measured | 3 writes, 1 read | [Round 2](probes/round-2.md) |
| Same row, first attempt as it happened | 4 calls, 0 failures | Not measured | 9 calls, with a wrong slot name and a leftover element | [Round 2](probes/round-2.md) |
| Apply a new class stack | 3 calls for 2 classes | 6 calls for 4 classes | 3 attempts for 2 classes | [Mast and Client-First](probes/mast-and-client-first.md), [Lumos](probes/lumos.md) |
| Reorder an existing stack | Fails until the new chain is created | Fails until the new chain is created | Not measured | [Round 2](probes/round-2.md), [Mast](probes/mast-and-client-first.md) |
| Build a hero and 3 cards | 6 calls, 0 failures | 1 build and 2 prop calls, 0 failures | About 8 calls, 0 failures, then 2 fix rounds found after publishing | [Round 4](probes/round-4-rendered.md) |
| Content pushed off-screen at 200% text | 307px at 1440 with a v2-style grid, none with v3's `grid-autofit` | None | None | [Round 4](probes/round-4-rendered.md), [v3](probes/client-first-v3.md) |
| H1 survives an agent text edit | Yes | Yes | No, the heading published as `<p>` | [Round 4](probes/round-4-rendered.md) |
| Style values an agent would see wrongly if it rewrote them | 0 | 7, all core grid gutters | 3 | [Round 3](probes/round-3.md), [Round 4](probes/round-4-rendered.md) |
| Formula variables, which the MCP cannot write | 0 of 37 | 17 of 144 | About 46 of 128 | [Round 3](probes/round-3.md) |
| How to change the type and spacing scale | Edit each class, because these values are not variables on this site | Edit static min and max number variables | Not possible through variables, because the numbers sit inside formulas | [Round 3](probes/round-3.md) |

Some of these rows need context:

- **The icon row results are not the same output.** Both took the same number of calls, but Client-First produced an empty placeholder where Lumos produced a real SVG icon. Client-First also needed 2 new class names, and Lumos needed none.
- **The class stack row compares different stack sizes.** Mast's 6 calls were for 4 classes, and a stack of 2 utilities was not tested on Mast.
- **The read-back row counts exposure, not current errors.** Those values read back correctly as they stand. The MCP reports them wrongly only after an agent writes them again. The published page stays correct either way.
- **The formula variable row is partly a design difference.** Client-First's 37 variables cover colors, opacity, radius, stroke, and font families. Type and spacing are not variables on this site, so they cannot be formulas.
- **The type and spacing row comes from reading each starter.** No agent actually wrote a new scale on any framework.
- **Client-First's one-call section test had a head start.** It used class stacks that the Relume style guide already ships. Mast or Lumos could be prepared the same way, so that test is not like for like.

These behaviors belong to the MCP rather than to a framework, but they affect each framework differently depending on how much it relies on components:

- Slots accepted only component instances. A plain element was refused by both routes tried on Lumos.
- A slot nested inside another slot could not be reached through 3 routes on Lumos.
- All 5 failed component builds left an orphan behind, across Mast and Lumos.
- Slot names shown by the MCP differed from the names it accepts, on both Mast and Lumos.
- Class-string props accepted classes that do not exist, with no error, on both Mast and Lumos. Style tools cannot see those classes.
- A conditional authored in the Designer read back as an opaque marker, and a routine visibility write removed it with no warning. This was tested on a Lumos component. See [Conditionals](probes/conditionals.md).
- Writes of custom-property styles and formula variables were rejected.

### A correction inside the data

Rounds 2 and 3 reported a `calc()` bug as silent corruption. Round 4 showed that this was wrong. Webflow stores and publishes the original `calc()`, and it computed correctly in the browser. Only the MCP's read-back reports the wrong value. The earlier files keep their original text with a correction at the top.

## Model evals

These 228 calls ran in isolation, with no docs, tools, or MCP. The predictions, fixtures, and original keys were hashed before the evals ran. See [the full write-up](evals/results.md).

### Writing classes from memory

Each model was asked for the classes for 10 tasks, using only the framework's name. An answer scored 2 if it was the right approach, 1 if the classes were real but the approach was not ideal, and 0 if any class was invented. Higher is better.

| Model | Client-First | Mast | Lumos | Lumos on the pre-registered key |
| --- | --- | --- | --- | --- |
| Haiku | 0.77 | 0.00 | 0.00 | 0.07 |
| Sonnet | 1.37 | 0.33 | 1.07 | 1.33 |
| Both | 1.07 | 0.17 | 0.53 | 0.70 |

Models often wrote Client-First classes when asked for Lumos or Mast. Mast and Lumos tied at 0.00 on Haiku.

**Client-First's lead over Mast is solid. Its lead over Lumos is not.** With only 10 tasks, the result depends on which tasks you count, as these Sonnet scores show:

| Tasks counted | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| All 10 | 1.37 | 0.33 | 1.07 |
| Without the 4 tasks where Client-First's answer is a custom class | 1.72 | 0.44 | 0.78 |
| Without the secondary button and centered text tasks | 1.21 | 0.17 | 1.33 |

The last row puts Lumos ahead. Those two tasks are where Lumos did worst, because the models invented classes for them, so dropping them removes real failures. It still shows how much two tasks can move the ranking.

Resampling the tasks shows how much each gap could move by chance. A range that crosses zero means the data cannot say which framework is ahead.

| Gap | Likely range |
| --- | --- |
| Client-First minus Lumos, Sonnet | −0.47 to +1.07 |
| Client-First minus Lumos, both models | −0.08 to +1.12 |
| Client-First minus Mast, both models | +0.43 to +1.35 |

An earlier version of this repo reported −0.17 to +0.77 for the Sonnet gap. That method treated all 30 answers as independent, but 3 answers to the same task are not, so it made the result look more certain than it is.

The Lumos key was revised after the runs to match the class list on the live Lumos starter. Both versions of the key and both sets of scores are published. The answers for all three frameworks were later checked against the published stylesheets of the test sites. Mast did not change, and Client-First moved from 1.07 to about 1.05. That check covers the v2-era Client-First site only. The key scores Client-First on v2 naming, so a valid v3 class such as `margin-bottom-small` still scores 0.

### Naming drift

Sonnet named the classes for 3 new components 10 times per framework, given a short summary of the naming rules. This counts how many different class strings it used per element, so lower is more consistent.

| Measure | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| All classes | 1.41 | 2.29 | 2.29 |
| Ignoring `u-` utilities, the fairer comparison | 1.41 | 1.71 | 1.53 |

### Reading a page

Models read a page's classes and answered 12 questions about it. Client-First scored 97%, Mast 99%, and Lumos 100%, so the test was too easy to separate them.

The only misses came on "make only the card titles bigger", where Lumos got 6 of 6, Mast 5 of 6, and Client-First 4 of 6. This result reflects the test pages. Only the Lumos test page was written with a class for the card title, and a real Client-First page would normally have one too.

## Limits

- **One run per test.** The test plan called for 3 runs, but each test ran once. The orphan, slot-name, order-sensitivity, and `calc` read-back findings were repeated. The rest were not. See [the replication list](probes/README.md#what-was-repeated).
- **Client-First v3 was mostly not tested.** The test site is v2-era. Emmett's assessment is that the changes from v2 to v3 are mostly minor and that the core structure is the same. A stylesheet comparison is consistent with the core carrying over: 107 of the site's 169 non-custom classes appear on the v3 cloneable, including the structure, button, and heading classes. v3 replaces paired spacing classes such as `margin-bottom margin-small` with single classes, and adds `grid-autofit`. No full build was done on v3, so these results may or may not carry over. Only `grid-autofit` was tested live, with a literal `20rem` in place of v3's variable. Everything else in the [v3 notes](probes/client-first-v3.md) comes from Finsweet's documentation.
- **The 200% text test is a stand-in.** It sets the root font size inside an iframe rather than changing a real browser preference.
- **Raw MCP call logs are not published.** The probe files are written summaries of those calls. The model evals are the exception, because their raw outputs are all here.
- **Some comparisons cover only two frameworks.** The theme and icon-row tests did not run on Mast.
- **Nothing here is a full build.** No test had an agent build a complete site from one brief on each framework.
- **The scope is the MCP.** These tests cover agent work through the MCP, on two Claude models. They do not compare the frameworks for work outside it.
- **The model evals used no site.** They show what models know from memory, not how an agent behaves on a real Lumos or Mast site.
- **Component results are specific failures, not a failure rate.** Client-First was not tested with components, and the same MCP limits would apply to any components built on it.

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
cd evals/scripts && python3 score.py && python3 bootstrap.py
```

The first command checks the pre-registered hashes. The others rebuild the score tables and likely ranges from the raw model outputs, and they need only Python 3.

## Test pages

Round 4's published pages were live when this repo was written, but they sit on sandbox sites and may be reset or removed. The Client-First page now shows the v3 `grid-autofit` grid, so it no longer shows the 307px overflow from round 4.

- [Client-First](https://relume-test-2-c16648.webflow.io/mcp-probes)
- [Mast](https://mast-starter-5ed4eb.webflow.io/mcp-probes)
- [Lumos](https://lumos-v2-starter-636f55.webflow.io/mcp-probes)

## Framework links

- [Client-First](https://finsweet.com/client-first) by Finsweet
- [Mast](https://mast-framework.webflow.io) by No-Code Supply Co.
- Lumos by Timothy Ricks

If you run these tests and get different results, please open an issue.
