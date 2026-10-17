(() => {
  const button = document.querySelector('.menu');
  const nav = document.querySelector('#nav');

  if (button && nav) {
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!open));
      button.setAttribute('aria-label', open ? 'Open navigation' : 'Close navigation');
      nav.classList.toggle('open', !open);
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      nav.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.setAttribute('aria-label', 'Open navigation');
    }));
  }

  const year = document.querySelector('#year');
  if (year) year.textContent = new Date().getFullYear();

  // Scroll progress is decorative and never blocks interaction.
  const progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  progress.innerHTML = '<span></span>';
  document.body.prepend(progress);
  const progressBar = progress.firstElementChild;
  const header = document.querySelector('.header');
  let ticking = false;

  const updateScrollUI = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const percent = scrollable > 0 ? Math.min(100, Math.max(0, window.scrollY / scrollable * 100)) : 0;
    progressBar.style.width = percent + '%';
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 12);
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateScrollUI);
      ticking = true;
    }
  }, { passive: true });
  updateScrollUI();

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealTargets = document.querySelectorAll(
    '.heading, .services article, .project, .notice, .about-copy, .steps article, .contact-card, .resume h2, main > .section > h1'
  );

  if (!reduceMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -36px 0px' });

    revealTargets.forEach((element, index) => {
      element.classList.add('js-reveal');
      if (element.matches('.services article, .steps article')) {
        element.style.transitionDelay = (index % 4) * 70 + 'ms';
      }
      revealObserver.observe(element);
    });
  }

  // Subtle pointer response only on fine-pointer devices; no effect on touch.
  const art = document.querySelector('.art');
  if (art && !reduceMotion && window.matchMedia('(pointer: fine)').matches) {
    art.addEventListener('pointermove', event => {
      const bounds = art.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      art.style.setProperty('--pointer-x', (x * 7).toFixed(2) + 'px');
      art.style.setProperty('--pointer-y', (y * 7).toFixed(2) + 'px');
    });
    art.addEventListener('pointerleave', () => {
      art.style.setProperty('--pointer-x', '0px');
      art.style.setProperty('--pointer-y', '0px');
    });
  }
})();