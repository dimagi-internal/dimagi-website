#!/usr/bin/env python3
"""(Re)apply the /podcast/ listing filter: blog-style search box + Product / Focus / Theme
dropdowns + the combined lazy-reveal/filter controller.

Source of truth is ../podcast_tags.py (filter_bar_html / FILTER_CSS / COMBINED_JS); this
script imports it so there is no duplicated markup to drift. It is *upgrading* (not just
additive): if an older chip-row filter is present it is replaced, so re-running after a
stale regen restores the current design.
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from podcast_tags import filter_bar_html, FILTER_CSS, COMBINED_JS  # noqa: E402

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login/podcast"
listing_path = os.path.join(ROOT, "index.html")
L = open(listing_path, encoding="utf-8").read()
orig = L

# NOTE: re.sub processes backslash escapes in a *string* replacement (e.g. the CSS escape
# "\2713" for the ✓ checkmark would be mangled into an octal escape). Pass replacements as
# functions (lambda m: text) so they are inserted verbatim.
def _const(text):
    return lambda m: text

# 1) head filter CSS — replace the existing "Episode filters" block, else insert it.
css_block = FILTER_CSS.strip("\n")
if "/* ── Episode filters" in L:
    L = re.sub(r"/\* ── Episode filters.*?(?=\n+/\* Podcast page header)",
               _const(css_block), L, count=1, flags=re.S)
else:
    L = L.replace("<style>\n/* ── Podcast page ── */",
                  "<style>\n/* ── Podcast page ── */\n" + FILTER_CSS, 1)

# 2) filter bar + empty state before the first grid — replace existing bar (old chip OR
#    new dropdown markup both start with .pod-filters and end at the pod-empty <p>), else insert.
if 'class="pod-filters"' in L:
    L = re.sub(r' {8}<div class="pod-filters".*?</button></p>',
               _const(filter_bar_html()), L, count=1, flags=re.S)
else:
    L = L.replace('      <div class="episodes-grid">',
                  filter_bar_html() + '\n\n      <div class="episodes-grid">', 1)

# 3) the controller <script> — replace the current filter/reveal script, else the bare
#    "Load More Episodes" reveal script, else insert before </body>.
if "Episode archive: lazy-reveal" in L:
    L = re.sub(r'<script>\s*\n/\* Episode archive: lazy-reveal.*?</script>',
               _const(COMBINED_JS), L, count=1, flags=re.S)
elif re.search(r'<script>\s*\n/\* "Load More Episodes".*?</script>', L, flags=re.S):
    L = re.sub(r'<script>\s*\n/\* "Load More Episodes".*?</script>',
               _const(COMBINED_JS), L, count=1, flags=re.S)
else:
    L = L.replace("</body>", COMBINED_JS + "\n</body>", 1)

open(listing_path, "w", encoding="utf-8").write(L)
print("Listing filter (re)applied:", "changed" if L != orig else "already current")
