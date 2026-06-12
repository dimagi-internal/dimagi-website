#!/usr/bin/env python3
"""Idempotently trim over-length blog meta descriptions to a clean <=155-char
boundary, and keep the 4 copies (meta / og / twitter / JSON-LD) in sync.

Search engines truncate descriptions around 155-160 chars, cutting mid-sentence.
Many Dimagi blog descriptions are WordPress auto-excerpts that run 170-300 chars
and/or end in a dangling "..." . This script:

  - decodes the current <meta name="description"> to plain unicode text
  - if it renders longer than MAX_KEEP chars, trims it to <=TARGET at the last
    sentence end (preferred) or word boundary, dropping trailing "...", commas
    and dangling connector words; never adds an ellipsis
  - writes the trimmed text back to all four locations, escaped correctly for
    each context (HTML attribute vs JSON string)

Re-running is safe: descriptions already <= MAX_KEEP are left untouched, and a
trimmed description is shorter than MAX_KEEP so it is not re-trimmed.

Usage:
  python3 Context/seo/trim_meta.py            # dry-run, prints before/after
  python3 Context/seo/trim_meta.py --apply    # write changes
"""
import os, re, sys, glob, html, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APPLY = "--apply" in sys.argv

TARGET = 155     # aim for <= this many rendered characters
MAX_KEEP = 160   # leave anything <= this untouched
MIN_SENTENCE = 110  # only cut at a sentence end if it keeps at least this much

CONNECTORS = {"and","or","but","the","a","an","to","of","in","for","with","on",
              "at","by","from","as","that","which","who","is","are","was","were",
              "this","its","their","our","we","it","&","into","onto","over","under",
              "between","through","across","about","after","before","while","when",
              "where","than","then","so","such","up","out","off","down","via","per",
              "has","have","had","not","also","more","most","very","both","each",
              "all","any","some","up","upon","within","without","toward","towards",
              "they","them","he","she","you","your","his","her","my","me","i",
              "will","can","may","might","would","could","should","do","does","did",
              "be","been","being","like"}

def trim_text(text):
    """Return text trimmed to <=TARGET rendered chars at a clean boundary."""
    text = text.strip()
    # drop any trailing ellipsis the excerpt generator left behind
    text = re.sub(r'\s*(\.\.\.|…)\s*$', '', text).strip()
    if len(text) <= MAX_KEEP:
        return text  # short enough already (after ellipsis strip)

    window = text[:TARGET + 1]
    # 1) prefer the last sentence end (. ! ?) followed by a space within window
    best = -1
    for m in re.finditer(r'[.!?](?=\s|$)', window):
        end = m.end()
        if end >= MIN_SENTENCE:
            best = end
    if best != -1:
        return text[:best].strip()

    # 2) otherwise cut at the last word boundary <= TARGET
    cut = window.rfind(" ")
    if cut == -1:
        cut = TARGET
    out = text[:cut].strip()
    # strip trailing punctuation and dangling connector words
    out = re.sub(r'[\s,;:–—-]+$', '', out)
    words = out.split()
    while words and words[-1].lower().strip('.,;:') in CONNECTORS:
        words.pop()
    out = " ".join(words)
    out = re.sub(r'[\s,;:–—-]+$', '', out).strip()
    return out

def html_attr(text):
    """Escape plain text for an HTML attribute value (double-quoted)."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

def json_str(text):
    """Escape plain text for a JSON string body (no surrounding quotes)."""
    return json.dumps(text, ensure_ascii=True)[1:-1]

def main():
    changed = 0
    for fp in sorted(glob.glob(os.path.join(ROOT, "blog", "*", "index.html"))):
        if os.sep + "author" in fp:
            continue
        src = open(fp, encoding="utf-8").read()
        m = re.search(r'<meta name="description" content="(.*?)">', src)
        if not m:
            continue
        raw = m.group(1)
        plain = html.unescape(raw)
        if len(plain) <= MAX_KEEP:
            continue
        trimmed = trim_text(plain)
        if trimmed == plain or not trimmed:
            continue

        attr = html_attr(trimmed)
        js = json_str(trimmed)
        new = src
        new = re.sub(r'(<meta name="description" content=")(.*?)(">)',
                     lambda mm: mm.group(1) + attr + mm.group(3), new, count=1)
        new = re.sub(r'(<meta property="og:description" content=")(.*?)(">)',
                     lambda mm: mm.group(1) + attr + mm.group(3), new, count=1)
        new = re.sub(r'(<meta name="twitter:description" content=")(.*?)(">)',
                     lambda mm: mm.group(1) + attr + mm.group(3), new, count=1)
        new = re.sub(r'("description":\s*")(.*?)(",)',
                     lambda mm: mm.group(1) + js + mm.group(3), new, count=1)

        slug = os.path.basename(os.path.dirname(fp))
        changed += 1
        if APPLY:
            open(fp, "w", encoding="utf-8").write(new)
        if changed <= 12 or not APPLY:
            print(f"[{slug}] {len(plain)} -> {len(trimmed)}")
            if changed <= 12:
                print(f"    OLD: {plain}")
                print(f"    NEW: {trimmed}\n")

    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} descriptions trimmed")

if __name__ == "__main__":
    main()
