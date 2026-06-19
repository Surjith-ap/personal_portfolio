/**
 * contact.js
 * Progressively enhanced async form submission.
 * Falls back to normal POST if JS is unavailable.
 */

document.addEventListener("DOMContentLoaded", () => {

  const form       = document.getElementById("contact-form");
  const submitBtn  = document.getElementById("submit-btn");
  const feedback   = document.getElementById("form-feedback");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Validate form before submission
    if (!form.checkValidity()) {
      feedback.textContent = "Please fill in all required fields correctly.";
      feedback.className = "form-feedback form-feedback--error";
      feedback.hidden = false;
      return;
    }

    const label   = submitBtn.querySelector(".btn__label");
    const loading = submitBtn.querySelector(".btn__loading");

    // ── Show loading state ─────────────────────────────────
    submitBtn.disabled = true;
    label.hidden   = true;
    loading.hidden = false;
    feedback.hidden = true;

    try {
      const data = new FormData(form);

      const res = await fetch(form.action, {
        method: "POST",
        body: data,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      // Flask redirects on success → res.url will differ from current page
      // We rely on the redirected response containing a flash message,
      // but for async we just check status and show inline feedback.
      if (res.ok) {
        showFeedback("✓ Message sent! I'll get back to you soon.", "success");
        form.reset();
      } else {
        showFeedback("Something went wrong. Please try again.", "error");
      }
    } catch {
      showFeedback("Network error — please check your connection and try again.", "error");
    } finally {
      submitBtn.disabled = false;
      label.hidden   = false;
      loading.hidden = true;
    }
  });

  function showFeedback(message, type) {
    feedback.textContent = message;
    feedback.className   = `form-feedback form-feedback--${type}`;
    feedback.hidden      = false;

    // Scroll into view on mobile
    feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });

    // Auto-hide success after 6 s
    if (type === "success") {
      setTimeout(() => { feedback.hidden = true; }, 6000);
    }
  }

});
