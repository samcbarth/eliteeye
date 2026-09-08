// Elite Eye — progressive enhancement only. Every effect here is decoration:
// with JS off the page is fully readable, and everything is disabled outright
// when the visitor asks for reduced motion.

const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Nothing is hidden by CSS until this class is set, so a script error, a
// blocked file or an observer that never fires can only cost the animation,
// never the content.
const root = document.documentElement;
if (!REDUCED) root.classList.add('js-motion');

// Belt and braces: whatever happens, everything is on screen shortly after
// load. showAll() is idempotent and also runs from the observer below.
const showAll = () => {
  document.querySelectorAll('.reveal, .stagger').forEach((el) => el.classList.add('is-visible'));
};
setTimeout(showAll, 2200);

// Hairline under the header once the hero scrolls past.
const header = document.querySelector('.site-header');
if (header) {
  const setScrolled = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
  setScrolled();
  addEventListener('scroll', setScrolled, { passive: true });
}

// Mobile nav.
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  });
  nav.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Menu';
    }
  });
}

// Index children of staggered containers so CSS can delay each one in turn.
document.querySelectorAll('.stagger').forEach((group) => {
  [...group.children].forEach((child, i) => child.style.setProperty('--i', i));
});

// Fade sections in on first scroll into view.
const reveals = document.querySelectorAll('.reveal, .stagger');
if (!REDUCED && reveals.length && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    }
  }, { rootMargin: '0px 0px -12% 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  showAll();
}

// Split the headline into words that rise into place on load. Done in JS so the
// HTML stays one clean string for search engines and screen readers.
const headline = document.querySelector('[data-rise]');
if (headline && !REDUCED) {
  const words = headline.textContent.trim().split(/\s+/);
  headline.textContent = '';
  words.forEach((word, i) => {
    const outer = document.createElement('span');
    outer.className = 'rise';
    const inner = document.createElement('span');
    inner.style.setProperty('--w', i);
    inner.textContent = word;
    outer.appendChild(inner);
    headline.appendChild(outer);
    if (i < words.length - 1) headline.appendChild(document.createTextNode(' '));
  });
}

// Parallax: shift each marked image against the scroll, capped so it never
// exposes an edge. One rAF-throttled scroll listener drives all of them.
const drifters = [...document.querySelectorAll('[data-parallax]')];
if (drifters.length && !REDUCED) {
  let ticking = false;

  const update = () => {
    ticking = false;
    const viewport = innerHeight;
    for (const el of drifters) {
      const box = el.getBoundingClientRect();
      if (box.bottom < -200 || box.top > viewport + 200) continue;
      // -1 when the element is entering at the bottom, 1 when it is leaving.
      const progress = (box.top + box.height / 2 - viewport / 2) / (viewport / 2 + box.height / 2);
      const range = Number(el.dataset.parallax) || 40;
      el.style.setProperty('--shift', `${(progress * range).toFixed(1)}px`);
    }
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  };

  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  update();

  // Some embedded viewers never emit scroll events. A cheap rAF loop keeps the
  // drift correct there; it costs one getBoundingClientRect per image per frame
  // and only runs while the tab is visible.
  let lastY = -1;
  const poll = () => {
    if (scrollY !== lastY) {
      lastY = scrollY;
      update();
    }
    requestAnimationFrame(poll);
  };
  requestAnimationFrame(poll);
}


// Marquee tiles carry data-src rather than src: the track is moved with a
// transform, so native lazy loading never fires for them and they scroll in
// blank. Instead the whole strip loads once when it approaches the viewport,
// which keeps them off the critical path without the blank-tile problem.
const marquee = document.querySelector('.marquee');
if (marquee) {
  const loadTiles = () => {
    // Set the <source> before the <img>, so the browser picks the WebP.
    marquee.querySelectorAll('source[data-srcset]').forEach((source) => {
      source.srcset = source.dataset.srcset;
      delete source.dataset.srcset;
    });
    marquee.querySelectorAll('img[data-src]').forEach((img) => {
      img.src = img.dataset.src;
      delete img.dataset.src;
    });
  };

  if ('IntersectionObserver' in window) {
    const mo = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        loadTiles();
        mo.disconnect();
      }
    }, { rootMargin: '600px 0px' });
    mo.observe(marquee);
    // Same failsafe as the reveals: never leave the strip empty.
    setTimeout(loadTiles, 3000);
  } else {
    loadTiles();
  }
}
