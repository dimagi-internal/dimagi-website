# Cleans leftover WordPress import artifacts from blog ARTICLE BODIES (not metadata).
# Idempotent: re-running on already-clean content changes nothing.
#
#   1. Strip <span style="font-weight: 400;">...</span> wrappers (keep inner content).
#      These are invisible WP cruft, but the prose default is font-weight:350 so the
#      400 spans actually render HEAVIER than the surrounding light text.
#   2. Unwrap <p><figure ...>...</figure></p>  ->  <figure ...>...</figure>
#      (a <figure> is block-level and is invalid inside a <p>).
#   3. Drop standalone empty spacer paragraphs: <p>&nbsp;</p>, <p></p>, <p> </p>, <p>&#160;</p>
#   4. Collapse 2+ consecutive inline &nbsp; into a single normal space inside prose.
#
# Only touches the prose body between <article class="article-body"> and its </article>,
# so nav / cover / related-cards / metadata are never altered. Run:
#     python3 Context/blog-import/clean_wp_artifacts.py
import re, os, glob

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
BLOG = os.path.join(ROOT, "blog")

SPAN400 = re.compile(r'<span style="font-weight: 400;">((?:(?!</?span\b).)*?)</span>', re.S)
FIG_IN_P = re.compile(r'<p>\s*(<figure\b[^>]*>.*?</figure>)\s*</p>', re.S)
EMPTY_P_LINE = re.compile(r'^[ \t]*<p>(?:&nbsp;|&#160;|\s)*</p>[ \t]*\r?\n', re.M)
NBSP_RUN = re.compile(r'(?:&nbsp;\s*){2,}')

BODY = re.compile(r'(<article class="article-body">.*?</article>)', re.S)

def clean_body(body):
    counts = {}
    # 1. strip font-weight:400 spans (loop in case of stacking)
    n = 0
    prev = None
    while prev != body:
        prev = body
        body, k = SPAN400.subn(r'\1', body)
        n += k
    counts['span400'] = n
    # 2. unwrap figures from paragraphs
    body, counts['fig'] = FIG_IN_P.subn(r'\1', body)
    # 3. collapse runs of 2+ &nbsp; to a single space (before empty-p so it can expose them)
    body, counts['nbsprun'] = NBSP_RUN.subn(' ', body)
    # 4. drop empty spacer paragraph lines
    body, counts['emptyp'] = EMPTY_P_LINE.subn('', body)
    return body, counts

def main():
    files = [BLOG + "/index.html"] + sorted(glob.glob(os.path.join(BLOG, "**", "index.html"), recursive=True))
    grand = {'span400':0,'fig':0,'nbsprun':0,'emptyp':0}
    touched = 0
    for fp in files:
        s = open(fp, encoding='utf-8').read()
        m = BODY.search(s)
        if not m:
            continue  # listing / author pages have no article-body
        body = m.group(1)
        new_body, counts = clean_body(body)
        if new_body != body:
            s = s[:m.start()] + new_body + s[m.end():]
            open(fp, 'w', encoding='utf-8').write(s)
            touched += 1
            for k in grand: grand[k] += counts[k]
            rel = os.path.relpath(fp, BLOG)
            print(f"  {rel}: " + ", ".join(f"{k}={v}" for k, v in counts.items() if v))
    print(f"\ntouched {touched} files | totals: " + ", ".join(f"{k}={v}" for k, v in grand.items()))

if __name__ == "__main__":
    main()
