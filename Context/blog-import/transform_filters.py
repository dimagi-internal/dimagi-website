# Owns the blog listing's FILTER UI.
# Emits a search box + four custom "pill" dropdowns (Focus / Type / Region / Sectors),
# the inline filter JS, and the dropdown CSS, and writes the per-card filter data
# attributes (data-product/type/topic/country=region/sector).
#
# Idempotent & non-lossy: reads the CURRENT card data attributes and preserves them
# (Focus topic 'Dimagi' is kept; region keys round-trip), so it can be re-run on the
# already-transformed state. Sectors come from consolidation_maps.resolve_topic so they
# stay aligned with each article's "Filed under" Solutions tag.
#
# Run order after a foreign blog regen (render_all.py):
#     python3 Context/blog-import/transform_filters.py
#     python3 Context/blog-import/apply_tag_pass.py
import re, os, sys, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from consolidation_maps import resolve_topic, resolve_country

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
IDX = os.path.join(ROOT, "blog", "index.html")
SEO = json.load(open(os.path.join(ROOT, "Context/blog-import/seo_tags.json")))

# Focus topics worth keeping as a Focus value (everything else collapses to None).
KEEP_TOPICS = {'Company', 'Ecosystem', 'Dimagi'}

# Specific country -> Region bucket. Region keys map to themselves so re-runs are stable.
COUNTRY2REGION = {
    'United States': 'United States',
    'India': 'Asia', 'Nepal': 'Asia', 'Tajikistan': 'Asia', 'Cambodia': 'Asia',
    'Indonesia': 'Asia', 'Vietnam': 'Asia', 'Pakistan': 'Asia',
    'Nigeria': 'Africa', 'Sierra Leone': 'Africa', 'Senegal': 'Africa',
    'Guinea': 'Africa', 'Ghana': 'Africa', 'Burkina Faso': 'Africa',
    'Niger': 'Africa', 'Benin': 'Africa', "Cote d'Ivoire": 'Africa',
    'Kenya': 'Africa', 'Ethiopia': 'Africa', 'Somalia': 'Africa',
    'Tanzania': 'Africa', 'Rwanda': 'Africa', 'Uganda': 'Africa',
    'South Africa': 'Africa', 'Malawi': 'Africa', 'Mozambique': 'Africa',
    'Zambia': 'Africa', 'Madagascar': 'Africa', 'Lesotho': 'Africa',
    'Mexico': 'Latin America', 'Jamaica': 'Latin America', 'Honduras': 'Latin America',
    'Guatemala': 'Latin America',
    'Global': 'None',
    'West Africa': 'Africa', 'East Africa': 'Africa', 'Southern Africa': 'Africa',
    'Africa': 'Africa', 'Asia': 'Asia', 'Latin America': 'Latin America',
}

PRODUCTS = ['CommCare', 'Connect', 'SureAdhere', 'Open Chat Studio']

# ---- ordered taxonomies for the dropdowns --------------------------------------------
FOCUS_ORDER  = ['CommCare', 'Connect', 'SureAdhere', 'Open Chat Studio', 'Dimagi']
TYPE_ORDER   = ['Case Study', 'Reflections', 'Announcement', 'Event']
REGION_ORDER = ['Africa', 'Asia', 'Latin America', 'United States']
# Sectors dropdown groups (broader "Solutions" set), sectors first in dimagi.com order.
SECTOR_ORDER  = ['Community Health', 'Primary Care', 'Immunizations',
                 'Maternal, Newborn & Child Health', 'Nutrition', 'Non-Communicable Diseases',
                 'Infectious Disease Prevention & Control', 'Mental Health', 'Agriculture',
                 'Education', 'Humanitarian Response', 'Livelihoods',
                 'Early Childhood Development', 'WASH']
USECASE_ORDER = ['Monitoring & Evaluation', 'Service Delivery', 'Research',
                 'Cash & Voucher Assistance', 'Campaigns', 'Remote Engagement',
                 'Workforce Management', 'Clinical Trials', 'Sponsorship']
ORGTYPE_ORDER = ['Governments', 'Social Enterprises']

s = open(IDX, encoding='utf-8').read()

# ---- 1. rewrite each card's filter data attributes -----------------------------------
present = {'focus': Counter(), 'type': Counter(), 'country': Counter(), 'sector': Counter()}

def a(v):  # escape ampersands for HTML attributes / text
    return v.replace('&', '&amp;')

def retag_block(m):
    block = m.group(0)
    open_tag = re.search(r'<article class="blog-card"[^>]*>', block).group(0)
    attrs = dict(re.findall(r'data-(\w+)="([^"]*)"', open_tag))
    sm = re.search(r'href="([^"/]+)/index\.html"', block)
    slug = sm.group(1) if sm else ''
    product = attrs.get('product') or 'None'
    ctype   = attrs.get('type') or 'None'
    topic   = attrs.get('topic', '')
    topic   = topic if topic in KEEP_TOPICS else 'None'
    if topic == 'Company':
        topic = 'Dimagi'
    tm = re.search(r'<h2 class="blog-card-title">(.*?)</h2>', block, re.S)
    title = re.sub('<[^>]+>', '', tm.group(1)).strip() if tm else ''
    se = SEO.get(slug, {})
    # Country = the SPECIFIC country (resolve_country), matching each article's "Filed under".
    # Continent-only / multi-country / global posts -> 'None'.
    country = resolve_country(slug, attrs.get('country', ''), se.get('seo1', ''), se.get('seo2', ''), title) or 'None'
    sector  = resolve_topic(slug, se.get('seo1', ''), se.get('seo2', '')) or 'None'
    # tally what's actually present for option building
    focus = product if product in PRODUCTS else (topic if topic in KEEP_TOPICS else 'None')
    if focus and focus != 'None': present['focus'][focus] += 1
    if ctype and ctype != 'None':  present['type'][ctype] += 1
    if country != 'None':          present['country'][country] += 1
    if sector != 'None':           present['sector'][sector] += 1
    new_open = (f'<article class="blog-card" data-product="{a(product)}" data-type="{a(ctype)}" '
                f'data-topic="{a(topic)}" data-country="{a(country)}" data-sector="{a(sector)}">')
    return block.replace(open_tag, new_open, 1)

s, ncards = re.subn(r'<article class="blog-card".*?</article>', retag_block, s, flags=re.S)

# ---- 2. build the filter bar markup --------------------------------------------------
def option(value):
    return (f'            <button type="button" class="blog-dd-option" role="option" '
            f'data-value="{a(value)}">{a(value)}</button>')

def dropdown(dim, label, all_label, groups, trailing=None):
    """groups: list of (group_title_or_None, [values]); empty groups are skipped.
    trailing: optional list of special option values (e.g. 'Multiple countries', 'None')
    rendered after a divider at the bottom of the menu."""
    out = [f'        <div class="blog-dd" data-dim="{dim}">',
           f'          <button type="button" class="blog-dd-trigger" aria-haspopup="listbox" aria-expanded="false">'
           f'<span class="blog-dd-label">{label}</span><span class="blog-dd-value">All</span>'
           f'<span class="blog-dd-chevron" aria-hidden="true"></span></button>',
           f'          <div class="blog-dd-menu" role="listbox" aria-label="{label}" hidden>',
           f'            <button type="button" class="blog-dd-option is-active" role="option" '
           f'data-value="all" aria-selected="true">{all_label}</button>']
    for title, values in groups:
        vals = [v for v in values if v]
        if not vals:
            continue
        if title:
            out.append(f'            <div class="blog-dd-group">{title}</div>')
        out.extend(option(v) for v in vals)
    if trailing:
        out.append('            <div class="blog-dd-sep" role="separator"></div>')
        out.extend(option(v) for v in trailing)
    out.append('          </div>')
    out.append('        </div>')
    return "\n".join(out)

def present_in_order(dim, order):
    pres = present[dim]
    ordered = [v for v in order if v in pres]
    extra = [v for v in pres if v not in order]   # safety: never silently drop a value
    return ordered + sorted(extra)

# Display labels (data-dim keys are kept as-is so the JS/matching is untouched):
#   data-dim "focus"  -> "Platform",  "country" -> "Country",  "sector" -> "Focus".
product_dd = dropdown('focus', 'Platform', 'All platforms',
                      [(None, present_in_order('focus', FOCUS_ORDER))])
type_dd    = dropdown('type', 'Type', 'All types',
                      [(None, present_in_order('type', TYPE_ORDER))])
# Country: specific countries A-Z, then "Multiple countries" + "None" pinned at the bottom.
specific_countries = sorted(c for c in present['country'] if c != 'Multiple countries')
country_trailing = (['Multiple countries'] if 'Multiple countries' in present['country'] else []) + ['None']
country_dd = dropdown('country', 'Country', 'All countries',
                      [(None, specific_countries)], trailing=country_trailing)
sec_pres   = present['sector']
focus_dd   = dropdown('sector', 'Focus', 'All focus areas', [
    ('Sectors',       [v for v in SECTOR_ORDER if v in sec_pres]),
    ('Use cases',     [v for v in USECASE_ORDER if v in sec_pres]),
    ('Organizations', [v for v in ORGTYPE_ORDER if v in sec_pres]),
    (None,            sorted(v for v in sec_pres
                             if v not in SECTOR_ORDER + USECASE_ORDER + ORGTYPE_ORDER)),
], trailing=['None'])

filters_html = (
    '      <div class="blog-filters" role="group" aria-label="Filter and search posts">\n'
    '        <div class="blog-search">\n'
    '          <svg class="blog-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.65" y2="16.65"></line></svg>\n'
    '          <input type="search" id="blogSearch" class="blog-search-input" placeholder="Search articles" aria-label="Search articles" autocomplete="off">\n'
    '        </div>\n'
    + product_dd + '\n' + type_dd + '\n' + country_dd + '\n' + focus_dd + '\n'
    + '        <button type="button" class="blog-clear" id="blogClear" hidden>Clear all</button>\n'
    '      </div>\n\n'
    '      <p class="blog-empty" id="blogEmpty" hidden>No articles match your filters. '
    '<button type="button" class="blog-empty-reset" id="blogEmptyReset">Clear filters</button></p>'
)

s = re.sub(r'<div class="blog-filters".*?(?=<div class="blog-grid")',
           filters_html + '\n\n      ', s, flags=re.S, count=1)

# ---- 3. dropdown + search CSS (between markers, before </style>) ----------------------
CSS_START = '/* == blog filter bar (dropdowns + search) :: generated == */'
CSS_END   = '/* == end blog filter bar == */'
CSS = r"""
.blog-filters { display: flex; flex-flow: row wrap; align-items: center; gap: 12px; margin-bottom: 40px; }
.blog-filters[hidden] { display: none; }
.blog-search { position: relative; flex: 1 1 230px; min-width: 200px; max-width: 320px; }
.blog-search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--muted-soft); pointer-events: none; }
.blog-search-input { width: 100%; font-family: var(--sans); font-size: 14px; color: var(--ink); padding: 11px 16px 11px 42px; border: 1px solid var(--line); border-radius: 999px; background: #fff; transition: border-color 150ms, box-shadow 150ms; }
.blog-search-input::placeholder { color: var(--muted-soft); }
.blog-search-input:focus { outline: none; border-color: var(--indigo); box-shadow: 0 0 0 3px rgba(56,67,208,0.12); }
.blog-dd { position: relative; }
.blog-dd-trigger { display: inline-flex; align-items: center; gap: 8px; font-family: var(--sans); font-size: 13px; font-weight: 500; padding: 10px 15px; border-radius: 999px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; transition: border-color 150ms, background 150ms; }
.blog-dd-trigger:hover { border-color: var(--rule); }
.blog-dd-label { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-soft); }
.blog-dd-value { color: var(--ink); }
.blog-dd-chevron { width: 7px; height: 7px; border-right: 1.5px solid var(--muted); border-bottom: 1.5px solid var(--muted); transform: rotate(45deg) translateY(-2px); margin-left: 1px; transition: transform 150ms; }
.blog-dd.is-open .blog-dd-trigger { border-color: var(--indigo); }
.blog-dd.is-open .blog-dd-chevron { transform: rotate(-135deg) translateY(1px); }
.blog-dd.is-set .blog-dd-trigger { border-color: var(--indigo); background: var(--paper-cool); }
.blog-dd.is-set .blog-dd-label { color: var(--indigo); }
.blog-dd-menu { position: absolute; top: calc(100% + 8px); left: 0; z-index: 40; min-width: 230px; max-height: 360px; overflow-y: auto; padding: 6px; background: #fff; border: 1px solid var(--line); border-radius: 14px; box-shadow: 0 14px 36px rgba(20,22,55,0.16); }
.blog-dd-menu[hidden] { display: none; }
.blog-dd-group { font-family: var(--sans); font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted-soft); padding: 10px 12px 4px; }
.blog-dd-group:first-child { padding-top: 4px; }
.blog-dd-option { display: flex; align-items: center; justify-content: space-between; gap: 10px; width: 100%; text-align: left; font-family: var(--sans); font-size: 13.5px; color: var(--ink); padding: 9px 12px; border: 0; border-radius: 9px; background: none; cursor: pointer; }
.blog-dd-option:hover { background: var(--paper-cool); }
.blog-dd-option.is-active { color: var(--indigo); font-weight: 600; }
.blog-dd-option.is-active::after { content: "\2713"; font-size: 12px; }
.blog-dd-sep { height: 1px; background: var(--line); margin: 6px 8px; }
.blog-clear { font-family: var(--sans); font-size: 13px; font-weight: 600; color: var(--indigo); background: none; border: 0; cursor: pointer; padding: 8px 6px; margin-left: 2px; }
.blog-clear[hidden] { display: none; }
.blog-clear:hover { text-decoration: underline; }
.blog-empty-reset { font-family: var(--sans); font-size: 15px; font-weight: 600; color: var(--indigo); background: none; border: 0; cursor: pointer; padding: 0; }
.blog-empty-reset:hover { text-decoration: underline; }
@media (max-width: 760px) { .blog-search { flex-basis: 100%; max-width: none; order: -1; } .blog-dd-menu { min-width: 200px; } }
"""
css_block = CSS_START + CSS + CSS_END
if CSS_START in s:
    s = re.sub(re.escape(CSS_START) + r'.*?' + re.escape(CSS_END), lambda _m: css_block, s, flags=re.S)
else:
    s = s.replace('</style>', css_block + '\n</style>', 1)

# ---- 4. inline filter JS (replace the <script> that holds `var INITIAL`) --------------
JS = r"""
/* Blog listing: search + Focus/Type/Region/Sectors dropdowns (AND), progressive reveal.
   Generated by Context/blog-import/transform_filters.py */
(function () {
  var INITIAL = 13, BATCH = 15;
  var DIMS = ['focus', 'type', 'country', 'sector'];
  // URL param names follow the visible labels (data-dim "focus"=Product, "sector"=Focus).
  var URLKEY = { focus: 'product', type: 'type', country: 'country', sector: 'focus' };
  var cards = [].slice.call(document.querySelectorAll('.blog-grid .blog-card'));
  var wrap = document.getElementById('blogMore');
  var btn = document.getElementById('blogMoreBtn');
  var empty = document.getElementById('blogEmpty');
  var clearBtn = document.getElementById('blogClear');
  var searchInput = document.getElementById('blogSearch');
  if (!cards.length || !wrap || !btn) return;

  var active = { focus: 'all', type: 'all', country: 'all', sector: 'all' };
  var query = '';
  var shown = INITIAL;
  var params = new URLSearchParams(window.location.search);

  // Optional "series" view (?series=careers from the Careers page): hide filters, match by title.
  var SERIES = { careers: { title: 'Day in the Life & Career Journeys',
    test: function (t) { return /day in the life|career journey/i.test(t); } } };
  var series = SERIES[(params.get('series') || '').toLowerCase()] || null;
  var filtersEl = document.querySelector('.blog-filters');
  if (series) { if (filtersEl) filtersEl.hidden = true; shown = 9999; }
  function seriesMatch(card) {
    if (!series) return true;
    var t = card.querySelector('.blog-card-title');
    return t ? series.test(t.textContent || '') : false;
  }

  // Focus is virtual: the card's product if it has one, else a Dimagi topic, else None.
  var FOCUS_PRODUCTS = { 'CommCare': 1, 'Connect': 1, 'SureAdhere': 1, 'Open Chat Studio': 1 };
  var FOCUS_TOPICS = { 'Dimagi': 1 };
  function focusOf(card) {
    var p = card.dataset.product || '', t = card.dataset.topic || '';
    if (FOCUS_PRODUCTS[p]) return p;
    if (FOCUS_TOPICS[t]) return t;
    return 'None';
  }
  function dimValue(card, dim) {
    return dim === 'focus' ? focusOf(card) : (card.dataset[dim] || 'None');
  }
  function searchText(card) {
    var t = card.querySelector('.blog-card-title'), d = card.querySelector('.blog-card-desc');
    return ((t ? t.textContent : '') + ' ' + (d ? d.textContent : '')).toLowerCase();
  }
  function matches(card) {
    if (!seriesMatch(card)) return false;
    if (query && searchText(card).indexOf(query) === -1) return false;
    return DIMS.every(function (dim) {
      return active[dim] === 'all' || dimValue(card, dim) === active[dim];
    });
  }
  function anyActive() {
    return query !== '' || DIMS.some(function (d) { return active[d] !== 'all'; });
  }

  function render() {
    var visibleCount = 0, matchCount = 0, firstVisible = null;
    cards.forEach(function (card) {
      if (matches(card)) {
        matchCount++;
        if (visibleCount < shown) { card.classList.remove('is-hidden'); if (!firstVisible) firstVisible = card; visibleCount++; }
        else card.classList.add('is-hidden');
      } else card.classList.add('is-hidden');
    });
    cards.forEach(function (card) { card.classList.toggle('is-featured', card === firstVisible); });
    wrap.hidden = visibleCount >= matchCount;
    if (empty) empty.hidden = matchCount > 0;
    if (clearBtn) clearBtn.hidden = !anyActive();
  }
  btn.addEventListener('click', function () { shown += BATCH; render(); });

  function syncUrl() {
    if (series) return;
    try {
      var p = new URLSearchParams();
      DIMS.forEach(function (dim) { if (active[dim] !== 'all') p.set(URLKEY[dim], active[dim]); });
      if (query) p.set('q', searchInput ? searchInput.value.trim() : query);
      var qs = p.toString();
      history.replaceState(null, '', qs ? ('?' + qs) : window.location.pathname);
    } catch (e) { /* file:// — pushState/replaceState may throw; ignore */ }
  }

  // ---- dropdowns ----
  var dds = [].slice.call(document.querySelectorAll('.blog-dd'));
  function closeAll(except) {
    dds.forEach(function (dd) {
      if (dd === except) return;
      dd.classList.remove('is-open');
      var m = dd.querySelector('.blog-dd-menu'); if (m) m.hidden = true;
      var tr = dd.querySelector('.blog-dd-trigger'); if (tr) tr.setAttribute('aria-expanded', 'false');
    });
  }
  dds.forEach(function (dd) {
    var dim = dd.getAttribute('data-dim');
    var trigger = dd.querySelector('.blog-dd-trigger');
    var menu = dd.querySelector('.blog-dd-menu');
    var valueEl = dd.querySelector('.blog-dd-value');
    var options = [].slice.call(dd.querySelectorAll('.blog-dd-option'));
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !dd.classList.contains('is-open');
      closeAll(dd);
      dd.classList.toggle('is-open', open);
      menu.hidden = !open;
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    options.forEach(function (opt) {
      opt.addEventListener('click', function () {
        var val = opt.getAttribute('data-value');
        active[dim] = val;
        options.forEach(function (o) {
          var on = o === opt;
          o.classList.toggle('is-active', on);
          o.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        valueEl.textContent = val === 'all' ? 'All' : opt.textContent;
        dd.classList.toggle('is-set', val !== 'all');
        closeAll(null);
        shown = INITIAL; render(); syncUrl();
      });
    });
  });
  document.addEventListener('click', function () { closeAll(null); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(null); });

  // ---- search ----
  if (searchInput) {
    var deb;
    searchInput.addEventListener('input', function () {
      clearTimeout(deb);
      deb = setTimeout(function () {
        query = searchInput.value.trim().toLowerCase();
        shown = INITIAL; render(); syncUrl();
      }, 120);
    });
  }

  // ---- clear ----
  function resetDd(dd) {
    var opts = [].slice.call(dd.querySelectorAll('.blog-dd-option'));
    opts.forEach(function (o, i) {
      var on = i === 0;
      o.classList.toggle('is-active', on);
      o.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    dd.classList.remove('is-set');
    var v = dd.querySelector('.blog-dd-value'); if (v) v.textContent = 'All';
  }
  function clearAll() {
    DIMS.forEach(function (d) { active[d] = 'all'; });
    query = '';
    if (searchInput) searchInput.value = '';
    dds.forEach(resetDd);
    shown = INITIAL; render(); syncUrl();
  }
  if (clearBtn) clearBtn.addEventListener('click', clearAll);
  var emptyReset = document.getElementById('blogEmptyReset');
  if (emptyReset) emptyReset.addEventListener('click', clearAll);

  // ---- restore state from the URL (shareable filtered views) ----
  (function applyFromUrl() {
    if (series) return;
    var q = params.get('q');
    if (q && searchInput) { searchInput.value = q; query = q.trim().toLowerCase(); }
    DIMS.forEach(function (dim) {
      var raw = params.get(URLKEY[dim]); if (!raw) return;
      var dd = document.querySelector('.blog-dd[data-dim="' + dim + '"]'); if (!dd) return;
      var opt = [].slice.call(dd.querySelectorAll('.blog-dd-option')).filter(function (o) {
        return o.getAttribute('data-value').toLowerCase() === raw.toLowerCase();
      })[0];
      if (opt) opt.click();   // reuse the option handler (sets active + label + state)
    });
  })();

  render();

  // Fade cover images in as they load.
  cards.forEach(function (card) {
    var img = card.querySelector('.blog-card-image img');
    if (!img || (img.complete && img.naturalWidth)) return;
    img.classList.add('img-pending');
    var done = function () { img.classList.remove('img-pending'); };
    img.addEventListener('load', done, { once: true });
    img.addEventListener('error', done, { once: true });
  });
})();
"""
new_script = '<script>' + JS + '</script>'
s, njs = re.subn(r'<script>(?:(?!</script>).)*?var INITIAL\b.*?</script>',
                 lambda _m: new_script, s, flags=re.S, count=1)

open(IDX, 'w', encoding='utf-8').write(s)

print(f"retagged {ncards} cards; script blocks replaced: {njs}")
for dim, order in (('focus', FOCUS_ORDER), ('type', TYPE_ORDER)):
    print(f"  {dim:8s}:", {v: present[dim][v] for v in present_in_order(dim, order)})
print(f"  country : {dict(present['country'].most_common())}  (+{ncards - sum(present['country'].values())} None)")
print("  sector  :", dict(present['sector'].most_common()))
