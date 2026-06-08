# Re-applies the curated Focus/Type tagging pass and propagates it to the whole blog.
# Self-contained & idempotent: reads the CURRENT cards in blog/index.html (so it works
# even after build_taxonomy.py / transform_filters.py regenerate the base tags), layers
# the curated overrides below, then writes:
#   - listing cards: data-product/type/topic/country + visible .blog-card-category = Focus
#   - each article: .article-category, breadcrumb crumb = Focus; "Filed under" = Focus, Type,
#     Geography(if any), then the page's existing topical tags (deduped)
#   - removes the now-empty "None" chips from the Focus and Type filter rows (Geography keeps None)
# Rules: every blog must have a Focus (CommCare/Connect/SureAdhere/Open Chat Studio/Company/
# Ecosystem) and a Type; Geography is optional. Run:  python3 Context/blog-import/apply_tag_pass.py
import re, os

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
IDX  = os.path.join(ROOT, "blog", "index.html")
PRODUCTS = {'CommCare','Connect','SureAdhere','Open Chat Studio'}
TOPICS   = {'Company','Ecosystem'}

FOCUS_OVERRIDE = {
 'predictive-analytics-public-health-malnutrition':'Ecosystem',
 'frontline-worker-advisory-panel-launch':'Company',
 'harnessing-ais-potential-to-improve-equity':'Ecosystem',
 'johnson-johnson-foundation-leveraging-advanced-analytics-to-develop-engagement-profiles':'Ecosystem',
 'researcher-spotlight-nick-tarantino':'Company',
 'what-we-learned-from-our-working-group-on-health-worker-wellbeing':'Company',
 'dimagi-renews-its-commitment-to-the-global-fund-with-a-5-million-pledge':'Company',
 'adpp-mozambique-tb-local-response':'Ecosystem',
 'pathfinder-youth-voices-for-agency-and-access-yuvaa-india':'Ecosystem',
 'global-fund-partnership':'Company',
 'malawi-ministry-of-health-cstock-supply-chain-management-application':'Ecosystem',
 'national-institutes-of-health-survivorcare-phase-ii':'Ecosystem',
 'vaccine-solution-covid-19-routine-immunization':'Ecosystem',
 'chatbots-support-the-right-to-health':'Ecosystem',
 'baobab-senegal-uncdf-commbanane-advisory-service':'Ecosystem',
 'undp-financial-education-application':'Ecosystem',
 'user-testing-chw-resilience-messaging':'Company',
 'covid-19-pandemic-preparedness-report':'Ecosystem',
 'tufts-iita-inddex24-nigeria':'Ecosystem',
 'egpaf-malawi-pepfar-gh002301':'Ecosystem',
 'cdc-foundation-pods-project':'Ecosystem',
 'covid-19-equitable-vaccine-delivery-challenges':'Ecosystem',
 'banyan-global-empleando-futuros':'Ecosystem',
 'global-digital-health-forum-2020':'Ecosystem',
 'great-reset-social-enterprise-wef':'Ecosystem',
 'google-org-medic-mobile-covid-19-flw-support':'Ecosystem',
 'field-research-storytelling':'Company',
 'field-research-card-sorting':'Company',
 'career-journey-of-simon-kelly':'Company',
 '2024-year-in-review':'Company',
 'learnings-from-5-years-of-new-business':'Company',
 'innovation-at-dimagi-part-3-evaluating-the-mission':'Company',
 'innovation-at-dimagi-part-4-innovation-funding':'Company',
}
TYPE_OVERRIDE = {
 'adpp-mozambique-tb-local-response':'Case Study',
 'pathfinder-youth-voices-for-agency-and-access-yuvaa-india':'Case Study',
 'malawi-ministry-of-health-cstock-supply-chain-management-application':'Case Study',
 'national-institutes-of-health-survivorcare-phase-ii':'Case Study',
 'baobab-senegal-uncdf-commbanane-advisory-service':'Case Study',
 'undp-financial-education-application':'Case Study',
 'tufts-iita-inddex24-nigeria':'Case Study',
 'egpaf-malawi-pepfar-gh002301':'Case Study',
 'cdc-foundation-pods-project':'Case Study',
 'banyan-global-empleando-futuros':'Case Study',
 'google-org-medic-mobile-covid-19-flw-support':'Case Study',
 'johnson-johnson-foundation-leveraging-advanced-analytics-to-develop-engagement-profiles':'Case Study',
 'taroworks-alternative-givedirectly-cash-transfer-case-study':'Case Study',
 'closing-post-discharge-gap-kangaroo-mother-care':'Case Study',
 'harnessing-ai-for-frontline-workers':'Case Study',
 'miraclefeet-drives-global-impact-through-commcare-and-the-impact-delivery-approach':'Case Study',
 'johnson-and-johnson-foundation-commcare-companion-application':'Case Study',
 'catholic-relief-services-technical-advisory-services-2021':'Case Study',
 'grassroot-soccer-adols':'Case Study',
 'tulasalud-commcare-community-health':'Case Study',
 'different-kind-of-tech-company':'Perspective',
 'refreshing-dimagi-and-commcare-brands-for-high-impact-growth':'Announcement',
}

def geo_ok(g): return g not in (None,'None','')

idx = open(IDX, encoding='utf-8').read()
final = {}   # slug -> (focus, type, geo)

def rewrite_card(m):
    block = m.group(0)
    sm = re.search(r'href="([^"/]+)/index\.html"', block); slug = sm.group(1) if sm else None
    a = dict(re.findall(r'data-(\w+)="([^"]*)"', re.search(r'<article[^>]*>', block).group(0)))
    # base classification from current card, then curated overrides
    base_focus = a.get('product') if a.get('product') in PRODUCTS else (a.get('topic') if a.get('topic') in TOPICS else '')
    focus = FOCUS_OVERRIDE.get(slug, base_focus or 'Ecosystem')
    tm = re.search(r'<h2 class="blog-card-title">(.*?)</h2>', block, re.S)
    title = re.sub('<[^>]+>','', tm.group(1)).strip() if tm else ''
    ctype = a.get('type','Perspective')
    if title.startswith('Innovation at Dimagi, Part'): ctype = 'Perspective'
    ctype = TYPE_OVERRIDE.get(slug, ctype)
    geo = a.get('country','None')
    final[slug] = (focus, ctype, geo)
    product = focus if focus in PRODUCTS else 'None'
    topic   = focus if focus in TOPICS else 'None'
    country = geo if geo_ok(geo) else 'None'
    block = re.sub(r'<article class="blog-card"[^>]*>',
        f'<article class="blog-card" data-product="{product}" data-type="{ctype}" data-topic="{topic}" data-country="{country}">', block, count=1)
    block = re.sub(r'<div class="blog-card-category">[^<]*</div>',
        f'<div class="blog-card-category">{focus}</div>', block, count=1)
    return block

idx, ncards = re.subn(r'<article class="blog-card".*?</article>', rewrite_card, idx, flags=re.S)
# drop now-empty None chips from Focus + Type rows (Geography keeps None)
for dim in ('focus','type'):
    idx = re.sub(r'\n\s*<button type="button" class="blog-filter" data-dim="'+dim+r'" data-filter="None"[^>]*>None</button>','', idx)
open(IDX,'w',encoding='utf-8').write(idx)

arts = 0
for slug,(focus,ctype,geo) in final.items():
    fp = os.path.join(ROOT,"blog",slug,"index.html")
    if not os.path.exists(fp): continue
    h = open(fp,encoding='utf-8').read()
    h = re.sub(r'<span class="article-category">[^<]*</span>', f'<span class="article-category">{focus}</span>', h, count=1)
    bm = re.search(r'<nav class="article-breadcrumb".*?</nav>', h, re.S)
    if bm:
        h = h.replace(bm.group(0), re.sub(r'<span>[^<]*</span>', f'<span>{focus}</span>', bm.group(0), count=1), 1)
    fm = re.search(r'(<div class="article-tags">)(.*?)(</div>)', h, re.S)
    if fm:
        existing = [e.strip() for e in re.findall(r'<span class="article-tag">(.*?)</span>', fm.group(2), re.S)]
        lead = [focus, ctype] + ([geo] if geo_ok(geo) else [])
        seen = set(x.lower() for x in lead); out = list(lead)
        for e in existing:
            if e and e.lower() not in seen: seen.add(e.lower()); out.append(e)
        inner = '\n' + '\n'.join(f'            <span class="article-tag">{t}</span>' for t in out) + '\n          '
        h = h[:fm.start(2)] + inner + h[fm.end(2):]
    open(fp,'w',encoding='utf-8').write(h); arts += 1

from collections import Counter
print(f"cards={ncards} articles={arts}")
print("Focus:", dict(Counter(f for f,_,_ in final.values())))
print("Type :", dict(Counter(t for _,t,_ in final.values())))
