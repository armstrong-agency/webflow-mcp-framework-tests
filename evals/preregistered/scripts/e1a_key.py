"""E1a intents and answer key, fixed before any model run.

Scoring per answer:
  2 = idiomatic: matches the key's idiom rule for that framework and every token is valid in vocab.py
  1 = every token is valid framework vocabulary, but the answer is not the idiom
  0 = any invented, wrong-framework, or malformed token (or empty answer)

Where a framework ships no utility for an intent, its idiom is a grammar-conforming custom class
(CF/Mast: folder_element; Lumos: type_element). That is the documented practice, and it is lenient
by construction: any well-formed custom name passes. Reported separately as "custom-class idioms".
Lumos idioms do not require the custom class to be present (utilities alone count), so Lumos is not
penalized for omitting the always-first custom class.
"""
from vocab import valid, is_cf_custom, is_lumos_custom, is_mast_custom

INTENTS = [
    ("section-pad", "the wrapper inside a page section that gives it large top/bottom padding plus the site-wide left/right page gutter"),
    ("center-text-mb", "a paragraph with centered text and a small bottom margin"),
    ("two-col", "the parent element of a layout with two equal columns that stack on mobile"),
    ("btn-secondary", "a secondary-style button"),
    ("container-lg", "a content container with a large max width"),
    ("h2-as-h3", "an h3 heading element that should look like an h2"),
    ("flex-between", "a flex row with items vertically centered and space between them"),
    ("margin-trim", "a content wrapper that removes the top margin of its first child and the bottom margin of its last child"),
    ("card-grid", "the parent element of a responsive grid of cards"),
    ("dark-section", "a page section with a dark theme"),
]

# Which framework/intent pairs have no dedicated utility, so the idiom is a custom class.
CUSTOM_IDIOM = {("cf", "two-col"), ("cf", "flex-between"), ("cf", "margin-trim"), ("cf", "card-grid"),
                ("mast", "margin-trim")}


def _only(ts, allowed):
    return set(ts) <= set(allowed)


def idiomatic(fw, intent, ts):
    s = set(ts)
    if fw == "cf":
        if intent == "section-pad":
            return s == {"padding-global", "padding-section-large"}
        if intent == "center-text-mb":
            return {"text-align-center"} <= s and ("margin-small" in s or "margin-xsmall" in s) and "margin-bottom" in s
        if intent == "btn-secondary":
            return {"button", "is-secondary"} <= s and _only(s, {"button", "is-secondary", "is-small"})
        if intent == "container-lg":
            return s == {"container-large"}
        if intent == "h2-as-h3":
            return "heading-style-h2" in s and _only(s, {"heading-style-h2"} | {t for t in s if is_cf_custom(t)})
        if intent in ("two-col", "flex-between", "margin-trim", "card-grid"):
            return len(ts) == 1 and is_cf_custom(ts[0])
        if intent == "dark-section":
            return any(t.startswith("section_") for t in s) and any(
                t.startswith("background-color-") or t.startswith("text-color-") or t.startswith("is-")
                or t.startswith("color-scheme-") for t in s)
    if fw == "mast":
        if intent == "section-pad":
            return "section" in s
        if intent == "center-text-mb":
            return "u-text-center" in s and ("u-mb-sm" in s or "u-mb-xs" in s)
        if intent == "two-col":
            return "row" in s and not any(t.startswith("col") for t in s)
        if intent == "btn-secondary":
            return "button" in s and any(t.startswith("cc-") for t in s)
        if intent == "container-lg":
            return "container" in s
        if intent == "h2-as-h3":
            return s == {"h2"}
        if intent == "flex-between":
            return {"row", "row-align-center", "row-justify-between"} <= s
        if intent == "margin-trim":
            return s == {"rich-text"} or (len(ts) == 1 and is_mast_custom(ts[0]))
        if intent == "card-grid":
            return "row" in s and not any(t.startswith("col") for t in s)
        if intent == "dark-section":
            return {"section", "u-mode-dark"} <= s
    if fw == "lumos":
        customs = {t for t in s if is_lumos_custom(t)}
        if intent == "section-pad":
            return any(t.endswith("_wrap") for t in s)
        if intent == "center-text-mb":
            return any(t in s for t in ("u-alignment-center", "u-text-align-center"))
        if intent == "two-col":
            return any(t.startswith("u-grid-") for t in s) or (len(ts) == 1 and len(customs) == 1)
        if intent == "btn-secondary":
            return "is-secondary" in s and len(customs) >= 1
        if intent == "container-lg":
            return "u-container" in s or any(t.startswith("u-container-") for t in s)
        if intent == "h2-as-h3":
            return "u-text-style-h2" in s
        if intent == "flex-between":
            return any(t.startswith("u-flex-horizontal") for t in s) and "u-align-items-center" in s and "u-justify-content-between" in s
        if intent == "margin-trim":
            return "u-margin-trim" in s
        if intent == "card-grid":
            return any(t in s for t in ("u-grid-autofit", "u-grid-autofill"))
        if intent == "dark-section":
            return "u-theme-dark" in s
    raise ValueError((fw, intent))


def score(fw, intent, ts):
    if not ts or not all(valid(fw, t) for t in ts):
        return 0
    return 2 if idiomatic(fw, intent, ts) else 1
