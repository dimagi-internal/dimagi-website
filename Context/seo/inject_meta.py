#!/usr/bin/env python3
"""Idempotently fill SEO/social metadata gaps across all source HTML pages.

For every page it ensures (only inserting what is MISSING, so already-complete
blog pages are left intact):
  - canonical link (derived from the served path)
  - Open Graph: type, url, title, description, site_name, locale, image(+alt)
  - Twitter card: card, title, description, image
  - resolves any RELATIVE og:image to an absolute https URL (fixes podcast bug)
  - robots meta (noindex for sign-in / 404, index otherwise)

Run from the project root. Re-running is safe.
"""
import os
import re
import html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "https://dimagi.com"
DEFAULT_IMG = f"{BASE}/assets/images/og-default.png"
EXCLUDE_DIRS = {"node_modules", "Context", "dist", ".git", ".wrangler", ".claude"}
NOINDEX = {"sign-in/index.html", "404.html"}

def iter_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)

def served_path(rel):
    """Map a file path to its served URL path (clean, trailing slash)."""
    p = rel.replace(os.sep, "/")
    if p == "index.html":
        return "/"
    if p == "404.html":
        return "/404.html"
    if p.endswith("/index.html"):
        return "/" + p[: -len("index.html")]
    return "/" + p

def abs_url(path):
    return BASE + path if path.startswith("/") else path

def resolve_img(content, rel):
    """Make an og:image absolute. Relative paths resolve against the file dir."""
    content = content.strip()
    if content.startswith("http://") or content.startswith("https://"):
        return content
    file_dir = "/" + os.path.dirname(rel.replace(os.sep, "/"))
    if file_dir == "/":
        file_dir = ""
    joined = os.path.normpath(os.path.join(file_dir, content)).replace(os.sep, "/")
    if not joined.startswith("/"):
        joined = "/" + joined
    return BASE + joined

def get(pattern, head):
    m = re.search(pattern, head, re.I)
    return m.group(1).strip() if m else None

def main():
    changed = 0
    for fp in iter_html():
        rel = os.path.relpath(fp, ROOT)
        with open(fp, encoding="utf-8") as f:
            src = f.read()
        head_m = re.search(r"<head\b[^>]*>(.*?)</head>", src, re.I | re.S)
        if not head_m:
            continue
        head = head_m.group(1)

        title = get(r"<title>(.*?)</title>", head) or "Dimagi"
        og_title = re.sub(r"\s*[|││]\s*Dimagi\s*$", "", title).strip() or title
        dm = re.search(r'<meta\s+name=["\']description["\']\s+content=(["\'])(.*?)\1', head, re.I | re.S)
        desc = dm.group(2).strip() if dm else ""

        path = served_path(rel)
        canonical = get(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', head) or abs_url(path)

        existing_img = get(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', head)
        img = resolve_img(existing_img, rel) if existing_img else DEFAULT_IMG

        is_noindex = rel.replace(os.sep, "/") in NOINDEX
        has = lambda needle: needle in head

        adds = []
        def add(line, marker):
            if not has(marker):
                adds.append(line)

        add(f'<link rel="canonical" href="{canonical}">', 'rel="canonical"')
        robots = "noindex, nofollow" if is_noindex else "index, follow, max-image-preview:large"
        add(f'<meta name="robots" content="{robots}">', 'name="robots"')
        add(f'<meta property="og:site_name" content="Dimagi">', 'og:site_name')
        add(f'<meta property="og:locale" content="en_US">', 'og:locale')
        add(f'<meta property="og:type" content="website">', 'og:type')
        add(f'<meta property="og:url" content="{canonical}">', 'og:url')
        add(f'<meta property="og:title" content="{og_title}">', 'og:title')
        if desc:
            add(f'<meta property="og:description" content="{desc}">', 'og:description')
        add(f'<meta property="og:image" content="{img}">', 'og:image')
        add(f'<meta property="og:image:alt" content="Dimagi — Digital Solutions for Frontline Work">', 'og:image:alt')
        add(f'<meta name="twitter:card" content="summary_large_image">', 'twitter:card')
        add(f'<meta name="twitter:title" content="{og_title}">', 'twitter:title')
        if desc:
            add(f'<meta name="twitter:description" content="{desc}">', 'twitter:description')
        add(f'<meta name="twitter:image" content="{img}">', 'twitter:image')

        # Fix a relative og:image already in the file (e.g. podcast pages)
        new_src = src
        if existing_img and not existing_img.startswith("http"):
            new_src = new_src.replace(
                f'property="og:image" content="{existing_img}"',
                f'property="og:image" content="{img}"',
            )

        if not adds:
            if new_src != src:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_src)
                changed += 1
            continue

        block = "\n".join(adds)
        # Insert after the description meta, else after <title>
        anchor = re.search(r'(<meta\s+name=["\']description["\'][^>]*>)', new_src, re.I)
        if not anchor:
            anchor = re.search(r'(</title>)', new_src, re.I)
        insert_at = anchor.end()
        new_src = new_src[:insert_at] + "\n" + block + new_src[insert_at:]
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_src)
        changed += 1

    print(f"updated {changed} pages")

if __name__ == "__main__":
    main()
