// Scene S1: two numbers. One square = $8,800. The field is drawn at $100 million, the bottom of "the low hundreds of
// millions" (the copy's words for the TBPN price). The count of squares is deliberately never shown.
// Static render: an SVG pattern field. With a scroll engine: a canvas that scrubs from one big square out to the field.
import { esc, clamp, lerp, $, css, reduced, scene, pinProgress } from '../lib.js';

export const id = 'fig-0-scale';
const N = Math.ceil(100000000 / 8800); // derived, internal only

export const LEGEND = [
  ['sw-one', '$8,800', 'Roger Sollenberger’s GoFundMe, as of this writing. One square.'],
  ['sw-many', 'One square = $8,800.', 'The field is drawn at $100 million, the bottom of “the low hundreds of millions” reported for OpenAI’s TBPN purchase.'],
];
export const NOTE = 'The reported TBPN price was not disclosed precisely; this view uses the lowest figure consistent with the reporting, so the real gap is likely larger.';

export function legendHtml() {
  return '<div class="scale-legend">' + LEGEND.map(([c, b, t]) => `<div><span class="swatch ${c}" aria-hidden="true"></span><span><b>${esc(b)}</b>${esc(t)}</span></div>`).join('') + `</div><p class="fig-note">${esc(NOTE)}</p>`;
}

export function html(_data, { alt }) {
  const s = 7, cols = 142, rows = Math.ceil(N / cols), full = Math.floor(N / cols), rem = N - full * cols, W = cols * s, H = rows * s;
  const svg = `<svg class="s1-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">`
    + `<defs><pattern id="s1sq" width="${s}" height="${s}" patternUnits="userSpaceOnUse"><rect width="${s - 1}" height="${s - 1}" fill="var(--ink)" opacity=".28"/></pattern></defs>`
    + `<rect x="0" y="0" width="${W}" height="${full * s}" fill="url(#s1sq)"/>`
    + (rem ? `<rect x="0" y="${full * s}" width="${rem * s}" height="${s}" fill="url(#s1sq)"/>` : '')
    + `<rect x="-2" y="-2" width="${s + 3}" height="${s + 3}" fill="var(--ink)" stroke="var(--bg)" stroke-width="1"/></svg>`;
  return `<div class="scale-wrap" role="img" aria-label="${esc(alt)}">${svg}<canvas class="s1-canvas" hidden aria-hidden="true"></canvas><span class="scale-pin-label" aria-hidden="true">$8,800</span></div>`;
}

export function mount(el, { scrub = true } = {}) {
  const wrap = $('.scale-wrap', el), cv = $('.s1-canvas', el), label = $('.scale-pin-label', el), box = el.closest('.s1') || el;
  if (!cv || reduced() || !scrub) return;
  const ctx = cv.getContext('2d');
  let W = 0, H = 0, dpr = 1, geom = null;
  function size() {
    const r = wrap.getBoundingClientRect(); W = Math.round(r.width); H = Math.round(r.height); dpr = Math.min(devicePixelRatio || 1, 2);
    cv.width = W * dpr; cv.height = H * dpr; cv.style.width = W + 'px'; cv.style.height = H + 'px';
    const sF = W > 700 ? 7 : W > 480 ? 5 : 4, cols = Math.max(1, Math.floor(W / sF)), rows = Math.ceil(N / cols);
    geom = { sF, cols, rows, s0: Math.min(W, H) * .8 };
  }
  function paint(p) {
    if (!geom) size();
    const { sF, cols, rows, s0 } = geom, e = clamp(p);
    const S = Math.exp(lerp(Math.log(s0), Math.log(sF), e));
    const ox = lerp((W - S) / 2, (W - cols * sF) / 2, e), oy = lerp((H - S) / 2, (H - rows * sF) / 2, e);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
    const ink = css('--ink'), g = Math.max(1, S * (1 - 1 / 7));
    const a = clamp((e - .06) * 4) * .28;
    if (a > 0) {
      ctx.fillStyle = ink; ctx.globalAlpha = a;
      const c0 = Math.max(0, Math.floor(-ox / S) - 1), c1 = Math.min(cols - 1, Math.ceil((W - ox) / S));
      const r0 = Math.max(0, Math.floor(-oy / S) - 1), r1 = Math.min(rows - 1, Math.ceil((H - oy) / S));
      for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) { const i = r * cols + c; if (i === 0 || i >= N) continue; ctx.fillRect(ox + c * S, oy + r * S, g, g); }
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = ink; ctx.fillRect(ox, oy, g, g);
    ctx.strokeStyle = css('--bg'); ctx.lineWidth = 1; ctx.strokeRect(ox - .5, oy - .5, g + 1, g + 1);
    label.style.transform = `translate(${Math.round(ox + g + 10)}px,${Math.round(oy + Math.min(g * .5, 18))}px)`;
  }
  wrap.classList.add('canvas-on'); cv.hidden = false; box.classList.add('s1-on');
  scene(box, (r, vh) => paint(clamp((pinProgress(r, vh) - .05) / .6)));
  addEventListener('resize', () => { geom = null; size(); });
  paint(0);
}
