#!/usr/bin/env python3
"""Normalize the Dimagi Pre-Login footer + chrome across every page.

The footer is copied inline into all ~293 pages and is regularly clobbered back
to an older shape by the blog/company page generators. This script REWRITES each
page's entire <footer>...</footer> block to the one canonical, agreed-upon footer
(the redesigned one first shipped on the home page), with relative paths fixed up
for each page's directory depth. It is IDEMPOTENT and safe to re-run any time
pages drift (e.g. after a regen).

Why wholesale replacement (vs. surgical edits): it is the only thing that both
standardizes the OLD inner-page footers AND re-asserts the NEW shape after a
generator clobbers a page. It also sidesteps the legacy "legal-sidebar trap"
entirely -- the in-body <ul class="legal-sidebar-nav"> on /legal/<doc>/ pages
lives OUTSIDE <footer>, so replacing only the <footer> block never touches it.

Canonical footer (set 2026-06-08):
  - Brand column: logo, mission line, colored social icons (LinkedIn/YouTube),
    cert badges (B Corp + Climate Neutral).
  - Columns: Products (Connect first), Professional Services, Company, Contact.
    NO Legal column.
  - Newsletter compacted under the Contact column (visual-only form).
  - Bottom legal row (shortened labels): Privacy, Terms, Business Agreement,
    Acceptable Use, Financial Conflict, Transparency, Trust Center.

Usage:
    python3 Context/normalize_footer.py           # fix in place, print a report
    python3 Context/normalize_footer.py --check    # report drift only, write nothing
                                                    # (exit code 1 if any drift)
"""
import os
import re
import sys
import glob

# ── ROOT = the Dimagi Pre-Login folder (this file lives in Context/) ──
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── CONVENTIONS (change here, re-run) ──
STYLES_V = "16"
NAV_V = "7"
OLD_MISSIONS = [
    "Technology that empowers frontline workers, strengthens programs, and drives lasting change in communities worldwide.",
]
NEW_MISSION = "Building and scaling sustainable, high-impact digital solutions that amplify frontline work."

# Canonical footer block. "{P}" is replaced with the page's relative path prefix
# to site root ("" for the home page, "../" one level down, "../../" two, ...).
FOOTER_TEMPLATE = '''<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img class="footer-logo" src="{P}assets/dimagi-logo.png" alt="Dimagi">
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
            <img src="{P}assets/images/about/b-corp-logo.png" alt="Certified B Corporation" loading="lazy">
          </a>
          <a class="footer-cert climate" href="https://www.climateneutral.org/brand/dimagi" target="_blank" rel="noopener" aria-label="Climate Neutral Certified">
            <img src="{P}assets/images/about/climate-neutral-badge.png" alt="Climate Neutral Certified" loading="lazy">
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
          <li><a href="{P}professional-services/global-services/index.html">Global Services</a></li>
          <li><a href="{P}professional-services/united-states/index.html">United States</a></li>
          <li><a href="{P}professional-services/india/index.html">India</a></li>
          <li><a href="{P}professional-services/research-data/index.html">Research &amp; Data</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="{P}company/about/index.html">About Us</a></li>
          <li><a href="{P}company/our-approach/index.html">Our Approach</a></li>
          <li><a href="{P}blog/index.html">Blog</a></li>
          <li><a href="{P}podcast/index.html">Podcast</a></li>
          <li><a href="{P}company/careers/index.html">Careers</a></li>
          <li><a href="{P}awards/index.html">Awards</a></li>
          <li><a href="{P}press/index.html">Press &amp; Coverage</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <ul>
          <li><a href="{P}contact/index.html">Contact Us</a></li>
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
        <a href="{P}legal/privacy-policy/index.html">Privacy</a>
        <a href="{P}legal/terms-of-service/index.html">Terms</a>
        <a href="{P}legal/business-agreement/index.html">Business Agreement</a>
        <a href="{P}legal/acceptable-use/index.html">Acceptable Use</a>
        <a href="{P}legal/financial-conflict/index.html">Financial Conflict</a>
        <a href="{P}legal/transparency-coverage/index.html">Transparency</a>
        <a href="https://dimagi.safebase.us/" target="_blank" rel="noopener">Trust Center</a>
      </div>
    </div>
  </div>
</footer>'''

# ── regexes ──
RE_STYLES = re.compile(r'styles\.css\?v=\d+')
RE_NAV = re.compile(r'nav\.js\?v=\d+')
RE_FOOTER = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S)


def build_footer(prefix):
    return FOOTER_TEMPLATE.replace('{P}', prefix)


def rel_prefix(path):
    """Relative path prefix from a page to the site root.

    "" for ROOT/index.html, "../" one dir down, "../../" two, etc.
    The blog template lives in Context/ but renders to /blog/<slug>/ (depth 2).
    """
    if os.path.basename(path) == 'blog_article_template.html':
        return '../../'
    rel = os.path.relpath(path, ROOT)
    depth = rel.count(os.sep)  # dirs between the file and root
    return '../' * depth


def normalize(html, prefix):
    """Return the normalized html (idempotent)."""
    # 1) cache-busters (these live in <head>/<script>, outside the footer)
    html = RE_STYLES.sub('styles.css?v=' + STYLES_V, html)
    html = RE_NAV.sub('nav.js?v=' + NAV_V, html)

    # 2) mission line anywhere it still appears in old copy
    for old in OLD_MISSIONS:
        html = html.replace(old, NEW_MISSION)

    # 3) wholesale-replace the footer block (pages with no <footer>, e.g.
    #    sign-in, are left untouched).
    if RE_FOOTER.search(html):
        html = RE_FOOTER.sub(lambda m: build_footer(prefix), html, count=1)

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
        new = normalize(orig, rel_prefix(f))
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
