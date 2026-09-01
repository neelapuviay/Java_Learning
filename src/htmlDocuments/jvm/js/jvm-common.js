/* ================================================================
   JVM INTERNALS SIMULATOR — SHARED JS UTILITIES
================================================================ */

const $ = id => document.getElementById(id);
const REDUCED = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
const esc = s => String(s).replace(/</g, '&lt;').replace(/>/g, '&gt;');

/**
 * Sequential step-by-step animation executor with cancellation support.
 */
function Seq() {
  let token = 0;
  let timers = [];
  return {
    run(steps, done) {
      this.cancel();
      const my = ++token;
      let i = 0;
      const next = () => {
        if (my !== token) return;
        if (i >= steps.length) {
          if (done) done();
          return;
        }
        const [delay, fn] = steps[i++];
        timers.push(setTimeout(() => {
          if (my !== token) return;
          try { fn(); } catch (e) { console.error('Seq step error:', e); }
          next();
        }, REDUCED ? 0 : delay));
      };
      next();
    },
    cancel() {
      token++;
      timers.forEach(clearTimeout);
      timers = [];
    }
  };
}

/**
 * Theme Synchronization: Syncs theme with parent container or localStorage
 */
(function initTheme() {
  const savedTheme = localStorage.getItem('jvm_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  window.addEventListener('message', (e) => {
    if (e.data && e.data.type === 'SET_THEME') {
      document.documentElement.setAttribute('data-theme', e.data.theme);
      localStorage.setItem('jvm_theme', e.data.theme);
    }
  });
})();
