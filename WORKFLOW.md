# Atlas — Workflow & Decision Protocol

*Companion to CLAUDE.md. Read both at session start.*

---

## Decision Authority

**Justin makes every decision.** No exceptions, no autonomous calls on structure, copy, or design.

- **James Bareham** (james@happicamp.com) — design advisor. Consult before implementing any new component type, layout pattern, or color usage not already defined in `DESIGN-TOKENS.md`. His principles live at `_reference/james-design-principles.md`.
- **Ryan** — data advisor. Consult before modifying `creators-data.json`, `creators-master.csv`, or the data pipeline (`convert.js`, `DATA-OPS-PROTOCOL.md`).

When in doubt: stop, surface the question, wait for Justin's call.

---

## What "Done" Means

A task is done when:
1. **It loads in the browser** — no console errors, no broken layout, no missing assets
2. **It fits design standards** — tokens from `variables.css`, load order correct, no hardcoded colors or unapproved font weights
3. **It's pushed to GitHub** — Cloudflare auto-deploys from main; local-only is not done

The CSS_AUDIT.md and JS_AUDIT.md files document the baseline. New work should not introduce violations that those audits fixed.

---

## Session Start Checklist

Before writing any code:

- [ ] Read `CLAUDE.md` (page inventory, CSS architecture, key constraints)
- [ ] Read `DESIGN-TOKENS.md` if the session touches any styling
- [ ] Read `DATA-OPS-PROTOCOL.md` if the session touches any JSON or CSV data
- [ ] If working from a Chat-originated brief: cross-reference file paths and page names against actual repo state — briefs can go stale

---

## Chat → Code Handoff

Claude Chat is good at briefs and strategy. Claude Code is authoritative on current file state. The failure mode is Chat writing a brief based on stale assumptions about what's in the repo.

**Before building from a Chat brief:**
1. List ambiguities in tiers: errors / questions / suggestions
2. Flag any file path that looks like a Chat artifact path (`/mnt/user-data/outputs/`) — those don't exist in the repo
3. Cross-reference any creator counts, page names, or component descriptions against actual files
4. Surface mismatches to Justin before building

---

## Deploy Process

1. Edit files locally
2. Verify in browser (load the page, check console, check design)
3. Justin pushes via **GitHub Desktop** — never `git push` from terminal
4. Cloudflare auto-deploys from main branch within ~1 minute
5. Test on live URL in a fresh incognito window (cached redirects can mask issues)

---

## When to Stop and Ask

Stop and surface to Justin when:
- A decision requires a judgment call on design that isn't covered by `DESIGN-TOKENS.md`
- A brief conflicts with current repo state in a way that affects the build approach
- A data operation would modify `creators-master.csv` or change the JSON schema
- A new page, component type, or URL pattern is being introduced
- James sign-off is required (see `CLAUDE.md` § "What requires James's sign-off")
