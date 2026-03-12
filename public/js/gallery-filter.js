document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.gallery-filter');
  const items = document.querySelectorAll('.gallery-item');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;

      // Update active button styles
      buttons.forEach(btn => {
        btn.classList.remove('border-gold-dark', 'text-gold-dark');
        btn.classList.add('border-gray-300', 'text-gray-600');
        btn.setAttribute('aria-pressed', 'false');
      });
      button.classList.remove('border-gray-300', 'text-gray-600');
      button.classList.add('border-gold-dark', 'text-gold-dark');
      button.setAttribute('aria-pressed', 'true');

      // Filter items
      items.forEach(item => {
        if (filter === 'all' || item.dataset.service === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
});
