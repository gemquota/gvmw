#!/usr/bin/env python3
"""Minimal stdlib Markdown -> standalone HTML renderer for MedB docs.

Supports the subset used in docs/: ATX headings, paragraphs, nested bullet and
numbered lists (2-space indents), pipe tables, fenced code, blockquotes, hr,
**bold**, *italic*, `code`. Output is a single self-contained HTML file.

    python3 tools/md2html.py docs/DECISIONS.md docs/DECISIONS.html
"""
import html
import re
import sys
from pathlib import Path


def inline(t: str) -> str:
    parts = re.split(r"(`[^`]+`)", t)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append(f"<code>{html.escape(p[1:-1])}</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", p)
        p = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', p)
        out.append(p)
    return "".join(out)


def render(md: str) -> str:
    lines = md.splitlines()
    out, i = [], 0
    list_stack = []  # (indent, tag)

    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][0] > to_indent:
            out.append(f"</li></{list_stack.pop()[1]}>")

    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^(\s*)([*-]|\d+\.)\s+(.*)$", ln)
        if m and not re.match(r"^\s*(---|\*\*\*)\s*$", ln):
            ind, tag = len(m.group(1)), ("ol" if m.group(2)[0].isdigit() else "ul")
            text = m.group(3)
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^\s*([*-]|\d+\.)\s+", lines[i]) \
                    and lines[i].startswith(" " * (ind + 2)):
                text += " " + lines[i].strip()
                i += 1
            if list_stack and ind > list_stack[-1][0]:
                out.append(f"<{tag}><li>")
                list_stack.append((ind, tag))
            else:
                close_lists(ind)
                if list_stack and list_stack[-1][0] == ind:
                    out.append("</li><li>")
                else:
                    out.append(f"<{tag}><li>")
                    list_stack.append((ind, tag))
            out.append(inline(text))
            continue
        if list_stack and ln.strip() and ln.startswith("  ") and not ln.lstrip().startswith("|"):
            close_lists(len(ln) - len(ln.lstrip()) - 1)  # continuation belongs to the enclosing item
            out.append("<p>" + inline(ln.strip()) + "</p>")
            i += 1
            continue
        if not ln.strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if not (j < len(lines) and list_stack and (re.match(r"^\s*([*-]|\d+\.)\s+", lines[j])
                                                        or lines[j].startswith("  "))):
                close_lists()
            i += 1
            continue
        close_lists()
        if ln.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if h:
            n = len(h.group(1))
            text = h.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{n} id="{anchor}">{inline(text)}</h{n}>')
            i += 1
            continue
        if re.match(r"^\s*(---|\*\*\*)\s*$", ln):
            out.append("<hr>")
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = lambda r: [c.strip() for c in r.strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells(rows[0])) + "</tr></thead><tbody>")
            for r in rows[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>")
            out.append("</tbody></table>")
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue
        buf = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||```|>|\s*([*-]|\d+\.)\s)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")
    close_lists()
    return "\n".join(out)


CSS = """body{font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;max-width:1100px;margin:2em auto;padding:0 1.2em;color:#1d232b}
h1{border-bottom:2px solid #1f2d3d;padding-bottom:.3em}h2{margin-top:2em;border-bottom:1px solid #ccd}h3{margin-top:1.5em}
code{background:#f1f3f6;padding:.05em .3em;border-radius:3px;font-size:.92em}pre{background:#f1f3f6;padding:.8em;overflow:auto}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92em}th,td{border:1px solid #d5d9e0;padding:.4em .55em;vertical-align:top;text-align:left}
th{background:#eef1f5}tr:nth-child(even) td{background:#fafbfc}blockquote{border-left:4px solid #9aa7b8;margin:1em 0;padding:.2em 1em;color:#444;background:#f7f8fa}
li{margin:.2em 0}hr{border:0;border-top:1px solid #ccd;margin:2em 0}.src{color:#777;font-size:.85em}"""


def main(src: str, dst: str) -> None:
    md = Path(src).read_text()
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), Path(src).stem)
    body = render(md)
    doc = (f"<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
           f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>\n"
           f"<p class=\"src\">Rendered from <code>{html.escape(Path(src).as_posix())}</code> "
           f"by tools/md2html.py. The Markdown file is the source of truth.</p>\n{body}\n</body></html>\n")
    Path(dst).write_text(doc)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
