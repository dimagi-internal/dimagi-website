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
TOPICS   = {'Company','Dimagi','Ecosystem'}   # 'Company' kept to read old cards; canonical label is now 'Dimagi'

FOCUS_OVERRIDE = {
 'predictive-analytics-public-health-malnutrition':'Ecosystem',
 'frontline-worker-advisory-panel-launch':'Company',
 'harnessing-ais-potential-to-improve-equity':'Open Chat Studio',   # AI/LLM piece, same as chatbots post (FLAG)
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
 'chatbots-support-the-right-to-health':'Open Chat Studio',
 'baobab-senegal-uncdf-commbanane-advisory-service':'Ecosystem',
 'undp-financial-education-application':'Ecosystem',
 'user-testing-chw-resilience-messaging':'Company',
 'covid-19-pandemic-preparedness-report':'Ecosystem',
 'tufts-iita-inddex24-nigeria':'Ecosystem',
 'egpaf-malawi-pepfar-gh002301':'Ecosystem',
 'cdc-foundation-pods-project':'Ecosystem',
 'covid-19-equitable-vaccine-delivery-challenges':'Ecosystem',
 'banyan-global-empleando-futuros':'Ecosystem',
 'global-digital-health-forum-2020':'Company',
 'great-reset-social-enterprise-wef':'Company',
 'google-org-medic-mobile-covid-19-flw-support':'Company',   # round 5: Dimagi, not CommCare
 'field-research-storytelling':'Company',
 'field-research-card-sorting':'Company',
 'career-journey-of-simon-kelly':'Company',
 '2024-year-in-review':'Company',
 'learnings-from-5-years-of-new-business':'Company',
 'innovation-at-dimagi-part-3-evaluating-the-mission':'Company',
 'innovation-at-dimagi-part-4-innovation-funding':'Company',
 # ---- round 2 (user directives 2026-06-08): explicit + "Dimagi in title -> Company" ----
 'refreshing-dimagi-and-commcare-brands-for-high-impact-growth':'Company',   # brand refresh
 'celebrating-20-years-of-impact':'Company',                                  # "20 years of impact"
 'inaugural-commcare-government-summit':'CommCare',                           # inaugural summit
 'zohaib-ali-khusru':'Company',                                              # day in the life
 'a-day-in-the-life-of-charles-aphrem':'Company',
 'a-day-in-the-life-of-dhivya-sivaramakrishnan':'Company',
 'a-day-in-the-life-of-wouter-vink':'Company',
 'dimagi-makes-the-inc-5000-list-for-the-tenth-time':'Company',
 'global-digital-health-forum-2025':'Company',                               # "Join Dimagi at GDHF"
 'gdhf-2024':'Company',                                                       # "Find Dimagi at GDHF"
 'dimagi-receives-25-million-to-develop-transformative-technology-for-frontline-workers':'Company',  # FLAG: corporate funding (was CommCare)
 'sentinel-audacious-project-2020':'Company',                                # FLAG: recognition (was CommCare)
 'usaid-global-health-innovation-index-commcare-2020':'Company',             # FLAG: recognition (was CommCare)
 # ---- round 5 (user directives 2026-06-08): Focus -> Dimagi ----
 'solutions-remote-impact-covid-19':'Company',          # "How Dimagi Helps Deliver Impact Remotely"
 'reflecting-on-2020':'Company',
 'crisis-response-corps-launch':'Company',
 'global-digital-health-forum-2022':'Company',
 '20-years-of-designing-under-the-mango-tree':'Company',
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
 'covid-19-response-jhu-digital-solutions-report':'Announcement',   # "Johns Hopkins Selects CommCare" reads as a press release
 # Day-in-the-Life + anniversary pieces are personal/company reflections, not Case Studies
 'zohaib-ali-khusru':'Perspective',
 'a-day-in-the-life-of-charles-aphrem':'Perspective',
 'a-day-in-the-life-of-dhivya-sivaramakrishnan':'Perspective',
 'a-day-in-the-life-of-wouter-vink':'Perspective',
 'a-day-in-the-life-of-aubrey-chirwa-senior-technical-project-analyst-solutions-division':'Perspective',
 'a-day-in-the-life-of-themba-nyirenda-senior-technical-project-analyst-solutions-division':'Perspective',
 'day-in-the-life-of-namrata-tomar-project-manager-solutions-division':'Perspective',
 'celebrating-20-years-of-impact':'Perspective',
 # ---- round 3 (user directives 2026-06-08) ----
 'unicef-health-campaign-digitalization-guidebook':'Announcement',
 'sureadheres-story':'Perspective',
 'commcare-connect-reaches-100000-deliveries':'Announcement',
 'commcare-connect-2023':'Announcement',
 'your-ultimate-accessibility-guide-designing-for-inclusion-and-empowering-all-users':'Perspective',
 '20-years-of-designing-under-the-mango-tree':'Perspective',
 'digital-health-must-invest-in-local-digital-ecosystems':'Perspective',
 'three-digital-tools-for-behavioral-health':'Perspective',
 'commcare-provider-program':'Announcement',
 # ---- round 4 (user directives 2026-06-08) ----
 'data-driven-program-improvements-webinar-miraclefeet':'Case Study',   # MiracleFeet "turning data into insights"
 'supporting-our-partners':'Perspective',
 'commcare-use-cases-operational-efficiency':'Announcement',            # "Scaling Beyond the Wall"
 # ---- round 5 (user directives 2026-06-08): retire 'Research' type — reassign every Research post ----
 'mhealth-interventions-bmc-macdonald':'Announcement',                 # New Study on Mobile Health Interventions
 'wellme-update2':'Announcement',                                      # WellMe: The Resilience Application
 'technoserve-monitoring-evaluation-tools-suite':'Case Study',
 'field-research-storytelling':'Reflections',                          # Tactics in Field Research
 'field-research-card-sorting':'Reflections',
 'researcher-spotlight-jack-hetherington':'Reflections',
 'researcher-spotlight-nick-tarantino':'Reflections',
 'predictive-analytics-public-health-malnutrition':'Reflections',      # Transforming Community Health
 # round 5: COVID-19 template-app posts -> Announcement
 'covid-19-template-application-port-of-entry':'Announcement',
 'covid-19-template-application-healthcare-provider-training-monitoring':'Announcement',
 'covid-19-template-application-facility-readiness':'Announcement',
 'covid-19-response-template-apps':'Announcement',                     # Template Applications (all phases)
 'theres-no-choice-but-to-act-now-who-contact-tracing-template-app-available-today':'Announcement',  # WHO contact-tracing template app
 'fast-company-world-changing-ideas-2021':'Announcement',             # Fast Company honor (was Case Study)
 'covid-19-pro-bono-project-highlights-2021':'Reflections',           # A Year of COVID-19 Response (was Case Study)
 'vaccine-solution-covid-19-routine-immunization':'Case Study',       # Mitigating... Global Vaccination (was Perspective)
}

# Geography overrides. 'None' removes it. India keep-list -> 'Asia' (India is merged into Asia;
# every other India card is dropped to None by the India->None rule in rewrite_card).
GEO_OVERRIDE = {
 'supporting-our-partners':'None',
 'researcher-spotlight-jack-hetherington':'None',
 'researcher-spotlight-nick-tarantino':'None',
 'commcare-eu-cloud-launch':'Asia',
 'frontline-worker-advisory-panel-launch':'Asia',
 'strengthening-mental-health-services-with-digital-solutions':'Asia',
}

def geo_ok(g): return g not in (None,'None','')

# Managed label values that the "Filed under" list re-derives from the lead [focus, type, geo].
# Strip any stale copies (e.g. a renamed 'Perspective', or an old Focus after a reassignment)
# from a page's existing tags so only genuinely topical tags + country names survive. Region
# names are stripped (the lead re-adds the canonical region); individual countries are kept.
MANAGED = {x.lower() for x in [
    'CommCare','Connect','SureAdhere','Open Chat Studio','Dimagi','Company','Ecosystem',
    'Case Study','Reflections','Announcement','Event','Perspective','Research','Product Update',
    'United States','Asia','India','Africa','Latin America','Global','None']}

idx = open(IDX, encoding='utf-8').read()
final = {}   # slug -> (focus, type, geo)

def rewrite_card(m):
    block = m.group(0)
    sm = re.search(r'href="([^"/]+)/index\.html"', block); slug = sm.group(1) if sm else None
    a = dict(re.findall(r'data-(\w+)="([^"]*)"', re.search(r'<article[^>]*>', block).group(0)))
    # base classification from current card, then curated overrides
    base_focus = a.get('product') if a.get('product') in PRODUCTS else (a.get('topic') if a.get('topic') in TOPICS else '')
    focus = FOCUS_OVERRIDE.get(slug, base_focus or 'Ecosystem')
    if focus == 'Company': focus = 'Dimagi'        # the 'Company' focus was relabeled 'Dimagi'
    if focus == 'Ecosystem': focus = 'CommCare'    # Ecosystem retired -> all remaining roll into CommCare
    tm = re.search(r'<h2 class="blog-card-title">(.*?)</h2>', block, re.S)
    title = re.sub('<[^>]+>','', tm.group(1)).strip() if tm else ''
    ctype = a.get('type','Perspective')
    if title.startswith('Innovation at Dimagi, Part'): ctype = 'Perspective'
    ctype = TYPE_OVERRIDE.get(slug, ctype)
    if ctype == 'Product Update': ctype = 'Announcement'   # Product Update type retired -> Announcement
    if ctype == 'Perspective': ctype = 'Reflections'       # round 5: 'Perspective' type relabeled 'Reflections'
    geo = GEO_OVERRIDE.get(slug, a.get('country','None'))
    if geo == 'India': geo = 'None'   # India merged into Asia; keep-list already set to Asia above
    final[slug] = (focus, ctype, geo)
    product = focus if focus in PRODUCTS else 'None'
    topic   = focus if focus in TOPICS else 'None'
    country = geo if geo_ok(geo) else 'None'
    block = re.sub(r'<article class="blog-card"[^>]*>',
        f'<article class="blog-card" data-product="{product}" data-type="{ctype}" data-topic="{topic}" data-country="{country}">', block, count=1)
    # Focus + Type badges over the card image (idempotent: handles old single-category or new wrapper form)
    badges = (f'<div class="blog-card-tags"><span class="blog-card-category">{focus}</span>'
              f'<span class="blog-card-type">{ctype}</span></div>')
    block = re.sub(r'<div class="blog-card-tags">.*?</div>', '<<B>>', block, count=1, flags=re.S)
    if '<<B>>' not in block:
        block = re.sub(r'<div class="blog-card-category">[^<]*</div>', '<<B>>', block, count=1)
    block = block.replace('<<B>>', badges)
    return block

idx, ncards = re.subn(r'<article class="blog-card".*?</article>', rewrite_card, idx, flags=re.S)
# drop now-empty None chips from Focus + Type rows (Geography keeps None)
for dim in ('focus','type'):
    idx = re.sub(r'\n\s*<button type="button" class="blog-filter" data-dim="'+dim+r'" data-filter="None"[^>]*>None</button>','', idx)
# retired chips: Ecosystem (Focus row), India (Geography row, merged into Asia), Product Update (Type row)
idx = re.sub(r'\n\s*<button type="button" class="blog-filter" data-dim="focus" data-filter="Ecosystem"[^>]*>Ecosystem</button>','', idx)
idx = re.sub(r'\n\s*<button type="button" class="blog-filter" data-dim="country" data-filter="India"[^>]*>India</button>','', idx)
idx = re.sub(r'\n\s*<button type="button" class="blog-filter" data-dim="type" data-filter="Product Update"[^>]*>Product Update</button>','', idx)
# round 5: rebuild the Type filter row in the requested order — Case Study, Reflections,
# Announcement, Event (Research retired; 'Perspective' renamed 'Reflections', moved right after Case Study)
_typechips = ['          <button type="button" class="blog-filter is-active" data-dim="type" data-filter="all" aria-pressed="true">All</button>']
for _v in ['Case Study', 'Reflections', 'Announcement', 'Event']:
    _typechips.append(f'          <button type="button" class="blog-filter" data-dim="type" data-filter="{_v}" aria-pressed="false">{_v}</button>')
idx = re.sub(r'(<span class="filter-label">Type</span>\s*<div class="filter-chips">)(.*?)(</div>)',
             lambda m: m.group(1) + "\n" + "\n".join(_typechips) + "\n          " + m.group(3),
             idx, count=1, flags=re.S)
# relabel the Focus 'Company' chip -> 'Dimagi'
idx = idx.replace('<button type="button" class="blog-filter" data-dim="focus" data-filter="Company" aria-pressed="false">Company</button>',
                  '<button type="button" class="blog-filter" data-dim="focus" data-filter="Dimagi" aria-pressed="false">Dimagi</button>')
# the inline focusOf() JS must recognize the renamed topic value
idx = idx.replace("var FOCUS_TOPICS = { 'Company': 1, 'Ecosystem': 1 };", "var FOCUS_TOPICS = { 'Dimagi': 1 };")
open(IDX,'w',encoding='utf-8').write(idx)

arts = 0
for slug,(focus,ctype,geo) in final.items():
    fp = os.path.join(ROOT,"blog",slug,"index.html")
    if not os.path.exists(fp): continue
    h = open(fp,encoding='utf-8').read()
    # round 5: remove the top category badge entirely; Focus/Type/Geography now live only in
    # the "Filed under" tags below. Idempotent: a no-op once the badge is gone.
    h = re.sub(r'[ \t]*<span class="article-category">[^<]*</span>\n?', '', h)
    bm = re.search(r'<nav class="article-breadcrumb".*?</nav>', h, re.S)
    if bm:
        # round 5: the last breadcrumb crumb is now the ARTICLE TITLE (was Focus). This matches the
        # BreadcrumbList JSON-LD already on the page (which ends with the title) and is the standard
        # "you are here" convention. Idempotent: re-writing the same title is a no-op.
        tm = re.search(r'<h1 class="article-title">(.*?)</h1>', h, re.S)
        crumb = re.sub(r'<[^>]+>', '', tm.group(1)).strip() if tm else focus
        h = h.replace(bm.group(0), re.sub(r'<span>[^<]*</span>', lambda _m: f'<span>{crumb}</span>', bm.group(0), count=1), 1)
    fm = re.search(r'(<div class="article-tags">)(.*?)(</div>)', h, re.S)
    if fm:
        existing = [e.strip() for e in re.findall(r'<span class="article-tag">(.*?)</span>', fm.group(2), re.S)
                    if e.strip().lower() not in MANAGED]
        lead = [focus, ctype] + ([geo] if geo_ok(geo) else [])
        seen = set(x.lower() for x in lead); out = list(lead)
        for e in existing:
            if e and e.lower() not in seen: seen.add(e.lower()); out.append(e)
        inner = '\n' + '\n'.join(f'            <span class="article-tag">{t}</span>' for t in out) + '\n          '
        h = h[:fm.start(2)] + inner + h[fm.end(2):]
    # round 5: remove the trailing legacy WordPress category from the byline
    # (date • read time • <category>). Keep the leading spans; drop the last content span
    # only when there are 3+ (date, read time, category). Idempotent: once trimmed to 2, it
    # no longer matches the 3+ guard, so re-runs leave date • read time intact.
    bd = re.search(r'<span class="article-byline-detail">(.*?)</span>\s*</div>', h, re.S)
    if bd:
        contents = re.findall(r'<span>([^<]*)</span>', bd.group(1))   # content spans (dots carry a class)
        if len(contents) >= 3:
            sep = '\n              <span class="dot"></span>\n              '
            bnew = '\n              ' + sep.join(f'<span>{c}</span>' for c in contents[:-1]) + '\n            '
            h = h[:bd.start(1)] + bnew + h[bd.end(1):]
    open(fp,'w',encoding='utf-8').write(h); arts += 1

from collections import Counter
print(f"cards={ncards} articles={arts}")
print("Focus:", dict(Counter(f for f,_,_ in final.values())))
print("Type :", dict(Counter(t for _,t,_ in final.values())))
