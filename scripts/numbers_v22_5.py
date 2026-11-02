#!/usr/bin/env python3
"""Every published number for Nodes and Networks, computed from v22.5 only.

Reads cohort_reference_expanded_v22.5.csv (read-only) and writes qa/numbers-v22.5.md.
Usage: python3 scripts/numbers_v22_5.py [--csv PATH] [--out PATH]
Default csv: ../paper-one-band-dataset/cohort_reference_expanded_v22.5.csv (a sibling checkout of this repo).

Definitions
  Rows        the 169 rows with a Band_Position (BELOW_BAND < $3.5M, IN_BAND $3.5M to $10M inclusive, ABOVE_BAND > $10M).
  Origin      Origin_Position: BORN_ABOVE = started above $10M (INHERITED), CROSSED = grew past, NEVER_CROSSED = under $10M.
              Grew past + started above = the 55 above-band rows; "under" = the 114 below/in-band rows.
  Wedges      the explorer's "6 ways" tab: started-above rows form one section (INHERITED_SCALE) whatever their M-code; crossed rows
              count under their published mechanism (Mechanism_Published, copied from nn/data/public-snapshot.json); below-band rows are BELOW.
  History     founding year before 1995 vs 1995 and after (the explorer's M.cut). A row with an unknown founding year is excluded
              from the history counts and from the era test.
  Cramer's V  V = sqrt(chi2 / (n * (min(r, c) - 1))), chi2 = sum (O - E)^2 / E with E = row total x column total / n, no continuity
              correction. df = (r - 1)(c - 1). p = upper tail of the chi-square distribution (regularised incomplete gamma, implemented
              here; no scipy). Also shown: the bias-corrected V (Bergsma 2013) for comparison with the earlier audit sheets.
              Tests: cohort (9) x band (3), n = 169; era (before 1995 / since) x band (3), n = 168 (Radio Jornalera NJ has no founding year).
              Expected counts below 5 are common in the cohort x band table (reported), so treat the p value as approximate.
"""
import csv, math, os, sys, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ARG = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
CSV = ARG("--csv", os.path.join(HERE, "..", "..", "paper-one-band-dataset", "cohort_reference_expanded_v22.5.csv"))
OUT = ARG("--out", os.path.join(HERE, "..", "qa", "numbers-v22.5.md"))
CUT = 1995

# OLD: the live explorer before v22.5 (preview/nn-launch-kit/explorer/index.html at commit 74d5e01) and the paper's known values.
OLD = {
    "N": 169, "bands_pct": (47.1, 20.0, 32.9), "bands_n": (80, 34, 55),
    "grew": 30, "started": 25, "under": 114,
    "cohorts": {"C1": 18, "C2": 26, "C3": 8, "C4": 44, "C5": 14, "C6": 8, "C7": 7, "C8": 27, "C9": 17},
    "cohort_band": {"C1": (0, 0, 18), "C2": (18, 5, 3), "C3": (3, 2, 3), "C4": (21, 13, 10), "C5": (3, 2, 9), "C6": (5, 2, 1), "C7": (6, 1, 0), "C8": (20, 7, 0), "C9": (4, 2, 11)},
    "wedges": {"M1": 0, "M2": 2, "M3": 10, "M4": 9, "M5": 7, "M6": 2, "INHERITED_SCALE": 25, "BELOW": 114},
    "pre": (24, 38), "post_over": (31, 130), "post_under": (99, 130),
    "V_cohort": 0.503, "V_era": 0.384,
}
# v22 data (explorer before v22.5) run through the same tests, to separate data change from method change.
V22_TABLES = {"cohort": [[0, 0, 18], [18, 5, 3], [3, 2, 3], [21, 13, 10], [3, 2, 9], [5, 2, 1], [6, 1, 0], [20, 7, 0], [4, 2, 11]],
              "era": [[11, 3, 24], [68, 31, 31]]}
NAMES = {"C1": "Legacy Publishers", "C2": "Creator Brands", "C3": "Barbell Hybrids", "C4": "Philanthropic Networks", "C5": "Public Media",
         "C6": "Collaboration Layers", "C7": "Worker Co-ops", "C8": "Civic & Community", "C9": "B2B & Professional"}
BANDS = ("BELOW_BAND", "IN_BAND", "ABOVE_BAND")
ORIG = {"BORN_ABOVE": "INHERITED", "CROSSED": "CROSSED", "NEVER_CROSSED": "NEVER_CROSSED"}
MCODE = lambda m: m.split("_")[0] if m.startswith("M") else m

# ---------- statistics ----------
def gammaincc(a, x):
    """Regularised upper incomplete gamma Q(a, x) (series for x < a+1, continued fraction otherwise)."""
    if x <= 0: return 1.0
    gln = math.lgamma(a)
    if x < a + 1:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1; d *= x / ap; s += d
            if abs(d) < abs(s) * 1e-15: break
        return 1.0 - s * math.exp(-x + a * math.log(x) - gln)
    b = x + 1 - a; c = 1e300; d = 1.0 / b; h = d
    for i in range(1, 1000):
        an = -i * (i - a); b += 2; d = an * d + b; d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c; c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1) < 1e-15: break
    return math.exp(-x + a * math.log(x) - gln) * h

def cramers(tab):
    r, c = len(tab), len(tab[0]); n = sum(map(sum, tab))
    rs = [sum(row) for row in tab]; cs = [sum(tab[i][j] for i in range(r)) for j in range(c)]
    exp = [[rs[i] * cs[j] / n for j in range(c)] for i in range(r)]
    chi = sum((tab[i][j] - exp[i][j]) ** 2 / exp[i][j] for i in range(r) for j in range(c))
    df = (r - 1) * (c - 1); k = min(r, c) - 1
    v = math.sqrt(chi / (n * k))
    phi2 = chi / n; phi2c = max(0.0, phi2 - df / (n - 1)); rc = r - (r - 1) ** 2 / (n - 1); cc = c - (c - 1) ** 2 / (n - 1)
    vc = math.sqrt(phi2c / (min(rc, cc) - 1))
    return dict(V=v, V_bc=vc, chi2=chi, df=df, p=gammaincc(df / 2, chi / 2), n=n, small=sum(1 for row in exp for e in row if e < 5), cells=r * c)

# ---------- load ----------
raw = open(CSV, "rb").read()
import io
rows = [r for r in csv.DictReader(io.StringIO(raw.decode("utf-8"), newline="")) if r["Band_Position"]]
assert len(rows) == 169, len(rows)
N = len(rows)
bi = lambda r: BANDS.index(r["Band_Position"])
fy = lambda r: int(float(r["Founding_Year"])) if r["Founding_Year"].replace(".0", "").isdigit() else None
for r in rows:
    r["_o"] = ORIG[r["Origin_Position"]]; r["_b"] = bi(r); r["_fy"] = fy(r)
    assert (r["_b"] == 2) == (r["_o"] != "NEVER_CROSSED"), r["Organization / Creator"]   # origin tags only on above-band rows

# ---------- numbers ----------
bands_n = tuple(sum(1 for r in rows if r["_b"] == b) for b in range(3))
bands_pct = tuple(round(100 * x / N, 1) for x in bands_n)
grew = sum(1 for r in rows if r["_o"] == "CROSSED"); started = sum(1 for r in rows if r["_o"] == "INHERITED"); under = N - grew - started
cohorts = collections.Counter(r["Cohort"] for r in rows)
cband = {c: tuple(sum(1 for r in rows if r["Cohort"] == c and r["_b"] == b) for b in range(3)) for c in sorted(NAMES)}
wedges = collections.Counter()
for r in rows:
    wedges["INHERITED_SCALE" if r["_o"] == "INHERITED" else ("BELOW" if r["_b"] < 2 else MCODE(r["Mechanism_Published"]))] += 1
wedges = {k: wedges.get(k, 0) for k in ("M1", "M2", "M3", "M4", "M5", "M6", "INHERITED_SCALE", "BELOW")}
pre = [r for r in rows if r["_fy"] and r["_fy"] < CUT]; post = [r for r in rows if r["_fy"] and r["_fy"] >= CUT]
nofy = [r["Organization / Creator"] for r in rows if not r["_fy"]]
pre_over = (sum(r["_b"] == 2 for r in pre), len(pre)); post_over = (sum(r["_b"] == 2 for r in post), len(post))
post_under = (len(post) - post_over[0], len(post))
V_c = cramers([[cband[c][b] for b in range(3)] for c in sorted(NAMES)])
era_tab = [[sum(1 for r in grp if r["_b"] == b) for b in range(3)] for grp in (pre, post)]
V_e = cramers(era_tab)
V_c22 = cramers(V22_TABLES["cohort"]); V_e22 = cramers(V22_TABLES["era"])
assert math.isclose(gammaincc(1, 3.0), math.exp(-3.0), rel_tol=1e-12)   # df = 2 check: Q(1, x) = exp(-x)

# ---------- grant dependency (paper claim) ----------
# "17 of 18 in-band nonprofits with computable grant data are more than 78% grant-dependent (range 82.5-102.3%); Colorado Sun the exception."
# Population A: every IN_BAND row with a Grant_Dependency_Pct (contributions / total revenue, Part VIII line 1h / line 12 of the cited filing).
# Population B: A restricted to rows with a 990 EIN (drops St. Louis Public Radio, a university unit whose figure comes from audited statements).
GD_T = 78.0
def gd_stats(pop):
    over = [(n_, p) for n_, p in pop if p > GD_T]; under = [(n_, p) for n_, p in pop if p <= GD_T]
    return dict(n=len(pop), over=len(over), lo=min(p for _, p in over), hi=max(p for _, p in over), exc=sorted(under, key=lambda x: x[1]))
gd_all = [(r["Organization / Creator"], float(r["Grant_Dependency_Pct"]), r["990_EIN"]) for r in rows if r["_b"] == 1 and r["Grant_Dependency_Pct"]]
GD_A = gd_stats([(a, b) for a, b, _ in gd_all]); GD_B = gd_stats([(a, b) for a, b, e in gd_all if e[:2].isdigit()])
V22_GD = dict(n=18, over=16, lo=78.4, hi=99.3, exc="Colorado Sun (49.1), LION Publishers (71.6)")   # v22 as built: same test on the v22 file
OLD_GD = ("17 of 18", "82.5-102.3%", "Colorado Sun")

# ---------- report ----------
f1 = lambda x: f"{x:.1f}"; f3 = lambda x: f"{x:.3f}"
def pfmt(p): return "< 0.0001" if p < 1e-4 else f"{p:.4f}"
L = []
L.append(f"# Numbers, v22.5\n\nGenerated by `scripts/numbers_v22_5.py` from `{os.path.basename(CSV)}` (md5 `{hashlib.md5(raw).hexdigest()}`). No other input. Method notes are in the script header.\n")
L.append("## N, bands, origin\n")
L.append(f"- N = **{N}**\n- Band: below $3.5M **{bands_n[0]}** ({f1(bands_pct[0])}%) / $3.5M to $10M **{bands_n[1]}** ({f1(bands_pct[1])}%) / above $10M **{bands_n[2]}** ({f1(bands_pct[2])}%)")
L.append(f"- Grew past $10M **{grew}**; started above $10M **{started}**; under $10M **{under}**")
L.append(f"- Started above, share of the {grew + started} over-$10M rows: **{started} of {grew + started} = {f1(100 * started / (grew + started))}%**\n")
L.append("## Cohorts\n\n| cohort | name | all | below $3.5M | $3.5M-$10M | above $10M |\n|---|---|---|---|---|---|")
for c in sorted(NAMES): L.append(f"| {c} | {NAMES[c]} | {cohorts[c]} | {cband[c][0]} | {cband[c][1]} | {cband[c][2]} |")
L.append(f"| all | | {N} | {bands_n[0]} | {bands_n[1]} | {bands_n[2]} |\n")
L.append("## Mechanism wedges (explorer 6 ways tab)\n\n| wedge | count |\n|---|---|")
for k, v in wedges.items(): L.append(f"| {k} | {v} |")
L.append(f"\nSum = {sum(wedges.values())}. M1 (bundle) is empty by design: every row selling a bundle started above $10M. The M-codes on started-above rows do not enter these counts.\n")
L.append("## History dek\n")
L.append(f"- Founded before {CUT}, over $10M: **{pre_over[0]} of {pre_over[1]}**\n- Founded {CUT} or later, over $10M: **{post_over[0]} of {post_over[1]}**\n- Founded {CUT} or later, under $10M: **{post_under[0]} of {post_under[1]}**\n- Excluded (founding year unknown): {', '.join(nofy)} ({len(nofy)} row)\n")
L.append("## Cramér's V\n")
L.append("Method in the script header. Era test excludes the one row with no founding year, so n = 168.\n")
L.append("| test | V | bias-corrected V | chi-square | df | p | n | cells with expected < 5 |\n|---|---|---|---|---|---|---|---|")
for nm, v in (("cohort (9) x band (3)", V_c), ("era (before / since 1995) x band (3)", V_e)):
    L.append(f"| {nm} | {f3(v['V'])} | {f3(v['V_bc'])} | {v['chi2']:.2f} | {v['df']} | {pfmt(v['p'])} | {v['n']} | {v['small']} of {v['cells']} |")
L.append(f"\nEra table (rows before / since; columns below / in / above): {era_tab}.\n")
L.append("v22 data (the live explorer before this version) through the same tests: "
         f"cohort V {f3(V_c22['V'])} (chi-square {V_c22['chi2']:.2f}, n {V_c22['n']}), era V {f3(V_e22['V'])} (chi-square {V_e22['chi2']:.2f}, n {V_e22['n']}). "
         "The older 0.503 and 0.384 are not reproduced by either dataset: 0.503 is the N = 170 value (`andy_decision_sheet_v22_1.md`: 0.503 to 0.490 at N = 169), and the origin of 0.384 (probably a different era binning) is not documented in the files I could read. Treat the OLD column below as the paper's printed values and the v22 column as the like-for-like comparison.\n")

L.append("## Grant dependency of in-band nonprofits\n")
L.append("Paper claim: 17 of 18 in-band nonprofits with computable grant data are more than 78% grant-dependent, range 82.5-102.3%, Colorado Sun the exception. "
         "Grant dependency = Part VIII contributions (line 1h) / total revenue (line 12) of the cited filing; threshold strictly above 78.0.\n")
excs = lambda g: ", ".join(f"{a} ({b:.1f})" for a, b in g["exc"])
L.append("| population | with data | above 78% | range of those above | at or below 78% |\n|---|---|---|---|---|")
L.append(f"| A: every in-band row with a value | {GD_A['n']} | {GD_A['over']} | {GD_A['lo']:.1f}-{GD_A['hi']:.1f}% | {excs(GD_A)} |")
L.append(f"| B: A with a 990 EIN (drops St. Louis Public Radio) | {GD_B['n']} | {GD_B['over']} | {GD_B['lo']:.1f}-{GD_B['hi']:.1f}% | {excs(GD_B)} |\n")
L.append("Neither population reproduces the paper's 17 of 18 or its 82.5-102.3% range. Two exceptions, not one: LION Publishers is at 71.6% (its FY2025 990 total is $4.6M; the v22 notes say 71.6 was verified unchanged). The 78.4% for St. Louis Public Radio is from the university's audited statements, not a 990, and it is the low end of the range in A. The 102.3% in the paper is not in v22 or v22.5 for any in-band row (the largest is 99.3, Wisconsin Watch; First Look Institute at 100.2% is under $3.5M). Cityside (82.5 to 86.4) and MuckRock (87.5 to 90.0) changed with the FY2025 refresh; neither changes the count. MinnPost (91.9 to 84.5) and Migrant Roots are not in-band, so they do not enter.\n")

# OLD -> NEW
def row(label, old, new, search, same_v22=None):
    flag = "same" if str(old) == str(new) else "**changed**"
    L.append(f"| {label} | {old} | {new} | {flag} | {same_v22 if same_v22 is not None else ''} | {search} |")
L.append("## OLD to NEW\n\nOLD = the live explorer before v22.5 and the paper's known values. Search strings are for finding the OLD value in the paper (try each; the paper's exact wording is not available to me, so strings are the number as written plus the nearest unit).\n")
L.append("| number | OLD | NEW | status | v22 recomputed (same method) | search for OLD in the paper |\n|---|---|---|---|---|---|")
row("N", OLD["N"], N, "`169`")
for i, nm in enumerate(("below $3.5M %", "$3.5M-$10M %", "above $10M %")):
    row(nm, f"{OLD['bands_pct'][i]:.1f}", f1(bands_pct[i]), f"`{OLD['bands_pct'][i]:.1f}%` ; `{OLD['bands_pct'][i]:.1f} percent`", f"{100 * OLD['bands_n'][i] / 169:.1f}")
for i, nm in enumerate(("below $3.5M n", "$3.5M-$10M n", "above $10M n")):
    row(nm, OLD["bands_n"][i], bands_n[i], f"`{OLD['bands_n'][i]} organizations` ; `{OLD['bands_n'][i]} of 169`")
row("grew past $10M", OLD["grew"], grew, "`30 grew` ; `30 organizations` ; `grew past $10M (30)`")
row("started above $10M", OLD["started"], started, "`25 started` ; `started above $10M (25)` ; `25 of the 55`")
row("under $10M", OLD["under"], under, "`114 under` ; `Under $10M 114` ; `114 organizations`")
row("started above, share of over $10M", "25 of 55 = 45.5%", f"{started} of {grew + started} = {f1(100 * started / (grew + started))}%", "`25 of 55` ; `45.5%` ; `more than four in ten`")
for c in sorted(NAMES):
    row(f"{c} {NAMES[c]}", OLD["cohorts"][c], cohorts[c], f"`{NAMES[c]} ({OLD['cohorts'][c]})` ; `{c} · {NAMES[c]} {OLD['cohorts'][c]}` ; `{OLD['cohorts'][c]} {NAMES[c].lower()}`")
for c in sorted(NAMES):
    row(f"{c} over $10M", f"{OLD['cohort_band'][c][2]} of {OLD['cohorts'][c]}", f"{cband[c][2]} of {cohorts[c]}", f"`{OLD['cohort_band'][c][2]} of {OLD['cohorts'][c]} over $10M`")
for k in wedges:
    row(f"wedge {k}", OLD["wedges"][k], wedges[k], f"`{OLD['wedges'][k]}` beside the {k} mechanism name")
row("before 1995 over $10M", "24 of 38", f"{pre_over[0]} of {pre_over[1]}", "`24 of 38`")
row("since 1995 over $10M", "31 of 130", f"{post_over[0]} of {post_over[1]}", "`31 of 130`")
row("since 1995 under $10M", "99 of 130", f"{post_under[0]} of {post_under[1]}", "`99 of 130`")
row("Cramér's V, cohort x band", f"{OLD['V_cohort']:.3f}", f3(V_c["V"]), "`0.503` ; `.503` ; `V = 0.503`", f3(V_c22["V"]))
row("Cramér's V, era x band", f"{OLD['V_era']:.3f}", f3(V_e["V"]), "`0.384` ; `.384` ; `V = 0.384`", f3(V_e22["V"]))
row("grant dependency: in-band nonprofits above 78%", OLD_GD[0], f"{GD_A['over']} of {GD_A['n']}", "`17 of 18` ; `more than 78` ; `78%`", f"{V22_GD['over']} of {V22_GD['n']}")
row("grant dependency: range of those above 78%", OLD_GD[1], f"{GD_A['lo']:.1f}-{GD_A['hi']:.1f}%", "`82.5` ; `102.3` ; `82.5 to 102.3`", f"{V22_GD['lo']}-{V22_GD['hi']}%")
row("grant dependency: exceptions", OLD_GD[2], excs(GD_A), "`Colorado Sun`", V22_GD["exc"])
L.append("\nIf a row says `same`, nothing to change for that number. Rows marked **changed** whose v22 column already equals NEW are method or count-basis corrections, not v22.5 data changes: the 47.1 / 20.0 / 32.9 split is the N = 170 split (80/34/56 of 170) and the current 169 rows give 47.3 / 20.1 / 32.5.\n")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", os.path.abspath(OUT))
