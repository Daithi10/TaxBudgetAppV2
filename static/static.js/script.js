document.addEventListener('DOMContentLoaded', function () {
  console.log("JavaScript is connected");

  // === 1. Hamburger menu toggle ===
  const hamburger = document.querySelector('.hamburger');
  const menu = document.querySelector('.navbar ul');

  if (hamburger && menu) {
    hamburger.addEventListener('click', function () {
      menu.classList.toggle('active');
    });
  }

  // === 2. Show/hide children details ===
  const hasChildrenCheckbox = document.querySelector('#has_children');
  const childrenDetails = document.querySelector('#children_details');

  if (hasChildrenCheckbox && childrenDetails) {
    childrenDetails.style.display = hasChildrenCheckbox.checked ? 'block' : 'none';

    hasChildrenCheckbox.addEventListener('change', function () {
      childrenDetails.style.display = this.checked ? 'block' : 'none';
    });
  }

  // === 3. Budget savings slider ===
  const savingsSlider = document.querySelector('#savings_percent');
  const savingsLabel = document.querySelector('#savings_label');
  const residualInput = document.querySelector('#residual_income');
  const savingsResult = document.querySelector('#savings_result');

  if (savingsSlider && savingsLabel && savingsResult && residualInput) {
    savingsSlider.addEventListener('input', function () {
      const percent = parseInt(this.value);
      savingsLabel.textContent = `${percent}%`;

      const residual = parseFloat(residualInput.value);
      if (!isNaN(residual)) {
        const savedAmount = (residual * percent / 100).toFixed(2);
        savingsResult.textContent = `You could save approximately €${savedAmount} per month.`;
      }
    });
  }

  // === 4. Registration form validation ===
  const form = document.querySelector('form');
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm_password');

  if (form && email && password && confirmPassword) {
    form.addEventListener('submit', function (e) {
      if (password.value !== confirmPassword.value) {
        e.preventDefault();
        alert("Passwords do not match.");
        return;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email.value)) {
        e.preventDefault();
        alert("Please enter a valid email address.");
        return;
      }
    });
  }

  // === 5. Contact form validation ===
  const contactForm = document.querySelector('.contact-form');

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      const name = contactForm.querySelector('#name');
      const email = contactForm.querySelector('#email');
      const message = contactForm.querySelector('#message');

      if (!name.value.trim() || !email.value.trim() || !message.value.trim()) {
        e.preventDefault();
        alert("Please fill in all the fields.");
        return;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email.value)) {
        e.preventDefault();
        alert("Please enter a valid email address.");
        return;
      }
    });
  }
});
