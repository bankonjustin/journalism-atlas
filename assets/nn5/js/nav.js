// Scene S3: Section II navigation. Desktop (>= 1180px): a compact dock down the left edge. Below that: a "Map" button
// that opens the same list as a bottom sheet. Shown only while the reader is inside Section II; it highlights the
// current cohort's station. Replaces the old dot rail.
import { esc, GROUP, GROUP_LABEL, $, $$, scene, onVisible } from './lib.js';
import { LINES } from './figs/fig2.js';

export function dockHtml(cards) {
  const by = Object.fromEntries(cards.map(c => [c.code, c]));
  return `<nav class="dock" id="dock" aria-label="Cohorts" hidden><div class="dock-head"><span>Cohorts</span><button type="button" class="dock-x" aria-label="Close map">Close</button></div>`
    + LINES.map(([g, codes]) => `<div class="dock-line g-${g}" role="group" aria-label="${esc(GROUP_LABEL[g])}"><ol>`
      + codes.map(c => `<li><a href="#${c.toLowerCase()}" data-c="${c}" aria-label="${c} ${esc(by[c].name)}, ${by[c].n} organizations"><i class="mk"></i><span class="dk-code">${c}</span><span class="dk-name">${esc(by[c].name)}</span><span class="dk-n">n=${by[c].n}</span></a></li>`).join('')
      + '</ol></div>').join('')
    + `<a class="dock-map" href="#fig-2-map">Back to the map</a></nav>`
    + `<button type="button" class="dock-btn" id="dockBtn" aria-controls="dock" aria-expanded="false" hidden>Map</button><div class="dock-scrim" hidden></div>`;
}

export function mount() {
  const dock = $('#dock'), btn = $('#dockBtn'), scrim = $('.dock-scrim'), sec = $('#cohorts');
  if (!dock || !sec) return;
  const wide = matchMedia('(min-width: 1180px)'), links = $$('a[data-c]', dock);
  let last = null, open = false;
  const setOpen = (v, restore = true) => {
    open = v; dock.classList.toggle('open', v); btn.setAttribute('aria-expanded', v); scrim.hidden = !v;
    if (v && !wide.matches) { dock.setAttribute('role', 'dialog'); dock.setAttribute('aria-modal', 'true'); dock.setAttribute('aria-label', 'Cohort map'); (links.find(a => a.classList.contains('cur')) || links[0]).focus(); }
    else { dock.removeAttribute('role'); dock.removeAttribute('aria-modal'); dock.setAttribute('aria-label', 'Cohorts'); if (restore && !v && last === 'btn') btn.focus(); }
  };
  btn.addEventListener('click', () => { last = 'btn'; setOpen(!open); });
  scrim.addEventListener('click', () => setOpen(false));
  $('.dock-x', dock).addEventListener('click', () => setOpen(false));
  dock.addEventListener('click', e => { if (e.target.closest('a') && !wide.matches) setOpen(false, false); });
  addEventListener('keydown', e => {
    if (!open || wide.matches) return;
    if (e.key === 'Escape') { setOpen(false); return; }
    if (e.key === 'Tab') { // keep focus inside the sheet
      const f = $$('a,button', dock).filter(x => x.offsetParent); if (!f.length) return;
      const a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    }
  });
  wide.addEventListener('change', () => setOpen(false, false));
  const cohorts = $$('.cohort');
  scene(sec, (r, vh) => {
    const inside = r.top < vh * .6 && r.bottom > vh * .35;
    dock.hidden = !inside && !open; btn.hidden = !inside || wide.matches;
    if (!inside) return;
    let cur = null;
    cohorts.forEach(c => { if (c.getBoundingClientRect().top < vh * .45) cur = c.id.toUpperCase(); });
    links.forEach(a => { const on = a.dataset.c === cur; a.classList.toggle('cur', on); if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
  });
}
