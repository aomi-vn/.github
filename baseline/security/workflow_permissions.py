from __future__ import annotations

import re
import sys
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
WORKFLOW_SUFFIXES = {".yml", ".yaml"}
WRITE_KEYS = frozenset(
    {
        "actions",
        "attestations",
        "checks",
        "contents",
        "deployments",
        "discussions",
        "id-token",
        "issues",
        "packages",
        "pages",
        "pull-requests",
        "repository-projects",
        "security-events",
        "statuses",
    }
)
READ_ONLY_VALUES = frozenset({"read", "none"})


def iter_workflows(root: Path) -> list[Path]:
    directory = root / WORKFLOW_DIR
    if not directory.is_dir():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in WORKFLOW_SUFFIXES and path.is_file()
    )


def top_level_permissions_block(text: str) -> tuple[int, str] | None:
    jobs_at = re.search(r"^jobs:\s*$", text, re.MULTILINE)
    head = text if jobs_at is None else text[: jobs_at.start()]
    match = re.search(r"^permissions:\s*(.*)$", head, re.MULTILINE)
    if not match:
        return None
    line_no = head[: match.start()].count("\n") + 1
    block_lines = [match.group(0)]
    for line in head[match.end() + 1 :].splitlines():
        if line and not line.startswith((" ", "\t")):
            break
        if line.strip():
            block_lines.append(line)
    return line_no, "\n".join(block_lines)


def permissions_values(block: str) -> dict[str, str]:
    if re.search(r"^permissions:\s*\{\}\s*$", block, re.MULTILINE):
        return {}
    if re.search(r"^permissions:\s*write-all\s*$", block, re.MULTILINE):
        return {"__write_all__": "write-all"}
    values: dict[str, str] = {}
    for line in block.splitlines()[1:]:
        match = re.match(r"^[\s-]*([a-z-]+):\s*(\S+)", line)
        if match:
            values[match.group(1)] = match.group(2).strip("'\"")
    if not values and re.search(r"^permissions:\s*(\S+)\s*$", block, re.MULTILINE):
        scalar = re.search(r"^permissions:\s*(\S+)\s*$", block, re.MULTILINE)
        if scalar:
            values["__scalar__"] = scalar.group(1)
    return values


def is_read_only(values: dict[str, str]) -> bool:
    if not values:
        return True
    if "__write_all__" in values or "__scalar__" in values:
        return False
    return all(value in READ_ONLY_VALUES for value in values.values())


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if "write-all" in text:
        return [f"{path}: must not use permissions write-all"]
    found = top_level_permissions_block(text)
    if found is None:
        return [
            f"{path}: missing top-level permissions (use permissions: {{}} or read-only scopes)"
        ]
    line_no, block = found
    values = permissions_values(block)
    if not is_read_only(values):
        bad = ", ".join(f"{key}={value}" for key, value in sorted(values.items()))
        return [f"{path}:{line_no}: top-level permissions must be read-only or empty, saw {bad}"]
    return []


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
    print("PASS workflow-permissions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
