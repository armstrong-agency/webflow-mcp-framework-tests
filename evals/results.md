# E1 legibility evals: Client-First vs Mast vs Lumos (2026-11-02)

Model-only evals (no Webflow MCP, no site). 228 isolated `claude -p` calls: no tools, MCP, skills or settings, neutral system prompt, empty working directory. Zero failed calls. Scripts, fixtures, raw outputs and scores are in this folder (`scripts/`, `fixtures/`, `raw/`, `raw/score-output.md`).

First person in this file is the Claude agent that ran the evals, and "lead agent" is the Claude session that coordinated it. See the disclosures in the repo README.

## Pre-registered predictions

Hashed in `PREREGISTRATION.md` before the first call. "Advocate" and "Planning notes" are predictions from the advocate reports and an unpublished planning document. "Eval agent" is the agent's own prediction, labelled "Mine" in the pre-registration.

| Eval | Prediction | Source | Result |
| --- | --- | --- | --- |
| E1a zero-shot | Mast scores highest | Advocate | **Wrong.** Mast came last on both models |
| E1a zero-shot | CF highest, Mast lowest | Eval agent | Right on both models under the verified Lumos key (v2). CF's Sonnet lead over Lumos (1.37 vs 1.07) is not statistically significant |
| E1b comprehension | CF best on structure questions, Mast best on spacing | Planning notes | **Not testable.** All three hit the ceiling on both question types |
| E1b comprehension | Lumos best on the global-change question | Eval agent | Right (6/6 vs CF 4/6) |
| E1c drift | Mast drifts least | Planning notes | **Wrong.** Mast drifted the most |
| E1c drift | CF drifts more than Lumos | Eval agent | **Wrong.** CF drifted the least |

## Method

**E1a.** 10 layout intents × 3 frameworks × 2 models (`claude-haiku-5-5`, `claude-sonnet-5-5`) × 3 samples = 180 calls. The prompt names the framework and gives no docs. Scoring is deterministic against a key written beforehand (`scripts/e1a_key.py`, `scripts/vocab.py`): 2 means idiomatic, 1 means every class is valid in the framework but the answer isn't idiomatic, 0 means any class is invented or from another framework. Where a framework has no utility for an intent, its idiom is a well-formed custom class (CF flex/grid/margin-trim, Mast margin-trim). I made one post-hoc parsing fix: only the first line of each answer is scored, so a correct answer followed by an unrequested explanation isn't zeroed. That moved CF from 0.98 to 1.07.

**E1b.** One hand-written page per convention (hero with eyebrow, h1, paragraph, two buttons and an image, then a dark 3-card grid), with class names only and no CSS or framework names. 12 questions in four types: P spacing (4), S structure/identity (4), V variant/styling (3), G global change (1). 3 samples × 2 models × 3 fixtures = 18 calls. An answer is correct when it names the right element or class and none of the listed distractors.

**E1c.** For each framework, a grammar summary of 108 to 124 words, then a request for JSON naming classes for the roles in three new components (17 roles in total). 10 Sonnet samples per framework, 30 calls. "Drift" is the number of distinct class strings per role across the 10 samples, so 1.0 means every sample agreed.

## Results

### E1a: zero-shot generation (mean score 0–2; zero-scored answers in brackets)

| Model | CF | Mast | Lumos |
| --- | --- | --- | --- |
| Haiku | **0.77** (18/30 zero) | 0.00 (30/30) | 0.00 (30/30) |
| Sonnet | **1.37** (8/30) | 0.33 (24/30) | 1.07 (13/30) |
| Both | **1.07** | 0.17 | 0.53 |
| Both, custom-class idioms excluded | 1.47 | 0.19 | 0.53 |

**Key change (v1 → v2, after the runs).** The v1 key built Lumos's `u-` vocabulary from the naming doc and probe logs, plus some plausible but unverified families. The lead agent then checked the class list on the live Lumos v2 Starter through the Webflow MCP: `u-section`, `u-section-spacer`, `u-container-small|full` and `u-theme-dark|light|brand|inherit` exist; `u-section-large`, `u-container-large`, every `u-text-align-*` class and `is-secondary` do not, because Lumos buttons use component variants rather than combos. v2 limits Lumos `u-` classes to the verified and documented set (`scripts/vocab.py`, `scripts/e1a_key.py`; the pre-registered v1 files are in `preregistered/scripts/` and v1 scores are in `raw/scores-v1.json`). v1 → v2 for Lumos: Haiku 0.07 → 0.00, Sonnet 1.33 → 1.07, both models 0.70 → 0.53. CF and Mast are unchanged. 14 answers changed:
- Up: `u-section u-theme-dark` for the dark section (Sonnet, 3 answers, 0 → 2); `u-container u-section` for section padding (Sonnet, 2 answers, 0 → 1, valid but the idiom is a `*_wrap` custom class).
- Down: `u-text-align-center u-margin-bottom-small` (4 answers, 2 → 0); `u-container-large` (Sonnet, 3 answers, 2 → 0); `u-flex-horizontal u-align-items-center u-justify-content-between` (Sonnet, 2 answers, 2 → 0), because only `u-flex-horizontal-wrap|nowrap` is verified, not bare `u-flex-horizontal`. That last one is the closest call. Counting bare `u-flex-horizontal` as valid would raise Lumos Sonnet to 1.20.
- Same: `button is-secondary` scores 0 under both keys.

**Sonnet ranking, CF vs Lumos:** on the verified vocabulary CF leads, 1.37 vs 1.07. The key no longer flips the ranking: CF stays ahead even if bare `u-flex-horizontal` counts. With 30 answers each, though, the difference (+0.30) is not significant: the bootstrap 95% interval is −0.17 to +0.77, and in 12% of resamples Lumos ties or wins. The ranking is CF ahead of Lumos on Sonnet; the gap is still within sampling noise at this sample size. Mast is last under every key.

Per intent, CF wins section padding (2.00), the h2-styled h3 (2.00) and the secondary button. Lumos wins margin trim (Sonnet answered `u-margin-trim` 3/3), the card grid (`card_list u-grid-autofit`) and the dark section (`u-section u-theme-dark`). Under v2 it scores 0 on centered text and the large container, because Sonnet's answers there use classes that don't exist (`u-text-align-center`, `u-container-large`). CF scored 0.00 on the flex row: CF has no flex utility, and the models invented one instead of reaching for a custom class.

**The finding that matters most is that CF is the default prior.** When a model doesn't know a framework, it answers in Client-First/Relume vocabulary:

- Haiku's "Lumos" answers: `padding-global padding-section-large`, `heading-style-h2`, `container-large`. 14 of its 30 Lumos answers are valid CF and invalid Lumos.
- Sonnet's "Mast" answer for section padding was `padding-global padding-section-large` in 3 of 3 samples. In total, 9 Haiku and 5 Sonnet Mast answers were valid CF.
- Haiku refused Mast outright 5 times: "I don't know the No-Code Supply Mast naming convention".
- Mast-specific vocabulary appeared only for `u-text-center u-mb-sm` (Sonnet, 3 of 3) and once for `h2`. There was never a `row`, `col-*`, `cc-*` or `u-mode-dark`.
- Sonnet answered Mast's margin trim with Lumos's `u-margin-trim` (2 of 3), and its flex row with Tailwind's `flex-row items-center justify-between` (3 of 3).
- CF wasn't clean either. Haiku used `btn is-secondary` and `margin-bottom-small` (CF uses two classes there). For "large container" Sonnet answered `max-width-large` 3 of 3, and for margin trim it invented `spacing-clean` 3 of 3.

### E1b: same-DOM comprehension (% correct)

| Slice | CF | Mast | Lumos |
| --- | --- | --- | --- |
| All | 97% (70/72) | 99% (71/72) | 100% (72/72) |
| P spacing | 100% | 100% | 100% |
| S structure | 100% | 100% | 100% |
| V variant | 100% | 100% | 100% |
| G "make only card titles bigger" | 67% (4/6) | 83% (5/6) | **100%** (6/6) |

There is a ceiling effect. When the names are on the page, both models read all three conventions perfectly, so this fixture can't separate them. The only misses were on Q7. The CF and Mast fixtures have no class that belongs to the card title alone (`heading-style-h5`, `h5`), so the correct answer was "none". Sonnet answered `heading-style-h5` twice and `h5` once, and restyling those would change every h5-styled heading on the site. Lumos gives the title its own class (`features_card_title`), so the answer was obvious.

### E1c: naming drift (Sonnet, 10 samples, 17 roles)

| Metric | CF | Mast | Lumos |
| --- | --- | --- | --- |
| Distinct class strings per role (lower is better) | **1.41** | 2.29 | 2.29 |
| Distinct, ignoring `u-` utilities | **1.41** | 1.71 | 1.53 |
| Tokens that follow the grammar | 100% | 99.1% | 100% |
| Samples with a non-conforming class | 0 | 2* | 0 |
| Classes per element | 1.06 | 1.29 | 1.26 |

\*`card team-card` is a single-level custom class with no underscore. It's arguably legal Mast, so this is a judgment call.

The drift looks different in each framework:

- **CF:** the main split was whether to repeat the component name, as in `pricing_card-price` (8) vs `pricing_price` (2). The badge got three names: `pricing_popular-badge` 6, `pricing_card-badge` 2, `pricing_badge` 2.
- **Mast:** mostly varies its choices of base class and stacked utility: title `h3` 5 / `h4` 4; price `h2` / `h2 u-mb-md` / `h2 u-mb-sm`; FAQ answer `rich-text` 5 / `paragraph-sm` 5. The closed vocabulary doesn't make the choices deterministic. Models still pick which closed classes to stack.
- **Lumos:** `pricing_card is-featured` 7 vs `is-popular` 3; FAQ question `faq_question` 4 / `faq_item_question` 3 / plus `u-text-style-large` on some. The FAQ answer and toggle icon each got 3 to 4 variants.

## Limitations

- **Sample size.** 3 samples per cell in E1a (n=30 per framework and model), 6 per fixture question in E1b, and 10 in E1c. A difference of 0.1–0.2 on E1a is noise. One model family only (Claude), not three.
- **I wrote the keys, the fixtures and the summaries.** The keys were hashed before the runs. The Lumos `u-` vocabulary was revised after the runs (v2, described above) to match the class list verified on the live Starter. The revision cut both ways: 5 answers went up and 9 went down. The pre-registered v1 scores are kept. Bare `u-flex-horizontal` is still unverified and is the only Lumos call that changes Lumos's Sonnet score (1.07 vs 1.20); it doesn't change the ranking. The CF and Mast vocabularies were not verified on live starters the same way.
- **The custom-class idiom is lenient.** Any well-formed name scores 2. That helps CF more than the others (4 intents vs 1 for Mast), so the table also reports scores with those intents excluded.
- **E1b is hand-written and too easy.** The names are self-describing in every convention, so the result says more about the fixture than the frameworks. A harder version would leave out spacing and theming names, or test whether a model can predict CSS effects.
- **The E1c summaries contain worked examples** (`pricing_card is-featured` and similar in all three), which pushes the models toward the same answers and understates drift for every framework. The Mast summary describes base classes plus utilities, which invites more classes per element, so its higher per-role count is partly how the grammar is built rather than naming noise. The utility-free row (1.41 / 1.71 / 1.53) is the fairer comparison.
- **Lint detection was not run.** The planned violation-detection eval was out of scope for this run.
- **Intents and questions are mine.** A Mast or Lumos advocate might pick intents that favour their framework, such as column spans per breakpoint or theme switching.
