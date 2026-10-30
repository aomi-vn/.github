from __future__ import annotations

import re
import sys
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
WORKFLOW_SUFFIXES = {".yml", ".yaml"}
SHA_REF = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*(?P<target>\S+)")
ORG_REUSABLE = re.compile(r"^aomi-vn/\.github/")


def iter_workflows(root: Path) -> list[Path]:
    directory = root / WORKFLOW_DIR
    if not directory.is_dir():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in WORKFLOW_SUFFIXES and path.is_file()
    )


def parse_uses(raw: str) -> tuple[str, str]:
    target = raw.split("#", 1)[0].strip()
    if "@" not in target:
        return target, ""
    repo, ref = target.rsplit("@", 1)
    return repo, ref


def is_local_uses(repo: str) -> bool:
    return repo.startswith("./") or repo.startswith("../")


def is_reusable_workflow(repo: str) -> bool:
    return ".github/workflows/" in repo and repo.endswith((".yml", ".yaml"))


def is_pinned_action(repo: str, ref: str) -> bool:
    if is_local_uses(repo):
        return True
    if is_reusable_workflow(repo):
        return bool(ORG_REUSABLE.match(repo))
    return bool(SHA_REF.match(ref))


def check_file(path: Path) -> list[str]:
    problems: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = USES.match(line)
        if not match:
            continue
        repo, ref = parse_uses(match.group("target"))
        if repo.startswith("docker://"):
            continue
        if not ref:
            problems.append(f"{path}:{line_no}: uses must pin an action ref")
            continue
        if not is_pinned_action(repo, ref):
            problems.append(
                f"{path}:{line_no}: third-party action {repo}@{ref} must use a full commit SHA"
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
    print("PASS action-pins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
