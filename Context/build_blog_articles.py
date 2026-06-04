#!/usr/bin/env python3
"""Build Dimagi blog article pages from the WordPress export for the in-scope
posts (2023+, not already imported, excluding the Commcare Provider directory).

Renders each post into the existing blog article template:
head/SEO/JSON-LD, hero (breadcrumb + category + deck + byline + share), cover,
prose body (cleaned WP block markup, anchored H2s), optional TOC, end-CTA,
filed-under tags, related cards, footer, scripts.

Usage:
    python3 build_blog_articles.py --list                 # print the 52 targets
    python3 build_blog_articles.py --slugs a,b,c          # build only these
    python3 build_blog_articles.py --all                  # build all 52
Writes:  blog/<slug>/index.html   and a manifest to Context/blog_build_manifest.json
Does NOT touch blog/index.html (the listing) — that's a separate step.
"""
import xml.etree.ElementTree as ET
import json, os, re, html, sys, argparse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORT = os.path.join(HERE, "Full Wordpress Export - June 3 2026.xml")
BLOG = os.path.join(ROOT, "blog")

def ln(t): return t.split('}')[-1]

# ---------------------------------------------------------------- parse export
def parse_export():
    authors = {}      # login -> display
    posts = {}        # slug -> dict
    thumb = {}        # post_id -> thumb attachment id
    att = {}          # attachment_id -> url
    pid2slug = {}
    for ev, el in ET.iterparse(EXPORT, events=("end",)):
        tag = ln(el.tag)
        if tag == 'author':
            login = disp = None
            for ch in el:
                if ln(ch.tag) == 'author_login': login = ch.text
                elif ln(ch.tag) == 'author_display_name': disp = ch.text
            if login: authors[login] = disp
            el.clear()
        elif tag == 'item':
            d = {'cats': [], 'tags': []}
            pid = tid = aurl = None
            for ch in el:
                t = ln(ch.tag); txt = ch.text or ''
                if t == 'post_id': pid = txt
                elif t == 'post_type': d['type'] = txt
                elif t == 'status': d['status'] = txt
                elif t == 'title': d['title'] = txt
                elif t == 'post_name': d['slug'] = txt
                elif t == 'post_date': d['date'] = txt
                elif t == 'creator': d['author_login'] = txt
                elif t == 'attachment_url': aurl = txt
                elif t == 'encoded' and ch.tag.endswith('}encoded'):
                    if 'content' in ch.tag: d['content'] = txt
                    else: d['excerpt'] = txt
                elif t == 'category':
                    dom = ch.get('domain')
                    if dom == 'category': d['cats'].append(txt or '')
                    elif dom == 'post_tag': d['tags'].append(txt or '')
                elif t == 'postmeta':
                    k = v = None
                    for mc in ch:
                        if ln(mc.tag) == 'meta_key': k = mc.text
                        elif ln(mc.tag) == 'meta_value': v = mc.text
                    if k == '_thumbnail_id': tid = v
            if d.get('type') == 'attachment' and aurl: att[pid] = aurl
            if d.get('type') == 'post':
                pid2slug[pid] = d.get('slug')
                if tid: thumb[pid] = tid
                d['_pid'] = pid
                if d.get('status') == 'publish' and d.get('slug'):
                    posts[d['slug']] = d
            el.clear()
    # resolve cover urls
    slug2pid = {v: k for k, v in pid2slug.items()}
    for slug, d in posts.items():
        pid = d.get('_pid')
        tid = thumb.get(pid)
        d['cover_url'] = att.get(tid) if tid else None
    return authors, posts

# ---------------------------------------------------------------- target set
def targets(posts):
    imported = set(x for x in os.listdir(BLOG) if os.path.isdir(os.path.join(BLOG, x)))
    out = []
    for slug, d in posts.items():
        if slug in imported: continue
        if d['date'] < '2023-01-01': continue
        if d['cats'] == ['Commcare Provider']: continue
        out.append(d)
    out.sort(key=lambda d: d['date'], reverse=True)
    return out

# ---------------------------------------------------------------- helpers
def author_name(login, authors):
    disp = authors.get(login) or login or 'Dimagi'
    # a display name with no space & all-lowercase is really a username -> Dimagi
    if disp and (' ' not in disp) and disp.islower():
        return 'Dimagi'
    if disp in ('admin', 'Guest Blog'): return 'Dimagi'
    # strip trailing ", Title at Org"
    return disp.split(',')[0].strip()

def initials(name):
    parts = [p for p in re.split(r'\s+', name.strip()) if p]
    if not parts: return 'D'
    if len(parts) == 1: return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

def month_year(iso): return datetime.strptime(iso[:10], "%Y-%m-%d").strftime("%b %Y")

def slugify(text):
    s = re.sub(r'<[^>]+>', '', text)
    s = html.unescape(s).lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s[:50] or 'section'

def text_only(h): return html.unescape(re.sub(r'<[^>]+>', '', h or ''))

# ---------------------------------------------------------------- content clean
def clean_body(raw):
    """WP block markup -> clean prose HTML; returns (html, [(anchor,label),...])."""
    s = raw or ''
    # drop WP block comments
    s = re.sub(r'<!--\s*/?wp:[^>]*?-->', '', s)
    # drop other HTML comments
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    # strip wp-block-* embeds/buttons/columns wrappers we can't render well
    s = re.sub(r'<figure class="wp-block-embed[^>]*>.*?</figure>', '', s, flags=re.S)
    s = re.sub(r'<div class="wp-block-buttons[^>]*>.*?</div>', '', s, flags=re.S)
    # unwrap simple column/group wrappers
    s = re.sub(r'</?div[^>]*class="wp-block-(group|columns|column)[^"]*"[^>]*>', '', s)
    # clean attributes that leak WP styling
    s = re.sub(r'\sclass="[^"]*wp-[^"]*"', '', s)
    s = re.sub(r'\s(srcset|sizes|data-[\w-]+)="[^"]*"', '', s)
    s = re.sub(r'\sid="[^"]*"', '', s)  # we re-add our own h2 ids
    # images: ensure lazy + decoding
    def fiximg(m):
        tag = m.group(0)
        if 'loading=' not in tag: tag = tag[:-1] + ' loading="lazy" decoding="async">'
        return tag
    s = re.sub(r'<img\b[^>]*>', fiximg, s)
    # external links: open in new tab
    def fixa(m):
        tag = m.group(0)
        if 'href="http' in tag and 'dimagi.com' not in tag and 'target=' not in tag:
            tag = tag[:-1] + ' target="_blank" rel="noopener">'
        return tag
    s = re.sub(r'<a\b[^>]*>', fixa, s)
    # add ids to h2 + collect toc
    toc = []
    def h2(m):
        inner = m.group(1)
        a = slugify(inner)
        label = text_only(inner)
        if len(label) > 24: label = label[:22].rstrip() + '…'
        toc.append((a, label))
        return f'<h2 id="{a}">{inner}</h2>'
    s = re.sub(r'<h2[^>]*>(.*?)</h2>', h2, s, flags=re.S)
    # demote any h1 in body to h2; keep h3/h4
    s = re.sub(r'<(/?)h1\b', r'<\1h2', s)
    # remove empty paragraphs / leftover whitespace blocks
    s = re.sub(r'<p>\s*(&nbsp;)?\s*</p>', '', s)
    s = re.sub(r'\n{3,}', '\n\n', s).strip()
    # mark the first paragraph as lead
    s = re.sub(r'<p>', '<p class="lead">', s, count=1) if s.startswith('<p>') else s
    return s, toc

def make_deck(d):
    ex = text_only(d.get('excerpt', '')).strip()
    if ex:
        return ex if len(ex) <= 200 else ex[:197].rstrip() + '…'
    body = text_only(re.sub(r'<!--.*?-->', '', d.get('content', ''), flags=re.S))
    body = re.sub(r'\s+', ' ', body).strip()
    cut = body[:200]
    p = cut.rfind('. ')
    return (cut[:p+1] if p > 80 else cut.rstrip() + '…')

def read_time(content):
    words = len(re.findall(r'\w+', text_only(content)))
    return max(1, round(words / 200))

# ---------------------------------------------------------------- classify
COUNTRIES = ["United States","Burkina Faso","Ethiopia","Guatemala","India","Kenya",
    "Mozambique","Nigeria","Senegal","Zimbabwe","Madagascar","Guinea","Ghana","Zambia",
    "Malawi","Tanzania","Uganda","Vermont","Arizona","Pima County","Somerville","Martha"]
US_HINTS = ["Vermont","Arizona","Pima County","Somerville","Martha","United States","U.S.","Massachusetts"]

def classify(d):
    title = html.unescape(d.get('title','')); body = text_only(d.get('content',''))
    cats = [c.lower() for c in d['cats']]; tags=[t.lower() for t in d['tags']]
    blob = (title + ' ' + ' '.join(d['cats']) + ' ' + ' '.join(d['tags'])).lower()
    full = (title + ' ' + body).lower()
    # product
    if 'sureadhere' in blob: product='SureAdhere'
    elif 'open chat studio' in full or 'catscoach' in full: product='Open Chat Studio'
    elif 'commcare connect' in full or re.search(r'\bconnect\b', title.lower()): product='Connect'
    elif any(k in full for k in ['year in review','enterprise summit','inc. 5000','inc 5000',
            'career journey','day in the life','as an intern','grand challenges','partnership',
            'announce','davos','spotlight','researcher spotlight','our culture','dimagi makes']):
        product='Dimagi (General)'
    else: product='CommCare'
    # type
    if 'case study' in title.lower() or 'case-study' in '-'.join(cats) or 'case study' in cats:
        typ='Case Study'
    elif any(k in full for k in ['summit','conference','recap','gdhf','ict4d','exhibit','webinar','forum']) \
         and any(k in title.lower() for k in ['summit','conference','recap','gtd','ict4d','exhibit','forum','join','at the']):
        typ='Events'
    else: typ='News'
    # topic
    def has(*ks): return any(k in full for k in ks)
    if has('case management'): topic='Case Management'
    elif has('data collection','offline data','mobile data','no-code','no code'): topic='Data Collection'
    elif has('malnutrition','nutrition'): topic='Nutrition'
    elif has('malaria','immuniz','vaccin','polio'): topic='Immunization'
    elif has('mental health','resilience','burnout','wellme'): topic='Mental Health'
    elif has('agricultur','livelihood','poultry','farmer'): topic='Agriculture'
    elif has('community health worker','chw','community health'): topic='Community Health'
    elif has('maternal','child health','newborn','early childhood'): topic='Maternal & Child Health'
    elif has('artificial intelligence',' ai ','large language','machine learning'): topic='AI for Good'
    elif has('career','day in the life','intern','culture','employee'): topic='Careers'
    elif has('usaid','funding','global development','impact delivery'): topic='Global Health'
    elif has('violence'): topic='Community Health'
    elif product=='Dimagi (General)': topic='Company News'
    else: topic='Global Health'
    # country
    country=None
    counts={}
    for c in COUNTRIES:
        n=len(re.findall(re.escape(c), title+' '+body))
        if n: counts[c]=n
    if counts:
        top=max(counts, key=counts.get)
        if top in US_HINTS: country='United States'
        elif top in ('Guinea','Ghana','Zambia','Malawi','Tanzania','Uganda','Madagascar',
                     'Kenya','Nigeria','Mozambique','Senegal','Zimbabwe','Ethiopia','India',
                     'Guatemala','Burkina Faso'):
            country=top
    return product, typ, topic, country

# ---------------------------------------------------------------- render
def esc(s, quote=True): return html.escape(s or '', quote=quote)

def render(d, authors, related):
    slug = d['slug']
    title = html.unescape(d['title'])
    product, typ, topic, country = classify(d)
    author = author_name(d.get('author_login'), authors)
    body, toc = clean_body(d.get('content',''))
    deck = make_deck(d)
    rt = read_time(d.get('content',''))
    my = month_year(d['date'])
    cover_url = d.get('cover_url') or ''
    ext = os.path.splitext(cover_url.split('?')[0])[1].lower() or '.jpg'
    if ext not in ('.jpg','.jpeg','.png','.webp'): ext='.jpg'
    cover_local = f"../../assets/images/{slug}/cover{ext}"
    canonical = f"https://dimagi.com/{slug}/"
    tagset = [t for t in [product, typ, topic, country] if t]
    # tags markup
    tags_html = '\n            '.join(f'<span class="article-tag">{esc(t)}</span>' for t in tagset)
    # toc markup (only if >=2 sections)
    toc_html = ''
    if len(toc) >= 2:
        links = '\n          '.join(f'<a href="#{a}">{esc(l)}</a>' for a,l in toc[:6])
        toc_html = f'''
      <aside class="article-toc" aria-label="Table of contents">
        <p class="article-toc-label">On this page</p>
        <nav>
          {links}
        </nav>
      </aside>'''
    # related cards
    rel_html = '\n\n'.join(related_card(r) for r in related)
    enc_url = canonical.replace(':','%3A').replace('/','%2F')
    enc_title = title.replace(' ','%20').replace('&','%26')
    fields = dict(
        title=esc(title), desc=esc(deck), author=esc(author), canonical=canonical,
        cover_url=esc(cover_url), date=d['date'][:10], section=esc(product),
        topic_tag=esc(topic), my=my, rt=str(rt), deck=esc(deck), product=esc(product),
        initials=initials(author), cover_local=cover_local, alt=esc(title),
        body=body, tags_html=tags_html, toc_html=toc_html, rel_html=rel_html,
        enc_url=enc_url, enc_title=enc_title, headline=esc(title, quote=False),
        kw=esc(', '.join(tagset)))
    out = TEMPLATE
    for k, v in fields.items():
        out = out.replace('[[' + k + ']]', v)
    return out

def related_card(r):
    return f'''        <a class="related-card" href="../{r['slug']}/index.html">
          <div class="related-card-thumb">
            <img src="../../assets/images/{r['slug']}/cover{r['ext']}" alt="{esc(r['title'])}" loading="lazy" decoding="async">
          </div>
          <div class="related-card-body">
            <div class="related-card-cat">{esc(r['product'])}</div>
            <h3 class="related-card-title">{esc(r['title'])}</h3>
            <div class="related-card-footer">
              <span class="related-card-date">{r['my']}</span>
              <span class="related-card-link">Read</span>
            </div>
          </div>
        </a>'''

# template is loaded from a sibling file to keep this script readable
with open(os.path.join(HERE, "blog_article_template.html"), encoding="utf-8") as fh:
    TEMPLATE = fh.read()

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--slugs', default='')
    args = ap.parse_args()
    authors, posts = parse_export()
    tgt = targets(posts)
    if args.list:
        for d in tgt:
            p,t,tp,c = classify(d)
            print(f"{d['date'][:10]} | {p:16} | {t:10} | {tp:20} | {c or '-':14} | {html.unescape(d['title'])[:55]}")
        print(f"\nTOTAL {len(tgt)}")
        return
    sel = tgt
    if args.slugs:
        want = set(args.slugs.split(','))
        sel = [d for d in tgt if d['slug'] in want]
    elif not args.all:
        sel = tgt[:3]
    # build a lookup for related cards (all targets + a few existing)
    def rel_meta(d):
        p,t,tp,c = classify(d)
        cu = d.get('cover_url') or ''
        ext = os.path.splitext(cu.split('?')[0])[1].lower()
        if ext not in ('.jpg','.jpeg','.png','.webp'): ext='.jpg'
        return {'slug':d['slug'],'title':html.unescape(d['title']),'product':p,
                'topic':tp,'my':month_year(d['date']),'ext':ext,'date':d['date']}
    metas = [rel_meta(d) for d in tgt]
    by_slug = {m['slug']:m for m in metas}
    manifest = []
    for d in sel:
        me = by_slug[d['slug']]
        # related = up to 3 others sharing topic, else most recent
        same = [m for m in metas if m['slug']!=d['slug'] and m['topic']==me['topic']]
        pool = same + [m for m in metas if m['slug']!=d['slug'] and m not in same]
        related = pool[:3]
        page = render(d, authors, related)
        outdir = os.path.join(BLOG, d['slug'])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir,'index.html'),'w',encoding='utf-8') as fh:
            fh.write(page)
        p,t,tp,c = classify(d)
        manifest.append({'slug':d['slug'],'title':html.unescape(d['title']),'date':d['date'][:10],
            'product':p,'type':t,'topic':tp,'country':c,'cover_url':d.get('cover_url'),
            'ext':me['ext'],'deck':make_deck(d),'my':month_year(d['date'])})
        print("built", d['slug'])
    json.dump(manifest, open(os.path.join(HERE,'blog_build_manifest.json'),'w'), indent=1)
    print(f"\n{len(manifest)} pages built; manifest -> Context/blog_build_manifest.json")

if __name__ == '__main__':
    main()
