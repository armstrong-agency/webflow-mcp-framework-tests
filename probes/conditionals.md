# Conditionals vs the Webflow MCP (verified 2026-11-02)

Source: [Webflow Help: Conditionals](https://help.webflow.com/hc/en-us/articles/33961320868115-Conditionals), read in full via browser. MCP surface: beta server v2.2.0 schemas plus `get_more_tools`, which answered "we have shown you the full tool list" when asked for a conditionals capability.

## What Conditionals are (per the article)

- Rule-based control of element settings and component props: **Visibility, Switch, Component variants, Text, Attributes, Images, Video**.
- Rules reference **component props** (inside a main component), **CMS fields** (in a Collection list/page), or **current locale data**.
- Rule vocabulary depends on data type: Contains / Starts with / Ends with (text), Is On/Off (switch), Is set / Is not set, Contains any (multi-reference), reference-field drill-down.
- **Condition groups** with any/all matching, each group with its own output; group order matters (first matching group wins); **fallback value** when nothing matches.
- Hidden elements are dropped from published code entirely unless "Keep in HTML when hidden" is set.
- Authored in the Designer via the "purple dot" on a setting or prop. The article describes no API.
- Explicit use cases: hide element when a prop is empty, set a nested component's variant from the parent's, **hide an optional slot with no content**, CMS-driven variants ("Featured" switch → Featured variant), locale banners.
- Quote: conditionals let one component adapt "without needing additional 'visibility' props or duplicate elements."

## What the MCP can and cannot do

| Capability | MCP |
| --- | --- |
| Static visibility on/off | Yes (`set_visibility` static_value) |
| Visibility bound directly to one boolean prop | Yes (`set_visibility` binding) — the old pattern Conditionals supersede |
| Tag/DOM id/settings bound directly to one prop or CMS/page/locale field | Yes (`set_settings` binding) |
| Rule-based conditionals: operators, groups, any/all, fallbacks, slot-empty checks | **No tool surface at all** |
| Conditional-driven variants, text, images, video | **No** |
| Read an existing conditional back | Unverified; no schema field names conditionals, so at best they are opaque |
| Risk | An agent calling `set_visibility`/`set_settings` on a setting that carries a conditional may silently replace it; untested because conditionals cannot be created headlessly |

## Exposure by framework

- The gap is a **platform/MCP gap, not a Lumos flaw**: any framework using components in CMS contexts would want conditionals.
- But exposure differs. Webflow positions conditionals as the successor to boolean visibility props and duplicate elements. Lumos-style closed components and Mast's prop-driven components migrate toward conditionals; Client-First's duplicate-section, class-only style is the one that needs them least.
- The one Lumos visibility mechanism that works through the MCP today (boolean Visibility props) is the mechanism Webflow now calls unnecessary.

## Round-trip test — RUN 2026-11-02

Fixture: "Probe Conditional" component on the Lumos starter; heading with a Designer-authored visibility conditional (rule: "Optional Text → Is set", output Visible, fallback Hidden), authored by Emmett in the Designer.

1. **Read:** `get_settings` all_raw_settings returned `visibility: {"sourceType": "conditional"}` — an opaque marker with no rules, operators, groups, or fallback. `all_resolved_settings` returned `visibility: null`. So a careful agent CAN detect "a conditional lives here" from raw settings, but can never read, evaluate, or reproduce it.
2. **Overwrite:** `set_visibility` static_value true succeeded with **no warning or error**. Re-read showed `visibility: true`; the conditional marker was gone. The MCP silently replaced a Designer-authored conditional with a static value.
3. **Designer-side confirmation (Emmett):** the heading renders visible and its visibility setting carries no conditional. Since the Optional Text prop was empty, a surviving conditional would have applied the Hidden fallback — the element being visible is behavioral proof the conditional is fully deleted, not orphaned. Fixture removed after the test.

Verdict: conditionals are **write-destroyable and read-opaque** through the MCP, confirmed on both the API side and the Designer side. Safe-agent rule: before any `set_visibility`/`set_settings` write, read raw settings and refuse to overwrite any value whose `sourceType` is `conditional`.
