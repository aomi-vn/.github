import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "no_comments.py"


def run(files: dict[str, str]) -> subprocess.CompletedProcess[str]:
    tmp = Path(tempfile.mkdtemp())
    git = ["git", "-C", str(tmp), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp)], check=True)
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "base"], check=True)
    for name, text in files.items():
        (tmp / name).write_text(text)
    subprocess.run([*git, "add", "."], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "change"], check=True)
    return subprocess.run([sys.executable, str(SCRIPT), "main~1"], cwd=tmp, capture_output=True, text=True)


class NoComments(unittest.TestCase):
    def test_hack_comment_in_ts_fails(self) -> None:
        self.assertEqual(run({"a.ts": "// quick hack, fix later\nexport const a = 1;\n"}).returncode, 1)

    def test_trailing_ts_comment_fails(self) -> None:
        self.assertEqual(run({"a.ts": "export const a = 1; // set a to one\n"}).returncode, 1)

    def test_python_comment_fails(self) -> None:
        self.assertEqual(run({"a.py": "x = 1  # type: ignore\n"}).returncode, 1)

    def test_url_and_hash_in_string_pass(self) -> None:
        files = {"a.ts": 'export const u = "https://aomi.vn";\n', "a.py": 's = "# not a comment"\n'}
        self.assertEqual(run(files).returncode, 0)

    def test_shebang_and_spdx_pass(self) -> None:
        self.assertEqual(run({"a.sh": "#!/usr/bin/env bash\n# SPDX-License-Identifier: MIT\necho hi\n"}).returncode, 0)

    def test_markdown_is_ignored(self) -> None:
        self.assertEqual(run({"a.md": "# Title\n"}).returncode, 0)


if __name__ == "__main__":
    unittest.main()
