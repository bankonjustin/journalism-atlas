#!/usr/bin/env python3
"""
check_brand.py: enforces the locked rules in docs/design/DESIGN-TOKENS-v16.md.

Allowlist, not blocklist: anything not named in v16 fails.

  python3 scripts/check_brand.py                  # ratchet: fail on any NEW violation (default; used by build-dist.sh)
  python3 scripts/check_brand.py --strict         # fail on ANY violation (target state)
  python3 scripts/check_brand.py --report         # print every violation, never fail
  python3 scripts/check_brand.py --write-baseline # rewrite scripts/brand-baseline.json (James approves via CODEOWNERS)
  python3 scripts/check_brand.py path/to/page.html ...   # check named files only (strict for those files)

Rules (v16 § Enforcement):
  font-family   a font not on the allowlist (Inter, Merriweather, Source Code Pro, Material Symbols Outlined)
  serif-scope   Merriweather outside an editorial article path
  serif-heading a serif on a heading-like selector, anywhere
  font-literal  a font named directly on a page instead of var(--font-*) (only variables.css may name families)
  font-size     text below 12px, anywhere (pages, inline styles, JS strings)
  font-weight   800 or 900
  pill-radius   border-radius 999px / 9999px
  color         a hex color not in the v16 palette (Tiers 1-5, Neutral and Cool scales)
  lime-text     Lime Green used as a text color
"""
import json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "scripts", "brand-baseline.json")

# ---- v16 allowlists (change only with a new token version) ----
FONTS_ALLOWED = {
    "inter", "inter fallback", "merriweather", "merriweather fallback",
    "source code pro", "source code pro fallback", "material symbols outlined",
    "sans-serif", "serif", "monospace", "inherit", "initial", "unset",
}
# Paths outside the rules (v16 § Exceptions). Add only with a new token version.
EXCLUDED = (
    "_deprecated/", "_reference/", "node_modules/", "dist/", "outputs/", "qa/", "docs/", "sessions/",
    ".claude/", ".beads/", "pipeline/", "scripts/",
    # Co-branded report exception: Nodes and Networks (ASU / Knight Center at Cronkite)
    "preview/nodes-and-networks-", "preview/nn-launch-kit/", "assets/nn5/", "nodes-networks-v5/", "tools/preview-build/",
    # Internal mock of a Google Form (uses Roboto to match Google Forms)
    "atlas-portal/google-form-template.html",
)
SERIF_ARTICLE_PATHS = ("watershed/",)   # body prose only; long-form report template pages join here when built
PALETTE = {
    # Tier 1
    "ceff00", "97d600", "5d7400",
    # Tier 2 Neutral and Cool
    "ffffff", "efefef", "c6c6c6", "909090", "5e5e5e", "303030", "121212", "000000",
    "efeff4", "c6c6cd", "909097", "5e5e64", "303036", "121218",
    # Tier 3
    "fff700", "806600", "ffaa00", "b35100", "ff66ff", "a100a1", "ff33cc", "a1006c", "00e5ff", "005ea3",
    # Tier 4 ATLAS_VIZ_COLORS (confirmed, probable, reserve)
    "78909c", "ff7043", "ba55cc", "c6a700", "ef0e61", "2196f3", "00acc1", "26a69a", "d81b72",
    "e53935", "7c4dff", "5b7fa6", "bf5a3a", "a1887f", "6a8d9b", "ea80fc", "40c4ff", "ffab40",
    # Tier 5
    "f50000", "ffbc00",
}

HEX = re.compile(r"(?<![\w&])#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b(?![\w-])")
FAMILY_DECL = re.compile(r"font-family\s*:\s*([^;}{<>\n]+)", re.I)
ATTR_END = re.compile(r"\"\s*(?:[\w-]+=|/?>)|\"\s*$")
GF_FAMILY = re.compile(r"[?&]family=([A-Za-z0-9+ ]+)")
FONTFACE = re.compile(r"@font-face\s*\{[^}]*?font-family\s*:\s*['\"]?([^;'\"]+)", re.I)
CANVAS_FONT = re.compile(r"\.font\s*=\s*['\"`][^'\"`]*?\d+px\s+([^'\"`]+)['\"`]")
SIZE = re.compile(r"font-size\s*:\s*([\d.]+)(px|rem|em)\b", re.I)
CANVAS_SIZE = re.compile(r"\.font\s*=\s*['\"`][^'\"`]*?\b([\d.]+)px", re.I)
SVG_SIZE = re.compile(r"font-size[\"']?\s*,\s*[\"']?([\d.]+)(px)?\b|font-size=\"([\d.]+)(px)?\"", re.I)
WEIGHT = re.compile(r"font-weight\s*:\s*(800|900)\b")
PILL = re.compile(r"border-radius\s*:\s*9{3,4}px")
LIME_TEXT = re.compile(r"(?:^|[;{\s\"'])color\s*:\s*(#97d600|var\(--color-lime\))", re.I)
RULEBLOCK = re.compile(r"([^{}]{1,400})\{([^{}]*)\}")
HEADINGISH = re.compile(r"(h[1-6]\b|title|head|claim|display|lede|dek|stat|numeral|pullquote|label|eyebrow|-n\b)", re.I)
SERIFISH = re.compile(r"merriweather|var\(--font-(editorial|prose|body|serif)\)|(?<!sans-)\bserif\b", re.I)

def norm_family(name):
    return name.strip().strip("'\"").replace("+", " ").strip().lower()

def scan(path, text):
    v = defaultdict(list)
    rel = path
    is_vars = rel.endswith("assets/css/variables.css")
    def add(rule, pos, detail):
        line = text.count("\n", 0, pos) + 1
        v[rule].append((line, detail[:90]))

    # fonts
    for m in FAMILY_DECL.finditer(text):
        val = ATTR_END.split(m.group(1))[0].strip()
        if not val:
            continue
        if "var(" not in val and not is_vars:
            add("font-literal", m.start(), val)
        for fam in re.sub(r"var\([^)]*\)", "", val).split(","):
            f = norm_family(fam)
            if f and f not in FONTS_ALLOWED and not f.startswith("var("):
                add("font-family", m.start(), fam.strip())
    for rx in (GF_FAMILY, FONTFACE, CANVAS_FONT):
        for m in rx.finditer(text):
            for fam in m.group(1).split(","):
                f = norm_family(fam)
                if f and f not in FONTS_ALLOWED:
                    add("font-family", m.start(), fam.strip())
    if not rel.startswith(SERIF_ARTICLE_PATHS) and not is_vars:
        for m in re.finditer(r"merriweather|--font-(editorial|prose)\b", text, re.I):
            add("serif-scope", m.start(), m.group(0))
    for m in RULEBLOCK.finditer(text):
        sel = m.group(1).strip().split("\n")[-1]
        fm = re.search(r"font-family\s*:\s*([^;]+)", m.group(2))
        if fm and HEADINGISH.search(sel) and SERIFISH.search(fm.group(1)):
            add("serif-heading", m.start(), sel.strip())

    # sizes
    for m in SIZE.finditer(text):
        n, unit = float(m.group(1)), m.group(2).lower()
        px = n if unit == "px" else n * 16
        if unit == "em":
            continue  # relative to parent; reviewed by eye
        if px < 12:
            add("font-size", m.start(), m.group(0))
    for m in CANVAS_SIZE.finditer(text):
        if float(m.group(1)) < 12:
            add("font-size", m.start(), m.group(0))

    for m in WEIGHT.finditer(text):
        add("font-weight", m.start(), m.group(0))
    for m in PILL.finditer(text):
        add("pill-radius", m.start(), m.group(0))
    for m in LIME_TEXT.finditer(text):
        add("lime-text", m.start(), m.group(0))

    # colors
    for m in HEX.finditer(text):
        h = m.group(1).lower()
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if h not in PALETTE:
            add("color", m.start(), "#" + m.group(1))
    return v

def files_to_check(args):
    if args:
        return [os.path.relpath(os.path.abspath(a), ROOT) for a in args]
    out = []
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in fs:
            if f.endswith((".html", ".css", ".js")) and not f.endswith(".min.js"):
                rel = os.path.relpath(os.path.join(d, f), ROOT)
                if not rel.startswith(EXCLUDED) and not any(x in rel for x in ("/vendor/", "/lib/")):
                    out.append(rel)
    return sorted(out)

def main():
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    results = {}
    for rel in files_to_check(paths):
        try:
            text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        v = scan(rel, text)
        if v:
            results[rel] = v
    counts = {f: {r: len(x) for r, x in v.items()} for f, v in results.items()}

    if "--write-baseline" in flags:
        json.dump(counts, open(BASELINE, "w"), indent=1, sort_keys=True)
        print(f"Baseline written: {sum(sum(c.values()) for c in counts.values())} known violations in {len(counts)} files.")
        return 0

    strict = "--strict" in flags or bool(paths)
    base = {} if strict else (json.load(open(BASELINE)) if os.path.exists(BASELINE) else {})
    new = []
    for f, rules in counts.items():
        for r, n in rules.items():
            allowed = base.get(f, {}).get(r, 0)
            if n > allowed:
                new.append((f, r, n, allowed))
    if "--report" in flags or new:
        for f, v in sorted(results.items()):
            for r, items in sorted(v.items()):
                if "--report" in flags or any(x[0] == f and x[1] == r for x in new):
                    for line, d in items:
                        print(f"{f}:{line}  {r}  {d}")
    total = sum(sum(c.values()) for c in counts.values())
    print(f"\n{total} violations in {len(counts)} files." + ("" if strict else f" Baseline allows {sum(sum(c.values()) for c in base.values())}."))
    if new and "--report" not in flags:
        print("\nFAILED: new violations of DESIGN-TOKENS-v16 (above). Use a token from docs/design/DESIGN-TOKENS-v16.md.")
        for f, r, n, a in new:
            print(f"  {f}: {r} {n} (baseline {a})")
        return 1
    print("OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
