# Dimagi Pre-Login blog page generator. exec() this, then define POSTS and call render(p).
import json, html as _html
from urllib.parse import quote

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"

CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>'
SVG_COPY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
SVG_LI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.25 8h4.5v13H.25V8zM8 8h4.3v1.78h.06c.6-1.13 2.07-2.32 4.26-2.32 4.56 0 5.4 3 5.4 6.9V21h-4.5v-5.7c0-1.36-.02-3.1-1.9-3.1-1.9 0-2.18 1.48-2.18 3v5.8H8V8z"/></svg>'
SVG_X = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 1.5h3.3l-7.2 8.2L23.7 22.5h-6.6l-5.2-6.8-6 6.8H2.6l7.7-8.8L2 1.5h6.8l4.7 6.2 5.4-6.2zm-1.2 19h1.8L7.1 3.4H5.2L17.7 20.5z"/></svg>'
SVG_TOP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg>'

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

FOOTER = '''<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img class="footer-logo" src="../../assets/dimagi-logo.png" alt="Dimagi">
        <p>Technology that empowers frontline workers, strengthens programs, and drives lasting change in communities worldwide.</p>
      </div>
      <div class="footer-col">
        <h5>Products</h5>
        <ul>
          <li><a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a></li>
          <li><a href="https://connect.dimagi.com/" target="_blank" rel="noopener">Connect</a></li>
          <li><a href="https://dimagi.com/sureadhere/" target="_blank" rel="noopener">SureAdhere</a></li>
          <li><a href="https://www.openchatstudio.com/" target="_blank" rel="noopener">Open Chat Studio</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Professional Services</h5>
        <ul>
          <li><a href="../../professional-services/index.html">Overview</a></li>
          <li><a href="../../professional-services/global-services/index.html">Global Services</a></li>
          <li><a href="../../professional-services/united-states/index.html">United States</a></li>
          <li><a href="../../professional-services/india/index.html">India</a></li>
          <li><a href="../../professional-services/research-data/index.html">Research &amp; Data</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="../../company/about/index.html">About Us</a></li>
          <li><a href="../../company/our-approach/index.html">Our Approach</a></li>
          <li><a href="../index.html">Blog</a></li>
          <li><a href="../../podcast/index.html">Podcast</a></li>
          <li><a href="../../company/careers/index.html">Careers</a></li>
          <li><a href="../../contact/index.html">Contact Us</a></li>
          <li><a href="../../press/index.html">Press &amp; Coverage</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Legal</h5>
        <ul>
          <li><a href="../../legal/privacy-policy/index.html">Privacy Policy</a></li>
          <li><a href="../../legal/terms-of-service/index.html">Terms of Service</a></li>
          <li><a href="../../legal/business-agreement/index.html">Business Agreement</a></li>
          <li><a href="../../legal/acceptable-use/index.html">Acceptable Use Policy</a></li>
          <li><a href="../../legal/financial-conflict/index.html">Financial Conflict of Interest</a></li>
          <li><a href="../../legal/transparency-coverage/index.html">Transparency in Coverage</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 DIMAGI, INC.</span>
      <div class="footer-legal">
        <a href="../../legal/privacy-policy/index.html">Privacy</a>
        <a href="../../legal/terms-of-service/index.html">Terms</a>
        <a href="../../legal/acceptable-use/index.html">Acceptable Use</a>
        <a href="https://dimagi.safebase.us/" target="_blank" rel="noopener">Trust Center</a>
      </div>
    </div>
  </div>
</footer>'''

def esc(s): return _html.escape(s, quote=True)

def build(p):
    slug=p['slug']; canon=f"https://dimagi.com/{slug}/"
    titletag=p['titletag']; desc=p['desc']; h1=p['h1']; deck=p['deck']
    cu=quote(canon, safe=''); tu=quote(p.get('sharetitle', h1), safe='')
    ld_article={"@context":"https://schema.org","@type":"Article","headline":h1,"description":desc,
        "image":p['ogimage'],"datePublished":p['date'],"dateModified":p['date'],
        "author":{"@type":"Person","name":p['author']},
        "publisher":{"@type":"Organization","name":"Dimagi","logo":{"@type":"ImageObject","url":"https://dimagi.com/wp-content/uploads/2023/11/dimagi_logo_46.png"}},
        "mainEntityOfPage":{"@type":"WebPage","@id":canon},"articleSection":p['category'],"keywords":p['keywords']}
    ld_bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://dimagi.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://dimagi.com/blog/"},
        {"@type":"ListItem","position":3,"name":h1}]}
    # share row
    share=f'''<div class="article-share">
          <span class="article-share-label">Share</span>
          <button class="article-share-btn article-copy" type="button" aria-label="Copy link" data-copy-url="{canon}">
            {SVG_COPY}
            <span class="article-copy-label">Copy link</span>
          </button>
          <a class="article-share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={cu}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">
            {SVG_LI}
            LinkedIn
          </a>
          <a class="article-share-btn" href="https://twitter.com/intent/tweet?url={cu}&amp;text={tu}" target="_blank" rel="noopener" aria-label="Share on X">
            {SVG_X}
            X
          </a>
        </div>'''
    cap = f'\n      <p class="article-cover-caption">{p["covercaption"]}</p>' if p.get('covercaption') else ''
    # toc
    toc=''
    if p.get('toc'):
        items='\n'.join(f'          <a href="#{a}">{l}</a>' for a,l in p['toc'])
        toc=f'''

      <aside class="article-toc" aria-label="Table of contents">
        <p class="article-toc-label">On this page</p>
        <nav>
{items}
        </nav>
      </aside>'''
    tags='\n'.join(f'            <span class="article-tag">{t}</span>' for t in p['tags'])
    cta=p['cta']; btnclass=cta.get('btnclass','btn-indigo btn-arrow')
    btntarget=' target="_blank" rel="noopener"' if cta['btnhref'].startswith('http') else ''
    endcta=f'''        <div class="article-end-cta">
          <h3>{cta['h3']}</h3>
          <p>{cta['p']}</p>
          <a class="btn {btnclass}" href="{cta['btnhref']}"{btntarget}>{cta['btntext']}</a>
        </div>'''
    # related cards
    rc=[]
    for r in p['related']:
        rc.append(f'''        <a class="related-card" href="{r['href']}">
          <div class="related-card-thumb">
            <img src="{r['img']}" width="{r['w']}" height="{r['h']}" alt="{esc(r['alt'])}" loading="lazy" decoding="async">
          </div>
          <div class="related-card-body">
            <div class="related-card-cat">{r['cat']}</div>
            <h3 class="related-card-title">{r['title']}</h3>
            <div class="related-card-footer">
              <span class="related-card-date">{r['date']}</span>
              <span class="related-card-link">Read</span>
            </div>
          </div>
        </a>''')
    related="\n\n".join(rc)
    ogalt=esc(p['ogalt'])
    out=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{titletag}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(p['author'])}">
<link rel="canonical" href="{canon}">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:locale" content="en_US">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="Dimagi">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{esc(p.get('ogtitle',h1))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{p['ogimage']}">
<meta property="og:image:width" content="{p['ogw']}">
<meta property="og:image:height" content="{p['ogh']}">
<meta property="og:image:alt" content="{ogalt}">
<meta property="article:published_time" content="{p['date']}">
<meta property="article:author" content="{esc(p['author'])}">
<meta property="article:section" content="{p['category']}">
<meta property="article:tag" content="{p['tags'][0]}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p.get('ogtitle',h1))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{p['ogimage']}">
<meta name="twitter:image:alt" content="{ogalt}">

<!-- Article structured data -->
<script type="application/ld+json">
{json.dumps(ld_article, indent=2)}
</script>

<!-- Breadcrumb structured data -->
<script type="application/ld+json">
{json.dumps(ld_bc, indent=2)}
</script>

<link rel="preload" as="image" href="../../assets/images/{slug}/{p['cover']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@200..700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/styles.css?v=3">
<link rel="stylesheet" href="../../assets/article.css?v=10">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>
<div class="reading-progress" aria-hidden="true"><span class="reading-progress-bar"></span></div>

{NAV}

<main id="main" class="article-wrap">

  <!-- Hero -->
  <header class="article-hero">
    <div class="container">
      <div class="article-prose-width">
        <nav class="article-breadcrumb" aria-label="Breadcrumb">
          <a href="../../index.html">Home</a>
          {CHEV}
          <a href="../index.html">Blog</a>
          {CHEV}
          <span>{p['crumb']}</span>
        </nav>
        <span class="article-category">{p['category']}</span>
        <h1 class="article-title">{h1}</h1>
        <p class="article-deck">{deck}</p>
        <div class="article-byline">
          <div class="article-byline-avatar" aria-hidden="true">{p['initials']}</div>
          <div class="article-byline-meta">
            <span class="article-byline-author">{esc(p['author'])}</span>
            <span class="article-byline-detail">
              <span>{p['datelabel']}</span>
              <span class="dot"></span>
              <span>{p['readtime']}</span>
              <span class="dot"></span>
              <span>{p['crumb']}</span>
            </span>
          </div>
        </div>
        {share}
      </div>
    </div>
  </header>

  <!-- Cover -->
  <div class="article-cover-wrap">
    <div class="container">
      <figure class="article-cover">
        <img src="../../assets/images/{slug}/{p['cover']}"
             width="{p['coverw']}" height="{p['coverh']}" fetchpriority="high" decoding="async"
             alt="{esc(p['coveralt'])}">
      </figure>{cap}
    </div>
  </div>

  <!-- Body -->
  <article class="article-body">
    <div class="container">
      <div class="article-prose-width prose">

{p['body']}

        <!-- End CTA -->
{endcta}

        <!-- Foot nav -->
        <div class="article-foot">
          <div class="article-foot-label">Filed under</div>
          <div class="article-tags">
{tags}
          </div>
        </div>

      </div>{toc}
    </div>
  </article>

  <!-- Related -->
  <section class="related-wrap">
    <div class="container">
      <div class="related-head">
        <span class="eyebrow">Keep reading</span>
        <h2>More from the Dimagi blog</h2>
      </div>
      <div class="related-grid">

{related}

      </div>

      <div class="related-foot">
        <a class="btn btn-primary btn-arrow" href="../index.html">See All Blogs</a>
      </div>
    </div>
  </section>

</main>

{FOOTER}

<button class="back-to-top" type="button" aria-label="Back to top">
  {SVG_TOP}
</button>

<script src="../../assets/js/nav.js"></script>
<script src="../../assets/js/article.js?v=8"></script>
</body>
</html>
'''
    return out

import os
def render(p):
    d=os.path.join(ROOT,"blog",p['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d,"index.html"),"w",encoding='utf-8').write(build(p))
    print("  wrote", p['slug'])
