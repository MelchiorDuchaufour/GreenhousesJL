// =====================================================================
// GreenhousesJL deck, fixed 1920x1080 stage scaled to fit the viewport
//                     + in-slide fragment reveals (data-fragment="N")
// =====================================================================
(() => {
  const stage   = document.getElementById('stage');
  const slides  = document.querySelectorAll('.slide');
  const total   = slides.length;

  // ----- Inject a subtle "↩ summary" link on every slide that isn't the
  // title, the summary, or the contents, so viewers can always jump back
  // to the clickable table of contents (slide 2b).
  slides.forEach((s) => {
    const ds = s.dataset.slide;
    if (ds === '1' || ds === '2' || ds === '2b') return;
    const a = document.createElement('a');
    a.className = 'back-to-summary';
    a.href = 'javascript:void(0)';
    a.textContent = '↩ contents';
    a.addEventListener('click', (e) => { e.preventDefault(); window.goToSlide('2b'); });
    s.appendChild(a);
  });
  const counter = document.getElementById('counter');
  const prev    = document.getElementById('prev');
  const next    = document.getElementById('next');

  const STAGE_W = 1920;
  const STAGE_H = 1080;
  const fit = () => {
    const margin = 60;
    const sx = window.innerWidth  / STAGE_W;
    const sy = (window.innerHeight - margin) / STAGE_H;
    const s  = Math.min(sx, sy);
    stage.style.setProperty('--scale', s.toString());
  };
  window.addEventListener('resize', fit);
  fit();

  // ----- per-slide step state -------------------------------------------
  let i    = 0;
  let step = 0;

  const maxStep = (slide) => {
    const frags = slide.querySelectorAll('[data-fragment]');
    if (frags.length === 0) return 0;
    let m = 0;
    frags.forEach(f => { m = Math.max(m, parseInt(f.dataset.fragment, 10) || 0); });
    return m;
  };

  const updateFragments = () => {
    const cur = slides[i];
    // expose the current step on the slide so CSS can target both
    // cumulative reveals (.shown class) and exclusive ones (data-step attr).
    cur.setAttribute('data-step', String(step));
    cur.querySelectorAll('[data-fragment]').forEach(el => {
      const n = parseInt(el.dataset.fragment, 10);
      el.classList.toggle('shown', n <= step);
    });
  };

  const footerPage = document.getElementById('footer-page');

  const show = (n) => {
    i = (n + total) % total;
    step = 0;
    slides.forEach((s, k) => s.classList.toggle('active', k === i));
    const label = `${String(i + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
    counter.textContent = `${i + 1} / ${total}`;
    if (footerPage) footerPage.textContent = label;
    // Mark the title slide so the footer can be hidden via CSS
    stage.classList.toggle('is-title', i === 0);
    updateFragments();
  };

  const advance = () => {
    const cur = slides[i];
    if (step < maxStep(cur)) {
      step++;
      updateFragments();
    } else {
      show(i + 1);
    }
  };

  const retreat = () => {
    if (step > 0) {
      step--;
      updateFragments();
    } else {
      show(i - 1);
    }
  };

  prev.addEventListener('click', () => retreat());
  next.addEventListener('click', () => advance());

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') advance();
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp')                  retreat();
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End')  show(total - 1);
    else if (e.key === 'f' || e.key === 'F') {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
  });

  // Public API: jump to a slide by its data-slide value (number or string like "10b")
  window.goToSlide = (dataSlide) => {
    const target = String(dataSlide);
    for (let k = 0; k < total; k++) {
      if (slides[k].dataset.slide === target) {
        show(k);
        return;
      }
    }
  };

  show(0);
})();
