#!/usr/bin/env python3
"""
check_brand.py: enforces the locked rules in docs/design/DESIGN-TOKENS-v16.md.

Allowlist, not blocklist: anything not named in v16 fails.

  python3 scripts/check_brand.py                  # ratchet: fail on any NEW violation (default; used by build-dist.sh)
  python3 scripts/check_brand.py --strict         # fail on ANY violation (target state)
  python3 scripts/check_brand.py --report         # print every violation, never fail
  python3 scripts/check_brand.py --write-baseline # rewrite scripts/brand-baseline.json (counts may only go down; see --guard-baseline)
  python3 scripts/check_brand.py --tight          # ratchet, plus fail when the baseline is loose (a count fell, or a listed file is gone). CI uses this
  python3 scripts/check_brand.py --guard-baseline <git-ref>   # CI only: fail if any baseline count is higher than at <git-ref>,
                                                  # unless scripts/check_brand.py itself changed since <git-ref>
  python3 scripts/check_brand.py path/to/page.html ...   # check named files only (strict for those files)

Rules (v16 § Enforcement):
  font-family   a font not on the allowlist (Inter, Merriweather, Source Code Pro, Material Symbols Outlined)
  serif-scope   Merriweather outside an editorial article path
  serif-heading a serif on a heading-like selector, anywhere
  font-literal  a font named directly on a page instead of var(--font-*) (only variables.css may name families)
  font-size     text below 12px, anywhere (pages, inline styles, JS strings)
  font-weight   800 or 900
  pill-radius   border-radius 999px / 9999px
  color         a hex color (3, 4, 6 or 8 digits) whose base is not in the v16 palette (Tiers 1-5, Neutral and Cool scales)
  lime-text     Lime Green used as a text color
  color-alpha   a 4- or 8-digit hex whose base IS a palette color: transparency, for James to review
  color-func    rgb(), rgba(), hsl() or hsla() in CSS, inline styles or JS strings (values are not mapped to the palette).
                Pure white or black at any alpha is flagged ONLY as a text color (color, -webkit-text-fill-color, caret-color,
                fill/stroke on SVG or canvas text); in shadows, borders, backgrounds and overlays it is allowed.
                Any other rgb/hsl value is flagged wherever it appears.
  color-name    a CSS named color (red, orange, tomato...) as the value of a color-bearing property or attribute;
                white, black, transparent, currentColor and the CSS-wide keywords are not flagged
"""
import json, os, re, subprocess, sys
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
    "preview/nodes-and-networks-", "preview/nn-launch-kit/", "assets/nn5/", "nn/", "nodes-networks-v5/", "tools/preview-build/",
    # Internal mock of a Google Form (uses Roboto to match Google Forms)
    "atlas-portal/google-form-template.html",
)
SERIF_ARTICLE_PATHS = ("watershed/",)   # editorial articles: watershed/ and long-form report template pages (v16 § Exceptions)
# add the long-form report path here when the first report page is built (v16 § Exceptions)
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

HEX = re.compile(r"(?<![\w&])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b(?![\w-])(?![^;{}\n\"'<>$]*\{)")
# A "#..." that is an anchor, an id lookup or a CSS selector, not a color: preceded by one of these, or followed by "{"
HEX_REF_BEFORE = re.compile(r"(?:href\s*=|url\(|querySelector(?:All)?\(|closest\(|getElementById\()\s*['\"]?\s*$", re.I)
COLOR_FUNC = re.compile(r"\b(?:rgba?|hsla?)\s*\([^)\n]{0,40}\)?", re.I)
NAMED_COLORS = frozenset("""aliceblue antiquewhite aqua aquamarine azure beige bisque blanchedalmond blue blueviolet brown
burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray
darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue
darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite
forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory
khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen
lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime
limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue
mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive
olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue
slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat whitesmoke yellow
yellowgreen""".split())   # white and black are palette colors; transparent, currentColor and CSS-wide keywords are never flagged
COLOR_PROP = re.compile(r"(?<![\w-])(?:color|background(?:-color)?|border(?:-[a-z-]+)?|outline(?:-[a-z-]+)?|fill|stroke|text-decoration-color|box-shadow|caret-color|accent-color|column-rule-color)[ \t]*:[ \t]*([^;}{\n\"'<>]*)", re.I)
COLOR_ATTR = re.compile(r"(?<![\w-])(?:fill|stroke)\s*=\s*[\"']([^\"'<>]*)[\"']", re.I)
COLOR_JS = (
    re.compile(r"\.attr\(\s*['\"](?:fill|stroke)['\"]\s*,\s*['\"]([^'\"]*)['\"]"),
    re.compile(r"\.style\(\s*['\"](?:color|fill|stroke|background)['\"]\s*,\s*['\"]([^'\"]*)['\"]"),
    re.compile(r"\.style\.(?:color|fill|stroke|background(?:Color)?)\s*=\s*['\"`]([^'\"`]*)['\"`]"),
    re.compile(r"\.(?:fillStyle|strokeStyle)\s*=\s*['\"`]([^'\"`]*)['\"`]"),
)
TEXT_COLOR_PROPS = {"color", "-webkit-text-fill-color", "caret-color"}
JS_PROP_BEFORE = (
    re.compile(r"\.(?:attr|style)\(\s*['\"]([-\w]+)['\"]\s*,\s*['\"`]?$"),
    re.compile(r"\.style\.(\w+)\s*=\s*['\"`]?$"),
    re.compile(r"\.(fillStyle|strokeStyle)\s*=\s*['\"`]?$"),
    re.compile(r"setAttribute\(\s*['\"]([-\w]+)['\"]\s*,\s*['\"`]?$"),
)
SVG_ATTR_BEFORE = re.compile(r"(?<![\w-])(fill|stroke)\s*=\s*[\"']$")
CSS_DECL_BEFORE = re.compile(r"\s*(-{0,2}[\w-]+)\s*:")
TEXTY_SELECTOR = re.compile(r"(?<![\w-])(?:text|tspan)(?![\w-])", re.I)
COLOR_WORD = re.compile(r"(?<![\w#.-])[a-z]+(?![\w(-])")
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

def white_or_black(call):
    """True for rgb/rgba/hsl/hsla that is pure white or pure black at any alpha."""
    name, _, args = call.partition("(")
    nums = re.findall(r"[\d.]+%?", args)
    if len(nums) < 3:
        return False
    if name.strip().lower().startswith("rgb"):
        vals = [(float(n[:-1]) * 2.55 if n.endswith("%") else float(n)) for n in nums[:3]]
        return all(abs(v - 255) < 0.5 for v in vals) or all(v < 0.5 for v in vals)
    light = nums[2]
    return light.endswith("%") and float(light[:-1]) in (0.0, 100.0)

def is_text_color(text, pos):
    """Is the color function at pos the value of a text-color property (or fill/stroke/fillStyle of text)?"""
    ls = text.rfind("\n", 0, pos) + 1
    line_pre = text[ls:pos]
    prop = None
    for rx in JS_PROP_BEFORE:
        m = rx.search(line_pre)
        if m:
            prop = m.group(1)
            break
    kind = "js" if prop else None
    if prop is None:
        m = SVG_ATTR_BEFORE.search(line_pre)
        if m:
            prop, kind = m.group(1), "svg"
    if prop is None:
        seg = text[max(0, pos - 300):pos]
        cut = max(seg.rfind(c) for c in ";{}\"'")
        m = CSS_DECL_BEFORE.match(seg[cut + 1:])
        if m:
            prop, kind = m.group(1), "css"
    if prop is None:
        return False
    prop = {"fillstyle": "fill", "strokestyle": "stroke"}.get(prop.lower(), prop.lower())
    if prop in TEXT_COLOR_PROPS:
        return True
    if prop not in ("fill", "stroke"):
        return False
    if kind == "svg":
        tag = re.findall(r"<(\w+)", text[max(0, pos - 400):pos])
        return bool(tag) and tag[-1].lower() in ("text", "tspan")
    if kind == "css":
        brace = text.rfind("{", 0, pos)
        if brace == -1 or text.rfind("}", brace, pos) != -1:
            return False
        sel = text[max(text.rfind("}", 0, brace), text.rfind(";", 0, brace)) + 1:brace]
        return bool(TEXTY_SELECTOR.search(sel))
    back = re.findall(r"\.append\(\s*['\"](\w+)['\"]\s*\)|\.select(?:All)?\(\s*['\"]([^'\"]+)['\"]\s*\)", text[max(0, pos - 400):pos])
    if back:                                    # D3: the element the attr/style chain was last built on
        last = (back[-1][0] or back[-1][1]).lower()
        return bool(TEXTY_SELECTOR.search(last))
    ahead = re.search(r"fillText|strokeText|fillRect|strokeRect|\.fill\(|\.stroke\(|\.arc\(", text[pos:pos + 300])
    return bool(ahead) and ahead.group(0) in ("fillText", "strokeText")   # canvas

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
        if HEX_REF_BEFORE.search(text[max(0, m.start() - 60):m.start()]):
            continue  # anchor, id lookup or url(#ref), not a color
        h = m.group(1).lower()
        alpha = len(h) in (4, 8)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        elif len(h) == 8:
            h = h[:6]
        if h not in PALETTE:
            add("color", m.start(), "#" + m.group(1))
        elif alpha:
            add("color-alpha", m.start(), "#" + m.group(1))
    for m in COLOR_FUNC.finditer(text):
        if white_or_black(m.group(0)) and not is_text_color(text, m.start()):
            continue  # white or black in a shadow, border, background or overlay is allowed; only text colors are locked
        add("color-func", m.start(), m.group(0))
    def named(value, pos):
        value = re.sub(r"(?:var|url)\([^)]*\)", " ", value.lower())
        for w in COLOR_WORD.finditer(value):
            if w.group(0) in NAMED_COLORS:
                add("color-name", pos, w.group(0))
    for m in COLOR_PROP.finditer(text):
        named(m.group(1), m.start())
    for m in COLOR_ATTR.finditer(text):
        named(m.group(1), m.start())
    for rx in COLOR_JS:
        for m in rx.finditer(text):
            named(m.group(1), m.start())
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

def guard_baseline(ref):
    """CI only. Counts in the working baseline may not exceed the baseline at <ref>, unless check_brand.py itself changed."""
    def git(*a):
        return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True)
    if git("rev-parse", "--verify", "--quiet", ref + "^{commit}").returncode != 0:
        print(f"guard-baseline: git ref '{ref}' not found (CI needs fetch-depth: 0).", file=sys.stderr)
        return 2
    old = git("show", f"{ref}:scripts/brand-baseline.json")
    if old.returncode != 0:
        print(f"guard-baseline: no baseline at {ref}; nothing to compare. OK")
        return 0
    old = json.loads(old.stdout)
    new = json.load(open(BASELINE)) if os.path.exists(BASELINE) else {}
    raised = [(f, r, n, old.get(f, {}).get(r, 0)) for f, rules in new.items() for r, n in rules.items()
              if n > old.get(f, {}).get(r, 0)]
    if not raised:
        print("guard-baseline: OK (no count went up)")
        return 0
    if git("diff", "--name-only", ref, "--", "scripts/check_brand.py").stdout.strip():
        print("guard-baseline: counts went up, allowed because scripts/check_brand.py changed in this pull request.")
        return 0
    for f, r, n, o in raised:
        print(f"  {f}: {r} {n} (was {o} at {ref})")
    print("\nBaseline went up. Counts may only fall unless check_brand.py changed in the same pull request.")
    return 1

def main():
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--guard-baseline" or a.startswith("--guard-baseline="):
            if a == "--guard-baseline":
                if i + 1 >= len(argv):
                    print("--guard-baseline needs a git ref", file=sys.stderr)
                    return 2
                return guard_baseline(argv[i + 1])
            return guard_baseline(a.split("=", 1)[1])
    flags = {a for a in argv if a.startswith("--")}
    paths = [a for a in argv if not a.startswith("--")]
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
    if "--report" in flags:
        by_rule = defaultdict(int)
        for rules in counts.values():
            for r, n in rules.items():
                by_rule[r] += n
        print("By rule:")
        for r, n in sorted(by_rule.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {r:14} {n}")
    if new and "--report" not in flags:
        print("\nFAILED: new violations of DESIGN-TOKENS-v16 (above). Use a token from docs/design/DESIGN-TOKENS-v16.md.")
        for f, r, n, a in new:
            print(f"  {f}: {r} {n} (baseline {a})")
        return 1
    if "--tight" in flags and not strict:
        loose = [(f, r, counts.get(f, {}).get(r, 0), a) for f, rules in base.items() for r, a in rules.items()
                 if counts.get(f, {}).get(r, 0) < a or not os.path.exists(os.path.join(ROOT, f))]
        if loose:
            for f, r, n, a in loose:
                print(f"  {f}: {r} {n} (baseline {a})" + ("" if os.path.exists(os.path.join(ROOT, f)) else "  [file no longer exists]"))
            print("\nBaseline is loose: run python3 scripts/check_brand.py --write-baseline and include scripts/brand-baseline.json in this change.")
            return 1
    print("OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
