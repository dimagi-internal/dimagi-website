#!/usr/bin/env python3
"""Fill descriptive alt text on inline blog images that have empty alt="".

Keys in alt_overrides.json are 'slug|filename'. For each blog article image with
a missing or empty alt whose src basename matches an override, set the alt.
Only touches images that are currently empty/missing alt, so it never overwrites
alt text that already exists. Idempotent.

Usage:
  python3 Context/seo/apply_alt.py            # dry-run
  python3 Context/seo/apply_alt.py --apply    # write changes
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BLOG = os.path.join(ROOT, "blog")
APPLY = "--apply" in sys.argv

def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

def main():
    table = {k: v for k, v in json.load(
        open(os.path.join(HERE, "alt_overrides.json"))).items()
        if not k.startswith("_")}

    changed = unmatched = 0
    used = set()
    for slug_dir in sorted(os.listdir(BLOG)):
        fp = os.path.join(BLOG, slug_dir, "index.html")
        if not os.path.isfile(fp):
            continue
        src = open(fp, encoding="utf-8").read()
        head, _, body = src.partition("</head>")
        if not body:
            body = src

        def repl(m):
            nonlocal changed
            tag = m.group(0)
            # only act on empty or missing alt
            if 'alt=' in tag and not re.search(r'alt=("|\')\s*("|\')', tag):
                return tag
            sm = re.search(r'src="([^"]*)"', tag)
            if not sm:
                return tag
            fname = os.path.basename(sm.group(1))
            key = f"{slug_dir}|{fname}"
            if key not in table:
                return tag
            used.add(key)
            alt = f'alt="{esc(table[key])}"'
            if re.search(r'alt=("|\')\s*("|\')', tag):
                new = re.sub(r'alt=("|\')\s*("|\')', alt, tag, count=1)
            else:  # missing entirely: insert after <img
                new = re.sub(r'<img\b', f'<img {alt}', tag, count=1)
            if new != tag:
                changed += 1
            return new

        new_body = re.sub(r"<img\b[^>]*>", repl, body)
        if new_body != body:
            out = head + "</head>" + new_body if "</head>" in src else new_body
            if APPLY:
                open(fp, "w", encoding="utf-8").write(out)

    for key in table:
        if key not in used:
            unmatched += 1
            print(f"  UNMATCHED (img not found / already had alt): {key}")

    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} alts set, {unmatched} unmatched")

if __name__ == "__main__":
    main()
