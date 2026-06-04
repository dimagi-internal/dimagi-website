#!/usr/bin/env python3
"""Generate sitemap.xml + robots.txt from each page's canonical URL.

Reads the canonical tag from every indexable HTML page (skipping any marked
noindex) so the sitemap URL set stays consistent with canonical signals.
"""
import os
import re
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "https://dimagi.com"
EXCLUDE_DIRS = {"node_modules", "Context", "dist", ".git", ".wrangler", ".claude"}

def iter_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)

def main():
    entries = {}
    for fp in iter_html():
        with open(fp, encoding="utf-8") as f:
            src = f.read()
        if re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex', src, re.I):
            continue
        m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', src, re.I)
        if not m:
            continue
        url = m.group(1).strip()
        mtime = datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat()
        # de-dupe; keep newest lastmod
        if url not in entries or mtime > entries[url]:
            entries[url] = mtime

    def priority(url):
        path = url[len(BASE):]
        if path == "/":
            return "1.0"
        depth = path.strip("/").count("/")
        if path.rstrip("/") in ("/blog", "/podcast", "/professional-services", "/contact"):
            return "0.9"
        if path.startswith("/legal"):
            return "0.3"
        return "0.7" if depth == 0 else "0.6"

    # Home first, then alphabetical
    urls = sorted(entries, key=lambda u: (u != BASE + "/", u))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{entries[u]}</lastmod>")
        lines.append(f"    <priority>{priority(u)}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /sign-in/\n"
        "\n"
        f"Sitemap: {BASE}/sitemap.xml\n"
    )
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"sitemap.xml: {len(urls)} urls; robots.txt written")

if __name__ == "__main__":
    main()
