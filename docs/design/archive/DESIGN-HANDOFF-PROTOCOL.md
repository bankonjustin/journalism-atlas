# DESIGN-HANDOFF-PROTOCOL.md
**Independent Journalism Atlas — James ↔ Justin ↔ Claude Code Workflow**
*Last updated: April 2026 | Commit this file to repo root*

---

## What This Document Is

A protocol for the three-node workflow that produces Atlas design implementations: James generates design direction in Claude Chat, Justin translates that into implementation briefs for Claude Code, Claude Code executes and deploys. This document is meant to be read by all three nodes — including James's Claude Chat instance and Justin's Claude Code instance — so the language is explicit about who does what and why.

---

## The Four-Step Workflow

```
1. James → Claude Chat       Design direction brief (markdown artifact)
2. Justin → Claude Code      Technical translation brief (reconciles brief to actual file)
3. Claude Code → Repo        Implementation + flagged ambiguities before any code touches
4. Repo → Browser            Live versioned URL for James to review
```

**Step 2 is the critical leverage point.** It's where mismatches between design intent and implementation reality get caught before they become broken code. Without it, Claude Code will make reasonable-sounding assumptions that are wrong — e.g., looking for D3 color arrays in a file that uses hand-coded inline SVG.

---

## Step 1: James's Brief Format

When generating design direction in Claude Chat, **always end with this structured block:**

```
## Implementation Handoff

**File target:** [filename, e.g. `partner-list-cillizza.html`]
**Source of truth:** DESIGN-TOKENS.md (or commit hash / date if referencing a specific version)
**CSS selectors to target:** [list the actual class/ID names you're working with — read the file first]
**Color values in use:** [list actual hex values currently in the file — read the file first]
**Ambiguities to resolve before coding:** [anything you're unsure about]
**Do NOT change:** [list elements, sections, or behaviors that must be preserved]
**Version behavior:** [new versioned file OR overwrite canonical]
```

**Before writing the brief, James's Claude should read the target file and produce:**
- A CSS selector inventory (all class names and IDs in the file)
- A color hex inventory (all hex values currently in use)

This takes one tool call and prevents the most common brief-to-implementation mismatch: James naming things that don't exist in the file.

---

## Step 2: Justin's Translation Brief

Between receiving James's brief and opening Claude Code, draft a short technical translation that confirms:

- **Actual file path** — what is the real path in the repo?
- **Rendering architecture** — is this inline SVG, D3, vanilla JS, or something else? This determines what's targetable.
- **CSS selector names** — do the class names in James's brief match actual selectors in the file?
- **Color mapping** — does James's color language map to the correct hex values? (e.g., "accent green" = `#ceff00` on dark backgrounds, `#97d600` on light)
- **DOM structure notes** — anything about the file structure Claude Code needs to know before touching it

Claude Code can generate this translation draft from the source file *before* James's brief arrives, so the two can be reconciled rather than one overriding the other.

---

## Step 3: Claude Code Behavior Rules

**Ambiguities stop the clock.** If anything in the brief is unclear — a selector that doesn't exist, a color reference that's ambiguous, a structural assumption that contradicts the file — Claude Code names it explicitly and waits for resolution. It does not infer and proceed.

**Claude Code fills gaps differently than Claude Chat.** Claude Chat will make a creative decision to resolve ambiguity and keep moving. Claude Code should not do this for implementation work. Gaps in the brief become questions, not silent choices.

**Implementation sequence:**
1. Read the target file
2. Produce a brief translation (selectors found, colors found, any structural notes)
3. Flag ambiguities explicitly — wait for Justin to confirm before touching code
4. Implement
5. Produce a diff summary of what changed and what was preserved

---

## Step 4: Versioning Pattern

**Default behavior: new versioned file, not an overwrite.**

Rather than overwriting the canonical file, produce a new versioned file:

```
partner-list-cillizza.html        ← canonical (do not touch until confirmed)
partner-list-cillizza-v2.html     ← new version for review
partner-list-cillizza-v3.html     ← subsequent iteration if needed
```

Each versioned file is a deployable URL. James can review all versions simultaneously in browser and direct which becomes canonical. Merge to canonical only after James confirms in browser. This is faster than reading a diff for design-heavy work.

**Exception:** If James explicitly specifies "overwrite canonical" in the brief, Claude Code can do so. Otherwise, version by default.

---

## Shared Vocabulary (Atlas Design System)

Mismatches in design language are a persistent source of translation loss. Use this table when writing briefs.

| James says | Codebase means |
|---|---|
| "accent green" / "neon green" | `#ceff00` — use on dark (`#313131` or black) backgrounds only |
| "lime green" | `#97d600` — use on light (`#efeff2`) backgrounds only |
| "dark olive" | `#5d7400` |
| "dark gray" / "charcoal" | `#313131` |
| "light gray" / "off-white" | `#efeff2` |
| "D3 visualization" | Likely **inline SVG** — check the file before assuming JavaScript |
| "the chart" | Identify the specific SVG or canvas element by selector |
| "Hanken Grotesk" | Primary font — Space Grotesk and Inter are being phased out |
| "the Atlas nav" | Standard nav pattern — reference a working page, not a spec |

**When in doubt, read the file.** Every brief should be grounded in what's actually in the code, not what we think is there.

This vocabulary is a living document. When a new term-to-token mapping is established, add it here and commit.

---

## What the Diff Summary Looks Like

After implementation, Claude Code should produce a brief summary to close the loop with James:

```
## Implementation Summary — [filename] — [date]

**What changed:**
- [list specific changes, referencing selectors and hex values]

**What was preserved (as requested):**
- [list elements that were explicitly kept]

**Ambiguities resolved as:**
- [any decisions made, with rationale]

**Ambiguities still open:**
- [anything that needs James or Justin to confirm before merge to canonical]

**Review URL:** [deployed link]
```

This goes back to James via Justin. The loop is: design brief → implementation → diff summary → browser review → canonical merge or next iteration.

---

## The Meta-Pattern

James and Justin are pair-programming across two Claude interfaces. The shared artifact layer — markdown files committed to the repo — is the communication protocol. The more structured those artifacts are, the less lossy the translation.

The goal: James describes a design decision once. It lands correctly in code. He reviews it in browser. No synchronous call required.

That's the target state. This protocol is how we get there.

---

## Quick Reference Checklist

**James, before submitting a brief:**
- [ ] Read the target file in Claude Chat
- [ ] Produced CSS selector inventory
- [ ] Produced color hex inventory
- [ ] Implementation Handoff block is at the bottom of the brief
- [ ] "Do NOT change" list is explicit

**Justin, before opening Claude Code:**
- [ ] Reconciled James's brief against actual file structure
- [ ] Confirmed rendering architecture (SVG vs JS vs other)
- [ ] Confirmed selector names match
- [ ] Confirmed color hex values match
- [ ] Translation brief is ready

**Claude Code, before touching the file:**
- [ ] Read the target file
- [ ] Produced brief translation (selectors, colors, structure)
- [ ] All ambiguities flagged and resolved
- [ ] Version behavior confirmed (new file vs overwrite)

---

*This document lives at repo root. It is intended to be read by Claude Code at the start of any design implementation session. When in doubt, follow this protocol exactly and ask rather than assume.*
