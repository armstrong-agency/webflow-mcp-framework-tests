# Round 2 MCP tests (2026-11-02)

> **Correction (round 4, rendered):** the calc/var "corruption" below is a read-back bug only. Webflow stores and publishes the original `calc()` correctly (verified in published CSS and computed values). Read "replaced by the bare variable" as "*reported* as the bare variable". See `round-4-rendered.md`.

Webflow MCP beta v2.2.0, headless data tools, MCP read-back only (no publish). Sites: Lumos v2 Starter, Relume sandbox (Client-First), Mast Starter (read-only this round). All test elements and styles removed afterwards and verified.

## E4b — Theme change cost ("make this section dark")

Same section on each: heading, paragraph, primary button, secondary button.

| | Client-First (Relume) | Lumos |
| --- | --- | --- |
| Successful writes | **5**: 2 combo-chain creates, section stack (`section_probe background-color-black text-color-white`), `button is-alternate`, `button is-secondary is-alternate` | **1**: Section Theme prop → Dark |
| Failed calls | 1 ("styles not found" on the new section stack) | 0 |
| Scales with | Every button, border, card, or colored element in the section | Nothing; one write regardless of contents |

Why: Relume's `color-scheme-1` class only sets the wrapper's background and text, from fixed variables, and the Color Schemes collection has a single mode. Relume buttons bind to primitives (`neutral-shade-7`, `neutral-white`), so they do not follow a dark section; each needs its `is-alternate` combo. Lumos's Section Dark variant sets the Theme collection to Dark mode on `u-section` (read back), and `button_main_element` reads `theme/button-primary/*` variables, so children follow automatically.

**Result:** Lumos took fewer writes and no failures, and its cost does not grow with the section's contents.

## E2b — Component tax (one icon + text row in an existing section)

| | Client-First | Lumos |
| --- | --- | --- |
| Clean path (knowing slot names and layout semantics) | 3 writes + 1 read: 2 class creates, 1 nested build | 3 writes + 1 read: 1 nested slot build (Layout > Icon / Typography Plain), Layout variant → Auto Width, text prop |
| Observed path, first attempt | 4 calls, 0 failures | **9 calls**: slot-name miss ("Slot" prop vs "Column 1"/"Column 2"), orphan Layout left behind, find + delete orphan, wrong structure (both children in Column 1 stack vertically), delete + rebuild, then props |
| New naming decisions | 2 (`probe_feature-row`, `probe_feature-icon`) | 0 |
| Icon | Empty placeholder div | Real SVG via Icon component |

**Verdict:** the pre-registered threshold was "≥3× sustains the tax argument, ≤1.5× kills it". Clean path is **1.0×**, so the per-element component tax argument collapses. What remains is the **first-attempt discovery cost** (2.25× here) driven by slot-name mismatches and non-atomic failures. Rephrase in the argument: not "components cost more calls", but "components cost more calls the first time, and failures leave debris".

## Replications

| Finding | Original | Round 2 | Status |
| --- | --- | --- | --- |
| Failed component builds leave orphans | L-4 (x2), M-3 (x2) | Lumos Layout into slot | **5/5 failed builds left an orphan** |
| Builder slot names differ from slot prop names | Section, Button Wrapper, Grid Row | Layout ("Slot" prop → "Column 1", "Column 2") | Replicated |
| Combo chains are order-sensitive | Mast M-1b | **Client-First** section stack reordered → "styles not found" | Replicated, now on CF too |
| Silent calc corruption | L-9c (opacity) | Same expression on a fresh class | Replicated 2/2 |

## New: the calc/var corruption rule, characterized

Writes through `update_style`, read back immediately:

| Written value | Stored as |
| --- | --- |
| `calc(1 - 0.4 * var(--_trigger---on))` (opacity) | bare `var(--_trigger---on)` |
| `calc(100% - var(--_trigger---on) * 2rem)` (width) | bare `var(--_trigger---on)` |
| `calc(var(--_spacing---space--4) * 2)` (padding-top) | bare `space--4`, half the intended value |
| `clamp(1rem, var(--_spacing---space--4), 3rem)` (font-size) | bare `space--4` |
| `min(50vh, var(--_spacing---space--4))` (max-height) | bare `space--4` |
| `calc(1rem + 2vw)` (no variable) | kept verbatim |
| `scale(calc(1 + 0.2 * var(...)))` (var nested inside another function, transform) | kept |

**Rule:** any value whose top level is `calc()`, `clamp()`, or `min()` and that references a Webflow variable is replaced by the bare variable. Every write reports success. Untested: `max()`, and `var()` references to plain custom properties that are not Webflow variables (e.g. `var(--number)`).

This is an MCP style-tool bug, not a framework flaw. Exposure differs by framework. Counted on each starter's full style dump (`get_styles` all, with properties):

| Starter | Styles | Values using math functions | Top-level math with a variable (corrupted if an agent rewrites them) |
| --- | --- | --- | --- |
| Client-First (Relume) | 553 | 0 | **0** |
| Lumos | 666 | 38 | **3** (recounted in round 3; 2 on styleguide-only classes; the real one is `.button_main_line` transform-origin). 4 more reference only plain custom properties, which survive. |
| Mast | 436 | 12 | **7** (recounted in round 3; all core grid: `.row` / `.col` gutters and the `row-gap-md` / `row-gap-sm` variants). 5 more reference only plain custom properties, which survive. |

Round 3 confirmed plain custom properties (not Webflow variables) are not corrupted, and recounted against each site's real variable list.
