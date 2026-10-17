#!/usr/bin/env python3
"""Reconstruct a UTC timeline from synthetic DFIR evidence."""

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CASE_DIR = PROJECT_DIR / "case-001"
EVIDENCE_DIR = CASE_DIR / "evidence-original"
OUTPUT_DIR = CASE_DIR / "output"

TIMESTAMP_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T"
    r"\d{2}:\d{2}:\d{2}Z)\s+(?P<details>.+)$"
)

EVIDENCE_FILES = ("auth.log", "process.log", "network.log")


def parse_evidence_file(path):
    """Parse events while retaining their source and line number."""
    events = []

    with path.open("r", encoding="utf-8") as evidence:
        for line_number, raw_line in enumerate(evidence, start=1):
            line = raw_line.strip()

            if not line:
                continue

            match = TIMESTAMP_PATTERN.match(line)
            if not match:
                raise ValueError(
                    f"Unrecognized record in {path.name}, "
                    f"line {line_number}: {line}"
                )

            timestamp = datetime.strptime(
                match.group("timestamp"), "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)

            events.append({
                "timestamp_utc": timestamp.isoformat(),
                "source": path.name,
                "source_line": line_number,
                "event_details": match.group("details"),
            })

    return events


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_events = []

    for filename in EVIDENCE_FILES:
        evidence_path = EVIDENCE_DIR / filename

        if not evidence_path.is_file():
            raise FileNotFoundError(
                f"Missing evidence file: {evidence_path}"
            )

        all_events.extend(parse_evidence_file(evidence_path))

    all_events.sort(
        key=lambda event: (
            event["timestamp_utc"],
            event["source"],
            event["source_line"],
        )
    )

    json_path = OUTPUT_DIR / "timeline.json"
    csv_path = OUTPUT_DIR / "timeline.csv"

    with json_path.open("w", encoding="utf-8") as output:
        json.dump(all_events, output, indent=2)
        output.write("\n")

    with csv_path.open("w", newline="", encoding="utf-8") as output:
        fields = [
            "timestamp_utc", "source", "source_line", "event_details"
        ]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_events)

    print(f"Case: DFIR-2026-001")
    print(f"Events reconstructed: {len(all_events)}")
    print("\nCHRONOLOGICAL TIMELINE (UTC)")
    print("=" * 100)

    for event in all_events:
        print(
            f"{event['timestamp_utc']} | "
            f"{event['source']}:{event['source_line']} | "
            f"{event['event_details']}"
        )

    print(f"\nJSON report: {json_path}")
    print(f"CSV report:  {csv_path}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Timeline reconstruction failed: {error}")
