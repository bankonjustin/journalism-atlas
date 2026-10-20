// Password gate for the unpublished Watershed preview.
// Only /watershed and /watershed/* are gated; everything else passes straight through.
// HTTP Basic auth: username ignored, password checked against env.WATERSHED_PASSWORD.
// Fails closed: if WATERSHED_PASSWORD is unset or empty, /watershed always returns 401.

const NOINDEX = 'noindex, nofollow';

function isGated(pathname) {
  return pathname === '/watershed' || pathname.startsWith('/watershed/');
}

function deny() {
  return new Response('Authentication required.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Watershed preview", charset="UTF-8"',
      'X-Robots-Tag': NOINDEX,
      'Cache-Control': 'no-store',
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}

// Compare SHA-256 digests byte by byte without early exit.
async function safeEqual(a, b) {
  const enc = new TextEncoder();
  const [da, db] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(a)),
    crypto.subtle.digest('SHA-256', enc.encode(b)),
  ]);
  const x = new Uint8Array(da);
  const y = new Uint8Array(db);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function passwordFrom(request) {
  const header = request.headers.get('Authorization') || '';
  const match = header.match(/^Basic\s+(.+)$/i);
  if (!match) return null;
  let decoded;
  try {
    decoded = atob(match[1]);
  } catch (e) {
    return null;
  }
  const i = decoded.indexOf(':');
  return i === -1 ? null : decoded.slice(i + 1);
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const { pathname } = new URL(request.url);
  if (!isGated(pathname)) return next();

  const expected = env.WATERSHED_PASSWORD;
  if (typeof expected !== 'string' || expected === '') return deny();

  const supplied = passwordFrom(request);
  if (supplied === null || !(await safeEqual(supplied, expected))) return deny();

  const response = await next();
  const out = new Response(response.body, response);
  out.headers.set('X-Robots-Tag', NOINDEX);
  out.headers.set('Cache-Control', 'private, no-store');
  return out;
}
