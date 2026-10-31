/* Nodes and Networks: ASU theme switch. Classic script, loaded synchronously in <head> (figures) or inlined by nn/build.py (explorer).
   The ASU theme is on when the URL has ?embed=1 or ?theme=asu. Without either, nothing here changes anything: the default edition is untouched.
   Single source of truth for the colors canvas and SVG code needs; the CSS variables live in nn-theme.css. */
(function () {
  var on = /[?&](?:theme=asu|embed=1)(?:&|$)/.test(location.search);
  window.NN_ASU_ON = on;
  if (!on) return;
  document.documentElement.setAttribute('data-nn-theme', 'asu');
  window.NN_FAM = 'Arial,Helvetica,sans-serif';
  // group colors and canvas neutrals on the black stage (a = journalism as most people picture it, b = philanthropy and public money, c = audiences and the market)
  window.NN_ASU_T = { a: '#FFC627', b: '#E74973', c: '#BFBFBF', neutral: '#747474', ink: '#fff', ink2: '#D0D0D0', grid: '#484848' };
  // literal grays and group hexes the explorer writes into SVG strings: old value -> ASU value (lowercase keys)
  var MAP = { '#bdbdbd': '#D0D0D0', '#d2d2d2': '#E8E8E8', '#cfcfcf': '#D0D0D0', '#8f8f8f': '#BFBFBF', '#8a8a8a': '#BFBFBF', '#9a9a9a': '#BFBFBF', '#a8a8a8': '#BFBFBF', '#7c7c7c': '#747474',
    '#666': '#747474', '#6a6a6a': '#747474', '#444': '#484848', '#4a4a4a': '#484848', '#3a3a3a': '#484848', '#2e2e2e': '#484848', '#262626': '#484848', '#1d1d1d': '#484848',
    '#f6c84e': '#FFC627', '#b23a5e': '#E74973' };
  window.NN_ASU_MAP = MAP;
  window.nnAsu = function (s) { return String(s).replace(/#[0-9a-fA-F]{3,6}\b/g, function (h) { return MAP[h.toLowerCase()] || h; }); };
})();
