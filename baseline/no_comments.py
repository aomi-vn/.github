import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

HASH_LANGS = {".py", ".sh", ".bash"}
SLASH_LANGS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}
ALLOWED = re.compile(r"^(#!|//\s*SPDX-License-Identifier:|#\s*SPDX-License-Identifier:)")
SLASH_COMMENT = re.compile(r"(^|[^:\"'`\\])(//|/\*)")


def added_lines(base: str) -> dict[str, set[int]]:
    diff = subprocess.run(
        ["git", "diff", "--unified=0", "--no-color", "--no-ext-diff", f"{base}...HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout
    result: dict[str, set[int]] = {}
    path = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else ""
        elif line.startswith("@@") and path:
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if match:
                start, count = int(match.group(1)), int(match.group(2) or "1")
                result.setdefault(path, set()).update(range(start, start + count))
    return result


def python_comments(text: str) -> set[int]:
    found: set[int] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                found.add(tok.start[0])
    except (tokenize.TokenError, SyntaxError):
        pass
    return found


def line_is_comment(suffix: str, line: str) -> bool:
    stripped = line.strip()
    if not stripped or ALLOWED.match(stripped):
        return False
    if suffix in HASH_LANGS:
        return stripped.startswith("#")
    return stripped.startswith(("//", "/*", "*")) or bool(SLASH_COMMENT.search(line))


def violations(base: str) -> list[str]:
    out: list[str] = []
    for path, lines in sorted(added_lines(base).items()):
        file = Path(path)
        if file.suffix not in HASH_LANGS | SLASH_LANGS or not file.is_file():
            continue
        text = file.read_text(errors="replace")
        rows = text.splitlines()
        py = python_comments(text) if file.suffix == ".py" else set()
        for n in sorted(lines):
            if n > len(rows):
                continue
            row = rows[n - 1]
            hit = (n in py and not ALLOWED.match(row.strip())) if file.suffix == ".py" else line_is_comment(file.suffix, row)
            if hit:
                out.append(f"{path}:{n}: {row.strip()[:120]}")
    return out


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    found = violations(base)
    for item in found:
        print(f"::error::no-comments: {item}")
    if found:
        print(f"no-comments: {len(found)} added comment line(s). Say it in code, names, tests, or the PR description. See docs/baseline.md.")
        return 1
    print("no-comments: no added comments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
