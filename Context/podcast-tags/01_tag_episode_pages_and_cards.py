#!/usr/bin/env python3
import re, os, sys

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login/podcast"

# ---- Facet label maps ----
LABEL = {
    # products
    'commcare':'CommCare','sureadhere':'SureAdhere','connect':'Connect','open-chat-studio':'Open Chat Studio',
    # sectors
    'community-health':'Community Health','maternal-newborn-child-health':'Maternal, Newborn & Child Health',
    'mental-health':'Mental Health','infectious-disease':'Infectious Disease','nutrition':'Nutrition',
    'child-health':'Child Health','livelihoods':'Livelihoods','humanitarian-response':'Humanitarian Response',
    # use cases
    'monitoring-evaluation':'Monitoring & Evaluation','cash-voucher-assistance':'Cash & Voucher Assistance',
    'service-delivery':'Service Delivery','workforce-management':'Workforce Management','sponsorship':'Sponsorship',
    # org types
    'governments':'Governments','international-ngos':'International NGOs','research-academic':'Research & Academic',
    'us-community-health':'US Community Health',
    # themes
    'ai':'AI','global-development':'Global Development','leadership':'Leadership','company-culture':'Company & Culture',
}

# ep number -> tags  (p=product, sec=sector, uc=use case, org=org type, th=theme, staff=bool)
D = {
 2:{'staff':1,'th':['company-culture']},
 3:{'p':['commcare'],'staff':1,'th':['company-culture']},
 4:{'p':['commcare'],'staff':1,'th':['company-culture']},
 5:{'p':['commcare'],'staff':1,'th':['global-development']},
 6:{'p':['commcare'],'staff':1,'org':['international-ngos'],'uc':['service-delivery']},
 7:{'p':['commcare'],'staff':1,'org':['governments']},
 8:{'staff':1,'sec':['community-health']},
 9:{'staff':1,'th':['global-development']},
 10:{'p':['commcare'],'staff':1,'th':['company-culture']},
 11:{'p':['commcare'],'th':['global-development']},
 12:{'p':['commcare'],'staff':1,'th':['global-development']},
 13:{'staff':1,'org':['governments'],'th':['global-development']},
 14:{'p':['commcare'],'staff':1,'sec':['nutrition'],'uc':['workforce-management'],'org':['governments']},
 15:{'p':['commcare'],'staff':1,'sec':['infectious-disease'],'uc':['service-delivery'],'org':['us-community-health']},
 16:{'staff':1,'th':['company-culture']},
 17:{'th':['global-development']},
 18:{'staff':1,'th':['company-culture']},
 19:{'staff':1,'th':['company-culture']},
 20:{'p':['commcare'],'org':['governments']},
 21:{'staff':1,'th':['company-culture']},
 22:{'org':['governments']},
 23:{'th':['ai','global-development']},
 24:{'staff':1,'th':['global-development']},
 25:{'p':['commcare'],'sec':['humanitarian-response'],'uc':['monitoring-evaluation'],'org':['international-ngos']},
 26:{'p':['commcare'],'sec':['maternal-newborn-child-health'],'uc':['service-delivery']},
 27:{'staff':1,'th':['ai']},
 28:{'staff':1,'sec':['mental-health']},
 29:{'staff':1,'sec':['community-health']},
 30:{'th':['leadership']},
 31:{'staff':1,'th':['company-culture']},
 32:{'staff':1,'th':['company-culture']},
 33:{'p':['commcare'],'sec':['infectious-disease'],'org':['international-ngos']},
 34:{'p':['commcare'],'sec':['community-health','maternal-newborn-child-health']},
 35:{'p':['commcare'],'sec':['community-health']},
 36:{'th':['global-development']},
 37:{'p':['open-chat-studio'],'staff':1,'th':['ai']},
 38:{'p':['commcare'],'staff':1,'sec':['mental-health']},
 39:{'p':['commcare'],'sec':['community-health']},
 40:{'p':['commcare'],'staff':1,'sec':['community-health'],'th':['company-culture']},
 41:{'sec':['mental-health'],'org':['research-academic']},
 42:{'p':['sureadhere'],'staff':1,'sec':['infectious-disease'],'org':['research-academic'],'th':['company-culture']},
 43:{'p':['sureadhere'],'sec':['infectious-disease']},
 44:{'staff':1,'sec':['mental-health']},
 45:{'staff':1,'th':['global-development']},
 46:{'sec':['community-health']},
 47:{'p':['commcare'],'sec':['community-health'],'org':['governments']},
 48:{'p':['commcare'],'sec':['mental-health']},
 49:{'staff':1,'th':['global-development']},
 50:{'p':['commcare'],'sec':['community-health'],'org':['us-community-health']},
 51:{'p':['sureadhere'],'staff':1,'sec':['infectious-disease']},
 52:{'th':['leadership']},
 53:{'staff':1,'th':['ai']},
 54:{'org':['governments','us-community-health'],'th':['ai']},
 55:{'p':['commcare'],'sec':['mental-health']},
 57:{'p':['commcare'],'sec':['child-health']},
 59:{'p':['open-chat-studio'],'staff':1,'th':['ai']},
 62:{'p':['connect'],'sec':['community-health'],'th':['global-development']},
 63:{'p':['connect'],'staff':1,'sec':['community-health']},
 64:{'p':['commcare'],'uc':['monitoring-evaluation'],'org':['international-ngos']},
 65:{'p':['commcare'],'org':['international-ngos'],'th':['global-development']},
 66:{'p':['commcare','sureadhere'],'staff':1,'th':['company-culture']},
 67:{'staff':1,'th':['global-development']},
 68:{'staff':1,'th':['company-culture']},
 69:{'p':['commcare'],'uc':['cash-voucher-assistance'],'th':['global-development']},
 70:{'p':['commcare'],'sec':['livelihoods'],'th':['global-development']},
 71:{'th':['global-development']},
 72:{'th':['leadership']},
 73:{'th':['global-development']},
 74:{'th':['leadership']},
 75:{'p':['commcare'],'staff':1,'th':['global-development']},
 76:{'th':['global-development']},
 77:{'staff':1,'th':['ai']},
 78:{'th':['global-development']},
 80:{'org':['research-academic'],'th':['ai']},
 81:{'uc':['sponsorship'],'th':['global-development']},
 82:{'p':['commcare'],'sec':['mental-health']},
 83:{'sec':['community-health'],'th':['ai']},
}

CHIP_CSS = """
/* ---- Topic tags ---- */
.ep-tags {
  list-style: none; display: flex; flex-wrap: wrap; gap: 8px;
  margin: 22px 0 0; padding: 0; position: relative; z-index: 1;
}
.ep-tag {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 6px 14px; border-radius: 999px;
  font-family: var(--sans); font-size: 12px; font-weight: 500;
  letter-spacing: 0.02em; line-height: 1;
  color: rgba(255,255,255,0.82);
  border: 1px solid rgba(255,255,255,0.20);
  background: rgba(255,255,255,0.05);
  transition: background 150ms, border-color 150ms, color 150ms;
}
.ep-tag:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.42); color: #fff; }
.ep-tag::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%;
  background: currentColor; opacity: 0.65; flex-shrink: 0;
}
.ep-tag--product {
  color: #6fe3d6; border-color: rgba(13,168,157,0.55); background: rgba(13,168,157,0.12);
}
.ep-tag--product:hover { background: rgba(13,168,157,0.22); border-color: rgba(13,168,157,0.8); color: #aef3ea; }
.ep-tag--theme { color: rgba(255,255,255,0.66); background: transparent; }
"""

def chip_row(tags):
    items = []
    def add(kind, slug, css):
        items.append(
            '          <li><a class="ep-tag ep-tag--%s" href="../index.html?%s=%s">%s</a></li>'
            % (css, kind, slug, LABEL[slug])
        )
    for s in tags.get('p', []):   add('product', s, 'product')
    for s in tags.get('sec', []): add('sector', s, 'solution')
    for s in tags.get('uc', []):  add('usecase', s, 'solution')
    for s in tags.get('org', []): add('orgtype', s, 'solution')
    for s in tags.get('th', []):  add('theme', s, 'theme')
    if not items:
        return ''
    return ('\n\n        <ul class="ep-tags" aria-label="Topics">\n'
            + '\n'.join(items) + '\n        </ul>')

# ---------- Build slug<->num map from the listing ----------
listing_path = os.path.join(ROOT, 'index.html')
L = open(listing_path, encoding='utf-8').read()
cards = re.findall(
    r'<div class="episode-num">(.*?)</div>.*?<a class="episode-link" href="(.*?)/index\.html"',
    L, re.S)
slug2num = {}
for num, slug in cards:
    m = re.search(r'(\d+)', re.sub('<[^>]+>', '', num))
    if m:
        slug2num[slug] = int(m.group(1))
assert len(slug2num) == 77, "expected 77 cards, got %d" % len(slug2num)

# ---------- 1) Episode pages: CSS + chip row ----------
ep_done = 0
for slug, n in slug2num.items():
    if n not in D:
        print("  !! no tag data for ep", n, slug); continue
    fp = os.path.join(ROOT, slug, 'index.html')
    t = open(fp, encoding='utf-8').read()
    orig = t
    # CSS: insert once after the `.ep-meta .dot {...}` rule
    if '/* ---- Topic tags ---- */' not in t:
        t = t.replace(
            '.ep-meta .dot { width: 3px; height: 3px; border-radius: 50%; background: rgba(254,175,49,0.6); }',
            '.ep-meta .dot { width: 3px; height: 3px; border-radius: 50%; background: rgba(254,175,49,0.6); }\n'
            + CHIP_CSS, 1)
    # Chip row: replace deck (+ any existing ep-tags) up to the closing hero-text </div>
    row = chip_row(D[n])
    t = re.sub(
        r'(<p class="ep-deck">.*?</p>)(?:\s*<ul class="ep-tags".*?</ul>)?\s*</div>',
        lambda m: m.group(1) + row + '\n      </div>',
        t, count=1, flags=re.S)
    if t != orig:
        open(fp, 'w', encoding='utf-8').write(t)
        ep_done += 1

print("Episode pages updated:", ep_done)

# ---------- 2) Listing: data attributes on cards ----------
def attrs_for(n):
    d = D.get(n, {})
    def join(k): return ' '.join(d.get(k, []))
    sector = join('sec'); uc = join('uc'); org = join('org')
    return (' data-product="%s" data-sector="%s" data-usecase="%s" data-orgtype="%s"'
            ' data-theme="%s" data-staff="%s"'
            % (join('p'), sector, uc, org, join('th'), 'yes' if d.get('staff') else 'no'))

def add_card_attrs(m):
    block = m.group(0)
    if 'data-product=' in block.split('>', 1)[0]:
        return block  # already tagged
    sm = re.search(r'<a class="episode-link" href="(.*?)/index\.html"', block)
    if not sm:
        return block
    n = slug2num.get(sm.group(1))
    if n is None:
        return block
    return block.replace('<article class="episode-card">',
                         '<article class="episode-card"%s>' % attrs_for(n), 1)

L2 = re.sub(r'<article class="episode-card">.*?</article>', add_card_attrs, L, flags=re.S)
print("cards given data-attrs:", L2.count('data-product='))

open(listing_path, 'w', encoding='utf-8').write(L2)
print("Listing data-attrs written.")
