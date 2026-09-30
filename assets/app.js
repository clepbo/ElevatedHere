/* ElevatedHere — motion engine
   Every entrance animation is two-way: it plays on the way down and reverses
   on the way back up. Vanilla, IO-driven, rAF-batched, fully disabled under
   prefers-reduced-motion. */

const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const raf = (f) => requestAnimationFrame(f);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* ---------- preloader ---------- */
function bootPreloader(done) {
  const pre = $('.pre'), word = $('.pre-word');
  const skip = !pre || !word || REDUCED || location.search.includes('nopre') || sessionStorage.getItem('eh-seen');
  if (skip) {
    if (pre) pre.classList.add('done');
    document.body.classList.remove('loading');
    done();
    return;
  }
  let finished = false;
  const finish = () => {
    if (finished) return;
    finished = true;
    sessionStorage.setItem('eh-seen', '1');   // only greet once per session
    pre.classList.add('done');
    document.body.classList.remove('loading');
    done();
  };
  setTimeout(finish, 2600);                    // failsafe if rAF is throttled

  const target = word.dataset.word || 'PROOF';
  const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#%&*+=<>';
  let frame = 0;
  const per = 3, total = target.length * per + 18;
  (function tick() {
    let out = '';
    for (let i = 0; i < target.length; i++) {
      if (frame > i * per + per) out += target[i];
      else if (target[i] === ' ') out += ' ';
      else out += glyphs[(Math.random() * glyphs.length) | 0];
    }
    word.textContent = out;
    if (++frame < total) raf(tick);
    else setTimeout(finish, 380);
  })();
}

/* ---------- shared scroll loop ---------- */
const jobs = [];
let ticking = false;
function onScroll() {
  if (ticking) return;
  ticking = true;
  raf(() => { const y = scrollY; jobs.forEach((j) => j(y)); ticking = false; });
}
addEventListener('scroll', onScroll, { passive: true });
addEventListener('resize', onScroll, { passive: true });

/* ---------- nav ---------- */
const nav = $('.nav');
if (nav) {
  jobs.push((y) => nav.classList.toggle('scrolled', y > 10));
  const t = $('.nav-toggle', nav), l = $('.nav-links', nav);
  if (t && l) {
    t.addEventListener('click', () => {
      const open = l.classList.toggle('open');
      t.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open);
    });
    l.addEventListener('click', (e) => {
      if (e.target.tagName !== 'A') return;
      l.classList.remove('open');
      t.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
    });
    addEventListener('keydown', (e) => {
      if (e.key !== 'Escape' || !l.classList.contains('open')) return;
      l.classList.remove('open');
      t.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
      t.focus();
    });
  }
}

/* ---------- scroll progress ---------- */
const barEl = $('.progress i');
if (barEl) jobs.push((y) => {
  const max = document.documentElement.scrollHeight - innerHeight;
  barEl.style.width = (max > 0 ? Math.min(y / max, 1) * 100 : 0) + '%';
});

/* ---------- two-way reveals ----------
   The observer toggles rather than unobserves, so scrolling back up plays
   every entrance in reverse. Counters reset so they re-run on re-entry. */
const ANIMATED = '.reveal, .stagger, .brow, .split, .cluster, .chartbox';

if (REDUCED || !('IntersectionObserver' in window)) {
  $$(ANIMATED).forEach((el) => el.classList.add('in'));
  $$('[data-count]').forEach(settle);
} else {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const el = e.target;
      if (e.isIntersecting) {
        el.classList.add('in');
        $$('[data-count]', el).forEach(countUp);
        if (el.matches('[data-count]')) countUp(el);
      } else {
        el.classList.remove('in');
        $$('[data-count]', el).forEach(resetCount);
        if (el.matches('[data-count]')) resetCount(el);
      }
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 });
  $$(ANIMATED).forEach((el) => io.observe(el));
  // counters that sit outside an animated wrapper
  $$('[data-count]').forEach((el) => { if (!el.closest(ANIMATED)) io.observe(el); });
}

function settle(el) { el.textContent = el.dataset.count; }

function resetCount(el) {
  if (!el.dataset.zero) return;
  el.dataset.running = '';
  el.textContent = el.dataset.zero;
}

function countUp(el) {
  if (el.dataset.zero === undefined) el.dataset.zero = el.textContent;  // remember the start state
  if (el.dataset.running === '1') return;
  el.dataset.running = '1';

  const raw = el.dataset.count;
  const m = raw.match(/-?[\d.,]+/);
  if (!m) { el.textContent = raw; return; }
  const n = m[0], target = parseFloat(n.replace(/,/g, ''));
  const dec = (n.split('.')[1] || '').length, comma = n.includes(',');
  const pre = raw.slice(0, m.index), post = raw.slice(m.index + n.length);
  const t0 = performance.now(), dur = 1400;
  (function f(now) {
    if (el.dataset.running !== '1') return;            // cancelled by scrolling away
    const p = Math.min((now - t0) / dur, 1);
    let v = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec);
    if (comma) v = Number(v).toLocaleString('en-US', { minimumFractionDigits: dec });
    el.textContent = pre + v + post;
    if (p < 1) raf(f);
  })(performance.now());
}

/* ---------- word-by-word highlight (inherently two-way) ---------- */
$$('[data-words]').forEach((box) => {
  const text = box.textContent.trim();
  const green = (box.dataset.green || '').split('|').filter(Boolean);
  box.textContent = '';
  const words = text.split(/\s+/).map((w) => {
    const s = document.createElement('span');
    s.className = 'w' + (green.some((g) => w.replace(/[^\w']/g, '').toLowerCase() === g.toLowerCase()) ? ' g' : '');
    s.textContent = w;
    box.append(s, document.createTextNode(' '));
    return s;
  });
  if (REDUCED) { words.forEach((w) => w.classList.add('on')); return; }
  jobs.push(() => {
    const r = box.getBoundingClientRect();
    const start = innerHeight * 0.88, end = innerHeight * 0.34;
    const p = Math.min(Math.max((start - r.top) / (start - end), 0), 1);
    const upto = Math.round(p * words.length);
    words.forEach((w, i) => w.classList.toggle('on', i < upto));
  });
});

/* ---------- testimonial carousel ---------- */
$$('[data-carousel]').forEach((car) => {
  const track = $('.ttrack', car), slides = $$('.tslide', track);
  const dots = $('.tdots', car.parentElement) || $('.tdots', car);
  let i = 0, timer;
  if (dots) slides.forEach((_, n) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', 'Story ' + (n + 1));
    b.addEventListener('click', () => { go(n); restart(); });
    dots.append(b);
  });
  function go(n) {
    i = (n + slides.length) % slides.length;
    track.style.transform = 'translateX(' + (-i * 100) + '%)';
    if (dots) $$('button', dots).forEach((b, k) => b.classList.toggle('on', k === i));
  }
  function restart() { clearInterval(timer); if (!REDUCED) timer = setInterval(() => go(i + 1), 5200); }
  go(0); restart();
  car.addEventListener('mouseenter', () => clearInterval(timer));
  car.addEventListener('mouseleave', restart);
});

/* ---------- FAQ accordion ---------- */
$$('.faq-item').forEach((item) => {
  const q = $('.faq-q', item), a = $('.faq-a', item);
  if (!q || !a) return;
  q.setAttribute('aria-expanded', 'false');
  q.addEventListener('click', () => {
    const open = item.classList.toggle('open');
    q.setAttribute('aria-expanded', String(open));
    a.style.maxHeight = open ? a.scrollHeight + 'px' : '0px';
  });
});
let rt;
addEventListener('resize', () => {
  clearTimeout(rt);
  rt = setTimeout(() => $$('.faq-item.open .faq-a').forEach((a) => { a.style.maxHeight = a.scrollHeight + 'px'; }), 150);
});

/* ---------- magnetic buttons (pointer devices only) ---------- */
if (!REDUCED && matchMedia('(pointer: fine)').matches) {
  $$('.btn').forEach((b) => {
    b.addEventListener('mousemove', (e) => {
      const r = b.getBoundingClientRect();
      b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.12) + 'px,'
                                       + ((e.clientY - r.top - r.height / 2) * 0.22) + 'px)';
    });
    b.addEventListener('mouseleave', () => { b.style.transform = ''; });
  });
}

/* ---------- seamless marquees ---------- */
$$('.ticker-track, .col').forEach((t) => { t.innerHTML += t.innerHTML; });

/* ---------- go ---------- */
document.body.classList.add('loading');
bootPreloader(() => {
  document.documentElement.classList.add('ready');
  onScroll();
});
onScroll();
