// Embed bootstrap: mounts exactly one figure and tells the host page its height.
// Message to the parent: {type:'nn:resize', v:1, fig:'<id>', height:<css px>, nonce:'<echo of ?n=>'}
import { $, parseHash } from './lib.js';
import * as fig1 from './figs/fig1.js';
import * as fig2 from './figs/fig2.js';
import * as fig4 from './figs/fig4.js';
import * as fig5 from './figs/fig5.js';
import * as scale from './figs/scale.js';

const D = JSON.parse($('#nn-data').textContent), id = document.body.dataset.fig, qs = new URLSearchParams(location.search);
const body = $('.fig-body');
const th = qs.get('theme'); if (th === 'light' || th === 'dark') document.documentElement.dataset.theme = th;
const state = qs.get('state') || parseHash();
if (id === 'fig-1-timeline') fig1.mount(body, { data: D.fig1, scrub: false });
if (id === 'fig-2-map') fig2.mount(body, { data: D.fig2, state, embed: true });
if (id === 'fig-4-threshold') fig4.mount(body, { data: D.fig4, state });
if (id === 'fig-5-bands') fig5.mount(body, { data: D.fig5, state: state === 'split' ? 'split' : state === 'pooled' ? 'pooled' : 'pooled' });
if (id === 'fig-0-scale') scale.mount(body, { scrub: false });

let last = 0, raf = 0;
const post = () => { raf = 0; const h = Math.ceil(document.documentElement.getBoundingClientRect().height);
  if (Math.abs(h - last) < 2) return; last = h;
  parent.postMessage({ type: 'nn:resize', v: 1, fig: id, height: h, nonce: qs.get('n') || '' }, '*'); };
const req = () => { if (!raf) raf = requestAnimationFrame(post); };
if (parent !== window) {
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(req).observe(document.documentElement);
  addEventListener('load', req); if (document.fonts && document.fonts.ready) document.fonts.ready.then(req); req();
}
