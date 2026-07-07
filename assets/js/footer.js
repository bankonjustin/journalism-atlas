/* =====================================================
   SHARED SITE FOOTER COMPONENT
   Appended to end of <body> on every page.
   CSS: assets/css/header.css (last stylesheet in <head>)
   ===================================================== */

(function () {
    var email = ['hell', 'o', '@journalism', 'atlas.com'].join('');

    var html = [
        '<footer class="site-footer">',
        '  <div class="footer-inner">',
        '    <div class="footer-top">',
        '      <div class="footer-brand">',
        '        <img src="/assets/images/logos/Journalism_Atlas_wordmark_stacked_white.png" alt="Independent Journalism Atlas" class="footer-wordmark">',
        '        <p class="footer-tagline">Independent journalism is moving. We\'re following it.</p>',
        '      </div>',
        '      <div class="footer-col">',
        '        <div class="footer-col-title">Explore</div>',
        '        <ul>',
        '          <li><a href="/search">The Atlas Database</a></li>',
        '          <li><a href="/lists">Collections</a></li>',
        '          <li><a href="/pulse">Atlas Pulse</a></li>',
        '          <!-- <li><a href="/beat-clusters">Beat Clusters</a></li> -->',
        '          <!-- <li><a href="/city-labs">City Labs</a></li> -->',
        '        </ul>',
        '      </div>',
        '      <div class="footer-col">',
        '        <div class="footer-col-title">About</div>',
        '        <ul>',
        '          <li><a href="/about-this-project">About This Project</a></li>',
        '          <li><a href="/how-we-did-this">How We Did This</a></li>',
        '          <li><a href="/research">Research &amp; Writing</a></li>',
        '          <li><a href="/advisory">Advisory Boards</a></li>',
        '        </ul>',
        '      </div>',
        '      <div class="footer-col">',
        '        <div class="footer-col-title">Connect</div>',
        '        <ul>',
        '          <li><a href="mailto:' + email + '">Email Us</a></li>',
        '          <li><a href="/submit">Submit a Creator</a></li>',
        '          <li><a href="/for-brands">Work With Us</a></li>',
        '        </ul>',
        '      </div>',
        '    </div>',
        '    <div class="footer-bottom">',
        '      <span class="footer-copy">© 2026 Independent Journalism Atlas</span>',
        '      <div class="footer-legal">',
        '        <a href="/privacy">Privacy</a>',
        '        <a href="/terms">Terms</a>',
        '      </div>',
        '    </div>',
        '  </div>',
        '</footer>'
    ].join('\n');

    document.body.insertAdjacentHTML('beforeend', html);
}());
