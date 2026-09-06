"use strict";

const form = document.querySelector("[data-fit-check]");

if (form) {
  const result = form.querySelector("[data-fit-result]");
  const next = form.querySelector("[data-fit-next]");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const checks = [...form.querySelectorAll('input[type="checkbox"]')];
    const selected = checks.filter((check) => check.checked).length;
    const ready = selected === checks.length;

    result.dataset.ready = String(ready);
    result.textContent = ready
      ? "Likely fixed-scope fit: all three boundaries are present."
      : `Not ready to scope yet: ${selected} of ${checks.length} boundaries are present.`;
    next.hidden = !ready;
  });
}
