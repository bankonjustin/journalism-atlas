// Figure 5: revenue band distribution by cohort (n=169). Rows in the paper's order (sorted by share above $10M).
// States: pooled | split | hi-ends | hi-phil. Pooled dots are neutral: group colour (plus a shape) appears only when split.
import { esc, GROUP, BANDS, pct, $, $$, reduced, setHash } from '../lib.js?v=a7031425';

export const id = 'fig-5-bands';
export const STATES = ['pooled', 'split', 'hi-ends', 'hi-phil'];
const HI = { 'hi-ends': ['C1', 'C7', 'C8'], 'hi-phil': ['C4'] };
const layoutOf = s => (s === 'pooled' ? 'pooled' : 'split');
const totals = rows => [0, 1, 2].map(b => rows.reduce((a, r) => a + r.bands[b], 0));
const total = rows => rows.reduce((a, r) => a + r.n, 0);

export function lede(rows, state) {
  const t = totals(rows), n = total(rows), by = c => rows.find(r => r.code === c);
  if (state === 'pooled') return `All ${n} organizations: ${t[0]} below $3.5M, ${t[1]} from $3.5M to $10M, ${t[2]} above $10M.`;
  if (state === 'split') return `The same ${n}, split into nine cohorts.`;
  if (state === 'hi-ends') {
    const l = by('C1'), k = by('C7'), c = by('C8');
    return `Legacy: ${l.bands[2]} of ${l.n} above $10M. Co-ops and civic: ${k.bands[2] + c.bands[2] === 0 ? 'none' : k.bands[2] + c.bands[2]} above $10M.`;
  }
  const p = by('C4');
  return `Philanthropic Networks: ${p.bands[0]} below $3.5M, ${p.bands[1]} in the middle, ${p.bands[2]} above $10M.`;
}

function dot(code, band, bare) { const g = GROUP[code]; return bare ? `<span class="dd g-${g}"></span>` : `<span class="dd g-${g}" data-c="${code}" data-b="${band}"></span>`; }
let BARE = false; // static stacked copies carry no data attributes (smaller HTML); only the live stage needs them
const dots = (code, band, k) => Array.from({ length: k }, () => dot(code, band, BARE)).join('');

export function gridHtml(rows, state) {
  const lay = layoutOf(state), n = total(rows), t = totals(rows);
  let h = `<div class="df-head"><div></div>${BANDS.map(b => `<div>${b}</div>`).join('')}</div>`;
  if (lay === 'pooled') {
    h += `<div class="df-row"><div class="df-label">All organizations<small>n=${n}</small></div>`
      + [0, 1, 2].map(b => `<div class="df-cell"><div class="df-dots" data-c="all" data-b="${b}">${rows.map(r => dots(r.code, b, r.bands[b])).join('')}</div><span class="df-count">${t[b]} (${pct(t[b], n)})</span></div>`).join('') + '</div>';
  } else {
    const hi = HI[state];
    rows.forEach(r => {
      const dim = hi && !hi.includes(r.code);
      h += `<div class="df-row g-${GROUP[r.code]}${dim ? ' dim' : ''}" data-c="${r.code}"><div class="df-label">${esc(r.name)}<small>n=${r.n}</small></div>`
        + r.bands.map((k, b) => `<div class="df-cell"><div class="df-dots" data-c="${r.code}" data-b="${b}">${dots(r.code, b, k)}</div><span class="df-count">${k ? `${k} (${pct(k, r.n)})` : 'none'}</span></div>`).join('') + '</div>';
    });
  }
  return h;
}

export function html(rows, { alt, state = 'pooled', toggle = true, label = true }) {
  BARE = !toggle; const lay = layoutOf(state);
  const tg = toggle ? `<div class="df-toggle" role="group" aria-label="View"><button type="button" data-m="pooled" aria-pressed="${lay === 'pooled'}">All ${total(rows)} together</button><button type="button" data-m="split" aria-pressed="${lay === 'split'}">Split by cohort</button></div>` : '';
  return `<div class="f5" data-state="${state}">${tg}<p class="df-lede" aria-live="polite">${esc(lede(rows, state))}</p>`
    + `<div class="df${lay === 'pooled' ? ' df-pooled' : ''}" role="img" aria-label="${esc(alt)}">${gridHtml(rows, state)}</div>`
    + (BARE = false, label ? `<div class="df-legend" aria-hidden="true"><span class="g-a"><i></i>Legacy, Creator, Barbell</span><span class="g-b"><i></i>Philanthropic, Public Media, Collaboration</span><span class="g-c"><i></i>Co-ops, Civic, B2B</span></div>` : '') + '</div>';
}

export function tableHtml(rows) {
  return '<table><caption class="sr">Organizations in each revenue band, by cohort</caption><thead><tr><th scope="col">Cohort</th><th scope="col">n</th><th scope="col">Below $3.5M</th><th scope="col">$3.5M–$10M</th><th scope="col">Above $10M</th></tr></thead><tbody>'
    + rows.map(r => `<tr><th scope="row">${r.code} ${esc(r.name)}</th><td>${r.n}</td>${r.bands.map(k => `<td>${k} (${pct(k, r.n)})</td>`).join('')}</tr>`).join('')
    + `<tr><th scope="row">All cohorts</th><td>${total(rows)}</td>${totals(rows).map(k => `<td>${k} (${pct(k, total(rows))})</td>`).join('')}</tr></tbody></table>`
    + '<p class="fig-note">Percentages are rounded, so a row can sum to 99 to 101.</p>';
}

// ---- interactive instance (story stage or embed) ----
export function mount(el, { data, state = 'pooled', onChange, animate = true } = {}) {
  const root = $('.f5', el), grid = $('.df', root), lede_ = $('.df-lede', root), btns = $$('.df-toggle button', root);
  const rows = data;
  let cur = root.dataset.state || 'pooled';
  const dotEls = () => $$('.dd', grid);

  function setState(next, { fromUser = false, anim = animate } = {}) {
    if (next === cur) return;
    const a = layoutOf(cur), b = layoutOf(next);
    if (a !== b) {
      const dots = dotEls(), first = new Map();
      if (anim && !reduced()) dots.forEach(d => first.set(d, d.getBoundingClientRect()));
      // rebuild shell, then move the existing dot elements into their new cells
      const holder = document.createElement('div'); holder.innerHTML = gridHtml(rows, next);
      const pool = new Map(); dots.forEach(d => { const k = d.dataset.c + '|' + d.dataset.b; (pool.get(k) || pool.set(k, []).get(k)).push(d); });
      $$('.df-dots', holder).forEach(c => {
        c.innerHTML = '';
        if (c.dataset.c === 'all') { // pooled: every cohort's dots for this band, in cohort order
          rows.forEach(r => (pool.get(r.code + '|' + c.dataset.b) || []).forEach(d => c.appendChild(d)));
        } else { (pool.get(c.dataset.c + '|' + c.dataset.b) || []).forEach(d => c.appendChild(d)); }
      });
      grid.replaceChildren(...holder.childNodes);
      grid.classList.toggle('df-pooled', b === 'pooled');
      if (anim && !reduced()) {
        grid.classList.add('flip'); setTimeout(() => grid.classList.remove('flip'), 1250);
        const now = dotEls(), last = now.map(d => d.getBoundingClientRect());           // all reads first
        now.forEach((d, i) => { const f = first.get(d); if (!f) return;                    // then all writes
          d.style.transition = 'none'; d.style.transform = `translate(${f.left - last[i].left}px,${f.top - last[i].top}px)`; });
        grid.offsetHeight;
        now.forEach((d, i) => { d.style.transition = `transform 900ms cubic-bezier(.65,0,.35,1) ${Math.round(i * 2)}ms`; d.style.transform = 'none'; });
      }
    } else {
      const hi = HI[next];
      $$('.df-row', grid).forEach(r => r.classList.toggle('dim', !!hi && !hi.includes(r.dataset.c)));
    }
    cur = next; root.dataset.state = next;
    lede_.textContent = lede(rows, next);
    btns.forEach(x => x.setAttribute('aria-pressed', x.dataset.m === layoutOf(next)));
    if (onChange) onChange(next, fromUser);
  }
  btns.forEach(x => x.addEventListener('click', () => { setState(x.dataset.m, { fromUser: true }); setHash(x.dataset.m === 'split' ? 'fig-5-split' : 'fig-5-pooled'); }));
  if (state !== cur) setState(state, { anim: false });
  return { setState, get state() { return cur; } };
}
