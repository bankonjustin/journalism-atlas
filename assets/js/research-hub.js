/* Research hub and piece-page modules. Vanilla JS, reads data/research.json and data/social.json.
   Floors rule: a module renders only when it has real material. Nothing here invents content.
   Mounts (all optional, found by attribute):
     [data-research-hub]                        the whole hub (hub page)
     [data-research-talked][data-piece="slug"]  "Talked about on" (piece pages)
     [data-research-cta="primary"][data-piece]  endcap button, rewritten from the record's cta_primary
   Bluesky: public AppView, read-only, no auth. Any failure renders nothing. */
(function () {
  'use strict';

  var PLATFORMS = { bluesky: 'Bluesky', instagram: 'Instagram', tiktok: 'TikTok', linkedin: 'LinkedIn', threads: 'Threads', youtube: 'YouTube' };
  var ACCOUNTS = { atlas: 'Independent Journalism Atlas' };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var APPVIEW = 'https://public.api.bsky.app/xrpc/';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function safeUrl(u) {
    if (!u) return '';
    if (u.charAt(0) === '/' && u.charAt(1) !== '/') return u;
    return /^https:\/\//i.test(u) ? u : '';
  }
  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})(?:-(\d{2}))?/.exec(d || '');
    if (!m) return '';
    var mon = MONTHS[+m[2] - 1];
    return m[3] ? mon + ' ' + (+m[3]) + ', ' + m[1] : mon + ' ' + m[1];
  }
  function weekday(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(d || '');
    if (!m) return '';
    return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date(Date.UTC(+m[1], +m[2] - 1, +m[3])).getUTCDay()];
  }
  function getJSON(url) {
    return fetch(url, { credentials: 'omit' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }
  function ctaHref(research, id, slug) {
    var c = research.ctas && research.ctas[id];
    if (!c || !c.label || !c.to) return null;
    return { label: c.label, href: c.to + '?source=' + encodeURIComponent(slug) + '&cta=' + encodeURIComponent(id) };
  }
  function ctaLink(research, id, slug, cls) {
    var c = ctaHref(research, id, slug);
    if (!c) return null;
    var a = el('a', cls, c.label + ' →');
    a.href = c.href;
    return a;
  }

  /* ---- Bluesky (live, read-only) ---- */
  function bskyWeb(uri, handle) {
    var m = /^at:\/\/([^/]+)\/app\.bsky\.feed\.post\/([^/]+)$/.exec(uri || '');
    return m ? 'https://bsky.app/profile/' + (handle || m[1]) + '/post/' + m[2] : '';
  }
  function postLinks(rec, domain) {
    var out = [];
    ((rec && rec.facets) || []).forEach(function (f) {
      (f.features || []).forEach(function (ft) { if (ft.uri) out.push(ft.uri); });
    });
    var ext = rec && rec.embed && rec.embed.external;
    if (ext && ext.uri) out.push(ext.uri);
    return out.filter(function (u) { return u.indexOf(domain) !== -1; });
  }
  function bskyCard(p, domain, pieces, accountKey) {
    var rec = p.record || {};
    var links = postLinks(rec, domain);
    var url = bskyWeb(p.uri, p.author && p.author.handle);
    if (!url) return null;
    var slug = '';
    pieces.forEach(function (pc) {
      var path = (pc.url || '').replace(/^https?:\/\/[^/]+/, '').replace(/\/$/, '');
      if (!slug && path.length > 1 && links.some(function (l) { return l.indexOf(domain + path) !== -1; })) slug = pc.slug;
    });
    var img = p.embed && p.embed.images && p.embed.images[0];
    return {
      id: 'bsky:' + p.uri, platform: 'bluesky', account: accountKey || (p.author && p.author.handle) || '', url: url, piece_slug: slug,
      poster_image: img ? img.thumb : '', alt: img ? (img.alt || '') : '', caption: rec.text || '', date: rec.createdAt || p.indexedAt || '', _links: links
    };
  }
  function fetchWithTimeout(url, ms) {
    var ctl = typeof AbortController === 'function' ? new AbortController() : null;
    var t = ctl ? setTimeout(function () { ctl.abort(); }, ms) : null;
    return fetch(url, { credentials: 'omit', signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { if (t) clearTimeout(t); return j; }, function (e) { if (t) clearTimeout(t); throw e; });
  }
  function loadBluesky(cfg, pieces) {
    var out = [];
    if (!cfg) return Promise.resolve(out);
    var domain = cfg.match_domain || 'journalismatlas.com';
    var jobs = [];
    (cfg.accounts || []).forEach(function (a) {
      var h = (a.handle || '').trim();
      if (!h || h.toUpperCase() === 'TBD') return;
      var q = 'getAuthorFeed?actor=' + encodeURIComponent(h) + '&filter=posts_no_replies&limit=' + (cfg.limit || 50);
      jobs.push(fetchWithTimeout(APPVIEW + 'app.bsky.feed.' + q, 6000).then(function (j) {
        (j.feed || []).forEach(function (f) {
          if (f.reason) return; // reposts
          var c = bskyCard(f.post, domain, pieces, a.account);
          if (c && c._links.length) out.push(c);
        });
      }).catch(function () { /* this account yields nothing */ }));
    });
    var pins = (cfg.pinned_uris || []).filter(Boolean);
    for (var i = 0; i < pins.length; i += 25) {
      var qs = pins.slice(i, i + 25).map(function (u) { return 'uris=' + encodeURIComponent(u); }).join('&');
      jobs.push(fetchWithTimeout(APPVIEW + 'app.bsky.feed.getPosts?' + qs, 6000).then(function (j) {
        (j.posts || []).forEach(function (p) { var c = bskyCard(p, domain, pieces, ''); if (c) out.push(c); });
      }).catch(function () {}));
    }
    return Promise.all(jobs).then(function () { return out; });
  }

  /* ---- Post cards (same component for hub flow and piece pages) ---- */
  function postCard(p) {
    var url = safeUrl(p.url);
    if (!url) return null;
    var name = PLATFORMS[p.platform] || '';
    if (!name) return null;
    var card = el('article', 'rh-card');
    var imgSrc = safeUrl(p.poster_image);
    if (imgSrc) {
      var img = el('img', 'rh-post-img');
      img.src = imgSrc; img.alt = p.alt || ''; img.loading = 'lazy'; img.decoding = 'async';
      card.appendChild(img);
    }
    var acct = ACCOUNTS[p.account] || p.account || '';
    card.appendChild(el('p', 'rh-meta', [name, acct, fmtDate(p.date)].filter(Boolean).join(' · ')));
    var cap = p.caption_short || p.caption || '';
    if (cap) card.appendChild(el('p', 'rh-post-cap', cap));
    var a = el('a', 'link-instruction', 'View on ' + name + ' →');
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
    card.appendChild(a);
    return card;
  }
  function byDateDesc(a, b) { return (b.date || '').localeCompare(a.date || ''); }
  function allPosts(social, pieces) {
    var staticPosts = (social && social.posts) || [];
    return loadBluesky(social && social.bluesky, pieces).then(function (live) {
      var seen = {};
      return staticPosts.concat(live).filter(function (p) {
        var k = p.url; if (!k || seen[k]) return false; seen[k] = 1; return true;
      }).sort(byDateDesc);
    });
  }

  /* ---- Sections ---- */
  function section(cls, eyebrow, heading) {
    var s = el('section', 'rh-sec ' + cls);
    var inn = el('div', 'rh-in');
    if (eyebrow) inn.appendChild(el('p', 'rh-eyebrow', eyebrow));
    if (heading) inn.appendChild(el('h2', 'rh-h2', heading));
    s.appendChild(inn);
    return { sec: s, inn: inn };
  }
  function pieceMeta(research, p) {
    var type = (research.types && research.types[p.type]) || '';
    var when = p.status === 'placeholder' ? (p.date ? 'Coming ' + [weekday(p.date), fmtDate(p.date)].filter(Boolean).join(', ') : 'Coming soon') : fmtDate(p.date);
    return [type, when].filter(Boolean).join(' · ');
  }
  function pieceLink(p, cls) {
    var url = safeUrl(p.url);
    if (p.status !== 'live' || !url || !p.link_label) return null;
    var a = el('a', cls, p.link_label + ' →');
    a.href = url;
    if (p.external) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    return a;
  }
  function featured(research, p) {
    var s = section('on-dark', 'Featured research', '');
    var img = safeUrl(p.hero_image && p.hero_image.src);
    var wrap = el('div', 'rh-feat' + (img ? ' rh-feat--img' : ''));
    if (img) {
      var i = el('img', 'rh-feat-img');
      i.src = img; i.alt = p.hero_image.alt || ''; i.decoding = 'async';
      wrap.appendChild(i);
    }
    var txt = el('div');
    txt.appendChild(el('p', 'rh-meta', pieceMeta(research, p)));
    txt.appendChild(el('h2', 'rh-feat-t', p.title));
    if (p.dek) txt.appendChild(el('p', 'rh-feat-b', p.dek));
    var act = el('div', 'rh-feat-act');
    var read = pieceLink(p, 'btn btn--primary');
    if (read) act.appendChild(read);
    var cta = p.cta_primary && ctaLink(research, p.cta_primary, p.slug, 'link-instruction');
    if (cta) act.appendChild(cta);
    txt.appendChild(act);
    wrap.appendChild(txt);
    s.inn.appendChild(wrap);
    return s;
  }
  function cards(research, list) {
    var grid = el('div', 'rh-grid');
    list.forEach(function (p) {
      var c = el('article', 'rh-card');
      c.appendChild(el('p', 'rh-meta', pieceMeta(research, p)));
      c.appendChild(el('h3', 'rh-card-t', p.title));
      if (p.dek) c.appendChild(el('p', 'rh-card-b', p.dek));
      var l = pieceLink(p, 'link-instruction');
      if (l) c.appendChild(l);
      grid.appendChild(c);
    });
    return grid;
  }
  function partnersBand(research, pieces) {
    var seen = {}, list = [];
    pieces.forEach(function (p) {
      (p.partners || []).forEach(function (pt) {
        if (!pt.name || seen[pt.name]) return;
        seen[pt.name] = 1; list.push(pt);
      });
    });
    if (list.length < 2) return null; // floor
    var s = section('', 'Partners and collaborators', '');
    var ul = el('ul', 'rh-partners');
    list.forEach(function (pt) {
      var li = el('li', 'rh-partner');
      var logo = safeUrl(pt.logo);
      if (logo) { var im = el('img', 'rh-partner-logo'); im.src = logo; im.alt = ''; im.loading = 'lazy'; li.appendChild(im); }
      var n = el('span', 'rh-partner-n');
      var url = safeUrl(pt.url);
      if (url) { var a = el('a', null, pt.name); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; n.appendChild(a); } else { n.textContent = pt.name; }
      li.appendChild(n);
      if (pt.role) li.appendChild(el('p', 'rh-partner-r', pt.role));
      ul.appendChild(li);
    });
    s.inn.appendChild(ul);
    var ask = ctaLink(research, 'partner-inquiry', 'research-hub', 'btn btn--primary');
    if (ask) s.inn.appendChild(ask);
    return s;
  }
  function signupBand(research) {
    var b = ctaLink(research, 'updates-signup', 'research-hub', 'btn btn--primary');
    if (!b) return null;
    var s = section('on-dark', 'Atlas updates', '');
    s.inn.appendChild(b);
    s.inn.appendChild(el('p', 'rh-cta-note', 'No spam. Unsubscribe any time.'));
    return s;
  }

  function renderHub(mount, research, social) {
    var pieces = (research.pieces || []).filter(function (p) { return p && p.slug && p.title; });
    var feat = pieces.filter(function (p) { return p.featured && p.status === 'live'; })[0];
    var rest = pieces.filter(function (p) { return p !== feat; }).sort(byDateDesc);
    var frag = document.createDocumentFragment();
    if (feat) frag.appendChild(featured(research, feat).sec);
    if (rest.length) {
      var s = section('on-dark', 'All research', '');
      s.inn.appendChild(cards(research, rest));
      frag.appendChild(s.sec);
    }
    var pb = partnersBand(research, pieces);
    var sb = signupBand(research);
    mount.textContent = '';
    mount.appendChild(frag);
    var feedMount = el('div');
    mount.appendChild(feedMount);
    if (pb) mount.appendChild(pb.sec);
    if (sb) mount.appendChild(sb.sec);
    allPosts(social, pieces).then(function (posts) {
      var cs = posts.map(postCard).filter(Boolean).slice(0, 12);
      if (!cs.length) return; // empty pool: the slot is skipped
      var f = section('', 'From our feeds', '');
      var grid = el('div', 'rh-grid rh-grid--3');
      cs.forEach(function (c) { grid.appendChild(c); });
      f.inn.appendChild(grid);
      feedMount.appendChild(f.sec);
    });
  }

  function renderPiece(research, social) {
    var pieces = research.pieces || [];
    function rec(slug) { return pieces.filter(function (p) { return p.slug === slug; })[0]; }
    var cta = document.querySelector('[data-research-cta="primary"]');
    if (cta) {
      var p = rec(cta.getAttribute('data-piece'));
      var c = p && p.cta_primary && ctaHref(research, p.cta_primary, p.slug);
      if (c) { cta.href = c.href; cta.textContent = c.label + ' →'; }
    }
    var tm = document.querySelector('[data-research-talked]');
    if (!tm) return;
    var slug = tm.getAttribute('data-piece');
    allPosts(social, pieces).then(function (posts) {
      var cs = posts.filter(function (p) { return p.piece_slug === slug; }).map(postCard).filter(Boolean);
      if (!cs.length) return; // floor: nothing until there are posts
      var inn = el('div', 'rh-in');
      inn.appendChild(el('h2', 'rh-h2', 'Talked about on'));
      var grid = el('div', 'rh-grid rh-grid--3');
      cs.forEach(function (c) { grid.appendChild(c); });
      inn.appendChild(grid);
      tm.textContent = '';
      tm.className = 'rh-talked';
      tm.appendChild(inn);
      tm.hidden = false;
    });
  }

  function init() {
    var hub = document.querySelector('[data-research-hub]');
    var piece = document.querySelector('[data-research-talked],[data-research-cta]');
    if (!hub && !piece) return;
    Promise.all([getJSON('/data/research.json'), getJSON('/data/social.json').catch(function () { return { posts: [] }; })])
      .then(function (r) { if (hub) renderHub(hub, r[0], r[1]); else renderPiece(r[0], r[1]); })
      .catch(function () { /* hub keeps its static fallback; piece pages keep their static endcap */ });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
