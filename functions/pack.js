// functions/pack.js
// Runs at the edge on every request to /pack

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Only intercept if this looks like a shared pack link
  const creatorsParam = url.searchParams.get('creators');
  const nameParam = url.searchParams.get('name');
  const fromParam = url.searchParams.get('from');

  // Fetch the real pack.html from the static asset
  const response = await env.ASSETS.fetch(request);

  // If no creators in URL, just pass through with basic static OG tags injected
  const html = await response.text();

  // Build dynamic values
  let ogTitle = 'Make a Starter Pack — Independent Journalism Atlas';
  let ogDescription = 'Curate your favourite independent journalists and share them as a postcard. 1,000+ creators across newsletters, podcasts, video, and more.';

  if (creatorsParam) {
    const names = creatorsParam
      .split(',')
      .map(n => decodeURIComponent(n).trim())
      .filter(Boolean);

    const packName = nameParam
      ? decodeURIComponent(nameParam)
      : 'An Atlas Pack';

    const from = fromParam
      ? decodeURIComponent(fromParam)
      : null;

    // e.g. "Sarah's Pack — 6 independent journalists to follow"
    ogTitle = from
      ? `${from} shared "${packName}" — Independent Journalism Atlas`
      : `"${packName}" — Independent Journalism Atlas`;

    // List up to 5 creator names inline, truncate the rest
    const preview = names.slice(0, 5).join(', ');
    const overflow = names.length > 5 ? ` + ${names.length - 5} more` : '';
    ogDescription = `${packName}: ${preview}${overflow}. Discover independent journalists on the Atlas.`;
  }

  const ogUrl = url.toString();
  const ogImage = 'https://journalismatlas.com/assets/images/og-pack-default.png'; // static fallback image

  // Inject OG tags into <head>
  const ogTags = `
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Independent Journalism Atlas" />
    <meta property="og:url" content="${escapeHtml(ogUrl)}" />
    <meta property="og:title" content="${escapeHtml(ogTitle)}" />
    <meta property="og:description" content="${escapeHtml(ogDescription)}" />
    <meta property="og:image" content="${ogImage}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${escapeHtml(ogTitle)}" />
    <meta name="twitter:description" content="${escapeHtml(ogDescription)}" />
    <meta name="twitter:image" content="${ogImage}" />
  `;

  // Also update the <title> tag
  const modifiedHtml = html
    .replace('</head>', `${ogTags}\n</head>`)
    .replace(
      '<title>Make a Starter Pack — Independent Journalism Atlas</title>',
      `<title>${escapeHtml(ogTitle)}</title>`
    );

  return new Response(modifiedHtml, {
    headers: {
      'content-type': 'text/html;charset=UTF-8',
      // Don't cache personalised pack URLs at the edge
      'cache-control': creatorsParam
        ? 'no-store'
        : 'public, max-age=3600',
    },
  });
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
