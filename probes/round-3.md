# Round 3 MCP tests (2026-11-02)

> **Correction (round 4, rendered):** the calc/var "corruption" below exists only in the MCP's read-back. Published CSS and computed values are correct, including the copied `.col` gutter (20px). The "double gutters" claim below is wrong. See `round-4-rendered.md`. The custom-variable-value write failures are unaffected; those writes really fail.

Webflow MCP beta v2.2.0, headless data tools, MCP read-back only. All probe styles and variables removed afterwards and verified.

## Calc/var corruption: remaining edges

Writes through `update_style` on a fresh class, read back immediately (adds to round 2's table):

| Written value | Stored as |
| --- | --- |
| `max(10rem, var(--_spacing---space--4))` | bare `space--4` (collapsed) |
| `calc(var(--_spacing---space--4) + var(--_spacing---space--2))` (two variables) | bare `space--4`; **the second variable is dropped entirely** |
| `calc(var(--number) * 1ch)` (plain custom property, not a Webflow variable) | kept verbatim |
| `calc(var(--_spacing---space--4, 1rem) * -1)` (Webflow variable **with a fallback**) | **kept verbatim** |

**Final rule:** a value whose top level is `calc`, `clamp`, `min`, or `max` and that references a Webflow variable without a fallback is replaced by the first referenced variable. The write reports success.
**Workaround:** add a fallback to every variable reference inside math, e.g. `var(--x, 1rem)`. Untested in rendered output.

## Exposure recount (against each site's real variable list)

| Starter | Style values at risk if an agent rewrites them |
| --- | --- |
| Client-First (Relume) | **0** |
| Lumos | **3**; 2 on styleguide-only classes, 1 real (`.button_main_line` transform-origin) |
| Mast | **7**, all core grid: `.row` and `.col` gutters, `row-gap-md` / `row-gap-sm` |

## New: custom variable values cannot be written at all

| Write | Result |
| --- | --- |
| Create Size variable, static `2rem` | OK |
| Create Size variable, custom `calc(var(--site--viewport-max) * 1rem)` | "An internal error occurred" |
| Update Size variable to custom `calc(2rem + 1vw)` (no variable) | internal error, value unchanged |
| Update Size variable to custom `calc(var(...) * 1rem)` | internal error, value unchanged |
| Create Color variable, custom `color-mix(in srgb, var(--swatch--brand-500), white 80%)` | internal error |
| Create Color variable, static `#c6fb50` | OK |
| Same custom-value create on the Relume site | internal error (MCP-wide, not site-specific) |

So an agent can read but never create or change any variable whose value is a formula. Reads work, so nothing is corrupted, but nothing can be edited either.

How much of each token system is formula-valued:

| Starter | Variables | Custom-valued | What an agent can still retune |
| --- | --- | --- | --- |
| Client-First (Relume) | 37 | **0** | Everything |
| Lumos | 128 | **~46**: all 10 font sizes, 8 space steps, 4 section spaces, site margin/gutter, color-mix brand shades | Colors (brand shades derive from static `brand-500`), radii, border widths. **Not** the type or spacing scale: the min/max numbers are baked inside each `clamp()` |
| Mast | 144 | **17**: fluid font sizes, section/card padding, container width, `light-dark()` colors | **Type and spacing scale too**: Mast keeps each fluid size's min and max in separate static Number variables (e.g. `h1/font-size-min-rem` = 2.8), so the formula never needs editing |

## When does the corruption actually bite?

- **Editing an unrelated property is safe.** Added `outline-offset` to Mast's `.col`; its existing `padding-left: calc(var(--_layout---grid--gap-main) / 2)` came back verbatim. (Reverted.)
- **Copying a value read from the site corrupts it.** Wrote `.col`'s exact padding string into a new class: stored as the bare `gap-main` variable, i.e. 40px instead of 20px. Double gutters, reported as success. This is the realistic agent move ("make a column like `.col` but…").

## Class-string props on Mast (replication of L-7)

Set a Mast Heading component's `Class` prop to `u-mb-sm u-text-centre totally-fake-class`. Accepted and read back verbatim, including the near-miss typo of the real utility `u-text-center`. Now replicated on both Lumos and Mast kits.
