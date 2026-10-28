# Atlas — Workflow & Decision Protocol

*Companion to CLAUDE.md. Read both at session start.*

---

## Decision Authority

**Justin makes product, structure, page, copy, build and release decisions.**

**Design values are not decisions to make in a session.** Colors, typefaces, sizes, weights, spacing, radius, icons and component states are locked in `docs/design/DESIGN-TOKENS-v16.md`. They change only through a new token version written or approved by **James Bareham** (Creative Director, james@journalismatlas.com). If a task seems to need one, stop and list it for James; don't build it, and don't map it to the nearest token.

- **James Bareham**: owns the design tokens and brand guide. His principles live at `_reference/james-design-principles.md`; where a value there conflicts with v16, v16 wins.
- **Ryan**: data advisor. Consult before modifying `creators-data.json`, `creators-master.csv`, or the data pipeline (`convert.js`, `DATA-OPS-PROTOCOL.md`).

When in doubt about anything other than design values: stop, surface the question, wait for Justin's call.

---

## What "Done" Means

A task is done when:
1. **It loads in the browser** — no console errors, no broken layout, no missing assets
2. **It fits design standards**: `python3 scripts/check_brand.py` passes (no new violations); tokens from `variables.css` only; fonts only through `var(--font-*)`; no hardcoded colors, unapproved fonts, sizes below the floor, or unapproved weights
3. **It's pushed to GitHub** — Cloudflare auto-deploys from main; local-only is not done

The CSS_AUDIT.md and JS_AUDIT.md files document the baseline. New work should not introduce violations that those audits fixed.

---

## Session Start Checklist

Before writing any code:

- [ ] Read `CLAUDE.md` (page inventory, CSS architecture, key constraints)
- [ ] Read docs/design/DESIGN-TOKENS-v16.md (Governance, Locks and Exceptions first) if the session touches any styling, inline styles, charts or canvas text
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

1. Work on the `dev` branch; Cloudflare builds a preview for it
2. Verify in the browser (load the page, check console, check design) and run `python3 scripts/check_brand.py`
3. Push `dev` via GitHub Desktop and open a pull request to `main`
4. James reviews design changes on the preview; files under CODEOWNERS need his approval. The `brand-check` status must pass
5. Merge; Cloudflare deploys `main` within about a minute
6. Test on the live URL in a fresh incognito window (cached redirects can mask issues)

---

## When to Stop and Ask

Stop and surface to Justin when:
- A decision requires a judgment call on design that isn't covered by `docs/design/DESIGN-TOKENS-v16.md`
- A brief, mockup or request names a font, color, size or rule that isn't in DESIGN-TOKENS-v16.md (apply by role; list the gap for James)
- `check_brand.py` fails and the fix would mean editing the baseline, the check, `variables.css` or the tokens
- A brief conflicts with current repo state in a way that affects the build approach
- A data operation would modify `creators-master.csv` or change the JSON schema
- A new page, component type, or URL pattern is being introduced
- James sign-off is required (see `docs/design/CLAUDE-DESIGN-RULES.md` § "What changes only with a new token version")
