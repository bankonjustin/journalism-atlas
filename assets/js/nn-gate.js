// Nodes and Networks time gate. One config value to fill in at launch; everything else follows.
// publishAt is an instant with an ET offset. D8 placeholder (noon ET); confirm with the ASU release time.
// SOFT: Justin sets `url` to the paper's published address. Until it is set, home and Overview link to the entry on /research (#nodes-and-networks);
// the entry itself (data-nn-optional) shows no link until `url` is set.
(function () {
  var NN = { publishAt: '2026-11-05T12:00:00-05:00', url: '/nodes-and-networks/' };

  var live = Date.now() >= Date.parse(NN.publishAt) || /[?&]nn=1\b/.test(location.search);
  if (!live) return; // before launch the markup already reads correctly, with no link

  // Elements that exist only after launch (e.g. the N&N line on /for-brands): same switch, same instant.
  document.querySelectorAll('[data-nn-show]').forEach(function (el) { el.hidden = false; });

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
