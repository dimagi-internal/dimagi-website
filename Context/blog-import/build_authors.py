#!/usr/bin/env python3
"""Build per-author archive pages + linkify article bylines.

For every blog post under blog/<slug>/index.html this:
  1. Parses the byline author string and splits it into contributor(s).
  2. Rewrites the byline so each person/org name links to /blog/author/<slug>/.
  3. Bumps the article.css cache-buster (a byline-link CSS rule is added).
Then it writes blog/author/<slug>/index.html for each distinct author, a grid of
all the posts they (co-)wrote, reusing the site nav/footer + .blog-card styles.

Idempotent + re-runnable. Run after any blog regen (render_all/apply_tag_pass),
the same way transform_filters.py / normalize_footer.py are re-applied.

    python3 Context/blog-import/build_authors.py
"""
import os, re, html, datetime, unicodedata, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # .../Dimagi Pre-Login
BLOG = os.path.join(ROOT, "blog")
AUTHOR_DIR = os.path.join(BLOG, "author")
ARTICLE_CSS = os.path.join(ROOT, "assets", "article.css")
CSS_VER = "12"                                          # new article.css cache key

# ---- contributor parsing rules -------------------------------------------
# Bylines that pack multiple PEOPLE -> the ordered list of names to link.
# (Affiliation-style bylines list only the person; the org tail stays plain.)
SPLIT = {
    "Paulo Nunes, Anita Kruger and Khanyisa Bomba":
        ["Paulo Nunes", "Anita Kruger", "Khanyisa Bomba"],
    "Neal Lesh, Clayton Sims, Cory Zue":
        ["Neal Lesh", "Clayton Sims", "Cory Zue"],
    "James Wolff and Kathleen Samways":
        ["James Wolff", "Kathleen Samways"],
    "Nisha Sinha, Dhivya Sivaramakrishnan &amp; Anna Dixon":
        ["Nisha Sinha", "Dhivya Sivaramakrishnan", "Anna Dixon"],
    "Lilianna Bagnoli, Christie Civetta":
        ["Lilianna Bagnoli", "Christie Civetta"],
    "Alberto Maldonado, Volunteers of America":
        ["Alberto Maldonado"],
    "Maureen Stickel, World Poultry Foundation":
        ["Maureen Stickel"],
}
# Merge a stray short byline into the person's canonical name.
ALIASES = {"Shabnam": "Shabnam Aggarwal"}


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "author"


def initials(name):
    words = [w for w in re.split(r"\s+", name) if w and w[0].isalpha()]
    if not words:
        return name[:1].upper()
    if len(words) == 1:
        return words[0][:1].upper()
    return (words[0][0] + words[1][0]).upper()


def link_entities(raw):
    """raw byline -> [(display_substring, canonical_name), ...] to link."""
    names = SPLIT.get(raw, [raw])
    out = []
    for n in names:
        canon = ALIASES.get(html.unescape(n).strip(), html.unescape(n).strip())
        out.append((n, canon))
    return out


def linkified_byline(raw):
    """Wrap each contributor substring in raw with an author-page link."""
    parts, cursor = [], 0
    for disp, canon in link_entities(raw):
        idx = raw.find(disp, cursor)
        if idx < 0:
            continue
        parts.append(raw[cursor:idx])
        parts.append(
            f'<a class="article-byline-author-link" '
            f'href="../author/{slugify(canon)}/index.html">{disp}</a>'
        )
        cursor = idx + len(disp)
    parts.append(raw[cursor:])
    return "".join(parts)


def date_sortkey(datelabel, iso):
    if iso:
        return iso[:10]
    for fmt in ("%b %Y", "%B %Y"):
        try:
            return datetime.datetime.strptime(datelabel, fmt).strftime("%Y-%m-01")
        except ValueError:
            pass
    return "0000-00-00"


# ---- scan posts -----------------------------------------------------------
def scan():
    authors = {}   # canon -> {"slug","names":set,"posts":[...]}
    touched = 0
    for d in sorted(os.listdir(BLOG)):
        fp = os.path.join(BLOG, d, "index.html")
        if d == "author" or not os.path.isfile(fp):
            continue
        s = open(fp, encoding="utf-8").read()

        m = re.search(r'<span class="article-byline-author">(.*?)</span>', s, re.S)
        if not m:
            continue
        inner = m.group(1).strip()

        # Re-run safe: if the byline is already linked, the anchors ARE the
        # per-contributor breakdown -> rebuild the registry from them and skip
        # re-linking. First pass: inner is the raw name(s).
        if "article-byline-author-link" in inner:
            ents = [
                (disp, ALIASES.get(html.unescape(disp).strip(), html.unescape(disp).strip()))
                for disp in re.findall(
                    r'<a class="article-byline-author-link"[^>]*>(.*?)</a>', inner, re.S)
            ]
            raw = None
        else:
            raw = inner
            ents = link_entities(raw)

        title = (re.search(r'<h1 class="article-title">(.*?)</h1>', s, re.S) or [None, ""])[1]
        desc = (re.search(r'<meta name="description" content="([^"]*)"', s) or [None, ""])[1]
        iso = (re.search(r'article:published_time" content="([^"]+)"', s) or [None, ""])[1][:10]
        dl = re.search(r'<span class="article-byline-detail">\s*<span>([^<]*)</span>', s)
        datelabel = dl.group(1).strip() if dl else ""
        fig = re.search(r'<figure class="article-cover"[^>]*>(.*?)</figure>', s, re.S)
        cov = re.search(r'src="[^"]*/([^"/]+)"', fig.group(1)) if fig else None
        coverfile = cov.group(1) if cov else "cover.jpg"

        post = dict(slug=d, title=title.strip(), desc=desc, datelabel=datelabel,
                    coverfile=coverfile, sortkey=date_sortkey(datelabel, iso))

        for disp, canon in ents:
            a = authors.setdefault(canon, dict(slug=slugify(canon), names=set(), posts=[]))
            a["names"].add(canon)
            if d not in {p["slug"] for p in a["posts"]}:
                a["posts"].append(post)

        # rewrite byline in place (only on the first, un-linked pass)
        if raw is not None:
            s = s.replace(
                m.group(0),
                f'<span class="article-byline-author">{linkified_byline(raw)}</span>', 1)
        # bump article.css cache key
        s2 = re.sub(r'(article\.css\?v=)\d+', r"\g<1>" + CSS_VER, s)
        if s2 != open(fp, encoding="utf-8").read():
            open(fp, "w", encoding="utf-8").write(s2)
            touched += 1

    # slug collision guard
    seen = {}
    for canon, a in authors.items():
        seen.setdefault(a["slug"], []).append(canon)
    for slug, names in seen.items():
        if len(names) > 1:
            print(f"  !! slug collision {slug!r}: {names}")
    return authors, touched


# ---- reusable nav / footer (lifted from blog/index.html, re-based) --------
def chrome():
    s = open(os.path.join(BLOG, "index.html"), encoding="utf-8").read()
    nav = re.search(r'<div class="nav-wrap">.*?</nav>\s*</div>\s*</div>', s, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", s, re.S).group(0)
    navjs = re.search(r'<script src="[^"]*nav\.js[^"]*"></script>', s).group(0)
    # blog/index.html is one level up from a post; author pages are two levels up.
    rebase = lambda block: block.replace('"../', '"../../../')
    return rebase(nav), rebase(footer), rebase(navjs)


HEAD_CSS = """
.author-hero { position: relative; padding: 86px 0 48px;
  background: linear-gradient(180deg, #ffffff 0%, #f5f7ff 100%);
  border-bottom: 1px solid var(--line); overflow: hidden; }
.author-hero::before { content:""; position:absolute; top:-200px; right:-140px;
  width:560px; height:560px; border-radius:50%;
  background: radial-gradient(circle, rgba(56,67,208,0.11), transparent 62%); }
.author-hero > .container { position: relative; z-index: 1; }
.author-back { font-family: var(--sans); font-size: 13px; font-weight: 600;
  letter-spacing: .02em; color: var(--indigo); display: inline-flex; gap: 6px;
  margin-bottom: 26px; }
.author-back::before { content: "\\2190"; }
.author-back:hover { color: var(--indigo-deep); }
.author-id { display: flex; align-items: center; gap: 20px; }
.author-avatar { width: 72px; height: 72px; border-radius: 50%;
  background: var(--grad-deep); display: flex; align-items: center;
  justify-content: center; flex-shrink: 0; color: #fff; font-weight: 600;
  font-size: 26px; letter-spacing: -.01em; }
.author-meta h1 { font-size: clamp(30px, 4vw, 46px); font-weight: 200;
  letter-spacing: -0.03em; line-height: 1.05; margin: 0 0 8px; color: var(--ink); }
.author-meta .author-eyebrow { font-family: var(--sans); font-size: 11px;
  font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted-soft); display: block; margin-bottom: 10px; }
.author-count { font-family: var(--sans); font-size: 13px; font-weight: 600;
  letter-spacing: .04em; color: var(--muted); }
.blog-grid-wrap { padding: 56px 0 100px; background: #f5f7ff; }
.blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.blog-card { position: relative; background: #fff; border: 1px solid var(--line);
  border-radius: var(--radius-lg); overflow: hidden; display: flex;
  flex-direction: column; transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease; }
.blog-card:hover { transform: translateY(-5px);
  box-shadow: 0 26px 50px -18px rgba(10,6,32,0.18); border-color: var(--rule); }
.blog-card-image { display: block; position: relative; aspect-ratio: 16 / 10;
  overflow: hidden; background: var(--grad-deep); flex-shrink: 0; }
.blog-card-image img { width: 100%; height: 100%; object-fit: cover; display: block;
  transition: transform 500ms ease; }
.blog-card:hover .blog-card-image img { transform: scale(1.05); }
.blog-card-image::after { content:""; position:absolute; inset:0;
  background: linear-gradient(180deg, rgba(10,6,32,0.22), transparent 36%); pointer-events:none; }
.blog-card-body { padding: 22px 24px 24px; display: flex; flex-direction: column; gap: 9px; flex: 1; }
.blog-card-title { font-size: 18px; font-weight: 600; letter-spacing: -0.02em;
  color: var(--ink); line-height: 1.34; display:-webkit-box; -webkit-box-orient:vertical;
  -webkit-line-clamp:2; overflow:hidden; }
.blog-card-desc { display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:2;
  overflow:hidden; font-size: 14px; color: var(--muted); line-height: 1.55; margin: 0; }
.blog-card-footer { display: flex; align-items: center; justify-content: space-between;
  margin-top: auto; padding-top: 16px; }
.blog-card-date { font-family: var(--sans); font-size: 11px; font-weight: 600;
  color: var(--muted-soft); letter-spacing: 0.06em; text-transform: uppercase; }
.blog-card-link { font-size: 13px; font-weight: 600; color: var(--indigo);
  display: inline-flex; align-items: center; gap: 4px; transition: gap 150ms, color 150ms; }
.blog-card-link::after { content: "\\2192"; }
.blog-card-link:hover { color: var(--indigo-deep); gap: 8px; }
@media (max-width: 900px) { .blog-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .blog-grid { grid-template-columns: 1fr; }
  .author-id { gap: 14px; } .author-avatar { width: 58px; height: 58px; font-size: 21px; } }
"""


def card_html(post):
    s, t, d = post["slug"], post["title"], post["desc"]
    label = post["datelabel"] or ""
    img = f"../../../assets/images/{s}/{post['coverfile']}"
    href = f"../../{s}/index.html"
    alt = t.replace('"', "&quot;")   # title is already HTML-escaped; don't double-escape
    return f"""    <article class="blog-card">
      <a class="blog-card-image" href="{href}">
        <img src="{img}" alt="{alt}" loading="lazy" decoding="async">
      </a>
      <div class="blog-card-body">
        <h2 class="blog-card-title">{t}</h2>
        <p class="blog-card-desc">{d}</p>
        <div class="blog-card-footer">
          <span class="blog-card-date">{label}</span>
          <a class="blog-card-link" href="{href}">Read more</a>
        </div>
      </div>
    </article>"""


def author_page(canon, info, nav, footer, navjs):
    posts = sorted(info["posts"], key=lambda p: p["sortkey"], reverse=True)
    n = len(posts)
    cards = "\n".join(card_html(p) for p in posts)
    title = html.escape(canon)
    count = f"{n} post" + ("" if n == 1 else "s")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Posts by {title} | Dimagi</title>
<meta name="description" content="Articles written by {title} on the Dimagi blog.">
<link rel="canonical" href="https://dimagi.com/blog/author/{info['slug']}/">
<meta name="robots" content="noindex, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@200..700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../../assets/styles.css?v=16">
<style>{HEAD_CSS}</style>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="author-hero">
    <div class="container">
      <a class="author-back" href="../../index.html">Back to all posts</a>
      <div class="author-id">
        <div class="author-avatar" aria-hidden="true">{initials(canon)}</div>
        <div class="author-meta">
          <span class="author-eyebrow">Author</span>
          <h1>{title}</h1>
          <span class="author-count">{count}</span>
        </div>
      </div>
    </div>
  </div>

  <div class="blog-grid-wrap">
    <div class="container">
      <div class="blog-grid">
{cards}
      </div>
    </div>
  </div>

</main>

{footer}
{navjs}
</body>
</html>
"""


def ensure_css_rule():
    s = open(ARTICLE_CSS, encoding="utf-8").read()
    if "article-byline-author-link" in s:
        return False
    rule = (
        "\n/* ---- Byline author link (-> /blog/author/<slug>/) ---- */\n"
        ".article-byline-author a,\n.article-byline-author-link {\n"
        "  color: inherit; text-decoration: none;\n"
        "  border-bottom: 1px solid transparent;\n"
        "  transition: color 140ms ease, border-color 140ms ease;\n}\n"
        ".article-byline-author a:hover,\n.article-byline-author-link:hover {\n"
        "  color: var(--indigo); border-bottom-color: currentColor;\n}\n"
    )
    anchor = ".article-byline-detail .dot"
    i = s.find(anchor)
    j = s.find("\n", s.find("}", i)) + 1 if i >= 0 else len(s)
    s = s[:j] + rule + s[j:]
    open(ARTICLE_CSS, "w", encoding="utf-8").write(s)
    return True


def main():
    authors, touched = scan()
    print(f"posts touched (byline linked + css bumped): {touched}")
    print(f"distinct authors: {len(authors)}")

    css_added = ensure_css_rule()
    print(f"article.css byline-link rule: {'added' if css_added else 'present'}")

    if os.path.isdir(AUTHOR_DIR):
        shutil.rmtree(AUTHOR_DIR)
    os.makedirs(AUTHOR_DIR, exist_ok=True)

    nav, footer, navjs = chrome()
    for canon, info in sorted(authors.items(), key=lambda kv: -len(kv[1]["posts"])):
        d = os.path.join(AUTHOR_DIR, info["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            author_page(canon, info, nav, footer, navjs))

    print(f"author pages written: {len(authors)}  ->  blog/author/<slug>/")
    top = sorted(authors.items(), key=lambda kv: -len(kv[1]["posts"]))[:8]
    for canon, info in top:
        print(f"   {len(info['posts']):>3}  {info['slug']:<26} {canon}")


if __name__ == "__main__":
    main()
