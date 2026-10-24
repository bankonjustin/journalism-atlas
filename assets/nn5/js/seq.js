// Scene S9: Figure 5 as a sticky sequence, driven by the locked sentences already in Section III.
// Wide screens only. Below 1100px, or with reduced motion, the same four states play as stacked figures in the
// prose (rendered at build time), not pinned. After the last step the free toggle returns.
import { $, $$, clamp, reduced, scene } from './lib.js?v=a7031425';
import * as f5 from './figs/fig5.js?v=a7031425';

export function mount(root, { data }) {
  const mq = matchMedia('(min-width: 1100px)');
  if (!mq.matches || reduced()) return null;
  const stage = $('.seq-stage', root), steps = $$('[data-step]', root);
  if (!stage || steps.length < 3) return null;
  root.classList.add('seq-on');
  $$('.seq-state', root).forEach(e => e.remove());   // the stacked copies are for phones and no-JS; drop 500+ nodes on desktop
  let userLock = false;
  const inst = f5.mount(stage, { data, state: 'pooled', onChange: (s, user) => { if (user) userLock = true; } });
  const frac = (el, line) => { const r = el.getBoundingClientRect(); return clamp((line - r.top) / Math.max(1, r.height)); };
  scene(root, (r, vh) => {
    const line = vh * .55, f = steps.map(s => frac(s, line));
    let want = 'pooled';
    if (f[0] >= .5) want = 'split';
    if (f[1] > 0) want = 'hi-ends';
    if (f[2] > 0) want = 'hi-phil';
    const done = f[2] >= .9;
    root.classList.toggle('seq-done', done);
    if (f[0] <= 0) userLock = false;          // scrolled back above the sequence: give control back to the page
    if (!userLock) inst.setState(want);
  });
  return inst;
}
