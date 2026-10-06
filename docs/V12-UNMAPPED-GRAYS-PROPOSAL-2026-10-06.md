# V12 unmapped grays — proposed nearest-step mapping (report only, nothing applied)

*2026-10-06. Grays in live code that are in neither v12 scale and are not one of the six retired values: **107 distinct colors, 1444 occurrences** (6-digit and expanded 3-digit hex; excludes `rgba()` forms, which need a separate pass). Proposed step = nearest Cool step by lightness (CIE L*), then adjusted by role: step 4 is never body/small text on white; borders snap to step 3 (light) or step 5 (dark); light text is only valid on a dark surface. Role comes from the CSS property on that line (`other/JS` = JS strings, SVG attributes, gradients, shorthands). Surface (light/dark) is not detected, so rows marked "verify surface" need a look. For James to approve in a follow-up; apply nothing.*

Decision for James: snap all of these, or only the six retired grays? v12's implementation note covers only the six. Warm-family grays are a different hue family from either scale; snapping them is a visible warmth shift.

| hex | uses | files | role mix | family | proposed Cool step | note | biggest file |
|---|---|---|---|---|---|---|---|
| `#888880` | 115 | 7 | other/JS 13, text 96, border 6 | warm | step 5 `#5e5e64` | text: step 4 not allowed for body/small text; chose 5 | research/figures/figure_1_funding_collapse_timeline.html |
| `#d4d4d8` | 105 | 28 | border 83, text 3, bg 2, other/JS 17 | neutral/cool | step 3 `#c6c6cd` |  | pulse.html |
| `#555555` | 91 | 20 | text 52, border 8, other/JS 31 | neutral/cool | step 5 `#5e5e64` |  | city-lab-chicago.html |
| `#888888` | 84 | 28 | text 80, other/JS 4 | neutral/cool | step 5 `#5e5e64` | text: step 4 not allowed for body/small text; chose 5 | atlas-signal-brief.html |
| `#666666` | 72 | 24 | text 51, other/JS 21 | neutral/cool | step 5 `#5e5e64` |  | assets/js/main.js |
| `#4a4a46` | 71 | 7 | other/JS 21, text 44, bg 6 | warm | step 5 `#5e5e64` |  | research/figures/figure_3_inn_concentration_treemap.html |
| `#b0b0b8` | 70 | 21 | text 35, border 33, other/JS 2 | neutral/cool | step 3 `#c6c6cd` | light text: only valid on a dark surface (step 3 on black); verify surface | city-lab-chicago.html |
| `#606068` | 63 | 21 | other/JS 4, text 59 | neutral/cool | step 5 `#5e5e64` |  | city-lab-chicago.html |
| `#faf9f5` | 62 | 7 | other/JS 50, bg 12 | warm | step 1 `#ffffff` |  | research/figures/figure_3_inn_concentration_treemap.html |
| `#111111` | 55 | 18 | other/JS 10, bg 20, border 1, text 24 | neutral/cool | step 7 `#121218` |  | for-brands.html |
| `#ddddd8` | 50 | 7 | other/JS 8, border 36, text 6 | warm | step 3 `#c6c6cd` | border: snapped to step 3 | research/figures/figure_3_inn_concentration_treemap.html |
| `#e0e0e0` | 47 | 12 | border 41, bg 2, other/JS 3, text 1 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | atlas-signal-brief.html |
| `#1a1a1a` | 38 | 12 | other/JS 9, border 10, bg 12, text 7 | neutral/cool | step 7 `#121218` |  | pulse.html |
| `#444444` | 34 | 29 | text 30, other/JS 2, border 1, bg 1 | neutral/cool | step 6 `#303036` |  | city-lab-chicago.html |
| `#aaaaaa` | 34 | 11 | text 33, border 1 | neutral/cool | step 4 `#909097` | text at step 4: large text only, FLAG | pulse.html |
| `#999999` | 32 | 13 | text 23, border 2, other/JS 7 | neutral/cool | step 4 `#909097` | text at step 4: large text only, FLAG | assets/css/main.css |
| `#1a1a18` | 31 | 7 | other/JS 19, text 12 | neutral/cool | step 7 `#121218` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#5f5e5a` | 30 | 6 | text 12, other/JS 18 | warm | step 5 `#5e5e64` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#2a2a2a` | 26 | 18 | bg 22, other/JS 2, border 2 | neutral/cool | step 6 `#303036` |  | atlas_pulse_intelligence.html |
| `#333333` | 22 | 14 | border 6, other/JS 3, text 10, bg 3 | neutral/cool | step 6 `#303036` |  | atlas-signal-brief.html |
| `#f0f0f0` | 19 | 11 | border 8, bg 11 | neutral/cool | step 2 `#efeff4` |  | atlas-signal-brief.html |
| `#222222` | 16 | 11 | other/JS 6, text 6, border 2, bg 2 | neutral/cool | step 6 `#303036` |  | beat-climate.html |
| `#fdf5e8` | 12 | 6 | bg 12 | warm | step 2 `#efeff4` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#fdf0f0` | 12 | 6 | bg 12 | warm | step 2 `#efeff4` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#f0faf7` | 12 | 6 | bg 12 | neutral/cool | step 1 `#ffffff` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#dddddd` | 11 | 5 | border 10, bg 1 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | assets/css/main.css |
| `#bbbbbb` | 11 | 5 | text 10, border 1 | neutral/cool | step 3 `#c6c6cd` | light text: only valid on a dark surface (step 3 on black); verify surface | pulse.html |
| `#5f6368` | 10 | 1 | text 10 | neutral/cool | step 5 `#5e5e64` |  | atlas-portal/google-form-template.html |
| `#fafafa` | 9 | 7 | bg 9 | neutral/cool | step 1 `#ffffff` |  | city-lab-chicago.html |
| `#e4e4e8` | 9 | 2 | border 7, bg 2 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | pulse.html |
| `#eeeeee` | 8 | 4 | border 6, other/JS 1, bg 1 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | assets/css/main.css |
| `#fce4ec` | 8 | 5 | bg 8 | warm | step 2 `#efeff4` |  | city-lab-chicago.html |
| `#e4e4e9` | 8 | 8 | bg 8 | neutral/cool | step 2 `#efeff4` |  | partners/ahp.html |
| `#f5f5f5` | 7 | 4 | bg 4, border 2, other/JS 1 | neutral/cool | step 2 `#efeff4` |  | atlas-signal-brief.html |
| `#e8e8e8` | 7 | 1 | border 7 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | city-lab-chicago.html |
| `#dddde0` | 7 | 1 | border 7 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | for-brands.html |
| `#f5f4ef` | 7 | 7 | other/JS 7 | warm | step 2 `#efeff4` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#eeeeea` | 6 | 6 | other/JS 6 | warm | step 2 `#efeff4` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#f0efe8` | 6 | 6 | bg 6 | warm | step 2 `#efeff4` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#c9c4b8` | 6 | 6 | other/JS 6 | warm | step 3 `#c6c6cd` |  | research/figures/figure_1_funding_collapse_timeline.html |
| `#f4f4f6` | 5 | 2 | bg 5 | neutral/cool | step 2 `#efeff4` |  | city-lab-chicago.html |
| `#e0e0e4` | 5 | 2 | border 4, bg 1 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | city-lab-dc-v3.html |
| `#cccccc` | 4 | 4 | border 2, text 1, other/JS 1 | neutral/cool | step 3 `#c6c6cd` |  | assets/css/main.css |
| `#ffebee` | 4 | 4 | bg 4 | warm | step 2 `#efeff4` |  | atlas-signal-brief.html |
| `#e8e8eb` | 4 | 2 | border 3, bg 1 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | index.html |
| `#e5e5e5` | 3 | 3 | border 3 | neutral/cool | step 3 `#c6c6cd` | border: snapped to step 3 | assets/css/header.css |
| `#1f1f1f` | 3 | 2 | border 3 | neutral/cool | step 7 `#121218` |  | index.html |
| `#f9f9f9` | 3 | 2 | bg 3 | neutral/cool | step 1 `#ffffff` |  | atlas-signal-brief.html |
| `#0d0d0d` | 3 | 3 | other/JS 1, bg 2 | neutral/cool | step 7 `#121218` |  | assets/js/main.js |
| `#f8f9fa` | 3 | 2 | bg 3 | neutral/cool | step 1 `#ffffff` |  | atlas-portal/google-form-template.html |
| `#2e2e2e` | 3 | 3 | other/JS 3 | neutral/cool | step 6 `#303036` |  | atlas_pulse_intelligence.html |
| `#777777` | 3 | 3 | other/JS 2, text 1 | neutral/cool | step 5 `#5e5e64` |  | atlas_pulse_intelligence.html |
| `#141414` | 3 | 2 | bg 3 | neutral/cool | step 7 `#121218` |  | atlas_pulse_intelligence.html |
| `#1c1c1c` | 3 | 2 | bg 1, other/JS 2 | neutral/cool | step 7 `#121218` |  | chicago-analysis.html |
| `#0a0a0a` | 3 | 2 | other/JS 1, bg 2 | neutral/cool | step 8 `#000000` |  | index.html |
| `#f8f8f8` | 3 | 1 | bg 1, other/JS 2 | neutral/cool | step 1 `#ffffff` |  | city-lab-chicago.html |
| `#221111` | 3 | 1 | other/JS 3 | warm | step 7 `#121218` |  | pulse.html |
| `#5a5a5a` | 2 | 2 | text 1, other/JS 1 | neutral/cool | step 5 `#5e5e64` |  | assets/css/main.css |
| `#48484f` | 2 | 2 | other/JS 2 | neutral/cool | step 5 `#5e5e64` |  | assets/css/variables.css |
| `#202124` | 2 | 1 | text 2 | neutral/cool | step 7 `#121218` |  | atlas-portal/google-form-template.html |

Remaining 47 colors (57 occurrences) are listed in the appendix as hex → proposed step only.

| hex | uses | proposed |
|---|---|---|
| `#3a3a3a` | 2 | step 6 |
| `#080810` | 2 | step 8 |
| `#f8f8f6` | 2 | step 1 |
| `#e8e8f0` | 2 | step 2 |
| `#f7f7fa` | 2 | step 1 |
| `#dfe6e9` | 2 | step 2 |
| `#110000` | 2 | step 8 |
| `#f0f0f2` | 2 | step 2 |
| `#2a2a24` | 2 | step 6 |
| `#23231d` | 2 | step 6 |
| `#ebebee` | 1 | step 3 |
| `#e5e5e8` | 1 | step 2 |
| `#424242` | 1 | step 6 |
| `#dadce0` | 1 | step 3 |
| `#f1f3f4` | 1 | step 2 |
| `#f9fff0` | 1 | step 1 |
| `#0d1400` | 1 | step 7 |
| `#08080f` | 1 | step 8 |
| `#050510` | 1 | step 8 |
| `#12121e` | 1 | step 7 |
| `#e0e0e3` | 1 | step 2 |
| `#c8c8c8` | 1 | step 3 |
| `#c8c8cc` | 1 | step 3 |
| `#fff5f7` | 1 | step 1 |
| `#fff8f8` | 1 | step 1 |
| `#fffbf0` | 1 | step 1 |
| `#f0f8e0` | 1 | step 2 |
| `#ffe8f0` | 1 | step 2 |
| `#ffe8e8` | 1 | step 2 |
| `#e8e8ec` | 1 | step 3 |
| `#fdfdf5` | 1 | step 1 |
| `#050505` | 1 | step 8 |
| `#060606` | 1 | step 8 |
| `#332222` | 1 | step 6 |
| `#443333` | 1 | step 6 |
| `#222211` | 1 | step 7 |
| `#7a7a70` | 1 | step 5 |
| `#c8c8bd` | 1 | step 3 |
| `#e8e8de` | 1 | step 2 |
| `#faf9fd` | 1 | step 1 |
| `#909098` | 1 | step 4 |
| `#f8f5f0` | 1 | step 2 |
| `#f0ebe1` | 1 | step 2 |
| `#8a8a8a` | 1 | step 4 |
| `#e8e2da` | 1 | step 2 |
| `#d0c8bc` | 1 | step 3 |
| `#fff0f0` | 1 | step 2 |
