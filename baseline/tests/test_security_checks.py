import tempfile
import unittest
from pathlib import Path

from baseline.security import action_pins, workflow_permissions


class WorkflowPermissionsTest(unittest.TestCase):
    def test_accepts_empty_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "name: CI\non: push\npermissions: {}\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps: []\n",
                encoding="utf-8",
            )
            self.assertEqual(workflow_permissions.check_root(root), [])

    def test_rejects_write_all(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "bad.yml").write_text(
                "permissions: write-all\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps: []\n",
                encoding="utf-8",
            )
            problems = workflow_permissions.check_root(root)
            self.assertTrue(any("write-all" in item for item in problems))

    def test_rejects_top_level_pr_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "bad.yml").write_text(
                "permissions:\n  contents: read\n  pull-requests: write\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps: []\n",
                encoding="utf-8",
            )
            self.assertTrue(workflow_permissions.check_root(root))


class ActionPinsTest(unittest.TestCase):
    def test_accepts_pinned_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "jobs:\n  x:\n    steps:\n      - uses: actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09\n",
                encoding="utf-8",
            )
            self.assertEqual(action_pins.check_root(root), [])

    def test_rejects_version_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "jobs:\n  x:\n    steps:\n      - uses: actions/checkout@v5\n",
                encoding="utf-8",
            )
            problems = action_pins.check_root(root)
            self.assertTrue(any("full commit SHA" in item for item in problems))

    def test_allows_org_reusable_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "jobs:\n  x:\n    uses: aomi-vn/.github/.github/workflows/baseline.yml@main\n",
                encoding="utf-8",
            )
            self.assertEqual(action_pins.check_root(root), [])


if __name__ == "__main__":
    unittest.main()
