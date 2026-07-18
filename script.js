// ===== Nav background on scroll =====
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('is-scrolled', window.scrollY > 20);
});

// ===== Scroll reveal =====
const revealEls = document.querySelectorAll('.reveal');

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

revealEls.forEach((el) => revealObserver.observe(el));

// ===== Work filters =====
const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.card');

filters.forEach((btn) => {
  btn.addEventListener('click', () => {
    filters.forEach((b) => b.classList.remove('is-active'));
    btn.classList.add('is-active');

    const target = btn.dataset.filter;
    cards.forEach((card) => {
      const match = target === 'all' || card.dataset.tag === target;
      card.classList.toggle('is-hidden', !match);
    });
  });
});

// ===== Footer year =====
document.getElementById('year').textContent = new Date().getFullYear();
