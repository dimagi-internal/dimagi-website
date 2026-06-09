# Fixes DOUBLE-escaped HTML entities across the blog (listing + every article page).
#
# WordPress copy already arrives single-escaped (e.g. "Dimagi&rsquo;s"). A later build
# step re-escaped the leading "&" a second time, producing "&amp;rsquo;". A browser then
# renders that as the LITERAL text "&rsquo;", so cards/sub-headers read "Dimagi&rsquo;s".
#
# This strips exactly one redundant "amp;" layer in front of a real entity token, turning
#   &amp;rsquo;  -> &rsquo;   (renders ')      &amp;amp; -> &amp; (renders &)
#   &amp;ndash;  -> &ndash;   (renders -)      etc.
# Legitimate single escapes ("M&amp;E", "Johnson &amp; Johnson") are untouched because the
# pattern only matches "&amp;" immediately followed by a known entity name + ";".
#
# Idempotent: re-running on already-fixed content changes nothing. Run:
#     python3 Context/blog-import/fix_entities.py
import re, os, glob

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
BLOG = os.path.join(ROOT, "blog")

# Named/numeric entity tokens that can legitimately appear right after a "&".
TOKEN = (r'amp|lt|gt|quot|apos|nbsp|copy|reg|trade|hellip|mdash|ndash|'
         r'lsquo|rsquo|ldquo|rdquo|sbquo|bdquo|laquo|raquo|deg|times|'
         r'#[0-9]+|#x[0-9a-fA-F]+')
DOUBLE = re.compile(r'&amp;(' + TOKEN + r');')

def fix(text):
    # Loop to collapse any multi-layer escaping (&amp;amp;rsquo; -> &amp;rsquo; -> &rsquo;).
    prev = None
    n = 0
    while prev != text:
        prev = text
        text, k = DOUBLE.subn(r'&\1;', text)
        n += k
    return text, n

def main():
    files = [os.path.join(BLOG, "index.html")] + sorted(glob.glob(os.path.join(BLOG, "*", "index.html")))
    total_files = 0
    total_subs = 0
    for fp in files:
        s = open(fp, encoding='utf-8').read()
        new, k = fix(s)
        if k:
            open(fp, 'w', encoding='utf-8').write(new)
            total_files += 1
            total_subs += k
            print(f"  {os.path.relpath(fp, ROOT)}: {k}")
    print(f"\nfixed {total_subs} double-escaped entities across {total_files} files")

if __name__ == "__main__":
    main()
