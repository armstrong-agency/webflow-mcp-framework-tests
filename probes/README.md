# MCP probes

These tests ask whether the Webflow MCP can do the things each framework depends on. Each one ran on a real starter site and was checked by reading the result back through the MCP. Round 4 then published test pages and measured them in Chrome.

The result files are working records, so they are terse and use test IDs such as `L-4`. The [repo README](../README.md) has the plain-language summary and a list of terms, and the plan at the bottom of this file explains each ID.

The original plan called for 3 runs per probe. Each probe ran once, on Webflow MCP beta v2.2.0. Test elements were removed after rounds 1 to 3, and the round 4 pages were left published so they could be measured.

## Reading order

| File | Covers | Main finding |
| --- | --- | --- |
| [lumos.md](lumos.md) | Lumos classes, slots, props, and variants | Classes work, but plain elements cannot go in slots and nested slots cannot be reached |
| [mast-and-client-first.md](mast-and-client-first.md) | Mast and Client-First classes and component builds | New class stacks must be created level by level, and failed component builds leave orphans |
| [conditionals.md](conditionals.md) | What the MCP can do with Webflow Conditionals | The MCP cannot read them, and a routine write silently deletes them |
| [round-2.md](round-2.md) | The cost of theme changes and components | A dark section took 1 write on Lumos and 5 on Client-First |
| [round-3.md](round-3.md) | Read-back exposure and formula variables | The MCP cannot write formula variables, and each starter depends on them to a different degree |
| [round-4-rendered.md](round-4-rendered.md) | Published pages, 200% text, and heading output | Client-First's custom grid overflowed, Lumos lost its H1, and the `calc()` bug was only in the read-back |
| [client-first-v3.md](client-first-v3.md) | What v3 documents, and the one v3 pattern tested live | v3's `grid-autofit` fixes the overflow, and the rest of v3 is untested |

Read round 4 before relying on any `calc()` claim from the earlier files. Round 4 corrected them, and each affected file carries a note at the top. The exposure counts in rounds 2 and 3 are values that would be misreported if an agent rewrote them. They read back correctly until then.

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
