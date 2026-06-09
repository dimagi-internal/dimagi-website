# Generates 2 page-only SEO tags per blog post from its real content (title+deck+body,
# boosted by the legacy Filed-under tags), then rewrites each article's "Filed under" to:
#   Focus, Type, Geography(if any), SEO-Tag-1, SEO-Tag-2
# (the curated lead tags from apply_tag_pass.py + 2 SEO tags; legacy noise tags dropped).
# These 2 tags are page-only — NOT added to the listing filter. Writes /tmp/seo_tags.json too.
import re, os, json, html as _html
from collections import Counter

ROOT="/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
rows=json.load(open('/tmp/blogs_current.json'))

# Unified pool of SEO-valuable tags -> regex keyword patterns (searched case-insensitively).
# Pick the 2 highest-scoring per post. Order/space matters only for readability.
TAGS = {
 # ---- health / program sectors ----
 'Maternal & Child Health':[r'maternal',r'newborn',r'\bchild health',r'pregnan',r'antenatal',r'postnatal',r'\bmother',r'infant',r'pediatric',r'clubfoot',r'kangaroo'],
 'Tuberculosis':[r'tuberculosis',r'\bTB\b'],
 'HIV & AIDS':[r'\bHIV\b',r'\bAIDS\b',r'PEPFAR',r'antiretroviral',r'adolescent treatment'],
 'Malaria':[r'malaria'],
 'Immunization':[r'immuniz',r'vaccin'],
 'Nutrition':[r'nutrition',r'malnutrition',r'\bfeeding\b',r'inddex',r'dietary'],
 'COVID-19':[r'covid',r'coronavirus',r'pandemic'],
 'Contact Tracing':[r'contact tracing'],
 'Mental Health':[r'mental health',r'wellbeing',r'\bresilience',r'psycholog',r'burnout'],
 'Supply Chain':[r'supply chain',r'\bstock\b',r'cstock',r'logistics',r'commodit'],
 'Family Planning':[r'family planning',r'reproductive',r'contracept'],
 'Cash Transfers':[r'cash transfer'],
 'Financial Inclusion':[r'financial education',r'microfinance',r'\bsavings\b',r'uncdf',r'financial inclusion'],
 'Agriculture':[r'agricultur',r'\bfarmer',r'livelihood',r'\bcrop'],
 'Education':[r'\beducation',r'classroom',r'universit',r'curriculum',r'\bschool'],
 'Tuberculosis Screening':[],  # reserved; not auto
 # ---- cross-cutting topics / themes ----
 'Case Management':[r'case management'],
 'Data Collection':[r'data collection',r'mobile data',r'\bforms?\b',r'\bsurvey'],
 'Offline Data Collection':[r'offline'],
 'Community Health Workers':[r'community health worker',r'\bCHWs?\b'],
 'Frontline Workers':[r'frontline worker',r'frontline health'],
 'Digital Health':[r'digital health',r'mhealth',r'ehealth',r'digital tool'],
 'Artificial Intelligence':[r'\bAI\b',r'artificial intelligence',r'large language model',r'\bLLM\b',r'generative',r'machine learning'],
 'Chatbots':[r'chatbot'],
 'Monitoring & Evaluation':[r'monitoring',r'evaluation',r'\bM&E\b',r'analytics',r'dashboard',r'impact measurement',r'predictive'],
 'App Building':[r'app building',r'no-code',r'low-code',r'build a mobile',r'application builder',r'app builder'],
 'Interoperability':[r'interoperab',r'\bFHIR\b',r'integration',r'\bDHIS2\b',r'\bAPI\b'],
 'Government Scale':[r'\bgovernment',r'ministry of health',r'\bnational\b',r'public sector'],
 'Last Mile':[r'last mile',r'\brural\b',r'\bremote\b',r'hard-to-reach',r'underserved'],
 'Social Enterprise':[r'social enterprise',r'\bB Corp',r'benefit corporation',r'social impact'],
 'Company Culture':[r'\bculture\b',r'\bcareer',r'\bhybrid\b',r'people operations',r'\bintern\b',r'life at dimagi'],
 'Innovation':[r'\binnovation',r'new business'],
 'Partnerships':[r'\bpartner',r'\bgrant\b',r'\bfunding\b',r'\bpledge',r'acquir'],
 'Global Development':[r'global development',r'international development',r'\bUSAID\b',r'\bNGO\b',r'humanitarian'],
}
# specific countries make strong SEO tags (more specific than the Geography region)
COUNTRIES=['India','Nigeria','Kenya','Malawi','Mozambique','Ethiopia','South Africa','Zambia',
 'Tanzania','Uganda','Senegal','Madagascar','Sierra Leone','Somalia','Jamaica','Cambodia',
 'Tajikistan','Guinea','Benin','Burkina Faso','Niger','Lesotho','Rwanda','Ghana','Bangladesh',
 'Nepal','Indonesia','Mexico','Zimbabwe','Guatemala','Honduras','Liberia','Vietnam']

def article_text(slug):
    fp=os.path.join(ROOT,"blog",slug,"index.html")
    if not os.path.exists(fp): return '', []
    h=open(fp,encoding='utf-8').read()
    m=re.search(r'<h1 class="article-title">(.*?)<div class="article-foot"',h,re.S)
    seg=m.group(1) if m else h
    body=_html.unescape(re.sub('<[^>]+>',' ',seg))
    legacy=[e.strip() for e in re.findall(r'<span class="article-tag">(.*?)</span>',h,re.S)]
    return body, legacy

def score_pool(title, deck, body, legacy, exclude):
    legacy_l=' '.join(legacy).lower()
    scores=Counter()
    for tag,pats in TAGS.items():
        if tag in exclude or not pats: continue
        s=0
        for p in pats:
            s+=3*len(re.findall(p,title,re.I))
            s+=2*len(re.findall(p,deck,re.I))
            s+=1*len(re.findall(p,body,re.I))
            if re.search(p,legacy_l,re.I): s+=4
        if s: scores[tag]=s
    # specific countries (title x3, body x1, legacy x4)
    for c in COUNTRIES:
        if c in exclude: continue
        s=3*len(re.findall(r'\b'+re.escape(c),title,re.I))+len(re.findall(r'\b'+re.escape(c),body,re.I))
        if any(c.lower()==l.lower() for l in legacy): s+=4
        if s: scores[c]=s
    return scores

out={}
for r in rows:
    body,legacy=article_text(r['slug'])
    deck=r['desc']; title=r['title']
    exclude={r['focus'], r['type'], r['geography']}
    sc=score_pool(title,deck,body,legacy,exclude)
    top=[t for t,_ in sc.most_common()]
    tags=top[:2]
    # fallbacks if fewer than 2 strong tags
    if len(tags)<2:
        fb = {'Dimagi':['Social Enterprise','Company Culture'],
              'Ecosystem':['Global Development','Digital Health'],
              'CommCare':['Data Collection','Digital Health'],
              'Connect':['Frontline Workers','Digital Health'],
              'SureAdhere':['Tuberculosis','Digital Health'],
              'Open Chat Studio':['Artificial Intelligence','Chatbots']}.get(r['focus'],['Digital Health','Frontline Workers'])
        for f in fb:
            if f not in tags and f not in exclude and len(tags)<2: tags.append(f)
    out[r['slug']]={'seo1':tags[0] if tags else '', 'seo2':tags[1] if len(tags)>1 else ''}

json.dump(out,open('/tmp/seo_tags.json','w'),indent=2)
json.dump(out,open(os.path.join(ROOT,"Context","blog-import","seo_tags.json"),'w'),indent=2)  # durable copy
print("generated SEO tags for",len(out),"posts")

# ---- write each article's "Filed under" = Focus, Type, Geography(if any), SEO1, SEO2 ----
def geo_ok(g): return g not in (None,'None','')
written=0
for r in rows:
    fp=os.path.join(ROOT,"blog",r['slug'],"index.html")
    if not os.path.exists(fp): continue
    h=open(fp,encoding='utf-8').read()
    s=out[r['slug']]
    cand=[r['focus'], r['type']] + ([r['geography']] if geo_ok(r['geography']) else []) + [s['seo1'], s['seo2']]
    seen=set(); final=[]
    for t in cand:
        if t and t.lower() not in seen: seen.add(t.lower()); final.append(t)
    fm=re.search(r'(<div class="article-tags">)(.*?)(</div>)', h, re.S)
    if fm:
        inner='\n'+'\n'.join(f'            <span class="article-tag">{t}</span>' for t in final)+'\n          '
        h=h[:fm.start(2)]+inner+h[fm.end(2):]
        open(fp,'w',encoding='utf-8').write(h); written+=1
print("rewrote Filed-under on",written,"articles")
print("\nTag1 distribution:",dict(Counter(v['seo1'] for v in out.values()).most_common(20)))
print("\nSample (20):")
for r in rows[:20]:
    s=out[r['slug']]
    print(f"  {r['focus']:9}/{r['type']:11} [{s['seo1']} | {s['seo2']}]  {r['title'][:48]}")
