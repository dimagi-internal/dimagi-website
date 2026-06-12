#!/usr/bin/env python3
"""Re-sync blog listing card blurbs to each article's current meta description.

The listing (blog/index.html) cards copy their <p class="blog-card-desc"> text
from each article's meta description at build time. After trim_meta.py shortened
148 descriptions, the listing kept the old long copies. This pulls each card's
blurb back in line with its article's current meta description.

The meta description is already escaped for an attribute (&amp; &lt; &gt; &quot;),
which is also valid as element text, so it is copied verbatim. Idempotent.

Usage:
  python3 Context/seo/sync_listing_desc.py            # dry-run
  python3 Context/seo/sync_listing_desc.py --apply    # write changes
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LISTING = os.path.join(ROOT, "blog", "index.html")
APPLY = "--apply" in sys.argv

def main():
    src = open(LISTING, encoding="utf-8").read()
    changed = missing = 0

    def fix_card(m):
        nonlocal changed, missing
        card = m.group(0)
        href = re.search(r'class="blog-card-image" href="([^"/]+)/', card)
        if not href:
            return card
        slug = href.group(1)
        fp = os.path.join(ROOT, "blog", slug, "index.html")
        if not os.path.isfile(fp):
            missing += 1
            return card
        md = re.search(r'<meta name="description" content="(.*?)">', open(fp, encoding="utf-8").read())
        if not md:
            return card
        desc = md.group(1).strip()
        new = re.sub(r'(<p class="blog-card-desc">).*?(</p>)',
                     lambda d: d.group(1) + desc + d.group(2), card, count=1, flags=re.S)
        if new != card:
            changed += 1
        return new

    out = re.sub(r'<article class="blog-card".*?</article>', fix_card, src, flags=re.S)
    if APPLY and out != src:
        open(LISTING, "w", encoding="utf-8").write(out)
    print(f"{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} card blurbs synced, {missing} missing-article")

if __name__ == "__main__":
    main()
