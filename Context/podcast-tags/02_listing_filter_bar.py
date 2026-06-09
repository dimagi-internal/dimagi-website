#!/usr/bin/env python3
import re, os
ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login/podcast"
listing_path = os.path.join(ROOT, 'index.html')
L = open(listing_path, encoding='utf-8').read()

LABEL = {
 'commcare':'CommCare','sureadhere':'SureAdhere','connect':'Connect','open-chat-studio':'Open Chat Studio',
 'community-health':'Community Health','maternal-newborn-child-health':'Maternal, Newborn & Child Health',
 'mental-health':'Mental Health','infectious-disease':'Infectious Disease','nutrition':'Nutrition',
 'child-health':'Child Health','livelihoods':'Livelihoods','humanitarian-response':'Humanitarian Response',
 'monitoring-evaluation':'Monitoring & Evaluation','cash-voucher-assistance':'Cash & Voucher Assistance',
 'service-delivery':'Service Delivery','workforce-management':'Workforce Management','sponsorship':'Sponsorship',
 'governments':'Governments','international-ngos':'International NGOs','research-academic':'Research & Academic',
 'us-community-health':'US Community Health',
 'ai':'AI','global-development':'Global Development','leadership':'Leadership','company-culture':'Company & Culture',
}

# Which values actually occur, in a sensible display order per dimension.
ROWS = [
 ('product','Product', ['commcare','connect','sureadhere','open-chat-studio']),
 ('sector','Sector',  ['community-health','mental-health','infectious-disease','maternal-newborn-child-health','nutrition','child-health','livelihoods','humanitarian-response']),
 ('usecase','Use Case',['monitoring-evaluation','service-delivery','cash-voucher-assistance','workforce-management','sponsorship']),
 ('orgtype','Org Type',['governments','international-ngos','us-community-health','research-academic']),
 ('theme','Theme',    ['ai','global-development','company-culture','leadership']),
]

def used(dim):
    return set(re.findall(r'data-%s="([^"]*)"' % dim, L))
present_vals = {}
for dim,_,_ in ROWS:
    s=set()
    for blob in re.findall(r'data-%s="([^"]*)"' % dim, L):
        for v in blob.split():
            if v: s.add(v)
    present_vals[dim]=s

def build_rows():
    out=['        <div class="pod-filters" role="group" aria-label="Filter episodes">']
    for dim,label,order in ROWS:
        vals=[v for v in order if v in present_vals[dim]]
        if not vals: continue
        out.append('          <div class="pod-filter-row">')
        out.append('            <span class="pod-filter-label">%s</span>' % label)
        out.append('            <div class="pod-filter-chips">')
        out.append('              <button type="button" class="pod-filter is-active" data-dim="%s" data-filter="all" aria-pressed="true">All</button>' % dim)
        for v in vals:
            out.append('              <button type="button" class="pod-filter" data-dim="%s" data-filter="%s" aria-pressed="false">%s</button>' % (dim, v, LABEL[v]))
        out.append('            </div>')
        out.append('          </div>')
    # Dimagi staff toggle
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

FILTER_HTML = build_rows()

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
/* While filtering, the revealed list collapses into the same 3-col grid */
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

changed=False
# 1) Filter CSS into the inline <style> (once)
if '/* ── Episode filters ── */' not in L:
    L = L.replace('<style>\n/* ── Podcast page ── */', '<style>\n/* ── Podcast page ── */\n' + FILTER_CSS, 1)
    changed=True

# 2) Filter bar + empty state before the first grid (once)
if 'class="pod-filters"' not in L:
    L = L.replace('      <div class="episodes-grid">',
                  FILTER_HTML + '\n\n      <div class="episodes-grid">', 1)
    changed=True

# 3) Replace the reveal <script> with the combined controller (once)
if 'pod-filtering' not in L.split('</style>')[-1] or 'function setActive' not in L:
    L2 = re.sub(r'<script>\s*\n/\* "Load More Episodes".*?</script>', COMBINED_JS, L, count=1, flags=re.S)
    if L2 != L:
        L = L2; changed=True
    else:
        print("  !! reveal script not found for replacement")

open(listing_path,'w',encoding='utf-8').write(L)
print("Listing updated:", changed)
print("present values:")
for dim,_,_ in ROWS: print('  ', dim, sorted(present_vals[dim]))
