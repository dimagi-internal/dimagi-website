#!/usr/bin/env python3
"""Render a High-Impact Growth episode page in the refreshed 70-82 layout.

Chrome (CSS/nav/footer) is pulled verbatim from a canonical refreshed page (ep-78)
so every episode shares the approved styling. Dynamic content comes from
Context/episodes/<slug>.json (extraction) + Context/editorial/<slug>.json (editorial).
Writes podcast/<slug>/index.html.
"""
import json, os, re, html, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from podcast_tags import chip_row, with_chip_css

ROOT = os.path.dirname(HERE)  # Dimagi Pre-Login/
TEMPLATE = os.path.join(ROOT, "podcast", "ep-78-what-makes-a-dollar-matter-lessons-from-coefficient-giving", "index.html")
TRANSCRIPT_MIN = 15
BRAND = "High-Impact Growth"

_tpl = open(TEMPLATE, encoding="utf-8").read()
# Fold the canonical episode-tag CSS into the shared <style> (idempotent, deduped).
STYLE = with_chip_css("<style>" + re.search(r"(?is)<style>(.*?)</style>", _tpl).group(1) + "</style>")
FOOTER = re.search(r"(?is)(<footer>.*?</footer>)", _tpl).group(1)

NAV = '''<div class="nav-wrap">
  <div class="container">
    <nav class="primary" data-nav-base="../../">
      <a class="logo" href="../../index.html">
        <img class="logo-img invert" src="../../assets/dimagi-logo.png" alt="Dimagi">
      </a>
      <div class="nav-links">
        <a href="#">Products</a>
        <a href="../../professional-services/index.html">Professional Services</a>
        <a href="../../company/about/index.html" class="nav-active">Company</a>
        <a href="../../contact/index.html">Contact Us</a>
      </div>
      <div class="nav-cta">
        <a class="btn btn-primary" href="../../sign-in/index.html">Sign In</a>
      </div>
    </nav>
  </div>
</div>'''


def dedash(s):
    if not s:
        return s or ""
    s = s.replace("—", " - ").replace("―", " - ")
    s = re.sub(r"\s+-\s+", " - ", s)
    return s


E = lambda s: html.escape(dedash(s or ""), quote=True)

ICONS = {
 "Spotify": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M7.5 9.5c3-1 6.5-.7 9 1"/><path d="M7 12.5c2.5-.8 5.5-.5 7.7 1"/><path d="M7.5 15.3c2-.6 4.3-.4 6 .8"/></svg>',
 "Apple Podcasts": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8" fill="currentColor" stroke="none"/></svg>',
 "YouTube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="4"/><polygon points="10 9 15 12 10 15 10 9" fill="currentColor" stroke="none"/></svg>',
 "Amazon Music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="10" x2="5" y2="14"/><line x1="9" y1="6" x2="9" y2="18"/><line x1="13" y1="3" x2="13" y2="21"/><line x1="17" y1="7" x2="17" y2="17"/><line x1="21" y1="10" x2="21" y2="14"/></svg>',
}


def fmt_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")


def listen_btn(label, href):
    return f'<a class="listen-btn" href="{E(href)}" target="_blank" rel="noopener">{ICONS[label]}\n            {label}</a>'


def youtube_embed_url(yt):
    m = re.search(r"youtu\.be/([A-Za-z0-9_\-]+)", yt or "") or re.search(r"[?&]v=([A-Za-z0-9_\-]+)", yt or "")
    return f"https://www.youtube.com/embed/{m.group(1)}" if m else None


def person_row(name, role, org, img=None, initials=None):
    if img:
        avatar = f'<div class="person-avatar"><img src="{img}" alt="{E(name)}" loading="lazy"></div>'
    else:
        ini = initials or "".join(w[0] for w in name.split()[:2]).upper()
        avatar = f'<div class="person-avatar" aria-hidden="true">{E(ini)}</div>'
    org_html = f'\n              <span class="person-org">{E(org)}</span>' if org else ""
    return f'''<div class="person-row">
            {avatar}
            <div class="person-info">
              <p class="person-name">{E(name)}</p>
              <p class="person-role">{role}</p>{org_html}
            </div>
          </div>'''


def build(ep, ed):
    num = ep["num"]; slug = ep["slug"]
    title = ep["title"]
    deck = ed.get("deck") or (ep["show_notes"][0] if ep["show_notes"] else "")
    seo = ed.get("seo_description") or deck
    og_desc = ed.get("og_description") or deck

    # ---- hero player ----
    if ep.get("spotify_id"):
        player = f'''<div class="ep-player">
          <iframe
            src="https://open.spotify.com/embed/episode/{ep["spotify_id"]}?utm_source=generator"
            width="100%" height="352" frameborder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            title="Spotify player: Episode {num} of {BRAND}"></iframe>
        </div>'''
    elif youtube_embed_url(ep.get("youtube")):
        player = f'''<div class="ep-player">
          <iframe
            src="{youtube_embed_url(ep["youtube"])}"
            width="100%" height="352" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            title="YouTube player: Episode {num} of {BRAND}"></iframe>
        </div>'''
    else:
        player = ""

    btns = []
    if ep.get("spotify_id"):
        btns.append(listen_btn("Spotify", f'https://open.spotify.com/episode/{ep["spotify_id"]}'))
    if ep.get("apple"):
        btns.append(listen_btn("Apple Podcasts", ep["apple"]))
    if ep.get("youtube"):
        btns.append(listen_btn("YouTube", ep["youtube"]))
    if ep.get("amazon"):
        btns.append(listen_btn("Amazon Music", ep["amazon"]))
    listen_row = ""
    if btns:
        listen_row = ('<div class="listen-row">\n          <span class="listen-label">Listen on</span>\n          '
                      + "\n          ".join(btns) + "\n        </div>")

    hero_player = ""
    if player or listen_row:
        hero_player = f'''
      <div class="ep-hero-player" id="listen">
        {player}
        {listen_row}
      </div>'''

    meta_bits = [f'<span class="ep-meta-brand">{BRAND} Podcast</span>',
                 '<span class="dot"></span>', f"<span>{E(fmt_date(ep['date']))}</span>"]
    if ep.get("duration"):
        meta_bits += ['<span class="dot"></span>', f"<span>{E(ep['duration'])}</span>"]
    NL = "\n          "
    meta_html = NL.join(meta_bits)

    # ---- stats band (only if real numbers) ----
    stats = ed.get("stats") or []
    stats_band = ""
    if stats:
        cells = "\n        ".join(
            f'''<div class="ep-stat">
          <div class="ep-stat-num">{E(s["num"])}</div>
          <div class="ep-stat-label">{E(s["label"])}</div>
        </div>''' for s in stats[:3])
        stats_band = f'''
  <section class="ep-stats-band" aria-label="Episode highlights">
    <div class="container">
      <div class="ep-stats-head">By the numbers</div>
      <div class="ep-stats">
        {cells}
      </div>
    </div>
  </section>'''

    # ---- body ----
    about = ed.get("about") or ep["show_notes"]
    about_html = "\n        ".join(f"<p>{E(p)}</p>" for p in about)

    quote_html = ""
    q = ed.get("pull_quote")
    if q and q.get("text"):
        cite = f'\n          <cite>{E(q["cite"])}</cite>' if q.get("cite") else ""
        quote_html = f'''
        <blockquote>
          <p>&ldquo;{E(q["text"])}&rdquo;</p>{cite}
        </blockquote>'''

    bullets = ed.get("bullets") or []
    bullets_html = ""
    if bullets:
        lis = "\n          ".join(f"<li>{dedash(b)}</li>" for b in bullets)
        bullets_html = f'''
        <h3 id="in-this-episode">In this episode</h3>
        <ul>
          {lis}
        </ul>'''

    transcript = ep.get("transcript") or []
    transcript_html = ""
    if len(transcript) >= TRANSCRIPT_MIN:
        paras = []
        for p in transcript:
            if p["speaker"]:
                paras.append(f'<p><span class="spk">{E(p["speaker"])}:</span> {E(p["text"])}</p>')
            else:
                paras.append(f'<p>{E(p["text"])}</p>')
        body = "\n              ".join(paras)
        transcript_html = f'''
        <details class="ep-transcript" id="transcript">
          <summary>
            <span class="ep-transcript-summary-left">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="14" y2="17"/></svg>
              Read the transcript
            </span>
            <span class="ep-transcript-toggle">
              <span class="label-closed">Expand</span><span class="label-open">Collapse</span>
              <svg class="ep-transcript-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
            </span>
          </summary>
          <div class="ep-transcript-body">
            <div class="ep-transcript-scroll">
              <p class="ep-transcript-note">This transcript was generated by AI and may contain typos and inaccuracies.</p>
              {body}
            </div>
          </div>
        </details>'''

    # ---- people (two boxes: guests | hosts) ----
    guests = ed.get("guests") or []
    host_rows = []
    if ep.get("host_jonathan", True):
        host_rows.append(person_row("Jonathan Jackson", "Co-Founder &amp; CEO", "Dimagi",
                                     img="../../assets/images/podcast/host-jonathan-jackson.jpg"))
    if ep.get("host_amie", True):
        host_rows.append(person_row("Amie Vaccaro", "VP of Growth &amp; Strategy", "Dimagi",
                                     img="../../assets/images/podcast/host-amie-vaccaro.jpg"))
    hosts_box = ""
    if host_rows:
        hosts_box = f'''<div class="people-box">
          <div class="people-subhead">{"Hosts" if len(host_rows) > 1 else "Host"}</div>
          {NL.join(host_rows)}
        </div>'''

    if guests:
        guest_rows = NL.join(
            person_row(g["name"], E(g.get("role", "")), g.get("org", ""),
                       img=g.get("img"), initials=g.get("initials"))
            for g in guests)
        guests_box = f'''<div class="people-box">
          <div class="people-subhead">{"Guests" if len(guests) > 1 else "Guest"}</div>
          {guest_rows}
        </div>'''
        people_inner = f'''<div class="people-cols">
        {guests_box}
        {hosts_box}
      </div>'''
    else:
        people_inner = f'''<div class="people-cols" style="grid-template-columns:minmax(0,560px);justify-content:center;">
        {hosts_box}
      </div>'''

    # ---- CTA primary ----
    if ep.get("spotify_id"):
        cta_label, cta_href = "Subscribe on Spotify", f'https://open.spotify.com/episode/{ep["spotify_id"]}'
    elif ep.get("youtube"):
        cta_label, cta_href = "Watch on YouTube", ep["youtube"]
    elif ep.get("apple"):
        cta_label, cta_href = "Listen on Apple Podcasts", ep["apple"]
    else:
        cta_label, cta_href = None, None
    cta_primary = (f'<a class="btn btn-on-dark btn-arrow" href="{E(cta_href)}" target="_blank" rel="noopener">{cta_label}</a>\n            '
                   if cta_label else "")

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Ep {num}: {E(title)} | {BRAND} | Dimagi</title>
<meta name="description" content="{E(seo)}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://dimagi.com/podcast/{slug}/">
<meta property="og:title" content="Ep {num}: {E(title)}">
<meta property="og:description" content="{E(og_desc)}">
<meta property="og:image" content="../../assets/images/high-impact-growth-podcast.jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/styles.css?v=15">
<link rel="stylesheet" href="../../assets/article.css?v=3">
{STYLE}
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{NAV}

<main id="main">

  <header class="ep-hero">
    <div class="container">
      <div class="ep-hero-text">
        <div class="ep-meta">
          {meta_html}
        </div>
        <h1 class="ep-title">{E(title)}</h1>
        <p class="ep-deck">{E(deck)}</p>{chip_row(num)}
      </div>
{hero_player}
    </div>
  </header>
{stats_band}

  <article class="article-body ep-body">
    <div class="container">
      <div class="article-prose-width prose">

        <h2 id="about">About this episode</h2>
        {about_html}
{quote_html}
{bullets_html}
{transcript_html}

      </div>
    </div>
  </article>

  <section class="people-band" id="people">
    <div class="container">
      <div class="people-head">
        <h2>Guests &amp; hosts</h2>
      </div>
      {people_inner}
    </div>
  </section>

  <section class="cta-band ep-cta">
    <div class="container">
      <div class="ep-cta-inner">
        <div class="ep-cta-art">
          <img src="../../assets/images/high-impact-growth-podcast.jpeg" alt="{BRAND} podcast cover art" loading="lazy">
        </div>
        <div class="ep-cta-text">
          <span class="eyebrow on-dark">Never miss an episode</span>
          <h2>Stories on building for high impact</h2>
          <p>{BRAND} brings you conversations with the leaders building digital solutions that are both deeply impactful and built to scale. Subscribe wherever you listen.</p>
          <div class="cta-actions">
            {cta_primary}<a class="btn btn-ghost-on-dark btn-arrow" href="../index.html">Browse all episodes</a>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>

{FOOTER}
<script src="../../assets/js/nav.js?v=6"></script>
</body>
</html>
'''


def load_editorial(slug):
    p = os.path.join(HERE, "editorial", slug + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def main(slugs):
    epdir = os.path.join(HERE, "episodes")
    if not slugs:
        slugs = [f[:-5] for f in os.listdir(epdir) if f.endswith(".json")]
    for slug in slugs:
        ep = json.load(open(os.path.join(epdir, slug + ".json"), encoding="utf-8"))
        ed = load_editorial(slug)
        out_dir = os.path.join(ROOT, "podcast", slug)
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(build(ep, ed))
        print(f"built ep{ep['num']:>3}  {slug}")


if __name__ == "__main__":
    main(sys.argv[1:])
