"""Self-report parse, need-to-know depth, profile merge."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-learn-pack/scripts"))

from merge_profile import merge_profile
from self_report import parse_self_report, render_need_to_know, self_report_template


class TestSelfReport(unittest.TestCase):
    def test_parse_known_and_unknown(self) -> None:
        md = (
            "## ack\n"
            "status: known\n"
            "how: finally after handle\n"
            "## lease\n"
            "status: unknown\n"
            "how: thought 60s kills GPU\n"
        )
        parsed = parse_self_report(md)
        self.assertEqual(parsed["ack"]["status"], "known")
        self.assertEqual(parsed["lease"]["status"], "unknown")
        self.assertIn("60s", parsed["lease"]["how"])

    def test_template_has_no_answers(self) -> None:
        text = self_report_template("61", ["ack", "lease"])
        self.assertIn("## ack", text)
        self.assertIn("status: unknown", text)
        self.assertNotIn("fail()", text)
        self.assertNotIn("answer:", text.lower())

    def test_need_to_know_full_on_unknown(self) -> None:
        sections = [
            {"id": "ack", "title": "Ack", "full": "FULL ACK", "recap": "short ack"},
            {"id": "lease", "title": "Lease", "full": "FULL LEASE", "recap": "short lease"},
        ]
        md = render_need_to_know(
            "Need to know",
            sections,
            {"ack": {"status": "known", "how": ""}},
        )
        self.assertIn("short ack", md)
        self.assertIn("FULL LEASE", md)
        self.assertNotIn("FULL ACK", md)

    def test_unknown_survives_until_known(self) -> None:
        profile = {"topics": {"lease": {"status": "unknown", "how": "old"}}}
        out = merge_profile(profile, {"lease": {"status": "unknown", "how": "still"}})
        self.assertEqual(out["topics"]["lease"]["status"], "unknown")
        out2 = merge_profile(profile, {"lease": {"status": "known", "how": "ok"}})
        self.assertEqual(out2["topics"]["lease"]["status"], "known")


if __name__ == "__main__":
    unittest.main()
