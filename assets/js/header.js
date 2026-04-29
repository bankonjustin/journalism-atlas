/* =====================================================
   SHARED SITE HEADER COMPONENT
   Injected synchronously at top of <body> on every page.
   CSS: assets/css/header.css (must be linked in <head>)
   ===================================================== */

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
    ensureFont('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;700&display=swap');
    ensureFont('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0');

    var html = [
        '<nav class="top-nav" id="siteTopNav">',
        '  <div class="nav-container">',
        '    <div class="nav-logo-search">',
        '      <a href="/" class="nav-logo">',
        '        <img src="/assets/images/logos/Journalism_Atlas_wordmark_horizontal_lockup_black.png" alt="Independent Journalism Atlas">',
        '      </a>',
        '      <div class="nav-search-container">',
        '        <input type="text" class="nav-search" placeholder="Search creators, topics, places..." id="navSearch" autocomplete="off">',
        '      </div>',
        '    </div>',
        '    <div class="nav-links">',
        '      <a href="/who-we-are.html" class="nav-link">Who We Are</a>',
        '      <a href="/about-this-project.html" class="nav-link">About This Project</a>',
        '      <a href="/how-we-did-this.html" class="nav-link">How We Did This</a>',
        '      <a href="/advisory.html" class="nav-link">Advisory Boards</a>',
        '      <a href="/submit.html" class="nav-link">Submit</a>',
        '      <a href="/research.html" class="nav-link">Our Research</a>',
        '    </div>',
        '    <button class="mobile-menu-button" id="mobileMenuButton" aria-label="Open menu">',
        '      <span class="material-symbols-outlined">menu</span>',
        '    </button>',
        '  </div>',
        '</nav>',
        '<div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>',
        '<div class="mobile-menu" id="mobileMenu">',
        '  <div class="mobile-menu-header">',
        '    <strong>Menu</strong>',
        '    <button class="mobile-menu-close" id="mobileMenuClose" aria-label="Close menu">',
        '      <span class="material-symbols-outlined">close</span>',
        '    </button>',
        '  </div>',
        '  <nav class="mobile-menu-links">',
        '    <a href="/who-we-are.html" class="mobile-menu-link">Who We Are</a>',
        '    <a href="/about-this-project.html" class="mobile-menu-link">About This Project</a>',
        '    <a href="/how-we-did-this.html" class="mobile-menu-link">How We Did This</a>',
        '    <a href="/advisory.html" class="mobile-menu-link">Advisory Boards</a>',
        '    <a href="/submit.html" class="mobile-menu-link">Submit</a>',
        '    <a href="/research.html" class="mobile-menu-link">Our Research</a>',
        '  </nav>',
        '</div>'
    ].join('\n');

    // Insert header as first content in <body>
    document.currentScript
        ? document.currentScript.insertAdjacentHTML('beforebegin', html)
        : document.body.insertAdjacentHTML('afterbegin', html);

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

        // On the home page main.js owns the search; skip navigation handler
        var path = window.location.pathname;
        var isHome = path === '/' || path === '/index.html' || path.endsWith('/index.html');
        if (isHome) return;

        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && this.value.trim()) {
                window.location.href = '/?search=' + encodeURIComponent(this.value.trim());
            }
        });
    }
}());
