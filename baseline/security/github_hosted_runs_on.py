from __future__ import annotations

import re
import sys
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
WORKFLOW_SUFFIXES = {".yml", ".yaml"}
RUNNER_KEY = re.compile(r"^\s*(runs-on|gate-runs-on):\s*(.+?)\s*$")
GITHUB_HOSTED = re.compile(
    r"(?<![\w./-])(ubuntu-[a-z0-9.-]+|windows-[a-z0-9.-]+|macos-[a-z0-9.-]+)(?![\w.-])",
    re.IGNORECASE,
)


def iter_workflows(root: Path) -> list[Path]:
    directory = root / WORKFLOW_DIR
    if not directory.is_dir():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in WORKFLOW_SUFFIXES and path.is_file()
    )


def github_hosted_in_runner_value(value: str) -> list[str]:
    found: list[str] = []
    for match in GITHUB_HOSTED.finditer(value):
        label = match.group(1)
        if label not in found:
            found.append(label)
    return found


def check_file(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = RUNNER_KEY.match(line)
        if not match:
            continue
        value = match.group(2)
        labels = github_hosted_in_runner_value(value)
        if labels:
            joined = ", ".join(labels)
            problems.append(
                f"{path}:{line_no}: {match.group(1)} must use VPS self-hosted labels, not GitHub-hosted ({joined})"
            )
    return problems


def check_root(root: Path) -> list[str]:
    problems: list[str] = []
    for path in iter_workflows(root):
        problems.extend(check_file(path))
    return problems


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[1]) if argv and len(argv) > 1 else Path(".")
    problems = check_root(root.resolve())
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    print("PASS github-hosted-runs-on")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
