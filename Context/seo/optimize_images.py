#!/usr/bin/env python3
"""Optimize blog/asset cover images for web delivery.

  - Opaque photographic PNG covers  -> JPEG q84 progressive (huge saving),
    original PNG removed, all HTML references rewritten cover.png -> cover.jpg.
  - PNG covers with real transparency -> kept as PNG, re-saved optimized.
  - JPEG covers over 500 KB          -> re-encoded q84 progressive in place.

Reference rewriting is keyed on the unique "<slug>/cover.png" substring so only
converted covers are touched. Run from project root; safe to re-run.
"""
import os
import glob
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
Q = 84

def is_transparent(im):
    if im.mode in ("RGBA", "LA"):
        a = im.getchannel("A")
        return a.getextrema()[0] < 250
    if im.mode == "P" and "transparency" in im.info:
        return True
    return False

converted = []   # slugs png->jpg
kept_png = 0
reencoded_jpg = 0
before = after = 0

for png in glob.glob("assets/images/*/cover.png"):
    before += os.path.getsize(png)
    im = Image.open(png)
    if is_transparent(im):
        im.save(png, optimize=True)
        kept_png += 1
        after += os.path.getsize(png)
        continue
    jpg = png[:-4] + ".jpg"
    im.convert("RGB").save(jpg, "JPEG", quality=Q, progressive=True, optimize=True)
    os.remove(png)
    after += os.path.getsize(jpg)
    converted.append(os.path.basename(os.path.dirname(png)))

# Recompress heavy JPEG covers in place (no reference change)
for jpg in glob.glob("assets/images/*/cover.jpg"):
    sz = os.path.getsize(jpg)
    # skip ones we just created from PNG (already q84)
    slug = os.path.basename(os.path.dirname(jpg))
    if slug in converted:
        continue
    if sz > 500 * 1024:
        im = Image.open(jpg).convert("RGB")
        im.save(jpg, "JPEG", quality=Q, progressive=True, optimize=True)
        reencoded_jpg += 1

# Rewrite references for converted covers across all HTML
ref_changes = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in
                   {"node_modules", "Context", "dist", ".git", ".wrangler", ".claude"}]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        src = open(fp, encoding="utf-8").read()
        new = src
        for slug in converted:
            new = new.replace(f"{slug}/cover.png", f"{slug}/cover.jpg")
        if new != src:
            open(fp, "w", encoding="utf-8").write(new)
            ref_changes += 1

print(f"PNG->JPEG converted: {len(converted)} covers")
print(f"transparent PNG kept+optimized: {kept_png}")
print(f"heavy JPEG re-encoded: {reencoded_jpg}")
print(f"HTML files with rewritten refs: {ref_changes}")
print(f"PNG-cover bytes: {before//1024} KB -> {after//1024} KB")
