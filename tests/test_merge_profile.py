"""profile.json merge: not_understood stays until a later quiz marks strong."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-learn-plan/scripts"))

from merge_profile import merge_profile  # noqa: E402


class TestMergeProfile(unittest.TestCase):
    def test_miss_survives_until_strong(self) -> None:
        profile = {"topics": {"lease": {"status": "not_understood", "miss": "old"}}}
        gaps = {
            "strong": [],
            "weak": ["lease"],
            "not_understood": [{"id": "lease", "miss": "still wrong"}],
        }
        out = merge_profile(profile, gaps)
        self.assertEqual(out["topics"]["lease"]["status"], "not_understood")

    def test_strong_clears_miss(self) -> None:
        profile = {"topics": {"lease": {"status": "not_understood", "miss": "old"}}}
        gaps = {"strong": ["lease"], "weak": [], "not_understood": []}
        out = merge_profile(profile, gaps)
        self.assertEqual(out["topics"]["lease"]["status"], "strong")


if __name__ == "__main__":
    unittest.main()
