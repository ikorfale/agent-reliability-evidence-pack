#!/usr/bin/env python3
"""Contract checks for public intake, privacy language, and aggregate telemetry."""

from __future__ import annotations

import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta: dict[tuple[str, str], str] = {}
        self.canonical: str | None = None
        self.json_ld: list[str] = []
        self._in_json_ld = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta":
            for key in ("name", "property"):
                if key in values and "content" in values:
                    self.meta[(key, values[key])] = values["content"]
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True

    def handle_data(self, data):
        if self._in_json_ld:
            self.json_ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_json_ld:
            self._in_json_ld = False


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

    def test_detail_free_email_cta_is_prefilled_and_bounded(self):
        page = (ROOT / "index.html").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertGreaterEqual(
            page.count("body=I%20want%20a%20detail-free%20feasibility%20check."),
            3,
        )
        self.assertIn("fit/not-fit reply", page)
        self.assertIn("fit/not-fit reply", readme)
        self.assertIn("fit/not-fit reply within 1 UTC day", page)
        self.assertIn("fit/not-fit reply within 1 UTC", readme)
        self.assertIn("Do not add details until a safe disclosure path is agreed", page)

    def test_public_metadata_preserves_offer_scope_and_price(self):
        parser = MetadataParser()
        parser.feed((ROOT / "index.html").read_text())
        canonical = "https://agent-reliability-evidence-pack-rho.vercel.app/"
        self.assertEqual(parser.canonical, canonical)
        self.assertEqual(parser.meta[("property", "og:url")], canonical)
        self.assertIn("$25", parser.meta[("property", "og:title")])
        self.assertEqual(parser.meta[("name", "twitter:card")], "summary")
        structured = json.loads("".join(parser.json_ld))
        self.assertEqual(structured["@type"], "Service")
        self.assertEqual(structured["offers"]["price"], "25")
        self.assertEqual(structured["offers"]["priceCurrency"], "USD")

    def test_machine_readable_offer_matches_public_contract(self):
        offer = json.loads((ROOT / "offer.json").read_text())
        page = (ROOT / "index.html").read_text()
        self.assertEqual(offer["status"], "available")
        self.assertEqual(offer["price"]["amount"], 25)
        self.assertEqual(offer["price"]["currency"], "USD")
        self.assertEqual(offer["scope"]["workflowCount"], 1)
        self.assertEqual(offer["scope"]["defaultDeliveryTargetUtcDays"], 3)
        self.assertFalse(offer["response"]["initialContactCreatesObligation"])
        self.assertFalse(offer["privacy"]["credentialsAccepted"])
        self.assertFalse(offer["privacy"]["tracking"])
        self.assertIn('type="application/json" href="/offer.json"', page)
        serialized = json.dumps(offer).lower()
        for forbidden in ("private key", "seed phrase", "0xba51", "bc1q", "3idb6"):
            self.assertNotIn(forbidden, serialized)

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

    def test_fit_check_is_local_only_and_routes_to_existing_offer(self):
        page = (ROOT / "index.html").read_text()
        script = (ROOT / "assets/fit-check.js").read_text()
        self.assertIn("60-second private fit check", page)
        self.assertIn("sends, stores, and records nothing", page)
        self.assertEqual(page.count('name="inspectable"'), 1)
        self.assertEqual(page.count('name="boundary"'), 1)
        self.assertEqual(page.count('name="observable"'), 1)
        self.assertIn("event.preventDefault()", script)
        self.assertIn("Likely fixed-scope fit", script)
        for forbidden in (
            "fetch(",
            "XMLHttpRequest",
            "sendBeacon",
            "document.cookie",
            "localStorage",
            "sessionStorage",
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
