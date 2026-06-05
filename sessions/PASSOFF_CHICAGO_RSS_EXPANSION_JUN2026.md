# Passoff — Chicago RSS Expansion
**Date:** June 5, 2026
**File edited:** `city-lab-chicago.html`

---

## Feed count

| | Before | After |
|---|---|---|
| Total CHICAGO_FEEDS | 31 | 65 |
| Creator layer | 23 | 26 |
| Institution layer | 8 | 39 |

---

## Tier-by-tier yield

| Tier | Checked | Confirmed | Not found | Dupes skipped |
|---|---|---|---|---|
| T1 — Soloprenuers / Collective | 5 | 3 | 1 | 1 |
| T2 — Nonprofit | 21 | 5 + 2 alt = 7 | 14 | 2 |
| T3 — For-Profit Legacy + New Media | 12 | 7 + 1 alt = 8 | 5 | 0 |
| T4 — For-Profit Niche | 30 | 11 + 1 alt = 12 | 19 | 0 |
| T5 — Other / Student | 8 | 4 | 4 | 0 |
| **Total** | **76** | **34** | **42** | **3** |

---

## Confirmed feeds added

### Tier 1 — Independent Creators / Collective

| Name | Layer | Beat | RSS |
|---|---|---|---|
| Unraveled | creator | General News ⚑ | https://www.unraveledpress.com/rss.xml |
| 350 Chicago | creator | Environment / Climate | https://350chicago.substack.com/feed |
| Sixty Inches From Center | creator | Arts & Culture | https://sixtyinchesfromcenter.org/feed |

### Tier 2 — Nonprofits

| Name | Layer | Beat | RSS |
|---|---|---|---|
| Evanston Roundtable | institution | City Hall & Neighborhoods | https://evanstonroundtable.com/feed |
| In These Times | institution | Labor / Politics | https://inthesetimes.com/rss |
| Streetsblog Chicago | institution | City Hall & Neighborhoods | https://chi.streetsblog.org/feed |
| WBEZ 91.5 FM | institution | General News (volume:high) | https://wbez.org/rss |
| Wednesday Journal | institution | City Hall & Neighborhoods | https://wednesdayjournalonline.com/feed |
| Capital B Gary | institution | Black Chicago / Community | https://capitalbnews.org/feed |
| PBS Chicago WTTW | institution | General News | https://news.wttw.com/rss.xml |

### Tier 3 — For-Profit Legacy

| Name | Layer | Beat | RSS |
|---|---|---|---|
| ABC 7 News Chicago | institution | General News (volume:high) | https://abc7chicago.com/feed |
| Chicago Magazine | institution | Arts & Culture | https://chicagomag.com/feed |
| Fox 32 Chicago | institution | General News (volume:high) | https://fox32chicago.com/rss.xml |
| NBC 5 News Chicago | institution | General News (volume:high) | https://nbcchicago.com/feed |
| Telemundo Chicago | institution | Immigration / Latino | https://telemundochicago.com/feed |
| WGN 9 TV | institution | General News (volume:high) | https://wgntv.com/feed |
| WGN 720 AM | institution | General News | https://wgnradio.com/feed |
| Chicago Sun-Times | institution | General News (volume:high) | https://chicago.suntimes.com/rss/index.xml |

### Tier 4 — For-Profit Niche

| Name | Layer | Beat | RSS |
|---|---|---|---|
| Chicago Reader | institution | Arts & Culture | https://chicagoreader.com/feed |
| Third Coast Review | institution | Arts & Culture | https://thirdcoastreview.com/feed |
| Windy City Times | institution | LGBTQ+ | https://windycitytimes.com/feed |
| Chicago Parent | institution | General News | https://chicagoparent.com/rss.xml |
| Chicago Crusader | institution | Black Chicago | https://chicagocrusader.com/feed |
| Negocios Now | institution | Business | https://negociosnow.com/feed |
| Urbanize Chicago | institution | City Hall & Neighborhoods | https://chicago.urbanize.city/rss.xml |
| Chicago Classical Review | institution | Arts & Culture | https://chicagoclassicalreview.com/feed |
| La Raza | institution | Immigration / Latino | https://laraza.com/feed |
| The Real Deal Chicago | institution | Business | https://therealdeal.com/chicago/feed |
| Crib Chatter | institution | Business | https://cribchatter.com/feed |
| Eater Chicago | institution | Arts & Culture | https://chicago.eater.com/rss/index.xml |

### Tier 5 — Student Media

| Name | Layer | Beat | RSS |
|---|---|---|---|
| The Chicago Maroon | institution | General News | https://chicagomaroon.com/feed |
| The Daily Northwestern | institution | General News | https://dailynorthwestern.com/feed |
| The DePaulia | institution | General News | https://depauliaonline.com/feed |
| The Loyola Phoenix | institution | General News | https://loyolaphoenix.com/feed |

---

## Not found — manual follow-up candidates

These outlets were checked but no RSS feed was discoverable. Worth a manual check for any that have high editorial value.

**High priority (notable outlets with no feed):**
- Chicago Tribune — paywalled; Tribune Publishing likely stripped public RSS
- Crain's Chicago Business — paywalled; no public feed detected
- CBS 2 Chicago — cbslocal.com URLs now redirect to cbsnews.com/chicago; no feed confirmed
- Axios Chicago — no standalone RSS (Axios uses email-first model)
- CWBChicago — crime/police beat; high-signal but no feed exposed
- The TRiiBE — high-value Black Chicago outlet; no RSS found (may be social-first)
- Chicago Defender — legacy Black press; no feed detected
- City Bureau — no RSS exposed; Documenters content is structured differently
- Cicero Independiente — bilingual outlet; no feed found
- Investigative Project on Race and Equity — no feed found
- Hyde Park Herald — no feed detected

**Lower priority (niche/community):**
- Daily Herald, Lawndale News, Loop North News, Uptown Update, McKinley Park News, Nadig Newspapers, eNews Park Forest, Northwest Herald, Irish American News, West of the I, Final Call News, TimeOut Chicago, The Daily Line, Capitalisnt, Newcity

**Nonprofit / Other no-feeds:**
- Lumpen Magazine, PBS affiliates (CAN TV), Public Narrative, Rebellious Magazine, Substance News, True Star Media, CHIRP Radio, Free Spirit Media, Kartemquin, Invisible Institute, The Lansing Journal, Vocalo, OTV Open Television

---

## Beats needing review

| Outlet | Current beat | Note |
|---|---|---|
| Unraveled | General News | Assign once editorial focus confirmed — appears to be press freedom / investigative |
| In These Times | Labor / Politics | "Labor / Politics" is not in existing beat filter chips — may need adding or remapping to existing beat |
| Environment / Climate | (new beat) | "350 Chicago" uses this beat — not currently in the scatter plot beat list or filter chips; flag for UI review |
| Capital B Gary | Black Chicago / Community | URL used is capitalbnews.org/feed (national feed) — may include non-Chicago content; consider filtering |

---

## Code changes made (Phase B)

- **B1** — Added 34 entries to `CHICAGO_FEEDS` (lines ~988–1025). Legacy broadcast outlets tagged `volume:'high'`.
- **B2** — Toggle buttons updated: "Creators" → "Independent Creators", "Institutions" → "Newsrooms & Institutions".
- **B4** — Coverage subhead updated to reflect full ecosystem scope.
- **B3 (volume flag)** — `volume:'high'` added to 7 legacy broadcast/print outlets. `renderBeatGroups()` UI indicator not implemented — optional per brief, deferred pending visual review.

---

## Verification checklist

Run in browser console on Coverage tab:
```javascript
console.log('Total feeds:', CHICAGO_FEEDS.length);
// Expected: 65

const layers = {};
CHICAGO_FEEDS.forEach(f => layers[f.layer] = (layers[f.layer]||0)+1);
console.log('By layer:', layers);
// Expected: {creator: 26, institution: 39}

const beats = {};
CHICAGO_FEEDS.forEach(f => beats[f.beat] = (beats[f.beat]||0)+1);
console.table(beats);
```
