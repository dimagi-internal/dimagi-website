/* Article page behaviors: reading-progress bar, copy-link share, back-to-top.
   Progressive enhancement — the page is fully usable without JS. */
(function () {
  var bar = document.querySelector('.reading-progress-bar');
  var toTop = document.querySelector('.back-to-top');
  var ticking = false;

  function update() {
    var doc = document.documentElement;
    var max = (doc.scrollHeight - window.innerHeight);
    var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    if (pct < 0) pct = 0; if (pct > 100) pct = 100;
    if (bar) bar.style.width = pct + '%';
    if (toTop) toTop.classList.toggle('is-visible', window.scrollY > 600);
    ticking = false;
  }
  function onScroll() {
    if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
  }
  if (bar || toTop) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
  }

  if (toTop) {
    toTop.addEventListener('click', function () {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }

  /* Copy-link buttons */
  var copyBtns = document.querySelectorAll('.article-copy');
  Array.prototype.forEach.call(copyBtns, function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-copy-url') || window.location.href;
      var label = btn.querySelector('.article-copy-label');
      var original = label ? label.textContent : null;
      function done() {
        btn.classList.add('is-copied');
        if (label) label.textContent = 'Copied!';
        setTimeout(function () {
          btn.classList.remove('is-copied');
          if (label && original !== null) label.textContent = original;
        }, 1800);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = url; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* Table of contents scrollspy */
  var toc = document.querySelector('.article-toc');
  if (toc) {
    var tocLinks = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    var tocTargets = tocLinks.map(function (a) {
      return document.getElementById(a.getAttribute('href').slice(1));
    });
    var spyTicking = false;
    function spyUpdate() {
      var activeHref = tocLinks.length ? tocLinks[0].getAttribute('href') : null;
      for (var i = 0; i < tocTargets.length; i++) {
        if (tocTargets[i] && tocTargets[i].getBoundingClientRect().top <= 120) {
          activeHref = tocLinks[i].getAttribute('href');
        }
      }
      for (var j = 0; j < tocLinks.length; j++) {
        tocLinks[j].classList.toggle('is-active', tocLinks[j].getAttribute('href') === activeHref);
      }
      spyTicking = false;
    }
    function spyScroll() {
      if (!spyTicking) { window.requestAnimationFrame(spyUpdate); spyTicking = true; }
    }
    window.addEventListener('scroll', spyScroll, { passive: true });
    window.addEventListener('resize', spyScroll, { passive: true });
    spyUpdate();
  }
})();
