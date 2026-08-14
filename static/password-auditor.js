/*
  Personal Password Auditor - Frontend logic

  PRIVACY / SECURITY NOTE:
  The password entered by the user NEVER leaves this file as plaintext.
  It is hashed locally with SHA-1 using the browser's built-in
  Web Crypto API (crypto.subtle). Only the first 5 characters of that
  hash (the k-anonymity "prefix") are sent to our backend, which forwards
  them to HIBP. The remaining hash suffix is compared locally, in the
  browser, against the list HIBP returns. The full password and full
  hash never travel over the network and are never stored anywhere.
*/

// ---- Element references ----
const form = document.getElementById("password-form");
const passwordInput = document.getElementById("password-input");
const toggleButton = document.getElementById("toggle-visibility");
const clearButton = document.getElementById("clear-button");
const checkButton = document.getElementById("check-button");
const loadingMessage = document.getElementById("loading-message");
const resultContainer = document.getElementById("result-container");
const errorContainer = document.getElementById("error-container");
const strengthBarFill = document.getElementById("strength-bar-fill");
const strengthLabel = document.getElementById("strength-meter");

// ---- Password visibility toggle ----
toggleButton.addEventListener("click", () => {
  const isHidden = passwordInput.type === "password";
  passwordInput.type = isHidden ? "text" : "password";
  toggleButton.textContent = isHidden ? "Hide" : "Show";
  toggleButton.setAttribute("aria-pressed", String(isHidden));
  toggleButton.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
});

// ---- Clear / reset ----
clearButton.addEventListener("click", () => {
  resetForm();
});

function resetForm() {
  form.reset();
  passwordInput.type = "password";
  toggleButton.textContent = "Show";
  toggleButton.setAttribute("aria-pressed", "false");
  hide(resultContainer);
  hide(errorContainer);
  hide(loadingMessage);
  updateStrengthMeter("");
  passwordInput.focus();
}

// ---- Live password strength meter ----
passwordInput.addEventListener("input", () => {
  updateStrengthMeter(passwordInput.value);
});

function updateStrengthMeter(password) {
  if (!password) {
    strengthBarFill.style.width = "0%";
    strengthBarFill.style.background = "var(--danger)";
    strengthLabel.textContent = "Strength: —";
    return;
  }

  const score = calculatePasswordStrength(password);
  const percentages = [20, 40, 60, 80, 100];
  const labels = ["Very weak", "Weak", "Fair", "Good", "Strong"];
  const colors = ["#ff5c5c", "#ff5c5c", "#ffb454", "#3ddc97", "#3ddc97"];

  const index = Math.min(score, 4);
  strengthBarFill.style.width = percentages[index] + "%";
  strengthBarFill.style.background = colors[index];
  strengthLabel.textContent = `Strength: ${labels[index]} (this is a basic estimate only)`;
}

/**
 * Very simple, transparent strength heuristic.
 * This is NOT a substitute for a breach check and is not a guarantee
 * of security - it only rewards length and character variety.
 */
function calculatePasswordStrength(password) {
  let score = 0;

  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  // Normalize the raw 0-6 score down to a 0-4 index range.
  return Math.min(4, Math.floor((score / 6) * 4) + (score >= 5 ? 1 : 0));
}

// ---- SHA-1 hashing using the Web Crypto API ----
async function sha1Hex(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-1", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("").toUpperCase();
}

// ---- Form submission: run the k-anonymity breach check ----
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const password = passwordInput.value;

  hide(resultContainer);
  hide(errorContainer);

  if (!password) {
    showError("Please enter a password to check.");
    return;
  }

  setLoading(true);

  try {
    // Step 1: hash locally. The plaintext password is used only here,
    // in memory, and is discarded once this function scope ends.
    const fullHash = await sha1Hex(password);
    const prefix = fullHash.slice(0, 5);
    const suffix = fullHash.slice(5);

    // Step 2: ask our backend for all suffixes matching this prefix.
    // Note: only the 5-character prefix is transmitted - never the
    // full hash and never the password.
    const response = await fetch(`/api/check/${prefix}`);

    if (!response.ok) {
      const errorBody = await safeJson(response);
      throw new Error(errorBody?.error || "The breach-check service returned an error.");
    }

    const data = await response.json();

    // Step 3: compare the suffix locally, in the browser.
    const matchCount = findMatchCount(data.suffixes, suffix);

    displayResult(matchCount);
  } catch (err) {
    showError(err.message || "Something went wrong while checking this password. Please try again.");
  } finally {
    setLoading(false);
  }
});

/**
 * Parses the "SUFFIX:COUNT" lines HIBP returns and looks for our
 * specific suffix. Returns the breach count, or 0 if no match is found.
 */
function findMatchCount(suffixesText, targetSuffix) {
  if (!suffixesText) return 0;

  const lines = suffixesText.split("\n");
  for (const line of lines) {
    const [lineSuffix, countStr] = line.trim().split(":");
    if (lineSuffix === targetSuffix) {
      return parseInt(countStr, 10) || 0;
    }
  }
  return 0;
}

function displayResult(matchCount) {
  resultContainer.innerHTML = "";
  resultContainer.classList.remove("safe", "breached");

  if (matchCount > 0) {
    resultContainer.classList.add("breached");
    resultContainer.innerHTML = `
      <h2>⚠️ Password Found in Breach Data</h2>
      <p><strong>Exposure count:</strong> ${matchCount.toLocaleString()} times</p>
      <p>This password has appeared in known data breaches. Change it immediately
      and avoid reusing it anywhere else.</p>
    `;
  } else {
    resultContainer.classList.add("safe");
    resultContainer.innerHTML = `
      <h2>✅ No Breach Matches Found</h2>
      <p>Your password is hashed locally in your browser. Only the first five characters of the SHA-1 hash are sent to the server. This does not
      guarantee the password is secure — use a strong, unique password and a
      password manager regardless.</p>
    `;
  }

  show(resultContainer);
}

// ---- Helpers ----
function setLoading(isLoading) {
  checkButton.disabled = isLoading;
  clearButton.disabled = isLoading;
  if (isLoading) {
    show(loadingMessage);
  } else {
    hide(loadingMessage);
  }
}

function showError(message) {
  errorContainer.textContent = message;
  show(errorContainer);
}

function show(el) {
  el.hidden = false;
}

function hide(el) {
  el.hidden = true;
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}
