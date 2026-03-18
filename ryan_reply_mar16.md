# Atlas Dev Update — For Ryan's Claude
### From Justin | March 16, 2026

---

## Overview

This is a reply to your March 16 data ops update. It covers: answers to your questions, things that have changed on the build/dev side that your Claude instance should know, and a list of open questions we need to think through together — especially around sub-lists and the views framework.

We're going to try to make these inter-workspace markdown exchanges a regular thing. Our Claude instances should be able to talk to each other with enough context to not repeat themselves.

---

## Answers to Your Questions

### Q1: Can Justin update the JSON conversion for the new column structure?
**Yes.** That's queued as the first Claude Code task. Ready to run as soon as we have the restructured CSV. Send it and we'll cut a new conversion pass.

### Q2: Keep or drop the original `Geography` column?
**Keep it in the CSV for now, but we'll likely drop it from the JSON once the structured geo fields are live and tested.** 

Reason: The live site currently reads `geography` as a single field for filtering. Before we retire it, we need to do a full audit of everywhere geography data is consumed — the main site, City Lab prototype pages (DC and Chicago specifically), any visualization modes that use it as a dimension. Plan is: ship new structured fields into the JSON alongside the old one, audit all consumers, then drop the old one once everything's migrated. We'll tell you when it's safe to drop from the CSV entirely.

### Q3: Sub-list format
**We need to design this together — more below.** But the short answer is: the format should map to how we want to surface these on the front end, and we have more use cases than just thematic/partner/manual. City Labs, B2B partner views, cohorts (WaPo Diaspora, philanthropist beat), and funder-facing demos all want versions of this. Let's not design a narrow format we'll immediately outgrow.

### Q4: Chat - SMS, Social - Threads, Patreon as official platform values?
**Add them to the data. Don't surface them in the filter UI yet.**

They'll pass cleanly through the JSON conversion. We'll add them to the filter once we've thought through the secondary platform strategy more broadly — which is one of the things we're actively thinking about on the build side. Speaking of which, see the "Things You Should Know" section below — we're entering a world where secondary platform data gets more important, and we want your pipeline to be ahead of that.

---

## Things Your Claude Should Know (Build/Dev Updates)

### 1. The live JSON schema (what the site actually reads today)

Current fields in `creators-data.json`:
```
name
channel
link
platform
topic
geography
group
```

That's it. `origin`, `notes`, `special_lists` etc. don't currently flow through to the JSON or render on the site. When Ryan's new schema adds fields, they'll need to be explicitly added to the conversion script AND to the rendering logic — they don't appear automatically.

### 2. Groups: primary-only rendering — this is intentional

The site renders only the **first** value in the `group` field for the treemap and sunburst visualizations. We made this decision deliberately after the treemap was fragmenting into 131 combinations instead of clean 9-group buckets.

**What this means for your data work:** When assigning Groups, put the most important / primary group first. The site will only use that one for visualization. Secondary group values are preserved in the data and could be used later (e.g. for profile page display), but right now only the first one counts visually.

This should be documented in your controlled vocabulary going forward: "Group: primary group first. Site renders primary only."

### 3. City Lab pages use the geography field

The DC and Chicago City Lab prototype pages filter on the existing `geography` field. When we migrate to structured geo fields, those pages will need updating too. We're planning a full geography audit before retiring the old field — just flag it so your instance knows the migration isn't instant.

### 4. Airtable migration is still pending

We're still on CSV → JSON as the pipeline. When the Airtable migration happens, the conversion process changes. For now, keep building the CSV pipeline cleanly — new columns you're adding should be designed with Airtable in mind (they'll become Airtable fields eventually), but no action needed yet.

### 5. Secondary platforms are becoming more important

The build side is actively thinking about how to display and filter by secondary platform data. As you add Link Secondary/Tertiary and their paired platform names, know that:
- This data will eventually surface on creator profile pages
- We may want to filter or browse by secondary platform (e.g. "who's also on Threads")
- The multi-platform creator display is a near-term design problem

So design your secondary platform columns with display and filtering in mind, not just data completeness. The more structured (Link + Platform paired per column), the better.

### 6. The "source of discovery" field has strategic value

The `origin` / source field (Ryan's List, Austin DC List, Liz Chicago Cohort, etc.) is currently internal-only. But we're starting to think about whether — and how — to surface it publicly or to partners. This matters for:
- Funder storytelling ("here's how we find creators no one else finds")
- Cohort-based views (WaPo Diaspora as a discoverable list, not just an internal tag)
- Partner credibility (showing Stacker or Apple News where creators come from)

For now, keep populating it consistently. We'll make the display decision on the build side. But know it's not just internal metadata anymore — it's potentially product-facing.

---

## Open Design Questions: Sub-Lists / Views Framework

This is the area we most need your Claude's thinking on. Justin's honest answer: it's still fuzzy, and we think the taxonomy folks should lead the design here rather than the dev side constraining it prematurely.

### The use cases we know exist

We're not designing for one thing. "Sub-lists" is really a family of use cases that might share infrastructure or might not:

1. **City Labs** — geographic subsets (Chicago, DC, Philadelphia). Already exist as prototype pages. Probably public.
2. **Partner deliverables** — filtered views for Chicago Public Media, data feeds for Stacker, demo pages for Knight. Semi-private or unlisted.
3. **Cohorts** — groups defined by shared origin or characteristic: WaPo Diaspora, philanthropist-beat journalists, Lenfest network, AAJA partner list, etc. Could go either way — public or private depending on the cohort.
4. **B2B client views** — custom filtered sets for paying partners (TEGNA, Apple News). Private or access-controlled.
5. **Thematic editorial lists** — "Rising voices in climate," "Best local politics newsletters," etc. Public, curatorially driven.

### Justin's instinct on the display question

Some of this gets layered on top of the public site as filterable tags. Some becomes new URLs (`/lists/wapo-diaspora`, `/city/chicago`). Some only lives in private B2B views that never touch the public site. It's probably a blend — and the right blend depends on the list type, not a single answer.

Which means the most important thing your Claude can do is help us **design a taxonomy of list types** that maps cleanly to display/access patterns. If we know what kind of list something is, we know how it should render and who should see it.

### The core architecture question we need you to help answer

**Is a sub-list a filtered view of the main database, or a separately maintained list of names?**

**Option A — Filter/tag layer:** Sub-lists are tags in the main CSV. "WaPo Diaspora" = a value in a `cohort` or `list_tag` field. The site renders filtered views. No separate file. Simple, but only works if every list criterion can be expressed as a field in the main data.

**Option B — Separate reference CSV:** A sub-list is its own file that references creators by name and adds list-specific metadata (list name, type, display order, notes). The site joins on name. More flexible, but creates a sync problem when creators get renamed or updated.

**Option C — Hybrid:** Tags in the main CSV for simple filter-based lists; separate reference files for ordered or editorially curated lists where sequence and list-specific metadata matter.

We don't have a strong answer. We think Option C is probably right but want your Claude to pressure-test it from the data side before we build toward it.

### Questions for your Claude to work through

1. **On the rejection tracker** — do you ever want this surfaced publicly ("we reviewed and didn't include X because Y") or is it always internal? This affects whether exclusion data needs a display-safe format.

2. **On the Language column** — is this primarily a filter dimension (users find Spanish-language creators) or a data completeness field (we know our English/non-English breakdown)? The answer changes how prominently it surfaces in the UI.

3. **On multi-effort creators** — one row per publication or one row per person with multiple links? Big implications for how City Labs count creators and how profile pages work.

4. **On origin/source data** — how much should users see about how a creator was found? Justin's answer: depends on the list type. A partner co-branded list should probably surface the partner name. An internal spidering session probably shouldn't. But we'd love your Claude's taxonomy thinking here — what are the categories of origin and what's the right public/private split for each?

5. **On the geography retirement question** — when we migrate from the freeform `geography` field to structured `geoCity`/`geoState`/`geoCountry`/`geoRegion` fields, what's your appetite for a parallel-fields transition period vs. a clean cutover? We can support either on the dev side but want to know what's less risky for your pipeline.

---

## What We're Building Next (So You Know What's Coming)

Things on the dev side that will create new data requirements:

- **Creator profile pages** — individual URLs per creator. Will surface all platform links, trust signals, beat/geo metadata. Your secondary links and structured geo fields will render here.
- **Geo filter upgrade** — once structured fields are in JSON, we'll build city/state/country drill-down filtering. The `geoCity` field is the key dimension.
- **Sub-list pages** — once we've designed the format together (see above), we'll build the front-end infrastructure to render them.
- **Trust framework v0.1** — Liz owns the standards side; we'll render Green/Yellow/Red signals on profiles when that's ready. No data changes needed from you yet.

---

## New Initiative: Atlas Partner Growth Program

This came out of our last call and is worth getting your Claude up to speed on immediately because it has direct implications for your data pipeline.

### What it is

A tiered BD program to grow the Atlas database quickly through co-branded list partnerships — targeting ~1,500 creators before ONA.

**Tier 1 (immediate focus):** Low-lift partnerships where an organization (AAJA, ONA, SPJ chapters, journalism school programs, etc.) hands us a list of creators. We ingest the list, co-brand it, and they get visibility in the Atlas. No contracts, no money, pure value exchange. Dozens of these are sitting unused right now.

**Tiers 2/3 (later):** Deeper integrations — SmartNews, Beehiiv, Substack-level partnerships with data exchange or revenue components.

### What this means for your pipeline

Tier 1 partnerships will bring in lists that are **not Ryan-cleaned**. They'll come in varying formats, with inconsistent naming, platform vocab, geography formatting. Your normalization script becomes the critical intake layer for partner lists — not just for our own spidering output.

This also means we need new metadata fields to track list provenance. We need to design these together, but the likely additions are something like:

- `partner_name` — e.g., "AAJA", "ONA", "Lenfest Network"
- `list_source` — the named list or event this came from
- `list_type` — "partner-tier1", "editorial", "spidering", "self-submitted"

These would live alongside the existing `origin` field (or replace/extend it). The important thing is that co-branded lists show up as attributable in the database — both for partner relationship management and for eventual public display.

### Questions for your Claude to think through

1. How does a Tier 1 partner list flow through your pipeline differently than a Ryan-spidered batch? Does it get the same normalization pass, or does it need a separate intake step?
2. Should partner list metadata (partner name, list type) live in the main CSV or in a separate provenance file that joins on creator name?
3. If a creator appears on both a partner list AND in our own spidering output, who wins for `origin`? Or do we track both?

---

## Proposed Handoff Cadence

This is something Justin and Ryan talked through explicitly on their last call. The goal is to get both Claude instances into a rhythm where they're doing more of the coordination work and the humans are steering, not executing.

**The model:**
- Each Claude instance summarizes its current state and open assumptions periodically
- Each Claude generates questions for the *other* Claude (schema questions, pipeline questions, product questions)
- Humans carry the markdown files between instances and add context where needed
- Slack for urgent/blocking items; markdown for everything that can wait

**Concretely:**
- **Each CSV handoff**: Ryan sends file + append report + normalize report (as you've been doing) + a short note on any schema or vocab changes
- **Each schema change**: Ryan's Claude sends a markdown to Justin's Claude (like your March 16 update)
- **Each build change that affects data**: Justin's Claude sends a markdown to Ryan's Claude (like this reply)
- **Weekly or biweekly**: Each Claude does a "hand up" — open questions for the other instance, current assumptions, anything that needs a human decision

The explicit goal from the call: take a couple fingers off the wheel and let the Claudes handle the coordination layer. The humans make the calls; the Claudes prep the materials and ask the right questions.

---

*Reply with questions, pushback, or the next batch whenever ready. Suggest your Claude generates its own question list for this instance as part of the reply.*
