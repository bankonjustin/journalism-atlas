// Stage for the launch video. Uses the explorer's own NN engine, data and layouts (extracted from index.html at render time).
const D = JSON.parse(document.getElementById('nn-data').textContent), N = D.nodes, M = D.meta, L = NN.build(D);
const T = { bg: '#000', a: '#F6C84E', b: '#B23A5E', c: '#A8A8A8', neutral: '#7C7C7C', ink: '#fff', ink2: '#bdbdbd', grid: '#262626' };
const W = window.W, Hh = window.H, cl = NN.cl, ss = NN.ss, eio = NN.eio, TAU = Math.PI * 2;
const REST = window.REST, F = REST.R / 311, r = x => x * F;
const cv = document.getElementById('st'), ctx = cv.getContext('2d'), out = document.getElementById('out'), octx = out.getContext('2d');
const PF = L.scatter.pos, PG = L.gov.pos, PW = L.ways.pos;
const TL = window.TL;   // timeline (ms), injected
const NAMES = window.NAMES;
const idx = nm => N.findIndex(n => n.nm.includes(nm));
const lerp = (a, b, k) => a + (b - a) * k;
// angular stagger like the explorer's own morph
const stag = (g) => ((Math.atan2(g.y, g.x) + Math.PI / 2 + 4 * Math.PI) % TAU) / TAU * .3;
function flight(from, to, k) {   // per-mark positions and progress
  const pos = [], e = [];
  for (let i = 0; i < N.length; i++) { const f = from[i], g = to[i], del = stag(g), ee = eio(cl((k - del) / .7)); pos.push({ x: lerp(f.x, g.x, ee), y: lerp(f.y, g.y, ee) }); e.push(ee); }
  return { pos, e };
}
let HP = null, HS = 1, HOX = 0, HTOP = 0, HR = 4.3;
function histUnit(cam) {   // unit coords (relative to camera) of each mark's slot in the real History chart
  return N.map(n => { const p = HP[n.i]; if (!p) return null; return { x: (HOX + p[0] * HS - cam.cx) / cam.R, y: (HTOP + p[1] * HS - cam.cy) / cam.R }; });
}
function mirrorExtra(alpha, pos, rot) {
  return (c, G, rp) => {
    if (alpha <= 0.002) return; const seg = Math.PI / 9;
    N.forEach((n, i) => { const p = pos[i], r = Math.hypot(p.x, p.y); let a = Math.atan2(p.y, p.x) + rot; a = ((a % TAU) + TAU) % TAU; const k = Math.floor(a / seg); let loc = a - k * seg; if (k % 2) loc = seg - loc;
      c.globalAlpha = alpha * .85; c.fillStyle = NN.mixc(T.neutral, '#BDBDBD', Math.min(1, r)); const s = L.MR * G.R * .4;
      for (let j = 0; j < 18; j++) { const ang = j * seg + (j % 2 ? seg - loc : loc); c.beginPath(); c.arc(G.cx + Math.cos(ang) * r * G.R, G.cy + Math.sin(ang) * r * G.R, s, 0, TAU); c.fill(); } });
    c.globalAlpha = 1;
  };
}
function nameExtra(lit, G0) {   // rings + leader + name pills for lit organizations
  return (c, G, rp) => {
    lit.forEach(({ i, a, label, dx, dy }) => {
      if (a <= .01) return; const [x, y] = rp(S_pos[i].x, S_pos[i].y), r = L.MR * G.R * G.boost;
      c.globalAlpha = a; c.strokeStyle = '#fff'; c.lineWidth = 2.4; c.beginPath(); c.arc(x, y, r * 2.1, 0, TAU); c.stroke();
      const fs = 27 * F; c.font = '700 ' + fs + 'px Arial, Helvetica, sans-serif'; c.textBaseline = 'middle';
      const w = c.measureText(label).width + 26, h = fs + 18, lx = x + dx * F, ly = y + dy * F;
      const bx = dx >= 0 ? lx : lx - w; c.strokeStyle = 'rgba(255,255,255,.8)'; c.lineWidth = 1.6; c.beginPath(); c.moveTo(x + Math.sign(dx || 1) * r * 2.1 * .7, y + Math.sign(dy || -1) * r * 2.1 * .7); c.lineTo(dx >= 0 ? lx : lx, ly); c.stroke();
      c.fillStyle = '#fff'; c.beginPath(); c.roundRect(bx, ly - h / 2, w, h, 8); c.fill();
      c.fillStyle = '#000'; c.textAlign = 'left'; c.fillText(label, bx + 13, ly + 1);
    });
    c.globalAlpha = 1;
  };
}
let S_pos = PG;
function stateAt(t) {
  const tl = TL, rest = { ...REST };
  let cam = { ...rest, rot: 0 }, pos, ce = 0, mutedA = 0, labelsTab = null, spokes = null, labelA = 0, chromeA = 0, appear = null, hl = null, boost = 1, extra = null, fadeA = 1;
  const base = i => 1;
  const ceArr = N.map(() => 0);
  if (t < tl.flyGov0) {                                  // 1. pooled field (neutral) + mirror flourish
    const k = t / tl.flyGov0; cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(282), r(306), ss(0, 1, k)), rot: .9 * Math.PI * (.55 * k + .45 * eio(k)) };
    pos = PF; const mir = ss(tl.mir0, tl.mir0 + .3 * 1000, t) * (1 - ss(tl.flyGov0 - .45 * 1000, tl.flyGov0, t));
    appear = N.map(() => 1 - .85 * mir); extra = mirrorExtra(mir, pos, cam.rot);
  } else if (t < tl.flyGov1) {                           // 2. turn into the nine cohort wedges
    const k = (t - tl.flyGov0) / (tl.flyGov1 - tl.flyGov0), f = flight(PF, PG, k); pos = f.pos; f.e.forEach((e, i) => ceArr[i] = ss(.78, 1, e));
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(306), r(330), eio(k)), rot: lerp(.9 * Math.PI, TAU, eio(k)) };
    labelsTab = 'gov'; spokes = 'gov'; labelA = chromeA = ss(.55, 1, k);
  } else if (t < tl.flyWays0) {                          // 3. governance: ceilings
    const k = (t - tl.flyGov1) / (tl.flyWays0 - tl.flyGov1); pos = PG; ceArr.fill(1);
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(330), r(346), ss(0, 1, k)), rot: 0 }; labelsTab = 'gov'; spokes = 'gov'; labelA = chromeA = 1;
    const cohOf = n => n.c, selA = tl.ceil.c1, selB = tl.ceil.c78;
    const fa = ss(selA[0], selA[0] + 350, t) * (1 - ss(selA[1] - 250, selA[1], t)), fb = ss(selB[0], selB[0] + 350, t) * (1 - ss(selB[1] - 250, selB[1], t));
    const any = Math.max(fa, fb);
    appear = N.map(n => { const on = n.c === 'C1' ? fa : (n.c === 'C7' || n.c === 'C8') ? fb : 0; return 1 - .78 * any * (1 - on); });
  } else if (t < tl.flyWays1) {                          // 4a. turn to the six ways
    const k = (t - tl.flyWays0) / (tl.flyWays1 - tl.flyWays0), f = flight(PG, PW, k); pos = f.pos; ceArr.fill(1);
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(346), r(311), eio(k)), rot: .55 * Math.sin(Math.PI * eio(k)) * -1 };
    const swap = k < .3; labelsTab = swap ? 'gov' : 'ways'; spokes = labelsTab; labelA = chromeA = swap ? 1 - ss(0, .3, k) : ss(.55, 1, k);
    mutedA = ss(0, .7, k);
  } else if (t < tl.beat5) {                             // 4b. names light in sequence
    const k = (t - tl.flyWays1) / (tl.beat5 - tl.flyWays1); pos = PW; ceArr.fill(1); mutedA = 1;
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(311), r(322), ss(0, .8, k)) * 1 - (t > tl.beat5 - 450 ? (322 - 311) * ss(tl.beat5 - 450, tl.beat5, t) : 0), rot: 0 };
    labelsTab = 'ways'; spokes = 'ways'; labelA = chromeA = 1;
    const lit = NAMES.map(o => { const a = ss(o.t0, o.t0 + 220, t) * (1 - ss(o.t1 - 200, o.t1, t)); return { ...o, a }; });
    const any = Math.max(0, ...lit.map(o => o.a));
    appear = N.map((n, i) => { const o = lit.find(q => q.i === i); const on = o ? o.a : 0; return n.o === 'CROSSED' ? 1 - .72 * any * (1 - on) : 1 - .35 * any * 0; });
    extra = nameExtra(lit);
  } else if (t < tl.flyHist0) {                          // beat 5 happens in the real explorer; hold the rest state
    pos = PW; ceArr.fill(1); mutedA = 1; labelsTab = 'ways'; spokes = 'ways'; labelA = chromeA = 1;
  } else if (t < tl.flyHist1) {                          // 6. turn to founding year (marks fly to where the History chart puts them)
    const k = (t - tl.flyHist0) / (tl.flyHist1 - tl.flyHist0), H = histUnit(rest), tgt = N.map((n, i) => H[i] || PW[i]), f = flight(PW, tgt, k); pos = f.pos; ceArr.fill(1);
    cam = { ...rest, rot: 0 }; mutedA = 1 - ss(0, .7, k); const swap = k < .3; labelsTab = 'ways'; spokes = 'ways'; labelA = chromeA = 1 - ss(0, .3, k);
    boost = lerp(1, HR * HS / (L.MR * rest.R), eio(k)); appear = N.map((n, i) => H[i] ? 1 : 1 - ss(0, .5, k));
  } else if (t < tl.rosette0) {                          // history hold (real chart cross-faded in by the compositor)
    const H = histUnit(rest); pos = N.map((n, i) => H[i] || PW[i]); ceArr.fill(1); boost = HR * HS / (L.MR * rest.R); appear = N.map((n, i) => H[i] ? 1 : 0);
  } else if (t < tl.rosette1) {                          // 7. settle into the rosette
    const k = (t - tl.rosette0) / (tl.rosette1 - tl.rosette0), H = histUnit(rest), src = N.map((n, i) => H[i] || PW[i]), f = flight(src, PG, k); pos = f.pos; ceArr.fill(1);
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(311), r(330), eio(k)), rot: lerp(-.5 * Math.PI, 0, eio(k)) }; boost = lerp(HR * HS / (L.MR * rest.R), 1, eio(k)); labelsTab = 'gov'; spokes = 'gov'; labelA = chromeA = ss(.55, 1, k);
    appear = N.map((n, i) => H[i] ? 1 : ss(.3, 1, k));
  } else {
    const k = cl((t - tl.rosette1) / (tl.end - tl.rosette1)); pos = PG; ceArr.fill(1);
    cam = { cx: REST.cx, cy: REST.cy, R: lerp(r(330), r(345), ss(0, 1, k)), rot: .1 * Math.sin(k * Math.PI) * 0 }; labelsTab = 'gov'; spokes = 'gov'; labelA = chromeA = 1;
  }
  S_pos = pos;
  const G = { w: W, h: Hh, cx: cam.cx, cy: cam.cy, R: cam.R, dpr: 2, narrow: false, boost };
  const st = { pos, ceArr, mutedA, labelsTab, spokes, labelA, chromeA, rot: cam.rot, hl: null, appear, extra };
  return { G, st };
}
window.renderAt = t => {
  const { G, st } = stateAt(t); NN.draw(ctx, G, D, L, T, st);
  octx.imageSmoothingQuality = 'high'; octx.drawImage(cv, 0, 0, W, Hh);
  return out.toDataURL('image/png').slice(22);
};
window.setHist = (hp, hs, hox, htop, r) => { HP = hp; HS = hs; HOX = hox; HTOP = htop; HR = r; };
window.placement = () => NAMES.map(o => { const n = N[o.i], k = L.ways.geo.findIndex(g => g.members.includes(o.i)); return { name: n.nm, cohort: n.c, origin: n.o, mech: n.m, wedge: k < 6 ? (k + 1) + ' · ' + M.paths[k].short : L.ways.geo[k].key, rev: n.rv }; });
window.ready = true;
