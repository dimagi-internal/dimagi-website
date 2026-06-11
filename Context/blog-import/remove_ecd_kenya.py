# Reverse the Saving Brains / Ugunja Kenya ECD blog (too old). Removes the listing
# card, sitemap entry, and tag_overrides row. Folder trashing is done separately.
import os, re
ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "commcare-ecd-community-health-volunteers-kenya"

# 1. listing card
idx = os.path.join(ROOT, "blog", "index.html")
s = open(idx, encoding='utf-8').read()
before = s.count('class="blog-card"')
# remove the whole article block (plus its leading whitespace/newline) for this slug
s2 = re.sub(r'\n?[ \t]*<article class="blog-card"(?:(?!</article>).)*?' + re.escape(SLUG) + r'.*?</article>',
           '', s, flags=re.S)
open(idx, 'w', encoding='utf-8').write(s2)
print("listing cards:", before, "->", s2.count('class="blog-card"'))

# 2. sitemap entry
sm = os.path.join(ROOT, "sitemap.xml")
t = open(sm, encoding='utf-8').read()
t2 = re.sub(r'\n?[ \t]*<url>(?:(?!</url>).)*?' + re.escape(SLUG) + r'.*?</url>', '', t, flags=re.S)
open(sm, 'w', encoding='utf-8').write(t2)
print("sitemap urls:", t.count('<url>'), "->", t2.count('<url>'))

# 3. tag_overrides row
to = os.path.join(HERE, "tag_overrides.csv")
lines = open(to, encoding='utf-8').read().splitlines(keepends=True)
kept = [l for l in lines if not l.startswith(SLUG + ",")]
open(to, 'w', encoding='utf-8').write("".join(kept))
print("tag_overrides rows removed:", len(lines) - len(kept))
print("DONE")
