// Figure 6 (explorer): the same 169 marks re-sorted by lens; distance from the center is revenue band. Motion only means "lens changed".
// Layouts are precomputed in tools/build_nodes169.py. No JS: a still of the governance lens plus the full list view.
import { esc, $, $$, reduced, css, setHash, GROUP_LABEL } from '../lib.js';

export const id = 'fig-6-kaleidoscope';
export const STATES = ['field', 'gov', 'mech', 'origin', 'born'];
export const LENSES = [['field', 'The field'], ['gov', 'Governance'], ['mech', 'Six ways past $10M'], ['origin', 'Born, crossed, never'], ['born', 'Founded']];
const DEFAULT = 'gov', RR = .35, SIZE = [.0095, .014, .0195];
const BANDS = ['Below $3.5M', '$3.5M–$10M', 'Above $10M'];
const STATUS = { CLOSED: 'closed', ACQUIRED: 'acquired', ABSORBED: 'absorbed' };
const lensOf = t => { const m = /^(?:fig-6-)?(field|gov|mech|origin|born)$/.exec(t || ''); return m ? m[1] : DEFAULT; };
const mechLabel = (m, k) => (m.mech.find(x => x.key === k) || {}).label || '';
export function caption(lens, data) {
  const m = data.meta, N = data.nodes, cnt = f => N.filter(f).length, co = c => m.cohorts.find(x => x.code === c);
  const c1 = co('C1'), c8 = co('C8');
  return {
    field: ['The field.', `${m.n} organizations pooled, no sorting. Nothing distinguishes one mark from another yet.`],
    gov: ['Governance.', `Nine wedges, one per cohort. Distance from the center is revenue band, with rings at $3.5M and $10M. ${c1.name}: ${c1.above} of ${c1.n} above $10M. ${c8.name}: ${c8.above} of ${c8.n}.`],
    mech: ['Six ways past $10M.', 'Wedges are the paper’s six mechanisms. Organizations already above $10M at launch sit in their own wedge.'],
    origin: ['Born, crossed, never.', `${cnt(d => d.orig === 'INHERITED')} were born above $10M or inherited the scale, ${cnt(d => d.orig === 'CROSSED')} crossed it, ${cnt(d => d.orig === 'NEVER_CROSSED')} never have.`],
    born: ['Founded.', `Distance from the center is founding year, oldest inside. ${cnt(d => d.fy >= 2008)} of ${m.n} were founded in 2008 or later.`],
  }[lens];
}
const wedgeList = (data, lens) => data.lenses[lens].geo.length
  ? data.lenses[lens].geo.map(g => `<li data-key="${esc(g.key)}" data-n="${g.n}"><b>${esc(g.label)}</b>${g.sub ? ' ' + esc(g.sub) : ''}<span>${g.n}</span></li>`).join('')
  : `<li data-key="all" data-n="${data.meta.n}"><b>All organizations</b><span>${data.meta.n}</span></li>`;

export function html(data, { alt, state = DEFAULT, still = '' }) {
  const [h, t] = caption(state, data);
  const btns = LENSES.map(([k, l]) => `<button type="button" class="kl-btn" data-lens="${k}" aria-pressed="${k === state}">${esc(l)}</button>`).join('');
  return `<div class="kl" data-state="${state}"><div class="kl-lenses" role="group" aria-label="Lens: how the ${data.meta.n} organizations are sorted">${btns}</div>`
    + `<div class="kl-panel"><div class="kl-stage"><canvas class="kl-cv" role="img" aria-label="${esc(alt)}"></canvas>`
    + (still ? `<img class="kl-still" src="${esc(still)}" alt="${esc(alt)}" width="1200" height="1200">` : '') + '<div class="kl-tip" role="status" hidden></div></div>'
    + `<p class="kl-key">${['a', 'b', 'c'].map(k => `<span><i class="${k}"></i>${esc(GROUP_LABEL[k])}</span>`).join('')}<span><i class="x"></i>Closed</span></p></div>`
    + `<p class="kl-cap" aria-live="polite"><b>${esc(h)}</b> ${esc(t)}</p><ul class="kl-wedges" aria-label="Wedges in this lens, with counts">${wedgeList(data, state)}</ul></div>`;
}

export function tableHtml(data) {
  const m = data.meta;
  return `<table><caption class="sr">All ${m.n} organizations: cohort, revenue band, founding year and, for those above $10M, how they got there</caption>`
    + '<thead><tr><th scope="col">Organization</th><th scope="col">Cohort</th><th scope="col">Revenue band</th><th scope="col">Founded</th><th scope="col">Above $10M</th><th scope="col">Note</th></tr></thead><tbody>'
    + data.nodes.map(d => `<tr><th scope="row">${esc(d.name)}</th><td>${d.c} ${esc(m.cohorts[d.ci].name)}</td><td>${BANDS[d.b]}</td>`
      + (d.un ? '<td></td><td></td><td>Figure unverified</td></tr>' : `<td>${d.fy || ''}</td><td>${d.b === 2 ? esc(mechLabel(m, d.mech)) + (d.orig === 'CROSSED' ? ' (crossed)' : '') : ''}</td><td>${[STATUS[d.cl], d.fl !== 'INCLUDE' ? 'proxy or historical figure' : ''].filter(Boolean).join('; ')}</td></tr>`)).join('')
    + '</tbody></table>';
}

export function mount(el, { data, state = DEFAULT, onChange, animate = true } = {}) {
  const root = $('.kl', el), cv = $('.kl-cv', root);
  if (!root || !cv) return;
  const stage = $('.kl-stage', root), tip = $('.kl-tip', root), capEl = $('.kl-cap', root), listEl = $('.kl-wedges', root), btns = $$('.kl-btn', root);
  const N = data.nodes, n = N.length, m = data.meta, ctx = cv.getContext('2d'), baseAlt = cv.getAttribute('aria-label');
  const T = { a: css('--kl-a') || '#F6C84E', b: css('--kl-b') || '#B23A5E', c: css('--kl-c') || '#A8A8A8', neutral: css('--kl-neutral') || '#7C7C7C',
    bg: css('--kl-bg') || '#000', ink: css('--kl-ink') || '#fff', ink2: css('--kl-ink-2') || '#bdbdbd', ink3: css('--kl-ink-3') || '#8a8a8a', grid: css('--kl-grid') || '#262626' };
  let cur = lensOf(state), P = N.map(d => d.p[cur].slice()), CB = N.map(() => (cur === 'field' ? 0 : 1)), prev = cur, g = 1, raf = 0, S = 0, dpr = 1;
  const mix = (h1, h2, t) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), a = p(h1), b = p(h2); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`; };

  function mark(x, y, s, shape, fill, edge, hollow) {
    ctx.beginPath();
    if (shape === 'a') ctx.arc(x, y, s, 0, Math.PI * 2);
    else if (shape === 'b') { const q = s * .9; ctx.rect(x - q, y - q, q * 2, q * 2); }
    else { const q = s * 1.25; ctx.moveTo(x, y - q); ctx.lineTo(x + q, y); ctx.lineTo(x, y + q); ctx.lineTo(x - q, y); ctx.closePath(); }
    if (hollow) { ctx.lineWidth = Math.max(1.5, s * .45); ctx.strokeStyle = fill; ctx.stroke(); return; }
    ctx.fillStyle = fill; ctx.fill();
    if (edge) { ctx.lineWidth = 1; ctx.strokeStyle = '#000'; ctx.stroke(); }
  }
  const font = (w, px) => `${w} ${px}px "Inter Tight", Arial, sans-serif`;
  function chrome(lens, alpha) {
    if (alpha <= 0) return;
    const cx = S / 2, R = S * RR, geo = data.lenses[lens].geo, narrow = S < 560;
    ctx.save(); ctx.globalAlpha = alpha; ctx.lineWidth = 1;
    const ring = (r, d, c) => { ctx.setLineDash(d); ctx.strokeStyle = c; ctx.beginPath(); ctx.arc(cx, cx, r, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]); };
    const pill = (t, r, a, c) => {   // label pill at the angle the layout script found furthest from any mark
      ctx.font = font(600, 12); const w = ctx.measureText(t).width + 12, x = cx + Math.cos(a) * r, y = cx + Math.sin(a) * r;
      ctx.fillStyle = '#000'; ctx.strokeStyle = '#4a4a4a'; ctx.beginPath(); ctx.rect(x - w / 2, y - 10, w, 20); ctx.fill(); ctx.stroke();
      ctx.fillStyle = c; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(t, x, y + .5);
    };
    (data.lenses[lens].rings || []).forEach((q, k) => { const r = q.r * R, yr = lens === 'born'; ring(r, yr ? [3, 5] : [4, 4], yr ? '#333' : k ? '#5a5a5a' : '#3a3a3a'); pill(q.t, r, q.a, yr ? T.ink3 : T.ink); });
    geo.forEach(G => {
      ctx.strokeStyle = T.grid; ctx.beginPath(); ctx.moveTo(cx + Math.cos(G.a0) * R * .1, cx + Math.sin(G.a0) * R * .1); ctx.lineTo(cx + Math.cos(G.a0) * R, cx + Math.sin(G.a0) * R); ctx.stroke();
      const am = (G.a0 + G.a1) / 2, x = cx + Math.cos(am) * R * 1.1, y = cx + Math.sin(am) * R * 1.1, cs = Math.cos(am), room = cs > .25 ? S - x - 4 : cs < -.25 ? x - 4 : S / 2;
      ctx.textAlign = cs > .25 ? 'left' : cs < -.25 ? 'right' : 'center'; ctx.textBaseline = 'middle';
      const big = Math.max(12, S / 44), sub = Math.max(12, S / 60), y0 = y;
      const w = (t, f) => { ctx.font = f; return ctx.measureText(t).width; };
      const parts = G.label.split(' '), rest = parts.slice(1).join(' ');
      let l1 = G.label, l2 = G.sub && !narrow && w(G.sub, font(500, sub)) < room ? G.sub : '';
      if (narrow || w(l1, font(700, big)) > room) {
        l1 = parts[0]; l2 = !narrow && rest && w(rest, font(500, sub)) < room ? rest : '';
      }
      ctx.fillStyle = T.ink; ctx.font = font(700, big); ctx.fillText(l1, x, y0 - (l2 ? 7 : 0));
      if (l2) { ctx.font = font(500, sub); ctx.fillStyle = T.ink2; ctx.fillText(l2, x, y0 + 8); }
    });
    ctx.restore();
  }
  function draw() {
    if (!S) return;
    const R = S * RR, cx = S / 2;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.fillStyle = T.bg; ctx.fillRect(0, 0, S, S);
    if (g < 1 && prev !== cur) { chrome(prev, 1 - g); chrome(cur, g); } else chrome(cur, 1);
    let drawn = 0;
    N.forEach((d, i) => {
      const k = CB[i], fill = mix(T.neutral, T[d.g], k);
      mark(cx + P[i][0] * R, cx + P[i][1] * R, SIZE[d.b] * R * 1.35 * (S < 420 ? 1.3 : 1), k >= .5 ? d.g : 'a', fill, d.g === 'a' && k >= .5, d.cl === 'CLOSED'); drawn++;
    });
    root.dataset.drawn = drawn;
  }
  function size() {
    dpr = Math.min(2, devicePixelRatio || 1); const w = Math.round(stage.getBoundingClientRect().width);
    if (!w || w === S) return; S = w; cv.width = Math.round(S * dpr); cv.height = Math.round(S * dpr); cv.style.height = S + 'px'; draw();
  }
  function settled() {
    const geo = data.lenses[cur].geo, out = {}; geo.forEach(G => { out[G.key] = 0; });
    if (geo.length) P.forEach(p => {
      let a = Math.atan2(p[1], p[0]); const G = geo.find(q => { for (const s of [-2, 0, 2]) { const v = a + s * Math.PI; if (v >= q.a0 - 1e-3 && v <= q.a1 + 1e-3) return true; } return false; });
      if (G) out[G.key]++;
    });
    root.dataset.wedges = JSON.stringify(out); root.dataset.lens = cur;
  }
  const hit = ev => {
    const r = cv.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, R = r.width * RR, c = r.width / 2;
    let best = -1, bd = 1e9; N.forEach((d, i) => { const dd = Math.hypot(c + P[i][0] * R - x, c + P[i][1] * R - y); if (dd < bd) { bd = dd; best = i; } });
    if (bd > (ev.pointerType === 'mouse' ? 14 : 24)) { tip.hidden = true; return; }
    const d = N[best], co = m.cohorts[d.ci];
    tip.innerHTML = `<b>${esc(d.name)}</b><span>${d.c} ${esc(co.name)} · ${BANDS[d.b]}${d.fy ? ' · founded ' + d.fy : ''}</span>`
      + (d.un ? '' : (d.b === 2 ? `<span>${esc(mechLabel(m, d.mech))}</span>` : '') + (STATUS[d.cl] ? `<span>Status: ${STATUS[d.cl]}</span>` : '') + (d.fl !== 'INCLUDE' ? '<span>Proxy or historical figure</span>' : ''));
    tip.hidden = false; const tw = tip.offsetWidth, th = tip.offsetHeight;
    tip.style.left = Math.min(Math.max(8, c + P[best][0] * R - tw / 2), r.width - tw - 8) + 'px';
    tip.style.top = (c + P[best][1] * R + 14 + th > r.height ? c + P[best][1] * R - th - 14 : c + P[best][1] * R + 14) + 'px';
  };
  cv.addEventListener('pointermove', hit); cv.addEventListener('pointerdown', hit); cv.addEventListener('pointerleave', () => { tip.hidden = true; });
  addEventListener('keydown', e => { if (e.key === 'Escape') tip.hidden = true; });

  function ui() {
    btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.lens === cur));
    const [h, t] = caption(cur, data); capEl.innerHTML = `<b>${esc(h)}</b> ${esc(t)}`; listEl.innerHTML = wedgeList(data, cur);
    cv.setAttribute('aria-label', `${baseAlt} ${h} ${t}`); root.dataset.state = cur;
  }
  function go(next, { user = false, anim = animate } = {}) {
    if (!STATES.includes(next) || next === cur) return;
    const from = P.map(p => p.slice()), to = N.map(d => d.p[next]); prev = cur; cur = next; tip.hidden = true; ui();
    if (user) setHash('fig-6-' + next);
    if (onChange) onChange(next, user);
    cancelAnimationFrame(raf);
    const toColor = next !== 'field', fromColor = prev !== 'field';
    if (!anim || reduced()) { P = to.map(p => p.slice()); CB = N.map(() => (toColor ? 1 : 0)); g = 1; prev = cur; draw(); settled(); return; }
    const t0 = performance.now(), DUR = 1050, STAG = 450, ease = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
    const delay = to.map(p => (Math.atan2(p[1], p[0]) + Math.PI) / (2 * Math.PI) * STAG);
    const step = now => {
      let done = true;
      N.forEach((d, i) => {
        const t = Math.min(1, Math.max(0, (now - t0 - delay[i]) / DUR)), e = ease(t); if (t < 1) done = false;
        P[i] = [from[i][0] + (to[i][0] - from[i][0]) * e, from[i][1] + (to[i][1] - from[i][1]) * e];
        CB[i] = fromColor === toColor ? (toColor ? 1 : 0) : (toColor ? e : 1 - e);
      });
      g = Math.min(1, (now - t0) / (DUR + STAG)); draw();
      if (!done) raf = requestAnimationFrame(step); else { g = 1; prev = cur; draw(); settled(); }
    };
    raf = requestAnimationFrame(step);
  }
  btns.forEach(b => b.addEventListener('click', () => go(b.dataset.lens, { user: true })));
  $('.kl-lenses', root).addEventListener('keydown', e => {
    const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!k) return;
    e.preventDefault(); const i = STATES.indexOf(cur), j = Math.min(STATES.length - 1, Math.max(0, i + k)), b = btns.find(x => x.dataset.lens === STATES[j]);
    if (b) { b.focus(); go(STATES[j], { user: true }); }
  });
  if (typeof ResizeObserver === 'function') new ResizeObserver(size).observe(stage);
  size(); ui(); settled();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
  return { setState: k => go(k), get state() { return cur; } };
}
