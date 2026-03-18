(function() {
  if (!sessionStorage.getItem('landing_page')) {
    sessionStorage.setItem('landing_page', window.location.href);
  }

  document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('[data-contact-form]');
    forms.forEach(initForm);
  });

  function initForm(form) {
    var params = new URLSearchParams(window.location.search);
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(function(key) {
      var field = form.querySelector('[name="' + key + '"]');
      if (field && params.get(key)) field.value = params.get(key);
    });
    ['gclid','gbraid','wbraid','gad_source'].forEach(function(key) {
      var field = form.querySelector('[name="' + key + '"]');
      if (field && params.get(key)) field.value = params.get(key);
    });
    var pageUrl = form.querySelector('[name="page_url"]');
    if (pageUrl) pageUrl.value = window.location.href;
    var pageReferrer = form.querySelector('[name="page_referrer"]');
    if (pageReferrer) pageReferrer.value = document.referrer;
    var landingPage = form.querySelector('[name="landing_page"]');
    if (landingPage) landingPage.value = sessionStorage.getItem('landing_page') || '';

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var honeypot = form.querySelector('[name="website"]');
      if (honeypot && honeypot.value) return;
      var submitBtn = form.querySelector('[type="submit"]');
      var originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
      var formData = new FormData(form);
      var data = {};
      formData.forEach(function(value, key) { if (key !== 'website') data[key] = value; });
      var webhookUrl = form.dataset.webhookUrl;
      fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      .then(function(response) {
        if (!response.ok) throw new Error('Network response was not ok');
        var formContainer = form.closest('[data-form-container]');
        formContainer.innerHTML = '<div class="text-center py-8"><div class="text-2xl font-bold text-green-700 mb-2">Thank You!</div><p class="text-gray-600">We\'ll be in touch within one business day. For immediate assistance, call <a href="tel:+18018146975" class="text-gold-dark font-semibold hover:underline">(801) 814-6975</a>.</p></div>';
      })
      .catch(function() {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        var errorDiv = form.querySelector('[data-form-error]');
        if (errorDiv) {
          errorDiv.textContent = 'Something went wrong. Please try again or call us directly.';
          errorDiv.classList.remove('hidden');
        }
      });
    });
  }
})();
