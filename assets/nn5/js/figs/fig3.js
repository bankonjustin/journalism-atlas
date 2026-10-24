// Figure 3: Defector revenue, Years 1-5. Static stacked bars (subscription, then all other). No animation.
// Two SVG variants (wide / narrow) switched by CSS, so there is no JS and no layout shift.
import { esc, fmtM } from '../lib.js?v=a7031425';

export const id = 'fig-3-defector';

function svg(rows, narrow, alt) {
  const W = narrow ? 340 : 760, H = narrow ? 320 : 340, pl = narrow ? 42 : 56, pr = 8, top = 30, bh = H - top - 56;
  const cw = (W - pl - pr) / rows.length, bw = Math.min(96, cw * .6), Y = v => top + bh - (v / 5) * bh;
  const yr = r => r.period.replace(/^Sep (\d{4})-Aug (\d{4})$/, (_, a, b) => `${a}–${b.slice(2)}`);
  let s = `<svg class="f3-svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(alt)}">`;
  [0, 1, 2, 3, 4, 5].forEach(v => {
    s += `<line x1="${pl}" x2="${W - pr}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--rule)"/>`
      + `<text x="${pl - 8}" y="${Y(v) + 4}" text-anchor="end" font-size="12" fill="var(--ink-3)">$${v}M</text>`;
  });
  rows.forEach((r, i) => {
    const cx = pl + cw * i + cw / 2, x = cx - bw / 2;
    s += `<rect x="${x}" y="${Y(r.sub)}" width="${bw}" height="${Y(0) - Y(r.sub)}" fill="var(--f3-sub)"/>`
      + `<rect x="${x}" y="${Y(r.total)}" width="${bw}" height="${Y(r.sub) - Y(r.total)}" fill="var(--f3-other)" stroke="var(--ink-3)" stroke-width=".75"/>`
      + `<text x="${cx}" y="${Y(r.total) - 8}" text-anchor="middle" font-size="${narrow ? 12 : 15}" font-weight="800" fill="var(--ink)">${fmtM(r.total)}</text>`
      + `<text x="${cx}" y="${(Y(r.sub) + Y(0)) / 2 + 5}" text-anchor="middle" font-size="${narrow ? 11 : 13}" font-weight="700" fill="#000">${fmtM(r.sub)}</text>`
      + `<text x="${cx}" y="${Y(0) + 20}" text-anchor="middle" font-size="${narrow ? 11 : 13}" font-weight="600" fill="var(--ink-2)">${yr(r)}</text>`;
  });
  return s + '</svg>';
}

export function html(rows, { alt }) {
  return `<div class="f3"><div class="f3-wide">${svg(rows, false, alt)}</div><div class="f3-narrow">${svg(rows, true, alt)}</div></div>`
    + `<div class="f3-legend" aria-hidden="true"><span><i class="sw-sub"></i>Subscription revenue</span><span><i class="sw-other"></i>All other revenue</span></div>`;
}

export function tableHtml(rows) {
  return '<table><caption class="sr">Defector revenue by September-to-August year, $ millions</caption><thead><tr><th scope="col">Year</th><th scope="col">Period</th><th scope="col">Total ($M)</th><th scope="col">Subscription ($M)</th><th scope="col">All other ($M)</th><th scope="col">Annual report</th></tr></thead><tbody>'
    + rows.map(r => `<tr><th scope="row">${r.year}</th><td>${esc(r.period)}</td><td>${r.total}</td><td>${r.sub}</td><td>${r.other}</td><td><a href="${esc(r.report_url)}" rel="noopener" target="_blank">Report</a></td></tr>`).join('')
    + '</tbody></table>';
}

export function mount() { /* static by design */ }
