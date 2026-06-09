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
    'research-academic': 'Research & Academic', 'us-community-health': 'US Community Health',
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
def filter_bar_html():
    out = ['        <div class="pod-filters" role="group" aria-label="Filter episodes">']
    for dim, key, label, order in ROWS:
        vals = [v for v in order if v in _present(key)]
        if not vals:
            continue
        out.append('          <div class="pod-filter-row">')
        out.append('            <span class="pod-filter-label">%s</span>' % label)
        out.append('            <div class="pod-filter-chips">')
        out.append('              <button type="button" class="pod-filter is-active" data-dim="%s" data-filter="all" aria-pressed="true">All</button>' % dim)
        for v in vals:
            out.append('              <button type="button" class="pod-filter" data-dim="%s" data-filter="%s" aria-pressed="false">%s</button>' % (dim, v, LABEL[v]))
        out.append('            </div>')
        out.append('          </div>')
    out.append('          <div class="pod-filter-row">')
    out.append('            <span class="pod-filter-label">Voices</span>')
    out.append('            <div class="pod-filter-chips">')
    out.append('              <button type="button" class="pod-filter is-active" data-dim="staff" data-filter="all" aria-pressed="true">All</button>')
    out.append('              <button type="button" class="pod-filter" data-dim="staff" data-filter="yes" aria-pressed="false">Dimagi Staff</button>')
    out.append('            </div>')
    out.append('          </div>')
    out.append('        </div>')
    out.append('        <p class="pod-empty" id="pod-empty" hidden>No episodes match those filters. <button type="button" id="pod-clear">Clear filters</button></p>')
    return '\n'.join(out)


FILTER_CSS = """
/* ── Episode filters ── */
.pod-filters { display:flex; flex-direction:column; gap:12px; margin:8px 0 30px; }
.pod-filter-row { display:flex; align-items:baseline; gap:16px; flex-wrap:wrap; }
.pod-filter-label {
  font-family:var(--sans); font-size:11px; font-weight:600; letter-spacing:0.12em;
  text-transform:uppercase; color:var(--muted-soft); width:74px; flex-shrink:0;
}
.pod-filter-chips { display:flex; flex-wrap:wrap; gap:8px; }
.pod-filter {
  font-family:var(--sans); font-size:13px; font-weight:500; letter-spacing:0.01em;
  padding:7px 15px; border-radius:999px; border:1px solid var(--line);
  background:#fff; color:var(--muted); cursor:pointer;
  transition:background 150ms,color 150ms,border-color 150ms;
}
.pod-filter:hover { border-color:var(--rule); color:var(--ink); }
.pod-filter.is-active { background:#9A2C23; border-color:#9A2C23; color:#fff; }
.pod-empty { font-size:15px; color:var(--muted); margin:8px 0 28px; }
.pod-empty button {
  font:inherit; color:#9A2C23; background:none; border:none; padding:0;
  text-decoration:underline; cursor:pointer;
}
.episode-card.filtered-out { display:none !important; }
body.pod-filtering #more-grid { display:grid !important; grid-template-columns:repeat(3,1fr); gap:24px; }
body.pod-filtering .archive-section { padding-bottom:0; }
body.pod-filtering .more-section { padding-top:0; }
@media (max-width:760px){ body.pod-filtering #more-grid { grid-template-columns:1fr; } }
@media (max-width:600px){ .pod-filter-row { gap:6px; } .pod-filter-label { width:auto; } }
"""


COMBINED_JS = """<script>
/* Episode archive: lazy-reveal by default; when any filter is active, show all matches
   across both grids (AND across dimensions, membership within a multi-valued card). */
(function(){
  var BATCH = 9;
  var moreGrid = document.getElementById('more-grid');
  var moreBtn  = document.getElementById('more-episodes-btn');
  var allCards = Array.prototype.slice.call(document.querySelectorAll('.episode-card'));
  var moreCards= moreGrid ? Array.prototype.slice.call(moreGrid.querySelectorAll('.episode-card')) : [];
  var fbtns    = Array.prototype.slice.call(document.querySelectorAll('.pod-filter'));
  var emptyEl  = document.getElementById('pod-empty');
  var clearEl  = document.getElementById('pod-clear');
  var DIMS = ['product','sector','usecase','orgtype','theme','staff'];
  var active = {product:'all',sector:'all',usecase:'all',orgtype:'all',theme:'all',staff:'all'};

  function filtering(){ for(var i=0;i<DIMS.length;i++){ if(active[DIMS[i]]!=='all') return true; } return false; }
  function matches(card){
    return DIMS.every(function(d){
      if(active[d]==='all') return true;
      return (card.dataset[d]||'').split(' ').indexOf(active[d]) !== -1;
    });
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
    if(filtering()){
      stopAuto();
      document.body.classList.add('pod-filtering');
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
      resetReveal();
    }
  }
  function setActive(dim,val){
    active[dim]=val;
    fbtns.forEach(function(b){
      if(b.dataset.dim===dim){
        var on=b.dataset.filter===val;
        b.classList.toggle('is-active',on);
        b.setAttribute('aria-pressed', on?'true':'false');
      }
    });
    apply();
  }

  if(moreGrid){
    sentinel=document.createElement('div'); sentinel.setAttribute('aria-hidden','true');
    sentinel.style.cssText='height:1px;width:100%;';
    moreGrid.parentNode.insertBefore(sentinel, moreGrid.nextSibling);
  }
  resetReveal();

  if(moreBtn){
    moreBtn.addEventListener('click', function(){
      if(filtering()) return;
      var done=revealNext(); moreBtn.style.display='none'; if(!done) startAuto();
    });
  }
  fbtns.forEach(function(b){ b.addEventListener('click', function(){ setActive(b.dataset.dim, b.dataset.filter); }); });
  if(clearEl){ clearEl.addEventListener('click', function(){ DIMS.forEach(function(d){ setActive(d,'all'); }); }); }

  var qs=new URLSearchParams(window.location.search);
  DIMS.forEach(function(d){ var v=qs.get(d); if(v) setActive(d,v); });
})();
</script>"""
