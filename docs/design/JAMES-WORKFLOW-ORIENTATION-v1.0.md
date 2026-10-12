# Working Natively with the Atlas Code — Orientation for James

**Version:** 1.0 · October 2026
**From:** Claude (Justin's Atlas project), written for James to read and to bring into his own Claude
**Companion files (all in `docs/design/` in the journalism-atlas repo):** `JAMES-THINK-IT-THROUGH-PROMPT-v1.0.md` (paste into your Claude), `CLAUDE-MD-DESIGN-LANE-SECTION-v1.0.md` (the rules Claude Code follows on your work, also added to `CLAUDE.md`)

## Changelog
- v1.0 (Oct 2026): first version.

---

## Why this, why now

The v14 token work just landed on the live site. It went well, but the way it got there is worth looking at. You designed in your Claude and sent a token doc. Justin passed it to his Claude Code. Code compared it with the real site and found places where the two disagreed (the header was already white, not black). Those questions went back to you through Justin, and the next version answered them. That happened v12 → v13 → v14 in one day.

None of that comes from bad specs. Your Claude was designing against a *description* of the site, not the site itself, and Justin was the only link between your Claude and his.

The goal of this memo is to change that. **Your Claude should be able to look at the actual code, and you should be able to see your changes rendered without Slack or Justin in the loop.** You try things, adjust, and build on your own. When something is ready, it moves to the live site.

## The ladder

There are four rungs. Start on Rung 1. Everything above it is optional, and you can stop on any rung that suits you. Each one gives you something concrete.

### Rung 1 — An Atlas Design project in Claude (start here)

**What it is.** A shared Claude Project for design work. It holds the real working files: `CLAUDE.md`, the current `DESIGN-TOKENS`, `ATLAS-BRAND-GUIDE-v3.md`, `variables.css`, and a few representative pages (homepage, search, a creator profile, a long-form page). No GitHub or setup is needed.

**What it gives you.**
- Your Claude reasons from the CSS that's actually live, not from memory or an older token version. Specs come out already matching the site.
- You can ask for a mockup of a change ("show me the search page with the v15 card treatment") and see it rendered as an artifact in the chat, built on the real markup.
- You can ask it to check your own rules before you send them: contrast ratios, where a variable is used, what else changes if you change one value.

**Its limit.** It's a snapshot. When the site changes, the files in the Project have to be refreshed (Justin will keep them current, or you can once you're on Rung 3).

### Rung 2 — Claude Design for new visual patterns

**What it is.** Claude's canvas tool for design work you can iterate on and share by link.

**Use it for.** Work that doesn't exist in code yet, like the postcard/profile-card system spec, the ATLAS_VIZ_COLORS category assignments (once Ryan's taxonomy settles), or a new page concept.

**What it gives you.** Exploration happens somewhere other than a Slack thread. A finished design becomes the target Claude Code builds toward.

### Rung 3 — Claude Code on a branch

**What it is.** Your own copy of the `journalism-atlas` repo on your machine, with Claude Code working in it on a branch named `james/<what-it-is>` (e.g. `james/card-radius`).

**What it gives you.** This is the full loop without Justin. You ask Claude Code to change `variables.css`, look at the result, adjust, and repeat. Your Claude also inherits the verification tooling built during the v14 rollout:
- a color resolver that proves a rename produced **zero rendered change** on every page (with a deliberate-break test to show the check works);
- the habit of splitting commits, so CSS/variable changes, `header.js` changes, and assets each land separately and can each be reverted on their own.

**How you see your work.**
- **Preview deploys (best):** the site deploys through Cloudflare Pages, which normally builds a preview URL for every pushed branch. Push `james/card-radius` and you get a link showing that branch as the real site. *To confirm: Justin needs to check preview deployments are switched on.*
- **Locally:** the site is static HTML with no build step, but opening a file directly in the browser won't fully work. Data loads by `fetch` and URLs are clean (`/search`, not `search.html`). Ask Claude Code to "serve the site locally" and it will start a small local server and give you an address.

### Rung 4 — Pull request → Justin merges → live

You push your branch with GitHub Desktop and open a pull request with the preview link and before/after screenshots. Justin reviews and merges it to `main`, and Cloudflare deploys it live. Your work lands as you built it, not as someone translated it.

## Where you can work directly, and where you use a branch

| Change | Where |
|---|---|
| Editing the design-token doc or the brand guide | **Commit straight to `main`.** These are documents. Nothing on the live site changes when they change. |
| Anything that changes what the site looks like (CSS, variables, templates, `header.js`/footer, logos and assets) | **A `james/…` branch, then a pull request.** Justin merges. |

The split works because the token doc is the source of truth. Once it lives in the repo and you edit it there, Claude Code always reads the current version, and v12 → v13 → v14 becomes commit history instead of five Slack attachments.

**Token-doc conventions** (same as every Atlas doc): bump the version in the filename (`DESIGN-TOKENS-v15.md`), add a changelog line saying what changed, and remove the superseded version in the same commit so only one is ever live. No "(1)" or "copy" filenames.

## Outside the design lane

Leave these alone, even on a branch:
- `creators-master.csv`, `creators-data.json`, `convert.js`, anything in `pipeline/`. These are the database, Ryan's and Justin's territory.
- Everything in `journalism-atlas-private` except reading for context.
- **Site copy**, for now. The brand guide's copy rules (Starter Pack naming, creator-count wording, "visitors" not "leads", TIJA LLC lines) are getting their own separate sweep. Flag copy issues and don't fix them inline.
- **Never push to `main` from Claude Code itself.** All pushes go through GitHub Desktop. This is the standing rule for everyone on Atlas.

## Rough edges

Here's what isn't fully confirmed yet:
- **Repo access.** Your access to `journalism-atlas-private` is confirmed. Write access to the production repo, `journalism-atlas`, needs confirming before Rung 3.
- **Preview deploys.** These are expected but not yet checked (see Rung 3).
- **Project files go stale.** That's a Rung 1 limitation, and it's the main reason Rung 3 is worth reaching eventually.
- **The merge step is a new queue.** If PRs sit waiting on Justin, the bottleneck has only moved. Say so if that starts happening.

## How to use this memo

Read it, then open your own Claude and paste in `JAMES-THINK-IT-THROUGH-PROMPT-v1.0.md` with this memo attached. Your Claude will ask how you like to work and help you choose where to start. That conversation is for you; it doesn't need to come back to Justin unless you want it to.

---

## Appendix — Setup checklist (Rungs 3–4 only)

1. **GitHub account** signed in, and confirm with Justin you can see `bankonjustin/journalism-atlas` with write access.
2. **GitHub Desktop** installed and signed in → *File → Clone repository* → `journalism-atlas` → save somewhere you'll find (e.g. `~/Documents/GitHub/`).
3. **Claude Code** in the Claude desktop app (the Code tab) → open the folder you just cloned.
4. **First branch:** in GitHub Desktop, *Current Branch → New Branch* → `james/hello`. Or ask Claude Code to create it.
5. **First change:** ask Claude Code for something tiny and harmless, then "serve the site locally" and look.
6. **Push the branch** in GitHub Desktop (*Publish branch*), then check for the Cloudflare preview link on the commit or PR.
7. **Open a pull request** (GitHub Desktop → *Create Pull Request*). Include the preview link and before/after screenshots. Tag Justin.
8. **Token-doc edits:** switch back to `main`, edit, commit with a changelog line, push.
