## E1a mean score (0-2)

| model | cf | mast | lumos |
|---|---|---|---|
| haiku | 0.77 (n=30, 0s=18) | 0.00 (n=30, 0s=30) | 0.07 (n=30, 0s=29) |
| sonnet | 1.37 (n=30, 0s=8) | 0.33 (n=30, 0s=24) | 1.33 (n=30, 0s=10) |
| all | 1.07 (n=60, 0s=26) | 0.17 (n=60, 0s=54) | 0.70 (n=60, 0s=39) |

Excluding custom-class idioms:
  cf: 1.47 (n=36)
  mast: 0.19 (n=54)
  lumos: 0.70 (n=60)

| intent | cf | mast | lumos |
|---|---|---|---|
| section-pad | 2.00 | 0.00 | 0.00 |
| center-text-mb | 1.33 | 1.00 | 1.33 |
| two-col | 1.00 | 0.00 | 1.00 |
| btn-secondary | 1.33 | 0.00 | 0.00 |
| container-lg | 1.50 | 0.00 | 1.00 |
| h2-as-h3 | 2.00 | 0.33 | 1.00 |
| flex-between | 0.00 | 0.00 | 0.67 |
| margin-trim | 0.17 | 0.00 | 1.00 |
| card-grid | 0.67 | 0.33 | 1.00 |
| dark-section | 0.67 | 0.00 | 0.00 |

## E1b % correct

| slice | cf | mast | lumos |
|---|---|---|---|
| all | 97% (70/72) | 99% (71/72) | 100% (72/72) |
| haiku | 100% (36/36) | 100% (36/36) | 100% (36/36) |
| sonnet | 94% (34/36) | 97% (35/36) | 100% (36/36) |
| type P | 100% (24/24) | 100% (24/24) | 100% (24/24) |
| type S | 100% (24/24) | 100% (24/24) | 100% (24/24) |
| type V | 100% (18/18) | 100% (18/18) | 100% (18/18) |
| type G | 67% (4/6) | 83% (5/6) | 100% (6/6) |

| q | cf | mast | lumos |
|---|---|---|---|
| Q1 (P) | 6/6 | 6/6 | 6/6 |
| Q2 (P) | 6/6 | 6/6 | 6/6 |
| Q3 (S) | 6/6 | 6/6 | 6/6 |
| Q4 (V) | 6/6 | 6/6 | 6/6 |
| Q5 (P) | 6/6 | 6/6 | 6/6 |
| Q6 (S) | 6/6 | 6/6 | 6/6 |
| Q7 (G) | 4/6 | 5/6 | 6/6 |
| Q8 (S) | 6/6 | 6/6 | 6/6 |
| Q9 (P) | 6/6 | 6/6 | 6/6 |
| Q10 (V) | 6/6 | 6/6 | 6/6 |
| Q11 (S) | 6/6 | 6/6 | 6/6 |
| Q12 (V) | 6/6 | 6/6 | 6/6 |

## E1c drift (sonnet, 10 samples each)

| metric | cf | mast | lumos |
|---|---|---|---|
| samples parsed | 10 | 10 | 10 |
| mean distinct class strings per role (of 10) | 1.41 | 2.29 | 2.29 |
| % tokens conforming | 100.0% | 99.1% | 100.0% |
| samples with any non-conforming class | 0 | 2 | 0 |
| mean classes per element | 1.06 | 1.29 | 1.26 |

cf per-role distinct: {'pricing.card': 1, 'pricing.popular_badge': 3, 'pricing.title': 1, 'pricing.price': 2, 'pricing.feature_list': 2, 'pricing.feature_item': 2, 'pricing.button': 1, 'team.card': 1, 'team.photo': 1, 'team.name': 2, 'team.role': 2, 'team.social_list': 1, 'team.social_link': 1, 'faq.item': 1, 'faq.question': 1, 'faq.answer': 1, 'faq.toggle_icon': 1}
cf invalid tokens: []

mast per-role distinct: {'pricing.card': 1, 'pricing.popular_badge': 3, 'pricing.title': 3, 'pricing.price': 3, 'pricing.feature_list': 2, 'pricing.feature_item': 3, 'pricing.button': 2, 'team.card': 2, 'team.photo': 3, 'team.name': 2, 'team.role': 2, 'team.social_list': 3, 'team.social_link': 2, 'faq.item': 1, 'faq.question': 4, 'faq.answer': 2, 'faq.toggle_icon': 1}
mast invalid tokens: ['team-card']

lumos per-role distinct: {'pricing.card': 2, 'pricing.popular_badge': 4, 'pricing.title': 3, 'pricing.price': 2, 'pricing.feature_list': 2, 'pricing.feature_item': 3, 'pricing.button': 1, 'team.card': 1, 'team.photo': 2, 'team.name': 2, 'team.role': 2, 'team.social_list': 2, 'team.social_link': 1, 'faq.item': 1, 'faq.question': 4, 'faq.answer': 4, 'faq.toggle_icon': 3}
lumos invalid tokens: []
