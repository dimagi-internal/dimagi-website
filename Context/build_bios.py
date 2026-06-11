#!/usr/bin/env python3
"""Generate leadership bio pages at /company/about/<slug>/, redirect stubs at the
old /person/<slug>/ URLs, and repoint the About-page name links internally.
Idempotent: re-run after any About-page regen. Slugs match the old dimagi.com
/person/ slugs so the 301 stubs map 1:1.

Run from the Dimagi Pre-Login repo root:  python3 Context/build_bios.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root

# slug, name, title (plain text), photo file, bio paragraph(s as list), extra (html or None)
PODCAST = ('../../../podcast/index.html',
           '../../../assets/images/high-impact-growth-podcast.jpeg',
           "Listen to Jonathan on Dimagi's podcast")

LEADERS = [
 ("jonathan-jackson", "Jonathan Jackson", "Co-Founder & CEO", "jonathan-jackson.jpg",
  ["Jonathan co-founded Dimagi and leads it as CEO, overseeing a global team that supports digital solutions in the vast majority of the world's countries. An award-winning social entrepreneur and software engineer, he made an early, uncompromising commitment to open technology that creates maximum good.",
   "A Schwab Foundation Social Entrepreneur recognized by Business Week as one of its most promising social entrepreneurs, Jonathan sits on the boards of SimPrints and Spark MicroGrants. He earned his bachelor's and master's in Electrical Engineering and Computer Science from MIT."],
  "podcast"),
 ("dr-vikram-sheel-kumar", "Dr. Vikram Sheel Kumar", "Founder & Chief Medical Officer", "vikram-kumar.jpg",
  ["An engineer and physician, Vikram co-founded Dimagi to bring the energy of the open-source movement to important problems in health. He completed graduate work at MIT's Media Lab and medical training at Harvard-MIT's Division of Health Sciences and Technology, graduating magna cum laude.",
   "His honors include MIT Technology Review recognition and a Paul and Daisy Soros Fellowship, and he has gone on to co-found Cogito Corp and Clear Creek Bio."],
  None),
 ("lucina-tse", "Lucina Tse", "Chief Operating Officer / Co-President", "lucina-tse.jpg",
  ["As COO, Lucina leads all facets of Dimagi's business and people operations, including finance, legal, and domestic and international operations. As Co-President, she manages corporate governance and drives strategic initiatives spanning mergers, acquisitions, and organizational growth.",
   "She holds an MBA from the University of Oxford and a BASc in Electrical Engineering from the University of Waterloo."],
  None),
 ("dr-neal-lesh", "Dr. Neal Lesh", "Chief Strategy Officer / Co-President", "neal-lesh.jpg",
  ["As Chief Strategy Officer, Neal supports a range of innovations at Dimagi, from data science and AI to research on scaling access to mental health care in low- and middle-income countries. He has spent years helping health programs across East and Southern Africa adopt data systems, building on an earlier academic career in data visualization and automated planning.",
   "He holds a PhD in Computer Science from the University of Washington and a master's in Global Health from the Harvard School of Public Health."],
  None),
 ("clayton-sims", "Clayton Sims", "Chief Technology Officer", "clayton-sims.jpg",
  ["Clayton directs the technical development of CommCare, one of the world's largest digital health platforms. Since 2006 he has led engineering efforts to design ICT systems that improve service delivery at the last mile, with a focus on human-centered design for low-resource settings.",
   "A former Visiting Lecturer in MIT's Computer Science department, he holds a BS and a Master of Engineering in Computer Science from MIT."],
  None),
 ("ismaila-diene", "Ismaila Diene", "Managing Director, Global Solutions", "ismaila-diene.jpg",
  ["Based in Senegal, Ismaila directs the Delivery team within the Solutions Division and serves as Regional Lead for West Africa. His background spans multi-disciplinary analysis in Paris and London and IT audit across West Africa, and he is passionate about leveraging technology to advance African development.",
   "A devoted fan of Hercule Poirot, he aspires to a mustache worthy of Agatha Christie's detective."],
  None),
 ("gillian-javetski", "Gillian Javetski", "Managing Director, CommCare", "gillian-javetski.jpg",
  ["Gillian has built her career in project, marketing, and operations roles across social impact technology organizations, including Vecna Cares, Telerivet, Partners In Health, and One Laptop Per Child. She previously co-founded and served as COO of an ICT services consulting firm working across Latin America and the Caribbean, and has managed more than 30 digital health projects in low-resource settings.",
   "She holds an MPH from Tufts University School of Medicine and a BA in International Relations and Community Health from Tufts."],
  None),
 ("matt-theis", "Matt Theis", "Managing Director, Connect", "matt-theis.jpg",
  ["Matt leads Connect, Dimagi's platform for delivering and verifying frontline work at scale. He brings a background in software development, engineering, and program management, with prior roles spanning aerospace and large-scale technology.",
   "He holds a BS in Aerospace and Astronautical Engineering from MIT."],
  None),
 ("lilian-rush-olson", "Lily Rush Olson", "Co-Managing Director, US Solutions", "lily-rush-olson.jpg",
  ["Lily co-leads Dimagi's US Solutions division, shaping strategy and partnerships for public health programs across the country. She was part of the team that brought Dimagi's global health expertise to the US market in response to COVID-19, and began her career building community health technology, including data systems work with Calcutta Kids in India."],
  None),
 ("sarah-sagan", "Sarah Sagan", "Co-Managing Director, US Solutions", "sarah-sagan.jpg",
  ["Sarah co-leads US Solutions, overseeing delivery, technology, and technical strategy for Dimagi's US Health Division and keeping it aligned with global strategy. With Dimagi since 2014, she was a key figure in the company's COVID-19 response and its entry into the US public health market."],
  None),
 ("kelly-collins", "Kelly Collins", "Managing Director, SureAdhere", "kelly-collins.jpg",
  ["An infectious disease epidemiologist and social entrepreneur, Kelly co-founded and led SureAdhere before its acquisition by Dimagi, and now leads the digital adherence team. Her 12+ years evaluating digital adherence across 25 countries have produced research published in The Lancet and JAMA that informed WHO tuberculosis treatment guidelines.",
   "She holds a PhD in Global Health from UC San Diego and an MPH in Epidemiology."],
  None),
]

NAV = '''<a class="skip-link" href="#main">Skip to content</a>

<div class="nav-wrap">
  <div class="container">
    <nav class="primary" data-nav-base="../../../">
      <a class="logo" href="../../../index.html">
        <img class="logo-img invert" src="../../../assets/dimagi-logo.png" alt="Dimagi">
      </a>
      <div class="nav-links">
        <a href="#">Products</a>
        <a href="#">Professional Services</a>
        <a href="../../../company/about/index.html" class="nav-active">Company</a>
        <a href="../../../contact/index.html">Contact Us</a>
      </div>
      <div class="nav-cta">
        <a class="btn btn-primary" href="../../../sign-in/index.html">Sign In</a>
      </div>
    </nav>
  </div>
</div>'''

FOOTER = '''<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img class="footer-logo" src="../../../assets/dimagi-logo.png" alt="Dimagi">
        <p>Building and scaling sustainable, high-impact digital solutions that amplify frontline work.</p>
        <div class="footer-social">
          <a href="https://www.linkedin.com/company/dimagi" target="_blank" rel="noopener" class="footer-social-link linkedin" aria-label="Follow Dimagi on LinkedIn">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.94 5a1.94 1.94 0 1 1-3.88 0 1.94 1.94 0 0 1 3.88 0zM3.4 8.4h3.1V21H3.4V8.4zm5.06 0h2.97v1.72h.04c.41-.78 1.42-1.6 2.93-1.6 3.13 0 3.71 2.06 3.71 4.74V21h-3.1v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94V21H8.46V8.4z"/></svg>
          </a>
          <a href="https://www.youtube.com/channel/UCt8JcRhWywkVJRR_YWv4OhA" target="_blank" rel="noopener" class="footer-social-link youtube" aria-label="Follow Dimagi on YouTube">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.5a3 3 0 0 0-2.1-2.1C19 4.9 12 4.9 12 4.9s-7 0-8.9.5A3 3 0 0 0 1 7.5 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.5a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.5zM9.75 15.5v-7l6 3.5-6 3.5z"/></svg>
          </a>
        </div>
        <div class="footer-certs">
          <a class="footer-cert bcorp" href="https://bcorporation.net/directory/dimagi-inc" target="_blank" rel="noopener" aria-label="Certified B Corporation">
            <img src="../../../assets/images/about/b-corp-logo.png" alt="Certified B Corporation" loading="lazy">
          </a>
          <a class="footer-cert climate" href="https://www.climateneutral.org/brand/dimagi" target="_blank" rel="noopener" aria-label="Climate Neutral Certified">
            <img src="../../../assets/images/about/climate-neutral-badge.png" alt="Climate Neutral Certified" loading="lazy">
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Products</h5>
        <ul>
          <li><a href="https://connect.dimagi.com/" target="_blank" rel="noopener">Connect</a></li>
          <li><a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a></li>
          <li><a href="https://dimagi.com/sureadhere/" target="_blank" rel="noopener">SureAdhere</a></li>
          <li class="footer-sublabel">Dimagi Labs</li>
          <li><a href="https://www.openchatstudio.com/" target="_blank" rel="noopener">Open Chat Studio</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Professional Services</h5>
        <ul>
          <li><a href="../../../professional-services/global-services/index.html">Global Services</a></li>
          <li><a href="../../../professional-services/united-states/index.html">United States</a></li>
          <li><a href="../../../professional-services/india/index.html">India</a></li>
          <li><a href="../../../professional-services/research-data/index.html">Research &amp; Data</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="../../../company/about/index.html">About Us</a></li>
          <li><a href="../../../company/our-approach/index.html">Our Approach</a></li>
          <li><a href="../../../blog/index.html">Blog</a></li>
          <li><a href="../../../podcast/index.html">Podcast</a></li>
          <li><a href="../../../company/careers/index.html">Careers</a></li>
          <li><a href="../../../awards/index.html">Awards</a></li>
          <li><a href="../../../press/index.html">Press &amp; Coverage</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <ul>
          <li><a href="../../../contact/index.html">Contact Us</a></li>
        </ul>
        <div class="footer-news">
          <p class="footer-news-label">Subscribe to our newsletter</p>
          <form class="footer-news-form" onsubmit="return false;">
            <input class="footer-news-input" type="email" name="email" placeholder="Your email" aria-label="Your email address" required>
            <button class="btn btn-primary footer-news-btn" type="submit">Subscribe</button>
          </form>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 DIMAGI, INC.</span>
      <div class="footer-legal">
        <a href="../../../legal/privacy-policy/index.html">Privacy</a>
        <a href="../../../legal/terms-of-service/index.html">Terms</a>
        <a href="../../../legal/business-agreement/index.html">Business Agreement</a>
        <a href="../../../legal/acceptable-use/index.html">Acceptable Use</a>
        <a href="../../../legal/financial-conflict/index.html">Financial Conflict</a>
        <a href="../../../legal/transparency-coverage/index.html">Transparency</a>
        <a href="https://dimagi.safebase.us/" target="_blank" rel="noopener">Trust Center</a>
      </div>
    </div>
  </div>
</footer>
<script src="../../../assets/js/nav.js?v=7"></script>'''

STYLE = '''<style>
/* ── Leadership bio page ── */
.bio-main { background: #fff; }
.bio-hero { background: #f5f7ff; padding: 40px 0 56px; }
.bio-back { display: inline-flex; align-items: center; gap: 6px; font-size: .92rem; color: #3843D0; font-weight: 500; margin-bottom: 28px; }
.bio-back:hover { text-decoration: underline; }
.bio-head { display: grid; grid-template-columns: 200px 1fr; gap: 40px; align-items: center; }
.bio-photo img { width: 200px; height: 200px; object-fit: cover; border-radius: 16px; box-shadow: 0 10px 34px rgba(22,0,109,.12); }
.bio-name { font-weight: 300; font-size: clamp(1.9rem, 1.3rem + 2vw, 2.6rem); letter-spacing: -0.01em; margin: 0 0 8px; color: #16006D; }
.bio-title { font-size: 1.05rem; color: #5f6a7d; font-weight: 500; }
.bio-body { max-width: 720px; margin: 48px auto 8px; }
.bio-body p { font-size: 1.06rem; line-height: 1.78; color: #36404f; margin: 0 0 20px; }
.bio-podcast { display: inline-flex; align-items: center; gap: 14px; margin-top: 12px; padding: 12px 16px; border: 1px solid #e6e3f5; border-radius: 12px; background: #f9f7ff; max-width: 720px; }
.bio-podcast img { width: 56px; height: 56px; object-fit: cover; border-radius: 8px; }
.bio-podcast .lp-label { font-weight: 500; color: #16006D; }
.bio-cta { max-width: 720px; margin: 32px auto 0; }
@media (max-width: 640px) {
  .bio-head { grid-template-columns: 1fr; gap: 22px; text-align: center; justify-items: center; }
  .bio-photo img { width: 168px; height: 168px; }
}
</style>'''

PAGE_TMPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{name} | Dimagi</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://dimagi.com/company/about/{slug}/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="Dimagi">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://dimagi.com/company/about/{slug}/">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://dimagi.com/assets/images/about/{photo}">
<meta property="og:image:alt" content="{name}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://dimagi.com/assets/images/about/{photo}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../../assets/styles.css?v=16">
{style}
</head>
<body>

{nav}

<main id="main" class="bio-main">

  <section class="bio-hero">
    <div class="container">
      <a class="bio-back" href="../index.html#leadership"><span aria-hidden="true">&larr;</span> Back to leadership</a>
      <div class="bio-head">
        <div class="bio-photo"><img src="../../../assets/images/about/{photo}" alt="{name}"></div>
        <div>
          <h1 class="bio-name">{name}</h1>
          <div class="bio-title">{title}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="bio-body">
        {body}
      </div>
      {extra}
      <div class="bio-cta">
        <a class="btn btn-ghost" href="../index.html#leadership">&larr; Meet the rest of the team</a>
      </div>
    </div>
  </section>

</main>

{footer}
</body>
</html>
'''

STUB_TMPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{name} | Dimagi</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://dimagi.com/company/about/{slug}/">
<meta http-equiv="refresh" content="0; url=../../company/about/{slug}/index.html">
<script>window.location.replace('../../company/about/{slug}/index.html');</script>
</head>
<body>
<p>Redirecting to <a href="../../company/about/{slug}/index.html">{name}</a>&hellip;</p>
</body>
</html>
'''

def esc(s):
    return html.escape(s, quote=True)

made = []
for slug, name, title, photo, paras, extra_kind in LEADERS:
    body = "\n        ".join(f"<p>{esc(p)}</p>" for p in paras)
    meta_desc = f"{name}, {title} at Dimagi. {paras[0]}"
    meta_desc = esc(meta_desc[:185].rsplit(' ', 1)[0])
    if extra_kind == "podcast":
        href, img, label = PODCAST
        extra = (f'<a class="bio-podcast" href="{href}">'
                 f'<img src="{img}" alt="High-Impact Growth podcast">'
                 f'<span class="lp-label">{esc(label)} <span aria-hidden="true">&rarr;</span></span></a>')
    else:
        extra = ""
    pagedir = os.path.join(ROOT, "company", "about", slug)
    os.makedirs(pagedir, exist_ok=True)
    page = PAGE_TMPL.format(name=esc(name), title=esc(title), slug=slug, photo=photo,
                            body=body, extra=extra, meta_desc=meta_desc,
                            nav=NAV, footer=FOOTER, style=STYLE)
    open(os.path.join(pagedir, "index.html"), "w").write(page)

    stubdir = os.path.join(ROOT, "person", slug)
    os.makedirs(stubdir, exist_ok=True)
    open(os.path.join(stubdir, "index.html"), "w").write(
        STUB_TMPL.format(name=esc(name), slug=slug))
    made.append(slug)

# Repoint the About-page name links: external /person/<slug>/ -> internal bio page
about = os.path.join(ROOT, "company", "about", "index.html")
htmltext = open(about).read()
before = htmltext
for slug, *_ in LEADERS:
    htmltext = htmltext.replace(
        f'href="https://dimagi.com/person/{slug}/" target="_blank" rel="noopener"',
        f'href="{slug}/index.html"')
open(about, "w").write(htmltext)
relinked = before.count('dimagi.com/person/') - htmltext.count('dimagi.com/person/')

print(f"bio pages + stubs generated: {len(made)}")
print(f"About-page links repointed: {relinked}")
print("remaining external /person/ links in About:", htmltext.count('dimagi.com/person/'))
