self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open('cartracker-static-v5');
    await cache.addAll([
      '/',
      '/static/autoprudente-favicon.png?v=2',
      '/static/manifest.webmanifest'
    ]);
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => !k.startsWith('cartracker-static-v5')).map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // Cache-first for static assets
  if (url.pathname.startsWith('/static/')) {
    event.respondWith((async () => {
      const cache = await caches.open('cartracker-static-v5');
      const cached = await cache.match(event.request);
      if (cached) return cached;
      const resp = await fetch(event.request);
      cache.put(event.request, resp.clone());
      return resp;
    })());
    return;
  }
  // Network-first for HTML pages to avoid stale content in PWA
  if (event.request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const resp = await fetch(event.request, { cache: 'no-store' });
        return resp;
      } catch (e) {
        const cache = await caches.open('cartracker-static-v5');
        const cached = await cache.match('/');
        return cached || new Response('Offline', { status: 503 });
      }
    })());
    return;
  }
  // Network-first for API calls
  if (url.pathname.startsWith('/api/')) {
    event.respondWith((async () => {
      try {
        const resp = await fetch(event.request);
        return resp;
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: 'offline' }), { status: 503, headers: { 'Content-Type': 'application/json' } });
      }
    })());
    return;
  }
});
