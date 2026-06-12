#!/usr/bin/env python3
"""Apply concise <title> overrides from title_overrides.json.

Over-length blog titles (>60 chars) get truncated in search results and the
browser tab, and the " | Dimagi" brand suffix never shows. This rewrites ONLY
the <title> element to a tight <=60-char version; the on-page <h1> and og:title
are left long and descriptive on purpose.

For durability it also patches the matching record's `titletag` in
records_archive/ when one exists, so a fresh render produces the short title too.

Idempotent: re-running sets the same value. Run after any blog regen, alongside
trim_meta.py / transform_filters.py / apply_tag_pass.py.

Usage:
  python3 Context/seo/apply_titles.py            # dry-run
  python3 Context/seo/apply_titles.py --apply    # write changes
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BLOG = os.path.join(ROOT, "blog")
RECORDS = os.path.join(ROOT, "Context", "blog-import", "records_archive")
BRAND = " | Dimagi"
APPLY = "--apply" in sys.argv

def esc_title(text):
    # <title> is PCDATA: escape &, <, > only (quotes are literal).
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def main():
    overrides = {k: v for k, v in json.load(
        open(os.path.join(HERE, "title_overrides.json"))).items()
        if not k.startswith("_")}

    changed = warn = 0
    for slug, short in overrides.items():
        full = short + BRAND
        if len(full) > 62:
            print(f"  WARN long ({len(full)}): {slug} -> {full}")
            warn += 1
        esc = esc_title(full)

        fp = os.path.join(BLOG, slug, "index.html")
        if not os.path.isfile(fp):
            print(f"  MISSING html: {slug}")
            warn += 1
            continue
        src = open(fp, encoding="utf-8").read()
        m = re.search(r"<title>(.*?)</title>", src, re.S)
        old = m.group(1) if m else ""
        if old != esc:
            new = re.sub(r"<title>.*?</title>", f"<title>{esc}</title>", src, count=1, flags=re.S)
            changed += 1
            if APPLY:
                open(fp, "w", encoding="utf-8").write(new)
            print(f"[{len(full):>2}] {slug}\n      {html.unescape(old)}\n   -> {full}")

        # keep the source record in sync if it exists
        rp = os.path.join(RECORDS, slug + ".json")
        if os.path.isfile(rp):
            rec = json.load(open(rp))
            if rec.get("titletag") != full:
                rec["titletag"] = full
                if APPLY:
                    json.dump(rec, open(rp, "w"), ensure_ascii=False, indent=2)

    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} titles, {warn} warnings")

if __name__ == "__main__":
    main()
