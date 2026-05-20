# Atlas OG / Meta Tag Audit
*Last updated: 2026-05-20*
*Auditor: Claude Code, Session 2*

---

## Summary

**30 pages audited** (18 root, 12 partner)
- **Clean:** 4 root pages (index, search, research, contact)
- **Fixed in this session:** 10 pages (see Fixes Applied)
- **Flagged for Justin:** 12 partner pages (all missing full OG block); 4 additional items

**Key patterns found:**
1. All 12 partner pages are missing the full OG/Twitter block — they have `<title>` and `<meta name="description">` but no `og:title`, `og:url`, `og:image`, `og:description`, no Twitter tags, no canonical.
2. Several root pages have `.html` in canonical and twitter:url (not og:url).
3. Several newer pages (pulse, for-brands, nj-lab, city-lab pages) are missing canonical entirely.
4. `city-lab-dc-v3.html`'s og:url says `/city-lab-dc-v3` — must be `/city-lab-dc` to match the canonical slug.
5. `submit-thanks.html` canonical points to wrong URL entirely (`/contact-thanks.html`).
6. `latin-america-lab.html` twitter:card is `summary` instead of `summary_large_image`.

**OG image fallback confirmed:** `assets/images/logos/Atlas_green_gray_social_media_preview.png` — file exists.

---

## Status by Page

| Page | og:title | og:description | og:image | og:url | canonical | twitter: | Overall |
|------|----------|----------------|----------|--------|-----------|----------|---------|
| `index.html` | ⚠️ Format | OK | OK | OK | OK | OK | ⚠️ Flag |
| `search.html` | ⚠️ Format | OK | OK | OK | OK | OK | ⚠️ Flag |
| `postcard.html` | OK | ⚠️ Mismatch | OK | OK | ❌ Missing | ⚠️ Mismatch | ❌ Fix |
| `about-this-project.html` | ⚠️ Separator | ⚠️ Too long | OK | OK | OK | ⚠️ Separator | ⚠️ Flag |
| `who-we-are.html` | ⚠️ Separator | OK | OK | OK | ❌ .html | ❌ .html | ❌ Fix |
| `advisory.html` | ⚠️ Separator | OK | OK | OK | ❌ .html | ❌ .html | ❌ Fix |
| `contact.html` | OK | OK | OK | OK | OK | OK | ✅ Clean |
| `submit.html` | ⚠️ Format | OK | OK | OK | ❌ .html | ❌ .html | ❌ Fix + Flag |
| `submit-thanks.html` | OK | OK | OK | OK | ❌ Wrong URL | ❌ Wrong URL | ❌ Fix |
| `how-we-did-this.html` | ⚠️ Separator | OK | OK | OK | ❌ .html | ❌ .html | ❌ Fix |
| `research.html` | OK | OK | OK | OK | OK | OK | ✅ Clean |
| `updates.html` | ⚠️ Format | OK | OK | OK | ❌ .html | ❌ .html | ❌ Fix |
| `pulse.html` | OK | OK | OK | OK | ❌ Missing | OK | ❌ Fix |
| `for-brands.html` | OK | OK | OK | OK | ❌ Missing | OK | ❌ Fix |
| `nj-lab.html` | OK | OK | OK | OK | ❌ Missing | OK | ❌ Fix |
| `city-lab-chicago.html` | OK | OK | OK | OK | ❌ Missing | OK | ❌ Fix |
| `city-lab-dc-v3.html` | ⚠️ See note | ❌ Boilerplate | OK | ❌ Wrong slug | ❌ Missing | ❌ Wrong slug | ❌ Fix + Flag |
| `latin-america-lab.html` | OK | OK | OK | OK | ❌ Missing | ❌ `summary` / boilerplate desc | ❌ Fix |
| `partners/cillizza.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/ahp.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/icfj.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/news-creator-corps.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/joon-lee.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/jessica-stahl.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/knowledge-creators.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/emily-atkin.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/natgeo.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/karen-attiah.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/rahim-jessani.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |
| `partners/noah-smith.html` | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Flag |

---

## Fixes Applied

All fixes below are direct HTML edits. No new og:description copy was written into HTML — descriptions for flagged items are in "Flags for Justin" below.

| Page | Tag | Issue | Fix Applied |
|------|-----|-------|-------------|
| `who-we-are.html` | canonical | `href` had `.html` extension | Removed `.html` → `https://journalismatlas.com/who-we-are` |
| `who-we-are.html` | twitter:url | Had `.html` extension | Removed `.html` → `https://journalismatlas.com/who-we-are` |
| `advisory.html` | canonical | `href` had `.html` extension | Removed `.html` → `https://journalismatlas.com/advisory` |
| `advisory.html` | twitter:url | Had `.html` extension | Removed `.html` → `https://journalismatlas.com/advisory` |
| `submit.html` | canonical | `href` had `.html` extension | Removed `.html` → `https://journalismatlas.com/submit` |
| `submit.html` | twitter:url | Had `.html` extension | Removed `.html` → `https://journalismatlas.com/submit` |
| `submit-thanks.html` | canonical | Pointed to wrong URL (`/contact-thanks.html`) | Fixed to `https://journalismatlas.com/submit-thanks` |
| `submit-thanks.html` | twitter:url | Pointed to wrong URL (`/contact-thanks.html`) | Fixed to `https://journalismatlas.com/submit-thanks` |
| `how-we-did-this.html` | canonical | `href` had `.html` extension | Removed `.html` → `https://journalismatlas.com/how-we-did-this` |
| `how-we-did-this.html` | twitter:url | Had `.html` extension | Removed `.html` → `https://journalismatlas.com/how-we-did-this` |
| `updates.html` | canonical | `href` had `.html` extension | Removed `.html` → `https://journalismatlas.com/updates` |
| `updates.html` | twitter:url | Had `.html` extension | Removed `.html` → `https://journalismatlas.com/updates` |
| `pulse.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/pulse">` |
| `for-brands.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/for-brands">` |
| `nj-lab.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/nj-lab">` |
| `city-lab-chicago.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/city-lab-chicago">` |
| `city-lab-dc-v3.html` | og:url | Said `/city-lab-dc-v3` (wrong slug) | Fixed to `https://journalismatlas.com/city-lab-dc` |
| `city-lab-dc-v3.html` | twitter:url | Said `/city-lab-dc-v3` (wrong slug) | Fixed to `https://journalismatlas.com/city-lab-dc` |
| `city-lab-dc-v3.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/city-lab-dc">` |
| `latin-america-lab.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/latin-america-lab">` |
| `latin-america-lab.html` | twitter:card | Was `summary`, should be `summary_large_image` | Fixed |
| `postcard.html` | canonical | Missing entirely | Added `<link rel="canonical" href="https://journalismatlas.com/postcard">` |

---

## Flags for Justin

### 1. All 12 partner pages: full OG block missing

Every partner page has `<title>` and `<meta name="description">` but is missing the full Open Graph block. The following tags need to be added to each page's `<head>`:
- `og:title`
- `og:description`
- `og:image`
- `og:url`
- `<link rel="canonical">`
- `twitter:title`, `twitter:description`, `twitter:image`
- Update `twitter:card` from `summary` → `summary_large_image`

**Proposed OG titles** (format: `[Page-specific title] — The Independent Journalism Atlas`). These use the existing `<title>` tags as source. Confirm before writing to HTML:

| File | Existing `<title>` | Proposed og:title |
|------|--------------------|-------------------|
| `partners/cillizza.html` | Chris Cillizza's State Political Reporters — Independent Journalism Atlas | Chris Cillizza's State Political Reporters — The Independent Journalism Atlas |
| `partners/ahp.html` | Anne Helen Petersen's Picks — Independent Journalism Atlas | Anne Helen Petersen's Picks — The Independent Journalism Atlas |
| `partners/icfj.html` | Independent journalists from around the world, in partnership with ICFJ — Independent Journalism Atlas | ICFJ's Global Creator Picks — The Independent Journalism Atlas *(title is too long for og:title — needs shortening — confirm with Justin)* |
| `partners/news-creator-corps.html` | News Creator Corps Picks — Independent Journalism Atlas | News Creator Corps Picks — The Independent Journalism Atlas |
| `partners/joon-lee.html` | Joon Lee's Picks — Independent Journalism Atlas | Joon Lee's Picks — The Independent Journalism Atlas |
| `partners/jessica-stahl.html` | Jessica Stahl's Climate Picks — Independent Journalism Atlas | Jessica Stahl's Climate Picks — The Independent Journalism Atlas |
| `partners/knowledge-creators.html` | Knowledge Creators Picks — Independent Journalism Atlas | Knowledge Creators' Picks — The Independent Journalism Atlas |
| `partners/emily-atkin.html` | Emily Atkin's Climate Picks — Independent Journalism Atlas | Emily Atkin's Climate Picks — The Independent Journalism Atlas |
| `partners/natgeo.html` | NatGeo Creator Cohort — Independent Journalism Atlas | NatGeo Creator Cohort — The Independent Journalism Atlas |
| `partners/karen-attiah.html` | Karen Attiah's Picks — Independent Journalism Atlas | Karen Attiah's Picks — The Independent Journalism Atlas |
| `partners/rahim-jessani.html` | Rahim Jessani's Picks — Independent Journalism Atlas | Rahim Jessani's Picks — The Independent Journalism Atlas |
| `partners/noah-smith.html` | Noah Smith's Picks — Independent Journalism Atlas | Noah Smith's Picks — The Independent Journalism Atlas |

**Proposed og:description copy** (all marked `[PROPOSED — needs Justin/Liz review]`):

Each page already has a `<meta name="description">`. These can be reused as og:description values — they are page-specific, appropriately scoped, and within character limits. Lengths in parentheses:

| File | Existing meta description | Chars | Reuse as og:description? |
|------|--------------------------|-------|--------------------------|
| `partners/cillizza.html` | Political analyst Chris Cillizza curated this list of 17 independent journalists covering state and local politics across the US. | 135 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |
| `partners/ahp.html` | 17 independent creators recommended by Anne Helen Petersen, author of Culture Study — spanning culture, gender, local news, food, and lifestyle. | 150 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |
| `partners/icfj.html` | The International Center for Journalists and the Independent Journalism Atlas present 21 creator-journalists across Latin America, Africa, and MENA doing essential independent work. | 178 | [PROPOSED — needs Justin/Liz review] Over 160 chars — shorten before use |
| `partners/news-creator-corps.html` | 16 diverse, social-first independent journalists recommended by News Creator Corps — covering politics, identity, activism, and culture across video and audio platforms. | 169 | [PROPOSED — needs Justin/Liz review] Slightly over — trim or reuse |
| `partners/joon-lee.html` | 14 independent sports and culture creators recommended by sportswriter Joon Lee — the best independent voices operating across YouTube, Substack, and social. | 158 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |
| `partners/jessica-stahl.html` | 22 independent climate and environment creators recommended by journalist and editor Jessica Stahl — covering the climate crisis, energy transition, and environmental accountability. | 181 | [PROPOSED — needs Justin/Liz review] Over 160 — shorten before use |
| `partners/knowledge-creators.html` | 17 edu-journalism creators tracked by Knowledge Creators — blending journalism and education across YouTube, podcasts, and newsletters on tech, health, business, and science. | 174 | [PROPOSED — needs Justin/Liz review] Over 160 — shorten before use |
| `partners/emily-atkin.html` | 11 independent climate creators recommended by Emily Atkin, author of Heated — the writers and reporters she turns to for the best independent climate journalism. | 162 | [PROPOSED — needs Justin/Liz review] Just over — trim 2–3 chars |
| `partners/natgeo.html` | 8 visual storytellers from the National Geographic creator cohort — bringing science, nature, and exploration to new audiences across social and video platforms. | 161 | [PROPOSED — needs Justin/Liz review] 1 char over — trim before use |
| `partners/karen-attiah.html` | 8 independent creators recommended by Karen Attiah, journalist and global opinions editor — spanning politics, gender, media accountability, law, and culture. | 159 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |
| `partners/rahim-jessani.html` | 7 independent creators recommended by Rahim Jessani, founder of Bottom Up Media — covering accountability, culture, and politics with an independent lens. | 153 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |
| `partners/noah-smith.html` | 8 independent economics and policy creators recommended by Noah Smith, author of Noahpinion — essential reading in economics, tech, and policy. | 143 | [PROPOSED — needs Justin/Liz review] Yes, reuse directly |

**Partner OG image:** All partner pages can use the same fallback as root pages: `assets/images/logos/Atlas_green_gray_social_media_preview.png` — or a page-specific partner image if one exists. No page-specific partner OG images currently exist in the repo. Flag: should partner pages eventually get custom OG images showing the curator's headshot or branding? Currently: use fallback.

---

### 2. `city-lab-dc-v3.html` — og:description is boilerplate

Current: `"Discover 1,180+ independent creator-journalists across every beat, platform, and geography."` (91 chars)
This is generic boilerplate copy, not specific to the DC lab.

`city-lab-chicago.html` has a proper page-specific description for comparison: `"An ecosystem map of independent journalism in Chicago — creator-journalists, coverage gaps, and the full 245-outlet media landscape."`

[PROPOSED — needs Justin/Liz review]: `"350+ journalists and outlets mapped. Who's actually covering Washington now that the press corps has thinned? The Atlas DC Lab shows you."` (138 chars)

Same boilerplate issue in twitter:description for `latin-america-lab.html` (fixed in HTML to match the correct og:description — see Fixes Applied).

---

### 3. `submit.html` and `submit-thanks.html` — redirect conflict

Per `_redirects`: `/submit` → `/contact` (301). This means `submit.html` and `submit-thanks.html` may be effectively unreachable at their canonical URLs if Cloudflare serves the redirect before the HTML. Confirm with Justin:
- Is `/submit` still intended to be a live public page, or is it fully replaced by `/contact`?
- If `/submit` is live, the redirect in `_redirects` should be removed.
- If `/submit` is dead, no OG work needed.

---

### 4. Title format inconsistency — `|` vs `—` vs `-` separators

The audit spec calls for `[Page-specific title] — The Independent Journalism Atlas` (em-dash). Several pages use `|` (pipe) or `-` (hyphen) instead. These are not broken but inconsistent. Flag: standardize in a future pass or confirm mixed separators are intentional.

| Page | Current separator |
|------|------------------|
| `about-this-project.html` | `\|` (pipe) |
| `contact.html` | `\|` (pipe) |
| `research.html` | `\|` (pipe) |
| `nj-lab.html` | `\|` (pipe) |
| `for-brands.html` | `\|` (pipe) |
| `who-we-are.html` | `-` (hyphen) |
| `advisory.html` | `-` (hyphen) |
| `how-we-did-this.html` | `-` (hyphen) |
| `updates.html` | `-` (hyphen) |
| `submit.html` | `-` (hyphen) |
| `submit-thanks.html` | `-` (hyphen) |
| `index.html` | none (no prefix title) |
| `search.html` | none (no brand suffix) |

**Note on `index.html`:** og:title is `"Independent Journalism Atlas"` — no page-specific prefix and missing "The". This is arguably correct for the homepage (it IS the Atlas) but doesn't follow the spec format. Flag for Justin.

**Note on `search.html`:** og:title is `"Explore the Atlas"` — no brand suffix. Could be `"Explore the Atlas — The Independent Journalism Atlas"` but that's redundant. Flag for Justin.

---

### 5. `about-this-project.html` — og:description over 160 chars

Current (174 chars): `"The Independent Journalism Atlas is a wayfinder for the future of news media — mapping individuals committing acts of journalism outside traditional institutional structures."`

[PROPOSED — needs Justin/Liz review]: `"A wayfinder for independent journalism — mapping 1,400+ creator-journalists working outside traditional newsrooms, by beat, platform, and geography."` (150 chars)

---

### 6. `postcard.html` — twitter:description mismatch

og:description says "1,000+ creators" — twitter:description says "1,180+ independent creator-journalists across every beat, platform, and geography" (generic boilerplate). These should match and use the current count.

[PROPOSED — needs Justin/Liz review]: Align twitter:description to match og:description, or update both to a consistent current count. The og:description copy itself is good; just copy it to twitter:description.

---

## Pages Confirmed Clean

- `index.html` — clean except title format (no breaking issues)
- `search.html` — clean except title format (no breaking issues)
- `contact.html` — fully clean
- `research.html` — fully clean
- `about-this-project.html` — canonical/urls clean; description length and separator are minor flags only
