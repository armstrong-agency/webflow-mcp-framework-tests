# Mast and Client-First probes

Webflow MCP 2.2.0 (beta server), headless data tools, 2026-11-02, one run per probe, MCP read-back only (no publish).

- Mast: Mast Starter
- Client-First: 2 Agent Sandbox | Blank Relume Style Guide

## Client-First

| ID | Mechanism | Result | Calls | Notes |
| --- | --- | --- | --- | --- |
| CF-3 | Whole section in one call: `section_probe` > `padding-global padding-section-large` > `container-large` > `probe_component` > heading, `text-size-medium` paragraph, `button is-secondary` | Pass | 1 (+1 to create two custom classes) | Read-back matched every class. The two-utility pair and `button is-secondary` combos already existed on the style guide. |
| CF-1 | New `is-secondary` combo on a new base, same name as the button's combo | Pass | 2 | No collision: `.probe_component.is-secondary` and `.button.is-secondary` stayed separate when `parent_style_names` is passed. |
| CF-2b | Stack two utilities never combined before (`text-size-medium` + `text-weight-semibold`) | Pass after fix | 3 | Same failure as Lumos L-1 and Mast M-1: "One or more styles not found" until the combo is created. |

## Mast

| ID | Mechanism | Result | Calls | Notes |
| --- | --- | --- | --- | --- |
| M-1 | Four-class stack `eyebrow u-text-center u-mb-sm u-mt-sm` | Pass after fix | 6 | `set_style` fails; creating the depth-4 combo directly fails ("Parent style eyebrow > u-text-center > u-mb-sm not found"); each level must be created in order (3 creates), then apply. |
| M-1b | Same four classes in a different order | Fail | 1 | Order-sensitive: each ordering is a different combo chain and must be built separately. |
| M-2 | `cc-` combo on `section` | Pass | 1 | |
| M-3 | Section > Grid Row > 2 Grid Column > Heading / Rich Text via nested slots | Pass | 3 | Slot names are per component and differ from the reported slot prop name ("Slot content"): Section and Grid Column use "slot", Grid Row uses "Add Grid Column". Each failed build left an orphan Section. |

## Observations

- The Mast v2.4 starter is component-first, like Lumos: Section, Grid Row, Grid Column and content components with slots, `Class` string props, and visibility props. Mast's grid is now built from components, not only `col-*` classes.
- Webflow stores every multi-class stack as an ordered combo chain. Any new chain must be created level by level before the MCP will apply it. The cost grows with stack depth and with every new ordering. Client-First's style of one custom class plus at most a pre-made utility pair sits at the cheap end; Mast's up-to-four utility stacks sit at the expensive end; Lumos (custom class plus up to four `u-` utilities) is the same as Mast.
- Slot-name mismatch and non-atomic failed builds reproduced on Mast exactly as on Lumos. Both are component-system issues, not naming issues.
