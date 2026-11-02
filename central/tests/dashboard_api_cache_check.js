// Node check for dashboard/api-cache.js (run: node tests/dashboard_api_cache_check.js).
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert");
const mem = new Map();
const localStorage = {
  getItem: k => (mem.has(k) ? mem.get(k) : null), setItem: (k, v) => mem.set(k, String(v)),
  removeItem: k => mem.delete(k), key: i => Array.from(mem.keys())[i], get length() { return mem.size; },
};
let calls = 0, mode = "ok";
const realFetch = async url => {
  calls++;
  if (mode === "limited") return new Response("{}", { status: 403 });
  return new Response(JSON.stringify({ url, n: calls }), { status: 200 });
};
global.window = { fetch: realFetch, localStorage };
eval(fs.readFileSync(path.join(__dirname, "..", "dashboard", "api-cache.js"), "utf8"));
const f = window.fetch;
(async () => {
  const api = "https://api.github.com/repos/DayneK/Central/git/trees/main?recursive=1";
  const a = await (await f(api)).json();
  const b = await f(api);
  assert.strictEqual(calls, 1, "second API call should be served from cache");
  assert.strictEqual(b.headers.get("X-Central-Cache"), "fresh");
  assert.deepStrictEqual(await b.json(), a);
  await f("https://raw.githubusercontent.com/DayneK/Central/main/README.md");
  await f("https://raw.githubusercontent.com/DayneK/Central/main/README.md");
  assert.strictEqual(calls, 3, "raw content is not cached");
  // Expire the entry and simulate a rate-limit refusal: stale copy is served.
  const key = "central-api:v1:" + api, entry = JSON.parse(mem.get(key)); entry.at = 0; mem.set(key, JSON.stringify(entry));
  mode = "limited";
  const c = await f(api);
  assert.strictEqual(c.status, 200);
  assert.strictEqual(c.headers.get("X-Central-Cache"), "stale-limited");
  // Non-GET requests pass straight through.
  const before = calls; await f(api, { method: "POST" }); assert.strictEqual(calls, before + 1);
  console.log("api-cache checks passed");
})().catch(e => { console.error(e); process.exit(1); });
