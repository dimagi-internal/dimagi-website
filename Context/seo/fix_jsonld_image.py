#!/usr/bin/env python3
"""
Align each blog post's JSON-LD Article `"image"` with its real cover.

Migrated posts shipped with JSON-LD structured-data images pointing at the old
dimagi.com/wp-content/... WordPress URLs. Many of those 404, and all of them are
inconsistent with the migrated local cover that og:image already uses. Search
engines read the JSON-LD image for rich results, so a 404/stale URL there hurts.

This script repoints the JSON-LD `"image"` to the post's og:image value (the
local /assets/images/<slug>/cover.* URL). It is idempotent: posts already pointing
at a non-wp-content image are left untouched.

Run from the site root:  python3 Context/seo/fix_jsonld_image.py [--dry-run]
"""
import re, glob, sys

DRY = '--dry-run' in sys.argv

def main():
    posts = sorted(glob.glob('blog/*/index.html'))
    changed = 0
    for f in posts:
        s = open(f, encoding='utf-8').read()
        m = re.search(r'("image"\s*:\s*")([^"]+)(")', s)   # first match = Article image
        if not m or 'wp-content' not in m.group(2):
            continue
        og = re.search(r'(?:property|name)="og:image"\s+content="([^"]+)"', s)
        if not og:
            continue
        new = s[:m.start()] + m.group(1) + og.group(1) + m.group(3) + s[m.end():]
        if new != s:
            changed += 1
            if not DRY:
                open(f, 'w', encoding='utf-8').write(new)
    print(("[dry-run] would change" if DRY else "updated"), changed, "posts")

if __name__ == '__main__':
    main()
