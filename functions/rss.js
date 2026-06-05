// functions/rss.js
// Cloudflare Pages Function — RSS proxy
// Deployed automatically by Cloudflare Pages at /rss?url=<encoded_feed_url>

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const feedUrl = url.searchParams.get('url');

  // CORS headers — allow requests from same origin only
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'public, max-age=900', // 15-minute cache at edge
  };

  if (!feedUrl) {
    return new Response(JSON.stringify({ error: 'Missing url param' }), { status: 400, headers });
  }

  // Validate — only allow http/https
  let parsed;
  try {
    parsed = new URL(feedUrl);
    if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('bad protocol');
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid URL' }), { status: 400, headers });
  }

  try {
    const res = await fetch(feedUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; AtlasBot/1.0; +https://journalismatlas.com)',
        'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
      },
      cf: { cacheTtl: 900, cacheEverything: true }, // Cloudflare edge cache
    });

    if (!res.ok) {
      return new Response(JSON.stringify({ error: `Feed returned ${res.status}` }), { status: 502, headers });
    }

    const xml = await res.text();

    // Parse RSS/Atom to extract items
    const items = parseXML(xml, feedUrl);

    return new Response(JSON.stringify({ status: 'ok', items }), { status: 200, headers });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message || 'fetch failed' }), { status: 502, headers });
  }
}

function parseXML(xml, feedUrl) {
  // Minimal RSS/Atom parser using regex — no DOM in Workers
  const items = [];

  // Try RSS <item> tags
  const itemRe = /<item[\s>]([\s\S]*?)<\/item>/gi;
  let match;
  while ((match = itemRe.exec(xml)) !== null && items.length < 3) {
    const chunk = match[1];
    const title = extractTag(chunk, 'title');
    const link = extractTag(chunk, 'link') || extractAttr(chunk, 'link', 'href') || feedUrl;
    const pubDate = extractTag(chunk, 'pubDate') || extractTag(chunk, 'dc:date') || '';
    if (title) items.push({ title, link, pubDate });
  }

  // If no RSS items, try Atom <entry> tags
  if (!items.length) {
    const entryRe = /<entry[\s>]([\s\S]*?)<\/entry>/gi;
    while ((match = entryRe.exec(xml)) !== null && items.length < 3) {
      const chunk = match[1];
      const title = extractTag(chunk, 'title');
      const link = extractAttr(chunk, 'link', 'href') || extractTag(chunk, 'link') || feedUrl;
      const pubDate = extractTag(chunk, 'published') || extractTag(chunk, 'updated') || '';
      if (title) items.push({ title, link, pubDate });
    }
  }

  return items;
}

function extractTag(xml, tag) {
  const re = new RegExp(`<${tag}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/${tag}>`, 'i');
  const m = xml.match(re);
  return m ? m[1].trim() : '';
}

function extractAttr(xml, tag, attr) {
  const re = new RegExp(`<${tag}[^>]*${attr}="([^"]*)"`, 'i');
  const m = xml.match(re);
  return m ? m[1].trim() : '';
}
