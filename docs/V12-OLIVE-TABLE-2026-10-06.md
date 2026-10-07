> **Superseded by `V13-OLIVE-TABLE-2026-10-06.md` (v13 rules).**
# V12 Dark Olive `#5d7400` — usage table (report only, nothing applied)

*2026-10-06. Ruling 4: hover uses (`--color-accent-hover`, search-button hover) stay untouched; this table covers every live occurrence. Total lines: **113** in 32 files. By role: text 57, fill 24, hover 17, border 11, other 4.*

Proposed replacements are suggestions for approval. Surface (light/dark) is inferred; "FLAG" rows need a human look. Where olive carried a brand-green cue as text or border, any monotone replacement loses it; that is a design call, not a technical one.

| file | line | element (selector) | property | role | proposed v12 replacement | note |
|---|---|---|---|---|---|---|
| about-this-project.html | 84 | `.about-eyebrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| about-this-project.html | 109 | `.about-read-more` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| about-this-project.html | 146 | `.pillar-number` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| about-this-project.html | 209 | `.team-title` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| about-this-project.html | 230 | `.team-link:hover` | border-color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| about-this-project.html | 230 | `.team-link:hover` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| about-this-project.html | 346 | `.looking-item::before` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| about-this-project.html | 440 | `.btn-lime-about:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| about-this-project.html | 528 | `JS / attr / inline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| assets/css/header.css | 132 | `.nav-search-btn:hover` | background | hover | leave (ruling 4); v12 hover = lime #97d600 | RULING 4: untouched |
| assets/css/variables.css | 23 | `/ :root` | --color-dark-olive | other | FLAG: needs a human look |  |
| assets/css/variables.css | 85 | `/ :root` | --color-accent-hover | hover | leave (ruling 4); v12 hover = lime #97d600 | RULING 4: untouched |
| atlas-portal/index.html | 32 | `:root` | --olive-green | other | FLAG: needs a human look |  |
| bluesky-creator-intelligence.html | 32 | `:root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| chicago-survey.html | 16 | `:root` | - | other | FLAG: needs a human look |  |
| city-lab-chicago.html | 54 | `.two-layer-pill` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 117 | `.context-toggle` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 143 | `.layer-stat-btn.active .layer-stat-label` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 156 | `.beat-chip.active, .plat-chip.active` | border-color | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| city-lab-chicago.html | 173 | `.row-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 187 | `.card-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 190 | `.empty-state a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 200 | `.feco-name:hover` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| city-lab-chicago.html | 220 | `.pulse-badge-text` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 372 | `JS / attr / inline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 453 | `JS / attr / inline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 455 | `JS / attr / inline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| city-lab-chicago.html | 944 | `LATS=['TikTok / Video','Podcast','Newsletter','Website'];const COLORS=` | - | other | FLAG: needs a human look |  |
| city-lab-chicago.html | 1129 | `if(lo)` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| contact.html | 116 | `.contribute-intro a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| for-brands.html | 132 | `.compare-th--right` | border-bottom | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| index.html | 146 | `/ .btn-lime` | border | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| index.html | 149 | `.btn-lime:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| index.html | 152 | `.btn-lime-lg` | border | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| index.html | 156 | `.btn-lime-lg:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| index.html | 164 | `.stat-num .stat-plus` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 165 | `.stat-num.green` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 168 | `.stat-sub` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 170 | `.stat-live-dot` | background | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| index.html | 173 | `.stat-cell--linked .stat-sub` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 243 | `.pulse-live-badge` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 243 | `.pulse-live-badge` | background | fill | rgba(48,48,54,0.08) (cool-6 tint) |  |
| index.html | 243 | `.pulse-live-badge` | border | border | rgba(48,48,54,0.25) (cool-6 at same alpha) |  |
| index.html | 244 | `.pulse-dot` | background | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| index.html | 249 | `.pulse-open-btn` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 249 | `.pulse-open-btn` | border | border | rgba(48,48,54,0.3) (cool-6 at same alpha) |  |
| index.html | 250 | `.pulse-open-btn:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| index.html | 256 | `.pulse-col-header--linked:hover .pulse-beat-count` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| index.html | 257 | `.pulse-beat-name` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 259 | `.pulse-dot-sm` | background | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| index.html | 264 | `.pulse-item-headline:hover` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| index.html | 265 | `.pulse-col-more` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 287 | `.cluster-count-n` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 296 | `.cluster-explore-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 299 | `.intel-footer a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 308 | `.research-badge` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 322 | `.research-card-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 345 | `.db-header-note` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| index.html | 1032 | `JS / attr / inline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/_reviewjames copy.html | 10 | `ink rel="stylesheet" href="../assets/css/variables.css"> <style> :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/_reviewjames.html | 10 | `ink rel="stylesheet" href="../assets/css/variables.css"> <style> :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/_shell.html | 40 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/ahp.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/cillizza.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/emily-atkin.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/icfj.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/iij.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/jessica-stahl.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/joon-lee.html | 16 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/karen-attiah.html | 16 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/knowledge-creators.html | 16 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/natgeo.html | 16 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/news-creator-corps.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/nj-lab.html | 102 | `.rc-attribution a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/nj-lab.html | 149 | `.filter-chip.active` | border-color | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| partners/nj-lab.html | 318 | `.partner-col-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/njlab copy.html | 102 | `.rc-attribution a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/njlab copy.html | 149 | `.filter-chip.active` | border-color | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| partners/njlab copy.html | 318 | `.partner-col-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/njlab.html | 102 | `.rc-attribution a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/njlab.html | 149 | `.filter-chip.active` | border-color | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| partners/njlab.html | 318 | `.partner-col-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| partners/noah-smith.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| partners/rahim-jessani.html | 20 | `s.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'); :root` | --olive | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| pulse.html | 146 | `.audience-bridge-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 153 | `.trend-up` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 249 | `.archive-method a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 455 | `.beat-tag` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 456 | `.beat-tag` | background | fill | rgba(48,48,54,0.08) (cool-6 tint) |  |
| pulse.html | 565 | `/ .pulse-dot-inline` | background | fill | --gray-cool-6 #303036 fill (white text 13:1) or acid #ceff00 + black text if it is a CTA/active |  |
| pulse.html | 607 | `.creator-chip:hover` | border-color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| pulse.html | 608 | `.creator-chip:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| pulse.html | 619 | `.creator-chip-count` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 620 | `.creator-chip-count` | background | fill | rgba(48,48,54,0.08) (cool-6 tint) |  |
| pulse.html | 713 | `.analysis-tab.active` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 806 | `.beat-more-btn:hover` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| pulse.html | 870 | `.pulse-brands-cta-btn` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 871 | `.pulse-brands-cta-btn` | border | border | rgba(48,48,54,0.35) (cool-6 at same alpha) |  |
| pulse.html | 879 | `.pulse-brands-cta-btn:hover` | background | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| pulse.html | 915 | `/ .intel-week-badge` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 962 | `a.intel-post-link:hover` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| pulse.html | 1044 | `.city-spotlight-eyebrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| pulse.html | 1047 | `.city-spotlight-cta` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 124 | `.ticker-header .eyebrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 194 | `.ticker-card-byline` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 219 | `.ticker-card-link` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 239 | `.btn-lime` | border | border | var(--color-border) #c6c6cd (light) or --gray-cool-5 (emphasis) |  |
| research.html | 384 | `.publications-section .eyebrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 460 | `.pub-arrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| research.html | 467 | `.pub-card:hover .pub-headline-text` | color | hover | v12 hover = lime #97d600 (hover uses stay untouched pending your OK) |  |
| research.html | 497 | `.press-section .eyebrow` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| wire.html | 185 | `.wire-text a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
| wire.html | 247 | `.wire-footer-band a` | color | text | var(--color-text) / --gray-cool-6 #303036 (or --color-heading for emphasis); loses green cue |  |
