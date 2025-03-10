document.querySelectorAll('.custom-input').forEach(input => {
  const placeholderText = input.getAttribute('data-placeholder') || 'Enter text...';

  input.textContent = placeholderText;
  input.style.color = '#888';

  input.addEventListener('focus', () => {
    if (input.textContent === placeholderText) {
      input.textContent = '';
      input.style.color = 'black';
    }
  });

  input.addEventListener('blur', () => {
    if (!input.textContent.trim()) {
      input.textContent = placeholderText;
      input.style.color = '#888';
    }
  });
});