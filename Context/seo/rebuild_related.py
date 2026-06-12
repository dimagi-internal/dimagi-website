#!/usr/bin/env python3
"""Rebuild the "More from the Dimagi blog" related-card grid on every blog
article to fix internal-link orphaning.

The original chooser (render_all.py related_for) always picked the 3 MOST RECENT
same-category articles, so older posts never appeared as anyone's related card.
Result: ~156 of 236 articles were orphans (0 inbound internal links) while a few
recent posts hoarded dozens. Orphaned pages get crawled and ranked worse.

This recomputes related cards by RELEVANCE (shared "Filed under" tags, weighted
by inverse document frequency, plus same category and date proximity) and then
balances inbound links so every article is linked from at least a few others.
It rewrites ONLY the contents of <div class="related-grid"> in each file.

Idempotent: same inputs produce the same grid. Run after any blog regen,
alongside trim_meta.py / apply_titles.py / transform_filters.py / apply_tag_pass.py.

Usage:
  python3 Context/seo/rebuild_related.py            # dry-run (orphan stats + sample)
  python3 Context/seo/rebuild_related.py --apply    # write changes
"""
import os, re, sys, glob, math, datetime, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BLOG = os.path.join(ROOT, "blog")
APPLY = "--apply" in sys.argv
N_CARDS = 3
POOL = 12          # consider this many most-relevant as the spreadable pool
MIN_INBOUND = 2    # repair pass lifts every article to at least this many inbound
                   # (dropping only cards that stay >= MIN_INBOUND, so no new orphans)

def g(pat, s, d=""):
    m = re.search(pat, s, re.S)
    return m.group(1).strip() if m else d

def load():
    arts = {}
    for fp in sorted(glob.glob(os.path.join(BLOG, "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(fp))
        if slug == "author":
            continue
        s = open(fp, encoding="utf-8").read()
        # skip noindex redirect stubs (meta-refresh to a consolidated post):
        # never use them as related-card sources, targets, or orphan candidates
        if 'http-equiv="refresh"' in s or "location.replace(" in s:
            continue
        title = g(r'<meta property="og:title" content="([^"]*)"', s) \
            or g(r'<h1 class="article-title">(.*?)</h1>', s)
        cat = g(r'<meta property="article:section" content="([^"]*)"', s, "Blog")
        iso = g(r'<meta property="article:published_time" content="([^"]*)"', s)[:10]
        tags = re.findall(r'<span class="article-tag">([^<]+)</span>', s)
        cov = g(r'<figure class="article-cover"[^>]*>\s*<img\b(.*?)>', s)
        csrc = g(r'src="([^"]*)"', cov)
        cbase = os.path.basename(csrc) if csrc else "cover.jpg"
        cw = g(r'width="(\d+)"', cov, "1200")
        ch = g(r'height="(\d+)"', cov, "800")
        try:
            label = datetime.datetime.strptime(iso, "%Y-%m-%d").strftime("%b %Y")
            order = iso
        except ValueError:
            label, order = "", "0000-00-00"
        arts[slug] = dict(slug=slug, fp=fp, title=title, cat=cat, iso=order,
                          label=label, tags=set(tags), cw=cw, ch=ch, cbase=cbase, src=s)
    return arts

def main():
    arts = load()
    slugs = list(arts)

    # inverse-document-frequency weight per tag (rare tags matter more)
    df = collections.Counter()
    for a in arts.values():
        for t in a["tags"]:
            df[t] += 1
    n = len(arts)
    idf = {t: math.log(1 + n / c) for t, c in df.items()}

    def rel(a, b):
        shared = a["tags"] & b["tags"]
        score = 3.0 * sum(idf[t] for t in shared)
        if a["cat"] == b["cat"]:
            score += 1.5
        # date proximity: small bonus when published near each other
        try:
            da = datetime.date.fromisoformat(a["iso"])
            db = datetime.date.fromisoformat(b["iso"])
            months = abs((da.year - db.year) * 12 + da.month - db.month)
            score += max(0.0, 1.0 - months / 36.0)
        except ValueError:
            pass
        return score

    # precompute, for each source, candidates sorted by relevance desc
    ranked = {}
    for s in slugs:
        cands = [t for t in slugs if t != s]
        cands.sort(key=lambda t: (-rel(arts[s], arts[t]), -1 if arts[t]["iso"] > arts[s]["iso"] else 1, t))
        ranked[s] = cands

    # only articles that actually render a related-grid can be link SOURCES/HOSTS
    linkable = [s for s in slugs if '<div class="related-grid">' in arts[s]["src"]]

    inbound = collections.Counter()
    chosen = {}
    # process oldest-first so newer (formerly favored) posts don't grab everything
    for s in sorted(linkable, key=lambda x: arts[x]["iso"]):
        cands = ranked[s]
        picks = cands[:2]                      # 2 strongest by relevance
        pool = [t for t in cands[2:POOL] if t not in picks]
        pool.sort(key=lambda t: (inbound[t], -rel(arts[s], arts[t]), t))
        if pool:
            picks.append(pool[0])              # spreader: least-linked relevant
        for p in picks[:N_CARDS]:
            inbound[p] += 1
        chosen[s] = picks[:N_CARDS]

    # repair pass: lift under-linked / orphan articles, respecting relevance
    # (only drop a host card that stays >= MIN_INBOUND and is less relevant than target)
    for target in sorted(slugs, key=lambda x: (inbound[x], arts[x]["iso"])):
        guard = 0
        while inbound[target] < MIN_INBOUND and guard < 40:
            guard += 1
            hosts = sorted((h for h in linkable if h != target and target not in chosen[h]),
                           key=lambda h: -rel(arts[h], arts[target]))
            placed = False
            for h in hosts[:40]:
                drop = None
                for c in chosen[h]:
                    if inbound[c] > MIN_INBOUND and rel(arts[h], arts[c]) < rel(arts[h], arts[target]):
                        if drop is None or inbound[c] > inbound[drop] or rel(arts[h], arts[c]) < rel(arts[h], arts[drop]):
                            drop = c
                if drop is not None:
                    chosen[h][chosen[h].index(drop)] = target
                    inbound[drop] -= 1
                    inbound[target] += 1
                    placed = True
                    break
            if not placed:
                break

    # guarantee zero orphans: force each remaining orphan into its most-relevant
    # host that has a redundant card (highest inbound, stays >= MIN_INBOUND)
    for target in [s for s in slugs if inbound[s] == 0]:
        hosts = sorted((h for h in linkable if h != target and target not in chosen[h]),
                       key=lambda h: -rel(arts[h], arts[target]))
        for h in hosts:
            drop = max((c for c in chosen[h] if inbound[c] > MIN_INBOUND),
                       key=lambda c: (inbound[c], -rel(arts[h], arts[c])), default=None)
            if drop is not None:
                chosen[h][chosen[h].index(drop)] = target
                inbound[drop] -= 1
                inbound[target] += 1
                break

    # render + write
    def card(t):
        a = arts[t]
        return (
'        <a class="related-card" href="../{slug}/index.html">\n'
'          <div class="related-card-thumb">\n'
'            <img src="../../assets/images/{slug}/{cbase}" width="{cw}" height="{ch}" alt="{title}" loading="lazy" decoding="async">\n'
'          </div>\n'
'          <div class="related-card-body">\n'
'            <div class="related-card-cat">{cat}</div>\n'
'            <h3 class="related-card-title">{title}</h3>\n'
'            <div class="related-card-footer">\n'
'              <span class="related-card-date">{label}</span>\n'
'              <span class="related-card-link">Read</span>\n'
'            </div>\n'
'          </div>\n'
'        </a>').format(slug=a["slug"], cbase=a["cbase"], cw=a["cw"], ch=a["ch"],
                       title=a["title"], cat=a["cat"], label=a["label"])

    changed = 0
    grid_re = re.compile(r'(<div class="related-grid">\s*).*?(\s*</div>\s*(?:<div class="related-foot">|</div>\s*</section>))', re.S)
    for s in chosen:
        a = arts[s]
        cards = "\n\n".join(card(t) for t in chosen[s])
        def repl(m):
            return '<div class="related-grid">\n\n' + cards + "\n\n      " + m.group(2).lstrip()
        new = grid_re.sub(repl, a["src"], count=1)
        if new != a["src"]:
            changed += 1
            if APPLY:
                open(a["fp"], "w", encoding="utf-8").write(new)

    orphans_after = [s for s in slugs if inbound[s] == 0]
    dist = collections.Counter(inbound[s] for s in slugs)
    nogrid = [s for s in slugs if '<div class="related-grid">' not in arts[s]["src"]]
    print(f"articles: {n}")
    print(f"inbound after rebuild -> orphans(0): {len(orphans_after)} {orphans_after} | "
          f"min {min(inbound[s] for s in slugs)} max {max(inbound[s] for s in slugs)}")
    print(f"articles with no related-grid to rewrite: {len(nogrid)} {nogrid}")
    print("inbound histogram (links->#articles):",
          {k: dist[k] for k in sorted(dist)})
    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} related grids rewritten")
    if not APPLY:
        sample = "azithromycin-mda-mali"
        print(f"\nsample related for [{sample}]:")
        for t in chosen[sample]:
            print(f"   {arts[t]['cat']:>10} | {arts[t]['label']:>8} | {t}")

if __name__ == "__main__":
    main()
