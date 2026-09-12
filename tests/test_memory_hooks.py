"""Skills point at the memory CLI."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestHooks(unittest.TestCase):
    def test_skills_point_at_memory_cli(self) -> None:
        spec = (ROOT / "skills/gsuper-write-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(spec, r"memory\.py\b.*\block\b")
        impl = (ROOT / "skills/gsuper-implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("memory.py find", impl)
        init = (ROOT / "skills/gsuper-init-project/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("memory.py", init)
        self.assertRegex(init, r"memory\.py\b.*\binit\b")
        self.assertNotIn("seed-xproject", init)
        mem = (ROOT / "skills/gsuper-memory/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("memory.py", mem)
        self.assertRegex(mem, r"memory\.sqlite init")
        self.assertNotIn("seed-xproject", mem)
        pack = (ROOT / "skills/gsuper-learn-pack/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("memory.py", pack)


if __name__ == "__main__":
    unittest.main()
