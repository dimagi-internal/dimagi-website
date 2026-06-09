import json,re,os,html
DIR="Context/blog-import/casestudy_extract"
def clean(c):
    # remove Divi shortcodes (opening tags w/ attrs, and closing) -> keep inner HTML
    c=re.sub(r'\[/?et_pb_[a-z0-9_]+[^\]]*\]',' ',c)
    c=re.sub(r'\[/?et_pb_[a-z0-9_]+\]',' ',c)
    return c
def textblocks(c):
    c=clean(c)
    # extract headings and paragraphs/lists in order
    out=[]
    for m in re.finditer(r'<(h[1-4]|p|li)[^>]*>(.*?)</\1>',c,re.I|re.S):
        tag=m.group(1).lower()
        t=re.sub(r'<[^>]+>','',m.group(2))
        t=html.unescape(t).replace('\xa0',' ').strip()
        t=re.sub(r'\s+',' ',t)
        if not t: continue
        out.append((tag,t))
    return out
for f in sorted(os.listdir(DIR)):
    if not f.endswith('.json'): continue
    d=json.load(open(f"{DIR}/{f}"))
    print("\n"+"="*90)
    print("SLUG:",f[:-5])
    print("TITLE:",html.unescape(d['title']))
    print("EXCERPT:",html.unescape(d['excerpt'])[:300])
    print("FEATURED:",d['featured'])
    print("-"*40)
    seen=set()
    for tag,t in textblocks(d['content']):
        key=(tag,t[:50])
        if key in seen: continue
        seen.add(key)
        if t.upper() in ('CASE STUDY','EXPLORE','COMMCARE','PODCAST','GUIDES AND TOOLKITS'): continue
        print(f"[{tag}] {t}")
