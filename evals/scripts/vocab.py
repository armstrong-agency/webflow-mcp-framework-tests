"""Per-framework class validity checkers, written from the grammar sources before any model run.

Sources: ~/.claude/skills/wf-reference/client-first.md, ~/.claude/skills/wf-reference/mast.md,
sandbox-cf-skills-test/lumos-naming.md, plus class names observed on the real starters.

valid(fw, token) answers "is this a class the framework's grammar permits?" It does not judge idiom.
Lumos's full utility list was not available offline, so its u- families are the documented or
observed ones plus u-margin-*/u-padding-*/u-alignment-* (plausible, unverified); see limitations.
"""
import re

SIZES = r"(0|tiny|xxsmall|xsmall|small|medium|large|xlarge|xxlarge|huge|xhuge|xxhuge|none|auto)"

CF_PATTERNS = [
    r"page-wrapper", r"main-wrapper",
    r"section_[a-z0-9-]+",
    r"[a-z0-9-]+_[a-z0-9-]+",                     # custom folder_element (one underscore)
    r"padding-global", r"padding-section-(small|medium|large)",
    r"container-(small|medium|large)",
    r"text-size-(tiny|small|regular|medium|large)",
    r"text-weight-(light|normal|medium|semibold|bold|xbold)",
    r"text-align-(left|center|right)",
    r"text-color-[a-z0-9-]+", r"text-style-[a-z0-9-]+",
    r"background-color-[a-z0-9-]+",
    r"heading-style-h[1-6]",
    r"button", r"button-group", r"is-[a-z0-9-]+",
    r"max-width-[a-z0-9-]+",
    r"(margin|padding)-(top|bottom|left|right|vertical|horizontal)",
    r"(margin|padding)-" + SIZES,
    r"spacer-[a-z0-9-]+",
    r"overflow-(hidden|visible|scroll|auto)", r"hide", r"hide-(tablet|mobile-landscape|mobile-portrait)",
    r"align-center", r"layer", r"pointer-events-(auto|none)", r"icon-(embed|height)-[a-z0-9-]+",
    r"form_[a-z0-9-]+", r"rich-text", r"z-index-[0-9]+", r"color-scheme-[0-9]+",
]

MAST_BP = r"(lg|md|sm|xs)"
MAST_SZ = r"(0|xs|sm|md|lg|xl|xxl|auto)"
MAST_PATTERNS = [
    r"page-wrapper", r"page-main",
    r"section", r"container", r"row", r"col",
    r"col-" + MAST_BP + r"-([1-9]|1[0-2])",
    r"col-" + MAST_BP + r"-offset-[0-6]",
    r"col-" + MAST_BP + r"-(first|last)",
    r"col-shrink", r"col-lg-contain-(left|right)",
    r"row-align-(start|center|end)", r"row-justify-(start|center|end|between|around)",
    r"row-gap-" + MAST_SZ,
    r"button", r"card", r"h[1-6]", r"paragraph-(xl|lg|sm)", r"eyebrow", r"rich-text",
    r"input-group", r"input",
    r"u-[mp][tblrxy]?-" + MAST_SZ,
    r"u-text-[a-z0-9-]+", r"u-d-[a-z0-9-]+", r"u-bg-[a-z0-9-]+", r"u-mode-(dark|light)",
    r"u-img-[a-z0-9-]+",
    r"cc-[a-z0-9-]+",
    r"(?!section_)[a-z0-9-]+(_[a-z0-9-]+)+",      # spare custom: context_name
]

LUMOS_PATTERNS = [
    # v2 key (rescore): u- vocabulary limited to classes verified on the live Lumos v2 Starter or
    # documented in lumos-naming.md. v1 also allowed u-text-*, u-container-*, u-margin-*/u-padding-*,
    # u-alignment-*, u-weight-* and any is-*, and lacked u-section / u-section-spacer.
    r"[a-z0-9]+(_[a-z0-9]+){1,3}",                # type_variation_element, underscores only, <=3
    r"is-(?!secondary$)[a-z0-9-]+",               # Lumos buttons use component variants, not is-secondary
    r"u-section", r"u-section-spacer",
    r"u-container", r"u-container-(small|full)",
    r"u-text-style-(h[1-6]|display|large|main|small)",
    r"u-margin-trim", r"u-display-contents",
    r"u-grid-(autofit|autofill|custom|subgrid|breakout)",
    r"u-flex-(horizontal|vertical)-(wrap|nowrap)", r"u-flex-(grow|shrink|noshrink)",
    r"u-align-(items|self)-(start|center|end|stretch|variable)",
    r"u-justify-content-(start|center|end|between|around|variable)",
    r"u-theme-(dark|light|brand|inherit)", r"u-brand-[a-z0-9-]+",
]

_COMPILED = {
    fw: [re.compile(r"^" + p + r"$") for p in pats]
    for fw, pats in (("cf", CF_PATTERNS), ("mast", MAST_PATTERNS), ("lumos", LUMOS_PATTERNS))
}


def valid(fw, token):
    return any(p.match(token) for p in _COMPILED[fw])


def tokens(answer):
    """Normalize a raw model answer into class tokens."""
    a = answer.strip().strip("`").strip()
    a = re.sub(r"^(html|css|text)\s*\n", "", a)
    a = a.replace(".", " ").replace(",", " ")
    a = re.sub(r'class\s*=\s*["\']?', " ", a)
    return [t for t in re.split(r"[\s\"'`]+", a.lower()) if t]


def is_cf_custom(t):
    return bool(re.match(r"^[a-z0-9-]+_[a-z0-9-]+$", t))


def is_lumos_custom(t):
    return bool(re.match(r"^[a-z0-9]+(_[a-z0-9]+){1,3}$", t))


def is_mast_custom(t):
    return bool(re.match(r"^(?!section_)[a-z0-9-]+(_[a-z0-9-]+)+$", t))
