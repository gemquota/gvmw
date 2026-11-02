/* Central dashboard: GitHub API cache.
 * Unauthenticated GitHub REST calls are limited to 60 per hour per IP address.
 * This wraps window.fetch for GET requests to api.github.com only:
 *  - fresh responses (younger than TTL_MS) are served from localStorage;
 *  - if the API refuses (403/429) or the network fails, a stale copy is served;
 *  - once BUDGET calls have been made in the current hour, stale copies are preferred.
 * raw.githubusercontent.com is not part of the API limit and is not cached here.
 * Nothing secret is stored: only public API JSON. Clear with CentralApiCache.clear().
 */
(function () {
  "use strict";
  var PREFIX = "central-api:v1:", BUDGET_KEY = "central-api:v1:budget";
  var TTL_MS = 15 * 60 * 1000, HOUR_MS = 60 * 60 * 1000, BUDGET = 45;
  var realFetch = window.fetch.bind(window);
  var store = null;
  try { store = window.localStorage; store.setItem(PREFIX + "probe", "1"); store.removeItem(PREFIX + "probe"); } catch (e) { store = null; }

  function urlOf(input) { return typeof input === "string" ? input : (input && input.url) || String(input); }
  function isApiGet(input, init) {
    var method = (init && init.method) || (input && typeof input === "object" && input.method) || "GET";
    return String(method).toUpperCase() === "GET" && /^https:\/\/api\.github\.com\//.test(urlOf(input));
  }
  function read(key) { try { return JSON.parse(store.getItem(key)); } catch (e) { return null; } }
  function write(key, value) {
    try { store.setItem(key, JSON.stringify(value)); }
    catch (e) { clear(); try { store.setItem(key, JSON.stringify(value)); } catch (e2) { /* quota: give up quietly */ } }
  }
  function clear() {
    if (!store) return;
    for (var i = store.length - 1; i >= 0; i--) { var k = store.key(i); if (k && k.indexOf(PREFIX) === 0) store.removeItem(k); }
  }
  function budget() {
    var b = read(BUDGET_KEY), now = Date.now();
    if (!b || now - b.start > HOUR_MS) b = { start: now, used: 0 };
    return b;
  }
  function respond(entry, state) {
    return new Response(entry.body, { status: 200, headers: { "Content-Type": "application/json", "X-Central-Cache": state } });
  }

  window.fetch = function (input, init) {
    if (!store || !isApiGet(input, init)) return realFetch(input, init);
    var key = PREFIX + urlOf(input), cached = read(key), now = Date.now(), b = budget();
    if (cached && now - cached.at < TTL_MS) return Promise.resolve(respond(cached, "fresh"));
    if (cached && b.used >= BUDGET) return Promise.resolve(respond(cached, "stale-budget"));
    b.used += 1; write(BUDGET_KEY, b);
    return realFetch(input, init).then(function (r) {
      if (r.ok) {
        return r.clone().text().then(function (body) { write(key, { at: Date.now(), body: body }); return r; });
      }
      if (cached && (r.status === 403 || r.status === 429)) return respond(cached, "stale-limited");
      return r;
    }, function (err) {
      if (cached) return respond(cached, "stale-offline");
      throw err;
    });
  };
  window.CentralApiCache = { clear: clear, ttlMs: TTL_MS, budget: function () { return budget(); } };
})();
