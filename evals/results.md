# Model eval results (2026-11-02)

These evals asked what Claude models know about Client-First, Mast, and Lumos on their own, with no Webflow MCP and no site. There were 228 separate `claude -p` calls, each with no tools, MCP, skills, or settings, a neutral system prompt, and an empty working folder. No call failed. The scripts, fixtures, raw outputs, and scores are all in this folder.

First person in this file means the Claude agent that ran the evals, and "lead agent" means the Claude session that coordinated it. See the disclosures in the [repo README](../README.md).

## What was predicted, and what happened

The predictions are in `PREREGISTRATION.md`. "Advocate" and "planning notes" come from the advocate reports and an unpublished planning document. "Eval agent" is the agent's own prediction, labelled "Mine" in that file.

| Eval | Prediction | Source | Result |
| --- | --- | --- | --- |
| Writing from memory | Mast scores highest | Advocate | **Wrong.** Mast was last on Sonnet and tied for last with Lumos on Haiku |
| Writing from memory | Client-First highest, Mast lowest | Eval agent | Mostly right. Client-First led on both models, but its Sonnet lead over Lumos is not reliable, and Mast tied Lumos on Haiku |
| Reading a page | Client-First best on structure, Mast best on spacing | Planning notes | **Not testable.** All three scored 100% on both question types |
| Reading a page | Lumos best on the card title question | Eval agent | Right, but this says little. The same agent wrote the test pages and knew only the Lumos page had a card title class |
| Naming drift | Mast drifts least | Planning notes | **Wrong.** Mast tied Lumos for the most drift on all classes, and drifted most with `u-` utilities ignored |
| Naming drift | Client-First drifts more than Lumos | Eval agent | **Wrong.** Client-First drifted the least |

## How each eval worked

**Writing from memory (E1a).** There were 10 layout tasks, 3 frameworks, 2 models (`claude-haiku-5-5` and `claude-sonnet-5-5`), and 3 samples each, for 180 calls. The prompt named the framework and gave no docs. A script scored each answer against a key: 2 means the right approach, 1 means every class is real but the approach is not ideal, and 0 means at least one class is invented or from another framework. Where a framework has no utility for a task, the right approach is a well-formed custom class. That applies to 4 tasks on Client-First and 1 on Mast. I made one parsing fix after the runs, scoring only the first line of each answer, so a correct answer followed by an unrequested explanation was not zeroed. That moved Client-First from 0.98 to 1.07.

**Reading a page (E1b).** There was one hand-written page per framework: a hero, then a dark 3-card grid, with class names but no CSS or framework names. Models answered 12 questions in four groups: spacing (4), structure (4), styling variants (3), and one global change. With 3 samples, 2 models, and 3 pages, that made 18 calls. An answer was correct if it named the right element or class and none of the listed wrong ones.

**Naming drift (E1c).** Each framework got a summary of its naming rules, 108 to 124 words long, followed by a request to name the classes for 3 new components (17 elements in total). Sonnet did this 10 times per framework, for 30 calls. Drift is the number of different class strings per element across the 10 samples, so 1.0 means every sample agreed.

## Writing from memory

Mean score from 0 to 2, with the share of zero-scored answers in brackets.

| Model | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| Haiku | **0.77** (18 of 30) | 0.00 (30 of 30) | 0.00 (30 of 30) |
| Sonnet | **1.37** (8 of 30) | 0.33 (24 of 30) | 1.07 (13 of 30) |
| Both | **1.07** | 0.17 | 0.53 |

### How solid is the ranking?

Client-First's lead over Mast holds up under every check here. Its lead over Lumos does not, because there are only 10 tasks and the two frameworks are strong on different ones. Client-First wins section padding, centered text, the secondary button, the large container, and the h3 styled as an h2. Lumos wins margin trim, the card grid, and the dark section.

This table uses the same tasks for every framework.

| Tasks counted | Model | Client-First | Mast | Lumos |
| --- | --- | --- | --- | --- |
| All 10 | Sonnet | 1.37 | 0.33 | 1.07 |
| All 10 | Both | 1.07 | 0.17 | 0.53 |
| Without Client-First's 4 custom-class tasks | Sonnet | 1.72 | 0.44 | 0.78 |
| Without Client-First's 4 custom-class tasks | Both | 1.47 | 0.22 | 0.39 |
| Without the secondary button and centered text | Sonnet | 1.21 | 0.17 | 1.33 |
| Without the secondary button and centered text | Both | 1.00 | 0.08 | 0.67 |

The custom-class rule is lenient, because any well-formed name scores 2. It did not actually lift Client-First, though. Its score rises when those tasks are removed, because models mostly invented utilities there instead of writing a custom class. Client-First scored 0.00 on the flex row for this reason.

The secondary button and centered text are where Lumos did worst, because the models invented classes such as `u-text-align-center`. Dropping them removes real failures, so that row is not fairer. It shows how much two tasks can move the ranking.

`scripts/bootstrap.py` estimates how far each gap could move by chance. It resamples the 10 tasks, because the 3 answers to one task are not independent. A range that crosses zero means the data cannot say which framework is ahead.

| Gap | Size | Likely range (95%) |
| --- | --- | --- |
| Client-First minus Lumos, Sonnet | +0.30 | −0.47 to +1.07 |
| Client-First minus Lumos, both models | +0.53 | −0.08 to +1.12 |
| Client-First minus Mast, both models | +0.90 | +0.43 to +1.35 |

An earlier version of this file reported −0.17 to +0.77 for the Sonnet gap. That method treated all 30 answers as independent. The script still prints it for comparison. Ten tasks is a small number to resample, so treat these ranges as rough.

### How the Lumos key changed

The original key built Lumos's `u-` classes from the naming docs and test logs, plus some plausible but unverified families. After the runs, the lead agent checked the class list on the live Lumos v2 Starter through the MCP. `u-section`, `u-section-spacer`, `u-container-small`, `u-container-full`, and the `u-theme-*` classes exist. `u-section-large`, `u-container-large`, every `u-text-align-*` class, and `is-secondary` do not, because Lumos buttons use component variants rather than combo classes.

The revised key is limited to classes checked against the starter. It lowered Lumos on Haiku from 0.07 to 0.00, on Sonnet from 1.33 to 1.07, and on both models from 0.70 to 0.53. Client-First and Mast did not change. Of the 14 answers that changed, 5 went up and 9 went down:

- **Up:** `u-section u-theme-dark` for the dark section (Sonnet, 3 answers, 0 to 2), and `u-container u-section` for section padding (Sonnet, 2 answers, 0 to 1).
- **Down:** `u-text-align-center u-margin-bottom-small` (4 answers, 2 to 0), `u-container-large` (Sonnet, 3 answers, 2 to 0), and `u-flex-horizontal u-align-items-center u-justify-content-between` (Sonnet, 2 answers, 2 to 0).

The last of those is the closest call, because only `u-flex-horizontal-wrap` and `-nowrap` exist on the starter. Counting bare `u-flex-horizontal` would raise Lumos on Sonnet to 1.20. `button is-secondary` scored 0 under both keys.

A later review found two mistakes in the revised key. It said Lumos had no text alignment utility, but `u-alignment-center` exists. It also required `is-secondary` for the secondary button while rejecting that class, so that task could not score 2. Both rules are fixed, and no score changed, because no answer used those classes.

The original key and its scores are in `preregistered/scripts/` and `raw/scores-v1.json`.

### Client-First is the default guess

The finding that matters most is that when a model does not know a framework, it answers in Client-First and Relume vocabulary.

- Haiku's "Lumos" answers included `padding-global padding-section-large`, `heading-style-h2`, and `container-large`. 14 of its 30 Lumos answers were valid Client-First and invalid Lumos.
- Sonnet's "Mast" answer for section padding was `padding-global padding-section-large` in 3 of 3 samples. In total, 9 Haiku and 5 Sonnet Mast answers were Client-First classes.
- Haiku refused Mast outright 5 times, with answers such as "I don't know the No-Code Supply Mast naming convention".
- Real Mast vocabulary appeared only for `u-text-center u-mb-sm` (Sonnet, 3 of 3) and once for `h2`. There was never a `row`, `col-*`, `cc-*`, or `u-mode-dark`.
- Sonnet answered Mast's margin trim with Lumos's `u-margin-trim` (2 of 3), and its flex row with Tailwind's `flex-row items-center justify-between` (3 of 3).
- Client-First was not clean either. Haiku used `btn is-secondary` and `margin-bottom-small`. For "large container" Sonnet answered `max-width-large` 3 of 3, and for margin trim it invented `spacing-clean` 3 of 3.

## Reading a page

| Question group | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| All | 97% (70 of 72) | 99% (71 of 72) | 100% (72 of 72) |
| Spacing | 100% | 100% | 100% |
| Structure | 100% | 100% | 100% |
| Styling variants | 100% | 100% | 100% |
| "Make only the card titles bigger" | 67% (4 of 6) | 83% (5 of 6) | 100% (6 of 6) |

When the names are on the page, both models read all three conventions almost perfectly, so this test cannot separate them.

All the misses were on the card title question, and that question reflects how the pages were written. Only the Lumos page has a class for the card title (`features_card_title`). The Client-First and Mast pages use `heading-style-h5` and `h5`, so the correct answer there was "none", and Sonnet answered with the shared class 3 times. A real Client-First page would normally give the title its own class, so this is not evidence against Client-First.

## Naming drift

| Measure | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| Different class strings per element (lower is better) | **1.41** | 2.29 | 2.29 |
| Same, ignoring `u-` utilities | **1.41** | 1.71 | 1.53 |
| Classes that follow the naming rules | 100% | 99.1% | 100% |
| Samples with a class that breaks the rules | 0 | 2* | 0 |
| Classes per element | 1.06 | 1.29 | 1.26 |

\*`card team-card` is a single-level custom class with no underscore. It is arguably legal Mast, so this is a judgment call.

The drift looks different in each framework:

- **Client-First:** the main split was whether to repeat the component name, as in `pricing_card-price` (8) and `pricing_price` (2). The badge got three names: `pricing_popular-badge` 6, `pricing_card-badge` 2, and `pricing_badge` 2.
- **Mast:** mostly varied which classes it picked and stacked. The title was `h3` 5 times and `h4` 4 times, and the FAQ answer was `rich-text` 5 times and `paragraph-sm` 5 times. A closed list of classes does not make the choices identical, because models still pick which ones to stack.
- **Lumos:** the card was `pricing_card is-featured` 7 times and `is-popular` 3 times, and the FAQ question was `faq_question` 4 times and `faq_item_question` 3 times. The FAQ answer and toggle icon each got 3 to 4 versions.

## Limits

- **Small samples.** There are 3 samples per task in the memory test, 6 per question in the reading test, and 10 in the drift test. Only Claude models were used.
- **I wrote the keys, pages, and summaries.** The Lumos key was revised after the runs, as described above. Bare `u-flex-horizontal` is the one remaining judgment call that would change Lumos's score.
- **Client-First was scored on v2 naming.** Client-First v3 came out shortly before these runs, and its one-class spacing such as `margin-bottom-small` still scores 0 here.
- **The class checks have limits.** The Lumos key was checked through the MCP. Client-First and Mast were checked later against the published stylesheets of the test sites. Mast did not change, and Client-First moved from 1.07 to about 1.05.
- **The reading test is hand-written and too easy.** The names describe themselves in every convention, so the result says more about the pages than the frameworks.
- **The drift summaries contain worked examples**, such as `pricing_card is-featured`, which push models toward the same answers and understate drift for all three. The Mast summary describes base classes plus utilities, which invites more classes per element. That is why the row ignoring `u-` utilities is the fairer comparison.
- **The planned test of spotting naming violations was not run.**
- **The tasks and questions are mine.** A Mast or Lumos advocate might pick tasks that favor their framework, such as column spans per breakpoint or theme switching.
