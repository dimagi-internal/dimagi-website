# Central render: consume per-post JSON records written by workflow agents,
# compute related-card cross-links, render each new article page via gen.py's build(),
# then regenerate blog/index.html's filter chips + grid from a full disk scan.
import json, os, re, glob, subprocess, html as _html

exec(open('/tmp/gen.py').read())  # gives build(), render(), ROOT, esc()

BLOG = os.path.join(ROOT, "blog")
IMPORT_DIR = "/tmp/blog_import"

def b_label(iso):
    # 2024-11-22 -> "Nov 2024"
    import datetime
    return datetime.date(*map(int, iso[:10].split('-'))).strftime("%b %Y")

# ---------- 1. load new records ----------
records = {}
for fp in glob.glob(os.path.join(IMPORT_DIR, "*.json")):
    r = json.load(open(fp))
    records[r['slug']] = r

# ---------- 2. parse an existing page into a registry entry ----------
def parse_page(slug):
    fp = os.path.join(BLOG, slug, "index.html")
    s = open(fp, encoding='utf-8').read()
    def g(pat, d=''):
        m = re.search(pat, s, re.S)
        return m.group(1).strip() if m else d
    title = g(r'<h1 class="article-title">(.*?)</h1>')
    cat = g(r'<span class="article-category">(.*?)</span>')
    iso = g(r'article:published_time" content="([^"]+)"')[:10]
    desc = g(r'<meta name="description" content="([^"]*)"')
    fig = g(r'<figure class="article-cover"[^>]*>(.*?)</figure>')
    src = re.search(r'src="([^"]+)"', fig)
    w = re.search(r'width="(\d+)"', fig)
    h = re.search(r'height="(\d+)"', fig)
    coverfile = os.path.basename(src.group(1)) if src else None
    cw = int(w.group(1)) if w else 1200
    ch = int(h.group(1)) if h else 750
    return dict(slug=slug, title=title, cat=cat, iso=iso, desc=desc,
                coverfile=coverfile, cw=cw, ch=ch)

# ---------- 3. build full registry (existing on disk + new records) ----------
registry = {}
existing = [d for d in os.listdir(BLOG)
            if os.path.isdir(os.path.join(BLOG, d))
            and os.path.exists(os.path.join(BLOG, d, "index.html"))]
for slug in existing:
    if slug in records:   # will be (re)written by this run; use record values below
        continue
    registry[slug] = parse_page(slug)
for slug, r in records.items():
    registry[slug] = dict(slug=slug, title=r['h1'], cat=r['category'],
                          iso=r['date'][:10], desc=r['desc'],
                          coverfile=r['cover'], cw=r['coverw'], ch=r['coverh'])

# ---------- 4. related-card chooser ----------
def related_for(slug):
    me = registry[slug]
    others = [e for s, e in registry.items() if s != slug]
    same = sorted([e for e in others if e['cat'] == me['cat']],
                  key=lambda e: e['iso'], reverse=True)
    rest = sorted([e for e in others if e['cat'] != me['cat']],
                  key=lambda e: e['iso'], reverse=True)
    pick = (same + rest)[:3]
    out = []
    for e in pick:
        out.append(dict(
            href=f"../{e['slug']}/index.html",
            img=f"../../assets/images/{e['slug']}/{e['coverfile']}",
            w=e['cw'], h=e['ch'], cat=e['cat'], title=e['title'],
            date=b_label(e['iso']),
            alt=re.sub('<[^>]+>', '', e['title'])))
    return out

# ---------- 5. render each new page ----------
n = 0
for slug, r in records.items():
    p = dict(r)
    p['related'] = related_for(slug)
    toc = r.get('toc') or []
    p['toc'] = [tuple(x) for x in toc] if len(toc) >= 3 else []
    p.setdefault('crumb', p['category'])
    render(p)
    n += 1
print(f"rendered {n} new article pages")

# ---------- 6. regenerate listing (filters + grid) from full disk scan ----------
all_slugs = [d for d in os.listdir(BLOG)
             if os.path.isdir(os.path.join(BLOG, d))
             and os.path.exists(os.path.join(BLOG, d, "index.html"))]
cards = []
cats_present = {}
for slug in all_slugs:
    e = registry.get(slug) or parse_page(slug)
    cats_present[e['cat']] = cats_present.get(e['cat'], 0) + 1
    cards.append(e)
cards.sort(key=lambda e: e['iso'], reverse=True)

PREF = ["CommCare", "Connect", "SureAdhere", "AI for Good", "Global Health",
        "Community Health", "Maternal &amp; Child Health", "Events",
        "Research", "Company"]
ordered = [c for c in PREF if c in cats_present] + \
          [c for c in sorted(cats_present) if c not in PREF]

fbtns = ['        <button type="button" class="blog-filter is-active" data-filter="all" aria-pressed="true">All</button>']
for c in ordered:
    fbtns.append(f'        <button type="button" class="blog-filter" data-filter="{c}" aria-pressed="false">{c}</button>')
filters_html = ('      <div class="blog-filters" role="group" aria-label="Filter posts by category">\n'
                + "\n".join(fbtns) + "\n      </div>")

def card_html(e):
    img = f"../assets/images/{e['slug']}/{e['coverfile']}"
    alt = re.sub('<[^>]+>', '', e['title'])
    href = f"{e['slug']}/index.html"
    return f'''        <article class="blog-card">
          <a class="blog-card-image" href="{href}">
            <img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async">
          </a>
          <div class="blog-card-body">
            <div class="blog-card-category">{e['cat']}</div>
            <h2 class="blog-card-title">{e['title']}</h2>
            <p class="blog-card-desc">{e['desc']}</p>
            <div class="blog-card-footer">
              <span class="blog-card-date">{b_label(e['iso'])}</span>
              <a class="blog-card-link" href="{href}">Read more</a>
            </div>
          </div>
        </article>'''

grid_html = '      <div class="blog-grid">\n\n' + "\n\n".join(card_html(e) for e in cards) + "\n\n      </div>"

idx_fp = os.path.join(BLOG, "index.html")
s = open(idx_fp, encoding='utf-8').read()
i1 = s.index('<div class="blog-filters"')
i1 = s.rfind('\n', 0, i1) + 1            # back up to start of the indented line
i2 = s.index('<div class="blog-more"')
i2 = s.rfind('\n', 0, i2) + 1
new = s[:i1] + filters_html + "\n\n" + grid_html + "\n\n      " + s[i2:]
open(idx_fp, 'w', encoding='utf-8').write(new)
print(f"regenerated listing: {len(cards)} cards, categories: {ordered}")
