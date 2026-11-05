"""E1b questions and answer key, fixed before any model run.

Fixtures: fixtures/a.html (CF), b.html (Mast), c.html (Lumos). Framework names are not in the HTML
or the prompt. An answer is correct when its tokens contain at least one accepted marker set and no
token from the listed distractors. Question types: P = spacing, S = structure/identity,
V = variant/styling, G = global change.

Lumos spacing (Q5, Q9) accepts the text element's own custom class or its u-text-style class,
because Lumos puts typographic margins in the text-style variables and the custom class; the
markup alone cannot show which. This leniency favours Lumos and is reported.
"""
from vocab import tokens

QUESTIONS = [
    ("Q1", "P", "Which element controls the top/bottom padding of the first (hero) section? Give that element's full class list."),
    ("Q2", "P", "Which element sets the site-wide left/right page gutter in the hero section? Give that element's full class list."),
    ("Q3", "S", "Which element sets the maximum content width in the hero section? Give that element's full class list."),
    ("Q4", "V", "Which single class makes the second button look different from the first?"),
    ("Q5", "P", "Which element's classes create the vertical space between the hero paragraph and the buttons? Give that element's full class list."),
    ("Q6", "S", "Which element lays out the three cards in columns? Give that element's full class list."),
    ("Q7", "G", "Which single class could you restyle to make ONLY the card titles bigger everywhere they appear on the site, without changing any other text? Answer \"none\" if no such class exists."),
    ("Q8", "S", "What is the full class list of the outermost element of the hero section?"),
    ("Q9", "P", "Which class sets the space below the eyebrow text (\"New release\")?"),
    ("Q10", "V", "Which class sets the font size of the hero paragraph?"),
    ("Q11", "S", "Which element groups the hero's text content (eyebrow, heading, paragraph, buttons)? Give that element's full class list."),
    ("Q12", "V", "Which class or classes make the card section use a dark color scheme?"),
]

# fixture -> question -> (accepted marker sets, distractor tokens)
KEY = {
    "cf": {
        "Q1": ([{"padding-section-large"}], {"container-large", "section_hero"}),
        "Q2": ([{"padding-global"}], {"container-large"}),
        "Q3": ([{"container-large"}], {"padding-global"}),
        "Q4": ([{"is-secondary"}], set()),
        "Q5": ([{"margin-top", "margin-medium"}, {"margin-top"}], {"text-size-medium", "margin-small"}),
        "Q6": ([{"features_list"}], {"features_component", "features_card"}),
        "Q7": ("none", None),
        "Q8": ([{"section_hero"}], {"padding-global"}),
        "Q9": ([{"margin-xsmall"}], {"margin-small"}),
        "Q10": ([{"text-size-medium"}], set()),
        "Q11": ([{"hero_content"}], {"hero_component"}),
        "Q12": ([{"background-color-black"}], set()),
    },
    "mast": {
        "Q1": ([{"section", "cc-hero"}, {"cc-hero"}], {"container"}),
        "Q2": ([{"container"}], {"section"}),
        "Q3": ([{"container"}], {"section", "row"}),
        "Q4": ([{"cc-secondary"}], set()),
        "Q5": ([{"u-mb-md"}], {"u-mb-sm"}),
        "Q6": ([{"row", "row-gap-md"}, {"row-gap-md"}], {"col", "col-lg-4"}),
        "Q7": ("none", None),
        "Q8": ([{"section", "cc-hero"}, {"cc-hero"}], {"container"}),
        "Q9": ([{"u-mb-sm"}], {"u-mb-md"}),
        "Q10": ([{"paragraph-lg"}], set()),
        "Q11": ([{"col", "col-lg-6"}, {"col-lg-6"}], {"row", "row-align-center"}),
        "Q12": ([{"u-mode-dark"}], set()),
    },
    "lumos": {
        "Q1": ([{"hero_wrap"}], {"hero_contain", "u-container"}),
        "Q2": ([{"u-container"}, {"hero_contain"}], {"hero_wrap"}),
        "Q3": ([{"u-container"}, {"hero_contain"}], {"hero_wrap"}),
        "Q4": ([{"is-secondary"}], set()),
        "Q5": ([{"hero_text"}, {"u-text-style-large"}, {"hero_button_wrap"}], set()),
        "Q6": ([{"features_list"}, {"u-grid-autofit"}], {"features_card"}),
        "Q7": ([{"features_card_title"}], {"u-text-style-h5"}),
        "Q8": ([{"hero_wrap"}], {"hero_contain"}),
        "Q9": ([{"hero_eyebrow"}, {"u-text-style-small"}], set()),
        "Q10": ([{"u-text-style-large"}], set()),
        "Q11": ([{"hero_content"}], {"hero_layout"}),
        "Q12": ([{"u-theme-dark"}], set()),
    },
}


def correct(fw, q, answer):
    accepted, distractors = KEY[fw][q]
    ts = set(tokens(str(answer)))
    if accepted == "none":
        return "none" in ts or str(answer).strip().lower().startswith("none")
    if ts & distractors:
        return False
    return any(m <= ts for m in accepted)
