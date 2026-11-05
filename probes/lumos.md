# Lumos probes

> **Correction (round 4, rendered):** the "silent corruption" in L-9c and the "one `calc` was silently rewritten" takeaway are a read-back bug only. Webflow stores and publishes the original `calc()`, and it computed correctly in the browser. See `round-4-rendered.md`. Whether the MCP can read existing conditionals was later tested in `conditionals.md`.

Site: Lumos v2 Starter, Webflow MCP 2.2.0 (beta server), headless data tools only, 2026-11-02. One run per probe. Evidence is MCP read-back; the webflow.io publish was declined, so rendered DOM/CSS is unchecked.

| ID | Mechanism | Result | Attempts | Notes |
| --- | --- | --- | --- | --- |
| L-4 | Assemble Section > Heading + Paragraph + Button Wrapper > Button via nested slots in one call | Pass | 3 | Slot names differ from slot prop names. `get_all_components` reports props "Container Slot" and "Slot"; the builder wants "Container" and "Content". Each wrong name returned an error **and left a partial Section on the page**. |
| L-7 | Classes string prop on an instance (`u-text-style-h3 probe-classes-test`) | Pass (unvalidated) | 1 | The prop is a raw `class` attribute bound to a string. A nonexistent class was accepted silently. These classes never appear in the style system, so style read-back cannot see or validate them. |
| L-8a | Switch an instance variant (Section Theme → Dark, Button → Secondary, Heading → H3) | Pass | 1 | Variant prop set with `type: string` and the variant id. |
| L-6a | Boolean Visibility prop false on an existing instance | Pass | 1 | Direct prop binding only. This is not Webflow Conditionals (rule groups, operators, fallback, slot-empty checks; drives visibility, variants, text, attributes, images, video). The MCP has no tool surface for Conditionals: `set_visibility` and `set_settings` accept only a single direct binding. |
| L-3 | Plain element into an open-component slot | Fail | 2 routes | Build into the instance: "doesn't support append". Move beside a slotted instance: "Cannot move an element before a component instance". Matches the guide: slots accept component instances only. |
| L-1 | Stack `u-text-style-h2` on custom class `probe_card_title` | Pass | 3 | `set_style` with both names fails with "One or more styles not found: probe_card_title, u-text-style-h2" though both exist. Works only after `create_style` of the combo `probe_card_title > u-text-style-h2`. The error does not point at the missing combo. |
| L-1b | Override one property on the stacked utility only | Pass | 1 | Global `.u-text-style-h2` unchanged. |
| L-2 | Rename the stacked utility h2 → h3 on one custom class | Pass | 1 | Override kept; global h2 untouched; combo now inherits global h3. |
| L-9a | Custom property `--probe-custom` via `update_style` | Fail | 1 | "Invalid style property --probe-custom". The whole update was rejected. |
| L-9b | `transform: scale(calc(1 + 0.2 * var(--_trigger---on)))` | Pass | 1 | Stored with the var bound to the Trigger variable. |
| L-9c | `opacity: calc(1 - 0.4 * var(--_trigger---on))` | **Silent corruption** | 1 | Reported success, but read-back shows opacity bound straight to the trigger variable; the `calc` was dropped. Off state would render opacity 0. |
| A-1 | Author a component: blank component, heading, `ComponentSlot` | Pass | 1 | |
| A-2 | Boolean prop bound to element visibility inside the definition | Pass | 1 | |
| A-3 | Fill the authored slot with a component on insert | Pass | 1 | Default slot name is "Slot". |
| X-1/L-8b | Variant with Theme "Dark mode" applied to the wrapper class for that variant only | Pass | 1 | Read-back: variant has the mode; base has none. |
| L-5 | Closed component: slot nested inside a Section instance's slot | Fail | 3 routes | Append into the instance refused; children inside an instance's slot are returned without element ids, so they cannot be used as anchors; `query_elements` finds 0 of them. No headless route found. |

## Takeaways

- Lumos's **class system** (custom + stacked `u-` + `is-`) works through the MCP, with one non-obvious extra step to create the combo.
- Lumos's **open component** workflow (any element in a slot) is blocked. Every piece of content has to be a component instance.
- Lumos's **closed component** workflow (nested slot) is blocked headlessly.
- **Conditionals** cannot be authored through the MCP. Simple prop-to-visibility bindings work; rule-based conditions do not exist on the tool surface. Unverified: whether the MCP can read existing conditionals or overwrites them when setting visibility.
- **Trigger & State** math is unsafe: custom properties are rejected and one `calc` was silently rewritten.
- **Classes props** move utilities outside the style system, so an agent can neither validate nor audit them through style tools.
- Two reliability hazards apply to any framework that leans on components: non-atomic failed builds, and slot names that do not match the reported prop names.
