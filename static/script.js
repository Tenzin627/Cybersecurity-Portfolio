/**
 * Cybersecurity Portfolio — client-side behavior.
 *
 * Covers: mobile navigation, smooth scrolling, dark/light theme (persisted
 * with localStorage), project filtering, and contact form validation.
 * No external libraries.
 */

document.addEventListener("DOMContentLoaded", () => {
  setYear();
  setupMobileNav();
  setupSmoothScroll();
  setupThemeToggle();
  setupProjectFilter();
  setupContactForm();
});

/* -------------------------------------------------------------------- */
/* Footer year                                                          */
/* -------------------------------------------------------------------- */

function setYear() {
  const yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
}

/* -------------------------------------------------------------------- */
/* Mobile navigation                                                    */
/* -------------------------------------------------------------------- */

function setupMobileNav() {
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");
  if (!navToggle || !navLinks) return;

  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Close the menu after tapping a link (mobile UX).
  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* -------------------------------------------------------------------- */
/* Smooth scrolling for in-page anchor links                            */
/* -------------------------------------------------------------------- */

function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetId = link.getAttribute("href");
      if (!targetId || targetId === "#") return;

      const target = document.querySelector(targetId);
      if (!target) return;

      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

/* -------------------------------------------------------------------- */
/* Theme toggle (dark / light) with localStorage persistence            */
/* -------------------------------------------------------------------- */

function setupThemeToggle() {
  const toggleBtn = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");
  const themeLabel = document.getElementById("themeLabel");
  const body = document.body;

  const savedTheme = localStorage.getItem("theme");
  const preferredTheme = savedTheme === "light" || savedTheme === "dark"
    ? savedTheme
    : "dark";

  applyTheme(preferredTheme);

  toggleBtn.addEventListener("click", () => {
    const currentTheme = body.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    localStorage.setItem("theme", nextTheme);
  });

  function applyTheme(theme) {
    body.setAttribute("data-theme", theme);
    const isDark = theme === "dark";
    themeIcon.textContent = isDark ? "\u263D" : "\u2600";
    themeLabel.textContent = isDark ? "Dark" : "Light";
    toggleBtn.setAttribute(
      "aria-label",
      isDark ? "Switch to light theme" : "Switch to dark theme"
    );
  }
}

/* -------------------------------------------------------------------- */
/* Project filtering                                                    */
/* -------------------------------------------------------------------- */

function setupProjectFilter() {
  const filterBar = document.getElementById("filterBar");
  const projectGrid = document.getElementById("projectGrid");
  if (!filterBar || !projectGrid) return;

  const filterButtons = filterBar.querySelectorAll(".filter-btn");
  const projectCards = projectGrid.querySelectorAll(".project-card");

  filterBar.addEventListener("click", (event) => {
    const button = event.target.closest(".filter-btn");
    if (!button) return;

    const selectedFilter = button.dataset.filter;

    filterButtons.forEach((btn) => {
      const isActive = btn === button;
      btn.classList.toggle("is-active", isActive);
      btn.setAttribute("aria-selected", String(isActive));
    });

    projectCards.forEach((card) => {
      const matches = selectedFilter === "all" || card.dataset.category === selectedFilter;
      card.classList.toggle("is-hidden", !matches);
    });
  });
}

/* -------------------------------------------------------------------- */
/* Contact form: client-side validation + submission                    */
/* -------------------------------------------------------------------- */

function setupContactForm() {
  const form = document.getElementById("contactForm");
  if (!form) return;

  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const messageInput = document.getElementById("message");
  const submitBtn = document.getElementById("submitBtn");
  const formStatus = document.getElementById("formStatus");

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const isValid = validateForm();
    if (!isValid) return;

    setSubmitting(true);
    clearStatus();

    try {
      const formData = new FormData(form);
      const response = await fetch("/contact", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showStatus(result.message, "success");
        form.reset();
      } else {
        showStatus(result.message || "Something went wrong. Please try again.", "error");
      }
    } catch (error) {
      showStatus("Network error. Please check your connection and try again.", "error");
    } finally {
      setSubmitting(false);
    }
  });

  function validateForm() {
    let isValid = true;

    isValid = validateField(
      nameInput,
      "nameError",
      nameInput.value.trim().length > 0,
      "Please enter your name."
    ) && isValid;

    isValid = validateField(
      emailInput,
      "emailError",
      emailPattern.test(emailInput.value.trim()),
      "Please enter a valid email address."
    ) && isValid;

    isValid = validateField(
      messageInput,
      "messageError",
      messageInput.value.trim().length > 0,
      "Please enter a message."
    ) && isValid;

    return isValid;
  }

  function validateField(input, errorId, condition, errorMessage) {
    const errorEl = document.getElementById(errorId);
    const row = input.closest(".form-row");

    if (condition) {
      row.classList.remove("has-error");
      errorEl.textContent = "";
      return true;
    }

    row.classList.add("has-error");
    errorEl.textContent = errorMessage;
    return false;
  }

  function setSubmitting(isSubmitting) {
    submitBtn.disabled = isSubmitting;
    submitBtn.textContent = isSubmitting ? "Sending..." : "Send Message";
  }

  function showStatus(message, type) {
    formStatus.textContent = message;
    formStatus.className = "form-status " + (type === "success" ? "is-success" : "is-error");
  }

  function clearStatus() {
    formStatus.textContent = "";
    formStatus.className = "form-status";
  }
}
