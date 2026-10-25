/* =====================================================
   SHARED SITE HEADER COMPONENT
   Injected synchronously at top of <body> on every page.
   CSS: assets/css/header.css (must be linked in <head>)
   ===================================================== */

/* =====================================================
   SITE STRIP CONFIG (one component, two modes). CSS: assets/css/header.css ("Site strip").
   Rendered above the header, not sticky (it scrolls away). Change this object to retire or swap the strip.
     id        dismissals are stored in localStorage under this id; a new id re-shows the strip
     expires   auto-hides after this date (end of day, local time)
     selfPath  on this path the strip shows `welcome`; everywhere else it shows `announce`
     hideOn    paths with no strip (the homepage has the porch instead)
     {count}   welcome mode only: filled from creators-data.json after page load (see _initStripCount)
   ===================================================== */
var ATLAS_STRIP = {
  id: 'watershed-2026-10',
  enabled: false,
  expires: '2026-11-15',
  selfPath: '/watershed/',
  hideOn: ['/'],
  announce: { label: 'New from the Atlas', text: 'A Watershed Moment for News Deserts', linkText: 'Read the essay', href: '/watershed/' },
  welcome:  { text: 'You\u2019re reading the Independent Journalism Atlas. We map {count} independent journalists by beat and place.',
              links: [ { text: 'Explore the Atlas', href: '/search' }, { text: 'How we find them', href: '/how-we-did-this.html' } ] }
};

// ── GA4 Analytics ────────────────────────────────────────────────────────────
(function() {
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-HZ9F351MRS';
    document.head.appendChild(script);
})();

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-HZ9F351MRS', {
    page_path: window.location.pathname
});

// Safe event helper — guards against ad blockers suppressing gtag
window.atlasTrack = function(eventName, params) {
    if (typeof gtag === 'function') {
        gtag('event', eventName, params || {});
    }
};
// ─────────────────────────────────────────────────────────────────────────────

(function () {
    // Ensure required fonts are loaded (no-op if already present)
    function ensureFont(href) {
        if (!document.querySelector('link[href="' + href + '"]')) {
            var link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            document.head.appendChild(link);
        }
    }
    ensureFont('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    ensureFont('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0');
    // Source Code Pro 500 for v15 Label/Tag/eyebrow/link styles (DESIGN-TOKENS-v15.md § Font Stack). Loaded now so it is
    // available site-wide; nothing switches to it yet (DM Mono / JetBrains Mono are still in use).
    ensureFont('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@500&display=swap');

    // Shared component behaviour (keeps aria-pressed / aria-selected in step with the selected class). See components.js.
    if (!document.querySelector('script[src*="/assets/js/components.js"]')) {
        var cs = document.createElement('script');
        cs.src = '/assets/js/components.js';
        cs.defer = true;
        document.head.appendChild(cs);
    }

    // Header theme: 'white' (default, live) or 'black' (DESIGN-TOKENS-v15.md § Site Header). Pages may request a
    // theme with <html data-header-theme="...">; the CSS lives in header.css. The logo is chosen from the theme:
    // blk on a white header, wht on a black header. The two files share identical geometry, so swapping them
    // causes no layout shift. Never recolor an SVG: swap the file.
    var HEADER_THEMES = {
        white: { logo: '/assets/images/logos/Atlas_logo_lockup_horizontal_blk_web.svg' },
        black: { logo: '/assets/images/logos/Atlas_logo_lockup_horizontal_wht_web.svg' }
    };
    // THE default. v14: white (matches the live site since the first commit). Black is a per-page choice.
    var DEFAULT_HEADER_THEME = 'white';
    var requestedTheme = document.documentElement.getAttribute('data-header-theme');
    var headerTheme = HEADER_THEMES[requestedTheme] ? requestedTheme : DEFAULT_HEADER_THEME;
    document.documentElement.setAttribute('data-header-theme', headerTheme);

    // ── Site strip (config: ATLAS_STRIP at the top of this file) ──
    function stripNorm(p) { return (p || '/').replace(/\/index\.html$/, '/').replace(/\.html$/, '').replace(/(.)\/$/, '$1') || '/'; }
    function stripEsc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
    function buildStrip() {
        var c = ATLAS_STRIP;
        if (!c || !c.enabled) return '';
        if (c.expires && new Date() > new Date(c.expires + 'T23:59:59')) return '';
        var here = stripNorm(window.location.pathname);
        for (var i = 0; i < (c.hideOn || []).length; i++) if (stripNorm(c.hideOn[i]) === here) return '';
        try { if (window.localStorage.getItem(c.id)) return ''; } catch (e) { /* storage blocked: just show the strip */ }
        var welcome = stripNorm(c.selfPath) === here;
        var body;
        if (welcome) {
            var w = c.welcome;
            var parts = w.text.split('{count}');
            var plain = stripEsc(parts.join('').replace(/\s{2,}/g, ' '));
            var msg;
            if (parts.length === 2) {
                // Two stacked versions share one grid cell, so the cell is as tall as the taller one and filling in
                // the count later cannot shift the layout. The no-number sentence shows until the count arrives.
                msg = '<span class="atlas-strip__msg"><span class="atlas-strip__v atlas-strip__v--plain">' + plain + '</span>' +
                      '<span class="atlas-strip__v atlas-strip__v--count" aria-hidden="true">' + stripEsc(parts[0]) +
                      '<span class="js-strip-count">0,000</span> ' + stripEsc(parts[1].replace(/^\s+/, '')) + '</span></span>';
            } else {
                msg = '<span class="atlas-strip__msg"><span class="atlas-strip__v">' + plain + '</span></span>';
            }
            var links = (w.links || []).map(function (l) {
                return '<a class="link-instruction" href="' + stripEsc(l.href) + '">' + stripEsc(l.text) + ' \u2192</a>';
            }).join('');
            body = msg + '<span class="atlas-strip__links">' + links + '</span>';
        } else {
            var a = c.announce;
            body = '<span class="atlas-strip__label">' + stripEsc(a.label) + '</span>' +
                   '<span class="atlas-strip__text">' + stripEsc(a.text) + '</span>' +
                   '<span class="atlas-strip__links"><a class="link-instruction" href="' + stripEsc(a.href) + '">' + stripEsc(a.linkText) + ' \u2192</a></span>';
        }
        return '<div class="atlas-strip" id="atlasStrip" role="region" aria-label="' + (welcome ? 'Welcome to the Atlas' : 'New from the Atlas') + '" data-strip-mode="' + (welcome ? 'welcome' : 'announce') + '">' +
               '<div class="atlas-strip__in"><div class="atlas-strip__body">' + body + '</div>' +
               '<button type="button" class="btn-icon atlas-strip__dismiss" id="atlasStripDismiss" aria-label="Dismiss"><span class="material-symbols-outlined" aria-hidden="true">close</span></button>' +
               '</div></div>';
    }
    var stripHtml = buildStrip();

    var html = stripHtml + [
        '<nav class="top-nav" id="siteTopNav" data-header-theme="' + headerTheme + '">',
        '  <div class="nav-container">',
        '    <div class="nav-logo-search">',
        '      <!-- FLAG FOR JAMES: logo wordmark length — consider icon-only treatment to free nav space -->',
        '      <a href="/" class="nav-logo">',
        '        <img src="' + HEADER_THEMES[headerTheme].logo + '" alt="Independent Journalism Atlas">',
        '      </a>',
        '      <div class="nav-search-container">',
        '        <input type="text" class="nav-search" placeholder="Search creators, topics, places..." id="navSearch" autocomplete="off" aria-label="Search creators, topics, places">',
        '        <button class="nav-search-btn" id="nav-search-btn" type="button">Search</button>',
        '      </div>',
        '    </div>',
        '    <div class="nav-links">',
        '      <a href="/pulse.html" class="nav-link nav-link--pulse"><span class="nav-pulse-dot"></span>Pulse</a>',
        '      <a href="/for-brands.html" class="nav-link">For Brands</a>',
        '      <a href="/research" class="nav-link">Research &amp; Writing</a>',
        '      <a href="/how-we-did-this.html" class="nav-link">How it works</a>',
        '    </div>',
        '    <button class="mobile-menu-button" id="mobileMenuButton" aria-label="Open menu">',
        '      <span class="material-symbols-outlined" aria-hidden="true">menu</span>',
        '    </button>',
        '  </div>',
        '</nav>',
        '<div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>',
        '<div class="mobile-menu" id="mobileMenu">',
        '  <div class="mobile-menu-header">',
        '    <strong>Menu</strong>',
        '    <button class="mobile-menu-close" id="mobileMenuClose" aria-label="Close menu">',
        '      <span class="material-symbols-outlined" aria-hidden="true">close</span>',
        '    </button>',
        '  </div>',
        '  <nav class="mobile-menu-links">',
        '    <a href="/pulse.html" class="mobile-menu-link">Pulse</a>',
        '    <a href="/for-brands.html" class="mobile-menu-link">For Brands</a>',
        '    <a href="/research" class="mobile-menu-link">Research &amp; Writing</a>',
        '    <a href="/how-we-did-this.html" class="mobile-menu-link">How it works</a>',
        '    <a href="/submit" class="mobile-menu-link">Submit</a>',
        '    <a href="/partners" class="mobile-menu-link">Partners</a>',
        '    <a href="/about-this-project.html" class="mobile-menu-link">About</a>',
        '    <a href="/contact.html" class="mobile-menu-link">Contact</a>',
        '  </nav>',
        '</div>'
    ].join('\n');

    // Insert header as first content in <body>
    document.currentScript
        ? document.currentScript.insertAdjacentHTML('beforebegin', html)
        : document.body.insertAdjacentHTML('afterbegin', html);

    if (stripHtml) {
        document.getElementById('atlasStripDismiss').addEventListener('click', function () {
            try { window.localStorage.setItem(ATLAS_STRIP.id, '1'); } catch (e) { /* ignore */ }
            var el = document.getElementById('atlasStrip');
            if (el && el.parentNode) el.parentNode.removeChild(el);
        });
        _initStripCount();
    }

    // Welcome mode only: fetch the creator count after the page has loaded and fill it in. Announce mode never fetches.
    // If the fetch fails the no-number sentence stays.
    function _initStripCount() {
        var strip = document.getElementById('atlasStrip');
        if (!strip || strip.getAttribute('data-strip-mode') !== 'welcome' || !strip.querySelector('.js-strip-count')) return;
        function run() {
            fetch('/assets/data/creators-data.json').then(function (r) { return r.json(); }).then(function (data) {
                if (!data || !data.length) return;
                var span = strip.querySelector('.js-strip-count');
                if (!span) return;
                span.textContent = data.length.toLocaleString();
                strip.setAttribute('data-count-ready', '');
                var v = strip.querySelector('.atlas-strip__v--count');
                if (v) v.removeAttribute('aria-hidden');
            }).catch(function () {});
        }
        if (document.readyState === 'complete') run(); else window.addEventListener('load', run);
    }

    // Phones (≤640px): the search box does not fit in the header, so move the same node into the mobile menu
    // (ids and event handlers stay as they are) and put it back above 640px. header.css has the matching styles.
    (function () {
        var mq = window.matchMedia('(max-width: 640px)');
        function placeSearch() {
            var box = document.querySelector('.nav-search-container');
            var menu = document.getElementById('mobileMenu');
            var home = document.querySelector('.nav-logo-search');
            var links = menu && menu.querySelector('.mobile-menu-links');
            if (!box || !home || !links) return;
            if (mq.matches) { if (box.parentNode !== menu) menu.insertBefore(box, links); }
            else if (box.parentNode !== home) home.appendChild(box);
        }
        placeSearch();
        if (mq.addEventListener) mq.addEventListener('change', placeSearch); else mq.addListener(placeSearch);
    }());

    // Mark the current page in the nav. header.css styles both values as "selected".
    //   aria-current="page": the nav item's own page (exact match; ".html" and trailing slash ignored)
    //   aria-current="true": a page inside that nav item's section (sub-pages)
    // SECTIONS lists the sub-pages per nav item. Add new sub-pages here.
    var SECTIONS = {
        '/research':            { prefixes: ['/research/'] },
        '/submit':              { pages: ['/submit-thanks'] },
        '/partners':            { prefixes: ['/partners/'] },
        '/about-this-project':  { pages: ['/who-we-are', '/advisory'] }
    };
    (function () {
        function norm(p) { return (p || '/').replace(/\/index\.html$/, '/').replace(/\.html$/, '').replace(/(.)\/$/, '$1') || '/'; }
        var here = norm(window.location.pathname);
        var links = document.querySelectorAll('#siteTopNav .nav-link, #mobileMenu .mobile-menu-link');
        for (var i = 0; i < links.length; i++) {
            var a = document.createElement('a'); a.href = links[i].getAttribute('href');
            var target = norm(a.pathname);
            if (target === here) { links[i].setAttribute('aria-current', 'page'); continue; }
            var sec = SECTIONS[target];
            if (!sec) continue;
            var inSection = (sec.pages && sec.pages.indexOf(here) !== -1) ||
                (sec.prefixes && sec.prefixes.some(function (p) { return here.indexOf(p) === 0; }));
            if (inSection) links[i].setAttribute('aria-current', 'true');
        }
    }());

    // Wire up behaviors after DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        _initScroll();
        _initMobileMenu();
        _initSearch();
    });

    function _initScroll() {
        var nav = document.getElementById('siteTopNav');
        if (!nav) return;
        window.addEventListener('scroll', function () {
            nav.classList.toggle('scrolled', window.scrollY > 10);
        }, { passive: true });
    }

    function _initMobileMenu() {
        var btn     = document.getElementById('mobileMenuButton');
        var menu    = document.getElementById('mobileMenu');
        var overlay = document.getElementById('mobileMenuOverlay');
        var close   = document.getElementById('mobileMenuClose');
        if (!btn || !menu) return;

        function openMenu()  { menu.classList.add('active'); overlay.classList.add('active'); }
        function closeMenu() { menu.classList.remove('active'); overlay.classList.remove('active'); }

        btn.addEventListener('click', openMenu);
        close.addEventListener('click', closeMenu);
        overlay.addEventListener('click', closeMenu);
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && menu.classList.contains('active')) closeMenu();
        });
    }

    function _initSearch() {
        var input = document.getElementById('navSearch');
        if (!input) return;

        // On the search page main.js owns the search; skip navigation handler
        var path = window.location.pathname;
        var isSearch = path === '/search' || path === '/search.html' || path.endsWith('/search.html');
        if (isSearch) return;

        function doSearch() {
            var q = input.value.trim();
            window.location.href = q ? '/search?search=' + encodeURIComponent(q) : '/search';
        }

        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') doSearch();
        });

        var btn = document.getElementById('nav-search-btn');
        if (btn) btn.addEventListener('click', doSearch);
    }
}());
