# SMARTNEWS-PAGE-BRIEF-v1.0

**Project:** SmartNews × Atlas announcement + creator intake page
**Repo:** journalism-atlas (production site)
**Owner:** Justin · **Design review:** James · **Partner review:** Bernie Davis (SmartNews)
**Target:** A gated page on the live site, close enough to final that James polishes it and Bernie approves it with light edits.

## Changelog

- **v1.0 (Oct 20, 2026)** — First brief. Scoped from the claude.ai prototype (v2), Gmail/Drive correspondence through Oct 19, and Justin's direction: more press-release, more generous to SmartNews, intake/discovery for future pilots, Atlas brand story, James's design principles, gated on the live site.

---

## 1. What we're making and why

SmartNews and the Atlas are launching a pilot that runs independent journalists' coverage of the **2026 midterm elections and their aftermath** inside the SmartNews app. Bernie approved an Atlas page announcing the pilot and the plan to keep signing up independent journalists and creators together.

The page has three jobs, in this order:

1. **Announce it like a news release**, as a joint SmartNews–Atlas announcement that gives SmartNews generous, equal-or-greater space.
2. **Run intake and discovery** for future pilots and opportunities. This is a permanent function, not a launch-week extra. The page should keep working as a sign-up surface after the news is old.
3. **Tell the Atlas story**: who we are, how verification works, why this partnership is the kind of thing the Atlas exists to make possible.

It ships **gated**: live at its real URL, but not linked, not indexed, and behind the site's existing preview gate until Justin flips one switch.

## 2. How we work (non-negotiable)

- Chat scoped this; Code builds it; Justin reviews. Nothing goes external until Justin has seen it.
- **Do not push.** Justin pushes via GitHub Desktop. Never run `git push`.
- **Flag, don't silently reconcile.** If anything in this brief conflicts with the repo, CLAUDE.md, the design tokens or the brand guide, stop and list it in the report. Don't pick a side quietly.
- Single-file HTML, vanilla JS, no build step, no frameworks, per CLAUDE.md.
- Every unconfirmed fact on the page goes in `[BRACKETS]` and in the placeholder list in the report. Don't invent quotes, numbers, dates or titles.

---

## 3. Step 0 — Verify before building

Report each item as FOUND (with path) or NOT FOUND. Do not build until Step 0 is reported.

1. Repo is at `~/Documents/GitHub/journalism-atlas/` (new machine, user `bankids`). Confirm the working tree is clean, or list uncommitted files. Don't touch them.
2. Read `CLAUDE.md` in full. Note anything that conflicts with this brief.
3. **Design source of truth.** Find `DESIGN-TOKENS-v14.md` (expected in `docs/design/`). Confirm `assets/css/variables.css` implements v14, or report the gap. If v14 isn't in the repo, stop and ask; don't fall back to an older tokens file silently.
4. **Brand guide.** Find `ATLAS-BRAND-GUIDE-v3.md`. As of Oct 7 it existed only in `~/Downloads`. If it's still not in the repo, report that, and read it from `~/Downloads` if present. Its copy rules (voice, how we describe ourselves) govern the page copy.
5. **James's design principles.** Find `james-design-principles.md` (or the PDF) in the repo or `docs/design/`. Report its location.
6. **The existing gate.** The Nodes and Networks preview page on journalismatlas.com is gated. Find that page and **report exactly how the gate works**: client-side password, Cloudflare Access, a `_headers` rule, a query-string key, or something else. Also report how it keeps the page out of search (meta robots, `_headers` X-Robots-Tag, sitemap exclusion). This page should reuse that mechanism, not invent a new one.
7. Find `partners/_shell.html`, `assets/js/header.js`, `assets/css/header.css`, `_redirects`, `_headers` (if present), `robots.txt`, `sitemap.xml` (if present).
8. Confirm `/partners/smartnews` is free (no existing file or redirect).
9. Find the prototype reference file. Justin will save it as `docs/briefs/smartnews/reference/smartnews-pilot-prototype-v2.html`. If it's not there, ask him for it before building.
10. Find the SmartNews logo. Use the one embedded in the prototype (sourced from SmartNews's own Midterm Pilot One-Pager). Extract it to `assets/images/partners/smartnews-logo.jpg`. Report its dimensions. If Bernie sends an official SVG later, it replaces this one.
11. Confirm how the site counts creators today (dynamic from `assets/data/creators-data.json`, per CLAUDE.md). **No hardcoded creator counts** on this page. Reuse whatever pattern the homepage uses.

---

## 4. Established facts (verified in Gmail/Drive, Oct 19–20, 2026)

Code can trust these. Copy should still route through `[BRACKETS]` where marked.

**The pilot**
- Joint pilot between SmartNews and TIJA LLC (the Atlas). Covers the 2026 midterm elections and their aftermath. Creator agreements end **Dec. 31, 2026**. Both sides intend to expand in 2027.
- Pieces run in **full text** in SmartNews's **Independent Voices** module on the politics vertical, alongside live election results. SmartNews has said it plans to also feature creators in **For You** and **push notifications**, but placement isn't guaranteed. Say "may also appear."
- Creators publish what they already publish. The feed comes from their own newsletter. Atlas sets up the feed and is the single contact with SmartNews.
- **Free content only.** Nothing paid or paywalled runs without the creator's express OK.
- Non-exclusive. Creators own their work. **Neither SmartNews nor Atlas may use creators' work to train AI.**
- Pieces carry a call to action back to the creator's own publication (custom CTA at Judd Legum's request; SmartNews agreed).
- Atlas passes along the performance data SmartNews shares (impressions, click-throughs). No clean subscriber attribution yet. Don't promise conversion numbers.
- Creators are paid a flat pilot fee. **Do not publish the amount.**
- The page can say there's room for **a few more** political writers in the pilot, and that we're taking applications for **future phases that expand toward other topics**.

**The cohort** (display order is Justin's call; alphabetical by last name is the default)

| Creator | Publication | Status (Oct 20) | Publicity rule |
|---|---|---|---|
| Jonathan Bernstein | [NEWSLETTER NAME] | Signed | Heads-up before naming |
| Chris Cillizza | [NEWSLETTER NAME] (Cheney Road Productions) | Signed | **Prior approval required** (Gia's Oct 14 edit) |
| Gabe Fleisher | Wake Up To Politics | Agreed Oct 19, not yet signed | Heads-up before naming |
| Judd Legum | Popular Information | Signed | Heads-up before naming |
| Tara Palmeri | The Red Letter | Ready to sign, two open questions | Heads-up before naming |

Store the cohort as a data constant (or a small JSON file) with a `status` field. Build a way to hide any creator whose status isn't `confirmed` with one edit. For now set all five to `confirmed` in a **preview** build and note it in the report; Justin will flip any that aren't signed before ungating.

**SmartNews**
- Founded 2012. Global news discovery company, machine learning plus relationships with 3,000+ publisher partners, "millions" of readers. Source: SmartNews's own sponsor text (ONA). Use as the **draft** boilerplate and mark `[CONFIRM WITH SMARTNEWS]`.
- The "4M+ readers a day" figure appears in Atlas outreach emails, not in anything from SmartNews. **Don't use a number** unless Bernie supplies it. Mark `[SMARTNEWS AUDIENCE FIGURE]`.
- Bernie Davis, Head of Media Partnerships, SmartNews.

**People and titles**
- Justin Bank, CEO and co-founder, TIJA LLC / the Independent Journalism Atlas (title per the signed agreements).

## 5. Assumptions to verify (memory-derived; Code confirms before relying on them)

- The gate pattern from Nodes and Networks is reusable for a second page. If it's page-specific, report how to generalize it rather than copy-pasting.
- `header.js` injects the site nav. Confirm whether a gated page should get the normal nav, or a stripped version so the page doesn't advertise the rest of the site to Bernie's colleagues before launch. Default: normal nav.
- `variables.css` already defines the stage/workspace colors and type scale from v14. If v14 introduced anything (new tokens, new type sizes, a different hero size), follow v14, not the older DESIGN-TOKENS.md in the Project.
- Partner pages under `partners/` are curated creator lists. This page is different (an announcement plus intake). Confirm `partners/smartnews.html` is still the right home, or recommend `/smartnews` with a redirect. Flag; don't decide.

---

## 6. Page scope

### URL and file
`partners/smartnews.html` → `https://journalismatlas.com/partners/smartnews` (pending item 5's last check).

### Structure (top to bottom)

Follow James's **surface hierarchy**: dark = stage (headlines, thesis, cohort, CTAs), light = workspace (reading, the form, the details). Don't alternate dark/light without a reason.

1. **Co-brand band (white).** Atlas lockup × SmartNews logo at **equal visual weight**. Neither mark is recolored. Links to both sites.

2. **Hero (dark stage). Lead with SmartNews.**
   - Kicker: `News release, [RELEASE DATE]`
   - Headline, SmartNews named first. Draft: *"SmartNews and the Independent Journalism Atlas bring independent journalists into the SmartNews app"*
   - Deck (2–3 sentences): the midterms and their aftermath; five founding creators by name; a few spots left; future phases on more topics.
   - A What / When / Who strip.
   - Two CTAs: **Apply to join** (to the form) and **Read the announcement** (to the release).

3. **Mirror routing (James's Mirror Principle).** Right under the hero, a short "Why are you here?" row that routes each visitor:
   - *I'm an independent journalist or creator* → form
   - *I want to recommend someone* → form, recommend mode
   - *I'm a reader* → how to find Independent Voices in SmartNews (`[APP STORE LINKS]`)
   - *I'm press or a partner* → media contacts
   One line of context per option (Explanation Principle).

4. **The release (white workspace, editorial column).** Merriweather body at the editorial width. Sidebar: apply button and media contacts.
   - Dateline lede, joint announcement.
   - What readers see in SmartNews and where.
   - Founding cohort paragraph.
   - **SmartNews quote first** (Bernie, `[DRAFT — BERNIE TO APPROVE]`).
   - How the program respects creators (terms from section 4).
   - Atlas quote (Justin, `[DRAFT — JUSTIN TO EDIT]`).
   - "What comes next": 2027 expansion, more creators, more topics; applications open.
   - Reuse the draft quotes from the prototype as the starting text.

5. **"Why SmartNews" (new section, dark or light at Code's judgment, justified in the report).** Give SmartNews real space, not just a boilerplate line: who reads it, how its politics experience works, why a mainstream aggregator audience matters for independents. Draw only on section 4 facts; everything else is a `[SMARTNEWS TO SUPPLY]` slot. Include a slot for an **in-app screenshot of the Independent Voices module** (`[SCREENSHOT FROM SMARTNEWS]`). This is the single strongest visual the page could have.

6. **Founding cohort (dark stage).** The grid from the prototype, built for **double the inventory** (5 now, 10+ later) with no layout change. Each card: name, publication, one-line description, link to their publication. The last card is the open seat ("A few spots open") linking to the form.

7. **Two ways in → three ways in (white).** Intake tracks, each a card:
   - **The election pilot:** open now, a few spots, politics writers.
   - **Future phases:** 2027, expanding toward other topics.
   - **Other opportunities:** stay in the Atlas's pool for future platform partnerships and pilots beyond SmartNews.

   This is where the page becomes permanent discovery infrastructure, not just a launch page.

8. **How it works for creators (white).** The four terms: your writing as it is; you stay in control; no AI training; built to grow your list (CTAs plus data, paid to take part).

9. **The Atlas story (dark stage, short).** Who we are and why this matters, in the brand guide's voice. Human-curated, verified database of independent creator-journalists, organized by beat, platform and geography. Creator count pulled live from `creators-data.json` (no hardcoded number). Verification standards in one plain sentence. Link to the main database. One sentence connecting this pilot to the Atlas's platform-partnership work. Keep it to a few sentences plus one stat. Brevity Principle.

10. **Apply to join (white). The form.** See section 7.

11. **About SmartNews / About the Atlas (white), media contacts, footer.** Standard site footer via the shared component if one exists.

### Copy rules
- Voice and self-description follow `ATLAS-BRAND-GUIDE-v3.md`. Report any line where the prototype copy conflicts with the guide, and use the guide.
- Plainspoken, not aphoristic.
- "The 2026 midterm elections and their aftermath," not "election season."
- Refer to "SmartNews" (one word, capital N). Not "Smart News."
- Sentence case for headings and buttons. No all-caps labels.

---

## 7. Intake form

The form must work as long-term discovery intake, and its fields should map cleanly onto the Atlas pipeline.

### Fields

| Field | Required | Notes |
|---|---|---|
| Mode | Yes | Toggle: *Applying for myself* / *Recommending someone*. Recommend mode relabels fields ("Their name", etc.) and adds "Your name and email" for the recommender. |
| Interested in | Yes | Multi-select: election pilot · future phases (other topics) · other Atlas opportunities |
| Name | Yes | |
| Email | Yes (self mode) | Optional in recommend mode |
| Publication or channel | Yes | |
| Link to your work | Yes | Maps to `Link Primary` |
| Where you publish | Yes | Short list mapped to the Atlas platform vocab (Substack, Beehiiv, Ghost, own site, YouTube, Podcast, TikTok, Other). Code: include the mapping to controlled platform-vocab values in a comment. |
| Main beat | Yes | Short human-friendly list. Code: include a mapping to the controlled Topic/Category vocabulary in a comment, and flag any options that don't map cleanly. |
| Where you're based | No | Free text; maps loosely to Geo fields |
| How often you publish | No | Select: weekly+ / a few times a month / monthly / less. (Feeds the Rule 7 inactivity check at intake.) |
| Anything else | No | |
| Consent | Yes | "The Independent Journalism Atlas and SmartNews can contact me about this program and future opportunities." |
| Hidden | Auto | `submitted_at`, `source=smartnews-page`, `page_version` |

Plus a honeypot field for spam. No CAPTCHA.

### Where submissions go — DECISION FOR JUSTIN (flag in report; build for option A)

- **A. Google Apps Script web app → a Google Sheet** *(recommended).* No new infrastructure, fits the static Cloudflare setup, and Ryan can review rows in a Sheet. Code writes the Apps Script source to `docs/briefs/smartnews/intake-apps-script.gs` with deploy steps. Justin deploys it and pastes the URL into a single `FORM_ENDPOINT` constant.
- B. Cloudflare Pages Function + D1/KV. More robust; new infrastructure. Scope only, don't build.
- C. Third-party embed (Tally/Typeform). Fastest; off-brand and outside the stack. Scope only.

While `FORM_ENDPOINT` is empty, the form runs in **preview mode**: validation works, and the success state says plainly that nothing was sent.

---

## 8. Gate

- Reuse the Nodes and Networks gate (Step 0, item 6).
- Page is **noindex** (meta robots and, if the site uses `_headers`, an X-Robots-Tag rule), excluded from any sitemap, and not linked from nav, homepage or the partners index.
- One clearly named switch ungates it at launch: e.g. `const GATED = true` plus the robots/sitemap changes. List every change needed to ungate as a short checklist in the report.
- If the existing gate is client-side only, say so in the report. That's acceptable for a pre-launch preview of non-secret content, but Justin should know.

---

## 9. Design system and James's principles

Use `variables.css` (v14 tokens) and the shared header/footer. Don't inline token values the stylesheet already defines.

How each principle should show up:

| Principle | On this page |
|---|---|
| Tool | Every section answers "what do I do here?" The form is the tool; everything else routes to it or earns trust for it. |
| Mirror | The "Why are you here?" routing row under the hero. |
| Explanation | Every section opens with one plain sentence on what it is. |
| Surface hierarchy | Dark = hero, cohort, Atlas story. Light = release, tracks, terms, form. Justify any other dark section in the report. |
| Brevity | Release body is the only long text. Every other section is a few sentences. |
| Scale | Cohort grid and track cards handle 2× without redesign. Test with 10 cohort entries. |
| Template | Cohort and tracks render from data. Recommend in the report whether this page should become a reusable "partner announcement" template for future platform partners. |

### Needs James's sign-off (list these in `REVIEW-NOTES-JAMES.md`; build them anyway)
- Co-brand band (white band holding a partner's logo at equal weight).
- Hero headline size, if v14's display size reads too small for a release headline.
- The routing row, the track cards and the cohort grid (new components, unless v14 already defines equivalents).
- Use of Merriweather for the release body and pull quotes.
- Any token value Code had to approximate.

---

## 10. Deliverables

All in the working tree, uncommitted, for Justin to review and push.

1. `partners/smartnews.html`: the gated page.
2. `assets/images/partners/smartnews-logo.jpg`: extracted logo.
3. `docs/briefs/smartnews/intake-apps-script.gs`: Apps Script source, with deploy steps in a header comment.
4. `docs/briefs/smartnews/REVIEW-NOTES-JAMES.md`: design items for James, each with a screenshot reference and the token or principle in question.
5. `docs/briefs/smartnews/REVIEW-CHECKLIST-BERNIE.md`: one page of what Bernie needs to approve or supply (his quote, boilerplate, audience figure, screenshot, logo file, press contact, release date, dateline).
6. `docs/briefs/smartnews/SMARTNEWS-PAGE-REPORT-v1.0.md`: Step 0 results, decisions made, every flag, the full placeholder list, the ungate checklist, and screenshots at 390 px and 1440 px, in light and dark mode.
7. A `LEAVE-OFF-LOG.md` entry. Add open decisions to `START-HERE.md` (see section 12).

## 11. Acceptance criteria

- Page loads at `/partners/smartnews` locally, is gated, and carries noindex.
- SmartNews is named first in the headline and has equal-weight logo placement, a quote, its own section and its own boilerplate.
- Form validates every required field, switches correctly between self and recommend modes, and posts to `FORM_ENDPOINT` when set (test against a request bin or a deployed test script, and report which).
- No hardcoded creator count. No invented facts. Every unconfirmed item is bracketed and listed.
- Cohort hides non-confirmed creators via the status field.
- Passes keyboard-only navigation with visible focus, has labeled inputs, and meets 4.5:1 contrast. Respects reduced motion.
- Works at 390 px with no horizontal scroll.
- Cillizza's card and mentions are flagged in the report as **needing his prior approval** before ungating.

## 12. Out of scope / open decisions (add to START-HERE.md)

- **Pushing:** Justin, via GitHub Desktop.
- **Sending to James or Bernie:** Justin.
- **Form backend:** A, B or C (section 7).
- **Cohort order and status:** Palmeri's two questions (do paywalled pieces count toward five a month; what happens if she falls short), Fleisher's signature, Cillizza's prior approval.
- **Release date and dateline.**
- **Whether this becomes a reusable partner-announcement template.**
- **URL:** `partners/smartnews` vs `/smartnews`.
