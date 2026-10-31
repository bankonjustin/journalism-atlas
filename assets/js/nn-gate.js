// Nodes and Networks date gate. One config value to fill in at launch; everything else follows.
// SOFT: Justin sets `url` to the paper's published address. Until it is set, home and Overview link to the entry on /research (#nodes-and-networks);
// the entry itself (data-nn-optional) shows no link until `url` is set.
(function () {
  var NN = { publishDate: '2026-11-05', url: '' };

  function todayET() {
    try { return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' }).format(new Date()); }
    catch (e) { return new Date().toISOString().slice(0, 10); }
  }
  var live = todayET() >= NN.publishDate || /[?&]nn=1\b/.test(location.search);
  if (!live) return; // before launch the markup already reads correctly, with no link

  var href = NN.url || '/research#nodes-and-networks';
  document.querySelectorAll('[data-nn-link]').forEach(function (el) {
    if (!NN.url && el.hasAttribute('data-nn-optional')) return;
    var a = document.createElement('a');
    a.href = href;
    a.className = el.getAttribute('data-nn-class') || 'link-instruction';
    a.textContent = 'Read the study →';
    el.replaceWith(a);
  });
})();
