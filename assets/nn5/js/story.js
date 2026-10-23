// Story page bootstrap. Everything is server-rendered; this only adds interaction and motion.
import { $, $$, parseHash, setHash, scene } from './lib.js';
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
const f4 = $('#fig-4-threshold .fig-body'); let f4h = null;
if (f4) f4h = fig4.mount(f4, { data: D.fig4, state: tok });
const s1 = $('.s1'); if (s1) scale.mount(s1);
const cl = $('.close'); if (cl) close.mount(cl);
nav.mount();

// Figure 5: sticky sequence on wide screens; otherwise the stacked states, plus a free toggle on the main figure
const sq = $('.seq'); let f5inst = null;
if (sq) {
  f5inst = seq.mount(sq, { data: D.fig5 });
  if (!f5inst) { const st = $('.seq-stage .fig-body', sq); f5inst = fig5.mount(st, { data: D.fig5, state: /^fig-5-split$/.test(tok) ? 'split' : 'pooled' }); }
}

// print: open every data table so it prints, then put them back
let reopened = [];
addEventListener('beforeprint', () => { reopened = $$('details.fig-table:not([open])'); reopened.forEach(d => { d.open = true; }); });
addEventListener('afterprint', () => { reopened.forEach(d => { d.open = false; }); });

// deep links: bare tokens only. Applied on load, again once fonts/layout settle, and on hashchange.
let touched = false;
['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(ev => addEventListener(ev, () => { touched = true; }, { once: true, passive: true }));
const topOf = el => el.getBoundingClientRect().top + scrollY;
function scrollToToken(t) {
  if (/^fig-5-(split|pooled)$/.test(t) && sq && sq.classList.contains('seq-on')) {
    const st = $$('[data-step]', sq)[0], r = st.getBoundingClientRect(), line = innerHeight * .55;
    scrollTo(0, topOf(st) + (t === 'fig-5-split' ? .65 : .1) * r.height - line); return;
  }
  const m = /^(fig-\d)-/.exec(t);
  const el = document.getElementById(t) || (m && $$('figure.fig').map(f => f.id).map(i => document.getElementById(i)).find(f => f.id.startsWith(m[1] + '-')));
  if (el) el.scrollIntoView();
}
function applyToken(t, scroll) {
  if (!t) return;
  if (/^fig-2-c[1-9]$/.test(t) && map) map.pick(t.slice(6).toUpperCase(), false);
  if (/^fig-4-(\d\d|threshold)$/.test(t) && f4h) f4h.apply(t);
  if (/^fig-5-(split|pooled)$/.test(t) && f5inst && !(sq && sq.classList.contains('seq-on'))) f5inst.setState(t === 'fig-5-split' ? 'split' : 'pooled', { anim: false });
  if (scroll) scrollToToken(t);
}
if (tok) {
  applyToken(tok, false);
  setTimeout(() => scrollToToken(tok), 80);
  const again = () => { if (!touched && parseHash() === tok) scrollToToken(tok); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => requestAnimationFrame(again));
  // layout can move after load (pinned scenes change page height): keep following it until fonts are ready and the layout
  // has been quiet for 700 ms, or the reader takes over, or 8 s pass (backstop)
  if (typeof ResizeObserver !== 'undefined') {
    let h = document.documentElement.scrollHeight, fontsReady = !(document.fonts && document.fonts.ready), quiet = null, done = false;
    const stop = () => { if (done) return; done = true; ro.disconnect(); clearTimeout(quiet); clearTimeout(cap); };
    const arm = () => { clearTimeout(quiet); quiet = setTimeout(() => { if (fontsReady) stop(); else arm(); }, 700); };
    const ro = new ResizeObserver(() => { if (touched) return stop(); const nh = document.documentElement.scrollHeight; if (nh !== h) { h = nh; again(); arm(); } });
    ro.observe(document.documentElement);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { fontsReady = true; arm(); });
    const cap = setTimeout(stop, 8000); arm();
  }
}
addEventListener('hashchange', () => { const t = parseHash(); applyToken(t, true); });
// a hash that records the last interaction goes stale once the reader has moved on: clear it (replaceState, so Back is
// untouched) when the figure it names is far off screen
const FIG_OF = { 'fig-1': 'fig-1-timeline', 'fig-2': 'fig-2-map', 'fig-4': 'fig-4-threshold', 'fig-5': 'fig-5-bands' };
let hq = false;
addEventListener('scroll', () => { if (hq) return; hq = true; requestAnimationFrame(() => { hq = false;
  const t = parseHash(), el = t && document.getElementById(FIG_OF[t.slice(0, 5)] || '');
  if (!el) return;
  const r = el.getBoundingClientRect();
  if (r.bottom < -innerHeight * .5 || r.top > innerHeight * 1.5) { try { history.replaceState(null, '', location.pathname + location.search); } catch (e) { /* ignore */ } } }); }, { passive: true });
