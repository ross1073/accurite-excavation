// Mobile menu toggle
(function () {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  const hamburger = document.getElementById('hamburger-icon');
  const closeIcon = document.getElementById('close-icon');

  if (!btn || !menu) return;

  let isOpen = false;

  function open() {
    isOpen = true;
    menu.classList.remove('hidden');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', 'Close navigation menu');
    hamburger.classList.add('hidden');
    closeIcon.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    isOpen = false;
    menu.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', 'Open navigation menu');
    hamburger.classList.remove('hidden');
    closeIcon.classList.add('hidden');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', function () {
    isOpen ? close() : open();
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen) {
      close();
      btn.focus();
    }
  });

  // Close when clicking a link inside the menu
  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', close);
  });
})();
