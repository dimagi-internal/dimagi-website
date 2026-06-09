#!/usr/bin/env python3
"""Normalize the Dimagi Pre-Login footer + nav chrome across every page.

The footer/nav is copied inline into all ~293 pages and is regularly clobbered
back to an older shape by the blog/company page generators. This script puts
every page back to the agreed conventions. It is IDEMPOTENT and footer-anchored,
so it is safe to re-run any time pages drift (e.g. after a regen).

What it enforces (edit the CONSTANTS below to change a convention once):
  1. Cache-busters: styles.css?v=<STYLES_V>, nav.js?v=<NAV_V>.
  2. Footer brand mission line -> NEW_MISSION.
  3. Footer "Products" column order: Connect before CommCare.
  4. Footer "Legal" column: "Financial Conflict of Interest" and
     "Transparency in Coverage" live in the footer-legal BOTTOM ROW (before
     Trust Center), NOT in the Legal column.

IMPORTANT TRAP this script is built around: the /legal/<doc>/ pages also contain
an in-body <ul class="legal-sidebar-nav"> that lists all 6 legal docs. That
sidebar must keep all 6. So the Legal-column edit is anchored at the footer
heading <h5>Legal</h5> and only touches text AFTER it -- the sidebar (which
appears earlier in the document) is never modified.

Usage:
    python3 Context/normalize_footer.py          # fix in place, print a report
    python3 Context/normalize_footer.py --check   # report drift only, write nothing
                                                   # (exit code 1 if any drift)
"""
import os
import re
import sys
import glob

# ── ROOT = the Dimagi Pre-Login folder (this file lives in Context/) ──
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── CONVENTIONS (change here, re-run) ──
STYLES_V = "14"
NAV_V = "6"
OLD_MISSIONS = [
    "Technology that empowers frontline workers, strengthens programs, and drives lasting change in communities worldwide.",
]
NEW_MISSION = "Building and scaling sustainable, high-impact digital solutions that amplify frontline work."

CC = '<li><a href="https://dimagi.com/commcare/" target="_blank" rel="noopener">CommCare</a></li>'
CN = '<li><a href="https://connect.dimagi.com/" target="_blank" rel="noopener">Connect</a></li>'

# ── regexes ──
RE_STYLES = re.compile(r'styles\.css\?v=\d+')
RE_NAV = re.compile(r'nav\.js\?v=\d+')
RE_PROD_SWAP = re.compile(r'([ \t]*)' + re.escape(CC) + r'\n([ \t]*)' + re.escape(CN))
RE_LI_FC = re.compile(r'[ \t]*<li><a href="([^"]*legal/financial-conflict/index\.html)">Financial Conflict of Interest</a></li>\n')
RE_LI_TC = re.compile(r'[ \t]*<li><a href="([^"]*legal/transparency-coverage/index\.html)">Transparency in Coverage</a></li>\n')
RE_FL_BLOCK = re.compile(r'<div class="footer-legal">(.*?)</div>', re.S)
RE_PRIVACY_PREF = re.compile(r'<a href="([^"]*?)legal/privacy-policy/index\.html">Privacy</a>')
RE_TRUST = re.compile(r'(\n[ \t]*)<a href="https://dimagi\.safebase\.us/" target="_blank" rel="noopener">Trust Center</a>')


def normalize(html):
    """Return the normalized html (idempotent)."""
    # 1) cache-busters
    html = RE_STYLES.sub('styles.css?v=' + STYLES_V, html)
    html = RE_NAV.sub('nav.js?v=' + NAV_V, html)

    # 2) mission line
    for old in OLD_MISSIONS:
        html = html.replace(old, NEW_MISSION)

    # 3) footer Products order: Connect before CommCare
    html = RE_PROD_SWAP.sub(lambda m: m.group(1) + CN + '\n' + m.group(2) + CC, html)

    # 4) footer Legal column move (anchored at <h5>Legal</h5>; sidebar untouched)
    mh = html.find('<h5>Legal</h5>')
    if mh != -1:
        head, tail = html[:mh], html[mh:]
        tail = RE_LI_FC.sub('', tail, count=1)
        tail = RE_LI_TC.sub('', tail, count=1)
        html = head + tail

    m = RE_FL_BLOCK.search(html)
    if m and 'financial-conflict' not in m.group(1):
        pm = RE_PRIVACY_PREF.search(m.group(1))
        if pm:
            pref = pm.group(1)
            fc = pref + 'legal/financial-conflict/index.html'
            tc = pref + 'legal/transparency-coverage/index.html'

            def repl(mm, fc=fc, tc=tc):
                ws = mm.group(1)
                return (ws + '<a href="%s">Financial Conflict of Interest</a>' % fc
                        + ws + '<a href="%s">Transparency in Coverage</a>' % tc
                        + ws + '<a href="https://dimagi.safebase.us/" target="_blank" rel="noopener">Trust Center</a>')
            html = RE_TRUST.sub(repl, html, count=1)
    return html


def targets():
    """All site HTML pages, plus the blog template (so regens inherit the footer)."""
    for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if os.sep + 'Context' + os.sep in f or os.sep + '.git' + os.sep in f:
            continue
        yield f
    tmpl = os.path.join(ROOT, 'Context', 'blog_article_template.html')
    if os.path.exists(tmpl):
        yield tmpl


def main():
    check = '--check' in sys.argv
    drifted = []
    for f in targets():
        orig = open(f, encoding='utf-8').read()
        new = normalize(orig)
        if new != orig:
            drifted.append(os.path.relpath(f, ROOT))
            if not check:
                open(f, 'w', encoding='utf-8').write(new)
    verb = "would change" if check else "normalized"
    print("%s: %d file(s)" % (verb, len(drifted)))
    for d in drifted:
        print("   ", d)
    if check and drifted:
        sys.exit(1)


if __name__ == '__main__':
    main()
