import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "timeline_reconstruction.py"
)

spec = importlib.util.spec_from_file_location("timeline_reconstruction", SCRIPT)
timeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(timeline)


class TimelineTests(unittest.TestCase):
    def test_valid_event_preserves_source_and_line(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "sample.log"
            evidence.write_text(
                "2026-10-17T09:14:03Z test event\n",
                encoding="utf-8",
            )

            events = timeline.parse_evidence_file(evidence)

            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["source"], "sample.log")
            self.assertEqual(events[0]["source_line"], 1)
            self.assertTrue(
                events[0]["timestamp_utc"].endswith("+00:00")
            )

    def test_malformed_event_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "bad.log"
            evidence.write_text("this is not a valid event\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                timeline.parse_evidence_file(evidence)

    def test_invalid_calendar_date_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "bad-date.log"
            evidence.write_text(
                "2026-99-99T09:14:03Z invalid date\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                timeline.parse_evidence_file(evidence)


if __name__ == "__main__":
    unittest.main(verbosity=2)
