# P7 — Digital Forensics & Incident Response (DFIR)

A Python-based digital forensics training project that verifies evidence
integrity, reconstructs event timelines, exports reports, and documents
incident findings using synthetic Linux logs.

## Objectives

- Verify evidence files using SHA-256 hashes.
- Reconstruct a chronological UTC timeline.
- Preserve source filenames and line numbers.
- Export events to JSON and CSV.
- Test malformed log records and invalid dates.
- Document findings, confidence, limitations, and response recommendations.

## Project structure

- `case-001/evidence-original/` — original synthetic evidence
- `case-001/evidence-working/` — working evidence area
- `case-001/analysis/` — forensic findings report
- `case-001/output/` — hashes and timeline reports
- `scripts/` — timeline reconstruction code
- `tests/` — automated unit tests

## Requirements

Python 3. No third-party packages are required.

## Run from the project root

Generate the timeline:

    python3 scripts/timeline_reconstruction.py

Run the unit tests:

    python3 -m unittest discover -s tests -v

Verify the original evidence:

    cd case-001
    sha256sum --check output/evidence-manifest.sha256

## Outputs

- `case-001/output/evidence-manifest.sha256`
- `case-001/output/timeline.json`
- `case-001/output/timeline.csv`
- `case-001/analysis/incident-findings.md`

## Evidence integrity and limitations

SHA-256 verification detects changes relative to the saved manifest.
It does not independently establish evidence authenticity or chain of custody.

This project uses fictional training logs and documentation-range IP addresses.
The event sequence does not, by itself, prove a real compromise, malicious
activity, or data exfiltration. Process-to-network relationships require
independent corroboration.

## Skills demonstrated

Python log parsing, timestamp normalization, chronological event reconstruction,
SHA-256 integrity verification, JSON/CSV reporting, unit testing, and forensic
documentation.
