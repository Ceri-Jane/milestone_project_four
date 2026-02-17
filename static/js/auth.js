/* jshint esversion: 8 */

/* ============================================================
   PASSWORD VISIBILITY TOGGLE
============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  const toggles = document.querySelectorAll(".toggle-password-btn");

  toggles.forEach((btn) => {
    const targetId = btn.dataset.target;
    const input = document.getElementById(targetId);

    if (!input) return;

    btn.addEventListener("click", () => {
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";

      btn.classList.toggle("is-visible", isPassword);
      btn.setAttribute(
        "aria-label",
        isPassword ? "Hide password" : "Show password"
      );
    });
  });
});