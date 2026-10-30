from __future__ import annotations

import sys
from pathlib import Path

AGENTS = Path("AGENTS.md")
MAX_AGENTS_BYTES = 4096
SKILLS = Path(".cursor/skills")


def verify_skill_paths(root: Path) -> list[Path]:
    found: list[Path] = []
    direct = root / SKILLS / "verify" / "SKILL.md"
    if direct.is_file():
        found.append(direct)
    if SKILLS.is_dir():
        for path in sorted(SKILLS.glob("verify-*/SKILL.md")):
            found.append(path)
    return found


def check_root(root: Path) -> list[str]:
    problems: list[str] = []
    agents = root / AGENTS
    if not agents.is_file():
        return ["missing AGENTS.md at repository root"]
    text = agents.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))
    if size > MAX_AGENTS_BYTES:
        problems.append(f"AGENTS.md is {size} bytes; limit {MAX_AGENTS_BYTES}")
    skills = verify_skill_paths(root)
    if not skills:
        problems.append("missing .cursor/skills/verify/SKILL.md or verify-*/SKILL.md")
    elif ".cursor/skills/verify" not in text and not any(
        path.parent.name in text for path in skills
    ):
        problems.append("AGENTS.md must point agents at the verify skill under .cursor/skills")
    verify_sh = root / "scripts" / "verify.sh"
    if verify_sh.is_file():
        line_count = sum(1 for _ in verify_sh.open("r", encoding="utf-8"))
        if line_count > 30:
            problems.append(f"scripts/verify.sh has {line_count} lines; shell glue limit is 30")
    return problems


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[1]) if argv and len(argv) > 1 else Path(".")
    problems = check_root(root.resolve())
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    print("PASS agent-friendly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
