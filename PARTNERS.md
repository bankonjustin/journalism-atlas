# Atlas Partner Pages — Directory
*Source of truth for all partner page files, status, and metadata*
*Last updated: April 2026*

---

## Convention

- All partner HTML files live in the **repo root** alongside `index.html`
- Naming: `partner-[slug].html` for institutional partners, `partner-list-[slug].html` for curator lists
- Shell template: `partner-page-shell-V1.html` — clone this for every new partner page
- V2+ suffix = staging version, not yet live. Remove suffix when promoted to live.
- Claude Code reads this file before touching any partner file

---

## Live Pages

| File | Partner | Type | Cards | Creators | Slug | Status |
|------|---------|------|-------|----------|------|--------|
| `partner-list-cillizza.html` | Chris Cillizza | Curator list | Minimal | 17 | `/partner-list-cillizza` | Live — V1 |
| `partner-list-grist.html` | Jess Stahl / Grist | Curator list | Minimal | ~20 | `/partner-list-grist` | Live — V1 |
| `partner-icfj.html` | ICFJ | Institutional | Blurb | 21 | `/partner-icfj` | Live — V1 |

## Staging (V2 — not yet live)

| File | Partner | Type | Cards | Creators | Notes |
|------|---------|------|-------|----------|-------|
| `partner-list-cillizza-V2.html` | Chris Cillizza | Curator list | Minimal | 17 | Shell rebuild. Needs browser review before replacing V1. |
| `partner-icfj-V2.html` | ICFJ | Institutional | Blurb | 21 | Shell rebuild. Logo wired to curators/ dir. Needs browser review. |
| `partner-page-shell-V1.html` | — | Shell/template | Both | — | Canonical template. Do not modify without updating this doc. |

## Pipeline (confirmed, not yet built)

| Partner | Type | Cards | Est. Creators | Notes |
|---------|------|-------|---------------|-------|
| Anne Helen Petersen | Curator list | Blurb | 23 | Largest single anchor. Data sourced, blurbs needed. |
| SembraMedia | Institutional | Blurb | TBD | MOU signed. Liz primary contact. |
| Grist (rebuild) | Curator list | Minimal→Blurb | ~20 | V1 predates shell. Rebuild when Cillizza/ICFJ V2 confirmed. |
| Project C | Institutional | Minimal | ~145 | Large count — may need pagination or filtered view. |
| ONA Creator Cohort | Institutional | Blurb | TBD | |
| CJF NextGen | Institutional | Blurb | TBD | |
| Going Solo | Institutional | TBD | TBD | |

---

## Asset Locations

| Asset type | Location |
|------------|----------|
| Partner logos (color) | `assets/images/curators/` |
| Partner logos (white, for hero) | `assets/images/curators/` |
| Atlas logos | `assets/images/logos/` |
| Shell template | `partner-page-shell-V1.html` (repo root) |

**Known assets in `assets/images/curators/`:**
- `ICFJ+ Logo_White.png` — hero panel (dark background)
- `ICFJ+ July 2025 Logo_Blue.png` — about card (light background)
- `Cillizza-1.jpg` — headshot, available if hero text treatment is ever replaced

---

## PARTNER Config Field Reference

When cloning the shell, update `const PARTNER = {}` with these fields:

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Full partner name |
| `shortName` | Yes | For stat strip label. Use org abbreviation for institutional (e.g. "ICFJ") |
| `channel` | Yes | Newsletter/org name |
| `url` | Yes | Partner's primary URL |
| `logoPath` | No | Path to white logo for hero. `null` = text treatment fallback |
| `logoPathColor` | No | Path to color logo for about card. `null` = initial treatment |
| `heroTitle` | No | Custom hero headline. If absent, formula is used: `"N journalists, curated by Name."` |
| `heroBlurb` | Yes | 2–3 sentence hero narrative |
| `pullQuote` | Yes | Pull quote for about section, attributed to partner |
| `aboutParagraphs` | Yes | Array of strings, 2–3 paragraphs |
| `creatorCount` | Yes | Actual count — must match CREATORS array length |
| `topicCount` | Yes | Count of distinct topics/beats in the list |
| `platformCount` | Yes | Count of distinct primary platforms |
| `geoCount` | Yes | Count of distinct states, regions, or countries |
| `geoLabel` | No | Stat strip cell 4 label. Default: `"States / regions covered"`. Override for global pages: `"Countries represented"` |
| `atlasTotal` | Yes | Current Atlas total. Keep as `"1,200+"` until next milestone |
| `year` | Yes | Current year |

---

## Rules for Claude Code

1. **Read this file first** before creating, editing, or renaming any partner page file.
2. **Never overwrite a live file** — always use V2 suffix for rebuilds. Justin promotes manually after browser review.
3. **Update this file** after building any new partner page — add it to the appropriate table.
4. **Creator data is always hardcoded** — no fetch() calls on partner pages. Data updates = edit the HTML directly until a dynamic data layer exists.
5. **Two creators exist in partner HTML but not in Atlas** (Bisan Owda as of April 2026). Do not add partner-only creators to `creators-master.csv` without explicit instruction from Justin.
6. **Shell is the canonical template** — if a design change needs to propagate to all partner pages, update the shell first, then rebuild affected pages from it.
