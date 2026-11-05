# Atlas Page Template Brief — November 2026

**For:** Justin Bank
**From:** James Bareham
**Date:** November 4, 2026
**Inherits:** DESIGN-TOKENS-v16.1.md and ATLAS-BRAND-GUIDE-v5.1.md. This brief adds no new design values, assets or rules.
**Replaces:** Atlas-Favicon-Fix-Brief-2026-11.md (not circulated). Its fix is Part 1 below.
**Scope:** this brief implements v16.1. Items marked for v17 are recorded for later and wait until v16.1 has been implemented and evaluated.

---

## Why this brief

Watershed shows the old favicon because its `<head>` was written by hand and drifted from the homepage's. The same thing can happen to any page built by copying another one: the favicon, the shared footer, font loading and metadata all depend on someone remembering them.

The goal is a structure where a new page gets the right head, header and footer by default, and the build fails if it doesn't.

**What's already a rule (v16.1), and what this brief adds:**

| | Source | Status |
|---|---|---|
| One shared header (`assets/js/header.js`) on every page | v16.1 § Site Header, § Font Loading | Existing rule |
| One shared footer (`footer.js`) on every public page; no page adds its own footer, strip or "Powered by" line | v16.1 § Site Footer | Existing rule |
| Fonts load only through `header.js` (plus Merriweather on editorial articles) | v16.1 § Font Loading | Existing rule |
| Every section uses the `full layout` container | v16.1 § Container Inner Padding | Existing rule |
| No dark-mode styles or `color-scheme: dark` | v16.1 § Interim Treatments | Existing rule |
| Shared head partial, page templates, `check_pages.py` | This brief | **Build and structure decisions: yours** |
| Which file is the favicon, and the icon markup | Not in v16.1 | **Undefined. Interim below; goes to v17** |

---

## Part 1: Fix Watershed now

So Watershed is right today, before the template work lands.

### Diagnose

```bash
# Compare icon tags on the homepage and Watershed
grep -n -i 'rel="\(shortcut \)\?icon\|apple-touch-icon\|rel="manifest' index.html watershed/index.html

# What is the root fallback?
ls -la favicon.ico 2>/dev/null

# Where the current icon files live
find . -name "icon.svg" -o -name "apple-touch-icon.png" | grep -v node_modules

# Does Watershed load the shared header and footer?
grep -n 'header.js\|footer.js' index.html watershed/index.html
```

Most likely causes, most probable first: Watershed has no icon tag (so browsers fall back to an old root `/favicon.ico`); a relative `href` copied from the homepage that 404s under `/watershed/`; a hard-coded link to an old file; or browser cache (check in a private window).

### Fix

1. Copy the homepage's icon `<link>` tags into `watershed/index.html` exactly, with root-relative paths (starting with `/`). Use the file the homepage already uses; don't choose another.
2. Replace the root `/favicon.ico` with the same current icon.
3. If Watershed doesn't load `header.js` and `footer.js` the way the homepage does, add them. Its "Tell us" and "Keep going" blocks are page body and stay.

Once Part 2 lands, Watershed moves onto the shared head partial like every other page.

---

## Part 2: The templated structure

All of this fits the current stack: plain HTML, CSS and vanilla JavaScript, built by `build-dist.sh`, hosted on Cloudflare Pages. Names below (folders, mount IDs, marker text) are proposals; match them to what the repo already uses.

### 2.1 One shared head partial

Create `partials/head.html`. It holds everything every page's head must carry, and nothing page-specific:

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Icon tags: copy the homepage's exactly, with root-relative paths -->
<link rel="icon" type="image/svg+xml" href="/[path to]/icon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/[path to]/apple-touch-icon.png">
<meta property="og:site_name" content="[homepage's current value]">
<link rel="stylesheet" href="/assets/css/variables.css">
<script src="/assets/js/header.js" defer></script>
```

Notes:

- **Only `icon.svg` and the 180px `apple-touch-icon.png`.** These are the only favicons any page uses. Don't add another icon file, size or format to the partial, and don't reference `Journalism_Atlas_favicon.png` (it's retired and deleted in v17).
- **The favicon goes in static HTML, not in `header.js`.** Browsers and link previews read icon tags from the HTML before scripts run, so a script-injected favicon is unreliable.
- Don't add `theme-color`, `color-scheme` or font links here. The first two would be new color decisions (and v16.1 rules out `color-scheme: dark`); fonts already load through `header.js`.
- Merriweather is not in the partial. Editorial articles add it in their own template (see 2.2), which keeps `serif-scope` meaningful.

**Include it at build time.** Each page's source head contains one marker line:

```html
<!-- atlas:head -->
```

`build-dist.sh` already substitutes `{{CREATOR_COUNT}}`; add a step that replaces the marker with the partial's contents after files are copied to `dist/`, e.g.:

```bash
python3 scripts/include_partials.py dist/
```

```python
# scripts/include_partials.py
import pathlib, sys
root = pathlib.Path(sys.argv[1])
head = pathlib.Path("partials/head.html").read_text()
for page in root.rglob("*.html"):
    text = page.read_text()
    if "<!-- atlas:head -->" in text:
        page.write_text(text.replace("<!-- atlas:head -->", head))
```

`check_brand.py` and `check_pages.py` both run on the source before the copy, as `check_brand.py` does today. `check_brand.py` scans `partials/head.html` as part of the source, so the partial is checked once rather than on every page.

Changing the favicon (or anything else in the partial) is then one edit, and every page picks it up on the next build.

### 2.2 Page templates

Create `templates/` with one file per page type. A new page always starts by copying one.

| Template | For | Differs by |
|---|---|---|
| `templates/page-standard.html` | Landing, product, Pulse, For Brands, partner, City Lab, research index pages | No serif anywhere |
| `templates/page-editorial.html` | Essays and editorial articles (Watershed is the model) | Loads Merriweather; prose in `--font-prose`; text column 680px; must live under an editorial article path |
| Long-form report | Reports | Already defined: `Atlas-Long-Form-Report-Template-2026-09.md`. Bring it onto the head partial and shared footer; its "Jump to" sub-nav follows v16.1 § Site Header |

The standard skeleton (mount-point IDs and the footer script path should match the homepage's):

```html
<!doctype html>
<html lang="en">
<head>
  <!-- atlas:head -->
  <title>[Page title]</title>
  <meta name="description" content="[one sentence]">
  <link rel="canonical" href="https://journalismatlas.com/[path]/">
  <meta property="og:title" content="[Page title]">
  <meta property="og:description" content="[one sentence]">
  <meta property="og:url" content="https://journalismatlas.com/[path]/">
  <meta property="og:image" content="[page image, or the site default the homepage uses]">
  <link rel="stylesheet" href="/assets/css/[page].css">
</head>
<body>
  <div id="site-header"></div>

  <main id="main">
    <section class="container">
      <!-- page content: role variables only, never hexes or font names -->
    </section>
  </main>

  <div id="site-footer"></div>
  <script src="/assets/js/footer.js" defer></script>
</body>
</html>
```

The editorial template is the same plus the Merriweather load (400, and italic 400/700 only if the prose uses them), the 680px text column for prose, and Watershed's skip link pattern if the shared header doesn't already provide one.

Title format, meta descriptions and default social image are copy and structure decisions: follow the homepage's current pattern unless you change it.

### 2.3 A one-command new page

So nobody copies an old page by hand:

```bash
# scripts/new_page.sh <path> <standard|editorial>
#   e.g. scripts/new_page.sh city-lab-austin standard
set -euo pipefail
path="$1"; type="$2"
mkdir -p "$path"
cp "templates/page-$type.html" "$path/index.html"
perl -pi -e "s#\[path\]#$path#g" "$path/index.html"   # perl rather than sed -i, so it works on macOS and Linux
echo "Created $path/index.html from page-$type. Fill in the [bracketed] fields."
```

Add one line to `WORKFLOW.md` (and the equivalent in `CLAUDE.md`): **new pages start from `scripts/new_page.sh`, never from a copy of an existing page.** This is a workflow instruction, not a design rule, so it doesn't conflict with `CLAUDE.md` restating v16.1 only.

### 2.4 `scripts/check_pages.py`: the structure check

`check_brand.py` checks design values. This new check covers page structure, and runs next to it in `build-dist.sh`, with the same fail-the-deploy behavior. Keep it a separate script: it enforces structure (your area) and existing v16.1 rules, and doesn't change `check_brand.py`.

| Rule | Fails on | Basis |
|---|---|---|
| `head-partial` | A source page without `<!-- atlas:head -->` | This brief |
| `own-icon` | Any `rel="icon"`, `apple-touch-icon` or manifest tag outside `partials/head.html`. This is what keeps `icon.svg` and `apple-touch-icon.png` the only favicons in use until v17 makes that a rule | This brief |
| `shared-header` | A page that doesn't load `header.js` and the header mount point | v16.1 § Site Header, § Font Loading |
| `shared-footer` | A public page that doesn't load `footer.js` and the footer mount point | v16.1 § Site Footer |
| `own-footer` | A `<footer>` that is a direct child of `<body>`, or any "Powered by" strip. (`<footer>` inside `<article>` or `<blockquote>` is semantic HTML and is fine) | v16.1 § Site Footer |
| `page-meta` | Missing `lang`, `<title>`, meta description or canonical | This brief |
| `serif-load` | A Merriweather load on a page outside an editorial article path | v16.1 § Font Loading (complements `serif-scope`) |

**Scope:** every public `.html` page, excluding `templates/` and `partials/` themselves. Skip the Exceptions register paths (Nodes and Networks, the internal Google Form mock-up) until James and you confirm which of these rules apply to them; v16.1 says the Atlas pages *around* a co-branded report follow the full rules, so those aren't skipped.

**Ratchet, like the brand check:** record today's failures in `scripts/pages-baseline.json`. The build fails if any file gains a failure, and **any page not in the baseline must pass with zero**. New pages are strict from day one; old pages come into line as they're touched.

### 2.5 Migrate existing pages

1. Run `check_pages.py` once and save the baseline.
2. Move pages onto the head partial and shared footer, highest-traffic first: homepage, Pulse, For Brands and Watershed, then the rest in order of traffic.
3. Each migrated page drops to zero in the baseline and stays there.
4. When the baseline is empty, switch `check_pages.py` to `--strict`.

---

## Acceptance checks

- [ ] Watershed shows the current green-and-black icon in a private window.
- [ ] `/favicon.ico` serves the current icon.
- [ ] `partials/head.html` exists, and the built `dist/` homepage and Watershed contain its icon tags.
- [ ] `scripts/new_page.sh test-page standard` produces a page that passes `check_pages.py` and `check_brand.py` with zero violations (then delete it).
- [ ] The same for `editorial` under an editorial article path.
- [ ] Every new page renders the shared header and footer, checked on the Cloudflare preview of the branch.
- [ ] `check_pages.py` runs in `build-dist.sh` and fails the deploy when a page gains a violation.
- [ ] `scripts/check_brand.py` passes.
- [ ] The answers in "What we need from you, Justin" are sent to James.

---

## For James's next token version (v17)

**Timing: v17 comes after v16.1, not alongside it.** v16.1 is implemented across the site and evaluated first. James starts v17 only after that evaluation. Nothing in this section changes what you build now: until v17 is issued, v16.1 and the interim treatments in this brief apply.

Not part of this build; recorded so the gaps are closed properly:

1. **Name the canonical favicon** (file, sizes, `apple-touch-icon`, manifest icons) and the required icon markup. Until then, the partial uses whatever the homepage uses today: `icon.svg` and a 180px `apple-touch-icon.png`. The favicon is a single green-and-black design that reads on both light and dark browser tabs. It doesn't switch with `prefers-color-scheme`, so it fits v16.1 § Interim Treatments as written, and `icon.svg` and the PNG show the same design. v17 should record this as the rule: one design, no theme switching, so a later version of the icon doesn't add a media query by accident.
   - **Only these two icons.** v17 should state that `icon.svg` and the 180px `apple-touch-icon.png` are the only favicons, with no other icon files on any page.
   - **Retire `Journalism_Atlas_favicon.png`.** v17 should remove it from the asset list and delete it from the repo, so it can't be used by accident. **Don't delete it before v17:** v16.1 still lists it, and it may be used somewhere other than as a favicon (see the checklist below). Until then, the `own-icon` check (Part 2.4) stops it, or any other file, from being used as a favicon.
2. **Decide whether the structure rules move into Enforcement**, either as rules in `check_brand.py` or by listing `check_pages.py` as a canonical check.
3. **Add `partials/`, `templates/` and `scripts/check_pages.py` to the protected files** for code-owner review after the level-set.
4. **Confirm how the Exceptions register paths are treated** by the header, footer and head rules.

### What we need from you, Justin

Please send James these answers when you do the Part 1 fix. They're the facts v17 needs to define the favicon; you can get most of them from the repo and the homepage's `<head>`.

- [ ] **Repo paths** for `icon.svg` and `apple-touch-icon.png`.
- [ ] **The exact `<link>` markup** the homepage uses for them, including `sizes` and `type`.
- [ ] **What's at `/favicon.ico`** now, and what you did with it in Part 1 (replaced with the new icon, removed or redirected).
- [ ] **The colors in `icon.svg`**, as the hex values in the file, so James can confirm they're Tier 1 values.
- [ ] **Whether `apple-touch-icon.png` has an opaque background** filled to its edges, or transparent areas.
- [ ] **Where `Journalism_Atlas_favicon.png`** (listed in v16.1) is still used anywhere in the site, as a favicon or anything else. James needs this before v17 retires and deletes it. Don't delete it yet.
- [ ] **Whether any other icons exist or are planned**, such as a web manifest with Android icons.
- [ ] **Which, if any, Exceptions register pages** (Nodes and Networks, the Google Form mock-up) load the shared header, footer or favicon today.

---

## Out of scope, for your call

While checking Watershed, two copy points against the Project Instructions: its em dashes are spaced ("still moving — across county lines"; the rule is word—word), and it says "more than 2,400 creator-journalists" where the public figure is "about 2,400–2,500." Watershed is your dated essay, so whether to change these is up to you.
