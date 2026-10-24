// The opening: the turn plays once inside the explorer's own canvas (the reference turnState, from the spiral to the end of the cohort
// sweep), hands off to the lens buttons, and cues the other lenses. Loaded on demand, so embeds without the opening never fetch it.
const SWEEP0 = 8900;

export function play(c) {
  const { N, LENS, cohorts, over, hint, btns, T, ss, eio, cl } = c;
  const SW = cohorts.map(q => (q.n < 10 ? 470 : 300)), SWEEP1 = SWEEP0 + SW.reduce((a, b) => a + b, 0), END = SWEEP1 + 900, n = N.length;
  const grp = k => N.find(d => d.ci === k).g;
  const sweepAt = t => { if (t < SWEEP0 || t >= SWEEP1) return -1; let s = SWEEP0; for (let k = 0; k < SW.length; k++) { s += SW[k]; if (t < s) return k; } return -1; };
  const ang = p => ((Math.atan2(p.y, p.x) + Math.PI / 2 + 4 * Math.PI) % (2 * Math.PI)) / (2 * Math.PI);
  const seg = Math.PI / 9;
  function fold(ctx, G, pos, mirror, appear) {                      // the kaleidoscope fold: illustration only, the marks are not repositioned by it
    N.forEach((d, i) => {
      const p = pos[i], r = Math.hypot(p.x, p.y); let a = ((Math.atan2(p.y, p.x) % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI); const k = Math.floor(a / seg); let loc = a - k * seg; if (k % 2) loc = seg - loc;
      const s = c.sz(d) * G.R * .85; ctx.globalAlpha = mirror * appear[i] * .9;
      for (let j = 0; j < 18; j++) { const an = j * seg + (j % 2 ? seg - loc : loc); c.shape(G.cx + Math.cos(an) * r * G.R, G.cy + Math.sin(an) * r * G.R, s, 'a', c.mix(T.neutral, '#BDBDBD', r), false, false); }
    });
    ctx.globalAlpha = 1;
  }
  function turnState(t) {
    const spin = 1.6 * Math.PI * eio(cl(t / 6400)), ca = Math.cos(spin), sa = Math.sin(spin), mirror = ss(1500, 2600, t) * (1 - ss(4200, 5000, t)), gov = LENS.gov.pos, fld = LENS.field.pos;
    const pos = [], ce = [], appear = [];
    N.forEach((d, i) => {
      const s = fld[i], fx = s.x * ca - s.y * sa, fy = s.x * sa + s.y * ca, g = gov[i], e = eio(cl((t - 5300 - ang(g) * 450) / 2200));
      pos.push({ x: fx + (g.x - fx) * e, y: fy + (g.y - fy) * e }); ce.push(ss(.78, 1, e)); appear.push(ss(d.fk / n * 1000, d.fk / n * 1000 + 260, t));
    });
    const sw = sweepAt(t);
    return { pos, ce, appear, pop: true, lens: 'gov', mirror, fold: (ctx, G) => fold(ctx, G, pos, mirror, appear), chromeA: ss(8000, 8800, t), zonesA: ss(7700, 8600, t), ringT: ss(7700, 8600, t), zoneLabelA: ss(8300, 9000, t), yearsA: 0, hl: sw < 0 ? null : sw };
  }
  function overlay(t) {
    let h = '';
    if (t < 1400) h = `<p class="big">${n} organizations.</p>`;
    else if (t < 4600) h = '<p class="small">Seen from far away.</p>';
    else if (t < 7700) h = '<p class="big">Now sort by governance.</p>';
    else if (t < SWEEP0) h = '<p class="small">Closer to the center, smaller budgets.</p>';
    else { const k = sweepAt(t); if (k >= 0) h = `<p class="coh ${grp(k)}">${cohorts[k].code}<span>${cohorts[k].name.replace(/&/g, '&amp;')}</span></p>`; }
    if (over.dataset.h !== h) { over.innerHTML = h; over.dataset.h = h; }
  }
  // the cue: the other lens buttons pulse in turn, three rounds, until the reader acts
  let timer = null;
  const stopCue = keep => { clearInterval(timer); timer = null; btns.forEach(b => b.classList.remove('pulse')); if (!keep) hint.classList.remove('on'); };
  c.cue = () => {
    stopCue(); hint.classList.add('on'); const others = btns.filter(b => b.getAttribute('aria-pressed') !== 'true'); let k = 0;
    timer = setInterval(() => { btns.forEach(b => b.classList.remove('pulse')); if (k >= others.length * 3) { stopCue(true); return; } others[k % others.length].classList.add('pulse'); k++; }, 650);
  };
  c.onAct = () => stopCue();
  stopCue(); c.begin();
  const t0 = performance.now();
  let lit = false;
  const step = now => {
    if (c.mode !== 'intro') return;
    const t = now - t0; if (!lit && t >= 7000) { lit = true; c.press(); }                 // Governance is pressed when the marks land, not before c.draw(turnState(Math.min(t, SWEEP1))); overlay(t);
    if (t < END) c.raf(step); else c.end(true);
  };
  c.raf(step);
}
