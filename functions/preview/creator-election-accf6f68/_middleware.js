// Password gate for /preview/creator-election-accf6f68/* (Cloudflare Pages Function, runs before the static files).
// The password is NOT in the repo: set PREVIEW_PASSWORD under Pages > Settings > Variables and Secrets (Production and Preview).
// If it is unset the gate stays closed (503). Any username works; only the password is checked.
const enc = new TextEncoder();

async function same(a, b) {
  // compare SHA-256 digests byte by byte, without early exit
  const [x, y] = await Promise.all([crypto.subtle.digest('SHA-256', enc.encode(a)), crypto.subtle.digest('SHA-256', enc.encode(b))]);
  const u = new Uint8Array(x), v = new Uint8Array(y);
  let d = 0;
  for (let i = 0; i < u.length; i++) d |= u[i] ^ v[i];
  return d === 0;
}

function deny(status, body, extra) {
  return new Response(body, { status, headers: Object.assign({ 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' }, extra || {}) });
}

export async function onRequest(context) {
  const secret = context.env && context.env.PREVIEW_PASSWORD;
  if (!secret) return deny(503, 'This preview is closed.');
  const h = context.request.headers.get('Authorization') || '';
  if (h.startsWith('Basic ')) {
    let pass = '';
    try {
      const raw = atob(h.slice(6));
      pass = raw.slice(raw.indexOf(':') + 1);
    } catch (e) { pass = ''; }
    if (await same(pass, secret)) {
      const res = await context.next();
      const out = new Response(res.body, res);
      out.headers.set('Cache-Control', 'private, no-store');
      out.headers.set('X-Robots-Tag', 'noindex, nofollow');
      return out;
    }
  }
  return deny(401, 'Password required.', { 'WWW-Authenticate': 'Basic realm="Atlas preview", charset="UTF-8"' });
}
