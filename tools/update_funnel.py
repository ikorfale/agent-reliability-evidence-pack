#!/usr/bin/env python3
"""Refresh checked-in aggregate funnel counts without fetching issue content."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import subprocess

REPOSITORY = "ikorfale/agent-reliability-evidence-pack"
EXCLUDED_LABEL = "telemetry-test"
OUTPUT = Path(__file__).resolve().parents[1] / "telemetry" / "funnel.json"
STAGES = {
    "requests": "request",
    "scopesAccepted": "scope-accepted",
    "delivered": "delivered",
}
QUERY = """query($queryString: String!) {
  search(query: $queryString, type: ISSUE, first: 1) { issueCount }
}"""


def public_issue_count(label: str) -> int:
    search = (
        f"repo:{REPOSITORY} is:issue label:{label} "
        f"-label:{EXCLUDED_LABEL}"
    )
    completed = subprocess.run(
        [
            "gh", "api", "graphql",
            "-f", f"query={QUERY}",
            "-F", f"queryString={search}",
            "--jq", ".data.search.issueCount",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(completed.stdout.strip())


def build_snapshot(counts: dict[str, int], generated_at: str) -> dict[str, object]:
    if set(counts) != set(STAGES) or any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in counts.values()
    ):
        raise ValueError("funnel counts must be non-negative integers for every stage")
    if not counts["delivered"] <= counts["scopesAccepted"] <= counts["requests"]:
        raise ValueError("funnel labels must remain cumulative stage subsets")
    return {
        "schemaVersion": 1,
        "generatedAt": generated_at,
        "repository": REPOSITORY,
        "source": "GitHub public issueCount by label",
        "excludedLabel": EXCLUDED_LABEL,
        "counts": counts,
    }


def main() -> None:
    counts = {name: public_issue_count(label) for name, label in STAGES.items()}
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    snapshot = build_snapshot(counts, generated_at.replace("+00:00", "Z"))
    OUTPUT.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {counts}")


if __name__ == "__main__":
    main()
