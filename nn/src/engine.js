// Nodes and Networks launch-kit engine: deterministic layouts and a canvas renderer shared by the explorer and the video capture page.
// Encoding: colour = governance group (3), shape = path to size (circle under $10M, square started above, triangle grew past), all marks the same size.
const NN = (() => {
  const TAU = Math.PI * 2, MR = .03;                                   // mark radius in stage units (R = 1)
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ss = (a, b, t) => { const x = cl((t - a) / (b - a)); return x * x * (3 - 2 * x); };
  const eio = x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  const wayKey = n => (n.o === 'INHERITED' ? 'INHERITED_SCALE' : n.m);
  const SHAPE = { INHERITED: 'sq', CROSSED: 'tri', NEVER_CROSSED: 'ci' };
  
  function fill(g, s, r0) {                                            // pack a group into concentric arcs, inside out
    const n = g.members.length, out = []; let k = 0, placed = 0, r = r0;
    while (placed < n) {
      r = r0 + k * s * .9;
      const cap = Math.max(1, Math.floor((g.a1 - g.a0) * r / s)), take = Math.min(cap, n - placed);
      const step = take < cap ? s / r : (g.a1 - g.a0) / cap, mid = (g.a0 + g.a1) / 2;
      for (let j = 0; j < take; j++) { const a = mid - step * (take - 1) / 2 + step * j; out.push([g.members[placed + j], Math.cos(a) * r, Math.sin(a) * r]); }
      placed += take; k++;
    }
    return { pts: out, outer: r };
  }
  function pack(groups, nodes) {
    const order = { NEVER_CROSSED: 0, CROSSED: 1, INHERITED: 2 };
    groups.forEach(g => g.members.sort((i, j) => order[nodes[i].o] - order[nodes[j].o] || (nodes[i].fy || 0) - (nodes[j].fy || 0) || i - j));
    let s = .17, res;
    for (let t = 0; t < 40; t++) { res = groups.map(g => fill(g, s, .17)); if (Math.max(...res.map(r => r.outer)) <= .93) break; s *= .97; }
    const pos = []; res.forEach(r => r.pts.forEach(([i, x, y]) => { pos[i] = { x, y }; }));
    return { pos, s };
  }

  function build(D) {
    const N = D.nodes, M = D.meta, L = {};
    // governance: wedges per cohort
    const govGeo = D.gov.map(g => ({ ...g, members: N.filter(n => n.c === g.key).map(n => n.i) }));
    L.gov = { geo: govGeo, ...pack(govGeo, N) };
    // six ways: six path sectors, the exception, started above, under $10M (weights give every labelled sector room)
    const keys = [...M.paths.map(p => p.key), 'EXCEPTION_PLATFORM_LICENSING', ...(N.some(n => n.o === 'INHERITED') ? ['INHERITED_SCALE'] : []), 'BELOW'];
    const mem = k => N.filter(n => wayKey(n) === k).map(n => n.i);
    const W = keys.map((k, x) => x < 6 ? 24 : k === 'EXCEPTION_PLATFORM_LICENSING' ? 18 : Math.max(14, mem(k).length + 12));
    const gap = .04, tot = W.reduce((a, b) => a + b, 0), unit = (TAU - gap * keys.length) / tot, ub = keys.indexOf('BELOW');
    const before = W.slice(0, ub).reduce((a, b) => a + b, 0) * unit + gap * ub, start = Math.PI / 2 - (before + W[ub] * unit / 2);
    let a = start; const wg = keys.map((k, x) => { const g = { key: k, a0: a, a1: a + W[x] * unit, members: mem(k) }; a += W[x] * unit + gap; return g; });
    L.ways = { geo: wg, ...pack(wg, N) };
    L.MR = Math.min(.045, .36 * Math.min(L.gov.s, L.ways.s));
    L.MR = Math.min(.045, .36 * Math.min(L.gov.s, L.ways.s)); L.scatter = { pos: N.map(n => ({ x: n.pf[0], y: n.pf[1] })) };
    return L;
  }
  const shapeOf = n => (n.m === 'EXCEPTION_PLATFORM_LICENSING' ? 'trid' : SHAPE[n.o]);
  const posOf = (L, tab) => (L[tab] || L.scatter).pos;

  // ---- drawing ----
  function mark(ctx, x, y, r, shape, fill, alpha) {
    const hollow = shape === 'trid'; if (hollow) shape = 'tri';
    ctx.globalAlpha = alpha; ctx.fillStyle = fill; ctx.strokeStyle = fill; ctx.beginPath();
    if (shape === 'ci') ctx.arc(x, y, r, 0, TAU);
    else if (shape === 'sq') { const q = r * .88; ctx.rect(x - q, y - q, 2 * q, 2 * q); }
    else { const q = r * 1.5; ctx.moveTo(x, y - q); ctx.lineTo(x + q * .866, y + q * .5); ctx.lineTo(x - q * .866, y + q * .5); ctx.closePath(); }
    if (hollow) { ctx.lineWidth = Math.max(1.5, r * .3); ctx.setLineDash([r * .7, r * .5]); ctx.stroke(); ctx.setLineDash([]); } else ctx.fill();
  }
  const mixc = (h1, h2, t) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), a = p(h1), b = p(h2); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`; };
  const fnt = (w, px, fam) => `${w} ${px}px ${fam || (typeof window !== 'undefined' && window.NN_FAM) || '"Inter Tight",Arial,sans-serif'}`;

  // labels for a tab: [{a, lines:[bold, small], key}] angles in radians, before rotation
  function labelsFor(D, L, tab, narrow, pad = .13) {
    const M = D.meta, N = D.nodes, c = (k, v) => { let s = M.cp[k]; if (v) for (const x in v) s = s.replace('{' + x + '}', v[x]); return s; };
    const rOf = (members, tabPos) => Math.min(1.1, Math.max(.6, Math.max(.3, ...members.map(i => Math.hypot(tabPos[i].x, tabPos[i].y))) + pad));
    if (tab === 'gov') {
      return L.gov.geo.map(g => { const c = M.cohorts.find(x => x.code === g.key); return { a: (g.a0 + g.a1) / 2, key: g.key, grp: c.g, r: rOf(g.members, L.gov.pos), lines: narrow ? [g.key] : [g.key, c.name] }; });
    }
    return L.ways.geo.map((g, x) => {
      const a = (g.a0 + g.a1) / 2, r = rOf(g.members, L.ways.pos);
      if (x < 6) return { a, r: Math.max(r, .7), key: g.key, lines: narrow ? [String(x + 1)] : [String(x + 1), M.paths[x].short] };
      if (g.key === 'EXCEPTION_PLATFORM_LICENSING') return { a, r: Math.max(r, .7), key: g.key, lines: narrow ? [c('labels.exception_short')] : [c('labels.exception_1'), c('labels.exception_2')] };
      if (g.key === 'INHERITED_SCALE') return { a, r, key: g.key, lines: narrow ? [c('labels.above_narrow'), '(' + g.members.length + ')'] : [c('labels.above_wide', { n: g.members.length })] };
      return { a, r, key: g.key, lines: narrow ? [c('labels.under_1')] : [c('labels.under_1'), c('labels.under_2')] };
    });
  }

  // S: {tab, pos, ce(0..1), chromeA, rot, mutedA(0..1 muting of BELOW), hl, labelA, tint}
  function draw(ctx, G, D, L, T, S) {
    const { w, h, cx, cy, R } = G, N = D.nodes, narrow = G.narrow, rot = S.rot || 0, cr = Math.cos(rot), sr = Math.sin(rot);
    const rp = (x, y) => [cx + R * (x * cr - y * sr), cy + R * (x * sr + y * cr)];
    ctx.save(); ctx.setTransform(G.dpr, 0, 0, G.dpr, 0, 0);
    if (T.bg) { ctx.fillStyle = T.bg; ctx.fillRect(0, 0, w, h); } else ctx.clearRect(0, 0, w, h);
    const lab = S.labelsTab ? labelsFor(D, L, S.labelsTab, narrow, G.labelPad) : [], fs = Math.max(11, Math.round(R / 24 * (G.fsScale || 1)));
    // spokes
    const geo = S.spokes && (S.spokes === 'ways' ? L.ways.geo : L.gov.geo);
    if (geo && S.chromeA > 0) {
      ctx.globalAlpha = S.chromeA; ctx.strokeStyle = T.grid; ctx.lineWidth = Math.max(1, R / 400);
      geo.forEach(g => { const a0 = g.a0, [x0, y0] = rp(Math.cos(a0) * .1, Math.sin(a0) * .1), [x1, y1] = rp(Math.cos(a0) * .98, Math.sin(a0) * .98); ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); });
      if (S.spokes === 'ways') { const dv = geo.find(g => g.key === 'INHERITED_SCALE'); if (dv) { ctx.strokeStyle = T.ink2; ctx.lineWidth = Math.max(1.5, R / 220); ctx.setLineDash([R / 60, R / 90]); const a0 = dv.a0 - .02, [x0, y0] = rp(Math.cos(a0) * .1, Math.sin(a0) * .1), [x1, y1] = rp(Math.cos(a0) * .98, Math.sin(a0) * .98); ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); ctx.setLineDash([]); } }
      ctx.globalAlpha = 1;
    }
    // marks
    const r = L.MR * R * G.boost;
    N.forEach((n, i) => {
      const p = S.pos[i], [x, y] = rp(p.x, p.y), ce = S.ceArr ? S.ceArr[i] : (S.ce == null ? 1 : S.ce);
      const muted = n.m === 'BELOW' || n.o === 'INHERITED' ? S.mutedA || 0 : 0, hlOff = S.hl != null && S.hlKeyOf && S.hlKeyOf(n) !== S.hl ? (S.dim == null ? .75 : S.dim) : 0;
      mark(ctx, x, y, r, ce > .5 ? shapeOf(n) : 'ci', mixc(T.neutral, T[n.g], ce), (1 - .66 * muted) * (1 - hlOff) * (S.appear ? S.appear[i] : 1));
    });
    ctx.globalAlpha = 1;
    // labels
    if (S.labelA > 0) {
      lab.forEach(l => {
        const a = l.a + rot, x = cx + Math.cos(a) * R * l.r, y = cy + Math.sin(a) * R * l.r, c = Math.cos(a), on = S.labelOn ? S.labelOn(l.key) : (S.hl == null || S.hl === l.key);
        if (S.labelOnly && !on) return; ctx.globalAlpha = S.labelA * (on ? 1 : .4); ctx.textBaseline = 'middle';
        const big = Math.round(fs * (narrow ? 1.05 : 1.25)), sub = Math.max(11, Math.round(fs * .85)), two = l.lines[1];
        ctx.font = fnt(700, big); const w1 = ctx.measureText(l.lines[0]).width; ctx.font = fnt(500, sub); const w2 = two ? ctx.measureText(two).width : 0, ww = Math.max(w1, w2);
        let al = c > .3 ? 'left' : c < -.3 ? 'right' : 'center', tx = x;
        if (al === 'left') tx = Math.min(x, w - ww - 3); else if (al === 'right') tx = Math.max(x, ww + 3); else tx = cl(x, ww / 2 + 3, w - ww / 2 - 3);
        ctx.textAlign = al; ctx.fillStyle = l.grp ? T[l.grp] : T.ink; ctx.font = fnt(700, big); ctx.fillText(l.lines[0], tx, y - (two ? fs * .55 : 0));
        if (two) { ctx.font = fnt(500, sub); ctx.fillStyle = T.ink2; ctx.fillText(two, tx, y + fs * .65); }
      });
      ctx.globalAlpha = 1;
    }
    if (S.extra) S.extra(ctx, G, rp);
    ctx.restore();
  }
  function geom(w, dpr, hFactor, pad = 0) {                              // pad: extra band above and below the circle, for annotations
    const narrow = w < 560, h0 = Math.round(w * (hFactor || (narrow ? 1.02 : .8))), R = narrow ? w * .37 : h0 * .4, h = h0 + 2 * pad;
    return { w, h, cx: w / 2, cy: h / 2, R, dpr, narrow, boost: narrow ? 1.12 : 1, pad };
  }
  return { wayKey, shapeOf, build, draw, geom, posOf, labelsFor, cl, ss, eio, mixc, SHAPE, MR, TAU };
})();
