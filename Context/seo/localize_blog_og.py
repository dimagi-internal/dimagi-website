#!/usr/bin/env python3
"""Repoint blog og:image / twitter:image from external WordPress URLs to the
locally-saved cover image, so social cards survive the dimagi.com migration.

For each blog/<slug>/index.html that has assets/images/<slug>/cover.* it sets
og:image, twitter:image and og:image:width/height to the local cover (absolute
URL, real dimensions). Posts without a local cover are left untouched.
"""
import os
import re
import glob
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "https://dimagi.com"

def main():
    changed = 0
    skipped = 0
    for idx in sorted(glob.glob(os.path.join(ROOT, "blog", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(idx))
        covers = sorted(glob.glob(os.path.join(ROOT, "assets", "images", slug, "cover.*")))
        if not covers:
            skipped += 1
            continue
        cover = covers[0]
        ext = os.path.splitext(cover)[1].lstrip(".")
        url = f"{BASE}/assets/images/{slug}/cover.{ext}"
        try:
            w, h = Image.open(cover).size
        except Exception:
            w = h = None

        with open(idx, encoding="utf-8") as f:
            src = f.read()
        new = src
        new = re.sub(r'(<meta\s+property="og:image"\s+content=")[^"]*(")',
                     rf'\g<1>{url}\g<2>', new)
        new = re.sub(r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")',
                     rf'\g<1>{url}\g<2>', new)
        if w and h:
            if re.search(r'<meta\s+property="og:image:width"', new):
                new = re.sub(r'(<meta\s+property="og:image:width"\s+content=")[^"]*(")',
                             rf'\g<1>{w}\g<2>', new)
                new = re.sub(r'(<meta\s+property="og:image:height"\s+content=")[^"]*(")',
                             rf'\g<1>{h}\g<2>', new)
            else:
                # insert dims right after the og:image tag
                new = re.sub(
                    r'(<meta\s+property="og:image"\s+content="[^"]*">)',
                    rf'\g<1>\n<meta property="og:image:width" content="{w}">\n'
                    rf'<meta property="og:image:height" content="{h}">',
                    new, count=1)

        if new != src:
            with open(idx, "w", encoding="utf-8") as f:
                f.write(new)
            changed += 1

    print(f"repointed {changed} blog posts to local covers; {skipped} without a local cover")

if __name__ == "__main__":
    main()
