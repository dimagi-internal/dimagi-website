#!/usr/bin/env python3
"""Single source of truth for High-Impact Growth episode tags + the /podcast/ filter.

Imported by build_episode.py (emits the hero chip row + chip CSS) and
build_listing.py (emits card data-attributes + the filter bar / CSS / JS), so a
regeneration *produces* the tags instead of wiping them.

Tag families:
  - product : commcare / sureadhere / connect / open-chat-studio       (teal chip)
  - sector / usecase / orgtype : the CommCare pre-login "Solutions" IA  (neutral chip)
  - theme   : ai / global-development / company-culture / leadership    (outline chip)
  - staff   : Dimagi-staff episode -> filter facet only (no visible chip)

Edit TAGS (keyed by episode number) to retag an episode.
"""

LABEL = {
    'commcare': 'CommCare', 'sureadhere': 'SureAdhere', 'connect': 'Connect',
    'open-chat-studio': 'Open Chat Studio',
    'community-health': 'Community Health',
    'maternal-newborn-child-health': 'Maternal, Newborn & Child Health',
    'mental-health': 'Mental Health', 'infectious-disease': 'Infectious Disease',
    'nutrition': 'Nutrition', 'child-health': 'Child Health', 'livelihoods': 'Livelihoods',
    'humanitarian-response': 'Humanitarian Response',
    'monitoring-evaluation': 'Monitoring & Evaluation',
    'cash-voucher-assistance': 'Cash & Voucher Assistance',
    'service-delivery': 'Service Delivery', 'workforce-management': 'Workforce Management',
    'sponsorship': 'Sponsorship',
    'governments': 'Governments', 'international-ngos': 'International NGOs',
    'research-academic': 'Research & Academic', 'us-community-health': 'United States',
    'ai': 'AI', 'global-development': 'Global Development',
    'leadership': 'Leadership', 'company-culture': 'Company & Culture',
}

# episode number -> {p: products, sec: sectors, uc: use cases, org: org types, th: themes, staff: bool}
TAGS = {
 2:  {'staff': 1, 'th': ['company-culture']},
 3:  {'p': ['commcare'], 'staff': 1, 'th': ['company-culture']},
 4:  {'p': ['commcare'], 'staff': 1, 'th': ['company-culture']},
 5:  {'p': ['commcare'], 'staff': 1, 'th': ['global-development']},
 6:  {'p': ['commcare'], 'staff': 1, 'org': ['international-ngos'], 'uc': ['service-delivery']},
 7:  {'p': ['commcare'], 'staff': 1, 'org': ['governments']},
 8:  {'staff': 1, 'sec': ['community-health']},
 9:  {'staff': 1, 'th': ['global-development']},
 10: {'p': ['commcare'], 'staff': 1, 'th': ['company-culture']},
 11: {'p': ['commcare'], 'th': ['global-development']},
 12: {'p': ['commcare'], 'staff': 1, 'th': ['global-development']},
 13: {'staff': 1, 'org': ['governments'], 'th': ['global-development']},
 14: {'p': ['commcare'], 'staff': 1, 'sec': ['nutrition'], 'uc': ['workforce-management'], 'org': ['governments']},
 15: {'p': ['commcare'], 'staff': 1, 'sec': ['infectious-disease'], 'uc': ['service-delivery'], 'org': ['us-community-health']},
 16: {'staff': 1, 'th': ['company-culture']},
 17: {'th': ['global-development']},
 18: {'staff': 1, 'th': ['company-culture']},
 19: {'staff': 1, 'th': ['company-culture']},
 20: {'p': ['commcare'], 'org': ['governments']},
 21: {'staff': 1, 'th': ['company-culture']},
 22: {'org': ['governments']},
 23: {'th': ['ai', 'global-development']},
 24: {'staff': 1, 'th': ['global-development']},
 25: {'p': ['commcare'], 'sec': ['humanitarian-response'], 'uc': ['monitoring-evaluation'], 'org': ['international-ngos']},
 26: {'p': ['commcare'], 'sec': ['maternal-newborn-child-health'], 'uc': ['service-delivery']},
 27: {'staff': 1, 'th': ['ai']},
 28: {'staff': 1, 'sec': ['mental-health']},
 29: {'staff': 1, 'sec': ['community-health']},
 30: {'th': ['leadership']},
 31: {'staff': 1, 'th': ['company-culture']},
 32: {'staff': 1, 'th': ['company-culture']},
 33: {'p': ['commcare'], 'sec': ['infectious-disease'], 'org': ['international-ngos']},
 34: {'p': ['commcare'], 'sec': ['community-health', 'maternal-newborn-child-health']},
 35: {'p': ['commcare'], 'sec': ['community-health']},
 36: {'th': ['global-development']},
 37: {'p': ['open-chat-studio'], 'staff': 1, 'th': ['ai']},
 38: {'p': ['commcare'], 'staff': 1, 'sec': ['mental-health']},
 39: {'p': ['commcare'], 'sec': ['community-health']},
 40: {'p': ['commcare'], 'staff': 1, 'sec': ['community-health'], 'th': ['company-culture']},
 41: {'sec': ['mental-health'], 'org': ['research-academic']},
 42: {'p': ['sureadhere'], 'staff': 1, 'sec': ['infectious-disease'], 'org': ['research-academic'], 'th': ['company-culture']},
 43: {'p': ['sureadhere'], 'sec': ['infectious-disease']},
 44: {'staff': 1, 'sec': ['mental-health']},
 45: {'staff': 1, 'th': ['global-development']},
 46: {'sec': ['community-health']},
 47: {'p': ['commcare'], 'sec': ['community-health'], 'org': ['governments']},
 48: {'p': ['commcare'], 'sec': ['mental-health']},
 49: {'staff': 1, 'th': ['global-development']},
 50: {'p': ['commcare'], 'sec': ['community-health'], 'org': ['us-community-health']},
 51: {'p': ['sureadhere'], 'staff': 1, 'sec': ['infectious-disease']},
 52: {'th': ['leadership']},
 53: {'staff': 1, 'th': ['ai']},
 54: {'org': ['governments', 'us-community-health'], 'th': ['ai']},
 55: {'p': ['commcare'], 'sec': ['mental-health']},
 57: {'p': ['commcare'], 'sec': ['child-health']},
 59: {'p': ['open-chat-studio'], 'staff': 1, 'th': ['ai']},
 62: {'p': ['connect'], 'sec': ['community-health'], 'th': ['global-development']},
 63: {'p': ['connect'], 'staff': 1, 'sec': ['community-health']},
 64: {'p': ['commcare'], 'uc': ['monitoring-evaluation'], 'org': ['international-ngos']},
 65: {'p': ['commcare'], 'org': ['international-ngos'], 'th': ['global-development']},
 66: {'p': ['commcare', 'sureadhere'], 'staff': 1, 'th': ['company-culture']},
 67: {'staff': 1, 'th': ['global-development']},
 68: {'staff': 1, 'th': ['company-culture']},
 69: {'p': ['commcare'], 'uc': ['cash-voucher-assistance'], 'th': ['global-development']},
 70: {'p': ['commcare'], 'sec': ['livelihoods'], 'th': ['global-development']},
 71: {'th': ['global-development']},
 72: {'th': ['leadership']},
 73: {'th': ['global-development']},
 74: {'th': ['leadership']},
 75: {'p': ['commcare'], 'staff': 1, 'th': ['global-development']},
 76: {'th': ['global-development']},
 77: {'staff': 1, 'th': ['ai']},
 78: {'th': ['global-development']},
 80: {'org': ['research-academic'], 'th': ['ai']},
 81: {'uc': ['sponsorship'], 'th': ['global-development']},
 82: {'p': ['commcare'], 'sec': ['mental-health']},
 83: {'sec': ['community-health'], 'th': ['ai']},
}

# Filter rows: (dimension/query-param, TAGS key, label, preferred display order)
ROWS = [
 ('product', 'p',   'Product',  ['commcare', 'connect', 'sureadhere', 'open-chat-studio']),
 ('sector',  'sec', 'Sector',   ['community-health', 'mental-health', 'infectious-disease',
                                  'maternal-newborn-child-health', 'nutrition', 'child-health',
                                  'livelihoods', 'humanitarian-response']),
 ('usecase', 'uc',  'Use Case', ['monitoring-evaluation', 'service-delivery',
                                  'cash-voucher-assistance', 'workforce-management', 'sponsorship']),
 ('orgtype', 'org', 'Org Type', ['governments', 'international-ngos', 'us-community-health',
                                  'research-academic']),
 ('theme',   'th',  'Theme',    ['ai', 'global-development', 'company-culture', 'leadership']),
]
# dimension -> chip css variant on the episode hero
_CHIP_VARIANT = {'product': 'product', 'sector': 'solution', 'usecase': 'solution',
                 'orgtype': 'solution', 'theme': 'theme'}
# card data-dim -> TAGS key (used to test which tag values are actually present)
_TAGKEY = {'product': 'p', 'sector': 'sec', 'usecase': 'uc', 'orgtype': 'org', 'theme': 'th'}


def _present(key):
    out = set()
    for t in TAGS.values():
        out.update(t.get(key, []))
    return out


# ---------------------------------------------------------------- episode hero
def chip_row(num):
    """The <ul class="ep-tags"> chip row for an episode hero (or '' if untagged)."""
    t = TAGS.get(num, {})
    items = []
    for dim, key, _, _order in ROWS:
        for slug in t.get(key, []):
            items.append(
                '          <li><a class="ep-tag ep-tag--%s" href="../index.html?%s=%s">%s</a></li>'
                % (_CHIP_VARIANT[dim], dim, slug, LABEL[slug]))
    if not items:
        return ''
    return ('\n\n        <ul class="ep-tags" aria-label="Topics">\n'
            + '\n'.join(items) + '\n        </ul>')


CHIP_CSS = """
/* ---- Topic tags ---- */
.ep-tags {
  list-style: none; display: flex; flex-wrap: wrap; gap: 8px;
  margin: 22px 0 0; padding: 0; position: relative; z-index: 1;
}
.ep-tag {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 6px 14px; border-radius: 999px;
  font-family: var(--sans); font-size: 12px; font-weight: 500;
  letter-spacing: 0.02em; line-height: 1;
  color: rgba(255,255,255,0.82);
  border: 1px solid rgba(255,255,255,0.20);
  background: rgba(255,255,255,0.05);
  transition: background 150ms, border-color 150ms, color 150ms;
}
.ep-tag:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.42); color: #fff; }
.ep-tag::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%;
  background: currentColor; opacity: 0.65; flex-shrink: 0;
}
.ep-tag--product {
  color: #6fe3d6; border-color: rgba(13,168,157,0.55); background: rgba(13,168,157,0.12);
}
.ep-tag--product:hover { background: rgba(13,168,157,0.22); border-color: rgba(13,168,157,0.8); color: #aef3ea; }
.ep-tag--theme { color: rgba(255,255,255,0.66); background: transparent; }
"""


def with_chip_css(style_block):
    """Return the page <style>...</style> block with exactly one copy of CHIP_CSS.

    Idempotent: strips any previously-injected copy, then re-inserts the canonical one
    right after the `.ep-meta .dot` rule so it lives with the hero styles.
    """
    import re
    # Strip a prior copy: from its header up to the next section comment or </style>.
    block = re.sub(r'\n/\* ---- Topic tags ---- \*/.*?(?=\n/\* ----|</style>)', '',
                   style_block, flags=re.S)
    anchor = '.ep-meta .dot { width: 3px; height: 3px; border-radius: 50%; background: rgba(254,175,49,0.6); }'
    if anchor in block:
        block = block.replace(anchor, anchor + '\n' + CHIP_CSS, 1)
    else:
        block = block.replace('</style>', CHIP_CSS + '</style>', 1)
    return block


# ---------------------------------------------------------------- listing card
def card_attrs(num):
    """The data-* attribute string for a listing <article class="episode-card">."""
    t = TAGS.get(num, {})
    j = lambda key: ' '.join(t.get(key, []))
    return (' data-product="%s" data-sector="%s" data-usecase="%s" data-orgtype="%s"'
            ' data-theme="%s" data-staff="%s"'
            % (j('p'), j('sec'), j('uc'), j('org'), j('th'), 'yes' if t.get('staff') else 'no'))


# ---------------------------------------------------------------- listing filter
# Blog-style filter bar: a search box + two dropdowns (Platform, Focus). Each option carries
# the card data-attribute it filters (data-dim), so one dropdown can span several card
# attributes. A value is either a slug (uses the group's default data-dim) or an explicit
# (data-dim, slug) pair when it filters a different attribute than the rest of its group.
# "Dimagi Staff" / Voices and the old standalone "Theme" dropdown are intentionally dropped:
# themes now live as a sub-category under Focus, limited to six options.
# Each group: (heading or None, default card data-dim, [values in display order]).
DROPDOWNS = [
 ('product', 'Platform', 'All platforms', [
    (None, 'product', ['commcare', 'connect', 'sureadhere', 'open-chat-studio']),
 ]),
 ('focus', 'Focus', 'All focus areas', [
    ('Sectors',   'sector',  ['community-health', 'mental-health', 'infectious-disease',
                              'maternal-newborn-child-health', 'nutrition', 'child-health',
                              'livelihoods', 'humanitarian-response']),
    ('Use cases', 'usecase', ['monitoring-evaluation', 'service-delivery',
                              'cash-voucher-assistance', 'workforce-management', 'sponsorship']),
    # Themes folded in from the old Theme dropdown, limited to six. AI / Global Development /
    # Company & Culture / Leadership are data-theme; Governments and United States are
    # data-orgtype, so they carry an explicit (dim, slug).
    ('Themes',    'theme',   ['ai', 'global-development', 'company-culture', 'leadership',
                              ('orgtype', 'governments'), ('orgtype', 'us-community-health')]),
 ]),
]

_SEARCH_ICON = ('<svg class="pod-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
                ' stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                '<circle cx="11" cy="11" r="7"></circle>'
                '<line x1="20" y1="20" x2="16.65" y2="16.65"></line></svg>')


def filter_bar_html():
    out = ['        <div class="pod-filters" role="group" aria-label="Filter and search episodes">']
    # search box
    out.append('          <div class="pod-search">')
    out.append('            ' + _SEARCH_ICON)
    out.append('            <input type="search" id="pod-search" class="pod-search-input" '
               'placeholder="Search episodes" aria-label="Search episodes" autocomplete="off">')
    out.append('          </div>')
    # dropdowns
    for key, label, all_label, groups in DROPDOWNS:
        # normalize every value to (data-dim, slug); drop values not present on any card.
        norm = []
        for heading, gdim, vals in groups:
            kept = []
            for v in vals:
                vdim, slug = v if isinstance(v, tuple) else (gdim, v)
                if slug in _present(_TAGKEY[vdim]):
                    kept.append((vdim, slug))
            if kept:
                norm.append((heading, kept))
        if not norm:
            continue
        out.append('          <div class="pod-dd" data-dd="%s">' % key)
        out.append('            <button type="button" class="pod-dd-trigger" aria-haspopup="listbox" aria-expanded="false">'
                   '<span class="pod-dd-label">%s</span><span class="pod-dd-value">All</span>'
                   '<span class="pod-dd-chevron" aria-hidden="true"></span></button>' % label)
        out.append('            <div class="pod-dd-menu" role="listbox" aria-label="%s" hidden>' % label)
        out.append('              <button type="button" class="pod-dd-option is-active" role="option" '
                   'data-dim="%s" data-value="all" aria-selected="true">%s</button>' % (norm[0][1][0][0], all_label))
        for i, (heading, kept) in enumerate(norm):
            if i > 0:
                out.append('              <div class="pod-dd-sep" role="separator"></div>')
            if heading:
                out.append('              <div class="pod-dd-group">%s</div>' % heading)
            for vdim, slug in kept:
                out.append('              <button type="button" class="pod-dd-option" role="option" '
                           'data-dim="%s" data-value="%s">%s</button>' % (vdim, slug, LABEL[slug]))
        out.append('            </div>')
        out.append('          </div>')
    out.append('          <button type="button" class="pod-clear" id="pod-clear" hidden>Clear all</button>')
    out.append('        </div>')
    out.append('        <p class="pod-empty" id="pod-empty" hidden>No episodes match your filters. '
               '<button type="button" id="pod-clear-empty">Clear filters</button></p>')
    return '\n'.join(out)


FILTER_CSS = """
/* ── Episode filters ── */
/* Blog-style filter bar: search box + Product / Focus / Theme dropdowns. */
.pod-filters { display:flex; flex-flow:row wrap; align-items:center; gap:12px; margin:8px 0 30px; }
.pod-filters[hidden] { display:none; }
.pod-search { position:relative; flex:1 1 230px; min-width:200px; max-width:320px; }
.pod-search-icon { position:absolute; left:16px; top:50%; transform:translateY(-50%); width:16px; height:16px; color:var(--muted-soft); pointer-events:none; }
.pod-search-input { width:100%; font-family:var(--sans); font-size:14px; color:var(--ink); padding:11px 16px 11px 42px; border:1px solid var(--line); border-radius:999px; background:#fff; transition:border-color 150ms, box-shadow 150ms; }
.pod-search-input::placeholder { color:var(--muted-soft); }
.pod-search-input:focus { outline:none; border-color:#9A2C23; box-shadow:0 0 0 3px rgba(154,44,35,0.14); }
.pod-dd { position:relative; }
.pod-dd-trigger { display:inline-flex; align-items:center; gap:8px; font-family:var(--sans); font-size:13px; font-weight:500; padding:10px 15px; border-radius:999px; border:1px solid var(--line); background:#fff; color:var(--ink); cursor:pointer; transition:border-color 150ms, background 150ms; }
.pod-dd-trigger:hover { border-color:var(--rule); }
.pod-dd-label { font-size:11px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-soft); }
.pod-dd-value { color:var(--ink); }
.pod-dd-chevron { width:7px; height:7px; border-right:1.5px solid var(--muted); border-bottom:1.5px solid var(--muted); transform:rotate(45deg) translateY(-2px); margin-left:1px; transition:transform 150ms; }
.pod-dd.is-open .pod-dd-trigger { border-color:#9A2C23; }
.pod-dd.is-open .pod-dd-chevron { transform:rotate(-135deg) translateY(1px); }
.pod-dd.is-set .pod-dd-trigger { border-color:#9A2C23; background:rgba(154,44,35,0.06); }
.pod-dd.is-set .pod-dd-label { color:#9A2C23; }
.pod-dd-menu { position:absolute; top:calc(100% + 8px); left:0; z-index:40; min-width:236px; max-height:360px; overflow-y:auto; padding:6px; background:#fff; border:1px solid var(--line); border-radius:14px; box-shadow:0 14px 36px rgba(20,22,55,0.16); }
.pod-dd-menu[hidden] { display:none; }
.pod-dd-group { font-family:var(--sans); font-size:10px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted-soft); padding:10px 12px 4px; }
.pod-dd-option { display:flex; align-items:center; justify-content:space-between; gap:10px; width:100%; text-align:left; font-family:var(--sans); font-size:13.5px; color:var(--ink); padding:9px 12px; border:0; border-radius:9px; background:none; cursor:pointer; }
.pod-dd-option:hover { background:rgba(154,44,35,0.06); }
.pod-dd-option.is-active { color:#9A2C23; font-weight:600; }
.pod-dd-option.is-active::after { content:"\\2713"; font-size:12px; }
.pod-dd-sep { height:1px; background:var(--line); margin:6px 8px; }
.pod-clear { font-family:var(--sans); font-size:13px; font-weight:600; color:#9A2C23; background:none; border:0; cursor:pointer; padding:8px 6px; margin-left:2px; }
.pod-clear[hidden] { display:none; }
.pod-clear:hover { text-decoration:underline; }
.pod-empty { font-size:15px; color:var(--muted); margin:8px 0 28px; }
.pod-empty button {
  font:inherit; color:#9A2C23; background:none; border:none; padding:0;
  text-decoration:underline; cursor:pointer;
}
.episode-card.filtered-out { display:none !important; }
/* While a filter/search is active, the controller relocates every "more" episode into the
   single archive grid, so all matches render in one continuous 3-col grid (no ragged seam
   where the top grid's half-empty last row met a fresh second grid). The compact "more"
   list section then has nothing left to show, so it collapses away entirely. */
body.pod-filtering .more-section { display:none; }
@media (max-width:760px){ .pod-search { flex-basis:100%; max-width:none; order:-1; } .pod-dd-menu { min-width:200px; } }
"""


COMBINED_JS = """<script>
/* Episode archive: lazy-reveal by default; when search or any dropdown filter is active,
   show all matches across both grids (AND across dropdowns; membership within a
   multi-valued card). Blog-style search + Product / Focus / Theme dropdowns. */
(function(){
  var BATCH = 9;
  var moreGrid = document.getElementById('more-grid');
  var moreBtn  = document.getElementById('more-episodes-btn');
  var allCards = Array.prototype.slice.call(document.querySelectorAll('.episode-card'));
  var moreCards= moreGrid ? Array.prototype.slice.call(moreGrid.querySelectorAll('.episode-card')) : [];
  var archiveGrid = document.querySelector('.archive-section .episodes-grid');

  // While filtering, pull every "more" episode up into the single archive grid so all
  // matches flow as one continuous 3-col grid; on clear, return them to #more-grid for
  // the default lazy-reveal list. Re-appending in array order preserves chronology.
  function mergeGrids(){ if(archiveGrid) moreCards.forEach(function(c){ archiveGrid.appendChild(c); }); }
  function splitGrids(){ if(moreGrid) moreCards.forEach(function(c){ moreGrid.appendChild(c); }); }
  var dds      = Array.prototype.slice.call(document.querySelectorAll('.pod-dd'));
  var emptyEl  = document.getElementById('pod-empty');
  var clearEl  = document.getElementById('pod-clear');
  var emptyClearEl = document.getElementById('pod-clear-empty');
  var searchEl = document.getElementById('pod-search');

  // Each dropdown holds one active {dim,value}; value 'all' means inactive. The option's
  // data-dim says which card attribute it filters (Focus mixes sector+usecase, Theme mixes
  // theme+orgtype), so one dropdown can span several card attributes.
  var active = {};
  dds.forEach(function(dd){ active[dd.getAttribute('data-dd')] = {dim:null, value:'all'}; });
  var query = '';

  function anyFilter(){
    if(query) return true;
    for(var k in active){ if(active[k].value!=='all') return true; }
    return false;
  }
  function cardText(card){
    var t=card.querySelector('.episode-title'), n=card.querySelector('.episode-num'),
        d=card.querySelector('.episode-card-body p');
    return ((t?t.textContent:'')+' '+(n?n.textContent:'')+' '+(d?d.textContent:'')).toLowerCase();
  }
  function matches(card){
    if(query && cardText(card).indexOf(query)===-1) return false;
    for(var k in active){
      var a=active[k];
      if(a.value==='all') continue;
      if((card.dataset[a.dim]||'').split(' ').indexOf(a.value)===-1) return false;
    }
    return true;
  }

  var shown=0, auto=false, scheduled=false, sentinel=null;
  function resetReveal(){
    shown=0;
    moreCards.forEach(function(c){ c.classList.add('is-hidden'); c.classList.remove('is-revealing'); });
    if(moreBtn) moreBtn.style.display = moreCards.length ? '' : 'none';
  }
  function revealNext(){
    moreCards.slice(shown, shown+BATCH).forEach(function(c){ c.classList.remove('is-hidden'); c.classList.add('is-revealing'); });
    shown=Math.min(shown+BATCH, moreCards.length);
    return shown>=moreCards.length;
  }
  function check(){
    if(!auto||!sentinel) return;
    var vh=window.innerHeight||document.documentElement.clientHeight, guard=0;
    while(shown<moreCards.length && sentinel.getBoundingClientRect().top - vh < 600 && guard++<30){
      if(revealNext()){ stopAuto(); return; }
    }
  }
  function onScroll(){ if(scheduled) return; scheduled=true; setTimeout(function(){ scheduled=false; check(); },90); }
  function startAuto(){ auto=true; window.addEventListener('scroll',onScroll,{passive:true}); window.addEventListener('resize',onScroll); }
  function stopAuto(){ auto=false; window.removeEventListener('scroll',onScroll); window.removeEventListener('resize',onScroll); }

  function apply(){
    if(anyFilter()){
      stopAuto();
      document.body.classList.add('pod-filtering');
      mergeGrids();
      if(moreBtn) moreBtn.style.display='none';
      var any=false;
      allCards.forEach(function(c){
        var m=matches(c);
        c.classList.toggle('filtered-out', !m);
        c.classList.remove('is-hidden');
        if(m) any=true;
      });
      if(emptyEl) emptyEl.hidden = any;
    } else {
      document.body.classList.remove('pod-filtering');
      allCards.forEach(function(c){ c.classList.remove('filtered-out'); });
      if(emptyEl) emptyEl.hidden = true;
      splitGrids();
      resetReveal();
    }
    if(clearEl) clearEl.hidden = !anyFilter();
    syncUrl();
  }

  // ---- dropdowns ----
  function closeAll(except){
    dds.forEach(function(dd){
      if(dd===except) return;
      dd.classList.remove('is-open');
      var m=dd.querySelector('.pod-dd-menu'); if(m) m.hidden=true;
      var tr=dd.querySelector('.pod-dd-trigger'); if(tr) tr.setAttribute('aria-expanded','false');
    });
  }
  dds.forEach(function(dd){
    var key=dd.getAttribute('data-dd');
    var trigger=dd.querySelector('.pod-dd-trigger');
    var menu=dd.querySelector('.pod-dd-menu');
    var valueEl=dd.querySelector('.pod-dd-value');
    var options=Array.prototype.slice.call(dd.querySelectorAll('.pod-dd-option'));
    trigger.addEventListener('click', function(e){
      e.stopPropagation();
      var open=!dd.classList.contains('is-open');
      closeAll(dd);
      dd.classList.toggle('is-open', open);
      menu.hidden=!open;
      trigger.setAttribute('aria-expanded', open?'true':'false');
    });
    options.forEach(function(opt){
      opt.addEventListener('click', function(){
        var val=opt.getAttribute('data-value'), dim=opt.getAttribute('data-dim');
        active[key]={dim:dim, value:val};
        options.forEach(function(o){
          var on=o===opt;
          o.classList.toggle('is-active', on);
          o.setAttribute('aria-selected', on?'true':'false');
        });
        valueEl.textContent = val==='all' ? 'All' : opt.textContent;
        dd.classList.toggle('is-set', val!=='all');
        closeAll(null);
        shown=0; apply();
      });
    });
  });
  document.addEventListener('click', function(){ closeAll(null); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeAll(null); });

  // ---- search ----
  if(searchEl){
    var deb;
    searchEl.addEventListener('input', function(){
      clearTimeout(deb);
      deb=setTimeout(function(){ query=searchEl.value.trim().toLowerCase(); apply(); }, 120);
    });
  }

  // ---- clear ----
  function resetDd(dd){
    var opts=Array.prototype.slice.call(dd.querySelectorAll('.pod-dd-option'));
    opts.forEach(function(o,i){ var on=i===0; o.classList.toggle('is-active', on); o.setAttribute('aria-selected', on?'true':'false'); });
    dd.classList.remove('is-set');
    var v=dd.querySelector('.pod-dd-value'); if(v) v.textContent='All';
    active[dd.getAttribute('data-dd')]={dim:null, value:'all'};
  }
  function clearAll(){
    dds.forEach(resetDd);
    query=''; if(searchEl) searchEl.value='';
    apply();
  }
  if(clearEl) clearEl.addEventListener('click', clearAll);
  if(emptyClearEl) emptyClearEl.addEventListener('click', clearAll);

  // ---- URL sync (deep-linkable; episode hero chips link with ?<dim>=<slug>) ----
  function syncUrl(){
    try {
      var p=new URLSearchParams();
      for(var k in active){ var a=active[k]; if(a.value!=='all' && a.dim) p.set(a.dim, a.value); }
      if(query) p.set('q', searchEl ? searchEl.value.trim() : query);
      var qs=p.toString();
      history.replaceState(null,'', qs ? ('?'+qs) : window.location.pathname);
    } catch(e){ /* file:// — replaceState may throw; ignore */ }
  }

  if(moreGrid){
    sentinel=document.createElement('div'); sentinel.setAttribute('aria-hidden','true');
    sentinel.style.cssText='height:1px;width:100%;';
    moreGrid.parentNode.insertBefore(sentinel, moreGrid.nextSibling);
  }
  resetReveal();
  if(moreBtn){
    moreBtn.addEventListener('click', function(){
      if(anyFilter()) return;
      var done=revealNext(); moreBtn.style.display='none'; if(!done) startAuto();
    });
  }

  // restore state from the URL: ?product / ?sector / ?usecase / ?theme / ?orgtype / ?q
  var params=new URLSearchParams(window.location.search);
  var q=params.get('q');
  if(q && searchEl){ searchEl.value=q; query=q.trim().toLowerCase(); }
  dds.forEach(function(dd){
    var options=Array.prototype.slice.call(dd.querySelectorAll('.pod-dd-option'));
    for(var i=0;i<options.length;i++){
      var dim=options[i].getAttribute('data-dim'), val=options[i].getAttribute('data-value');
      if(val==='all') continue;
      var raw=params.get(dim);
      if(raw && raw.toLowerCase()===val.toLowerCase()){ options[i].click(); break; }
    }
  });

  apply();
})();
</script>"""
