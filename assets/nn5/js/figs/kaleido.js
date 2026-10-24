// Figure 6 (explorer): the same 169 marks re-sorted by lens; distance from the center is revenue band (shaded zones), or founding year.
// The layouts are the reference engine's, precomputed in tools/build_nodes169.py. The opening (the turn) lives in kaleido-intro.js and loads on demand.
import { esc, $, $$, reduced, css, setHash, GROUP_LABEL } from '../lib.js';

export const id = 'fig-6-kaleidoscope';
export const STATES = ['field', 'gov', 'mech', 'origin', 'born'];
export const LENSES = [['field', 'The field'], ['gov', 'Governance'], ['mech', 'Six ways past $10M'], ['origin', 'How they got past $10M'], ['born', 'When they started']];
const DEFAULT = 'gov', SIZE = [.0095, .014, .0195], TH = [.465, .66], ZONE = [[.1, TH[0]], [TH[0], TH[1]], [TH[1], .97]], TINT = [.02, .04, .065];
const STATUS = { CLOSED: 'closed', ACQUIRED: 'acquired', ABSORBED: 'absorbed' };
const lensOf = t => { const m = /^(?:fig-6-)?(field|gov|mech|origin|born)$/.exec(t || ''); return m ? m[1] : ''; };
const mechLabel = (m, k) => (m.mech.find(x => x.key === k) || {}).label || '';
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), ss = (a, b, t) => { const x = cl((t - a) / (b - a)); return x * x * (3 - 2 * x); };
const eio = x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

// Captions come from the data, except the mechanism caption, which stays the interim wording until the $10M sentence is approved.
export function caption(lens, data) {
  const m = data.meta, N = data.nodes, cnt = f => N.filter(f).length, co = c => m.cohorts.find(x => x.code === c), c1 = co('C1'), c8 = co('C8');
  return {
    field: ['The field.', `All ${m.n}, unsorted. From here it looks like the trends you already know.`],
    gov: ['Governance.', `Nine wedges, one per cohort: who owns it, who decides, how it is funded. ${c1.name}: ${c1.above} of ${c1.n} over $10M. ${c8.name}: ${c8.above} of ${c8.n}.`],
    mech: ['Six ways past $10M.', 'Wedges are the paper’s six mechanisms. Organizations already above $10M at launch sit in their own wedge.'],
    origin: ['How they got past $10M.', `${cnt(d => d.orig === 'INHERITED')} started above it, ${cnt(d => d.orig === 'CROSSED')} grew past it, ${cnt(d => d.orig === 'NEVER_CROSSED')} are still under. Colour shows which governance groups do the growing.`],
    born: ['When they started.', `Distance from the center now means founding year, oldest inside. ${cnt(d => d.fy >= 2008)} of ${m.n} started in 2008 or later.`],
  }[lens];
}
const wedgeList = (data, lens) => data.lenses[lens].geo.length
  ? data.lenses[lens].geo.map(g => `<li data-key="${esc(g.key)}" data-n="${g.n}"><b>${esc(g.label)}</b>${g.sub ? ' ' + esc(g.sub) : ''}<span>${g.n}</span></li>`).join('')
  : `<li data-key="all" data-n="${data.meta.n}"><b>All organizations</b><span>${data.meta.n}</span></li>`;

export function html(data, { alt, state = DEFAULT, still = '', page = false }) {
  const [h, t] = caption(state, data);
  return `<div class="kl${page ? ' kl--page' : ''}" data-state="${state}"><div class="kl-lenses" role="group" aria-label="Lens: how the ${data.meta.n} organizations are sorted">`
    + LENSES.map(([k, l]) => `<button type="button" class="kl-btn" data-lens="${k}" aria-pressed="${k === state}">${esc(l)}</button>`).join('') + '</div>'
    + '<div class="kl-hint" aria-hidden="true"><span class="arr"></span>Try another lens</div>'
    + `<div class="kl-panel"><div class="kl-stage"><canvas class="kl-cv" role="img" aria-label="${esc(alt)}"></canvas>`
    + (still ? `<img class="kl-still" src="${esc(still)}" alt="${esc(alt)}" width="1200" height="1344">` : '')
    + '<div class="kl-over" aria-hidden="true"></div><button type="button" class="kl-btn kl-ghost kl-skip" hidden>Skip</button><div class="kl-tip" role="status" hidden></div></div></div>'
    + `<p class="kl-cap" aria-live="polite"><b>${esc(h)}</b> ${esc(t)}</p><button type="button" class="kl-btn kl-ghost kl-replay" hidden>Replay the turn</button>`
    + `<div class="kl-legend">${['a', 'b', 'c'].map(k => `<span><i class="${k}"></i>${esc(GROUP_LABEL[k])}</span>`).join('')}<span><i class="x"></i>Closed</span>`
    + '<span class="zones">Closer to the center, smaller budget: under $3.5M, $3.5M–$10M, over $10M. Bigger marks are in bigger bands.</span></div>'
    + `<ul class="kl-wedges" aria-label="Wedges in this lens, with counts">${wedgeList(data, state)}</ul></div>`;
}

export function tableHtml(data) {
  const m = data.meta;
  return `<table><caption class="sr">All ${m.n} organizations: cohort, revenue band, year started and, for those over $10M, how they got there</caption>`
    + '<thead><tr><th scope="col">Organization</th><th scope="col">Cohort</th><th scope="col">Revenue band</th><th scope="col">Started</th><th scope="col">Over $10M</th><th scope="col">Note</th></tr></thead><tbody>'
    + data.nodes.map(d => `<tr><th scope="row">${esc(d.name)}</th><td>${d.c} ${esc(m.cohorts[d.ci].name)}</td><td>${m.bands[d.b]}</td>`
      + (d.un ? '<td></td><td></td><td>Figure unverified</td></tr>' : `<td>${d.fy || ''}</td><td>${d.b === 2 ? esc(mechLabel(m, d.mech).replace(/^\d /, '')) + (d.orig === 'CROSSED' ? ' (grew past it)' : '') : ''}</td><td>${[STATUS[d.cl], d.fl !== 'INCLUDE' ? 'proxy or historical figure' : ''].filter(Boolean).join('; ')}</td></tr>`)).join('')
    + '</tbody></table>';
}

export function mount(el, { data, state = '', onChange, animate = true, intro = false } = {}) {
  const root = $('.kl', el), cv = $('.kl-cv', root);
  if (!root || !cv) return;
  const stage = $('.kl-stage', root), tip = $('.kl-tip', root), capEl = $('.kl-cap', root), listEl = $('.kl-wedges', root), btns = $$('.kl-btn[data-lens]', root);
  const over = $('.kl-over', root), skipB = $('.kl-skip', root), hint = $('.kl-hint', root), replay = $('.kl-replay', root);
  const N = data.nodes, m = data.meta, ctx = cv.getContext('2d'), baseAlt = cv.getAttribute('aria-label'), BANDS = m.bands, YEARS = m.years;
  const T = { a: css('--kl-a') || '#F6C84E', b: css('--kl-b') || '#B23A5E', c: css('--kl-c') || '#A8A8A8', neutral: css('--kl-neutral') || '#7C7C7C', bg: css('--kl-bg') || '#000',
    ink: css('--kl-ink') || '#fff', ink2: css('--kl-ink-2') || '#bdbdbd', ink3: css('--kl-ink-3') || '#8a8a8a', grid: css('--kl-grid') || '#262626' };
  const LENS = {}; STATES.forEach(k => { const L = data.lenses[k]; LENS[k] = { pos: N.map(d => ({ x: d.p[k][0], y: d.p[k][1] })), geo: L.geo, zl: L.zl, yl: L.yl }; });
  const sz = d => SIZE[d.b], yearR = y => .13 + .8 * Math.pow((y - 1840) / 186, 2.2);
  const mix = (h1, h2, t) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), a = p(h1), b = p(h2); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`; };
  const given = lensOf(state);
  let cur = given || DEFAULT, P = LENS[cur].pos.map(p => ({ ...p })), mode = 'idle', raf = 0, hovered = null, G = null, dpr = 1, pills = [], intros = 0, onAct = null;

  function shape(x, y, s, g, fill, edge, hollow) {
    ctx.beginPath();
    if (g === 'a') ctx.arc(x, y, s, 0, Math.PI * 2);
    else if (g === 'b') { const q = s * .9; ctx.rect(x - q, y - q, 2 * q, 2 * q); }
    else { const q = s * 1.25; ctx.moveTo(x, y - q); ctx.lineTo(x + q, y); ctx.lineTo(x, y + q); ctx.lineTo(x - q, y); ctx.closePath(); }
    if (hollow) { ctx.lineWidth = Math.max(1.5, s * .35); ctx.strokeStyle = fill; ctx.stroke(); return; }
    ctx.fillStyle = fill; ctx.fill(); if (edge) { ctx.lineWidth = 1.2; ctx.strokeStyle = '#000'; ctx.stroke(); }
  }
  const font = (w, px) => `${w} ${px}px "Inter Tight", Arial, sans-serif`;
  function pill(txt, x, y, fs, fg, alpha) {
    ctx.font = font(600, fs); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const w = ctx.measureText(txt).width + fs * .6, h = fs * 1.6; ctx.fillStyle = 'rgba(0,0,0,.78)'; ctx.fillRect(x - w / 2, y - h / 2, w, h); ctx.fillStyle = fg; ctx.fillText(txt, x, y);
    if (alpha > .5) pills.push([x - w / 2, y - h / 2, w, h]);
  }
  function geom() {
    dpr = Math.min(2, devicePixelRatio || 1); const w = Math.round(stage.getBoundingClientRect().width) || 358, h = Math.round(w * 1.12);
    if (!G || G.w !== w || cv.width !== Math.round(w * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); cv.style.height = h + 'px'; }
    G = { w, h, cx: w / 2, cy: w * .6, R: w * .355, narrow: w < 560 };
  }
  // st: { pos, ce, appear, pop, lens, chromeA, zonesA, yearsA, zoneLabelA, ringT, mirror, fold, hl }
  function scene(st) {
    const { w, h, cx, cy, R } = G, fs = Math.max(12, Math.round(R / 24)), L = LENS[st.lens], pf = s => Math.max(12, Math.round(R / 24 * s)), BN = G.narrow ? ['<$3.5M', BANDS[1], '>$10M'] : BANDS; pills = [];   // narrow canvases use the compact band names, as wedge labels drop to codes

    ctx.save(); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.fillStyle = T.bg; ctx.fillRect(0, 0, w, h);
    if (st.zonesA > 0) {                                                      // revenue bands as places: shaded zones, brighter outward
      for (let z = 2; z >= 0; z--) { ctx.beginPath(); ctx.arc(cx, cy, ZONE[z][1] * R, 0, Math.PI * 2); ctx.arc(cx, cy, ZONE[z][0] * R, 0, Math.PI * 2, true); ctx.fillStyle = `rgba(255,255,255,${TINT[z] * st.zonesA})`; ctx.fill('evenodd'); }
      ctx.globalAlpha = st.zonesA; ctx.setLineDash([R / 60, R / 60]); ctx.lineWidth = Math.max(1, R / 300);
      TH.forEach((r, k) => { ctx.strokeStyle = k ? '#6a6a6a' : '#4a4a4a'; ctx.beginPath(); ctx.arc(cx, cy, r * R, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (st.ringT == null ? 1 : st.ringT)); ctx.stroke(); });
      ctx.setLineDash([]); ctx.globalAlpha = 1;
    }
    if (st.yearsA > 0) { ctx.globalAlpha = st.yearsA; ctx.setLineDash([R / 90, R / 60]); ctx.strokeStyle = '#3a3a3a'; ctx.lineWidth = Math.max(1, R / 320); YEARS.forEach(y => { ctx.beginPath(); ctx.arc(cx, cy, yearR(y) * R, 0, Math.PI * 2); ctx.stroke(); }); ctx.setLineDash([]); ctx.globalAlpha = 1; }
    if (st.chromeA > 0 && L.geo.length) {                                    // spokes and wedge labels
      ctx.globalAlpha = st.chromeA; ctx.strokeStyle = T.grid; ctx.lineWidth = Math.max(1, R / 400);
      L.geo.forEach(g => { ctx.beginPath(); ctx.moveTo(cx + Math.cos(g.a0) * R * .1, cy + Math.sin(g.a0) * R * .1); ctx.lineTo(cx + Math.cos(g.a0) * R * .98, cy + Math.sin(g.a0) * R * .98); ctx.stroke(); });
      L.geo.forEach((g, k) => {
        const am = (g.a0 + g.a1) / 2, x = cx + Math.cos(am) * R * 1.12, y = cy + Math.sin(am) * R * 1.12, cs = Math.cos(am), on = st.hl == null || st.hl === k, room = cs > .3 ? w - x - 4 : cs < -.3 ? x - 4 : w / 2;
        ctx.textAlign = cs > .3 ? 'left' : cs < -.3 ? 'right' : 'center'; ctx.textBaseline = 'middle';
        const big = Math.round(fs * 1.25), sub = Math.max(12, Math.round(fs * .85)), wd = (t, f) => { ctx.font = f; return ctx.measureText(t).width; }, parts = g.label.split(' '), rest = parts.slice(1).join(' ');
        let l1 = g.label, l2 = g.sub && !G.narrow && wd(g.sub, font(500, sub)) < room ? g.sub : '';
        if (G.narrow || wd(l1, font(700, big)) > room) { l1 = parts[0]; l2 = !G.narrow && rest && wd(rest, font(500, sub)) < room ? rest : ''; }
        ctx.fillStyle = on ? T.ink : T.ink3; ctx.font = font(700, big); ctx.fillText(l1, x, y - (l2 ? fs * .55 : 0));
        if (l2) { ctx.font = font(500, sub); ctx.fillStyle = on ? T.ink2 : T.ink3; ctx.fillText(l2, x, y + fs * .65); }
      });
      ctx.textBaseline = 'alphabetic'; ctx.globalAlpha = 1;
    }
    if (st.fold && st.mirror > .001) st.fold(ctx, G);                         // the kaleido fold (opening only)
    const base = 1 - (st.mirror || 0), boost = w < 420 ? 1.3 : 1;
    N.forEach((d, i) => {
      const p = st.pos[i], ap = st.appear ? st.appear[i] : 1; if (ap <= 0 || base <= .001) return;
      const ce = st.ce ? st.ce[i] : 1, pop = st.pop ? 1 + .45 * Math.sin(Math.PI * ce) : 1, s = sz(d) * R * 1.4 * boost * (.4 + .6 * ap) * (1 + .5 * (1 - ap)) * pop;
      ctx.globalAlpha = base * ap * (st.hl != null && L.geo.length && d.ci !== st.hl ? .16 : 1);
      shape(cx + p.x * R, cy + p.y * R, s, ce > .5 ? d.g : 'a', mix(T.neutral, T[d.g], ce), d.g === 'a' && ce > .5, d.cl === 'CLOSED' && ce > .99);
    });
    ctx.globalAlpha = 1;
    if (st.zonesA > 0 && L.zl.length) { ctx.globalAlpha = st.zonesA * (st.zoneLabelA == null ? 1 : st.zoneLabelA); L.zl.forEach((q, k) => pill(BN[k], cx + Math.cos(q.a) * q.r * R, cy + Math.sin(q.a) * q.r * R, pf(1.15), k === 2 ? T.ink : T.ink2, ctx.globalAlpha)); ctx.globalAlpha = 1; }
    if (st.yearsA > 0 && L.yl.length) { ctx.globalAlpha = st.yearsA; L.yl.forEach((q, k) => pill(String(YEARS[k]), cx + Math.cos(q.a) * q.r * R, cy + Math.sin(q.a) * q.r * R, pf(.85), T.ink2, ctx.globalAlpha)); ctx.globalAlpha = 1; }
    ctx.restore(); root.dataset.drawn = N.length;
  }
  function draw(st) {
    geom(); scene(st);
    if (hovered != null && mode !== 'intro') { const p = st.pos[hovered]; ctx.save(); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.beginPath(); ctx.arc(G.cx + p.x * G.R, G.cy + p.y * G.R, sz(N[hovered]) * G.R * 2.4 + 2, 0, 7); ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke(); ctx.restore(); }
  }
  const idleSt = () => { const L = LENS[cur]; return { pos: P, lens: cur, chromeA: 1, zonesA: L.zl.length ? 1 : 0, yearsA: L.yl.length ? 1 : 0, ce: N.map(() => (cur === 'field' ? 0 : 1)) }; };
  const blend = (from, to, t, stagger, dur) => N.map((d, i) => { const g = to[i], f = from[i], del = ((Math.atan2(g.y, g.x) + Math.PI / 2 + 4 * Math.PI) % (2 * Math.PI)) / (2 * Math.PI) * stagger, e = eio(cl((t - del) / dur)); return { x: f.x + (g.x - f.x) * e, y: f.y + (g.y - f.y) * e, e }; });

  // Where each mark actually sits (wedge counts) and whether any label pill covers a mark: read by qa.py.
  function settled() {
    const geo = LENS[cur].geo, out = {}; geo.forEach(q => { out[q.key] = 0; });
    P.forEach(p => { const a = Math.atan2(p.y, p.x), q = geo.find(g => [-2, 0, 2].some(s => { const v = a + s * Math.PI; return v >= g.a0 - 1e-3 && v <= g.a1 + 1e-3; })); if (q) out[q.key]++; });
    root.dataset.wedges = JSON.stringify(out); root.dataset.lens = cur; root.dataset.mode = mode;
    root.dataset.covered = P.filter(p => pills.some(r => { const x = G.cx + p.x * G.R, y = G.cy + p.y * G.R; return x > r[0] && x < r[0] + r[2] && y > r[1] && y < r[1] + r[3]; })).length;
    root.dataset.pills = pills.length;
  }
  function ui() {
    btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.lens === cur));
    const [h, t] = caption(cur, data); capEl.innerHTML = `<b>${esc(h)}</b> ${esc(t)}`; listEl.innerHTML = wedgeList(data, cur);
    cv.setAttribute('aria-label', `${baseAlt} ${h} ${t}`); root.dataset.state = cur;
  }
  function fitCap() {                                                          // reserve the tallest caption, so changing lens never moves what is below it
    const keep = capEl.innerHTML; capEl.style.minHeight = ''; let mx = 0;
    STATES.forEach(k => { const [h, t] = caption(k, data); capEl.innerHTML = `<b>${esc(h)}</b> ${esc(t)}`; mx = Math.max(mx, capEl.offsetHeight); });
    capEl.innerHTML = keep; capEl.style.minHeight = Math.max(mx, parseFloat(getComputedStyle(capEl).minHeight) || 0) + 'px';
  }
  function go(name, user) {
    if (!LENS[name] || (name === cur && mode !== 'intro')) return;
    if (onAct) onAct(); if (mode === 'intro') ctl.end(false);
    const from = cur, fromPos = P.map(p => ({ ...p })), Lf = LENS[from], Lt = LENS[name]; cur = name; tip.hidden = true; ui();
    if (user) setHash('fig-6-' + name);
    if (onChange) onChange(name, !!user);
    cancelAnimationFrame(raf);
    if (reduced() || !animate) { P = Lt.pos.map(p => ({ ...p })); mode = 'idle'; draw(idleSt()); settled(); return; }
    const t0 = performance.now(), cF = from === 'field' ? 0 : 1, cT = name === 'field' ? 0 : 1; mode = 'trans';
    const step = now => {
      const dt = now - t0, bp = blend(fromPos, Lt.pos, dt, 400, 1500), mm = ss(0, 900, dt), swap = dt < 600; P = bp;
      draw({ pos: bp, lens: swap ? from : name, chromeA: swap ? 1 - ss(0, 500, dt) : ss(600, 1200, dt), zonesA: (Lf.zl.length ? 1 : 0) + ((Lt.zl.length ? 1 : 0) - (Lf.zl.length ? 1 : 0)) * mm,
        yearsA: (Lf.yl.length ? 1 : 0) + ((Lt.yl.length ? 1 : 0) - (Lf.yl.length ? 1 : 0)) * mm, zoneLabelA: ss(1400, 1900, dt), ce: bp.map(q => cF + (cT - cF) * ss(.75, 1, q.e)) });
      if (dt < 1950) raf = requestAnimationFrame(step); else { P = Lt.pos.map(q => ({ ...q })); mode = 'idle'; draw(idleSt()); settled(); }
    };
    raf = requestAnimationFrame(step);
  }
  btns.forEach(b => b.addEventListener('click', () => go(b.dataset.lens, true)));
  $('.kl-lenses', root).addEventListener('keydown', e => {                       // arrow keys step through the lenses
    const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!k) return;
    e.preventDefault(); const j = cl(STATES.indexOf(cur) + k, 0, STATES.length - 1), b = btns.find(x => x.dataset.lens === STATES[j]); if (b) { b.focus(); go(STATES[j], true); }
  });
  const hit = ev => {
    if (mode === 'intro') return;
    const r = cv.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, k = r.width / G.w; let best = -1, bd = 1e9;
    N.forEach((d, i) => { const dd = Math.hypot((G.cx + P[i].x * G.R) * k - x, (G.cy + P[i].y * G.R) * k - y); if (dd < bd) { bd = dd; best = i; } });
    if (bd > (ev.pointerType === 'mouse' ? 14 : 24)) { tip.hidden = true; if (hovered != null) { hovered = null; if (mode === 'idle') draw(idleSt()); } return; }
    hovered = best; if (mode === 'idle') draw(idleSt());
    const d = N[best], co = m.cohorts[d.ci], px = (G.cx + P[best].x * G.R) * k, py = (G.cy + P[best].y * G.R) * k;
    tip.innerHTML = `<b>${esc(d.name)}</b><span>${d.c} ${esc(co.name)} · ${BANDS[d.b]}${d.fy ? ' · started ' + d.fy : ''}</span>`
      + (d.un ? '' : (d.b === 2 ? `<span>${esc(mechLabel(m, d.mech).replace(/^\d /, ''))}</span>` : '') + (STATUS[d.cl] ? `<span>Status: ${STATUS[d.cl]}</span>` : '') + (d.fl !== 'INCLUDE' ? '<span>Proxy or historical figure</span>' : ''));
    tip.hidden = false; const tw = tip.offsetWidth, th = tip.offsetHeight;
    tip.style.left = Math.min(Math.max(8, px - tw / 2), r.width - tw - 8) + 'px'; tip.style.top = (py - th - 14 < 0 ? py + 14 : py - th - 14) + 'px';
  };
  cv.addEventListener('pointermove', hit); cv.addEventListener('pointerdown', e => { if (onAct) onAct(); hit(e); });
  cv.addEventListener('pointerleave', () => { tip.hidden = true; hovered = null; if (mode === 'idle') draw(idleSt()); });
  addEventListener('keydown', e => { if (e.key === 'Escape') tip.hidden = true; });

  // Hand-off surface for the opening (kaleido-intro.js, loaded on demand). It plays only when the reader arrives without a lens link.
  const ctl = {
    N, LENS, T, mix, sz, shape, yearR, cohorts: m.cohorts, over, skipB, hint, btns, blend, ss, eio, cl, draw,
    get G() { geom(); return G; }, set onAct(f) { onAct = f; }, get mode() { return mode; },
    begin() { cancelAnimationFrame(raf); cur = 'gov'; mode = 'intro'; intros++; root.dataset.intros = intros; ui(); capEl.innerHTML = '<b>Watch the turn.</b> The same marks, sorted by governance.'; skipB.hidden = false; tip.hidden = true; root.dataset.mode = 'intro'; },
    end(cue) { cancelAnimationFrame(raf); mode = 'idle'; skipB.hidden = true; over.innerHTML = ''; over.dataset.h = ''; P = LENS[cur].pos.map(p => ({ ...p })); ui(); draw(idleSt()); settled(); if (cue && ctl.cue) ctl.cue(); },
    raf: f => { raf = requestAnimationFrame(f); },
  };
  const play = () => import('./kaleido-intro.js').then(M => M.play(ctl));
  skipB.addEventListener('click', () => ctl.end(true));
  if (intro) replay.hidden = false;
  replay.addEventListener('click', () => { if (reduced()) { cur = 'gov'; P = LENS.gov.pos.map(p => ({ ...p })); ui(); draw(idleSt()); settled(); } else play(); });
  function start() {
    geom(); ui(); fitCap(); draw(idleSt()); settled();                        // first paint is always the finished Governance (or the linked lens)
    if (!intro) return;
    if (reduced()) { hint.classList.add('on'); return; }                       // reduced motion: no opening, hint only
    if (given) return;                                                          // a lens link skips the opening
    const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { io.disconnect(); play(); } }, { threshold: .4 }); io.observe(cv);
  }
  if (typeof ResizeObserver === 'function') new ResizeObserver(() => { if (mode === 'idle') { draw(idleSt()); settled(); } }).observe(stage);
  start();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (mode === 'idle') { draw(idleSt()); settled(); } });
  return { setState: k => go(k), get state() { return cur; } };
}
