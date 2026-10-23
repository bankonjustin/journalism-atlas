// Figure 4: share of revenue from grants and donations, 17 nonprofit newsrooms with $3.5M-$10M revenue.
// Static apart from the slider. 80% is the paper's threshold and the default; Reset returns to it.
// Counts compare the displayed (rounded) percentages with a strict ">", so the sentence is honest at every value.
import { esc, $, $$, setHash } from '../lib.js';

export const id = 'fig-4-threshold';
export const PAPER = 80;

const count = (rows, t) => rows.filter(r => r.pct > t).length;
export function readout(rows, t) {
  const k = count(rows, t);
  return `<b>${k} of ${rows.length}</b> get more than ${t}% of revenue from grants and donations.`
    + (t === PAPER ? ' <span class="lp-paper">80% is the threshold used in the paper.</span>'
      : ` <span class="lp-paper">The paper uses 80%.</span>`);
}

export function html(rows, { alt, threshold = PAPER, controls = true }) {
  const t = threshold;
  const ctl = controls
    ? `<div class="lp-controls"><label for="lpRange">Move the dependence threshold</label>`
      + `<input type="range" id="lpRange" min="40" max="99" step="1" value="${t}" aria-valuetext="${t} percent" aria-describedby="lpOut">`
      + `<output class="lp-val-now" for="lpRange" aria-hidden="true">${t}%</output>`
      + `<button type="button" class="btn-reset" id="lpReset"${t === PAPER ? ' hidden' : ''}>Reset to 80%</button></div>`
    : '';
  const plot = rows.map(r =>
    `<div class="lp-row${r.pct > t ? ' over' : ''}" data-v="${r.pct}"><span class="lp-name" title="${esc(r.name)}">${esc(r.name)}</span>`
    + `<span class="lp-track"><span class="lp-stem" style="width:${r.pct}%"></span><span class="lp-dot" style="left:${r.pct}%"></span></span>`
    + `<span class="lp-val">${r.pct}%</span></div>`).join('');
  return `${ctl}<p class="lp-readout" id="lpOut" aria-live="polite">${readout(rows, t)}</p>`
    + `<div class="lp" role="img" aria-label="${esc(alt)}"><div class="lp-plot" style="--t:${t}">${plot}<div class="lp-th"><span>${t}%</span></div></div></div>`
    + `<p class="lp-key" aria-hidden="true"><span class="k-over"></span>more than the threshold <span class="k-under"></span>at or below it</p>`;
}

export function tableHtml(rows) {
  return '<table><caption class="sr">Share of revenue from grants and donations, by organization</caption><thead><tr><th scope="col">Organization</th><th scope="col">Grants and donations (% of revenue)</th><th scope="col">Filing year</th></tr></thead><tbody>'
    + rows.map(r => `<tr><th scope="row">${esc(r.name)}</th><td>${r.pct}%</td><td>${esc(r.filing_year)}</td></tr>`).join('')
    + '</tbody></table>';
}

export function mount(el, { data, state } = {}) {
  const rows = data, rng = $('#lpRange', el), out = $('#lpOut', el), plot = $('.lp-plot', el), th = $('.lp-th', el),
    reset = $('#lpReset', el), now = $('.lp-val-now', el);
  if (!rng) return;
  function place(userSet) {
    const t = +rng.value;
    plot.style.setProperty('--t', t); th.firstChild.textContent = t + '%';
    $$('.lp-row', plot).forEach(row => row.classList.toggle('over', +row.dataset.v > t));
    out.innerHTML = readout(rows, t);
    rng.setAttribute('aria-valuetext', t + ' percent'); if (now) now.textContent = t + '%';
    if (reset) reset.hidden = t === PAPER;
    if (userSet) setHash(t === PAPER ? 'fig-4-threshold' : 'fig-4-' + t);
  }
  rng.addEventListener('input', () => place(true));
  reset.addEventListener('click', () => { rng.value = PAPER; place(true); rng.focus(); });
  const m = /^fig-4-(\d\d)$/.exec(state || '');
  if (m && +m[1] >= 40 && +m[1] <= 99) rng.value = m[1];
  place(false);
}
