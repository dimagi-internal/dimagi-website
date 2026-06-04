#!/usr/bin/env python3
"""Build editorial JSON records for the genuinely-remaining blog posts and drop
them in /tmp/blog_import/ so the existing render_all.py can render pages + rebuild
the index consistently. Also downloads each cover to assets/images/<slug>/.

Excludes: posts already imported (slug or title match), the 17 'Commcare Provider'
directory stubs, and French-language posts.

    python3 build_remaining_records.py --list     # show importable set
    python3 build_remaining_records.py --build     # write records + download covers
"""
import importlib.util, os, re, html, json, sys, struct, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)                     # Context/
ROOT = os.path.dirname(PARENT)                     # project root
spec = importlib.util.spec_from_file_location("bb", os.path.join(PARENT, "build_blog_articles.py"))
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)
BLOG = os.path.join(ROOT, "blog")
IMPORT_DIR = "/tmp/blog_import"
IMG_ROOT = os.path.join(ROOT, "assets", "images")

# ---- which posts are already imported (slug or fuzzy title) ----
def norm(t):
    t = html.unescape(t or '').lower(); t = re.sub(r'[^a-z0-9 ]', '', t); return re.sub(r'\s+', ' ', t).strip()

def imported_index():
    slugs = set(); titles = {}
    for d in os.listdir(BLOG):
        p = os.path.join(BLOG, d, "index.html")
        if not os.path.isfile(p): continue
        slugs.add(d)
        h = open(p, encoding='utf-8', errors='ignore').read()
        m = re.search(r'<h1[^>]*article-title[^>]*>(.*?)</h1>', h, re.S) or re.search(r'<title>(.*?)</title>', h, re.S)
        if m: titles[norm(re.sub(r'\s*\|\s*Dimagi', '', m.group(1)))] = d
    return slugs, titles

FRENCH = re.compile(r'\b(numériques?|choisit|centrée|modèles|outils|pour soutenir|prendre en charge|développer|riposte)\b', re.I)

def importable():
    authors, posts = bb.parse_export()
    slugs, titles = imported_index()
    out = []
    for d in posts.values():
        if d['slug'] in slugs: continue
        nt = norm(d['title'])
        if any(nt == it or (len(nt) > 20 and (nt in it or it in nt)) for it in titles): continue
        if d['cats'] == ['Commcare Provider']: continue
        if FRENCH.search(html.unescape(d['title'])): continue
        out.append(d)
    out.sort(key=lambda d: d['date'], reverse=True)
    return authors, out

# ---- single-category classification (matches live filter chip set) ----
def category_for(d):
    slug = d['slug']; title = html.unescape(d['title']).lower()
    if re.search(r'career journey|day in the life|as an intern|life of -|life of\b', title): return 'Company'
    if 'researcher spotlight' in title: return 'Research'
    if 'namaste' in slug or 'neurodevelopment' in title or 'autism' in title: return 'Community Health'
    if 'provider program' in title or 'provider profile' in title or 'oikoi' in slug: return 'CommCare'
    return 'CommCare'   # how-to / case-management / data-collection guides

CTA = {
    'Company': {"h3": "Build your career at Dimagi", "p": "We're hiring people who want to use technology to amplify frontline impact.", "btntext": "See open roles", "btnhref": "../../company/careers/index.html"},
    'Research': {"h3": "Explore our research", "p": "See how Dimagi partners with researchers to generate evidence on what works for frontline programs.", "btntext": "Research & Data", "btnhref": "../../professional-services/research-data/index.html"},
    'Community Health': {"h3": "See CommCare in action", "p": "Find out how teams use CommCare to deliver and monitor community health programs at scale.", "btntext": "Get in touch", "btnhref": "../../contact/index.html"},
    'CommCare': {"h3": "See what CommCare can do", "p": "Explore how CommCare helps frontline teams collect data, manage cases, and scale their impact.", "btntext": "Get in touch", "btnhref": "../../contact/index.html"},
}

def img_dims(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    if head[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', head[16:24]); return w, h
    if head[:2] == b'\xff\xd8':  # jpeg: scan SOF
        with open(path, 'rb') as f:
            f.read(2); b = f.read(1)
            while b and b != b'':
                while b != b'\xff': b = f.read(1)
                marker = f.read(1)
                if marker in (b'\xc0', b'\xc1', b'\xc2', b'\xc3'):
                    f.read(3); h, w = struct.unpack('>HH', f.read(4)); return w, h
                seg = f.read(2)
                if len(seg) < 2: break
                f.read(struct.unpack('>H', seg)[0] - 2); b = f.read(1)
    return 1200, 630

def download_cover(slug, url):
    if not url: return None, 1200, 630
    ext = os.path.splitext(url.split('?')[0])[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'): ext = '.jpg'
    d = os.path.join(IMG_ROOT, slug); os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, "cover" + ext)
    subprocess.run(["curl", "-sL", "--max-time", "40", "-o", dest, url], check=False)
    if not os.path.isfile(dest) or os.path.getsize(dest) < 1000:
        return None, 1200, 630
    w, h = img_dims(dest)
    return "cover" + ext, w, h

def indent(body, n=8):
    pad = ' ' * n
    return '\n'.join((pad + ln if ln.strip() else ln) for ln in body.split('\n'))

def make_record(d, authors, download=True):
    slug = d['slug']; title = html.unescape(d['title']).strip()
    cat = category_for(d)
    author = bb.author_name(d.get('author_login'), authors)
    body, toc = bb.clean_body(d.get('content', ''))
    deck = bb.make_deck(d)
    cover_url = d.get('cover_url') or ''
    if download:
        cov, cw, ch = download_cover(slug, cover_url)
    else:
        cov, cw, ch = "cover.jpg", 1200, 630
    if not cov: cov, cw, ch = "cover.jpg", 1200, 630
    tags = [cat] + [t for t in (d.get('tags') or []) if t and t.lower() != cat.lower()][:2]
    if len(tags) == 1:
        tags += ['CommCare'] if cat != 'CommCare' else ['Frontline Workers']
    rec = {
        "slug": slug, "h1": title, "titletag": f"{title} | Dimagi", "ogtitle": title,
        "desc": deck, "deck": deck, "date": d['date'][:10],
        "datelabel": bb.month_year(d['date']), "author": author,
        "initials": bb.initials(author), "category": cat, "crumb": cat,
        "readtime": f"{bb.read_time(d.get('content',''))} min read",
        "cover": cov, "coverw": cw, "coverh": ch,
        "coveralt": title, "ogimage": cover_url or f"https://dimagi.com/assets/images/{slug}/{cov}",
        "ogw": cw, "ogh": ch, "ogalt": title,
        "keywords": ", ".join(tags), "body": indent(body),
        "toc": toc if len(toc) >= 3 else [], "tags": tags, "cta": CTA[cat],
    }
    return rec

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--list'
    authors, posts = importable()
    if mode == '--list':
        for d in posts:
            print(f"{d['date'][:10]} | {category_for(d):16} | {html.unescape(d['title'])[:60]}")
        print(f"\nIMPORTABLE: {len(posts)}")
        return
    os.makedirs(IMPORT_DIR, exist_ok=True)
    for d in posts:
        rec = make_record(d, authors, download=True)
        json.dump(rec, open(os.path.join(IMPORT_DIR, d['slug'] + ".json"), "w"), indent=1)
        print("record+cover:", d['slug'], f"({rec['cover']} {rec['coverw']}x{rec['coverh']})")
    print(f"\nwrote {len(posts)} records to {IMPORT_DIR}")

if __name__ == '__main__':
    main()
