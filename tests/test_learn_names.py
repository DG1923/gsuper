"""Unique learn pack filenames."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-learn-pack/scripts"))

from names import (
    material_filename,
    need_to_know_filename,
    pack_filename,
    self_report_filename,
    slug,
)


class TestNames(unittest.TestCase):
    def test_pack_filename_unique_shape(self) -> None:
        name = pack_filename("x-project", "61 reusable")
        self.assertEqual(name, "gsuper-pack-x-project-61-reusable.md")

    def test_material_filename_includes_concept(self) -> None:
        name = material_filename("x-project", "pickleball-highlight", "ball-accel")
        self.assertEqual(
            name, "gsuper-material-x-project-pickleball-highlight-ball-accel.md"
        )

    def test_need_to_know_and_self_report(self) -> None:
        self.assertEqual(
            need_to_know_filename("x-project", "61"),
            "need-to-know-x-project-61.md",
        )
        self.assertEqual(self_report_filename("61"), "self-report-61.md")

    def test_slug_strips_junk(self) -> None:
        self.assertEqual(slug("  Foo_Bar!! "), "foo-bar")


if __name__ == "__main__":
    unittest.main()
