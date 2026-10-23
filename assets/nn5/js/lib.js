// Shared helpers. No DOM access at import time: the figure modules also run under Node for build-time rendering.

export const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const ease = t => (t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

// Cohort metadata: group a (gold) = C1-3, b (maroon) = C4-6, c (grey) = C7-9. The ONLY use of the group colours.
export const GROUP = { C1: 'a', C2: 'a', C3: 'a', C4: 'b', C5: 'b', C6: 'b', C7: 'c', C8: 'c', C9: 'c' };
export const GROUP_LABEL = {
  a: 'Journalism as most people picture it',
  b: 'How public-minded funding becomes reporting',
  c: 'New ways audiences and markets pay directly',
};
export const SHAPE = { a: 'circle', b: 'square', c: 'diamond' }; // secondary encoding, for colour-blind readers

export const BANDS = ['Below $3.5M', '$3.5M–$10M', 'Above $10M'];

export const fmtM = v => '$' + (Math.round(v * 100) % 10 ? v.toFixed(2) : v.toFixed(1)) + 'M';
export const pct = (a, b) => Math.round((a / b) * 100) + '%';

// ---- browser-only helpers (call from mount functions only) ----
export const $ = (s, r = document) => r.querySelector(s);
export const $$ = (s, r = document) => [...r.querySelectorAll(s)];
export const reduced = () => typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
export const debounce = (f, ms = 150) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => f(...a), ms); }; };
export const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

export function onVisible(el, fn, threshold = .35) {
  if (!el) return;
  if (typeof IntersectionObserver === 'undefined') { fn(); return; }
  const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); fn(); } }, { threshold });
  io.observe(el);
}

// One scroll listener for every scene. A scene registers a callback that gets called (rAF-throttled) while
// its element is within one viewport of the screen. Callbacks read geometry only; they write via CSS vars.
const scenes = new Set();
let queued = false, bound = false;
function tick() {
  queued = false;
  const vh = innerHeight;
  for (const s of scenes) {
    const r = s.el.getBoundingClientRect();
    if (r.bottom < -vh || r.top > vh * 2) { if (s.active) { s.active = false; s.fn(r, vh); } continue; }
    s.active = true; s.fn(r, vh);
  }
}
function request() { if (!queued) { queued = true; requestAnimationFrame(tick); } }
export function scene(el, fn) {
  const s = { el, fn, active: false };
  scenes.add(s);
  if (!bound) { bound = true; addEventListener('scroll', request, { passive: true }); addEventListener('resize', request); }
  request();
  return () => scenes.delete(s);
}
// progress through a tall container whose child is `position: sticky; top: 0`: 0 when it pins, 1 when it releases
export const pinProgress = (r, vh) => clamp(-r.top / Math.max(1, r.height - vh));

// Deep-link tokens: bare tokens only, e.g. #fig-5-split. One writer, so scenes don't fight over the hash.
export function setHash(token) {
  if (!/^[\w.-]+$/.test(token)) return;
  try { history.replaceState(null, '', '#' + token); } catch (e) { /* sandboxed iframe: ignore */ }
}
export function parseHash() {
  const t = (typeof location !== 'undefined' ? location.hash : '').slice(1);
  return /^[\w.-]+$/.test(t) ? t : '';
}
