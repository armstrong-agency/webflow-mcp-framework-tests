# MCP probes

These probes ask whether the Webflow MCP can perform the mechanics each framework depends on. Each one ran on a real starter for its framework and was read back through the MCP. Round 4 published test pages and measured them in Chrome.

The original plan called for 3 runs per probe. Each probe ran once, on Webflow MCP beta v2.2.0. Test elements were removed after rounds 1 to 3, and the round 4 pages were left published so they could be measured.

## Reading order

| File | Covers |
| --- | --- |
| [lumos.md](lumos.md) | Lumos classes, slots, props, variants, and `calc()` values |
| [mast-and-client-first.md](mast-and-client-first.md) | Mast and Client-First classes, stacks, and component builds |
| [conditionals.md](conditionals.md) | What the MCP can do with Webflow Conditionals, including a round-trip test |
| [round-2.md](round-2.md) | Theme change cost, component cost, and replications |
| [round-3.md](round-3.md) | Read-back exposure, formula variables, and class-string props on Mast |
| [round-4-rendered.md](round-4-rendered.md) | Published pages, including 200% text and heading output |
| [client-first-v3.md](client-first-v3.md) | What v3 documents, and the one v3 pattern tested live |

Read round 4 before relying on any `calc()` claim from the earlier files. Round 4 corrected them, and each affected file carries a note at the top.

These files were edited for publication in three ways. Sections that discussed an unpublished planning document were removed, Webflow site ids and a note about a private skill file were removed, and this README replaced the original plan's "3 times" wording. Test results were not changed.

## What was repeated

| Finding | Repeated on | Status |
| --- | --- | --- |
| Failed component builds leave orphans | Lumos and Mast | 5 of 5 failed builds |
| Slot names differ from slot prop names | Lumos and Mast | Repeated |
| Combo chains are order-sensitive | Mast and Client-First | Repeated |
| `calc()` with a variable reads back wrong | Lumos, on a fresh class | 2 of 2, and later shown to be read-back only |
| Class-string props accept nonexistent classes | Lumos and Mast | Repeated |

Every other result is a single run.

## Probe plan

| ID | Framework | Mechanism | Pass when |
| --- | --- | --- | --- |
| CF-1 | Client-First | Custom class and `is-` combo, with the same combo name on a second base | Each combo attaches to its own base |
| CF-2 | Client-First | Two existing global utilities on one Div (`padding-global` and `padding-section-large`) | Both stay global, with no new or empty class |
| CF-3 | Client-First | `folder_element` custom class with rem values bound to variables | Styles saved with variable references |
| M-1 | Mast | Four existing `u-` utilities stacked on one element | All four stay global, with no combo chain |
| M-2 | Mast | `cc-` combo on a base class (`section cc-home`) | Combo saved on the base only |
| M-3 | Mast | Grid spans `row` > `col col-lg-6 col-md-12` | Classes applied as existing globals |
| L-1 | Lumos | `u-` utility stacked on a custom class, overriding one property on the stacked instance | Override scoped, global utility unchanged |
| L-2 | Lumos | Rename a stacked utility (`u-text-style-h2` to `-h3`) on one custom class | Only that stack changes |
| L-3 | Lumos | Add a slot to a component and drop a plain element into it (open component) | Plain element lands in the slot |
| L-4 | Lumos | Fill a slot with a component instance | Instance lands in the slot |
| L-5 | Lumos | Nested slot inside a slot with `u-display-contents` (closed component) | Inner slot exposed on the outer instance |
| L-6 | Lumos | Boolean prop bound to visibility, toggled per instance | Element hidden in the DOM when false |
| L-7 | Lumos | Classes or attribute prop bound to an element attribute | Attribute renders per instance |
| L-8 | Lumos | Variant with a theme variable mode applied | Variant renders the mode's colors |
| L-9 | Lumos | Custom property with a `calc(var(--_trigger---on))` value | Value saved and rendered verbatim |
| X-1 | All | Create a variant and set a per-variant style override | Override scoped to the variant |

The IDs in the result files sometimes describe a variation of the planned probe. Where they differ, the result file's description is what actually ran.
