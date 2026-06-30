/* =========================================================
   CampusEnergy — shared UI behavior
   ========================================================= */

const CE = (() => {

  function initRevealOnScroll(root = document) {
    const els = root.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || !els.length) {
      els.forEach((el) => el.classList.add('is-visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    els.forEach((el, i) => { el.style.setProperty('--i', i % 8); io.observe(el); });
  }

  function initButtonEffects(root = document) {
    root.querySelectorAll('.btn').forEach((btn) => {
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        const mx = (e.clientX - r.left - r.width / 2) * 0.08;
        const my = (e.clientY - r.top - r.height / 2) * 0.18;
        btn.style.setProperty('--bx', `${mx}px`);
        btn.style.setProperty('--by', `${my}px`);
      });
      btn.addEventListener('pointerleave', () => {
        btn.style.setProperty('--bx', `0px`);
        btn.style.setProperty('--by', `0px`);
      });
      btn.addEventListener('click', (e) => {
        const r = btn.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        const size = Math.max(r.width, r.height) * 1.4;
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${e.clientX - r.left - size / 2}px`;
        ripple.style.top = `${e.clientY - r.top - size / 2}px`;
        btn.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
      });
    });
  }

  function setButtonLoading(btn, loading) {
    if (!btn) return;
    btn.classList.toggle('is-loading', !!loading);
    btn.disabled = !!loading;
  }

  function ensureToastStack() {
    let stack = document.querySelector('.toast-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.className = 'toast-stack';
      stack.setAttribute('aria-live', 'polite');
      document.body.appendChild(stack);
    }
    return stack;
  }

  function toast(message, type = 'success', timeout = 3600) {
    const stack = ensureToastStack();
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.innerHTML = `<span>${type === 'success' ? '⚡' : '⚠'}</span><span>${message}</span>`;
    stack.appendChild(el);
    setTimeout(() => {
      el.classList.add('leaving');
      el.addEventListener('animationend', () => el.remove());
    }, timeout);
  }

  function validateField(fieldEl, isValid, message) {
    fieldEl.classList.toggle('invalid', !isValid);
    fieldEl.classList.toggle('valid', isValid && fieldEl.querySelector('input').value.length > 0);
    const err = fieldEl.querySelector('.field-error');
    if (err && message) err.textContent = message;
  }

  function buildFooter() {
    return `
    <footer class="site-footer">
      <div class="footer-top">
        <div>
          <div class="brand" style="margin-bottom:14px;">
            <span class="bolt"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg></span>
            <span class="c1">Campus</span><span class="c2">Energy</span>
          </div>
          <p style="max-width:260px; font-size:0.88rem;">Tracking how our campus uses power, one building at a time.</p>
          <p style="margin-top:18px; font-size:0.82rem; color:var(--text-faint);">© 2024 — 2026 CampusEnergy</p>
        </div>
        <div class="footer-cols">
          <div class="footer-col">
            <h4>Platform</h4>
            <a href="posts.html">Posts</a>
            <a href="profile.html">Profile</a>
            <a href="login.html">Sign in</a>
          </div>
          <div class="footer-col">
            <h4>Data</h4>
            <a href="posts.html">Consumption logs</a>
            <a href="#">Building reports</a>
            <a href="#">Predictions</a>
          </div>
          <div class="footer-col">
            <h4>Resources</h4>
            <a href="about.html">About us</a>
            <a href="#">API docs</a>
            <a href="#">Contact</a>
          </div>
          <div class="footer-col">
            <h4>Company</h4>
            <a href="about.html">Our mission</a>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <nav class="footer-nav">
          <a href="index.html">Home</a>
          <a href="about.html">About Us</a>
          <a href="posts.html">Posts</a>
        </nav>
        <div class="footer-socials">
          <a class="social-dot" href="#" aria-label="X / Twitter">𝕏</a>
          <a class="social-dot" href="#" aria-label="Instagram">◎</a>
          <a class="social-dot" href="#" aria-label="LinkedIn">in</a>
        </div>
      </div>
    </footer>`;
  }

  function mountFooter(targetSelector = '#site-footer') {
    const target = document.querySelector(targetSelector);
    if (target) target.outerHTML = buildFooter();
  }

  async function mountTopbar({ active = '', mountSelector = '#site-topbar' } = {}) {
    const target = document.querySelector(mountSelector);
    if (!target) return;

    let session = null;
    try { session = await CampusEnergyAPI.getCurrentUser(); } catch (e) { session = null; }

    const navLink = (href, label, key) =>
      `<a href="${href}" class="${active === key ? 'active' : ''}">${label}</a>`;

    const rightSide = session
      ? `<div class="nav-right">
           <span class="welcome-text">Welcome, <strong>${session.username}</strong>!</span>
           <button class="avatar-btn" id="avatarBtn" title="My profile">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
           </button>
         </div>`
      : `<a class="btn-login-pill" href="login.html">Login</a>`;

    target.outerHTML = `
    <header class="topbar">
      <a class="brand" href="index.html">
        <span class="bolt"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg></span>
        <span class="c1">Campus</span><span class="c2">Energy</span>
      </a>
      <nav class="nav-links">
        ${navLink('index.html', 'Home', 'home')}
        ${navLink('about.html', 'About Us', 'about')}
      </nav>
      ${rightSide}
    </header>`;

    const avatarBtn = document.getElementById('avatarBtn');
    if (avatarBtn) avatarBtn.addEventListener('click', () => (window.location.href = 'profile.html'));
  }

  function initAll(opts = {}) {
    const run = async () => {
      await mountTopbar(opts.topbar || {});
      mountFooter(opts.footerSelector);
      initRevealOnScroll();
      initButtonEffects();
      if (typeof opts.onReady === 'function') opts.onReady();
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', run);
    } else {
      run();
    }
  }

  return { initAll, initRevealOnScroll, initButtonEffects, setButtonLoading, toast, validateField, mountTopbar, mountFooter };
})();
