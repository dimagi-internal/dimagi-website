# Single source of truth for the blog "Filed under" consolidation:
#   each post -> Focus, Type (handled in apply_tag_pass.py) + one specific Country
#   + one Solutions-aligned tag (sector > use case > org type).
# Imported by both apply_tag_pass.py (writes the pages) and build_tag_xlsx.py (the sheet).
#
# The general RULES (keyword maps, pattern-based skips) live here in code.
# The per-slug DECISIONS (country / solutions_tag / skip + a note) live in the editable
# `tag_overrides.csv` next to this file — edit that to retag a post; no code change needed.
import os, csv

# ---- RULES: topical SEO value -> canonical dimagi.com Solutions label --------------
SECTOR = {
    'Maternal & Child Health': 'Maternal, Newborn & Child Health',
    'Mental Health': 'Mental Health',
    'Immunization': 'Immunizations',
    'Nutrition': 'Nutrition',
    'Agriculture': 'Agriculture',
    'Education': 'Education',
    'Community Health Workers': 'Community Health',
    # Canonical dimagi.com / CommCare Solutions wording is "… Prevention & Control".
    'COVID-19': 'Infectious Disease Prevention & Control',
    'Tuberculosis': 'Infectious Disease Prevention & Control',
    'HIV & AIDS': 'Infectious Disease Prevention & Control',
    'Malaria': 'Infectious Disease Prevention & Control',
    'Contact Tracing': 'Infectious Disease Prevention & Control',
    'Family Planning': 'Maternal, Newborn & Child Health',   # folded into the canonical MNCH sector
    'Financial Inclusion': 'Livelihoods',
}
USECASE = {
    'Monitoring & Evaluation': 'Monitoring & Evaluation',
    'Cash Transfers': 'Cash & Voucher Assistance',
    'Case Management': 'Service Delivery',
}
ORGTYPE = {
    'Government Scale': 'Governments',
    'Social Enterprise': 'Social Enterprises',
}

# ---- RULES: country resolution from title/slug / SEO -------------------------------
COUNTRY_WORDS = {  # case-insensitive substring in title/slug -> Country
    'guinea': 'Guinea', 'nigeria': 'Nigeria', 'south africa': 'South Africa',
    'south-africa': 'South Africa', 'ghana': 'Ghana', 'ethiopia': 'Ethiopia',
    'tanzania': 'Tanzania', 'madagascar': 'Madagascar', 'tajikistan': 'Tajikistan',
    'mozambique': 'Mozambique', 'malawi': 'Malawi', 'senegal': 'Senegal',
    'honduras': 'Honduras', 'cambodia': 'Cambodia', 'lesotho': 'Lesotho',
    'jamaica': 'Jamaica',
    'vermont': 'United States', 'arizona': 'United States', 'pima': 'United States',
    'somerville': 'United States', 'martha': 'United States', 'iowa': 'United States',
    'san francisco': 'United States', 'pakistan': 'Pakistan', 'kenya': 'Kenya',
}
SEO_COUNTRIES = {'Guinea','India','Nigeria','South Africa','Ghana','Ethiopia','Tanzania',
    'Madagascar','Tajikistan','Mozambique','Malawi','Senegal','Honduras','Cambodia','Lesotho'}

# ---- RULES: specific country -> Region bucket (the blog geography filter is region-level) --
# Every country resolve_country() can emit must appear here. Region names map to themselves
# and 'Multiple countries' is its own bucket, so resolution is idempotent on re-runs.
# 'Global' / 'None' / '' resolve to no region.
COUNTRY2REGION = {
    'United States': 'United States',
    'India': 'Asia', 'Nepal': 'Asia', 'Tajikistan': 'Asia', 'Cambodia': 'Asia',
    'Indonesia': 'Asia', 'Vietnam': 'Asia', 'Pakistan': 'Asia', 'Bangladesh': 'Asia',
    'Nigeria': 'Africa', 'Sierra Leone': 'Africa', 'Senegal': 'Africa',
    'Guinea': 'Africa', 'Ghana': 'Africa', 'Burkina Faso': 'Africa',
    'Niger': 'Africa', 'Benin': 'Africa', "Cote d'Ivoire": 'Africa',
    'Kenya': 'Africa', 'Ethiopia': 'Africa', 'Somalia': 'Africa',
    'Tanzania': 'Africa', 'Rwanda': 'Africa', 'Uganda': 'Africa',
    'South Africa': 'Africa', 'Malawi': 'Africa', 'Mozambique': 'Africa',
    'Zambia': 'Africa', 'Madagascar': 'Africa', 'Lesotho': 'Africa', 'Cameroon': 'Africa',
    'Mexico': 'Latin America', 'Jamaica': 'Latin America', 'Honduras': 'Latin America',
    'Guatemala': 'Latin America',
    # region self-maps + the multi-country bucket (idempotent round-trip)
    'Africa': 'Africa', 'Asia': 'Asia', 'Latin America': 'Latin America',
    'West Africa': 'Africa', 'East Africa': 'Africa', 'Southern Africa': 'Africa',
    'Multiple countries': 'Multiple countries',
}

# ---- RULES: pattern-based "no country/topic" (staff/series families) ---------------
SKIP_PREFIX = ('a-day-in-the-life', 'day-in-the-life', 'career-journey',
               'building-in-the-open', 'innovation-at-dimagi-part', 'researcher-spotlight',
               'field-research', 'global-digital-health-forum')

# ---- DECISIONS: per-slug overrides loaded from tag_overrides.csv -------------------
COUNTRY_OVERRIDE, TOPIC_OVERRIDE, SKIP_SLUGS = {}, {}, set()
_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tag_overrides.csv')
with open(_CSV, encoding='utf-8') as _f:
    for _r in csv.DictReader(_f):
        _slug = (_r.get('slug') or '').strip()
        if not _slug:
            continue
        if (_r.get('country') or '').strip():
            COUNTRY_OVERRIDE[_slug] = _r['country'].strip()
        if (_r.get('solutions_tag') or '').strip():
            TOPIC_OVERRIDE[_slug] = _r['solutions_tag'].strip()
        if (_r.get('skip') or '').strip().lower() in ('yes', 'y', 'true', '1', 'x'):
            SKIP_SLUGS.add(_slug)

# ---- resolution -------------------------------------------------------------------
def is_skip(slug):
    return slug in SKIP_SLUGS or any(slug.startswith(p) for p in SKIP_PREFIX)

def resolve_country(slug, geo, s1, s2, title):
    if is_skip(slug):
        return ''
    if slug in COUNTRY_OVERRIDE:
        return COUNTRY_OVERRIDE[slug]
    for v in (s1, s2):
        if v in SEO_COUNTRIES:
            return v
    hay = (title + ' ' + slug).lower()
    for w, c in COUNTRY_WORDS.items():
        if w in hay:
            return c
    if geo == 'United States':
        return 'United States'
    return ''   # continent-only / multi-country -> blank

def resolve_region(slug, geo, s1, s2, title):
    # The blog geography filter is REGION-level: resolve the specific country, then map it to
    # its Region bucket (Africa / Asia / Latin America / United States). The 'Multiple countries'
    # bucket is kept as-is; continent-only / global / none -> '' (no region).
    c = resolve_country(slug, geo, s1, s2, title)
    if not c or c == 'None':
        return ''
    return COUNTRY2REGION.get(c, '')

def resolve_topic(slug, s1, s2):
    # An explicit per-slug Solutions tag (tag_overrides.csv) wins even for "skip" posts —
    # e.g. company/recognition posts the user deliberately filed under a sector.
    if slug in TOPIC_OVERRIDE:
        return TOPIC_OVERRIDE[slug]
    if is_skip(slug):
        return ''
    for tier in (SECTOR, USECASE, ORGTYPE):
        for v in (s1, s2):
            if v in tier:
                return tier[v]
    return ''
