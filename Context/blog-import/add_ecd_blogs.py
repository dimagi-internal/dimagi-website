# One-off: add two backdated ECD case-study blogs, embed the FCW video, and
# wire both into the listing grid + sitemap. Surgical (no global taxonomy rebuild).
#   1. MAHAY Mikolo ECD cluster-RCT, Madagascar (BMC Public Health, Sep 2024)
#   2. Ugunja Community Resource Center CommCare ECD app, Kenya (Saving Brains, 2014)
# Run:  python3 Context/blog-import/add_ecd_blogs.py
import os, re, json, shutil, html as _html

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
BLOG = os.path.join(ROOT, "blog")
IMG  = os.path.join(ROOT, "assets", "images")
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "gen.py")).read())  # build(), render(), esc(), ROOT(overwritten below)
ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"

MONTHS = {m:i for i,m in enumerate(
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 1)}

VIDEO_FCW = "fuTUDu6mwcE"

def video_figure(yt_id, title, caption):
    return (
'        <figure class="article-inline-figure">\n'
'          <div style="position:relative;width:100%;aspect-ratio:16/9;border-radius:12px;overflow:hidden;">\n'
f'            <iframe src="https://www.youtube.com/embed/{yt_id}" title="{esc(title)}"\n'
'                    style="position:absolute;inset:0;width:100%;height:100%;border:0;" loading="lazy"\n'
'                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>\n'
'          </div>\n'
f'          <figcaption>{caption}</figcaption>\n'
'        </figure>')

# ---------------------------------------------------------------- records
mahay_body = """        <p class="lead">Can early childhood development reach young children at national scale by riding on the health and nutrition programs that already exist? A cluster-randomized trial in rural Madagascar set out to answer that question, layering structured ECD stimulation onto an existing community nutrition program and using <a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a> to track every session in the field.</p>

        <h2 id="the-challenge">Reaching the youngest children at scale</h2>
        <p>The first 1,000 days shape a child&rsquo;s cognitive and physical development for life, yet structured early stimulation rarely reaches families in low-resource rural settings. Building a standalone ECD service for every village is expensive. The more promising path is integration: adding developmental stimulation to the health and nutrition contacts that community health workers already deliver. The open question is whether integration actually works, or whether asking community workers to do more simply crowds out the services families came for.</p>

        <h2 id="a-trial-in-the-highlands">A cluster-randomized trial in the central highlands</h2>
        <p>Researchers ran the trial across 75 communities in two regions of Madagascar&rsquo;s central highlands, Amoron&rsquo;i Mania and Haute Matsiatra, reaching 9,408 children aged 6 to 30 months and their caregivers. The MAHAY Mikolo program delivered age-specific stimulation activities through twelve fortnightly group sessions over six months, led by the same community health workers who run the existing nutrition program. One treatment arm added take-home toy boxes and rotating book libraries to test whether materials in the home would deepen engagement.</p>

        <h2 id="tracking-on-commcare">Tracking every session on CommCare</h2>
        <p>To measure feasibility honestly, the team needed reliable attendance data from dozens of villages. Community health workers recorded participation in both the ECD sessions and the existing health and nutrition sessions on CommCare, uploading to a shared digital platform for routine monitoring and evaluation. That gave the researchers a continuous, village-level record of who attended what, the foundation for a differences-in-differences analysis of whether the new ECD offer pulled families away from existing services.</p>

        <h2 id="what-the-data-showed">What the data showed</h2>
        <p>The program proved deliverable: community health workers completed roughly 95% of planned sessions, and 30 to 32% of eligible families registered across cycles. Crucially, offering ECD sessions had no significant effect on families&rsquo; monthly attendance at the existing health and nutrition sessions, evidence that integration did not crowd out the core program. Take-home toy boxes did not raise ECD attendance overall, though they showed modest benefits among children who had not previously participated. Wealthier households, and those already engaged with health services, were the most likely to enroll, a reminder that integration alone does not automatically reach the hardest-to-reach.</p>

        <h2 id="why-it-matters">Why it matters for integrated ECD</h2>
        <p>The trial offers practical evidence that early childhood development can be folded into an existing community nutrition platform without sacrificing the services already in place, and that a frontline workforce can deliver it with high fidelity when given simple digital tools to manage and monitor the work. The findings also sharpen the next question for program designers: how to lift enrollment among the families who need stimulation most. Full methods and results are published open-access in <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11428953/" target="_blank" rel="noopener">BMC Public Health</a>.</p>
"""

ugunja_body = """        <p class="lead">In western Kenya, the Ugunja Community Resource Center set out to put early childhood development tools directly in the hands of community health volunteers and parents, building a smartphone application on <a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a> to help families nurture children in their most formative first two years.</p>

        <h2 id="the-gap">Closing the early development gap in rural Kenya</h2>
        <p>For children from birth to age two, the right stimulation, nutrition, and timely care can change the entire trajectory of their development. In rural and peri-urban communities around Ugunja, in Kenya&rsquo;s Siaya County, that early support is often out of reach, and the community health volunteers who visit households have had few practical tools for assessing or fostering a child&rsquo;s development. Ugunja Community Resource Center wanted to change that with technology volunteers and parents could actually use.</p>

        <h2 id="the-app">A CommCare app for community health volunteers</h2>
        <p>The team built a suite of mobile applications on CommCare, the open-source platform from Dimagi, designed to support volunteers and caregivers alike. The apps packaged practical advice, tools, educational aids, and structured forms for assessing and fostering early childhood development, covering cognitive development, nutrition, illness management, and strategies for cognitive stimulation. A cloud-based server and dashboard let supervisors monitor performance indicators, while training modules brought volunteers up to speed on using the tools in the field.</p>

        <h2 id="proof-of-concept">Proof-of-concept results</h2>
        <p>As a Saving Brains proof-of-concept project funded by Grand Challenges Canada, the work was designed to test whether the approach could move the needle. The project reached 471 households with children under three, trained and equipped 30 community health volunteers with development-support tools, and produced three service-delivery prototypes. It set an ambitious target of halving the share of children scoring below their age-expected developmental range, and it generated a policy brief for Kenya&rsquo;s ministries of Health and Education.</p>

        <h2 id="from-proof-to-policy">From proof of concept to policy</h2>
        <p>By pairing community health volunteers with simple mobile tools, the project showed how digital early childhood development support can fit into existing community health structures, and how the data those tools capture can inform both supervision and national policy. The work was carried out with collaborators including Harvard Business School, the University of Pennsylvania, and Kenya Methodist University. Read more about the project on the <a href="https://www.savingbrainsinnovation.net/projects/0352-03/" target="_blank" rel="noopener">Saving Brains</a> innovation platform.</p>
"""

ECD_CTA = {'h3': 'See what CommCare can do for your program',
           'p': 'Talk with our team about digitizing service delivery and monitoring for your frontline workforce.',
           'btntext': 'Get in touch', 'btnhref': '../../contact/index.html'}

mahay = dict(
    slug="integrating-ecd-health-nutrition-madagascar",
    h1="Integrating Early Childhood Development into Health &amp; Nutrition: Evidence from Madagascar",
    titletag="Integrating ECD into Health &amp; Nutrition in Madagascar | Dimagi",
    ogtitle="Integrating Early Childhood Development into Health & Nutrition: Evidence from Madagascar",
    desc="A cluster-randomized trial in rural Madagascar layered early childhood development stimulation onto an existing community nutrition program, using CommCare to track attendance, and found integration worked without crowding out existing services.",
    deck="A cluster-randomized trial layered ECD stimulation onto an existing community nutrition program in rural Madagascar, with community health workers recording every session on CommCare.",
    date="2024-09-27", datelabel="Sep 2024", author="Dimagi", initials="D",
    category="CommCare", crumb="CommCare", readtime="5 min read",
    cover="cover.jpg", coverw=1200, coverh=750,
    coveralt="Community health worker leading an early childhood development session with caregivers and young children in rural Madagascar",
    covercaption="The MAHAY Mikolo program delivered ECD stimulation through community health workers across 75 communities in Madagascar&rsquo;s central highlands.",
    ogimage="https://dimagi.com/assets/images/integrating-ecd-health-nutrition-madagascar/cover.jpg",
    ogw=1200, ogh=750,
    ogalt="Early childhood development session in rural Madagascar",
    keywords="early childhood development, ECD, CommCare, Madagascar, community health workers, nutrition, cluster-randomized trial, MAHAY Mikolo, child development, monitoring and evaluation",
    body=mahay_body,
    toc=[["the-challenge","Reaching at scale"],["a-trial-in-the-highlands","A trial in the highlands"],
         ["tracking-on-commcare","Tracking on CommCare"],["what-the-data-showed","What the data showed"],
         ["why-it-matters","Why it matters"]],
    tags=["CommCare","Research","Early Childhood Development","Madagascar"],
    cta=ECD_CTA,
)

ugunja = dict(
    slug="commcare-ecd-community-health-volunteers-kenya",
    h1="CommCare for Early Childhood Development: Equipping Community Health Volunteers in Kenya",
    titletag="CommCare for Early Childhood Development in Kenya | Dimagi",
    ogtitle="CommCare for Early Childhood Development: Equipping Community Health Volunteers in Kenya",
    desc="The Ugunja Community Resource Center built a CommCare app to help community health volunteers and parents in western Kenya assess and foster early childhood development for children under two, as a Saving Brains proof-of-concept project.",
    deck="A Saving Brains proof-of-concept project equipped community health volunteers in western Kenya with a CommCare app to assess and foster early childhood development for children under two.",
    date="2014-10-01", datelabel="Oct 2014", author="Dimagi", initials="D",
    category="CommCare", crumb="CommCare", readtime="4 min read",
    cover="cover.jpg", coverw=715, coverh=370,
    coveralt="Community health volunteers and caregivers with young children in Ugunja, western Kenya",
    covercaption="The Ugunja Community Resource Center equipped community health volunteers with CommCare tools for early childhood development.",
    ogimage="https://dimagi.com/assets/images/commcare-ecd-community-health-volunteers-kenya/cover.jpg",
    ogw=715, ogh=370,
    ogalt="Community health volunteers supporting early childhood development in Kenya",
    keywords="early childhood development, ECD, CommCare, Kenya, community health volunteers, Saving Brains, Grand Challenges Canada, child development, mobile health, Ugunja",
    body=ugunja_body,
    toc=[["the-gap","Closing the gap"],["the-app","A CommCare app"],
         ["proof-of-concept","Proof-of-concept results"],["from-proof-to-policy","From proof to policy"]],
    tags=["CommCare","Case Study","Early Childhood Development","Kenya"],
    cta=ECD_CTA,
)

NEW = [mahay, ugunja]

# ---------------------------------------------------------------- cover images
SAVED_KENYA = "/Users/gillianjavetski/.claude/projects/-Users-gillianjavetski-Documents-Gillian-Coding/43c73c63-2235-4dcd-9753-39244c01afe3/tool-results/webfetch-1781183594919-ktlpox.jpg"
os.makedirs(os.path.join(IMG, mahay['slug']), exist_ok=True)
os.makedirs(os.path.join(IMG, ugunja['slug']), exist_ok=True)
# MAHAY: reuse the existing on-brand Madagascar field cover (same country/theme; real site asset)
shutil.copy(os.path.join(IMG, "reducing-childhood-malnutrition-in-madagascar", "cover.jpg"),
            os.path.join(IMG, mahay['slug'], "cover.jpg"))
# Ugunja: the real project photo fetched from the Saving Brains page
if os.path.exists(SAVED_KENYA):
    shutil.copy(SAVED_KENYA, os.path.join(IMG, ugunja['slug'], "cover.jpg"))
else:
    raise SystemExit("Kenya cover image not found at " + SAVED_KENYA)
print("covers in place")

# ---------------------------------------------------------------- parse existing listing cards
idx_fp = os.path.join(BLOG, "index.html")
S = open(idx_fp, encoding='utf-8').read()
card_re = re.compile(r'<article class="blog-card".*?</article>', re.S)
existing_cards = card_re.findall(S)

def card_slug(c):
    m = re.search(r'href="([^"/]+)/index\.html"', c); return m.group(1) if m else None
def card_date_key(c):
    m = re.search(r'class="blog-card-date">([A-Z][a-z]{2}) (\d{4})<', c)
    if not m: return (0,0)
    return (int(m.group(2)), MONTHS.get(m.group(1),0))
listing = {card_slug(c): c for c in existing_cards}

# related: 3 ECD/early-development posts pulled from the live listing
def related_from_listing(slugs):
    out=[]
    for s in slugs:
        c = listing.get(s)
        if not c: continue
        title = re.search(r'class="blog-card-title">(.*?)</h2>', c, re.S).group(1).strip()
        img   = re.search(r'class="blog-card-image"[^>]*>\s*<img src="([^"]+)"', c, re.S).group(1)
        img   = img.replace("../assets/", "../../assets/")
        date  = re.search(r'class="blog-card-date">(.*?)</span>', c).group(1).strip()
        prod  = re.search(r'data-product="([^"]*)"', c).group(1)
        out.append(dict(href=f"../{s}/index.html", img=img, w=1200, h=750,
                        cat=prod, title=title, date=date, alt=re.sub('<[^>]+>','',title)))
    return out[:3]

mahay['related']  = related_from_listing(["ecd-digital-transformation",
                        "reducing-childhood-malnutrition-in-madagascar",
                        "predictive-analytics-public-health-malnutrition"])
ugunja['related'] = related_from_listing(["ecd-digital-transformation",
                        "rti-cambodia-iecd-early-childhood-development",
                        "predictive-analytics-public-health-malnutrition"])

# ---------------------------------------------------------------- render the two pages
AUTHOR_LINK = '<span class="article-byline-author"><a class="article-byline-author-link" href="../author/dimagi/index.html">Dimagi</a></span>'
for p in NEW:
    p2 = dict(p); p2['toc'] = [tuple(x) for x in p['toc']]
    htmlout = build(p2)
    htmlout = htmlout.replace('<span class="article-byline-author">Dimagi</span>', AUTHOR_LINK)
    os.makedirs(os.path.join(BLOG, p['slug']), exist_ok=True)
    open(os.path.join(BLOG, p['slug'], "index.html"), "w", encoding='utf-8').write(htmlout)
    print("rendered", p['slug'])

# ---------------------------------------------------------------- listing card for a new post
def new_card(p):
    sector = "Early Childhood Development"
    typ = p['tags'][1]  # Research / Case Study
    country = "Africa"
    img = f"../assets/images/{p['slug']}/{p['cover']}"
    href = f"{p['slug']}/index.html"
    alt = re.sub('<[^>]+>','', p['h1'])
    return (
f' <article class="blog-card" data-product="CommCare" data-type="{typ}" data-topic="None" data-country="{country}" data-sector="{sector}">\n'
f' <a class="blog-card-image" href="{href}">\n'
f' <img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async">\n'
f' </a>\n'
f' <div class="blog-card-body">\n'
f' <h2 class="blog-card-title">{p["h1"]}</h2>\n'
f' <p class="blog-card-desc">{esc(p["desc"])}</p>\n'
f' <div class="blog-card-footer">\n'
f' <span class="blog-card-date">{p["datelabel"]}</span>\n'
f' <a class="blog-card-link" href="{href}">Read more</a>\n'
f' </div>\n'
f' </div>\n'
f' </article>')

# guard against re-insert; drop any prior copies of our slugs, then add fresh
cards = [c for c in existing_cards if card_slug(c) not in (mahay['slug'], ugunja['slug'])]
cards.append(new_card(mahay)); cards.append(new_card(ugunja))
cards.sort(key=card_date_key, reverse=True)  # stable within same month
grid_inner = "\n".join(cards)

# replace grid contents between <div class="blog-grid"> ... <div class="blog-more"
g0 = S.index('<div class="blog-grid">')
g0e = S.index('>', g0) + 1
gm = S.index('<div class="blog-more"', g0e)
# back up to the indentation start of blog-more line
gm_line = S.rfind('\n', 0, gm) + 1
new_S = S[:g0e] + "\n" + grid_inner + "\n      " + S[gm_line:]
open(idx_fp, "w", encoding='utf-8').write(new_S)
print(f"listing rebuilt: {len(cards)} cards")

# ---------------------------------------------------------------- FCW video embed (record + rendered html)
def insert_video_after_lead(html, fig):
    if VIDEO_FCW in html and 'youtube.com/embed/'+VIDEO_FCW in html:
        return html, False  # already embedded
    m = re.search(r'(<p class="lead">.*?</p>)', html, re.S)
    if not m: return html, False
    return html[:m.end()] + "\n\n" + fig + html[m.end():], True

fcw_fig = video_figure(VIDEO_FCW,
    "FCW: Amplifying early childhood development with CommCare",
    "Watch how the Foundation for Community Work uses CommCare to empower its home visitors.")

# 6a. rendered page
fcw_fp = os.path.join(BLOG, "ecd-digital-transformation", "index.html")
fh = open(fcw_fp, encoding='utf-8').read()
fh2, ch = insert_video_after_lead(fh, fcw_fig)
if ch: open(fcw_fp, "w", encoding='utf-8').write(fh2)
print("FCW page video:", "added" if ch else "already present")

# 6b. archived record (so a future regen keeps the video)
rec_fp = os.path.join(HERE, "records_archive", "ecd-digital-transformation.json")
rec = json.load(open(rec_fp))
nb, ch2 = insert_video_after_lead(rec['body'], fcw_fig)
if ch2:
    rec['body'] = nb
    json.dump(rec, open(rec_fp, "w"), ensure_ascii=False, indent=1)
print("FCW record video:", "added" if ch2 else "already present")

# ---------------------------------------------------------------- tag_overrides rows
to_fp = os.path.join(HERE, "tag_overrides.csv")
to = open(to_fp, encoding='utf-8').read()
for p, country in [(mahay,"Madagascar"), (ugunja,"Kenya")]:
    if p['slug'] not in to:
        if not to.endswith("\n"): to += "\n"
        to += f'{p["slug"]},{country},Early Childhood Development,,"ECD blog added {p["datelabel"]}; backdated"\n'
open(to_fp, "w", encoding='utf-8').write(to)
print("tag_overrides updated")

# ---------------------------------------------------------------- sitemap
sm_fp = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_fp, encoding='utf-8').read()
# detect existing blog url pattern
sample = re.search(r'<loc>([^<]*ecd-digital-transformation[^<]*)</loc>', sm)
print("sitemap blog url sample:", sample.group(1) if sample else "NONE")
for p in NEW:
    if p['slug'] in sm: continue
    url = (sample.group(1).replace("ecd-digital-transformation", p['slug'])
           if sample else f"https://dimagi.com/{p['slug']}/")
    entry = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{p['date']}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n"
    sm = sm.replace("</urlset>", entry + "</urlset>")
open(sm_fp, "w", encoding='utf-8').write(sm)
print("sitemap updated")
print("DONE")
