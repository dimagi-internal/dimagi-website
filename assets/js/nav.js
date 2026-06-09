(function () {
  var nav = document.querySelector('nav.primary');
  if (!nav) return;

  /* Depth-aware base path — set via data-nav-base on <nav class="primary">.
     './'  for homepage, '../' for depth-1 pages, '../../' for depth-2 pages. */
  var navBase = (nav.dataset && nav.dataset.navBase) || './';

  function makeDropdown(triggerText, col, width) {
    var links = nav.querySelector('.nav-links');
    if (!links) return;

    var triggerLink = null;
    var anchors = links.querySelectorAll('a');
    for (var i = 0; i < anchors.length; i++) {
      if (anchors[i].textContent.trim() === triggerText) {
        triggerLink = anchors[i]; break;
      }
    }
    if (!triggerLink) return;

    var itemsHTML = col.items.map(function (item) {
      var extra = item.external ? ' target="_blank" rel="noopener"' : '';
      return '<a href="' + item.href + '"' + extra + '>' + item.label + '</a>';
    }).join('');

    var headingHTML = col.heading
      ? '<div class="nav-dropdown-heading">' + col.heading + '</div>'
      : '';

    var dropClass = width === 'sm' ? 'nav-dropdown nav-dropdown--sm' : 'nav-dropdown';

    var wrap = document.createElement('span');
    wrap.className = 'nav-dropdown-wrap';
    triggerLink.parentNode.insertBefore(wrap, triggerLink);
    wrap.appendChild(triggerLink);

    triggerLink.insertAdjacentHTML('beforeend',
      '<svg class="nav-chevron" width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden="true">'
      + '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
      + '</svg>');

    wrap.insertAdjacentHTML('beforeend',
      '<div class="' + dropClass + '">'
      + '<div class="nav-dropdown-inner" style="grid-template-columns:1fr;">'
      + '<div class="nav-dropdown-col">'
      + headingHTML + itemsHTML
      + '</div></div></div>');

    var closeTimer = null;
    function open()        { clearTimeout(closeTimer); wrap.classList.add('is-open'); }
    function close()       { wrap.classList.remove('is-open'); }
    function closeDelayed(){ closeTimer = setTimeout(close, 200); }

    wrap.addEventListener('mouseenter', function () { if (window.innerWidth > 980) open(); });
    wrap.addEventListener('mouseleave', function () { if (window.innerWidth > 980) closeDelayed(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.addEventListener('click',   function (e) { if (!wrap.contains(e.target)) close(); });
  }

  /* ── PRODUCTS ── */
  makeDropdown('Products', {
    heading: 'Our Products',
    items: [
      { label: 'Connect',          href: 'https://connect.dimagi.com/',        external: true },
      { label: 'CommCare',         href: 'https://dimagi.com/commcare/',      external: true },
      { label: 'SureAdhere',       href: 'https://dimagi.com/sureadhere/',     external: true },
      { label: 'Open Chat Studio', href: 'https://www.openchatstudio.com/',    external: true }
    ]
  }, 'sm');

  /* ── PROFESSIONAL SERVICES ── */
  makeDropdown('Professional Services', {
    items: [
      { label: 'Global Services',  href: navBase + 'professional-services/global-services/index.html' },
      { label: 'United States',    href: navBase + 'professional-services/united-states/index.html' },
      { label: 'Research & Data',  href: navBase + 'professional-services/research-data/index.html' }
    ]
  }, 'sm');

  /* ── COMPANY ── */
  makeDropdown('Company', {
    items: [
      { label: 'About Us',     href: navBase + 'company/about/index.html' },
      { label: 'Our Approach', href: navBase + 'company/our-approach/index.html' },
      { label: 'Blog',         href: navBase + 'blog/index.html' },
      { label: 'Podcast',      href: navBase + 'podcast/index.html' },
      { label: 'Careers',      href: navBase + 'company/careers/index.html' }
    ]
  }, 'sm');

  /* ── SIGN IN (CTA dropdown) ── */
  (function () {
    var cta = nav.querySelector('.nav-cta');
    if (!cta) return;
    var trigger = null;
    var anchors = cta.querySelectorAll('a');
    for (var i = 0; i < anchors.length; i++) {
      if (anchors[i].textContent.trim().indexOf('Sign In') === 0) { trigger = anchors[i]; break; }
    }
    if (!trigger) return;

    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');

    var items = [
      { label: 'Connect',          href: 'https://connect.dimagi.com/accounts/login/' },
      { label: 'CommCare',         href: 'https://www.commcarehq.org/accounts/login/' },
      { label: 'SureAdhere',       href: 'https://secure.sureadhere.com/' },
      { label: 'Open Chat Studio', href: 'https://chatbots.dimagi.com/accounts/login/' }
    ];
    var itemsHTML = items.map(function (it) {
      return '<a href="' + it.href + '" target="_blank" rel="noopener">' + it.label + '</a>';
    }).join('');

    var wrap = document.createElement('span');
    wrap.className = 'nav-dropdown-wrap nav-signin-wrap';
    trigger.parentNode.insertBefore(wrap, trigger);
    wrap.appendChild(trigger);

    trigger.insertAdjacentHTML('beforeend',
      '<svg class="nav-chevron" width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden="true">'
      + '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
      + '</svg>');

    wrap.insertAdjacentHTML('beforeend',
      '<div class="nav-dropdown nav-dropdown--sm nav-dropdown--right">'
      + '<div class="nav-dropdown-inner" style="grid-template-columns:1fr;">'
      + '<div class="nav-dropdown-col">'
      + '<div class="nav-dropdown-heading">Sign in to</div>'
      + itemsHTML
      + '</div></div></div>');

    var closeTimer = null;
    function open()        { clearTimeout(closeTimer); wrap.classList.add('is-open'); trigger.setAttribute('aria-expanded', 'true'); }
    function close()       { wrap.classList.remove('is-open'); trigger.setAttribute('aria-expanded', 'false'); }
    function closeDelayed(){ closeTimer = setTimeout(close, 200); }

    /* Desktop: hover opens, click toggles (and won't navigate away).
       Mobile (<=980): the dropdown is hidden, so the button falls back to the sign-in page. */
    wrap.addEventListener('mouseenter', function () { if (window.innerWidth > 980) open(); });
    wrap.addEventListener('mouseleave', function () { if (window.innerWidth > 980) closeDelayed(); });
    trigger.addEventListener('click', function (e) {
      if (window.innerWidth > 980) {
        e.preventDefault();
        if (wrap.classList.contains('is-open')) close(); else open();
      }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.addEventListener('click',   function (e) { if (!wrap.contains(e.target)) close(); });
  }());

  /* ── SITE SEARCH ── */
  (function () {
    var cta = nav.querySelector('.nav-cta');
    if (!cta) return;

    var INDEX = [
      { t:'Home', s:'Dimagi', u: navBase + 'index.html', k:'home overview frontline digital solutions' },
      { t:'CommCare', s:'Products', u:'https://dimagi.com/commcare/', x:1, k:'data collection app builder no-code platform case management frontline' },
      { t:'Connect', s:'Products', u:'https://connect.dimagi.com/', x:1, k:'verified service delivery marketplace workers payments' },
      { t:'SureAdhere', s:'Products', u:'https://dimagi.com/sureadhere/', x:1, k:'medication adherence tuberculosis tb video observed therapy' },
      { t:'Open Chat Studio', s:'Products', u:'https://www.openchatstudio.com/', x:1, k:'ai chatbot llm assistant' },
      { t:'Professional Services', s:'Services', u: navBase + 'professional-services/index.html', k:'implementation deploy scale services experts' },
      { t:'Global Services', s:'Services', u: navBase + 'professional-services/global-services/index.html', k:'africa asia echis community health national scale international ict4d' },
      { t:'Africa', s:'Services', u: navBase + 'professional-services/africa/index.html', k:'africa echis community health national scale benin ethiopia burkina faso madagascar mozambique south africa niger nigeria senegal ministry' },
      { t:'United States', s:'Services', u: navBase + 'professional-services/united-states/index.html', k:'us public health behavioral health government state' },
      { t:'India', s:'Services', u: navBase + 'professional-services/india/index.html', k:'india asia nutrition maternal health delhi' },
      { t:'Research & Data', s:'Services', u: navBase + 'professional-services/research-data/index.html', k:'research evidence publications studies data' },
      { t:'About Us', s:'Company', u: navBase + 'company/about/index.html', k:'about mission benefit corporation social enterprise team' },
      { t:'Our Approach', s:'Company', u: navBase + 'company/our-approach/index.html', k:'approach values how we work' },
      { t:'Careers', s:'Company', u: navBase + 'company/careers/index.html', k:'jobs hiring careers work openings' },
      { t:'Blog', s:'Company', u: navBase + 'blog/index.html', k:'blog articles posts' },
      { t:'Podcast', s:'Company', u: navBase + 'podcast/index.html', k:'podcast high impact growth episodes' },
      { t:'Press & Coverage', s:'Company', u: navBase + 'press/index.html', k:'press news media coverage' },
      { t:'Contact Us', s:'Get in touch', u: navBase + 'contact/index.html', k:'contact demo talk sales email' },
      { t:'Sign In', s:'Account', u: navBase + 'sign-in/index.html', k:'sign in login account' },
      { t:'Privacy Policy', s:'Legal', u: navBase + 'legal/privacy-policy/index.html', k:'privacy policy legal' },
      { t:'Terms of Service', s:'Legal', u: navBase + 'legal/terms-of-service/index.html', k:'terms of service legal' }
    ];

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nav-search-btn';
    btn.setAttribute('aria-label', 'Search the site');
    btn.innerHTML = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="6.25" stroke="currentColor" stroke-width="1.6"/><path d="M13.8 13.8L18 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';
    cta.appendChild(btn); /* to the right of Sign In */

    var ov = document.createElement('div');
    ov.className = 'search-overlay';
    ov.innerHTML =
      '<div class="search-panel" role="dialog" aria-modal="true" aria-label="Site search">'
      + '<div class="search-input-wrap">'
      +   '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="6.25" stroke="currentColor" stroke-width="1.6"/><path d="M13.8 13.8L18 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
      +   '<input type="text" class="search-input" placeholder="Search Dimagi…" aria-label="Search the site" autocomplete="off">'
      +   '<span class="search-esc">ESC</span>'
      + '</div>'
      + '<div class="search-results" role="listbox"></div>'
      + '</div>';
    document.body.appendChild(ov);

    var input = ov.querySelector('.search-input');
    var results = ov.querySelector('.search-results');
    var activeIdx = -1;

    function render(list) {
      if (!list.length) {
        results.innerHTML = '<div class="search-empty">' + (input.value.trim() ? 'No results found' : 'Type to search the site') + '</div>';
        activeIdx = -1; return;
      }
      activeIdx = 0;
      results.innerHTML = list.map(function (r, i) {
        var ext = r.x ? ' target="_blank" rel="noopener"' : '';
        return '<a class="search-result' + (i === 0 ? ' is-active' : '') + '" href="' + r.u + '"' + ext + ' role="option">'
          + '<span class="search-result-section">' + r.s + '</span>'
          + '<span class="search-result-title">' + r.t + '</span></a>';
      }).join('');
    }

    function doSearch(q) {
      q = q.trim().toLowerCase();
      if (!q) return [];
      var toks = q.split(/\s+/);
      var scored = [];
      for (var n = 0; n < INDEX.length; n++) {
        var item = INDEX[n];
        var title = item.t.toLowerCase();
        var hay = (item.t + ' ' + item.s + ' ' + (item.k || '')).toLowerCase();
        var ok = true, score = 0;
        for (var i = 0; i < toks.length; i++) {
          if (hay.indexOf(toks[i]) === -1) { ok = false; break; }
          if (title.indexOf(toks[i]) === 0) score += 3;
          else if (title.indexOf(toks[i]) !== -1) score += 2;
          else score += 1;
        }
        if (ok) scored.push({ item: item, score: score });
      }
      scored.sort(function (a, b) { return b.score - a.score; });
      return scored.slice(0, 8).map(function (s) { return s.item; });
    }

    function setActive(i) {
      var nodes = results.querySelectorAll('.search-result');
      if (!nodes.length) return;
      activeIdx = (i + nodes.length) % nodes.length;
      for (var j = 0; j < nodes.length; j++) nodes[j].classList.toggle('is-active', j === activeIdx);
      nodes[activeIdx].scrollIntoView({ block: 'nearest' });
    }

    function open()  { ov.classList.add('is-open'); document.body.style.overflow = 'hidden'; input.value = ''; render([]); setTimeout(function () { input.focus(); }, 30); }
    function close() { ov.classList.remove('is-open'); document.body.style.overflow = ''; }

    btn.addEventListener('click', open);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    input.addEventListener('input', function () { render(doSearch(input.value)); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(activeIdx + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(activeIdx - 1); }
      else if (e.key === 'Enter') {
        var a = results.querySelectorAll('.search-result')[activeIdx];
        if (a) { if (a.target === '_blank') window.open(a.href, '_blank', 'noopener'); else window.location.href = a.href; }
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ov.classList.contains('is-open')) { close(); btn.focus(); }
      else if (e.key === '/' && !ov.classList.contains('is-open')) {
        var ae = document.activeElement, tag = ae ? ae.tagName : '';
        if (tag !== 'INPUT' && tag !== 'TEXTAREA') { e.preventDefault(); open(); }
      }
    });
  }());

  /* ── MOBILE HAMBURGER ── */
  var links = nav.querySelector('.nav-links');
  if (!links) return;

  var btn = document.createElement('button');
  btn.className = 'nav-hamburger';
  btn.setAttribute('aria-label', 'Toggle navigation');
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = '<span></span><span></span><span></span>';
  nav.appendChild(btn);

  function closeMobile() {
    links.classList.remove('is-open');
    btn.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
  }

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    var isOpen = links.classList.toggle('is-open');
    btn.classList.toggle('is-open', isOpen);
    btn.setAttribute('aria-expanded', String(isOpen));
  });

  document.addEventListener('click',   function (e) { if (!nav.contains(e.target)) closeMobile(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMobile(); });
  window.addEventListener('resize',    function ()  { if (window.innerWidth > 980) closeMobile(); });
}());
