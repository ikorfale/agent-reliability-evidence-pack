#!/usr/bin/env python3
"""Contract checks for the shipped reference artifact and inactive payment state."""

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

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta":
            for key in ("name", "property"):
                if key in values and "content" in values:
                    self.meta[(key, values[key])] = values["content"]


class OfferContractTest(unittest.TestCase):
    def test_active_intake_moves_to_bemjamin_catalog(self):
        config = (ROOT / ".github/ISSUE_TEMPLATE/config.yml").read_text()
        self.assertIn("ikorfale/bemjamin-site/issues/new", config)
        self.assertIn("Payment is inactive", config)
        self.assertFalse((ROOT / ".github/ISSUE_TEMPLATE/reliability-pack.md").exists())
        self.assertTrue((ROOT / "docs/historical-intake/reliability-pack.md").exists())
        self.assertTrue((ROOT / "docs/historical-intake/private-scope-contact.md").exists())

    def test_machine_status_fails_closed_on_payment(self):
        offer = json.loads((ROOT / "offer.json").read_text())
        self.assertEqual(offer["status"], "reference_artifact_intake_moved_payment_inactive")
        self.assertFalse(offer["activeOffer"])
        self.assertFalse(offer["payment"]["acceptingFunds"])
        self.assertIsNone(offer["payment"]["address"])
        self.assertEqual(offer["payment"]["intendedNetwork"], "Solana")
        self.assertEqual(offer["payment"]["intendedAssets"], ["USDC", "USDT"])
        self.assertEqual(offer["historical"]["originalProvider"], "Banantiy")
        self.assertEqual(offer["historical"]["originalPilotPriceUsd"], 25)

    def test_public_page_is_proof_not_checkout(self):
        page = (ROOT / "index.html").read_text()
        lowered = page.lower()
        self.assertIn("shipped reference", lowered)
        self.assertIn("payment inactive", lowered)
        self.assertIn("no funds are accepted", lowered)
        self.assertIn("originally published by banantiy", lowered)
        self.assertIn("maintained by bemjamin", lowered)
        self.assertIn("bemjamin-site.vercel.app/#services", page)
        self.assertNotIn("request a $25 pack", lowered)
        self.assertNotIn("verify, then pay", lowered)

    def test_public_metadata_uses_canonical_avatar(self):
        parser = MetadataParser()
        parser.feed((ROOT / "index.html").read_text())
        self.assertIn("public proof", parser.meta[("property", "og:title")].lower())
        self.assertTrue(parser.meta[("property", "og:image")].endswith("/bemjamin-avatar-256.png"))
        self.assertEqual((ROOT / "bemjamin-avatar-256.png").stat().st_size, 156160)

    def test_reference_scope_remains_bounded(self):
        offer = json.loads((ROOT / "offer.json").read_text())
        self.assertEqual(offer["referenceScope"]["workflowCount"], 1)
        self.assertEqual(offer["referenceScope"]["primaryQuestionCount"], 1)
        self.assertTrue(any("bounded negative result" in item for item in offer["referenceScope"]["deliverables"]))
        serialized = json.dumps(offer).lower()
        for phrase in ("credential", "malware", "surveillance", "guarantees"):
            self.assertIn(phrase, serialized)

    def test_browser_telemetry_has_no_storage_or_event_sink(self):
        script = (ROOT / "assets/funnel.js").read_text()
        self.assertIn('credentials: "omit"', script)
        for forbidden in ("document.cookie", "localStorage", "sessionStorage", "sendBeacon", "XMLHttpRequest"):
            self.assertNotIn(forbidden, script)

    def test_telemetry_snapshot_has_only_aggregate_fields(self):
        snapshot = json.loads((ROOT / "telemetry/funnel.json").read_text())
        self.assertEqual(set(snapshot), {"schemaVersion", "generatedAt", "repository", "source", "excludedLabel", "counts"})
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
