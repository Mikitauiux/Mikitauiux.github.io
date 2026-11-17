// Shared script for the home page and case pages. Every page-specific block checks that its section exists.
gsap.registerPlugin(ScrollTrigger);

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = matchMedia('(pointer: fine)').matches;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

/* ---------- Text splitting (keeps an accessible label on the parent) ---------- */
function split(el, unit) {
  const text = el.textContent.trim();
  el.setAttribute('aria-label', text);
  el.textContent = '';
  const parts = unit === 'char' ? [...text] : text.split(/(\s+)/);
  parts.forEach(part => {
    if (unit === 'word' && /^\s+$/.test(part)) { el.append(' '); return; }
    const span = document.createElement('span');
    span.className = unit;
    span.setAttribute('aria-hidden', 'true');
    span.textContent = part === ' ' ? ' ' : part;
    el.append(span);
  });
  return $$('.' + unit, el);
}
$$('.split').forEach(el => split(el, 'char'));
$$('.split-words').forEach(el => split(el, 'word'));

/* ---------- Smooth scroll ---------- */
let lenis = null;
if (!reduce && window.Lenis) {
  lenis = new Lenis({ lerp: 0.09 });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}
function scrollToEl(target, immediate = false) {
  if (lenis) lenis.scrollTo(target, { duration: 1.6, immediate });
  else target.scrollIntoView({ behavior: reduce || immediate ? 'auto' : 'smooth' });
}
$$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
  const target = $(a.getAttribute('href'));
  if (!target) return;
  e.preventDefault();
  scrollToEl(target);
}));

/* ---------- Page transitions: lime curtain covers the page, then navigates ---------- */
const curtain = $('.curtain');
$$('a[data-transition]').forEach(a => a.addEventListener('click', e => {
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0 || reduce || !curtain) return;
  e.preventDefault();
  gsap.set(curtain, { visibility: 'visible' });
  gsap.fromTo(curtain, { yPercent: 100 }, { yPercent: 0, duration: 0.7, ease: 'expo.inOut', onComplete: () => (location.href = a.href) });
}));
// Back/forward cache restores the page with the curtain still down.
addEventListener('pageshow', e => { if (e.persisted && curtain) gsap.set(curtain, { yPercent: -100, visibility: 'hidden' }); });

/* ---------- Intro: preloader on first visit, curtain reveal afterwards ---------- */
let seen = false;
try { seen = sessionStorage.getItem('seen') === '1'; sessionStorage.setItem('seen', '1'); } catch (e) {}
const preloader = $('.preloader');

function jumpToHash() {
  const target = location.hash && $(location.hash);
  if (target) { ScrollTrigger.refresh(); scrollToEl(target, true); }
}

if (reduce) {
  preloader && preloader.remove();
  curtain && (curtain.style.visibility = 'hidden');
  addEventListener('load', jumpToHash);
} else {
  lenis && lenis.stop();
  const tl = gsap.timeline({ onComplete: () => { lenis && lenis.start(); jumpToHash(); } });

  if (preloader && !seen) {
    curtain && gsap.set(curtain, { visibility: 'hidden' });
    const num = $('.preloader__num');
    const count = { v: 0 };
    tl.to(count, { v: 100, duration: 1.8, ease: 'power3.inOut', onUpdate: () => (num.textContent = Math.round(count.v)) })
      .to('.preloader__bar span', { scaleX: 1, duration: 1.8, ease: 'power3.inOut' }, 0)
      .to('.preloader__count, .preloader__top', { yPercent: -40, opacity: 0, duration: 0.5, ease: 'power2.in' })
      .to(preloader, { clipPath: 'inset(0 0 100% 0)', duration: 1, ease: 'expo.inOut', onComplete: () => preloader.remove() }, '-=0.15');
  } else {
    preloader && preloader.remove();
    if (curtain) tl.to(curtain, { yPercent: -100, duration: 0.9, ease: 'expo.inOut', delay: 0.1 }).set(curtain, { visibility: 'hidden' });
  }

  if ($('.hero')) {
    tl.from('.hero__title .char', { yPercent: 115, rotate: 8, duration: 1.3, stagger: 0.04, ease: 'expo.out' }, '-=0.55')
      .from('.hero__eyebrow, .nav, .hero__meta > *', { y: 24, opacity: 0, duration: 0.9, stagger: 0.08, ease: 'power3.out' }, '-=1');
  }
  if ($('.cs-hero')) {
    tl.from('.cs-hero__title .char', { yPercent: 115, duration: 1.2, stagger: 0.03, ease: 'expo.out' }, '-=0.5')
      .from('.cs-hero [data-fade]', { y: 30, opacity: 0, duration: 0.9, stagger: 0.07, ease: 'power3.out' }, '-=0.9');
  }
}

/* ---------- Videos play only while visible ---------- */
const videoObserver = new IntersectionObserver(entries => entries.forEach(e => {
  if (e.isIntersecting) e.target.play().catch(() => {}); else e.target.pause();
}), { rootMargin: '200px' });
$$('video[data-autoplay]').forEach(v => {
  if (reduce) v.controls = true;
  else videoObserver.observe(v);
});

/* ---------- Case slides: tap to zoom on small screens ---------- */
if ($('.cs-shot')) {
  const dialog = document.createElement('dialog');
  dialog.className = 'zoom';
  dialog.innerHTML = '<button class="zoom__close" aria-label="Close">×</button><div class="zoom__scroll" data-lenis-prevent></div><p class="zoom__hint">Swipe to explore</p>';
  document.body.append(dialog);
  const box = $('.zoom__scroll', dialog);
  $('.zoom__close', dialog).addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { box.replaceChildren(); lenis && lenis.start(); });

  $$('.cs-shot').forEach(shot => shot.addEventListener('click', () => {
    if (innerWidth >= 900) return;
    const media = shot.firstElementChild.cloneNode();
    media.removeAttribute('loading');
    box.replaceChildren(media);
    if (media.tagName === 'VIDEO') { media.muted = true; media.play().catch(() => {}); }
    lenis && lenis.stop();
    dialog.showModal();
    box.scrollTo(0, 0);
  }));
}

/* ---------- Scroll animations (skipped for reduced motion: content stays static) ---------- */
if (!reduce) {
  // Hero: title drifts and spreads, WebGL fades out
  if ($('.hero')) {
    gsap.to('.hero__title', {
      yPercent: 35, letterSpacing: '0.02em', ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
    ScrollTrigger.create({
      trigger: '.hero', start: 'top top', end: 'bottom top',
      onUpdate: self => window.heroGL && window.heroGL.setScroll(self.progress)
    });
  }

  // Marquee: constant loop, speed boosted by scroll velocity
  const loops = $$('.marquee__inner').map((el, i) =>
    i % 2
      ? gsap.fromTo(el, { xPercent: -50 }, { xPercent: 0, duration: 32, ease: 'none', repeat: -1 })
      : gsap.to(el, { xPercent: -50, duration: 28, ease: 'none', repeat: -1 })
  );
  if (loops.length) {
    let settle;
    ScrollTrigger.create({
      onUpdate(self) {
        const boost = Math.min(Math.abs(self.getVelocity()) / 250, 6);
        loops.forEach(t => t.timeScale(1 + boost));
        clearTimeout(settle);
        settle = setTimeout(() => loops.forEach(t => gsap.to(t, { timeScale: 1, duration: 1, ease: 'power2.out' })), 120);
      }
    });
  }

  // About: photo mask reveal + parallax, words light up as you scroll
  if ($('.intro')) {
    gsap.timeline({ scrollTrigger: { trigger: '.intro__photo', start: 'top 80%' } })
      .fromTo('.intro__photo-frame', { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, ease: 'expo.inOut' })
      .from('.intro__photo img', { scale: 1.4, duration: 1.8, ease: 'expo.out' }, 0.2)
      .from('.intro__photo figcaption span', { y: 16, opacity: 0, stagger: 0.1, duration: 0.8, ease: 'power3.out' }, 0.8);
    gsap.fromTo('.intro__photo img', { yPercent: -7 }, {
      yPercent: 7, ease: 'none',
      scrollTrigger: { trigger: '.intro', start: 'top bottom', end: 'bottom top', scrub: true }
    });
    gsap.fromTo('.intro__text .word', { opacity: 0.12 }, {
      opacity: 1, stagger: 0.1, ease: 'none',
      scrollTrigger: { trigger: '.intro__text', start: 'top 80%', end: 'bottom 45%', scrub: true }
    });
  }

  // Section headings
  $$('.section-head__title').forEach(h => {
    gsap.from(h, { yPercent: 40, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: h, start: 'top 85%' } });
  });

  // Stats: count-up numbers (home impact + case hero)
  $$('.stats').forEach(stats => {
    $$('.stat', stats).forEach((stat, i) => {
      const el = $('.stat__num', stat);
      const { prefix = '', suffix = '', to } = el.dataset;
      const n = { v: 0 };
      el.textContent = prefix + 0 + suffix;
      gsap.timeline({ scrollTrigger: { trigger: stats, start: 'top 85%' } })
        .from(stat, { y: 60, opacity: 0, duration: 1, ease: 'expo.out' }, i * 0.1)
        .to(n, { v: +to, duration: 2, ease: 'power3.out', onUpdate: () => (el.textContent = prefix + Math.round(n.v) + suffix) }, i * 0.1);
    });
  });

  // Rows: staggered reveal
  ['.cap', '.exp__row', '.tools li'].forEach(sel => {
    if (!$(sel)) return;
    // Hide up front: hiding on enter makes already-visible rows blink and jump.
    gsap.set(sel, { y: 50, opacity: 0 });
    ScrollTrigger.batch(sel, {
      start: 'top 90%', once: true,
      onEnter: els => gsap.to(els, { y: 0, opacity: 1, duration: 1, stagger: 0.08, ease: 'expo.out' })
    });
  });

  // Big split titles in footer / next-case
  $$('.contact__title, .cs-next__title').forEach(title => {
    gsap.from($$('.char', title), {
      yPercent: 110, duration: 1.2, stagger: 0.04, ease: 'expo.out',
      scrollTrigger: { trigger: title, start: 'top 85%' }
    });
  });

  // Nav switches to dark text over the lime contact footer
  if ($('.contact')) {
    ScrollTrigger.create({ trigger: '.contact', start: 'top 40px', end: 'bottom top', toggleClass: { targets: '.nav', className: 'nav--dark' } });
  }

  // Home work: horizontal pinned scroll on desktop, simple reveals on mobile
  if ($('.work')) {
    const mm = gsap.matchMedia();
    mm.add('(min-width: 900px)', () => {
      const track = $('.work__track');
      const distance = () => Math.max(0, track.scrollWidth - innerWidth);
      const horizontal = gsap.to(track, {
        x: () => -distance(), ease: 'none',
        scrollTrigger: {
          trigger: '.work', start: 'top top', end: () => '+=' + distance(),
          pin: true, scrub: 1, invalidateOnRefresh: true,
          onUpdate: self => gsap.set('.work__progress span', { scaleX: self.progress })
        }
      });
      $$('.case').forEach(c => {
        // Cards already on screen when the pin starts reveal on vertical entry; the rest as they slide in.
        const visibleAtStart = c.offsetLeft < innerWidth * 0.85;
        gsap.from($('.case__media', c), {
          clipPath: 'inset(0% 0% 100% 0% round 20px)', duration: 1.4, ease: 'expo.inOut',
          scrollTrigger: visibleAtStart
            ? { trigger: '.work', start: 'top 60%' }
            : { trigger: c, containerAnimation: horizontal, start: 'left 85%' }
        });
      });
    });
    mm.add('(max-width: 899px)', () => {
      $$('.case').forEach(c => gsap.from(c, { y: 80, opacity: 0, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: c, start: 'top 85%' } }));
    });
  }

  // Case page: cover grows to full width, shots rise in
  if ($('.cs-cover')) {
    gsap.fromTo('.cs-cover__frame', { scale: 0.86 }, {
      scale: 1, ease: 'none',
      scrollTrigger: { trigger: '.cs-cover', start: 'top bottom', end: 'top 15%', scrub: true }
    });
  }
  $$('.cs-shot').forEach(shot => {
    gsap.from(shot, { y: 90, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: shot, start: 'top 92%' } });
  });
}

/* ---------- Pointer effects (desktop only) ---------- */
if (finePointer && !reduce) {
  const cursor = $('.cursor');
  const label = $('.cursor__label');
  const cx = gsap.quickTo(cursor, 'x', { duration: 0.35, ease: 'power3' });
  const cy = gsap.quickTo(cursor, 'y', { duration: 0.35, ease: 'power3' });
  document.documentElement.classList.add('has-cursor');
  addEventListener('pointermove', e => { cx(e.clientX); cy(e.clientY); cursor.classList.add('is-visible'); });
  document.documentElement.addEventListener('mouseleave', () => cursor.classList.remove('is-visible'));
  document.addEventListener('pointerover', e => {
    const labelled = e.target.closest('[data-cursor]');
    const link = e.target.closest('a, button');
    cursor.classList.toggle('is-label', !!labelled);
    cursor.classList.toggle('is-link', !labelled && !!link);
    if (labelled) label.textContent = labelled.dataset.cursor;
  });

  $$('[data-magnetic]').forEach(el => {
    const xTo = gsap.quickTo(el, 'x', { duration: 0.6, ease: 'power3' });
    const yTo = gsap.quickTo(el, 'y', { duration: 0.6, ease: 'power3' });
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      xTo((e.clientX - r.left - r.width / 2) * 0.35);
      yTo((e.clientY - r.top - r.height / 2) * 0.35);
    });
    el.addEventListener('pointerleave', () => {
      gsap.to(el, { x: 0, y: 0, duration: 1, ease: 'elastic.out(1, 0.35)', overwrite: true });
    });
  });

  // 3D tilt on case covers
  $$('.case__media').forEach(media => {
    media.addEventListener('pointermove', e => {
      const r = media.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      gsap.to(media, { rotateY: px * 8, rotateX: -py * 8, duration: 0.6, ease: 'power3.out', transformPerspective: 1200 });
    });
    media.addEventListener('pointerleave', () => {
      gsap.to(media, { rotateY: 0, rotateX: 0, duration: 1, ease: 'elastic.out(1, 0.45)' });
    });
  });
}

/* ---------- Local time in Wroclaw ---------- */
const clock = $('.clock');
if (clock) {
  const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Warsaw' });
  const tick = () => (clock.textContent = fmt.format(new Date()) + ' CET');
  tick();
  setInterval(tick, 30000);
}

// Fonts and lazy images change layout, so measure pins and triggers again once they are in.
document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh());
addEventListener('load', () => ScrollTrigger.refresh());
