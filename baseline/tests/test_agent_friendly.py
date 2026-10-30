import tempfile
import unittest
from pathlib import Path

from baseline import agent_friendly


class AgentFriendlyTest(unittest.TestCase):
    def test_passes_minimal_template_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text(
                "See `.cursor/skills/verify/SKILL.md` and run npm run verify.\n",
                encoding="utf-8",
            )
            skill = root / ".cursor" / "skills" / "verify"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: verify\n---\n", encoding="utf-8")
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "verify.sh").write_text("#!/usr/bin/env bash\nexec true\n", encoding="utf-8")
            self.assertEqual(agent_friendly.check_root(root), [])


if __name__ == "__main__":
    unittest.main()
