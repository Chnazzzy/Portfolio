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

const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.card');

filters.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;

    filters.forEach((btn) => btn.classList.toggle('is-active', btn === button));

    cards.forEach((card) => {
      const matches = filter === 'all' || card.dataset.tag === filter;
      card.classList.toggle('is-hidden', !matches);
    });
  });
});

document.getElementById('year').textContent = new Date().getFullYear();