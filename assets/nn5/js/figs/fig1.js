// Figure 1: funding and organization timeline, 2018-2026. Four lanes, 15 dated events.
// Static render: a horizontal SVG (>= 700px) and a vertical list (< 700px). Static default selection is the
// earliest event. With a scroll engine (wide screens, no reduced motion) the lines draw left to right as the reader
// scrolls and selection follows the latest lit station.
import { esc, GROUP, clamp, $, $$, reduced, scene, pinProgress } from '../lib.js';

export const id = 'fig-1-timeline';
const W = 900, X0 = 40, X1 = W - 30, LANE_GAP = 104, Y0 = 92, H = 456;
const X = t => X0 + ((t - 2018) / 9) * (X1 - X0);
const laneClass = i => 'lane-' + i;

function layout(data) {
  const { lanes, events } = data;
  const pos = [];
  lanes.forEach((ln, li) => {
    let last = -99;
    events.filter(e => e.lane === ln).forEach(e => {
      let x = X(e.t); if (x - last < 26) x = last + 26; last = x;
      pos.push({ e, li, x, y: Y0 + li * LANE_GAP });
    });
  });
  return pos;
}
const chip = t => {
  const m = /^C(\d)/.exec(t), g = m ? GROUP['C' + m[1]] : '';
  return `<span class="tag${g ? ' g-' + g : ''}"><i></i>${esc(t)}</span>`;
};
export function detail(e) {
  return `<span class="when">${esc(e.date)}</span><span class="what">${esc(e.label)}</span>`
    + `<span class="tags"><span class="tag"><i></i>${esc(e.lane)}</span>${e.tags.map(chip).join('')}${e.tags.length ? '' : '<span class="tag">No cohort tagged</span>'}</span>`;
}

export function html(data, { alt }) {
  const { lanes, events } = data, pos = layout(data), first = events[0];
  let s = `<svg class="tl-svg" viewBox="0 0 ${W} ${H}" role="group" aria-label="${esc(alt)}">`;
  for (let y = 2018; y <= 2026; y++) {
    const x = X(y);
    s += `<line x1="${x}" x2="${x}" y1="28" y2="${H - 10}" stroke="var(--rule)"/><text x="${x}" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--ink-3)">${y}</text>`;
  }
  lanes.forEach((ln, li) => {
    const y = Y0 + li * LANE_GAP;
    s += `<text x="${X0}" y="${y - 26}" font-size="14" font-weight="800" fill="var(--ink)">${esc(ln)}</text>`
      + `<path class="tl-line ${laneClass(li)}" pathLength="1" d="M${X0} ${y} H${X1}" fill="none" stroke-linecap="round"/>`;
  });
  pos.forEach(({ e, x, y, li }, i) => {
    const idx = events.indexOf(e);
    s += `<g class="tl-node lit${idx === 0 ? ' on' : ''}" tabindex="0" role="button" aria-pressed="${idx === 0}" data-i="${idx}" data-x="${((x - X0) / (X1 - X0)).toFixed(4)}" aria-label="${esc(e.date + ': ' + e.label)}">`
      + `<circle class="hit" cx="${x}" cy="${y}" r="22" fill="transparent"/><circle class="halo" cx="${x}" cy="${y}" r="20"/><circle class="dot" cx="${x}" cy="${y}" r="10"/></g>`;
  });
  s += '</svg>';
  const list = lanes.map(ln => `<section class="tl-lane" aria-label="${esc(ln)}"><p class="tl-lane-h">${esc(ln)}</p><ol>`
    + events.filter(e => e.lane === ln).map(e => `<li><span class="when">${esc(e.date)}</span><span class="what">${esc(e.label)}</span>${e.tags.length ? `<span class="tags">${e.tags.map(chip).join('')}</span>` : ''}</li>`).join('')
    + '</ol></section>').join('');
  return `<div class="tl"><p class="hint tl-hint">Select any station to see the event and the cohorts it hit.</p>`
    + `<div class="tl-desk">${s}<div class="tl-detail" aria-live="polite">${detail(first)}</div></div>`
    + `<div class="tl-mobile" aria-label="${esc(alt)}">${list}</div></div>`;
}

export function tableHtml(data) {
  return '<table><caption class="sr">Funding and organization events, 2018 to 2026</caption><thead><tr><th scope="col">Date</th><th scope="col">Lane</th><th scope="col">Event</th><th scope="col">Cohorts tagged</th><th scope="col">Source</th></tr></thead><tbody>'
    + data.events.map(e => `<tr><th scope="row">${esc(e.date)}</th><td>${esc(e.lane)}</td><td>${esc(e.label)}</td><td>${e.tags.length ? esc(e.tags.join('; ')) : 'none'}</td><td><a href="${esc(e.source_url)}" rel="noopener" target="_blank">Source<span class="sr"> (opens in new tab)</span></a></td></tr>`).join('')
    + '</tbody></table>';
}

export function mount(el, { data, scrub = true } = {}) {
  const events = data.events, nodes = $$('.tl-node', el), det = $('.tl-detail', el), svg = $('.tl-svg', el);
  if (!svg) return;
  let pinnedAt = -1;
  const select = (i, user) => {
    nodes.forEach(n => { const on = +n.dataset.i === i; n.classList.toggle('on', on); n.setAttribute('aria-pressed', on); });
    det.innerHTML = detail(events[i]);
    if (user) pinnedAt = curP;
  };
  nodes.forEach(g => {
    const go = () => select(+g.dataset.i, true);
    g.addEventListener('click', go); g.addEventListener('focus', go);
    g.addEventListener('keydown', ev => {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(); }
      const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
      if (step) { ev.preventDefault(); const t = nodes.find(n => +n.dataset.i === +g.dataset.i + step); if (t) t.focus(); }
    });
  });
  let curP = 1;
  const host = el.closest('.tl-scene');
  if (!scrub || !host || reduced() || innerWidth < 900) return;
  host.classList.add('scrub-on');
  const hint = $('.tl-hint', el); if (hint) hint.textContent = 'Scroll to light the stations, or select any one to see the event and the cohorts it hit.';
  const mq = matchMedia('(max-width: 899px)');
  scene(host, (r, vh) => {
    if (mq.matches) { host.classList.remove('scrub-on'); svg.style.removeProperty('--p'); nodes.forEach(n => n.classList.add('lit')); return; }
    host.classList.add('scrub-on');
    const p = pinProgress(r, vh); curP = p;
    svg.style.setProperty('--p', p.toFixed(4));
    let lastLit = 0;
    nodes.forEach(n => { const lit = +n.dataset.x <= p + 0.001; n.classList.toggle('lit', lit); if (lit) lastLit = Math.max(lastLit, +n.dataset.i); });
    if (pinnedAt >= 0 && Math.abs(p - pinnedAt) > .03) pinnedAt = -1;
    if (pinnedAt < 0) {
      // follow the latest lit station in date order
      const litIdx = nodes.filter(n => n.classList.contains('lit')).map(n => +n.dataset.i);
      const want = litIdx.length ? Math.max(...litIdx) : 0;
      if (!nodes[0] || !nodes.find(n => +n.dataset.i === want && n.classList.contains('on'))) select(want, false);
    }
  });
}
