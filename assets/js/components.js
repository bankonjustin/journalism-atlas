/* =====================================================
   SHARED COMPONENT BEHAVIOUR (v15)
   Loaded by header.js on every page. docs/design/DESIGN-TOKENS-v15.md § Interactive States

   Keeps the ARIA state v15 styles from in step with the "selected" class the page scripts
   already toggle. For every secondary button that sits in a group of two or more (a filter row,
   a toggle group, a tab strip) it mirrors the class onto:
     aria-pressed="true|false"   for toggle filters
     aria-selected="true|false"  for tabs (role="tab", or inside role="tablist")
   Page scripts keep toggling their own class (.active, .is-selected, .selected, *--active);
   they don't need to know about ARIA. A button outside a group (a lone action) is left alone,
   and so is any button that opts out with data-no-state.
   ===================================================== */
(function () {
    var SELECTED = /^(active|is-active|selected|is-selected|current)$|--(active|selected)$/;

    function isSelected(el) {
        for (var i = 0; i < el.classList.length; i++) {
            if (SELECTED.test(el.classList[i])) return true;
        }
        return false;
    }
    function inGroup(el) {
        var p = el.parentElement;
        if (!p) return false;
        var n = 0;
        for (var i = 0; i < p.children.length; i++) {
            if (p.children[i].classList.contains('btn--secondary')) n++;
        }
        return n >= 2;
    }
    function sync(el) {
        if (el.hasAttribute('data-no-state') || !inGroup(el)) return;
        var isTab = el.getAttribute('role') === 'tab' || !!el.closest('[role="tablist"]');
        var attr = isTab ? 'aria-selected' : 'aria-pressed';
        var val = isSelected(el) ? 'true' : 'false';
        if (el.getAttribute(attr) !== val) el.setAttribute(attr, val);
    }
    function scan(root) {
        if (!root || !root.querySelectorAll) return;
        if (root.matches && root.matches('.btn--secondary')) sync(root);
        var list = root.querySelectorAll('.btn--secondary');
        for (var i = 0; i < list.length; i++) sync(list[i]);
    }

    function start() {
        scan(document);
        new MutationObserver(function (muts) {
            muts.forEach(function (m) {
                if (m.type === 'attributes') {
                    if (m.target.classList && m.target.classList.contains('btn--secondary')) sync(m.target);
                } else {
                    for (var i = 0; i < m.addedNodes.length; i++) {
                        if (m.addedNodes[i].nodeType === 1) scan(m.addedNodes[i]);
                    }
                    if (m.target.nodeType === 1) scan(m.target.parentElement || m.target);
                }
            });
        }).observe(document.documentElement, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'] });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
    else start();
}());
