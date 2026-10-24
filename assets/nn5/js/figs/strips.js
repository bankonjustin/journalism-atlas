// Scene S4: a band strip for each cohort header, built from Figure 5's counts only. Neutral tints: group colour is
// already carried by the cohort line above it. No mechanism counts.
import { BANDS, esc } from '../lib.js?v=a7031425';

export const id = 'band-strips';

export function html(row) {
  const [lo, mid, hi] = row.bands, n = row.n;
  const alt = `${row.code}: ${lo} below $3.5M, ${mid} from $3.5M to $10M, ${hi} above $10M (n=${n})`;
  const seg = (k, i) => k ? `<span class="bs-seg bs-${i}" style="flex:${k}"><b>${k}</b></span>` : '';
  return `<div class="band-strip" role="img" aria-label="${esc(alt)}"><div class="bs-bar">${row.bands.map(seg).join('')}</div>`
    + `<div class="bs-key" aria-hidden="true">${BANDS.map((b, i) => `<span><i class="bs-sw bs-${i}"></i>${b}</span>`).join('')}</div></div>`;
}
