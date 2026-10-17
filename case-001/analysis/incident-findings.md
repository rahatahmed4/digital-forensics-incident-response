# Digital Forensics Incident Findings

## Case information

- Case ID: DFIR-2026-001
- Case name: Simulated Linux Workstation Compromise
- Analyst: Rahat Ahmed
- Environment: Ubuntu VirtualBox lab
- Evidence type: Synthetic training artifacts
- Status: Open — further validation required

## 1. Executive summary

Three synthetic log files contain eight timestamped events between
09:14:03 and 09:19:15 UTC on 17 October 2026. The records show a successful
SSH login, a privileged command, a process start involving curl, outbound
connection records, a failed SSH login for an invalid user, and creation
of a file under /tmp.

These events warrant investigation in the fictional scenario. However,
the supplied logs alone do not establish that the workstation was
compromised, that the outbound connections were malicious, or that data
was exfiltrated.

## 2. Evidence reviewed

- evidence-original/auth.log
- evidence-original/process.log
- evidence-original/network.log
- output/evidence-manifest.sha256
- output/timeline.json
- output/timeline.csv

The SHA-256 manifest was checked against all three original log files.
All three integrity checks returned OK at the time of verification.

## 3. Reconstructed timeline

All timestamps below are UTC on 17 October 2026.

| Time | Source | Recorded event |
|---|---|---|
| 09:14:03 | auth.log:1 | SSH password login accepted for analyst from 203.0.113.77 |
| 09:16:41 | auth.log:2 | analyst ran /usr/bin/id through sudo |
| 09:17:05 | process.log:1 | Process event records /usr/bin/curl, PID 2501 |
| 09:17:08 | network.log:1 | Outbound connection record to 198.51.100.24:443, PID 2501 |
| 09:18:12 | auth.log:3 | Failed SSH password for invalid user backup from 203.0.113.77 |
| 09:18:30 | process.log:2 | File-creation event for /tmp/.cache-sync, PID 2518 |
| 09:19:02 | process.log:3 | Privileged command event records /usr/bin/id |
| 09:19:15 | network.log:2 | Outbound connection record to 198.51.100.24:443, PID 2518 |

## 4. Findings and confidence

### Finding 1 — Successful SSH login is recorded

- Evidence: auth.log:1
- Observation: A password-based SSH login for analyst was accepted.
- Assessment: The login is a useful starting point for investigating
  account activity.
- Confidence: High that the synthetic record states this; unknown whether
  a comparable real-world event occurred.
- Follow-up: Correlate with authoritative SSH logs, account ownership,
  source attribution, and expected access records.

### Finding 2 — Process and outbound-connection events are temporally close

- Evidence: process.log:1 and network.log:1
- Observation: The process event for PID 2501 precedes a connection record
  referencing the same PID by three seconds.
- Assessment: This is a correlation worth validating, not proof that curl
  initiated the connection. The supplied records do not independently
  validate process-to-network attribution.
- Confidence: High for the recorded timestamps; limited for causation.
- Follow-up: Review trustworthy process-audit and network telemetry.

### Finding 3 — A file is recorded under /tmp

- Evidence: process.log:2
- Observation: The log records creation of /tmp/.cache-sync by PID 2518.
- Assessment: The filename and location merit examination but are not
  sufficient to label the file malicious.
- Confidence: High for the synthetic log entry; file contents and intent
  are unknown.
- Follow-up: In a real investigation, preserve the file and metadata,
  calculate a hash, and examine it in a controlled environment.

### Finding 4 — A failed SSH login follows the accepted login

- Evidence: auth.log:1 and auth.log:3
- Observation: The same recorded source address appears in an accepted
  login and a later failed attempt for invalid user backup.
- Assessment: The sequence may be relevant, but does not prove that both
  attempts came from the same person or that the accepted login was
  unauthorized.
- Confidence: High for the entries; attribution remains unverified.
- Follow-up: Compare identity-provider, firewall, VPN, and SSH records.

### Finding 5 — Integrity verification succeeded

- Evidence: output/evidence-manifest.sha256
- Observation: All three original synthetic logs matched their recorded
  SHA-256 digests during verification.
- Assessment: This supports that the files matched the manifest at the
  time checked. It does not independently prove who collected them,
  when they were collected, or whether the initial evidence was authentic.

## 5. Indicators and limitations

- 203.0.113.77 and 198.51.100.24 are documentation/test IP addresses.
  They are placeholders in this fictional case, not actionable attribution.
- The evidence is synthetic and was created for training.
- No packet capture, original host disk image, independent audit source,
  file contents, or validated process genealogy was supplied.
- A timestamp sequence establishes ordering in the supplied records,
  not a complete causal narrative.
- The current script rejects malformed records rather than recovering
  past them; this is appropriate for a small lab but needs explicit
  handling in a production forensic pipeline.

## 6. Recommended response actions

For a comparable real incident, subject to organizational procedures:

1. Preserve original evidence and record collection details, timestamps,
   time zone, examiner, and chain of custody.
2. Validate the login with authoritative authentication and access logs.
3. Acquire relevant host and network telemetry using approved procedures.
4. Preserve and safely examine the file and associated process artifacts.
5. Determine whether the account activity was authorized before deciding
   on containment or credential rotation.
6. Document every action and maintain hashes for collected evidence.
7. Escalate containment decisions through the incident-response process.

## 7. Conclusion

The synthetic records present several investigative leads: an accepted
SSH login, nearby process and network events, and a file-creation event.
The evidence is sufficient to demonstrate timeline reconstruction and
basic integrity verification, but insufficient to conclude that a
successful compromise or data exfiltration occurred.

Case status remains open pending corroboration.

## Reproducibility

Timeline generation:
python3 scripts/timeline_reconstruction.py

Unit tests:
python3 -m unittest discover -s tests -v

Evidence integrity verification:
cd case-001 && sha256sum --check output/evidence-manifest.sha256
