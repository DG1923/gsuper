"""build_gaps splits topics into strong / weak / not_understood."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-learn-plan/scripts"))

from gaps import build_gaps  # noqa: E402


class TestBuildGaps(unittest.TestCase):
    def test_build_gaps_splits_strong_and_miss(self) -> None:
        questions = [
            {
                "id": "q1",
                "topic": "ack",
                "answer": 0,
                "miss_if_wrong": "thought ack-then-generate",
            },
            {
                "id": "q2",
                "topic": "lease",
                "answer": 1,
                "miss_if_wrong": "thought lease kills GPU",
            },
        ]
        chosen = {"q1": 0, "q2": 0}  # q2 wrong
        g = build_gaps("61", questions, chosen)
        self.assertEqual(g["score"], {"correct": 1, "total": 2})
        self.assertEqual(g["strong"], ["ack"])
        self.assertIn("lease", g["weak"])
        self.assertEqual(
            g["not_understood"],
            [{"id": "lease", "miss": "thought lease kills GPU"}],
        )
        self.assertNotIn("ack", g["weak"])


if __name__ == "__main__":
    unittest.main()
