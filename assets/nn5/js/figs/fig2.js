// Figure 2: the nine cohorts as a transit map. Three lines (the three groups), nine stations sized by n.
import { esc, GROUP, GROUP_LABEL, $, $$, setHash } from '../lib.js?v=a7031425';

export const id = 'fig-2-map';
export const LINES = [['a', ['C1', 'C2', 'C3']], ['b', ['C4', 'C5', 'C6']], ['c', ['C7', 'C8', 'C9']]];
export const size = n => Math.round(20 + Math.sqrt(n / 44) * 26);

export function cardHtml(c) {
  return `<div class="mc-code" aria-hidden="true">${c.code}</div><div class="mc-body"><p class="mc-name"><strong>${esc(c.name)}</strong></p><p>${esc(c.def)}</p>`
    + `<div class="mc-row"><span class="chip chip-solid">n=${c.n}</span><span class="chip">${esc(c.model)}</span></div>`
    + `<p class="mc-ex">Examples: ${c.examples.map(esc).join(' · ')}</p><p class="mc-note">${esc(c.tension)}</p>`
    + `<a class="mc-go" href="#${c.code.toLowerCase()}">Read the full ${c.code} profile</a></div>`;
}

export function html(cards, { alt, sel = 'C1' }) {
  const by = Object.fromEntries(cards.map(c => [c.code, c]));
  let h = `<div class="map" role="group" aria-label="${esc(alt)}"><div class="map-trunk" aria-hidden="true"></div><span class="map-origin" aria-hidden="true"></span>`;
  LINES.forEach(([g, codes]) => {
    h += `<div class="map-line g-${g}" role="group" aria-label="${esc(GROUP_LABEL[g])}">`;
    codes.forEach(code => { const c = by[code];
      h += `<button type="button" class="station" data-id="${code}" aria-pressed="${code === sel}" style="--s:${size(c.n)}px"><span class="st-box"><span class="st-dot"></span></span><span class="st-name">${esc(c.name)}</span><span class="st-n">${code}, n=${c.n}</span></button>`; });
    h += `<div class="lbl">${esc(GROUP_LABEL[g])}</div></div>`;
  });
  h += `</div><div class="map-card g-${GROUP[sel]}" aria-live="polite">${cardHtml(by[sel])}</div>`;
  return h;
}

export function tableHtml(cards) {
  return '<table><caption class="sr">The nine cohorts</caption><thead><tr><th scope="col">Cohort</th><th scope="col">Organizations</th><th scope="col">Revenue model</th><th scope="col">Definition</th><th scope="col">Examples</th></tr></thead><tbody>'
    + cards.map(c => `<tr><th scope="row">${c.code} ${esc(c.name)}</th><td>${c.n}</td><td>${esc(c.model)}</td><td>${esc(c.def)}</td><td>${c.examples.map(esc).join('; ')}</td></tr>`).join('')
    + '</tbody></table>';
}

export function mount(el, { data, state, embed } = {}) {
  const by = Object.fromEntries(data.map(c => [c.code, c])), card = $('.map-card', el);
  const pick = (code, user) => {
    $$('.station', el).forEach(b => b.setAttribute('aria-pressed', b.dataset.id === code));
    card.className = 'map-card g-' + GROUP[code]; card.innerHTML = cardHtml(by[code]);
    if (embed) $$('.mc-go', card).forEach(a => { a.href = '../../#' + code.toLowerCase(); a.target = '_blank'; a.rel = 'noopener'; });
    if (user) setHash('fig-2-' + code.toLowerCase());
  };
  $$('.station', el).forEach(b => b.addEventListener('click', () => pick(b.dataset.id, true)));
  const m = /^fig-2-(c[1-9])$/.exec(state || ''); if (m) pick(m[1].toUpperCase(), false);
  return { pick };
}
