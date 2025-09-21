// Utility: clamp
const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

// Sticky header shadow
const header = document.querySelector('[data-blur]');
window.addEventListener('scroll', () => {
  const y = window.scrollY || 0;
  if(!header) return;
  header.classList.toggle('scrolled', y > 6);
});

// Intersection-based reveals
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if(entry.isIntersecting){
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll('.reveal-up').forEach(el => observer.observe(el));

// Parallax orb canvas
const c = document.getElementById('orb');
if (c) {
  const ctx = c.getContext('2d');
  let w, h, t = 0;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  function resize(){
    w = c.clientWidth; h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr;
    ctx.scale(dpr, dpr);
  }
  function loop(){
    t += 0.01;
    ctx.clearRect(0,0,w,h);
    const cx = w*0.5 + Math.sin(t*0.8)*40;
    const cy = h*0.5 + Math.cos(t*0.6)*30;
    const r = Math.max(w,h)*0.35 + Math.sin(t)*8;
    const grad = ctx.createRadialGradient(cx, cy, r*0.1, cx, cy, r);
    grad.addColorStop(0, 'rgba(102,178,255,0.9)');
    grad.addColorStop(0.5, 'rgba(102,178,255,0.15)');
    grad.addColorStop(1, 'rgba(102,178,255,0)');
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.fill();
    requestAnimationFrame(loop);
  }
  resize(); loop();
  window.addEventListener('resize', resize);
}

// Tilt cards
document.querySelectorAll('.tilt').forEach((card) => {
  const r = 10; // max tilt deg
  card.addEventListener('pointermove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;   // 0..1
    const y = (e.clientY - rect.top) / rect.height;   // 0..1
    const rx = clamp((0.5 - y) * (r*2), -r, r);
    const ry = clamp((x - 0.5) * (r*2), -r, r);
    card.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) translateZ(0)`;
  });
  card.addEventListener('pointerleave', () => {
    card.style.transform = 'rotateX(0) rotateY(0)';
  });
});

// Mobile drawer
const drawer = document.getElementById('nav-drawer');
const toggle = document.querySelector('.nav-toggle');
const closeBtn = document.querySelector('.close-drawer');
if (toggle && drawer){
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    drawer.hidden = expanded;
  });
  closeBtn?.addEventListener('click', () => {
    toggle.setAttribute('aria-expanded', 'false');
    drawer.hidden = true;
  });
  drawer.addEventListener('click', (e) => {
    if (e.target === drawer){ // click backdrop
      toggle.setAttribute('aria-expanded', 'false');
      drawer.hidden = true;
    }
  });
}

// Theme toggle
const toggleBtn = document.getElementById('theme-toggle');
if (toggleBtn){
  toggleBtn.addEventListener('click', () => {
    const light = document.documentElement.classList.toggle('light');
    toggleBtn.setAttribute('aria-pressed', String(light));
  });
}

// Year
document.getElementById('year').textContent = new Date().getFullYear();
