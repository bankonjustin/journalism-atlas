// Embed bootstrap: mounts exactly one figure (loaded on demand) and tells the host page its height.
// Message to the parent: {type:'nn:resize', v:1, fig:'<id>', height:<css px>, nonce:'<echo of ?n=>'}
import { $, parseHash } from './lib.js';

const D = JSON.parse($('#nn-data').textContent), id = document.body.dataset.fig, qs = new URLSearchParams(location.search);
const body = $('.fig-body');
const th = qs.get('theme'); if (th === 'light' || th === 'dark') document.documentElement.dataset.theme = th;
const state = qs.get('state') || parseHash();
const LOAD = {
  'fig-0-scale': async () => (await import('./figs/scale.js')).mount(body, { scrub: false }),
  'fig-1-timeline': async () => (await import('./figs/fig1.js')).mount(body, { data: D.fig1, scrub: false }),
  'fig-2-map': async () => (await import('./figs/fig2.js')).mount(body, { data: D.fig2, state, embed: true }),
  'fig-4-threshold': async () => (await import('./figs/fig4.js')).mount(body, { data: D.fig4, state }),
  'fig-5-bands': async () => (await import('./figs/fig5.js')).mount(body, { data: D.fig5, state: state === 'split' || /^fig-5-split$/.test(state) ? 'split' : 'pooled' }),
};
if (LOAD[id]) await LOAD[id]();   // fig-3-defector is static: nothing to load

let last = 0, raf = 0;
const post = () => { raf = 0; const h = Math.ceil(document.documentElement.getBoundingClientRect().height);
  if (Math.abs(h - last) < 2) return; last = h;
  parent.postMessage({ type: 'nn:resize', v: 1, fig: id, height: h, nonce: qs.get('n') || '' }, '*'); };
const req = () => { if (!raf) raf = requestAnimationFrame(post); };
if (parent !== window) {
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(req).observe(document.documentElement);
  addEventListener('load', req); if (document.fonts && document.fonts.ready) document.fonts.ready.then(req); req();
}
