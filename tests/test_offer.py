#!/usr/bin/env python3
"""Contract checks for public intake, privacy language, and aggregate telemetry."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OfferContractTest(unittest.TestCase):
    def test_intake_templates_are_sanitized_and_labeled(self):
        request = (ROOT / ".github/ISSUE_TEMPLATE/reliability-pack.md").read_text()
        private = (ROOT / ".github/ISSUE_TEMPLATE/private-scope-contact.md").read_text()
        self.assertIn("labels: request", request)
        self.assertIn("safe to publish permanently", request)
        self.assertIn("Smallest safe trigger or synthetic/redacted trace", request)
        self.assertIn("labels: request, private-scope", private)
        self.assertIn("posted no private request content", private)
        self.assertNotIn("**What must remain private:**", request)

    def test_offer_states_privacy_and_refusal_contract(self):
        combined = "\n".join([
            (ROOT / "README.md").read_text(),
            (ROOT / "index.html").read_text(),
        ]).lower()
        for phrase in (
            "credentials and production dumps are never accepted",
            "private request content",
            "unsafe production",
            "refuse",
            "no cookies",
            "fingerprinting",
        ):
            self.assertIn(phrase, combined)

    def test_browser_telemetry_has_no_storage_or_event_sink(self):
        script = (ROOT / "assets/funnel.js").read_text()
        self.assertIn('credentials: "omit"', script)
        for forbidden in (
            "document.cookie",
            "localStorage",
            "sessionStorage",
            "sendBeacon",
            "XMLHttpRequest",
        ):
            self.assertNotIn(forbidden, script)

    def test_telemetry_snapshot_has_only_aggregate_fields(self):
        snapshot = json.loads((ROOT / "telemetry/funnel.json").read_text())
        self.assertEqual(
            set(snapshot),
            {"schemaVersion", "generatedAt", "repository", "source", "excludedLabel", "counts"},
        )
        self.assertEqual(set(snapshot["counts"]), {"requests", "scopesAccepted", "delivered"})
        self.assertTrue(all(type(value) is int and value >= 0 for value in snapshot["counts"].values()))

    def test_snapshot_builder_rejects_invalid_or_extra_data(self):
        path = ROOT / "tools/update_funnel.py"
        spec = importlib.util.spec_from_file_location("update_funnel", path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        valid = {"requests": 1, "scopesAccepted": 0, "delivered": 0}
        self.assertEqual(module.build_snapshot(valid, "2026-09-05T00:00:00Z")["counts"], valid)
        with self.assertRaises(ValueError):
            module.build_snapshot({**valid, "requestBody": 1}, "2026-09-05T00:00:00Z")
        with self.assertRaises(ValueError):
            module.build_snapshot(
                {"requests": 0, "scopesAccepted": 1, "delivered": 0},
                "2026-09-05T00:00:00Z",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
