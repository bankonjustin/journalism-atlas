// Scene S10: "Stations under construction." Dashed neutral lines extend off the network for each item Section IV
// names, labelled with the copy's own nouns and dates. Neutral ink only (group colours are data, not decoration).
// Draws once, when it scrolls into view; reduced motion shows the final state.
import { esc, $$, onVisible, reduced } from '../lib.js?v=a7031425';

export const id = 'close';
export const ITEMS = [
  ['Cloudflare: charging AI crawlers, July 2025', 62],
  ['Cloudflare: pay per use, July 2026', 74],
  ['RSL', 38],
  ['Free Our Feeds', 52],
  ['AT Protocol', 46],
  ['Lenfest: newsroom–creator partnerships', 80],
];

export function html() {
  return `<section class="close" aria-labelledby="close-h"><p class="close-kicker" id="close-h">Stations under construction</p><ul class="close-list">`
    + ITEMS.map(([t, len], i) => `<li style="--len:${len}%;--i:${i}"><span class="close-trunk" aria-hidden="true"></span><span class="close-stub" aria-hidden="true"></span><span class="close-node" aria-hidden="true"></span><span class="close-label">${esc(t)}</span></li>`).join('')
    + `</ul><span class="close-run" aria-hidden="true"></span></section>`;
}

export function mount(el) {
  if (reduced()) { el.classList.add('in'); return; }
  onVisible(el, () => el.classList.add('in'), .25);
}
