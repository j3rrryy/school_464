const now = new Date();
const staticCacheName = `school-464-v${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}`;
const filesToCache = [
  "/offline/",
  "/static/main/css/style.37d0bdce.css",
  "/static/main/js/script.359f958d.js",
  "/static/main/favicons/favicon.ico",
  "/static/main/img/logo.svg",
  "/static/main/img/pwa/icon-192x192.png",
  "/static/main/img/pwa/icon-256x256.png",
  "/static/main/img/pwa/icon-384x384.png",
  "/static/main/img/pwa/icon-512x512.png",
  "/static/main/img/pwa/splash-640x1136.png",
  "/static/main/img/pwa/splash-750x1334.png",
  "/static/main/img/pwa/splash-828x1792.png",
  "/static/main/img/pwa/splash-1125x2436.png",
  "/static/main/img/pwa/splash-1170x2532.png",
  "/static/main/img/pwa/splash-1179x2556.png",
  "/static/main/img/pwa/splash-1242x2208.png",
  "/static/main/img/pwa/splash-1242x2688.png",
  "/static/main/img/pwa/splash-1284x2778.png",
  "/static/main/img/pwa/splash-1290x2796.png",
  "/static/main/img/pwa/splash-1488x2266.png",
  "/static/main/img/pwa/splash-1536x2048.png",
  "/static/main/img/pwa/splash-1620x2160.png",
  "/static/main/img/pwa/splash-1640x2360.png",
  "/static/main/img/pwa/splash-1668x2224.png",
  "/static/main/img/pwa/splash-1668x2388.png",
  "/static/main/img/pwa/splash-2048x2732.png",
];

// ======================

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => cache.addAll(filesToCache)),
  );
});

// ======================

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter(
              (key) => key.startsWith("school-464-") && key !== staticCacheName,
            )
            .map((key) => caches.delete(key)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

// ======================

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (
    url.pathname.startsWith("/admin/") ||
    url.pathname.startsWith("/ckeditor5/") ||
    url.pathname.endsWith("service-worker.js") ||
    url.pathname.endsWith("manifest.json") ||
    url.pathname.startsWith("/static/admin/") ||
    url.pathname.startsWith("/static/ckeditor5/")
  )
    return;

  if (req.mode === "navigate") {
    event.respondWith(fetch(req).catch(() => caches.match("/offline/")));
    return;
  }

  event.respondWith(
    caches
      .match(req)
      .then((r) => r || fetch(req).catch(() => Response.error())),
  );
});
