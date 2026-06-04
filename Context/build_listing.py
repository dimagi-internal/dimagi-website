#!/usr/bin/env python3
"""Rebuild podcast/index.html episode grid as the full 77-episode archive (newest first).
Preserves the existing built cards' hand-written blurbs; adds the 64 back-catalog cards
using each episode's editorial deck as the blurb."""
import json, os, re, html
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LISTING = os.path.join(ROOT, "podcast", "index.html")
E = lambda s: html.escape(s or "", quote=False)

def month_year(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %Y")

def trim(text, limit=210):
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    p = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if p > 80:
        return cut[:p + 1]
    return cut[:cut.rfind(" ")].rstrip(",;: ") + "."

def card(num, date_label, title, blurb, href):
    # Use the episode's stylized Spotify cover when we have one; otherwise the
    # generic show cover with the play-icon overlay.
    cover_path = os.path.join(ROOT, "assets", "images", "podcast", "covers", href + ".jpg")
    if os.path.exists(cover_path):
        thumb = (f'<div class="episode-card-thumb">\n'
                 f'            <img src="../assets/images/podcast/covers/{href}.jpg" '
                 f'alt="High-Impact Growth Episode {num} cover" loading="lazy">\n'
                 f'          </div>')
    else:
        thumb = ('<div class="episode-card-thumb">\n'
                 '            <img src="../assets/images/high-impact-growth-podcast.jpeg" alt="Podcast cover" loading="lazy">\n'
                 '            <div class="episode-card-thumb-overlay">\n'
                 '              <div class="episode-play-icon">\n'
                 '                <svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>\n'
                 '              </div>\n'
                 '            </div>\n'
                 '          </div>')
    return f'''        <article class="episode-card">
          {thumb}
          <div class="episode-card-body">
            <div class="episode-num">Episode {num} &middot; {date_label}</div>
            <div class="episode-title">{title}</div>
            <p style="font-size:13px;color:var(--muted);line-height:1.5;margin:0;">{blurb}</p>
            <a class="episode-link" href="{href}/index.html">Listen now</a>
          </div>
        </article>'''

html_doc = open(LISTING, encoding="utf-8").read()

# 1) capture existing cards keyed by episode number (preserve their content verbatim)
existing = {}
for m in re.finditer(r'(?s)<article class="episode-card">.*?</article>', html_doc):
    block = m.group(0)
    nm = re.search(r"Episode\s+(\d+)\s*&middot;\s*([^<]+)</div>", block)
    tm = re.search(r'<div class="episode-title">(.*?)</div>', block, re.S)
    bm = re.search(r'<p style="font-size:13px[^"]*">(.*?)</p>', block, re.S)
    hm = re.search(r'href="([^"]+)/index\.html"', block)
    if nm and tm and hm:
        n = int(nm.group(1))
        existing[n] = card(n, nm.group(2).strip(), tm.group(1).strip(),
                           (bm.group(1).strip() if bm else ""), hm.group(1))

# 2) build new cards from manifest + editorial + extraction
manifest = json.load(open(os.path.join(HERE, "podcast-build-manifest.json")))
cards_by_num = dict(existing)
for row in manifest:
    if row["built"]:
        continue
    slug = row["slug"]
    ep = json.load(open(os.path.join(HERE, "episodes", slug + ".json"), encoding="utf-8"))
    edp = os.path.join(HERE, "editorial", slug + ".json")
    ed = json.load(open(edp, encoding="utf-8")) if os.path.exists(edp) else {}
    blurb = ed.get("deck") or (ep["show_notes"][0] if ep["show_notes"] else "")
    cards_by_num[row["num"]] = card(row["num"], month_year(row["date"]),
                                    E(ep["title"]), E(trim(blurb)), slug)

# 3) first 9 (always shown) -> Meet the Hosts -> the rest behind a "More Episodes" button
nums = sorted(cards_by_num, reverse=True)
grid1 = "\n\n".join(cards_by_num[n] for n in nums[:9])
grid2 = "\n\n".join(cards_by_num[n] for n in nums[9:])

hosts_section = '''  <!-- Meet the Hosts -->
  <section class="section hosts-section">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">The Hosts</span>
        <h2 class="section-title">Meet the hosts</h2>
        <p class="section-lede">High-Impact Growth is hosted by Dimagi CEO Jonathan Jackson and CommCare VP of Growth &amp; Strategy Amie Vaccaro.</p>
      </div>
      <div class="hosts-grid">
        <article class="host-card">
          <div class="host-card-photo"><img src="../assets/images/podcast/host-jonathan-jackson.jpg" alt="Jonathan Jackson" loading="lazy"></div>
          <div class="host-card-text">
            <p class="host-card-name">Jonathan Jackson</p>
            <p class="host-card-role">Co-Founder &amp; CEO, Dimagi</p>
            <p class="host-card-bio">Jonathan is the Co-Founder and Chief Executive Officer of Dimagi. He oversees a global team supporting digital solutions across the vast majority of countries with globally-recognized partners, and has led Dimagi to become a leading social enterprise and the creator of CommCare, the world's most widely used data collection platform.</p>
            <a class="host-card-link" href="https://www.linkedin.com/in/jonathanljackson/" target="_blank" rel="noopener">LinkedIn</a>
          </div>
        </article>
        <article class="host-card">
          <div class="host-card-photo"><img src="../assets/images/podcast/host-amie-vaccaro.jpg" alt="Amie Vaccaro" loading="lazy"></div>
          <div class="host-card-text">
            <p class="host-card-name">Amie Vaccaro</p>
            <p class="host-card-role">VP of Growth &amp; Strategy, CommCare</p>
            <p class="host-card-bio">Amie leads the team responsible for CommCare's brand strategy and for driving awareness and demand for its offerings. She is passionate about bringing together creativity, empathy, and technology to help people thrive, and brings over 15 years of experience, including 10 years in B2B technology product marketing.</p>
            <a class="host-card-link" href="https://www.linkedin.com/in/amievaccaro/" target="_blank" rel="noopener">LinkedIn</a>
          </div>
        </article>
      </div>
    </div>
  </section>'''

full_block = (
    '<div class="episodes-grid">\n\n' + grid1 +
    '\n\n      </div>\n    </div>\n  </section>\n\n' +
    hosts_section + '\n\n'
    '  <!-- More Episodes -->\n'
    '  <section class="section more-section">\n'
    '    <div class="container">\n'
    '      <div class="episodes-grid" id="more-grid">\n\n' + grid2 +
    '\n\n      </div>\n'
    '      <div class="more-wrap">\n'
    '        <button type="button" id="more-episodes-btn" class="btn btn-indigo btn-arrow">More Episodes</button>\n'
    '      </div>\n'
    '    </div>\n  </section>')

# idempotent splice: from the first episodes-grid through the last </section> before </main>
html_doc, n = re.subn(r'(?s)<div class="episodes-grid">.*</section>(\s*</main>)',
                      lambda m: full_block + m.group(1), html_doc, count=1)
assert n == 1, "grid splice failed"

# 4) reframe the first section header for a complete archive
html_doc = html_doc.replace("<span class=\"eyebrow\">Recent Episodes</span>",
                            "<span class=\"eyebrow\">The Archive</span>")
html_doc = html_doc.replace("<h2 class=\"section-title\">Latest conversations</h2>",
                            "<h2 class=\"section-title\">Every episode</h2>")
html_doc = html_doc.replace(
    "Browse the most recent episodes of High Impact Growth, with the full archive on dimagi.com.",
    "The complete High Impact Growth archive, from the first episode to the latest.")

open(LISTING, "w", encoding="utf-8").write(html_doc)
print(f"listing rebuilt: {len(cards_by_num)} cards ({len(existing)} existing preserved, "
      f"{len(cards_by_num)-len(existing)} new)")
