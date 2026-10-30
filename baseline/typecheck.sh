#!/usr/bin/env bash
set -euo pipefail
ran=0
if [ -f tsconfig.json ]; then
  strict=$(npx --no-install tsc --showConfig | jq -r '.compilerOptions.strict // false')
  if [ "$strict" != "true" ]; then
    echo "::error::typecheck: tsconfig.json must set compilerOptions.strict to true"
    exit 1
  fi
  npx --no-install tsc --noEmit
  ran=1
fi
if [ -f pyproject.toml ]; then
  mypy_files=$(python3 -c 'import tomllib; print(" ".join(tomllib.load(open("pyproject.toml","rb")).get("tool",{}).get("mypy",{}).get("files",[])) or ".")')
  if [ -f uv.lock ]; then
    uv run --locked --with mypy mypy --strict $mypy_files
  else
    uvx mypy --strict $mypy_files
  fi
  ran=1
fi
if [ "$ran" = 0 ]; then
  echo "::error::typecheck: no tsconfig.json or pyproject.toml found"
  exit 1
fi
echo "typecheck: strict typecheck passed."
