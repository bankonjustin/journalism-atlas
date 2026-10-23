// Scene S5: inline trajectories. Rule: two or more values of the same measure, in the locked copy, with a stated
// direction. Every label is the copy's own wording of the value; unreported years stay blank (no interpolation).
// "series" connects only consecutive reported years. "arrow" draws two points joined by a direction arrow, no line
// through the unreported years between them. A range end ("$6M-$8M") is drawn as a band, not a point.
import { esc } from '../lib.js';

export const id = 'sparks';
const W = 300, H = 112, PL = 14, PR = 14, PT = 30, PB = 34;

export function html(s) {
  const pts = s.pts, ymax = Math.max(...pts.map(p => p.y1 ?? p.y)) * 1.12;
  const Y = v => PT + (H - PT - PB) * (1 - v / ymax);
  let X;
  if (s.kind === 'series') { const xs = pts.map(p => p.x), a = Math.min(...xs), b = Math.max(...xs); X = v => PL + 20 + (v - a) / (b - a) * (W - PL - PR - 40); }
  else X = (v, i) => (i === 0 ? PL + 34 : W - PR - 34);
  const px = pts.map((p, i) => ({ ...p, cx: X(p.x, i) }));
  let g = `<line x1="${PL}" x2="${W - PR}" y1="${Y(0)}" y2="${Y(0)}" stroke="var(--rule)"/>`;
  if (s.kind === 'series') {
    px.forEach((p, i) => { const q = px[i + 1]; if (q && q.x - p.x === 1) g += `<line x1="${p.cx}" y1="${Y(p.y)}" x2="${q.cx}" y2="${Y(q.y)}" stroke="var(--ink)" stroke-width="2.5"/>`; });
  } else {
    const a = px[0], b = px[1], y1 = Y(a.y), y2 = Y(b.y1 ? (b.y0 + b.y1) / 2 : b.y);
    g += `<line x1="${a.cx + 8}" y1="${y1}" x2="${b.cx - 10}" y2="${y2}" stroke="var(--ink-3)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#sk-${s.id})"/>`;
  }
  px.forEach((p, i) => {
    const anchor = s.kind === 'series' ? (i === 0 ? 'start' : i === px.length - 1 ? 'end' : 'middle') : (i === 0 ? 'start' : 'end');
    const lx = anchor === 'start' ? p.cx - 6 : anchor === 'end' ? p.cx + 6 : p.cx;
    if (p.y1) {
      g += `<rect x="${p.cx - 7}" y="${Y(p.y1)}" width="14" height="${Y(p.y0) - Y(p.y1)}" fill="var(--ink)" opacity=".85"/>`
        + `<text x="${lx}" y="${Y(p.y1) - 8}" text-anchor="${anchor}" font-size="12" font-weight="800" fill="var(--ink)">${esc(p.label)}</text>`;
    } else {
      g += `<circle cx="${p.cx}" cy="${Y(p.y)}" r="5" fill="var(--ink)"/>`
        + `<text x="${lx}" y="${Y(p.y) - 10}" text-anchor="${anchor}" font-size="12" font-weight="800" fill="var(--ink)">${esc(p.label)}</text>`;
    }
    if (p.xl) g += `<text x="${p.cx}" y="${H - 12}" text-anchor="${i === 0 && s.kind !== 'series' ? 'start' : i === px.length - 1 && s.kind !== 'series' ? 'end' : 'middle'}" font-size="11" font-weight="600" fill="var(--ink-3)" ${s.kind !== 'series' ? `dx="${i === 0 ? -34 + 6 : 34 - 6}"` : ''}>${esc(p.xl)}</text>`;
  });
  const alt = `${s.name}: ` + pts.map(p => p.label + (p.xl ? ` (${p.xl})` : '')).join(', then ');
  return `<figure class="spark"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}"><defs><marker id="sk-${s.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--ink-3)"/></marker></defs>${g}</svg><figcaption>${esc(s.name)}</figcaption></figure>`;
}

export const rowHtml = list => `<div class="spark-row">${list.map(html).join('')}</div>`;
