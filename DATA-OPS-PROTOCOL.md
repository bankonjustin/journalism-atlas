# DATA-OPS-PROTOCOL.md
**Independent Journalism Atlas — Data Operations Protocol**
*Current State | Last updated: June 2026*
*Owner: Ryan Kellett (ryan@journalismatlas.com)*

---

## Purpose of this document

This is the authoritative reference for how creator data moves through the Atlas pipeline — from first mention to live in the database. It supersedes all prior handoff notes, Cowork session logs, and earlier pipeline documentation including `atlas-handoff-note.md`, `rejections-passoff.md`, and any `proposals.csv`-era references.

For planned future expansions to the schema and pipeline, see `DATA-ROADMAP.md` (location below). This document covers only what is currently operational.

---

## Reference doc locations (updated July 7, 2026 — private repo setup)

**Correction to the July 7 filesystem-audit note that used to live here:** these docs are no longer in `~/Downloads/`. They've moved into a new private repo, `journalism-atlas-private` (github.com/bankonjustin/journalism-atlas-private — access: Justin, Ryan, Liz, James). Rationale: real version history worth tracking, but content (named individuals, internal editorial judgment, private contact data) inappropriate for this public repo. Full context: `Atlas Spidering/sessions/PASSOFF_FILESYSTEM_AUDIT_JUL2026.md` and the private repo's own `README.md`.

| Doc | Actual location |
|---|---|
| `ATLAS-EDITORIAL-STANDARDS.md` | `journalism-atlas-private/docs/ATLAS-EDITORIAL-STANDARDS-v1.4.md`. A maintained mirror also exists at `~/Downloads/ATLAS-EDITORIAL-STANDARDS-v1_4.md` **solely** because `liz-editorial.md` (Atlas Spidering workspace) hardcodes that path as a read-only tool scope — that mirror must be updated by hand whenever this doc's version bumps, until `liz-editorial.md` is repointed directly (flagged, not yet done — requires sign-off per the out-of-scope rule on that file). |
| `REJECTION_GUIDE.md` | `journalism-atlas-private/docs/REJECTION_GUIDE-v1.0.md` |
| `DATA-ROADMAP.md` | `journalism-atlas-private/docs/DATA-ROADMAP-v1.0.md` |
| `atlas-private-columns.csv` | `journalism-atlas-private/data/atlas-private-columns.csv` — **this is now the live file.** Ryan edits it there directly; see the private repo's `HANDOFF.md`. The old `~/Downloads/` copies are archived, not live. |

**Naming convention (standing rule, adopted July 7, 2026):** `DOCNAME-vX.Y.md`, version bumps require a changelog entry inside the doc, and no parenthetical duplicate filenames (`(1)`, `(2)`) ever — archive or delete a duplicate on sight. This supersedes the unversioned-filename convention this section recommended earlier the same day; Justin's call, adopted going forward for all docs in the private repo.

---

## Current state (June 2026)

- **Master CSV:** 1,718 rows, zero duplicate slugs (June 2026 — 24 creators appended from the June human review batch; bsky enrichment pass completed June 18)
- **Schema:** 19 public columns (18 original + `partner_lists`, added May 2026). ⚠️ Note: the working master file in active use (`atlasmaster_june23_bsky_enriched.csv` lineage) is currently carrying 18 columns — `Partner Lists` is not yet present in that file. Re-add the column at the next Final Clean so the file matches the documented 19-column schema before sending to Justin.
- **Private columns:** `atlas-private-columns.csv` at 1,602 rows after the June batch. Must be brought to parity with master (1,718) — see Step 4 private columns sync.
- **Staging:** `proposals.csv` is retired — [Intake Queue Google Sheet](https://docs.google.com/spreadsheets/d/1Fve8IJp6jvilXNdcN2MOBrjmqTFMAvR3/edit?usp=sharing) is now the staging layer
- **Rejections:** [Rejections Google Sheet](https://docs.google.com/spreadsheets/d/1tvoG2IXB9K07WYQpgmKYOlRFPwPq6I52/edit?usp=sharing) is canonical — replaces `pipeline/rejections.csv`
- **Shadow Lists:** [Shadow Lists Google Sheet](https://docs.google.com/spreadsheets/d/1I9qKTGetIArHob_XGMweKn8rkFPBTm6c/edit?usp=sharing) — managed by Justin
- **Live site:** journalismatlas.com

> ⚠️ **Known script issue:** `atlas_groups.py` and `atlas_append.py` still use the old form `"Science, Health & Environment"` (with comma). The master CSV uses the correct form `"Science Health & Environment"` (no comma). Do NOT run group normalization until these scripts are updated. Justin owns this fix.

---

## The team

| Person | Role in pipeline |
|---|---|
| Ryan | Data owner. All editorial calls, pipeline runs, CSV delivery to Justin. |
| Justin | Site code, deploy, pipeline scripts, Atlas Pulse. Delivers spidering batches. |
| Liz | Reviewer. Co-reviews proposals; can approve/reject. Owns description editorial standard. |
| Anna | Reviewer (part-time). |
| Claude (Chat) | Assists Ryan with research, enrichment, and review during Data Fill. Assists with drafting documents. |
| Claude (Code) | Justin's environment. Runs pipeline scripts, spidering, Pulse. Does not touch master CSV without explicit instruction. |

**Core rule:** Claude never auto-deletes or auto-reclassifies rows without Ryan's approval. Flag; Ryan decides.

---

## The pipeline at a glance

```
Pre-Intake Sources
  Slack / Spidering (Justin) / Contact Form / Partner Lists
          ↓
    Data Fill (Ryan + Claude Chat)
  Dedup · Light enrichment · Auto-reject obvious failures
          ↓
    Intake Queue (Google Sheet)
  Shared: Ryan, Liz, Anna, Justin
  Decisions: Approved / Rejected / Shadow List / Hold
          ↓
    Human Approval + Data Enrichment
  Three-question test · Full 19-column fill · Private data collected
  Rejections logged · Shadow list routed · Methodology documented
          ↓
    Final Clean (Ryan)
  Private data split · Partner CSVs generated · Schema validation
          ↓
    Append to Master
  Full CSV sent to Justin via Slack · Justin runs pipeline + deploy
  Justin sends confirmation .md back to Ryan
          ↓
    Atlas Pulse picks up new feeds automatically
```

---

## Step 0: Pre-intake sources

Names arrive from four channels. No vetting happens here — this is raw intake only.

| Source | Format | Notes |
|---|---|---|
| **`#atlas-add-to-list` (Slack)** | URL, name + URL, screenshot, or name only | Dedicated drop channel. Team-only: Ryan, Liz, Justin, Anna. Pulled weekly by Claude. See subsection below. |
| **Spidering (Justin)** | .xlsx or .csv | Structured batches with Name, URL, Beat, Verdict (YES/MAYBE/VERIFY), Source Anchor, Notes. Justin's `process_recs.py` pre-dedupes against master + rejections before delivery. |
| **Contact form (journalismatlas.com)** | Google Sheet | Creator self-submission, third-party tip, correction request, or feedback. Lands in the [Contact Form Responses Sheet](https://docs.google.com/spreadsheets/d/1gG-2DgBeM8O8MWgQn1qeRi7PB25E-mHnJY-OJ4QmFTk/edit). Pulled by Claude on the same cadence as Slack. See subsection below. |
| **Partner org / curator list** | Spreadsheet or CSV | External batch from a partner (e.g. ICFJ, ONA cohort). Non-standard columns likely. Treated as its own batch; origin tracked in `partner_lists` column. |

**Key rule:** Nothing enters the intake queue without going through Data Fill first. No manual additions directly to the Google Sheet.

---

### `#atlas-add-to-list` — Slack channel intake

**Channel:** `#atlas-add-to-list` (private, team-only: Ryan, Liz, Justin, Anna)

**Purpose:** A dedicated drop zone for creator suggestions from anywhere the team encounters them — conferences, LinkedIn posts, other newsletters, direct referrals. No vetting happens in the channel. It is raw intake only, identical in pipeline status to other pre-intake sources.

**Cadence:** Claude reads the channel weekly and presents a parsed candidate list to Ryan before taking any action. Claude does not add anything to the Intake Queue or the master CSV without Ryan's explicit go-ahead after reviewing the list.

**What gets posted and how Claude handles it:**

| Format | Example | How Claude handles it |
|---|---|---|
| Plain URL | `https://ashevegashotsheet.substack.com/` | Treat URL as the primary link; infer creator name and platform from the domain |
| URL + context note | `https://instagram.com/p/XYZ` + "Lynne from the Chicago event" | Use the note as a name hint; resolve the URL to the creator's profile (not the individual post) as the primary link |
| Screenshot | LinkedIn post showing newsletter creator | Read the image; identify the creator being proposed — which may be the poster's own profile, a creator featured in the post, a recommendation in the caption, or a list of names. See screenshot handling below. |
| Name only (no URL) | "We should add John Smith" | Flag to Ryan — insufficient for Data Fill without a primary link; hold until Ryan supplies a URL |

**Screenshot handling:**

> ⚠️ **API limitation:** The Slack API does not return image file contents — only metadata. Ryan must manually copy screenshots from `#atlas-add-to-list` into the Claude Chat session for Claude to read them. This is a required manual step before Claude can process any screenshot-based submission.

The poster of a screenshot is rarely the creator being proposed. The referenced creator may be visible in a profile view, named in a caption, featured in a post someone else shared, or part of a list. Claude reads the image and identifies the most plausible candidate(s).

- **If the intent is clear** (e.g., a newsletter's homepage is visible, or a single named creator is obviously the subject): Claude proceeds directly with that creator and states its interpretation.
- **If the intent is ambiguous** (e.g., a social post mentioning multiple creators, a screenshot of a recommendation thread, a conference slide with a list of names): Claude presents Ryan with numbered options before proceeding. Example:

  > "This screenshot could be proposing: (1) Amy Bushatz / Mat-Su Sentinel — the creator featured in the LinkedIn post; (2) Dan Oshinsky — the LinkedIn poster who shared the story. My read is (1). Confirm or redirect?"

Ryan selects before Claude runs Data Fill on any screenshot candidate.

**Weekly pull — Claude's output to Ryan:**

Claude reads all messages in `#atlas-add-to-list` since the last pull timestamp, parses them into candidates, and presents the following summary before doing anything else:

```
#atlas-add-to-list — week of [date]
[N] candidates from [N] messages

1. Ashevegas Hot Sheet
   URL: https://ashevegashotsheet.substack.com/
   Posted by: Liz | Format: plain URL | Platform: Newsletter - Substack

2. Lynne [last name unknown]
   URL: https://instagram.com/[profile to resolve]
   Posted by: Justin | Note: "from the Chicago event" | Needs: profile URL resolution

3. Amy Bushatz / Mat-Su Sentinel
   URL: [to look up]
   Posted by: Ryan | Format: screenshot (LinkedIn post) | Interpretation: creator featured in post
   ⚠️ Screenshot was manually provided by Ryan — confirm this interpretation before proceeding

Proceed with Data Fill on all, some, or let me know which to skip.
```

Ryan confirms — all, a subset, or with edits — before Claude runs Data Fill on any candidate. This is a hard stop; Claude does not proceed speculatively.

---

### Contact Form (Atlas website) — Google Sheet intake

**Source:** [Contact Form Responses Sheet](https://docs.google.com/spreadsheets/d/1gG-2DgBeM8O8MWgQn1qeRi7PB25E-mHnJY-OJ4QmFTk/edit) — the responses sheet behind the contact form on journalismatlas.com. Owned by Ryan.

**Purpose:** Public-facing intake. Anyone on the web can submit a creator (themselves or someone else), request a correction to an existing entry, or leave general feedback. This is raw intake only — identical in pipeline status to Slack and spidering. Nothing enters the intake queue without going through Data Fill first.

**Cadence:** Claude reads the sheet on the same cadence as the Slack channel and presents a parsed candidate list to Ryan before taking any action. Claude does not add anything to the Intake Queue or the master without Ryan's explicit go-ahead.

**⚠️ Branched form structure:** The form is multi-path, and the column layout shifts depending on which path the submitter chose. The `I want to:` column is the router. Claude must read that column first to know how to interpret the rest of the row. The paths are:

| `I want to:` value | What it is | How Claude handles it |
|---|---|---|
| **Submit myself to join The Atlas** | Creator self-submission | New candidate. Fields: name, channel name, primary URL, topics, location, email. Run dedup + Data Fill. |
| **Submit someone else I know to join The Atlas** | Third-party tip | New candidate. Fields: creator name, channel, URL, submitter's relationship, submitter email. Run dedup + Data Fill. |
| **Update or correct my entry in The Atlas** | Correction request | NOT a new row. Match to existing master row by name/URL; surface the requested change to Ryan as an edit, not an intake. |
| **Leave other feedback** | General feedback | Not intake. Summarize for Ryan; no pipeline action. |

Because the columns are offset per path, do not read the sheet positionally across all rows. Parse each row according to its `I want to:` value. When in doubt about which path a row belongs to or which creator a correction refers to, present numbered options to Ryan rather than guessing (same rule as screenshot handling).

**Correction requests are a distinct workflow.** A row asking to fix an existing entry (wrong geography, name spelling, platform change, topic tags) is an edit to master, not a new intake. These bypass the intake queue entirely — Ryan applies the correction directly to the master at the next Final Clean. Claude surfaces them in the weekly pull under a separate "Corrections" heading so they don't get mixed in with new candidates.

**Weekly pull output** mirrors the Slack format, segmented by path:

```
Contact Form — week of [date]
[N] new candidates · [N] corrections · [N] feedback items

NEW CANDIDATES
1. [Creator] — [URL] — submitted by [self / name]
   ...

CORRECTIONS (route to Ryan, not intake queue)
1. [Creator] — requested change: [summary] — matches master row [slug]?

FEEDBACK (no pipeline action)
1. [summary]

Proceed with Data Fill on the new candidates? Corrections and feedback are listed for your review.
```

---

## Step 1: Data Fill

**Trigger:** On-demand, triggered by batch size or Ryan's availability. Not a fixed day. Future: cron automation.

**Who:** Ryan, assisted by Claude Chat.

**Purpose:** Thin, fast enrichment pass to make rows review-ready. This is not full schema fill — that happens at human review.

### Dedup check (run in this order)

1. Check against master CSV by URL (normalized) and name
2. Check against Rejections Google Sheet by name (case-insensitive)
3. Check against partner list CSVs

Redundancy is intentional — Justin pre-dedupes spidering output, but duplication is the most common error in the pipeline. Checking twice catches what slips through.

### Light enrichment per row

- Verify name spelling
- Confirm primary link resolves (HTTP 200)
- Identify platform (from URL domain)
- Assign one topic/beat
- Note obvious geography if visible from bio or site
- Write one-sentence description

Do not fill geo splits or Groups at this stage. **Do** identify and order all platforms per the Platform Assignment Rules below — platform structure is cheaper to get right once, with the creator's profile open, than to reconstruct later at review. Leave a platform slot blank rather than guess; a blank is a signal to the reviewer, a wrong entry is not.

### Platform Assignment Rules

**Primary platform** is the creator's owned or monetized home — the place where they have a direct relationship with their audience. In order of precedence:

1. A newsletter (Substack, Beehiiv, Ghost, etc.)
2. An owned website or independent publication
3. A monetization hub (Patreon, membership, paid subscription)
4. Only if none of the above exist: the social platform with the largest following

Most creators point their social channels *toward* one of these owned spaces. That destination is the primary, even when a social account has somewhat more followers. Record the owned/monetized home as Platform Primary.

**Large-scale-gap override:** when a social account dwarfs the owned/monetized home in audience — roughly a 10x+ difference (e.g., 2K newsletter vs. 200K TikTok) — the social account becomes Primary instead. At that scale the social platform is where the audience actually knows the creator, and recording the small newsletter as primary would misrepresent the relationship. Below that gap, the owned home wins.

**Platforms 2, 3, 4** are ranked by **size × activity**:

- Start with follower/subscriber count as the baseline ordering.
- Adjust upward for posting frequency. A smaller platform the creator posts to daily ranks above a larger platform they post to rarely. Active engagement outranks raw audience size.
- A platform that meets the activity threshold (below) but is clearly secondary in both size and cadence goes in the lowest available slot.

**Activity threshold for listing a platform at all:** the creator must have posted on that platform within the **last four months**. A platform with no post in four months is not listed, even if the account exists and the link resolves. (This matches the `inactive` rejection threshold and keeps dead weight out of the card.)

### Finding a creator's full platform footprint

Rather than fetching each egress-blocked platform directly (Substack, Beehiiv, Instagram), resolve the creator's **link aggregator or profile bio**, which lists every place they publish:

- Check for a Linktree, Beacons, Stan, or similar link-in-bio page.
- Check the "links" or bio section of the primary platform's profile.
- Check the footer/about page of an owned website.

These pages are the single most reliable source for the complete, current platform list — and they sidestep the scraping blocks, because the aggregator itself is usually fetchable even when the destination platforms are not. Treat the link-in-bio as the source of truth for *which* platforms exist; apply the size×activity rules above to *order* them.

**Run this on every row.** Link-in-bio resolution is a required Data Fill step, not an optional one — it's what makes the platform footprint accurate rather than inferred. If it proves too slow at batch scale, do not silently drop it: flag the time cost to Ryan and revise this protocol to scope it down (e.g., required only for bare social-handle submissions).

### Auto-reject at Data Fill (skip; log to rejections sheet)

Flag and remove — do not add to intake queue:

| Signal | Action |
|---|---|
| Primary URL is dead/404 **and** no current home can be found via search or link-in-bio | Reject: `insufficient` — note "no live presence" |
| Primary URL is dead/404 **but** creator has moved to a new home (found via search/link-in-bio) | Update the URL to the new home; do not reject. Note the migration. |
| Creator is reachable but has not posted anywhere in 4+ months, with no "I've stopped" notice | Reject: `inactive` — note last-seen date. Applies even when this is the creator's only active platform: a 4-month silence moves the whole row to rejection, not just a thinner platform list. |
| Creator is active but their real home is a different platform than submitted | Re-assign per Platform Assignment Rules; submitted URL may become Platform 2+ or drop off entirely |
| Obvious multi-staff org, no named individual creator | Reject: `scope` — note "org rule" |
| Already in master CSV | Reject: `duplicate` |
| Already in rejections sheet | Skip — no new entry needed |
| Already in a partner list CSV | Reject: `duplicate` |
| Cannot identify who this creator is from others with same name | Reject: `insufficient` |

### Output

Cleaned rows added to the Intake Queue Google Sheet with: Name, URL, Platform, Beat/Topic, Geography (rough), one-sentence description, Source, Spidering Verdict (if from Justin).

---

## Step 2: Intake Queue (Google Sheet)

The intake queue is a shared Google Sheet. It is the only staging layer between pre-intake and approval. `proposals.csv` is retired.

**Access:** Ryan, Liz, Anna, Justin — all with edit permissions.

### Column structure

| Column | Notes |
|---|---|
| Creator Name | As submitted; Ryan verifies spelling at Data Fill |
| URL | Primary link, confirmed resolving |
| Platform Primary | From URL domain |
| Beat / Topic | One value from Atlas taxonomy |
| Geography | Rough — city or country |
| One-sentence description | Written at Data Fill |
| Source / Origin | Which channel or batch |
| Spidering Verdict | YES / MAYBE / VERIFY (if from Justin); blank otherwise |
| Decision | **Approved / Rejected / Shadow List / Hold** |
| Reason Code | Required if Rejected or Shadow List |
| Reviewer | Who made the decision |
| Notes | Free text; edge case context |
| (All 19 schema fields) | Reviewers complete these for approved rows |

**Reviewer role:** Reviewers fill in and edit all fields, including correcting prefilled data from Data Fill. Prefill is a starting point, not final. Decision is set only after schema fields are complete.

### Decision values

- **Approved** — passes three-question test; all fields complete; ready for final clean
- **Rejected** — fails qualification; reason code required; move to Rejections Sheet
- **Shadow List** — not an individual creator but worth tracking (co-op, indie outlet, named-founder org); move to Shadow Lists Sheet
- **Hold** — needs more information; stays in queue with a note (e.g. "verify cadence," "pre-launch," "affiliation unclear")

---

## Step 3: Human approval + data enrichment

For every row reaching decision, reviewers apply the five-question qualification test and complete the full schema.

### Multi-reviewer vote workflow (current practice)

For batches that contain edge cases or any entry where qualification is not obvious, decisions are made by a three-reviewer vote rather than a single reviewer's call. This is the workflow used in the June 2026 batch.

- Claude prepares a review vote file with one entry per creator. Each entry includes Claude's own original determination and reasoning so reviewer agreement and disagreement (Human Overrides — see Step 3 methodology) are visible.
- The three reviewers — Ryan, Justin, Liz — each vote independently: **YES** (add to Atlas) · **NO** (do not add) · **SHADOW** (route to Shadow Lists).
- Each reviewer returns a completed copy as `HUMAN_REVIEW_VOTE_[name].md`. Claude tabulates.
- **Majority of three determines the outcome. Ties go to Ryan.**
- A reviewer's vote can arrive after the initial tabulation. Decisions already at 2-0 are provisional but hold unless the late reviewer actively flips one. (In the June 2026 batch, Liz had not voted at tabulation time; Ryan + Justin formed a majority on every entry, so all decisions held pending her input.)
- Clean, obvious adds and obvious rejections do not require the full three-reviewer vote — they can be handled in the normal single-pass review. The vote workflow is for batches with genuine edge cases.

> **⚠️ PROPOSED CHANGE — NOT YET ACTIVE.** The team is considering revising the human-review process. This is documented here so it is easy to switch on once agreed, but **the current workflow above remains in force until Ryan confirms the change.** When the team is ready, replace the "Multi-reviewer vote workflow" section above with the agreed new process and note the change in the version/standing-reminders log. Do not adopt any new review process speculatively — confirm with Ryan first. *(Placeholder for the specifics of the proposed change — to be filled in when the team aligns.)*

### Qualification

See **`ATLAS-EDITORIAL-STANDARDS.md`** for the complete qualification framework — the five-question test, all named rules, edge case precedents, and the Shadow Lists boundary. The protocol does not duplicate that content here.

Quick reference: a creator must be (1) independent, (2) have an identifiable content product, (3) making a significant professional effort, (4) doing work that advances information or understanding, and (5) credibly and ethically produced. All five must be satisfied.

For reason code definitions and the `scope` vs `not-journalism` distinction, see **`REJECTION_GUIDE.md`**.

### Full schema fill (approved rows)

Complete all 19 public columns:

```
Creator Name · slug · Creator Channel · Link Primary ·
Platform Primary · Platform 2 Name · Platform 2 Link ·
Platform 3 Name · Platform 3 Link · Platform 4 Name · Platform 4 Link ·
Topic/Category · Geography · Groups · Geo City · Geo State ·
Geo Country · Geo Region · Partner Lists
```

Also collect private fields (kept separate from public master):
- `contact_email`
- `notes`
- `origin_list`

> ⚠️ Private fields are NEVER written into the public master CSV. They are stored separately and joined by slug.

### Partner list field

The `partner_lists` column (column 19) is pipe-delimited. If a creator comes from a partner org batch, record the partner name here. Example: `ICFJ|ONA Cohort 26`. The creator also appears in the relevant partner CSV that Justin uses to build the partner page.

### Rejection logging

For rejected rows, add to the Rejections Google Sheet:

| Field | Notes |
|---|---|
| Creator Name | As submitted |
| Reason Code | `legacy` / `inactive` / `duplicate` / `not-journalism` / `scope` / `insufficient` / `other` |
| Reason Description | Human-readable version |
| Note | Freeform — why specifically |
| URL Reviewed | The URL that informed the decision |
| Date Rejected | ISO date |
| Rejected By | Reviewer name |

**Reason code guidance:**

- `legacy` — staff at traditional/institutional outlet; not independent
- `inactive` — no posts within ~4 months
- `duplicate` — already in master or on a partner list
- `not-journalism` — content is not journalism-adjacent (lifestyle, brand, commerce)
- `scope` — real journalist but not a creator-journalist in the Atlas sense (e.g. wire reporter, journalism educator without their own channel)
- `insufficient` — too early-stage, unverifiable, or pre-launch
- `other` — catch-all; always include a detailed note (e.g. deceased)

**`scope` vs `not-journalism`:** `scope` = real journalist, wrong model for Atlas. `not-journalism` = content itself fails the journalism-adjacent test.

**Rejection is not permanent.** If a creator's situation changes (e.g. legacy journalist goes independent, academic launches consistent new channel), remove the rejection entry and run them through the pipeline fresh.

### Shadow list routing

Entries marked Shadow List go to the Shadow Lists Google Sheet, managed by Justin. Minimum fields: outlet name, named creator(s), URL, category, brief description.

Categories: `co-op` (worker-owned newsrooms) · `indie-outlet` (founder-led newsrooms with staff) · `named-founder-org` (org-rejections where founder may qualify individually).

### Methodology documentation

Routine rejection notes stay in the Rejections Sheet only. Edge cases that set precedent or establish a new rule are:
1. Added as a named rule to `ATLAS-EDITORIAL-STANDARDS.md`
2. Documented as a `.md` case study file in `case-studies/`

The Editorial Standards document is versioned when rules change. The protocol does not need to change when editorial rules change.

### Human Override tracking

When a human reviewer decision conflicts with Claude's original determination (Claude said NO/HOLD/SHADOW, humans voted the creator IN — or vice versa), that disagreement is a signal, not just a one-off. It means Claude's judgment and the team's actual standards are out of alignment on some category, and the gap should be closed so the judgment improves over time.

**The rule:** After any review session, scan for Human Overrides. For each one, ask whether it reveals a pattern that should change how Claude judges future candidates. If yes, propose a new or revised named rule in `ATLAS-EDITORIAL-STANDARDS.md`.

**What counts as a Human Override:**
- Claude pre-judged `not-journalism` / `scope` / reject, humans voted YES
- Claude recommended HOLD, humans voted YES (or NO)
- Claude recommended SHADOW, humans voted YES for the main Atlas (or vice versa)

**How to track:**
- In the review vote file, Claude's original determination is recorded alongside each entry so overrides are visible at tabulation.
- At session close, Claude lists the overrides and flags any that cluster into a pattern (e.g. "five food/local-guide entries Claude bounced as `not-journalism` were all voted in").
- A clustered pattern becomes a proposed named rule. A genuinely one-off override becomes a case study, not a rule change (never revise a rule to fit a single unusual case).

**Precedent:** The June 2026 batch produced 13 Human Overrides. The clustered pattern — food, local-guide, and entrepreneurship content that Claude filtered too strictly on criterion 4 — became **Rule 10 (journalism-adjacency breadth standard)** in Editorial Standards v1.3. The Virgil Texas co-host override became **Rule 11 (co-host policy)**. This is the workflow working as intended: surface the disagreement, find the pattern, codify it, improve future judgment.

---

## Step 4: Final clean

**Trigger:** Manual, on same on-demand cadence as Data Fill. Ryan exports approved rows from the intake queue sheet.

### Tasks

**Private data split:** Remove `contact_email`, `notes`, `origin_list` from the public output. Store separately, joined by slug.

**Private columns sync (REQUIRED — never skip):** Any time a new master is printed, `atlas-private-columns.csv` must be updated in the same pass so the two files never diverge. The private file must have exactly one row per master slug. **As of July 7, 2026, this file lives in the `journalism-atlas-private` repo** (`data/atlas-private-columns.csv`) — edit and commit it there directly, not in a local Downloads copy. See that repo's `HANDOFF.md`.

- For every newly appended creator, add a stub row to `atlas-private-columns.csv`: `slug | Creator Name | Special Lists | Notes | Contact | Origin List`.
- `slug` is the join key and must match the master slug exactly.
- The `Notes` field should capture any editorial context from the review session — vote outcome, any reviewer override of Claude's pre-judgment, flags to monitor, and URL corrections made during intake.
- `Contact` and `Origin List` are populated from the private fields collected at Step 3; leave blank if not available rather than guessing.
- After updating, verify: private row count equals master row count, and there are no duplicate slugs and no orphan slugs (a private slug with no matching master row, or vice versa).

> This step is the most commonly forgotten one. If a master is sent to Justin without the matching private columns update, the private file silently falls behind and every future join breaks for the missing rows. Treat "print master → update private columns" as a single inseparable action.

**Master-CSV snapshot (REQUIRED, added July 7, 2026):** Every time a new master CSV is printed for send-off, copy it — dated, unmodified — into `journalism-atlas-private/data/snapshots/creators-master-YYYYMMDD.csv` (private repo, same access as the private columns file above). This is the only version history the master CSV has; there was previously no formal mechanism for this, only ad hoc dated backup copies accumulating loose in `~/Downloads/` and in this repo's own `assets/data/` (`creators-master-backup-*.csv` — flagged separately, not yet cleaned up as of this writing). Trigger: same moment the private columns sync happens, so a Final Clean produces exactly one snapshot, one private-columns update, and one master send-off together.

**Partner CSV generation:** For any creator flagged in `partner_lists`: generate a separate partner CSV matching the 19-column master schema. The creator appears in both master and the partner CSV.

**Schema validation before sending:**

- All 19 public columns present and in correct order
- No private columns in public output
- No duplicate slugs
- Platform vocab is controlled (see SCHEMA-VOCAB.md)
- Geo fields properly split (City / State / Country / Region)
- Groups values use `Science Health & Environment` (no comma)
- `partner_lists` values are pipe-delimited with consistent partner name spelling
- Geo Country uses two-letter ISO codes; `US` not `USA`
- `atlas-private-columns.csv` row count equals master row count; no duplicate or orphan slugs (private columns sync was completed)

### Output

Full master CSV print — not just new rows. Ryan sends the complete updated master (and any partner CSVs) to Justin via Slack.

---

## Step 5: Append to master + deploy

**Ryan → Justin:** Full master CSV + partner CSVs via Slack.

**Justin runs:**
```
normalize → groups → slug → verify → platform cleanup
→ node convert.js → site rebuild
```

Justin checks for duplicate slugs and schema issues before deploy.

> ⚠️ Justin must fix `atlas_groups.py` and `atlas_append.py` to use `"Science Health & Environment"` (no comma) before running group normalization on any append.

**Justin → Ryan:** Confirmation `.md` back to Ryan after deploy:
- Row count before and after
- Any rows skipped and why
- Live URL confirmed

Ryan uses this confirmation to track what is actually live until GitHub access is set up.

**Atlas Pulse:** New creators' RSS feeds are picked up automatically on the next Pulse run. No manual step required. Dark creator feed fixes (broken Link Primary URLs) are corrected by Ryan in the master CSV; Pulse picks up the fix on the next rebuild.

---

## The 19-column public schema

Exact column headers in order:

```
Creator Name | slug | Creator Channel | Link Primary |
Platform Primary | Platform 2 Name | Platform 2 Link |
Platform 3 Name | Platform 3 Link | Platform 4 Name | Platform 4 Link |
Topic/Category | Geography | Groups |
Geo City | Geo State | Geo Country | Geo Region |
Partner Lists
```

Column 19 (`Partner Lists`) was added May 2026. Pipe-delimited. Empty string if creator is not on any partner list.

---

## Controlled vocabularies

### Platform Primary (and Platform 2–4 Name)

```
Newsletter - Substack          Video - YouTube
Newsletter - Beehiiv           Video - Instagram
Newsletter - Ghost             Video - TikTok
Newsletter - Buttondown        Video - Twitch
Newsletter - Other
Podcast                        Social - Twitter / X
Website                        Social - BlueSky
Patreon                        Social - LinkedIn
Chat - SMS                     Social - Facebook
                               Social - Instagram
                               Social - Threads
                               Social - TikTok
```

Common corrections: `Blog` → `Website` · `Substack` → `Newsletter - Substack` · `YouTube` → `Video - YouTube` · `X` → `Social - Twitter / X` · `Bluesky` → `Social - BlueSky`

### Groups (9 values)

```
Power & Politics
Money & Work
Culture & Media
Science Health & Environment   ← no comma
Social Issues
Civic Life
General News
Journalism Formats
Lifestyle & Personal Life
```

### Geography format

| Type | Format | Example |
|---|---|---|
| US city | `City, ST` | `Chicago, IL` |
| US state only | `State Name - US` | `North Carolina - US` |
| US national | `National - US` | `National - US` |
| Washington DC | `Washington, DC` | `Washington, DC` |
| International city | `City, Country` | `London, UK` |
| International country | Country name | `United Kingdom` |
| Global | `International` | `International` |

Geo Country: two-letter ISO codes. `US` not `USA`.

### Geo Region

`Northeast` · `Midwest` · `South` · `West` · `Mid-Atlantic` (DC specifically) · `National` · `International`

---

## Pipeline scripts reference

All scripts live in `pipeline/`. Run from the repo root using `pipeline/atlas_*.py` except `atlas_append.py`, which must be run from inside `pipeline/`.

```bash
# Append (dry-run first)
python3 pipeline/atlas_append.py atlas-master.csv new_rows.csv --dry-run
python3 pipeline/atlas_append.py atlas-master.csv new_rows.csv

# Normalize
python3 pipeline/atlas_normalize.py atlas-master.csv --dry-run
python3 pipeline/atlas_normalize.py atlas-master.csv --output atlas-master.csv

# Slugs
python3 pipeline/atlas_slug.py generate "Creator Name"
python3 pipeline/atlas_slug.py check atlas-master.csv

# Versioning (auto-runs before any write step)
python3 pipeline/atlas_version.py snapshot atlas-master.csv --label "label"
python3 pipeline/atlas_version.py list atlas-master.csv
python3 pipeline/atlas_version.py rollback atlas-master.csv
```

Snapshots are stored in `.atlas_versions/` as timestamped CSVs. Always snapshot before any write operation.

---

## Google Sheets structure

Three Google Sheets replace the prior local CSV files:

| Sheet | URL | Replaces | Owner |
|---|---|---|---|
| **Intake Queue** | https://docs.google.com/spreadsheets/d/1Fve8IJp6jvilXNdcN2MOBrjmqTFMAvR3/edit?usp=sharing | `proposals.csv` | Ryan (primary), shared with Liz/Anna/Justin |
| **Rejections** | https://docs.google.com/spreadsheets/d/1tvoG2IXB9K07WYQpgmKYOlRFPwPq6I52/edit?usp=sharing | `pipeline/rejections.csv` | Ryan (primary); Justin's Claude reads from this sheet, not a local CSV |
| **Shadow Lists** | https://docs.google.com/spreadsheets/d/1I9qKTGetIArHob_XGMweKn8rkFPBTm6c/edit?usp=sharing | No prior equivalent | Justin (primary) |

Justin: update `process_recs.py` and any spidering dedup logic to read from the Rejections Google Sheet URL above rather than a local `rejections.csv` path. The sheet ID is `1tvoG2IXB9K07WYQpgmKYOlRFPwPq6I52`.

---

## Private data file

Private creator data lives in a local CSV file managed by Ryan. It is intentionally not stored in Google Sheets — the data includes contact emails and internal notes that should not be accessible via a shared link.

**File:** `atlas-private-columns.csv`
**Schema:** `slug | Creator Name | Notes | Contact | Origin List`
**Joined to master by:** `slug`

| Column | What it holds |
|---|---|
| `slug` | Join key — must match master `slug` exactly |
| `Creator Name` | Name (redundant, for readability) |
| `Notes` | Free-text internal notes from Ryan or team |
| `Contact` | Creator's email address |
| `Origin List` | Which intake batch or source the creator came from |

**Rules:**
- Never write any of these columns into the public master CSV
- When the intake queue produces approved rows, private fields (Contact, Notes, Origin List) are collected at Step 3 (Human Approval) and written here, not to master
- The `Special Lists` column from the prior schema is retired — partner list membership now lives in the `partner_lists` column in master
- Revisit moving to Google Sheets when the creator claim system is live and contact data becomes actively managed

**Current state (June 2026):** 1,602 rows after the June human review batch (24 new stubs added). Must be brought to 1,718 to match master at the next Final Clean — see the private columns sync step in Step 4. One row per master slug is the invariant; any divergence means the sync step was skipped.

---

## Known issues and standing reminders

| Issue | Status | Owner |
|---|---|---|
| `atlas_groups.py` and `atlas_append.py` use old comma form `"Science, Health & Environment"` | **Not fixed** — do NOT run group normalization until resolved | Justin |
| `atlas_append.py` must be run from inside `/pipeline/` directory | Standing quirk | — |
| Substack / Beehiiv / Instagram egress-blocked in Cowork | Use web search snippets instead of web fetch for research on these platforms | — |
| 164 dark creators in Atlas Pulse (broken feed URLs) | Primary URLs corrected in master CSV (May 2026). Feed resolution is Justin's Pulse task — not a Ryan pipeline item. | Justin (Pulse) |
| Root-level `rejections.csv` in repo is an empty shell | Ignore — active rejections are in the Rejections Google Sheet | — |
| `atlas_verify_state.json` link cache is currently empty | Will rebuild on first verify run | — |
| Working master is 18 columns — `Partner Lists` (col 19) missing from current file | Re-add at next Final Clean before sending to Justin | Ryan |
| `SCHEMA-VOCAB.md` (cited above under Final Clean schema validation) lives in `Atlas Spidering/core/SCHEMA-VOCAB.md`, a separate untracked workspace — not in this repo | Found during July 7, 2026 filesystem audit. Not fixed — flagging for Ryan/Justin to decide whether it should be copied into this repo or cited by absolute path | Ryan / Justin |
| Private columns at 1,602 vs master 1,718 — sync incomplete | Bring to parity at next Final Clean (private columns sync step) | Ryan |
| Human-review process change under consideration | Documented as a not-yet-active placeholder in Step 3; switch on only after team agrees | Ryan |

---

*This document is maintained by Ryan. Update it when the pipeline changes. If something here is wrong, say so in Slack.*
