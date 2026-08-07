# Atlas Partner Pages — Directory
*Source of truth for all partner page files, status, and metadata*
*Last updated: August 6, 2026*

---

## Convention

- All partner HTML files live in the **`partners/` subdirectory**
- Naming: `partners/[slug].html` → `/partners/[slug]` (clean URL via Cloudflare Pages)
- Shell template: `partners/_shell.html` — clone this for every new partner page
- V2+ suffix = staging version, not yet live. Remove suffix when promoted to live.
- Old root-level partner URLs redirect to new paths via `_redirects` at repo root
- Claude Code reads this file before touching any partner file

---

## Partner Index

| File | Description | Status | URL | Deploy |
|------|-------------|--------|-----|--------|
| `partners/index.html` | Partner index holding page | Pre-launch | `/partners` | Live |

---

## Published Pages (13 total)

Published and reachable by direct URL. Deliberately unlinked from nav / `partners/index.html` / `_redirects` / any sitemap while design direction is still being decided — "Live" implies discoverable, which these intentionally are not yet.

| File | Partner | URL | Status |
|------|---------|-----|--------|
| `partners/cillizza.html` | Chris Cillizza | `/partners/cillizza` | Published, unlinked |
| `partners/icfj.html` | ICFJ | `/partners/icfj` | Published, unlinked |
| `partners/ahp.html` | Anne Helen Petersen | `/partners/ahp` | Published, unlinked |
| `partners/jessica-stahl.html` | Jessica Stahl | `/partners/jessica-stahl` | Published, unlinked |
| `partners/news-creator-corps.html` | News Creator Corps | `/partners/news-creator-corps` | Published, unlinked |
| `partners/joon-lee.html` | Joon Lee | `/partners/joon-lee` | Published, unlinked |
| `partners/knowledge-creators.html` | Knowledge Creators | `/partners/knowledge-creators` | Published, unlinked |
| `partners/emily-atkin.html` | Emily Atkin | `/partners/emily-atkin` | Published, unlinked |
| `partners/natgeo.html` | NatGeo | `/partners/natgeo` | Published, unlinked |
| `partners/karen-attiah.html` | Karen Attiah | `/partners/karen-attiah` | Published, unlinked |
| `partners/rahim-jessani.html` | Rahim Jessani | `/partners/rahim-jessani` | Published, unlinked |
| `partners/noah-smith.html` | Noah Smith | `/partners/noah-smith` | Published, unlinked |
| `partners/iij.html` | Institute for Independent Journalists (IIJ) | `/partners/iij` | Published, unlinked — built Aug 1, 122 creators, pending confirmation of partnership next steps before any wider promotion |

---

## Card structure — open question

`PARTNERS.md` previously described a two-tier card system ("Minimal" vs. "Blurb"). As of the Aug 6 audit, no structural distinction exists across any of the 13 files above — every page uses the same `PARTNER_CONFIG` shape, including 3 `aboutParagraphs` entries regardless of partner type. Whether a real tier system (e.g. relationship-only vs. BD-showcase vs. a heavier institutional tier) is worth building is an open design question for James, not a settled system — do not assume a tier label on any page below reflects an actual structural difference.

---

## City Lab Partnerships

| Lab | Partner | Status | Lab URL | Partner page |
|-----|---------|--------|---------|--------------|
| NJ State Lab | Center for Cooperative Media, Montclair State University | Live — May 2026 | `/nj-lab` | `/partners/ccm` (not yet built — brief: ccm-partner-page-brief.md) |

**CCM notes:**
- Research by Carrie Brown, Ph.D., Tara George, M.A., Joe Amditis, M.A.
- CCM logo pending — placeholder comment in nj-lab.html
- Paper URL placeholder — update `<a href>` in Section 2 and CTA when paper is published
- `partners/ccm.html` needs to be built (separate session)
- Aug 6, 2026: the `nj-lab.html` CTA that linked live to `/partners/ccm` (a 404, since the file doesn't exist) has been neutralized to plain text with a `TODO` comment — see `nj-lab.html` CTA footer. Re-link once `ccm.html` ships.

---

## Asset Locations

| Asset type | Location |
|------------|----------|
| Partner logos (color) | `assets/images/curators/` |
| Partner logos (white, for hero) | `assets/images/curators/` |
| Atlas logos | `assets/images/logos/` |
| Shell template | `partners/_shell.html` |

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
| `atlasTotal` | Yes | Current Atlas total. Keep as `"1,700+"` until next milestone |
| `year` | Yes | Current year |

---

## Rules for Claude Code

1. **Read this file first** before creating, editing, or renaming any partner page file.
2. **Never overwrite a live file** — always use V2 suffix for rebuilds. Justin promotes manually after browser review.
3. **Update this file** after building any new partner page — add it to the appropriate table.
4. **Creator data is always hardcoded** — no fetch() calls on partner pages. Data updates = edit the HTML directly until a dynamic data layer exists.
5. **Two creators exist in partner HTML but not in Atlas** (Bisan Owda as of April 2026). Do not add partner-only creators to `creators-master.csv` without explicit instruction from Justin.
6. **Shell is the canonical template** — if a design change needs to propagate to all partner pages, update the shell first, then rebuild affected pages from it.
