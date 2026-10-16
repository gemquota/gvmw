// Small dependency-free layered DAG renderer (SVG, left -> right).
import { h, s } from "./dom.js";

export function dag({ nodes, edges, highlight = [], focus, onClick, nodeW = 190, nodeH = 46, gapX = 70, gapY = 16, fit = false }) {
  const ids = new Set(nodes.map((n) => n.id));
  const E = edges.filter((e) => ids.has(e.from) && ids.has(e.to));
  const preds = new Map(nodes.map((n) => [n.id, []]));
  for (const e of E) preds.get(e.to).push(e.from);
  const layer = new Map();
  const depth = (id, seen = new Set()) => {
    if (layer.has(id)) return layer.get(id);
    if (seen.has(id)) return 0;
    seen.add(id);
    const ps = preds.get(id);
    const d = ps.length ? 1 + Math.max(...ps.map((p) => depth(p, seen))) : 0;
    layer.set(id, d);
    return d;
  };
  nodes.forEach((n) => depth(n.id));
  const layers = [];
  for (const n of nodes) (layers[layer.get(n.id)] ||= []).push(n);
  // one barycentre pass for fewer crossings
  const pos = new Map();
  layers.forEach((L, i) => {
    if (i > 0) L.sort((a, b) => bary(a) - bary(b));
    L.forEach((n, j) => pos.set(n.id, j));
  });
  function bary(n) { const ps = preds.get(n.id); return ps.length ? ps.reduce((t, p) => t + (pos.get(p) ?? 0), 0) / ps.length : 0; }
  const maxRows = Math.max(1, ...layers.map((L) => L.length));
  const W = layers.length * (nodeW + gapX) - gapX + 40, H = maxRows * (nodeH + gapY) - gapY + 40;
  const xy = new Map();
  layers.forEach((L, i) => {
    const off = ((maxRows - L.length) * (nodeH + gapY)) / 2;
    L.forEach((n, j) => xy.set(n.id, { x: 20 + i * (nodeW + gapX), y: 20 + off + j * (nodeH + gapY) }));
  });
  const hl = new Set(highlight.map((e) => e.from + ">" + e.to));
  const svg = s("svg", { width: fit ? "100%" : W, height: fit ? null : H, viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: "xMinYMin meet", style: fit ? `min-width:${Math.round(W * 0.6)}px` : null, role: "img", "aria-label": "graph" },
    s("defs", null,
      s("marker", { id: "arrow", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, s("path", { d: "M0,0 L10,5 L0,10 z" })),
      s("marker", { id: "arrow-bad", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, s("path", { d: "M0,0 L10,5 L0,10 z" }))));
  for (const e of E) {
    const a = xy.get(e.from), b = xy.get(e.to);
    const x1 = a.x + nodeW, y1 = a.y + nodeH / 2, x2 = b.x - 2, y2 = b.y + nodeH / 2, mx = (x1 + x2) / 2;
    const isHl = hl.has(e.from + ">" + e.to) || e.prop;
    svg.appendChild(s("path", { class: "edge" + (isHl ? " prop" : ""), d: `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`, "marker-end": isHl ? "url(#arrow-bad)" : "url(#arrow)" }));
  }
  for (const n of nodes) {
    const { x, y } = xy.get(n.id);
    const g = s("g", { class: `node s-${n.status || "ok"} t-${n.type || "p"}${n.id === focus ? " focus" : ""}${onClick ? " click" : ""}`, transform: `translate(${x},${y})`, tabindex: onClick ? 0 : null, role: onClick ? "button" : null },
      s("title", { text: (n.title || n.id) + (n.status ? " — " + n.status : "") }),
      s("rect", { width: nodeW, height: nodeH, rx: 10 }),
      s("text", { x: 10, y: 19, text: clip(n.label || n.id, 26) }),
      s("text", { x: 10, y: 35, class: "sub", text: clip(n.sub || n.id, 30) }));
    if (onClick) {
      g.addEventListener("click", () => onClick(n));
      g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); onClick(n); } });
    }
    svg.appendChild(g);
  }
  return h("div", { class: "graph" }, svg);
}
function clip(t, n) { t = String(t); return t.length > n ? t.slice(0, n - 1) + "…" : t; }
