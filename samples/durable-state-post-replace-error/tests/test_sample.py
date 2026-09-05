#!/usr/bin/env python3
"""Reproduce the baseline failure and verify the bounded patch."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SAMPLE = Path(__file__).resolve().parents[1]
UPSTREAM = SAMPLE / "fixture" / "upstream" / "durable_state.py"
PATCH = SAMPLE / "patches" / "classify-post-replace-errors.patch"
EXPECTED_SHA256 = "118fe51f71916158eb48bffc6d1d910f44155251950e8a6d6dce9c1e1e27d37e"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trigger(module, directory: Path):
    destination = directory / "state.json"
    destination.write_bytes(b"old\n")

    def fail(point: str) -> None:
        if point == "after-replace":
            raise RuntimeError("injected post-replace failure")

    caught = None
    try:
        module.durable_replace(destination, b"new\n", hook=fail)
    except Exception as error:  # evidence captures the exact exported type
        caught = error
    return caught, destination.read_bytes()


class SampleEvidenceTest(unittest.TestCase):
    def test_vendored_source_matches_public_v0_4_0(self):
        digest = hashlib.sha256(UPSTREAM.read_bytes()).hexdigest()
        self.assertEqual(digest, EXPECTED_SHA256)

    def test_public_v0_4_0_reports_ordinary_error_after_publication(self):
        module = load_module(UPSTREAM, "durable_state_v040")
        with tempfile.TemporaryDirectory() as directory:
            error, contents = trigger(module, Path(directory))
        self.assertIs(type(error), RuntimeError)
        self.assertEqual(str(error), "injected post-replace failure")
        self.assertEqual(contents, b"new\n")

    def test_patch_classifies_the_post_replace_outcome(self):
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            shutil.copy2(UPSTREAM, checkout / "durable_state.py")
            completed = subprocess.run(
                ["git", "apply", "--check", str(PATCH)], cwd=checkout,
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            subprocess.run(["git", "apply", str(PATCH)], cwd=checkout, check=True)
            module = load_module(checkout / "durable_state.py", "durable_state_patched")
            error, contents = trigger(module, checkout)
        self.assertIs(type(error), module.ReplacementPublishedError)
        self.assertIs(type(error.__cause__), RuntimeError)
        self.assertEqual(contents, b"new\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
