"use strict";

fetch("/telemetry/funnel.json", { cache: "no-store", credentials: "omit" })
  .then((response) => {
    if (!response.ok) throw new Error(`telemetry snapshot: ${response.status}`);
    return response.json();
  })
  .then((snapshot) => {
    const fields = {
      requests: snapshot.counts.requests,
      scopesAccepted: snapshot.counts.scopesAccepted,
      delivered: snapshot.counts.delivered,
    };
    for (const [name, value] of Object.entries(fields)) {
      if (!Number.isSafeInteger(value) || value < 0) throw new Error("invalid count");
      document.querySelector(`[data-funnel="${name}"]`).textContent = String(value);
    }
    document.querySelector("[data-funnel-updated]").textContent =
      `Snapshot refreshed ${snapshot.generatedAt}.`;
  })
  .catch(() => {
    document.querySelector("[data-funnel-updated]").textContent =
      "Snapshot unavailable; audit the public label links below.";
  });
