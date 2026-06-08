# Reshape the blog filters per request:
#  - Product row merged into "Focus" (renamed from Topic), placed at the TOP of the filters:
#    Focus leads with the products, then thematic topics (Company, Ecosystem)
#  - Focus topics: keep only Company + Ecosystem (AI for Good dropped); removed topics -> None
#  - Country -> Geography (regions); Asian countries collapse to Asia, with India broken out; + None
# Re-runnable from the per-country export/regen state (cards carry per-country data-country).
# NOTE: the Focus row's single-select reset behaviour lives in blog/index.html's inline JS, not here.
import re, os
ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
IDX = os.path.join(ROOT, "blog", "index.html")

KEEP_TOPICS = {'Company', 'Ecosystem'}

COUNTRY2REGION = {
    'United States': 'United States',
    'India': 'India', 'Nepal': 'Asia', 'Tajikistan': 'Asia',
    'Cambodia': 'Asia', 'Indonesia': 'Asia', 'Vietnam': 'Asia',
    'Nigeria': 'Africa', 'Sierra Leone': 'Africa', 'Senegal': 'Africa',
    'Guinea': 'Africa', 'Ghana': 'Africa', 'Burkina Faso': 'Africa',
    'Niger': 'Africa', 'Benin': 'Africa', "Cote d'Ivoire": 'Africa',
    'Kenya': 'Africa', 'Ethiopia': 'Africa', 'Somalia': 'Africa',
    'Tanzania': 'Africa', 'Rwanda': 'Africa', 'Uganda': 'Africa',
    'South Africa': 'Africa', 'Malawi': 'Africa', 'Mozambique': 'Africa',
    'Zambia': 'Africa', 'Madagascar': 'Africa', 'Lesotho': 'Africa',
    'Mexico': 'Latin America', 'Jamaica': 'Latin America', 'Honduras': 'Latin America',
    'Global': 'None',
    # Region identity/merge keys: keep this script idempotent when re-run on the
    # already-regionalized state. West/East/Southern Africa all roll up to Africa.
    'West Africa': 'Africa', 'East Africa': 'Africa', 'Southern Africa': 'Africa',
    'Africa': 'Africa', 'Asia': 'Asia', 'Latin America': 'Latin America',
}

s = open(IDX, encoding='utf-8').read()

def retag(m):
    attrs = dict(re.findall(r'data-(\w+)="([^"]*)"', m.group(1)))
    product = attrs.get('product') or 'None'
    ctype = attrs.get('type') or 'None'
    topic = attrs.get('topic', '')
    topic = topic if topic in KEEP_TOPICS else 'None'
    geo = COUNTRY2REGION.get(attrs.get('country', ''), 'None')
    return (f'<article class="blog-card" data-product="{product}" data-type="{ctype}" '
            f'data-topic="{topic}" data-country="{geo}">')

s, n = re.subn(r'<article class="blog-card"([^>]*)>', retag, s)

def row(label, dim, values):
    chips = [f'          <button type="button" class="blog-filter is-active" data-dim="{dim}" data-filter="all" aria-pressed="true">All</button>']
    for v in values:
        chips.append(f'          <button type="button" class="blog-filter" data-dim="{dim}" data-filter="{v}" aria-pressed="false">{v}</button>')
    chips.append(f'          <button type="button" class="blog-filter" data-dim="{dim}" data-filter="None" aria-pressed="false">None</button>')
    return ('        <div class="filter-row">\n'
            f'          <span class="filter-label">{label}</span>\n'
            '          <div class="filter-chips">\n' + "\n".join(chips) + "\n"
            '          </div>\n        </div>')

PRODUCTS = ['CommCare', 'Connect', 'SureAdhere', 'Open Chat Studio']
TYPES = ['Case Study', 'Announcement', 'Product Update', 'Event', 'Research', 'Perspective']
TOPICS = ['Company', 'Ecosystem']
GEO = ['United States', 'Asia', 'India', 'Africa', 'Latin America']

def focus_row():
    # Merged "Focus" row at the top, exposed as ONE virtual 'focus' dimension that
    # blog/index.html's inline JS computes per card (its product if any, else a
    # Company/Ecosystem topic, else "None"). Products lead, then thematic topics, then
    # a "None" chip for posts with no product and no Focus topic.
    chips = ['          <button type="button" class="blog-filter is-active" data-dim="focus" data-filter="all" aria-pressed="true">All</button>']
    for v in PRODUCTS + TOPICS:
        chips.append(f'          <button type="button" class="blog-filter" data-dim="focus" data-filter="{v}" aria-pressed="false">{v}</button>')
    chips.append('          <button type="button" class="blog-filter" data-dim="focus" data-filter="None" aria-pressed="false">None</button>')
    return ('        <div class="filter-row">\n'
            '          <span class="filter-label">Focus</span>\n'
            '          <div class="filter-chips">\n' + "\n".join(chips) + "\n"
            '          </div>\n        </div>')

filters_html = ('      <div class="blog-filters" role="group" aria-label="Filter posts">\n'
                + "\n".join([focus_row(),
                             row('Type', 'type', TYPES),
                             row('Geography', 'country', GEO)])
                + '\n      </div>')

s = re.sub(r'<div class="blog-filters".*</div>\s*(?=<div class="blog-grid")',
           filters_html + '\n\n      ', s, flags=re.S, count=1)

open(IDX, 'w', encoding='utf-8').write(s)

# report distribution
from collections import Counter
def dist(dim):
    return Counter(re.findall(rf'data-{dim}="([^"]*)"', s))
print(f"retagged {n} cards")
for d in ['product', 'type', 'topic', 'country']:
    print(f"  {d}:", dict(dist(d)))
