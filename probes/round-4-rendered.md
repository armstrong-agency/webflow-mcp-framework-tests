# Round 4: rendered verification on webflow.io (2026-11-02)

All three starters published to their webflow.io subdomains only (no custom domains), with Emmett's approval. Probe pages:
- https://relume-test-2-c16648.webflow.io/mcp-probes (Client-First)
- https://mast-starter-5ed4eb.webflow.io/mcp-probes (Mast)
- https://lumos-v2-starter-636f55.webflow.io/mcp-probes (Lumos)

Measured in Chrome on the published pages, via same-origin iframes at fixed widths. "200%" = root font-size set to 200% inside the iframe, a stand-in for a user's browser text-size preference: pixel media queries do not react, rem-based sizing does. One run per condition.

## Correction: the calc/var "corruption" is a read-back bug, not data loss

| Class (written via MCP) | MCP read-back | Published CSS | Computed in browser |
| --- | --- | --- | --- |
| `.probe_calc-render` opacity `calc(1 - 0.4 * var(--_trigger---on))` | bare variable | `calc(1 - .4 * var(--_trigger---on))` | **0.6** (correct) |
| `.probe_calc-fallback` same with `, 1` fallback | verbatim | verbatim | **0.6** (correct) |
| `.probe_col-copy` = `.col`'s `calc(var(--_layout---grid--gap-main) / 2)` | bare variable | `calc(var(--_layout---grid--gap-main) / 2)` | **20px**, identical to `.col` |

Webflow stores and publishes the math correctly. The MCP's style read-back reports any top-level `calc`/`clamp`/`min`/`max` that contains a Webflow variable as just the variable. Consequences:
- **No rendered damage.** Rounds 2 and 3 claimed "doubled gutters", "opacity 0", and "half the padding". All of those claims are **wrong**.
- **Agents still misread their own work.** A write-then-verify loop sees the wrong value and may "fix" a correct style. That is a smaller, real issue. The exposure counts (CF 0, Lumos 3, Mast 7) now measure exposure to misreads, not breakage.
- The fallback form `var(--x, 1rem)` both reads back and renders correctly, so it stays a good agent rule.

## Theme cascade (Lumos), rendered

Dark section: background rgb(31,29,30), text white. Secondary button text turned white automatically. Primary button keeps its brand background (lime) with dark text, correct in both themes. **Confirmed on the live page.**

## Hidden-prop element

A paragraph hidden with its Visibility prop (`false`), carrying a unique marker string, is **absent from the published HTML**, not just hidden with CSS. Confirmed.

## NEW: setting Lumos heading text through the MCP removes the heading tag

- Lumos Typography Heading stores its text as a rich-text prop. Setting that prop with the MCP (`rich_text_inner_text`) published as `<div class="u-heading …"><p>Build structured…</p></div>`, so **the page has no H1**.
- Control: an untouched Typography Heading on the same page published as `<div class="u-heading"><h2>…</h2></div>`.
- So the MCP's rich-text setter, which the schema says does not parse headings, converts a heading component into a paragraph and reports success. Visual size is unchanged (the variant class still applies), so it cannot be spotted without reading the HTML.
- Applies to any rich-text prop used for headings. Mast's Heading (textContent + Tag prop) and Client-First (native heading element) both rendered a real `<h1>`.

## NEW: a blank MCP-created page lacks Lumos's required scaffolding

The Lumos Autofit grid rendered as a single 1440px column until I added Lumos's **Global Styles** and **Starter CSS** components to the page. Those components carry the CSS that turns data attributes (`data-number`, `data-large-columns`) into the variables the grid uses. A page created through the MCP starts empty, so an agent must know to add Lumos's page structure. I also first misread "Minimum Column Size" (it is rem, default 12), because nothing in the MCP explains a prop's units. Both problems showed up only on the rendered page.

## Responsive and 200% text test

Same content on each (eyebrow, H1, paragraph, 2 buttons, 3 cards), built the idiomatic way:
- **CF:** custom classes with a `1fr 1fr 1fr` grid plus one tablet override.
- **Mast:** Section / Grid Row / three 4/12 Grid Columns / Card.
- **Lumos:** Section / Grid (Autofit, 3 max) / three Card Primary, with Global Styles present.

| | Client-First | Mast | Lumos |
| --- | --- | --- | --- |
| Card columns at 1440 / 768 / 480 / 320, normal text | 3 / 1 / 1 / 1 | 3 / 2 / 1 / 1 | 3 / 3 / 2 / 1 |
| Visible off-screen elements, normal text | 0 everywhere | 0 everywhere | 0 everywhere |
| Card columns at 200% text | 3 / 1 / 1 / 1 | 3 / 2 / 1 / 1 | **3 / 1 / 1 / 1 (adapts)** |
| **Visible overflow at 200% text** | **1440: cards 307px off-screen; 480: 13px; 320: 165px** | none | none |
| Invisible page-width overflow at 320 / 200% (no visible element off-screen) | — (visible overflow instead) | 124px | 110px |
| H1 on the page | yes | yes | **no** (MCP rich-text damage) |
| Build effort | 6 calls, 0 failures | 1 build + 2 prop calls, 0 failures | ~8 calls, 0 failures; plus 2 fix rounds (grid prop units, missing Global Styles) found only after publishing |

Why Client-First broke: the custom grid's `1fr` columns cannot shrink below their content, and pixel breakpoints do not fire when the text doubles. At 1440 with 200% text it stays at 3 columns and the third card runs 307px past the edge; at 320 each card is 469px wide. An agent building blind would not see this, because nothing looks wrong at normal text size. Lumos's grid primitives (auto-fit with `min()`, `minmax(0, 1fr)`) and Mast's components handled it.

**Verdict on the breakpointless claim:** confirmed for Lumos, and Mast also passed. The Client-First failure belongs to the agent-written custom grid, which is exactly the risk the Lumos advocate named: in Client-First the agent writes the layout primitives itself.
