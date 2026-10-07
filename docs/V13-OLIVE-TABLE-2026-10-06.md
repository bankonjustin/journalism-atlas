# V13 Dark Olive `#5d7400` usage table (report only, nothing applied)

*2026-10-06, redone against DESIGN-TOKENS-v13.md. Supersedes `V12-OLIVE-TABLE-2026-10-06.md`. **86 literal lines** (hex and `rgba(93,116,0,…)`) in 10 files, plus 82 uses through `var()`. By class: KEEP-AS-OLIVE 65, CHANGE 13, REVIEW 7, ON-DARK 1. Surface: measured from the DOM where the element rendered; 10 literal lines were not observed (hover/JS states) and are classified from role, assuming a light page; they are marked "(surface unverified)".*

**Classes.** KEEP-AS-OLIVE: text/icon/thin stroke on a light surface (becomes `var(--color-accent-on-light)`); olive *hover text/icon/stroke* on light is allowed. CHANGE: a fill, button background or hover fill (v13 forbids olive as a fill). ON-DARK: olive on a dark surface (use acid/lime). REVIEW: role unclear.

| file:line | element | property | state | surface | class | proposed v13 replacement |
|---|---|---|---|---|---|---|
| about-this-project.html:84 | `.about-eyebrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| about-this-project.html:109 | `.about-read-more` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| about-this-project.html:146 | `.pillar-number` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| about-this-project.html:209 | `.team-title` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| about-this-project.html:230 | `.team-link:hover` | border-color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| about-this-project.html:230 | `.team-link:hover` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| about-this-project.html:346 | `.looking-item::before` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| about-this-project.html:440 | `.btn-lime-about:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| about-this-project.html:528 | `<a.about-section> (inline)` | style | - | unobserved (unverified) | REVIEW | needs a human look |
| assets/css/header.css:180 | `.nav-search-btn:hover` | background | :hover | mixed | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| city-lab-chicago.html:54 | `.two-layer-pill` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:117 | `.context-toggle` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:143 | `.layer-stat-btn.active .layer-stat-label` | color | .active | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:156 | `.beat-chip.active, .plat-chip.active` | border-color | .active | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:173 | `.row-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:187 | `.card-link` | color | - | unobserved (unverified) | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:190 | `.empty-state a` | color | - | unobserved (unverified) | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:200 | `.feco-name:hover` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| city-lab-chicago.html:220 | `.pulse-badge-text` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| city-lab-chicago.html:372 | `<a.tab-pane> (inline)` | style | - | unobserved (unverified) | REVIEW | needs a human look |
| city-lab-chicago.html:453 | `<a.missing-cta> (inline)` | style | - | unobserved (unverified) | REVIEW | needs a human look |
| city-lab-chicago.html:455 | `<a.creators-view-toggle> (inline)` | style | - | unobserved (unverified) | REVIEW | needs a human look |
| city-lab-chicago.html:944 | `(JS/other)` | js | - | unobserved (unverified) | REVIEW | needs a human look |
| city-lab-chicago.html:1129 | `(JS/other)` | style | - | unobserved (unverified) | REVIEW | needs a human look |
| contact.html:116 | `.contribute-intro a` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| for-brands.html:132 | `.compare-th--right` | border-bottom | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:146 | `.btn-lime` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:149 | `.btn-lime:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:152 | `.btn-lime-lg` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:156 | `.btn-lime-lg:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:164 | `.stat-num .stat-plus` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:165 | `.stat-num.green` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:168 | `.stat-sub` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:170 | `.stat-live-dot` | background | - | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:173 | `.stat-cell--linked .stat-sub` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:243 | `.pulse-live-badge` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:243 | `.pulse-live-badge` | background | - | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:243 | `.pulse-live-badge` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:244 | `.pulse-dot` | background | - | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:249 | `.pulse-open-btn` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:249 | `.pulse-open-btn` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:250 | `.pulse-open-btn:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:257 | `.pulse-beat-name` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:259 | `.pulse-dot-sm` | background | - | unobserved (unverified) | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| index.html:264 | `.pulse-item-headline:hover` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| index.html:265 | `.pulse-col-more` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:287 | `.cluster-count-n` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:296 | `.cluster-explore-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:299 | `.intel-footer a` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:308 | `.research-badge` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:322 | `.research-card-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:345 | `.db-header-note` | color | - | unobserved (unverified) | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| index.html:1032 | `<a> (inline)` | style | - | mixed | REVIEW | needs a human look |
| partners/nj-lab.html:102 | `.rc-attribution a` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/nj-lab.html:149 | `.filter-chip.active` | border-color | .active | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/nj-lab.html:318 | `.partner-col-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/njlab.html:102 | `.rc-attribution a` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/njlab.html:149 | `.filter-chip.active` | border-color | .active | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/njlab.html:318 | `.partner-col-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:146 | `.audience-bridge-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:153 | `.trend-up` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:249 | `.archive-method a` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:455 | `.beat-tag` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:456 | `.beat-tag` | background | - | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| pulse.html:565 | `.pulse-dot-inline` | background | - | dark | ON-DARK | acid #ceff00 (active/CTA) or lime #97d600 (hover/focus) |
| pulse.html:607 | `.creator-chip:hover` | border-color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| pulse.html:608 | `.creator-chip:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| pulse.html:619 | `.creator-chip-count` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:620 | `.creator-chip-count` | background | - | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| pulse.html:713 | `.analysis-tab.active` | color | .active | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:806 | `.beat-more-btn:hover` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| pulse.html:870 | `.pulse-brands-cta-btn` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:871 | `.pulse-brands-cta-btn` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:879 | `.pulse-brands-cta-btn:hover` | background | :hover | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| pulse.html:915 | `.intel-week-badge` | color | - | unknown(gradient) | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:962 | `a.intel-post-link:hover` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| pulse.html:1044 | `.city-spotlight-eyebrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| pulse.html:1047 | `.city-spotlight-cta` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:124 | `.ticker-header .eyebrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:194 | `.ticker-card-byline` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:219 | `.ticker-card-link` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:239 | `.btn-lime` | border | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:384 | `.publications-section .eyebrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:460 | `.pub-arrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| research.html:467 | `.pub-card:hover .pub-headline-text` | color | :hover | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| research.html:497 | `.press-section .eyebrow` | color | - | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |

## Olive through `var()` (not in the original 113)

| file:line | element | property | via | surface | class | proposed |
|---|---|---|---|---|---|---|
| assets/css/main.css:428 | `.clear-filters-top` | border | `--color-dark-olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| assets/css/main.css:442 | `.clear-filters-top:hover` | background | `--color-dark-olive` | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| assets/css/main.css:443 | `.clear-filters-top:hover` | border-color | `--color-dark-olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| assets/css/main.css:532 | `.view-btn:hover:not(.active)` | border-color | `--color-dark-olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) (hover text/icon/stroke on light: allowed) |
| assets/css/main.css:1060 | `.sunburst-creator-avatar` | background | `--color-dark-olive` | unobserved | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| atlas-portal/index.html:512 | `.message.success` | color | `--olive-green` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| atlas-portal/index.html:605 | `.footer-section a` | color | `--olive-green` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| bluesky-creator-intelligence.html:52 | `.badge-atlas` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| bluesky-creator-intelligence.html:56 | `.header-cta` | border | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| bluesky-creator-intelligence.html:57 | `.header-cta:hover` | background | `--olive` | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| bluesky-creator-intelligence.html:172 | `.sort-btn.active` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| bluesky-creator-intelligence.html:199 | `.ci-platform.cross` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| for-brands.html:287 | `.form-submit:hover` | background | `--color-dark-olive` | light | CHANGE | fill: acid #ceff00 + black text (CTA/active) or lime #97d600 (hover); not olive. Tints: acid tint or step-2 gray (design call) |
| partners/_reviewjames.html:28 | `a.pagelink` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_reviewjames.html:30 | `.pill-confirmed` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_shell.html:90 | `.partner-url` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_shell.html:114 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_shell.html:143 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_shell.html:171 | `.region-label` | color | `--olive` | unobserved | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/_shell.html:191 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/ahp.html:115 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/ahp.html:158 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/ahp.html:183 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/ahp.html:217 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/ahp.html:229 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/cillizza.html:111 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/cillizza.html:154 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/cillizza.html:171 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/cillizza.html:209 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/cillizza.html:221 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/emily-atkin.html:97 | `.chip.active` | border-color | `--olive` | unobserved | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/emily-atkin.html:122 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/emily-atkin.html:136 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/emily-atkin.html:159 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/emily-atkin.html:170 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/icfj.html:69 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/icfj.html:84 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/icfj.html:92 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/icfj.html:101 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/icfj.html:115 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/iij.html:64 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/iij.html:79 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/iij.html:83 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/iij.html:94 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/iij.html:106 | `.about-link` | color | `--olive` | unobserved | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/jessica-stahl.html:58 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/jessica-stahl.html:72 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/jessica-stahl.html:80 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/jessica-stahl.html:88 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/jessica-stahl.html:100 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/joon-lee.html:46 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/joon-lee.html:54 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/joon-lee.html:59 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/joon-lee.html:67 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/karen-attiah.html:45 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/karen-attiah.html:53 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/karen-attiah.html:58 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/karen-attiah.html:65 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/knowledge-creators.html:42 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/knowledge-creators.html:54 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/knowledge-creators.html:62 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/knowledge-creators.html:70 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/knowledge-creators.html:77 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/natgeo.html:45 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/natgeo.html:53 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/natgeo.html:58 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/natgeo.html:65 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/news-creator-corps.html:65 | `.chip.active` | border-color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/news-creator-corps.html:83 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/news-creator-corps.html:91 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/news-creator-corps.html:102 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/news-creator-corps.html:114 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/noah-smith.html:66 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/noah-smith.html:74 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/noah-smith.html:82 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/noah-smith.html:97 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/rahim-jessani.html:66 | `.creator-channel` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/rahim-jessani.html:74 | `.card-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/rahim-jessani.html:82 | `.atlas-attribution-body a` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| partners/rahim-jessani.html:92 | `.about-link` | color | `--olive` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| wire.html:185 | `.wire-text a` | color | `--color-accent-hover` | unobserved | KEEP-AS-OLIVE | var(--color-accent-on-light) |
| wire.html:247 | `.wire-footer-band a` | color | `--color-accent-hover` | light | KEEP-AS-OLIVE | var(--color-accent-on-light) |

## Variable definitions holding olive (21) and comment lines (2)

These are not rendered; they complete the original count. A definition is classified by what its consumers do (see the `var()` table above).

| file:line | variable | consumers (class) | note |
|---|---|---|---|
| assets/css/variables.css:23 | `--color-dark-olive` | no consumers | brand palette name; fine as a definition (design-element color) |
| assets/css/variables.css:72 | `--color-accent-on-light` | no consumers | v13 token (new in Phase 1) |
| assets/css/variables.css:74 | `--color-focus-on-light` | no consumers |  |
| assets/css/variables.css:88 | `--color-accent-hover` | no consumers | **hover fill today** (search button) and other hover backgrounds: v13 forbids an olive fill; the token itself should not be olive |
| bluesky-creator-intelligence.html:32 | `--olive` | KEEP-AS-OLIVE 4, CHANGE 1 |  |
| index.html:256 | `--linked` | no consumers |  |
| partners/_reviewjames.html:10 | `--olive` | KEEP-AS-OLIVE 2 |  |
| partners/_shell.html:40 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/ahp.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/cillizza.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/emily-atkin.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/icfj.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/iij.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/jessica-stahl.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/joon-lee.html:16 | `--olive` | KEEP-AS-OLIVE 4 |  |
| partners/karen-attiah.html:16 | `--olive` | KEEP-AS-OLIVE 4 |  |
| partners/knowledge-creators.html:16 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/natgeo.html:16 | `--olive` | KEEP-AS-OLIVE 4 |  |
| partners/news-creator-corps.html:20 | `--olive` | KEEP-AS-OLIVE 5 |  |
| partners/noah-smith.html:20 | `--olive` | KEEP-AS-OLIVE 4 |  |
| partners/rahim-jessani.html:20 | `--olive` | KEEP-AS-OLIVE 4 |  |
| atlas-portal/index.html:32 | (comment) | n/a | `/* DESIGN-TOKEN FIX: Dark olive variable removed — color retired from ` |
| chicago-survey.html:16 | (comment) | n/a | `/* DESIGN-TOKEN FIX: --olive (#5d7400) removed — retired from palette ` |

## Reconciliation with the original 113

86 literal lines + 21 definitions + 2 comments = 109; the other 4 are lines in "… copy" files (`partners/njlab copy.html` ×3, `partners/_reviewjames copy.html` ×1) that duplicate `njlab.html` / `_reviewjames.html` and are classified the same as their originals. Total 113.

## Notes
- **The search button hover** (`header.css` `.nav-search-btn:hover`, olive background + white text) is a hover *fill*: CHANGE under v13 (lime hover fill with black text is the v13 hover).
- v13 lets olive color hover *text/icon/stroke* on light; those rows are KEEP-AS-OLIVE.
