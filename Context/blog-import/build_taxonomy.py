# Build the full 4-dimension blog filter (Product/Type/Topic/Country).
# Classifies every card by mining its own article page (title+deck+body),
# then (in apply mode) tags each card with data-product/type/topic/country and
# rebuilds the filter into 4 labeled rows. Dry-run by default.
import re, os, sys, html as _html
from collections import Counter

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
IDX = os.path.join(ROOT, "blog", "index.html")
APPLY = "--apply" in sys.argv

idx = open(IDX, encoding='utf-8').read()

# --- pull every card: slug, title, topic(category), from the listing ---
card_re = re.compile(
    r'<article class="blog-card"[^>]*>\s*'
    r'<a class="blog-card-image" href="([^"/]+)/index\.html">.*?'
    r'<div class="blog-card-category">([^<]+)</div>\s*'
    r'<h2 class="blog-card-title">(.*?)</h2>', re.S)
cards = [(m.group(1), m.group(2).strip(), re.sub('<[^>]+>', '', m.group(3)).strip())
         for m in card_re.finditer(idx)]

COUNTRIES = {
    'India':['India'], 'Nigeria':['Nigeria'], 'Kenya':['Kenya'], 'Malawi':['Malawi'],
    'Mozambique':['Mozambique'], 'Ethiopia':['Ethiopia'], 'South Africa':['South Africa'],
    'Zambia':['Zambia'], 'Tanzania':['Tanzania'], 'Uganda':['Uganda'], 'Senegal':['Senegal'],
    'Madagascar':['Madagascar'], 'Sierra Leone':['Sierra Leone'], 'Somalia':['Somalia'],
    'Jamaica':['Jamaica'], 'Cambodia':['Cambodia'], 'Tajikistan':['Tajikistan'],
    'Guinea':['Guinea'], 'Benin':['Benin'], 'Burkina Faso':['Burkina Faso'], 'Niger':['Niger'],
    "Cote d'Ivoire":["Cote d", "Côte d", 'Ivory Coast'], 'Lesotho':['Lesotho'],
    'Rwanda':['Rwanda'], 'Ghana':['Ghana'], 'Bangladesh':['Bangladesh'], 'Nepal':['Nepal'],
    'Indonesia':['Indonesia'], 'Mexico':['Mexico'],
    'United States':['United States','Vermont','Arizona','Somerville','Pima County','Iowa','Island Health'],
}
# USAID and its spelled-out forms must NOT count as "United States" (they appear everywhere).
USAID_NOISE = re.compile(r'USAID|United States Agency for International Development|U\.?S\.?\s*Agency for International Development', re.I)

def classify(slug, topic, title):
    fp = os.path.join(ROOT, "blog", slug, "index.html")
    body_txt = ""
    if os.path.exists(fp):
        h = open(fp, encoding='utf-8').read()
        m = re.search(r'<h1 class="article-title">(.*?)<section class="related-wrap"', h, re.S)
        seg = m.group(1) if m else h
        body_txt = _html.unescape(re.sub('<[^>]+>', ' ', seg))
    text = title + " " + body_txt
    tl = title.lower(); txt_l = text.lower()

    # ---- country: weighted (title x3) count, highest wins, else Global ----
    title_c = USAID_NOISE.sub(' ', title)
    body_c = USAID_NOISE.sub(' ', body_txt)
    cc = Counter()
    for canon, pats in COUNTRIES.items():
        for p in pats:
            n_title = len(re.findall(r'\b' + re.escape(p), title_c, re.I))
            n_body = len(re.findall(r'\b' + re.escape(p), body_c, re.I))
            cc[canon] += n_title * 3 + n_body
    cc = {k: v for k, v in cc.items() if v > 0}
    if 'Niger' in cc and 'Nigeria' in cc:   # de-overlap safety
        pass
    country = max(cc, key=cc.get) if cc else 'Global'

    # ---- product ----
    if 'sureadhere' in txt_l or topic == 'SureAdhere':
        product = 'SureAdhere'
    elif topic == 'Connect' or 'commcare connect' in txt_l or re.search(r'\bconnect\b', tl):
        product = 'Connect'
    elif 'open chat studio' in txt_l:
        product = 'Open Chat Studio'
    elif topic == 'CommCare' or txt_l.count('commcare') >= 2:
        product = 'CommCare'
    else:
        product = ''   # general/company post: only shows under Product=All

    # ---- type ----
    if 'case study' in tl or topic in ('Community Health',) and 'case study' in txt_l:
        ctype = 'Case Study'
    elif 'case study' in tl:
        ctype = 'Case Study'
    elif topic == 'Events' or any(k in tl for k in ['summit','forum','conference','webinar','gdhf','ict4d','enterprise summit']):
        ctype = 'Event'
    elif any(k in tl for k in ['announc','partner','launch','grant','award','receives','pledge','funding','acquires','named','selected','inc. 5000','inc 5000','climate neutral','certified','renews','commitment']):
        ctype = 'Announcement'
    elif topic == 'Research' or any(k in tl for k in ['research','study','evaluation','trial','analytics','predictive','price sensitivity']):
        ctype = 'Research'
    elif any(k in tl for k in ['introducing','new ','update','fall 20','spring 20','product','feature','case list','fhir','explorer','data lives','eu cloud']):
        ctype = 'Product Update'
    else:
        ctype = 'Perspective'

    # A country-specific post about a product, not already an event/announcement/etc.,
    # is in practice a case study / project profile.
    if ctype == 'Perspective' and country != 'Global' and product in ('CommCare', 'Connect', 'SureAdhere'):
        ctype = 'Case Study'

    return product, ctype, topic, country

rows = []
for slug, topic, title in cards:
    p, t, top, c = classify(slug, topic, title)
    rows.append((slug, p, t, top, c))

def dist(i, name):
    c = Counter(r[i] for r in rows)
    print(f"\n== {name} ({len([r for r in rows if r[i]])}/{len(rows)} tagged) ==")
    for k, n in c.most_common():
        print(f"   {n:3d}  {k or '(none)'}")

print(f"classified {len(rows)} cards")
dist(1, "PRODUCT"); dist(2, "TYPE"); dist(3, "TOPIC"); dist(4, "COUNTRY")

if not APPLY:
    print("\n(dry run — pass --apply to write)")
    sys.exit(0)

# ---------------- APPLY ----------------
tagmap = {r[0]: r[1:] for r in rows}  # slug -> (product, type, topic, country)

def card_attrs(m):
    p, t, top, c = tagmap[m.group('slug')]
    a = []
    if p: a.append(f'data-product="{p}"')
    a += [f'data-type="{t}"', f'data-topic="{top}"', f'data-country="{c}"']
    return f'<article class="blog-card" {" ".join(a)}>' + m.group('after')

new_idx = re.sub(
    r'<article class="blog-card"[^>]*>(?P<after>\s*<a class="blog-card-image" href="(?P<slug>[^"/]+)/index\.html")',
    card_attrs, idx)

def row(label, dim, values):
    chips = [f'          <button type="button" class="blog-filter is-active" data-dim="{dim}" data-filter="all" aria-pressed="true">All</button>']
    for v in values:
        chips.append(f'          <button type="button" class="blog-filter" data-dim="{dim}" data-filter="{v}" aria-pressed="false">{v}</button>')
    return ('        <div class="filter-row">\n'
            f'          <span class="filter-label">{label}</span>\n'
            '          <div class="filter-chips">\n' + "\n".join(chips) + "\n"
            '          </div>\n        </div>')

PRODUCTS = [p for p in ['CommCare','Connect','SureAdhere','Open Chat Studio'] if p in Counter(r[1] for r in rows)]
TYPES = [t for t in ['Case Study','Announcement','Product Update','Event','Research','Perspective'] if t in Counter(r[2] for r in rows)]
TOPICS = ['CommCare','Connect','SureAdhere','AI for Good','Global Health','Community Health','Maternal &amp; Child Health','Events','Research','Company']
ccount = Counter(r[4] for r in rows)
COUNTRY_CHIPS = ['Global'] + [c for c, n in ccount.most_common() if n >= 3 and c != 'Global']

filters_html = ('      <div class="blog-filters" role="group" aria-label="Filter posts">\n'
                + "\n".join([row('Product','product',PRODUCTS),
                             row('Type','type',TYPES),
                             row('Topic','topic',TOPICS),
                             row('Country','country',COUNTRY_CHIPS)])
                + '\n      </div>')

new_idx = re.sub(r'<div class="blog-filters".*</div>\s*(?=<div class="blog-grid")',
                 filters_html + '\n\n      ', new_idx, flags=re.S, count=1)

open(IDX, 'w', encoding='utf-8').write(new_idx)
print(f"\nAPPLIED: tagged {len(rows)} cards; filter rows -> Product{PRODUCTS} Type{TYPES} Country{COUNTRY_CHIPS}")
