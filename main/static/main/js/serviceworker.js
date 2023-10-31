var staticCacheName = "school-464-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/main/css/style.css',
    '/static/main/js/script.js',
    '/static/main/favicons/favicon.ico',
    '/static/main/img/pwa/icon-192x192.png',
    '/static/main/img/pwa/icon-256x256.png',
    '/static/main/img/pwa/icon-384x384.png',
    '/static/main/img/pwa/icon-512x512.png',
    '/static/main/img/pwa/splash-640x1136.png',
    '/static/main/img/pwa/splash-750x1334.png',
    '/static/main/img/pwa/splash-828x1792.png',
    '/static/main/img/pwa/splash-1125x2436.png',
    '/static/main/img/pwa/splash-1170x2532.png',
    '/static/main/img/pwa/splash-1179x2556.png',
    '/static/main/img/pwa/splash-1242x2208.png',
    '/static/main/img/pwa/splash-1242x2688.png',
    '/static/main/img/pwa/splash-1284x2778.png',
    '/static/main/img/pwa/splash-1290x2796.png',
    '/static/main/img/pwa/splash-1488x2266.png',
    '/static/main/img/pwa/splash-1536x2048.png',
    '/static/main/img/pwa/splash-1620x2160.png',
    '/static/main/img/pwa/splash-1640x2360.png',
    '/static/main/img/pwa/splash-1668x2224.png',
    '/static/main/img/pwa/splash-1668x2388.png',
    '/static/main/img/pwa/splash-2048x2732.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("school-464-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});