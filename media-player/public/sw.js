// Offline support for the phone app: keeps the app itself (page, icons, fonts) on the phone.
// Songs are not cached here — they live in the app's own song library (IndexedDB).
const CACHE = 'playlist-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];
const CDN = /^(fonts\.googleapis\.com|fonts\.gstatic\.com|unpkg\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)$/;

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('playlist-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Page: try the network first (so updates arrive), fall back to the saved copy when offline.
async function page(req) {
  const cache = await caches.open(CACHE);
  try {
    const res = await Promise.race([fetch(req), new Promise((_, rej) => setTimeout(() => rej(new Error('slow')), 4000))]);
    if (res && res.ok) cache.put('./index.html', res.clone());
    return res;
  } catch (_) {
    return (await cache.match('./index.html')) || (await cache.match('./')) || Response.error();
  }
}
// App files: answer from the saved copy at once, refresh it in the background.
async function fresh(req) {
  const cache = await caches.open(CACHE), hit = await cache.match(req);
  const net = fetch(req).then(res => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; }).catch(() => null);
  return hit || (await net) || Response.error();
}
// Fonts and libraries from CDNs never change at a given URL: keep the first copy.
async function keep(req) {
  const cache = await caches.open(CACHE), hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone());
  return res;
}

self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || req.headers.has('range')) return;
  if (url.origin === self.location.origin) {
    if (/\/(api|stream)\//.test(url.pathname)) return;          // live data from a laptop server
    e.respondWith(req.mode === 'navigate' ? page(req) : fresh(req));
  } else if (CDN.test(url.hostname)) {
    e.respondWith(keep(req));
  }                                                              // anything else (e.g. the laptop link): straight to the network
});
