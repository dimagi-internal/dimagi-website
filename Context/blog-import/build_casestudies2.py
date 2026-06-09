# -*- coding: utf-8 -*-
"""Build 9 migrated dimagi.com case-study pages as dated Dimagi blog articles.
Source facts: Context/blog-import/casestudy_pdfs/*.txt (real PDFs). No fabricated numbers.
Convention mirrors the prior batch (e.g. blog/naatal-mbay-commcare-agricultural-support).
"""
import os, html, urllib.parse

BLOG = os.path.join(os.path.dirname(__file__), "..", "..", "blog")
BLOG = os.path.abspath(BLOG)

SKELETON = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<link rel="icon" type="image/png" href="../../assets/favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>@@TITLE_ESC@@ | Dimagi</title>
<meta name="description" content="@@DESC_ESC@@">
<meta name="author" content="Dimagi">
<link rel="canonical" href="@@ORIG_URL@@">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:locale" content="en_US">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="Dimagi">
<meta property="og:url" content="@@ORIG_URL@@">
<meta property="og:title" content="@@TITLE_ESC@@">
<meta property="og:description" content="@@DESC_ESC@@">
<meta property="og:image" content="https://dimagi.com/assets/images/@@SLUG@@/cover.jpg">
<meta property="og:image:width" content="@@COVER_W@@">
<meta property="og:image:height" content="@@COVER_H@@">
<meta property="og:image:alt" content="@@COVER_ALT_ESC@@">
<meta property="article:published_time" content="@@DATE_ISO@@">
<meta property="article:author" content="Dimagi">
<meta property="article:section" content="CommCare">
<meta property="article:tag" content="Case Study">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE_ESC@@">
<meta name="twitter:description" content="@@DESC_ESC@@">
<meta name="twitter:image" content="https://dimagi.com/assets/images/@@SLUG@@/cover.jpg">
<meta name="twitter:image:alt" content="@@COVER_ALT_ESC@@">

<!-- Article structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "@@TITLE_JSON@@",
  "description": "@@DESC_JSON@@",
  "image": "https://dimagi.com/assets/images/@@SLUG@@/cover.jpg",
  "datePublished": "@@DATE_ISO@@",
  "dateModified": "@@DATE_ISO@@",
  "author": { "@type": "Organization", "name": "Dimagi" },
  "publisher": {
    "@type": "Organization",
    "name": "Dimagi",
    "logo": { "@type": "ImageObject", "url": "https://dimagi.com/wp-content/uploads/2023/11/dimagi_logo_46.png" }
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "@@ORIG_URL@@" },
  "articleSection": "CommCare",
  "keywords": "@@KEYWORDS_JSON@@"
}
</script>

<!-- Breadcrumb structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://dimagi.com/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://dimagi.com/blog/" },
    { "@type": "ListItem", "position": 3, "name": "@@TITLE_JSON@@" }
  ]
}
</script>

<link rel="preload" as="image" href="../../assets/images/@@SLUG@@/cover.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@200..700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/styles.css?v=15">
<link rel="stylesheet" href="../../assets/article.css?v=10">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>
<div class="reading-progress" aria-hidden="true"><span class="reading-progress-bar"></span></div>

<div class="nav-wrap">
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
</div>

<main id="main" class="article-wrap">

  <!-- Hero -->
  <header class="article-hero">
    <div class="container">
      <div class="article-prose-width">
        <nav class="article-breadcrumb" aria-label="Breadcrumb">
          <a href="../../index.html">Home</a>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          <a href="../index.html">Blog</a>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          <span>@@TITLE_ESC@@</span>
        </nav>
        <h1 class="article-title">@@TITLE_ESC@@</h1>
        <p class="article-deck">@@DECK@@</p>
        <div class="article-byline">
          <div class="article-byline-avatar" aria-hidden="true">D</div>
          <div class="article-byline-meta">
            <span class="article-byline-author">Dimagi</span>
            <span class="article-byline-detail">
              <span>@@DATE_DISPLAY@@</span>
              <span class="dot"></span>
              <span>@@READ@@ min read</span>
            </span>
          </div>
        </div>
        <div class="article-share">
          <span class="article-share-label">Share</span>
          <button class="article-share-btn article-copy" type="button" aria-label="Copy link" data-copy-url="@@ORIG_URL@@">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            <span class="article-copy-label">Copy link</span>
          </button>
          <a class="article-share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url=@@ORIG_URL_ENC@@" target="_blank" rel="noopener" aria-label="Share on LinkedIn">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.25 8h4.5v13H.25V8zM8 8h4.3v1.78h.06c.6-1.13 2.07-2.32 4.26-2.32 4.56 0 5.4 3 5.4 6.9V21h-4.5v-5.7c0-1.36-.02-3.1-1.9-3.1-1.9 0-2.18 1.48-2.18 3v5.8H8V8z"/></svg>
            LinkedIn
          </a>
          <a class="article-share-btn" href="https://twitter.com/intent/tweet?url=@@ORIG_URL_ENC@@&amp;text=@@TITLE_URLENC@@" target="_blank" rel="noopener" aria-label="Share on X">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 1.5h3.3l-7.2 8.2L23.7 22.5h-6.6l-5.2-6.8-6 6.8H2.6l7.7-8.8L2 1.5h6.8l4.7 6.2 5.4-6.2zm-1.2 19h1.8L7.1 3.4H5.2L17.7 20.5z"/></svg>
            X
          </a>
        </div>
      </div>
    </div>
  </header>

  <!-- Cover -->
  <div class="article-cover-wrap">
    <div class="container">
      <figure class="article-cover" style="aspect-ratio:3/2;">
        <img src="../../assets/images/@@SLUG@@/cover.jpg"
             style="width:100%;height:100%;object-fit:cover;object-position:center;"
             width="@@COVER_W@@" height="@@COVER_H@@" fetchpriority="high" decoding="async"
             alt="@@COVER_ALT_ESC@@">
      </figure>
      <p class="article-cover-caption">@@COVER_CAPTION@@</p>
    </div>
  </div>

  <!-- Body -->
  <article class="article-body">
    <div class="container">
      <div class="article-prose-width prose">

@@BODY@@

        <!-- Foot nav -->
        <div class="article-foot">
          <div class="article-foot-label">Filed under</div>
          <div class="article-tags">
@@FILED@@
          </div>
        </div>

      </div>
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

@@RELATED@@

      </div>

      <div class="related-foot">
        <a class="btn btn-primary btn-arrow" href="../index.html">See All Blogs</a>
      </div>
    </div>
  </section>

</main>

<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img class="footer-logo" src="../../assets/dimagi-logo.png" alt="Dimagi">
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
            <img src="../../assets/images/about/b-corp-logo.png" alt="Certified B Corporation" loading="lazy">
          </a>
          <a class="footer-cert climate" href="https://www.climateneutral.org/brand/dimagi" target="_blank" rel="noopener" aria-label="Climate Neutral Certified">
            <img src="../../assets/images/about/climate-neutral-badge.png" alt="Climate Neutral Certified" loading="lazy">
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Products</h5>
        <ul>
          <li><a href="https://connect.dimagi.com/" target="_blank" rel="noopener">Connect</a></li>
          <li><a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a></li>
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
          <li><a href="../../blog/index.html">Blog</a></li>
          <li><a href="../../podcast/index.html">Podcast</a></li>
          <li><a href="../../company/careers/index.html">Careers</a></li>
          <li><a href="../../awards/index.html">Awards</a></li>
          <li><a href="../../press/index.html">Press &amp; Coverage</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <ul>
          <li><a href="../../contact/index.html">Contact Us</a></li>
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
        <a href="../../legal/privacy-policy/index.html">Privacy</a>
        <a href="../../legal/terms-of-service/index.html">Terms</a>
        <a href="../../legal/business-agreement/index.html">Business Agreement</a>
        <a href="../../legal/acceptable-use/index.html">Acceptable Use</a>
        <a href="../../legal/financial-conflict/index.html">Financial Conflict</a>
        <a href="../../legal/transparency-coverage/index.html">Transparency</a>
        <a href="https://dimagi.safebase.us/" target="_blank" rel="noopener">Trust Center</a>
      </div>
    </div>
  </div>
</footer>

<button class="back-to-top" type="button" aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg>
</button>

<script src="../../assets/js/nav.js?v=6"></script>
<script src="../../assets/js/article.js?v=8"></script>
</body>
</html>
"""

# ---- shared cover dims (post-crop) ----
DIMS = {
  "access-madagascar-commcare-remote-health": (610, 407),
  "hmhb-tajikistan-commcare-maternal-child-health": (1144, 763),
  "rti-cambodia-iecd-early-childhood-development": (610, 407),
  "enabling-supportive-supervision-malawi": (936, 624),
  "suaahara-ii-commcare-community-maternal-child-health": (610, 407),
  "smash-mobil-commcare-local-supply-chains": (610, 407),
  "sickle-cell-foundation-ghana-newborn-screening": (610, 407),
  "abt-associates-vectorlink-malaria-control": (610, 407),
  "egpaf-baylor-commcare-hiv-patient-tracking": (610, 407),
}

CC = '<a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a>'

def endcta(h3, p):
    return ('        <div class="article-end-cta">\n'
            '          <h3>%s</h3>\n          <p>%s</p>\n'
            '          <a class="btn btn-indigo btn-arrow" href="../../contact/index.html">Get in touch</a>\n'
            '        </div>') % (h3, p)

def callout(label, num, text):
    return ('        <div class="article-callout">\n'
            '          <div class="article-callout-label">%s</div>\n'
            '          <div class="article-callout-num">%s</div>\n'
            '          <p class="article-callout-text">%s</p>\n        </div>') % (label, num, text)

def quote(q, cite):
    return ('        <blockquote>\n          <p>&ldquo;%s&rdquo;</p>\n'
            '          <cite>%s</cite>\n        </blockquote>') % (q, cite)

# ============ ARTICLES ============
ARTICLES = []

# 1. ACCESS Madagascar
ARTICLES.append(dict(
  slug="access-madagascar-commcare-remote-health",
  orig="https://dimagi.com/case-study/access-madagascar/",
  title="ACCESS Madagascar: CommCare for Health in Remote, Low-Connectivity Settings",
  card_title="ACCESS Madagascar: CommCare for Remote, Low-Connectivity Health",
  deck="How the USAID-funded ACCESS program equipped 3,500 community health volunteers with an offline-first CommCare app, reaching remote Malagasy communities and feeding 779 indicators into the Ministry of Public Health&rsquo;s DHIS2.",
  desc="How the USAID-funded ACCESS program in Madagascar equipped 3,500 community health volunteers with an offline-first CommCare app and fed 779 indicators into the Ministry of Public Health's DHIS2.",
  date_display="Jun 2022", date_iso="2022-06-01", read=4,
  cover_alt="A community health volunteer reviewing case information with community members in rural Madagascar.",
  caption="A community health volunteer reviews case data on CommCare during a community visit in Madagascar.",
  keywords="CommCare, Case Study, Madagascar, community health, ACCESS, MSH, USAID, DHIS2",
  country="Madagascar", sector="Maternal, Newborn &amp; Child Health",
  related=["hmhb-tajikistan-commcare-maternal-child-health","enabling-supportive-supervision-malawi","sickle-cell-foundation-ghana-newborn-screening"],
  body="""        <p class="lead">The Accessible Continuum of Care and Essential Services Sustained (ACCESS) program is a five-year, USAID-funded project led by Management Sciences for Health (MSH) to strengthen Madagascar&rsquo;s health system. Since 2016 it has used {cc} to put job aids, counseling tools, and disease classification in the hands of community health volunteers, even where there is no internet.</p>

        <h2 id="connectivity">Reaching health workers where connectivity runs out</h2>
        <p>Madagascar&rsquo;s 28 million people are spread across 22 regions, and only about a third of the country&rsquo;s 18,000 community health volunteers (CHVs) have reliable internet. Paper forms left the Ministry of Public Health (MOPH) without timely data, so ACCESS needed a tool that worked fully offline. The CommCare app was designed for three tiers of users: those with a smartphone and internet, those with a smartphone but no internet who submit their monthly indicators by SMS, and those without a device who report through a colleague. Every user gets the same experience; only how they sync differs.</p>

        <h2 id="one-app">One app across the continuum of care</h2>
        <p>Originally built for family planning, antenatal care, and children from birth to five, the app expanded as the program grew to include surveillance and rapid-response modules for plague and COVID-19. Its integrated child-care module guides CHVs through the symptoms noted during a consultation, prompts a rapid diagnostic test, and displays job aids based on what is entered, while a stock module tracks medication and auto-generates resupply orders by SMS.</p>

        {quote}

        <h2 id="results">Better testing, better treatment</h2>
        <p>From October 2020 to September 2021, ACCESS studied malaria care for children under five. CHVs using CommCare tested 96% of under-fives with fever for malaria, compared with 78% among CHVs without it, and treated 85% of confirmed cases versus 79%, showing stronger adherence to protocol. The surveillance module, which tracks 16 disease symptoms and three animal-health events, also helped the MOPH detect suspected Rift Valley Fever in the Atsimo Andrefana region in March 2021.</p>

        {callout}

        <p>By April 2022 the app was aggregating data for 774 locations and feeding 779 indicators into the MOPH&rsquo;s DHIS2, with more than 3,500 CHVs using it. As the five-year program prepared to hand the system to the MOPH, Dimagi focused on local hosting and capacity transfer so the tool could be sustained as a government-owned platform.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("CommCare! Grassroots community saves lives through high tech!","Dr. Serge Raharison, Chief of Party, USAID ACCESS Program"),
      callout=callout("Malaria cases tested by CommCare users","96%","CHVs using CommCare tested 96% of children under five with fever for malaria, compared with 78% among CHVs without it, and showed stronger adherence to treatment protocols."),
      endcta=endcta("Running a program in low-connectivity settings?","Talk to our team about how CommCare&rsquo;s offline-first design can reach frontline workers wherever they are.")),
))

# 2. HMHB Tajikistan
ARTICLES.append(dict(
  slug="hmhb-tajikistan-commcare-maternal-child-health",
  orig="https://dimagi.com/case-study/tajikistan/",
  title="Healthy Mother, Healthy Baby: Digitally Transforming Service Delivery in Tajikistan",
  card_title="Healthy Mother, Healthy Baby: Digital Care in Tajikistan",
  deck="How the USAID-funded HMHB Activity used CommCare to digitize Tajikistan&rsquo;s maternal and child health services across 12 districts, from a 2,000-question facility assessment to a suite of frontline apps feeding DHIS2.",
  desc="How the USAID-funded Healthy Mother, Healthy Baby Activity used CommCare to digitize maternal and child health services across 12 districts of Tajikistan, feeding data into DHIS2.",
  date_display="Apr 2022", date_iso="2022-04-01", read=4,
  cover_alt="A health worker in Tajikistan using a CommCare application on a tablet.",
  caption="Healthy Mother, Healthy Baby equips health workers in Tajikistan&rsquo;s Khatlon region with CommCare apps for maternal and child care.",
  keywords="CommCare, Case Study, Tajikistan, maternal and child health, HMHB, Abt Associates, USAID, DHIS2",
  country="Tajikistan", sector="Maternal, Newborn &amp; Child Health",
  related=["access-madagascar-commcare-remote-health","rti-cambodia-iecd-early-childhood-development","suaahara-ii-commcare-community-maternal-child-health"],
  body="""        <p class="lead">The USAID-funded Healthy Mother, Healthy Baby (HMHB) Activity set out to improve maternal and child health in Tajikistan, which has some of the highest rates of maternal and child mortality and child stunting in Central Asia. Led by Abt Associates with the Ministry of Health and Social Protection of the Population (MoHSSP), HMHB uses {cc} to digitize service delivery across 12 districts of the Khatlon region.</p>

        <h2 id="ecosystem">From paper registries to a digital ecosystem</h2>
        <p>Health service data in Tajikistan was largely paper-based, delaying care and clouding decision-making. Starting in September 2020, HMHB built a suite of CommCare applications for health workers and community leaders, with data flowing directly into a DHIS2 instance so managers could act on it quickly. Both CommCare and DHIS2 are open-source &ldquo;global goods&rdquo; used in many countries, giving the MoHSSP a foundation it can sustain.</p>

        <h2 id="apps">A suite of apps for every stage of care</h2>
        <ul>
          <li><strong>Rapid Health Facility Assessment (RHFA):</strong> digitized the WHO&rsquo;s 2,000-plus-question facility assessment; in 2021 it assessed 24 facilities (12 primary health care centers and 12 district hospitals) to baseline planning.</li>
          <li><strong>Continuous Medical Education (CME):</strong> tracks training and skills milestones for health workers and flags who has not completed modules by set dates.</li>
          <li><strong>Knowledge, Access and Practice (KAP):</strong> an anonymous household survey that maps community attitudes and shapes social behavior change priorities.</li>
          <li><strong>Maternal Nutrition and Child Health (MNCH):</strong> a three-part app for community events, antenatal and postpartum tracking with a personalized visit scheduler, and nutrition monitoring for children under five.</li>
        </ul>

        {quote}

        {callout}

        <p>By 2022 the program had more than 600 health workers using the apps, with the community-events module alone reaching 463 users across 380 villages, and the systems were built to scale across all of Tajikistan as the government advances country-wide digitalization and policy reform.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("Together with Dimagi, HMHB is pushing the frontiers of impact in the digital health landscape of Tajikistan.","Clifford Lubitz, Chief of Party, Healthy Mother, Healthy Baby"),
      callout=callout("Question facility assessment, digitized","2,000+","HMHB digitized the WHO&rsquo;s 2,000-plus-question Rapid Health Facility Assessment in CommCare, turning a slow paper process into a baseline managers could use to plan services across Khatlon."),
      endcta=endcta("Strengthening a national health system?","Talk to our team about building a connected CommCare and DHIS2 ecosystem for frontline care.")),
))

# 3. RTI Cambodia IECD
ARTICLES.append(dict(
  slug="rti-cambodia-iecd-early-childhood-development",
  orig="https://dimagi.com/case-study/mhealth-rti/",
  title="USAID Cambodia IECD: CommCare Job Aids Help Young Children Thrive",
  card_title="USAID Cambodia IECD: CommCare Job Aids for Young Children",
  deck="How RTI International used CommCare to digitize community health worker job aids for Cambodia&rsquo;s Integrated Early Childhood Development Activity, registering more than 5,000 households across two provinces.",
  desc="How RTI International used CommCare to digitize community health worker job aids for Cambodia's Integrated Early Childhood Development Activity, registering more than 5,000 households.",
  date_display="May 2022", date_iso="2022-05-01", read=3,
  cover_alt="A community health worker in Cambodia supporting a caregiver and young child.",
  caption="RTI&rsquo;s IECD Activity uses CommCare to help community health workers support caregivers and young children in Cambodia.",
  keywords="CommCare, Case Study, Cambodia, early childhood development, RTI International, USAID, nutrition",
  country="Cambodia", sector="Early Childhood Development",
  related=["suaahara-ii-commcare-community-maternal-child-health","hmhb-tajikistan-commcare-maternal-child-health","access-madagascar-commcare-remote-health"],
  body="""        <p class="lead">RTI International launched the USAID/Cambodia Integrated Early Childhood Development (IECD) Activity in July 2020 to help the country&rsquo;s most vulnerable newborns and young children reach their full potential. Dimagi partnered with RTI to build {cc} job aids that put nurturing-care guidance in the hands of community health workers.</p>

        <h2 id="first-1000-days">A multi-sectoral approach to the first 1,000 days</h2>
        <p>In Cambodia, more than 30% of children aged 3 to 5 are behind on developmental milestones and about 32% of under-fives are stunted. The IECD Activity addresses this holistically, strengthening nutrition services, nutrition-sensitive agriculture and livelihoods, water and sanitation, and responsive caregiving, with an emphasis on the first 1,000 days and on screening for developmental delays early.</p>

        <h2 id="apps">Three apps, one integrated platform</h2>
        <ul>
          <li><strong>Minimum Viable Product (MVP):</strong> the core job aid for community health workers to register households, screen children, run home visits, and create and follow up on referrals.</li>
          <li><strong>Cohort Evaluation (CE):</strong> collects longitudinal impact-evaluation data, linking child and caregiver records within households over time.</li>
          <li><strong>Performance Monitoring Service Protocol (PMSP):</strong> surveys for agriculture, nutrition, and social and behavior change, built on CommCare repeat groups so enumerators only answer the questions that apply to each household.</li>
        </ul>

        {quote}

        {callout}

        <p>After partnering with Dimagi in February 2021 for 14 months of app-building support, RTI moved to formalize a further 18 months to double the number of users, extending the reach of digital job aids that help children with developmental delays get the care they need.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("Within the IECD CommCare app, CHWs have the benefit of less paper-based work, a simpler process for tracking information, and more time for positive interaction with caregivers.","Seng Yeng, M&amp;E Manager, RTI Cambodia"),
      callout=callout("Households registered","5,000+","In 14 months of app-building support, the IECD Activity digitized the registration of more than 5,000 households and 25,000 household members across two provinces in Cambodia."),
      endcta=endcta("Designing job aids for frontline workers?","Talk to our team about turning paper protocols into offline CommCare job aids.")),
))

# 4. Malawi ISS
ARTICLES.append(dict(
  slug="enabling-supportive-supervision-malawi",
  orig="https://dimagi.com/case-study/enabling-supportive-supervision-to-improve-health-outcomes-in-malawi/",
  title="Enabling Supportive Supervision to Improve Health Outcomes in Malawi",
  card_title="Enabling Supportive Supervision to Improve Health Outcomes in Malawi",
  deck="How Malawi&rsquo;s Ministry of Health and Population replaced paper supervision checklists with a CommCare-based digital integrated supportive supervision tool across all 29 districts, made visible through a live dashboard.",
  desc="How Malawi's Ministry of Health and Population replaced paper supervision checklists with a CommCare-based digital integrated supportive supervision tool across all 29 districts.",
  date_display="Sep 2022", date_iso="2022-09-01", read=4,
  cover_alt="A health worker in Malawi assessing a child during a facility visit.",
  caption="Supervisors across Malawi&rsquo;s 29 districts use the CommCare-based digital ISS tool to assess health facilities each quarter.",
  keywords="CommCare, Case Study, Malawi, health systems strengthening, supportive supervision, MoHP, ONSE, DHIS2",
  country="Malawi", sector="Service Delivery",
  related=["access-madagascar-commcare-remote-health","abt-associates-vectorlink-malaria-control","egpaf-baylor-commcare-hiv-patient-tracking"],
  body="""        <p class="lead">The Ministry of Health and Population (MoHP) in Malawi uses a digital integrated supportive supervision (ISS) tool, built by Dimagi on {cc}, to oversee the quality of care across the country&rsquo;s health facilities. Developed in 2018 under the USAID-supported ONSE Health Activity, it is now a standard quarterly supervision, monitoring, and decision-making instrument.</p>

        <h2 id="paper">When paper hides the problems</h2>
        <p>Malawi had paper supervision protocols since the early 2000s, but the lack of visibility meant decision-makers were not truly in control of the programs they were accountable for. Action items were hard to track, bottlenecks went unresolved, and printing checklists strained the ministry budget. Together, these gaps put a heavy burden on system performance.</p>

        <h2 id="tablets">A tablet in every district</h2>
        <p>Each of Malawi&rsquo;s 29 districts is equipped with five tablets preloaded with the ISS app. Supervisors from district health management teams use them to conduct quarterly supervision across government, Christian Health Association of Malawi (CHAM), and selected private facilities, fully offline, syncing when they have connectivity. The app&rsquo;s 12 modules guide supervisors through approved checklists; when a response falls short of the desired state, the app flags it yellow or red and prompts an action item to close the gap. Data flows to an Apache Superset dashboard and integrates with DHIS2 to eliminate duplicate reporting.</p>

        {quote}

        {callout}

        <p>The visibility has had concrete results. Dowa District Hospital used ISS dashboard data to engage members of parliament and local partners, who pooled resources to fix long-standing waste-management and water problems at facilities like Chankhungu. Between 2018 and mid-2022 Dimagi transferred hosting and app-building skills to the MoHP&rsquo;s Digital Health Division so the tool can be sustained as a government-owned platform.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("The deployment of the digital ISS tool and dashboard has greatly empowered me as National ISS Coordinator to identify zones and districts that are lagging behind in facility supervision and target follow-up support more efficiently.","Dr. Malangizo Mbewe, Deputy Director and National ISS Coordinator, MoHP"),
      callout=callout("Districts supervised","29","Every district in Malawi now runs quarterly supportive supervision on the CommCare-based ISS tool, with results visible to national decision-makers through a live dashboard."),
      endcta=endcta("Strengthening supervision and quality of care?","Talk to our team about digitizing supportive supervision with CommCare.")),
))

# 5. Suaahara II
ARTICLES.append(dict(
  slug="suaahara-ii-commcare-community-maternal-child-health",
  orig="https://dimagi.com/case-study/suaahara-ii-commcare-for-community-based-maternal-child-health/",
  title="Suaahara II: CommCare for Community-Based Maternal &amp; Child Health in Nepal",
  card_title="Suaahara II: CommCare for Maternal &amp; Child Health in Nepal",
  deck="How the seven-year, USAID-funded Suaahara II program used CommCare to register 2 million households and reach 10 million people across 42 of Nepal&rsquo;s 77 districts.",
  desc="How the seven-year, USAID-funded Suaahara II program used CommCare to register 2 million households and reach 10 million people across 42 of Nepal's 77 districts.",
  date_display="Mar 2021", date_iso="2021-03-01", read=4,
  cover_alt="A frontline worker in Nepal counseling a mother during a household visit.",
  caption="Suaahara II frontline workers use CommCare to register households and counsel mothers across rural Nepal.",
  keywords="CommCare, Case Study, Nepal, nutrition, Suaahara, USAID, maternal and child health, Helen Keller",
  country="Nepal", sector="Nutrition",
  related=["rti-cambodia-iecd-early-childhood-development","access-madagascar-commcare-remote-health","hmhb-tajikistan-commcare-maternal-child-health"],
  body="""        <p class="lead">Suaahara II (SII) is a seven-year, USAID-funded program that uses a household-based approach to improve the nutrition of pregnant and lactating women and children under two across 42 of Nepal&rsquo;s 77 districts. Building on lessons from Suaahara I, the consortium chose {cc} to give frontline workers the timely, targeted data they were missing.</p>

        <h2 id="1000-day">Finding the 1,000-day households</h2>
        <p>The program needed to identify which households were in the critical 1,000-day window between conception and a child&rsquo;s second birthday, collect regular data on their behaviors, and make it instantly usable for field staff. SII built three connected CommCare applications:</p>
        <ul>
          <li><strong>Community Mapping Census:</strong> a door-to-door roster of every household, used to prioritize visits and send stage-based SMS messages.</li>
          <li><strong>Monitoring Tools:</strong> follows 1,000-day mothers through pregnancy, the first six months, and months 7 to 24, tracking targets like antenatal visits and iron-folic-acid intake.</li>
          <li><strong>Job Aid:</strong> gives community nutrition facilitators situation-appropriate counseling scripts for each household visit.</li>
        </ul>

        {quote}

        {callout}

        <p>The investment paid off beyond the numbers. In 2017 SII won the grand prize in USAID&rsquo;s Innovation to Action, which partners tied directly to its use of CommCare, and when COVID-19 reached Nepal in 2020, the existing database of phone numbers let the program pivot to tele-counseling and SMS to keep care going.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("CommCare is amazing. It has helped us to collect high-volume information easily and also in the management and monitoring of a huge amount of staff spread across a huge geographical area.","Bharat Sarma Prasai, Program Coordinator, Suaahara II"),
      callout=callout("Households registered","2 million","Between December 2016 and December 2020, Suaahara II&rsquo;s 1,500 frontline workers used CommCare to register 2 million households and 10 million Nepali residents, including about 200,000 women in the 1,000-day window."),
      endcta=endcta("Running a large community health program?","Talk to our team about scaling household-level data collection with CommCare.")),
))

# 6. SMASH Mobil
ARTICLES.append(dict(
  slug="smash-mobil-commcare-local-supply-chains",
  orig="https://dimagi.com/case-study/smash-mobil-commcare-for-improving-local-supply-chains/",
  title="SMASH Mobil: CommCare for Improving Local Supply Chains in Haiti",
  card_title="SMASH Mobil: CommCare for Local Supply Chains in Haiti",
  deck="How the SMASH program built SMASH Mobil on CommCare to track Haiti&rsquo;s sorghum supply chain end to end, helping train 7,104 smallholder farmers and lift their revenue by 78%.",
  desc="How the SMASH program built SMASH Mobil on CommCare to track Haiti's sorghum supply chain end to end, helping train 7,104 smallholder farmers and lift revenue by 78%.",
  date_display="Aug 2018", date_iso="2018-08-01", read=3,
  cover_alt="A field agent in Haiti recording crop data on a tablet with a farmer.",
  caption="SMASH Mobil, built on CommCare, tracks Haiti&rsquo;s sorghum supply chain from planting to delivery.",
  keywords="CommCare, Case Study, Haiti, agriculture, supply chain, SMASH, BRANA, RTI International",
  country="Haiti", sector="Agriculture",
  related=["abt-associates-vectorlink-malaria-control","access-madagascar-commcare-remote-health","suaahara-ii-commcare-community-maternal-child-health"],
  body="""        <p class="lead">In 2013, the Brasserie Nationale d&rsquo;Ha&iuml;ti (BRANA, a Heineken subsidiary) launched the Smallholder Alliance for Sorghum in Haiti (SMASH) to build a local sorghum supply chain. In 2016, SMASH partnered with RTI International and Dimagi to build SMASH Mobil on {cc}, an Android-based system that monitors the program in near real time, from land preparation to grain delivery.</p>

        <h2 id="field-report">Closing the gap between the field and the report</h2>
        <p>BRANA had imported 100% of its ingredients until 2011, and rebuilding a local supply chain meant working with smallholder farmers in a country where the UN estimates 59% of people live below the poverty line. SMASH Mobil was designed to close the discrepancy between what was happening in the field and what was being reported, while supporting monitoring and evaluation.</p>

        <h2 id="planting-to-brew">Tracking sorghum from planting to brew house</h2>
        <ul>
          <li><strong>Supplier Relationship Management (SRM):</strong> tracks suppliers from first contact through field health monitoring, technical advice, training attendance, and demo plots, even helping detect crop infestations early.</li>
          <li><strong>Supply Chain Management (SCM):</strong> runs from purchase through inventory, warehousing, transport logistics, and post-harvest quality assurance.</li>
          <li><strong>Reporting and visual analytics:</strong> aggregates the data into an interactive Tableau dashboard and CommCare&rsquo;s built-in reports so managers and shareholders can monitor progress in near real time.</li>
        </ul>

        {callout}

        <p>SMASH Mobil also cut the time agents spent on paper reports from 30 minutes to under 3 minutes per form, freeing agronomists to focus on training and support. Data-driven decision-making, once a foreign concept for the program, became an everyday reality.</p>

{endcta}""".format(
      cc=CC,
      callout=callout("Smallholder farmers trained","7,104","Since 2013 SMASH has trained 7,104 smallholder farmers in improved sorghum production, with farmers seeing a 57% increase in yields and a 78% increase in revenue from sorghum."),
      endcta=endcta("Building a supply chain with smallholders?","Talk to our team about tracking agricultural value chains end to end with CommCare.")),
))

# 7. Sickle Cell Foundation of Ghana
ARTICLES.append(dict(
  slug="sickle-cell-foundation-ghana-newborn-screening",
  orig="https://dimagi.com/case-study/sickle-cell-foundation-commcare-for-mitigating-child-deaths-from-hereditary-disease/",
  title="Sickle Cell Foundation of Ghana: CommCare for Newborn Screening",
  card_title="Sickle Cell Foundation of Ghana: CommCare for Newborn Screening",
  deck="How the Sickle Cell Foundation of Ghana digitized its National Newborn Screening Program on CommCare, registering more than 12,500 newborns and making sure no child slips through follow-up.",
  desc="How the Sickle Cell Foundation of Ghana digitized its National Newborn Screening Program on CommCare, registering more than 12,500 newborns and tightening follow-up.",
  date_display="Jun 2019", date_iso="2019-06-01", read=4,
  cover_alt="A nurse in Ghana registering a mother and newborn on a mobile device.",
  caption="Nurses screen newborns for sickle cell disease and register them in CommCare at sites across Ghana.",
  keywords="CommCare, Case Study, Ghana, newborn screening, sickle cell disease, Sickle Cell Foundation, Novartis",
  country="Ghana", sector="Maternal, Newborn &amp; Child Health",
  related=["egpaf-baylor-commcare-hiv-patient-tracking","enabling-supportive-supervision-malawi","access-madagascar-commcare-remote-health"],
  body="""        <p class="lead">Every year, more than 400,000 children are born with sickle cell disease (SCD), three-quarters of them in sub-Saharan Africa, and the WHO estimates that 70% of SCD deaths are preventable with early detection and care. Since 2017, Dimagi has partnered with the Sickle Cell Foundation of Ghana (SCFG) to digitize the National Newborn Screening Program on {cc}.</p>

        <h2 id="lost">Found at birth, lost to follow-up</h2>
        <p>In countries across Africa, 50 to 90% of undiagnosed children with SCD die before age five. Babies are screened at birth or at their first immunization visit, but the hard part is finding the family again once lab results come back. With paper records, it was difficult to know how well follow-up was being handled, and cases could fall through the cracks.</p>

        {quote}

        <h2 id="smart-agenda">A smart agenda that closes the loop</h2>
        <p>The SCFG app replaced paper across the whole workflow, from registering samples and family contacts, to tracking samples to the lab in Accra, to distributing results and enrolling presumptive cases into specialized care at Komfo Anokye Teaching Hospital. A built-in &ldquo;smart agenda&rdquo; makes sure health workers follow through on every child: a verified user must manually close each case and give a reason, and the app will not let a case be marked lost to follow-up until six months have passed since the test result.</p>

        {callout}

        <p>The application is run by a small team of 40 nurses, a nurse coordinator, three lab technicians, and supervision staff, and is intended to grow into a comprehensive set of SCD tools across Ghana. Universal newborn screening, the SCFG estimates, could save the lives of up to 9 million newborns in sub-Saharan Africa before 2050.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("Screening is currently established at 40 sites, but reaches only about 4 percent of all newborns.","Prof. Kwaku Ohene-Frempong, President, Sickle Cell Foundation of Ghana"),
      callout=callout("Newborns registered","12,500+","Within 18 months of launching in November 2017, the CommCare app had registered more than 12,500 newborns across six sites in two districts of Ghana, with more added every day."),
      endcta=endcta("Digitizing a screening or registry program?","Talk to our team about building reliable patient tracking and follow-up on CommCare.")),
))

# 8. Abt Associates VectorLink
ARTICLES.append(dict(
  slug="abt-associates-vectorlink-malaria-control",
  orig="https://dimagi.com/case-study/abt-associates-vectorlink/",
  title="Abt Associates VectorLink: CommCare for Reducing Malaria",
  card_title="Abt Associates VectorLink: CommCare for Reducing Malaria",
  deck="How Dimagi has supported the PMI VectorLink indoor residual spraying program since 2014, running two CommCare apps across 17 countries and eight languages to keep spray campaigns on target.",
  desc="How Dimagi has supported the PMI VectorLink indoor residual spraying program since 2014, running two CommCare apps across 17 countries and eight languages to keep malaria spray campaigns on target.",
  date_display="Aug 2021", date_iso="2021-08-01", read=4,
  cover_alt="An indoor residual spraying team in protective gear preparing for a malaria campaign.",
  caption="PMI VectorLink spray teams report daily progress through CommCare across 17 countries in Africa.",
  keywords="CommCare, Case Study, malaria, indoor residual spraying, PMI VectorLink, Abt Associates, infectious disease",
  country="Multiple countries", sector="Infectious Disease Prevention &amp; Control",
  related=["egpaf-baylor-commcare-hiv-patient-tracking","enabling-supportive-supervision-malawi","access-madagascar-commcare-remote-health"],
  body="""        <p class="lead">Africa accounts for over 90% of the world&rsquo;s roughly 400,000 annual malaria deaths, and indoor residual spraying (IRS) is one of the WHO&rsquo;s two most effective forms of vector control. In 2014, Dimagi joined the U.S. President&rsquo;s Malaria Initiative (PMI) and Abt Associates to build the mHealth backbone of the PMI VectorLink IRS program on {cc}.</p>

        <h2 id="race">Spray campaigns are a race against the season</h2>
        <p>IRS teams of spray operators and supervisors work in remote areas with limited connectivity, tight implementation windows, and large seasonal teams, all while collecting data that demands immediate follow-up. Enough structures have to be sprayed in a given area before the malaria season for the campaign to work, so monitoring daily progress is vital.</p>

        <h2 id="one-system">One system, 17 countries, eight languages</h2>
        <ul>
          <li>A supervisory application with five compliance checklists and a data-collection verification form.</li>
          <li>An SMS progress-monitoring tracker: team leaders send a structured daily SMS with the number of sprayers, structures found, structures sprayed, and insecticide units used, routed through Telerivet into CommCare.</li>
          <li>Daily email reports to Abt staff, supervisors, and government stakeholders, plus conditional alerts that ping a supervisor automatically if a site fails to report.</li>
        </ul>
        <p>Two master applications feed 17 country domains translated into eight languages, each customized with lookup tables.</p>

        {quote}

        {callout}

        <p>When COVID-19 made in-person training impossible in 2020, Dimagi set up three new countries remotely, conducting training in English, French, and Portuguese. Each year the team revises the applications with Abt Associates to keep campaigns efficient and on target.</p>

{endcta}""".format(
      cc=CC,
      quote=quote("The CommCare application has contributed to the improvement in speed of availability of vector control data and has enhanced IRS field supervision.","Albert Acquaye, Senior Associate, Abt Associates"),
      callout=callout("Countries across Africa","17","Dimagi supports the PMI VectorLink mHealth system in 17 countries across Africa. In 2020, with roughly 1,931 users configured, the broader PMI AIRS program helped protect an estimated 21.3 million people from malaria."),
      endcta=endcta("Coordinating a multi-country campaign?","Talk to our team about running large, time-sensitive field campaigns on CommCare.")),
))

# 9. EGPAF & Baylor Lesotho
ARTICLES.append(dict(
  slug="egpaf-baylor-commcare-hiv-patient-tracking",
  orig="https://dimagi.com/case-study/egpaf-baylor-college-of-medicine-commcare-for-hiv-patient-tracking-and-appointment-reminders/",
  title="EGPAF &amp; Baylor in Lesotho: CommCare for HIV Patient Tracking",
  card_title="EGPAF &amp; Baylor in Lesotho: CommCare for HIV Patient Tracking",
  deck="How EGPAF-Lesotho and Dimagi built a CommCare patient-tracking and SMS appointment-reminder system that kept 78% of clinic appointments on schedule and cut patients lost to follow-up to just 3%.",
  desc="How EGPAF-Lesotho and Dimagi built a CommCare patient-tracking and SMS appointment-reminder system that kept 78% of clinic appointments on schedule and cut patients lost to follow-up to 3%.",
  date_display="Nov 2020", date_iso="2020-11-01", read=4,
  cover_alt="A health worker in Lesotho updating patient records on a mobile phone.",
  caption="EGPAF-Lesotho health workers use CommCare to track HIV patients and send SMS appointment reminders.",
  keywords="CommCare, Case Study, Lesotho, HIV, EGPAF, Baylor, PEPFAR, patient tracking, appointment reminders",
  country="Lesotho", sector="Infectious Disease Prevention &amp; Control",
  related=["abt-associates-vectorlink-malaria-control","enabling-supportive-supervision-malawi","sickle-cell-foundation-ghana-newborn-screening"],
  body="""        <p class="lead">Lesotho has one of the highest HIV incidence rates in the world, with 340,000 people living with HIV as of 2018. With support from PEPFAR, the Elizabeth Glaser Pediatric AIDS Foundation (EGPAF)-Lesotho and Dimagi built a {cc} patient-tracking and appointment-reminder system to keep patients in care across HIV, TB, and maternal and child health programs.</p>

        <h2 id="cascade">Keeping patients in the cascade of care</h2>
        <p>An interruption in antiretroviral therapy (ART) can be nearly as harmful as stopping treatment, and defaulting drives both poorer outcomes and higher costs. Operational data was collected by hand with long delays, duplicate patient records doubled tracking effort, and migrant populations who self-transferred between facilities were easily mistaken for defaulters.</p>

        <h2 id="reminders">Reminders, tracking, and transfers</h2>
        <p>The app tracks each patient through the care cycle with a unique ID and GPS, and automatically sends SMS reminders three days before an appointment and three days after a missed one. A second version, launched in January 2019, added bulk updates so a whole Community ART Group could be updated in one form, and transfer tracking so patients moving between facilities or districts, sometimes across the border into South Africa, stay in care rather than appearing to default.</p>

        {callout}

        <p>The pilot began in 2016 in Berea and Leribe, scaled to the lowlands districts in 2017, and reached all of Lesotho&rsquo;s districts by 2018. In 2020, Dimagi worked with Baylor College of Medicine Children&rsquo;s Foundation to transfer two districts to its ETHICS program, and during the national COVID-19 lockdown the system&rsquo;s data helped plan drug ordering and multi-month dispensing to keep patients safe.</p>

{endcta}""".format(
      cc=CC,
      callout=callout("Patients lost to follow-up","3%","By 2019 the system had 286,808 clients registered and was sending about 1,520 SMS reminders a day, keeping 78% of appointments on schedule and cutting patients lost to follow-up to just 3%."),
      endcta=endcta("Reducing loss to follow-up in your program?","Talk to our team about patient tracking and SMS reminders on CommCare.")),
))

# ============ render ============
def esc(s):
    return html.escape(s, quote=True)
def jsonesc(s):
    # for JSON string context: unescape HTML entities to plain, escape quotes/backslashes
    t = html.unescape(s)
    return t.replace('\\','\\\\').replace('"','\\"')

AMAP = {a['slug']: a for a in ARTICLES}

def related_html(slugs):
    out = []
    for s in slugs:
        a = AMAP[s]; w,h = DIMS[s]
        out.append(
          '        <a class="related-card" href="../%s/index.html">\n'
          '          <div class="related-card-thumb">\n'
          '            <img src="../../assets/images/%s/cover.jpg" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">\n'
          '          </div>\n'
          '          <div class="related-card-body">\n'
          '            <div class="related-card-cat">CommCare</div>\n'
          '            <h3 class="related-card-title">%s</h3>\n'
          '            <div class="related-card-footer">\n'
          '              <span class="related-card-date">%s</span>\n'
          '              <span class="related-card-link">Read</span>\n'
          '            </div>\n'
          '          </div>\n'
          '        </a>' % (s, s, w, h, esc(html.unescape(a['card_title'])), a['card_title'], a['date_display']))
    return "\n\n".join(out)

def filed_html(a):
    tags = ["CommCare","Case Study", a['country'], a['sector']]
    return "\n".join('            <span class="article-tag">%s</span>' % t for t in tags)

for a in ARTICLES:
    w,h = DIMS[a['slug']]
    page = SKELETON
    repl = {
      "@@SLUG@@": a['slug'],
      "@@ORIG_URL@@": a['orig'],
      "@@ORIG_URL_ENC@@": urllib.parse.quote(a['orig'], safe=''),
      "@@TITLE_ESC@@": a['title'],            # title already uses &amp; etc where needed
      "@@TITLE_JSON@@": jsonesc(a['title']),
      "@@TITLE_URLENC@@": urllib.parse.quote(html.unescape(a['title']), safe=''),
      "@@DESC_ESC@@": esc(a['desc']),
      "@@DESC_JSON@@": jsonesc(a['desc']),
      "@@DECK@@": a['deck'],
      "@@DATE_DISPLAY@@": a['date_display'],
      "@@DATE_ISO@@": a['date_iso'],
      "@@READ@@": str(a['read']),
      "@@COVER_W@@": str(w), "@@COVER_H@@": str(h),
      "@@COVER_ALT_ESC@@": esc(a['cover_alt']),
      "@@COVER_CAPTION@@": a['caption'],
      "@@KEYWORDS_JSON@@": jsonesc(a['keywords']),
      "@@FILED@@": filed_html(a),
      "@@BODY@@": a['body'],
      "@@RELATED@@": related_html(a['related']),
    }
    for k,v in repl.items():
        page = page.replace(k, v)
    d = os.path.join(BLOG, a['slug'])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", a['slug'], "(%s, %dx%d)" % (a['date_display'], w, h))

print("\nDONE: %d articles" % len(ARTICLES))
