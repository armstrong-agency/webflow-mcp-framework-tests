# Client-First v3 and the test results (2026-11-02)

Client-First v3 was released **October 23, 2026** (Finsweet changelog). Sources: the [changelog](https://finsweet.com/client-first/docs/changelog), [landing page](https://finsweet.com/client-first), [core structure](https://finsweet.com/client-first/docs/core-structure-strategy), [spacing](https://finsweet.com/client-first/docs/spacing-strategy), [classes strategy 2](https://finsweet.com/client-first/docs/classes-strategy-2), [variables](https://finsweet.com/client-first/docs/variables), [component naming](https://finsweet.com/client-first/docs/component-naming), [Client-First for AI](https://finsweet.com/client-first/docs/client-first-skill), all read in the browser, plus the published v3 cloneable's stylesheet (client-first-cloneable.webflow.io, published Oct 23 2026).

Note: the probe sandbox is a Relume (v2-era) style guide. Except where marked "tested", everything below is v3 as documented, not tested end to end.

## What changed in v3, mapped to what the tests found

| v3 change | What it fixes from our tests |
| --- | --- |
| **Default core structure:** section padding lives on `section_[id]` via variables (`.section_rename{padding: var(--_layout---section-padding--medium) var(--_layout---spacing--global-padding)}`); `padding-global padding-section-*` only as an optional layer | The combo-chain tax. The most common two-class stack in v2 is gone from the default structure; a section is one class. |
| **One-class spacing:** `padding-bottom-medium`, `margin-top-small`, `gap-[size]`, each a single variable-bound class | Spacing needs no direction + size class pair, so no combo chains to pre-create and no order sensitivity. |
| **Responsive spacing via variable modes per breakpoint** | Agents stop writing tablet/mobile spacing overrides element by element. Responsive values are set once, as plain values per mode, which the MCP can write. |
| **New grid utilities:** `grid-autofit-[size]` = `repeat(auto-fit, minmax(min(100%, var(--_sizes---grid-columns--size)), 1fr))`, plus `grid-autofill-*` | **The 200% text failure. Tested, below.** |
| **Buttons and text bound to Theme semantic variables** (`--_theme---button-primary--background`, `--_theme---text--primary`) | Prerequisite for one-switch dark sections like Lumos. The cloneable ships one mode; the docs say to add modes plus a `theme-dark` class. One-time setup, then per-section theming should match Lumos. Not tested. |
| **No formula variables or math-with-variables in the stylesheet** (0 `calc(var)` / `clamp(var)` in the published v3 CSS; all variables are plain values or references) | Zero exposure to both MCP bugs found: formula variables can't be written, and math with variables reads back wrong. An agent can edit every v3 token. |
| **Native Section element by default** | Semantic `<section>` without manual tag changes. |
| **Component naming convention** (`Group / Identifier`, e.g. `Card / Blog Post`) | Gives agents a naming rule for components, the one area CF previously left open. |
| **Classes strategy: custom class first, utility on top; max 4 stacked; no new styles on stacked utilities** | Formalizes the shallow-stack doctrine that kept CF cheap in our probes. |
| **`client-first.md` (beta): "every Client-First rule, written for AI agents working through the Webflow MCP"** | Finsweet now officially targets agents on the MCP. It covers naming, structure, variables, spacing, typography, folders, component naming, global styles, and accessibility, plus how the agent should work: what to check first, what to ask before changing, what to report. Finsweet calls it beta, "won't produce a launch-ready project on its own." Not yet downloaded or read (download needs approval). |

## Tested: v3 autofit grid fixes the 200% text failure

Same Client-First probe section. The card grid changed from the v2-style `1fr 1fr 1fr` + tablet override to v3's autofit pattern, with no breakpoint override (literal 20rem in place of v3's `--_sizes---grid-columns--small` = 20rem). Republished, measured in Chrome:

| | v2-style grid (round 4) | v3 autofit grid |
| --- | --- | --- |
| Columns, normal text, 1440 / 768 / 480 / 320 | 3 / 1 / 1 / 1 | 3 / 2 / 1 / 1 |
| Columns, 200% text | 3 / 1 / 1 / 1 | **1 / 1 / 1 / 1 (adapts)** |
| Visible overflow at 200% | 307px at 1440, 13px at 480, 165px at 320 | **none at any width** |
| Writes to build the grid | 2 (base + tablet override) | 1 |

So the round-4 Client-First failure was a v2-pattern failure. v3's built-in grid utility matches Lumos's breakpointless behavior with one class. The leftover invisible page-width overflow at 320px / 200% (100px) matches Mast and Lumos and has no visible element.

## What v3 doesn't change

- Conditionals are still read-opaque and write-destroyable through the MCP (a platform issue).
- Component slots still accept only component instances, but CF doesn't depend on them.
- New class stacks still need combo chains created first. v3 just makes them rarer.
- The agent still writes custom classes for layouts (Classes strategy 2: "we encourage custom class creation"). The 200% risk returns whenever an agent hand-writes a grid instead of using `grid-autofit-*`. That's an agent-rule issue: "use `grid-autofit-*` for card grids."
