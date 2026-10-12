# Design Change Handoff Format — v1.0

*For James (and any Claude he's working with) to follow when sending a design/token update to Justin.*
*Goal: keep doing exactly what you're already doing well — this just names the shape so it's consistent every time, and so it can go straight into execution without someone re-describing it first.*

---

## The short version

Your last two handoffs (v10, v11) already had the right shape almost by accident — versioned, dated, self-diffing, with a decision log. This doc just makes that shape explicit and repeatable. **How you send it doesn't change** — same as always, Slack, with the updated `.md` file attached.

The only change is on our end: once a handoff has this shape, we can drop it straight into a GitHub Issue on the repo without re-describing it first — and it's easier to find again later than Slack scrollback ("why does the site use Inter" should have a permanent answer). That's our step, not yours — no GitHub needed on your side.

---

## What to include, every time

### 1. Header block
```
# [Doc name] — v[N]
Last updated: [date]
Previous version: v[N-1] ([date])
Owner: James (james@happicamp.com)
```

### 2. "What changed" — decision-level only

One numbered item per change. Each item = **what** changed + **why**, in a sentence or two. This is the part that goes straight into a brief's "established facts" almost unedited — keep it there, don't go further.

```
- **[Thing] changed: [old] → [new].** [One or two sentences on why.]
```

**Don't include implementation specifics** — which CSS file, which class name, which component. Not because that's not useful information in general, but because it's frequently wrong relative to what's actually in the live repo (this round: assumed the font loaded from one place, it turned out to load from 54 different places; assumed save/follow/bookmark toggles existed, they don't exist at all). Guessing at implementation creates false confidence that's worse than not guessing. If you *do* know something repo-specific and want to flag it, mark it explicitly as unverified: *"possible implementation note, not confirmed against the live repo."*

### 3. An explicit "unchanged" line

The single highest-value sentence in the whole doc — it tells whoever's implementing exactly what NOT to touch:

```
No other token values changed. [List what's untouched: colors, spacing, etc.]
```

### 4. The full updated reference file, attached

Not just the diff — the whole doc, so it can replace the canonical file wholesale rather than someone reconstructing a merge.

### 5. Decision log — append, don't rewrite

Keep using the same table, add rows, never edit old ones:

```
| Date | Decision | Rationale |
|------|----------|-----------|
| [Date] | [What changed] | [Why] |
```

This is what gives us the version history Justin mentioned — it's already working, just keep doing it.

---

## What NOT to worry about

- Which files it touches, how it's implemented, whether it's "just CSS" or needs behavior changes — that's the executor's job to figure out from the actual repo, every time, regardless of what anyone assumes going in.
- Getting the format perfect. This is a starting shape, not a compliance checklist.

---

## Minimal copy-paste template

```markdown
# [System] Tokens — v[N]
Last updated: [date]
Previous version: v[N-1]
Owner: James

### What changed in v[N]
- **[Change 1]:** [what + why]
- **[Change 2]:** [what + why]
- **No other values changed.** [what's untouched]

---
[full updated reference content below]
```

---

## Delivery

Nothing changes here — keep sending it exactly like you have been:

1. Post the update in Slack, same as always, with the full updated `.md` file attached.
2. That's it on your end — no GitHub, no new tooling, no login to set up.
3. We take it from there: dropping it into a GitHub Issue on our side so it's easier to find later and hand straight to Claude Code.

---

**Version history**
- v1.0 — Sept 20, 2026 — initial format guide, written after the v11 handoff (Inter/Merriweather/icon fill states).
