// Story page bootstrap. Everything is server-rendered; this only adds interaction and motion.
import { $, $$, parseHash, setHash } from './lib.js';
import * as fig1 from './figs/fig1.js';
import * as fig2 from './figs/fig2.js';
import * as fig4 from './figs/fig4.js';
import * as fig5 from './figs/fig5.js';
import * as scale from './figs/scale.js';
import * as close from './figs/close.js';
import * as nav from './nav.js';
import * as seq from './seq.js';

const D = JSON.parse($('#nn-data').textContent);
const tok = parseHash();

// progress bar (decorative)
const bar = $('#progressBar');
let q = false;
addEventListener('scroll', () => { if (q) return; q = true; requestAnimationFrame(() => { q = false;
  const h = document.documentElement, max = h.scrollHeight - h.clientHeight; bar.style.width = (max > 0 ? h.scrollTop / max * 100 : 0) + '%'; }); }, { passive: true });

function go(id) { const el = document.getElementById(id); if (el) setTimeout(() => el.scrollIntoView(), 80); }

// figures
const f1 = $('#fig-1-timeline .fig-body'); if (f1) fig1.mount(f1, { data: D.fig1 });
const f2 = $('#fig-2-map .fig-body'); let map = null;
if (f2) map = fig2.mount(f2, { data: D.fig2, state: tok });
const f4 = $('#fig-4-threshold .fig-body'); if (f4) fig4.mount(f4, { data: D.fig4, state: tok });
const s1 = $('.s1'); if (s1) scale.mount(s1);
const cl = $('.close'); if (cl) close.mount(cl);
nav.mount();

// Figure 5: sticky sequence on wide screens; otherwise the stacked states, plus a free toggle on the main figure
const sq = $('.seq'); let f5inst = null;
if (sq) {
  f5inst = seq.mount(sq, { data: D.fig5 });
  if (!f5inst) { const st = $('.seq-stage .fig-body', sq); f5inst = fig5.mount(st, { data: D.fig5, state: /^fig-5-split$/.test(tok) ? 'split' : 'pooled' }); }
}

// deep links: bare tokens only
if (tok) {
  const m = /^(fig-\d)-/.exec(tok);
  if (tok === 'fig-5-split' || tok === 'fig-5-pooled') {
    if (sq && sq.classList.contains('seq-on')) { const step = $$('[data-step]', sq)[tok === 'fig-5-split' ? 0 : 0]; setTimeout(() => step.scrollIntoView({ block: tok === 'fig-5-split' ? 'end' : 'start' }), 80); }
    else go('fig-5-bands');
  } else if (m) go($$('figure.fig').map(f => f.id).find(i => i.startsWith(m[1] + '-')) || tok);
  else go(tok);
}
