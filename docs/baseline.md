# Aomi engineering baseline

Every Aomi repo calls `aomi-vn/.github/.github/workflows/baseline.yml`. Its `ci-gate` job is the only required check in org ruleset `default-branch-ci-gate`, so a repo adopts the baseline by adding one caller file and joining the ruleset.

| Job | Rule | Runs on |
| --- | --- | --- |
| `verify` | Runs the repo's `verify-command`, which drives the app the way a user does (see the repo's `.cursor/skills/verify/SKILL.md`). | push and PR |
| `no-comments` | Fails when the PR adds a comment line. | PR |
| `typecheck` | `tsc --noEmit` with `strict: true` required in `tsconfig.json`; `mypy --strict` when `pyproject.toml` exists, on `[tool.mypy] files` if set (else `.`), via `uv run --locked` when `uv.lock` exists so project stubs resolve. | push and PR |
| `agent-review` | One LLM review per PR, posted as a single comment that is edited in place on each push. Fails closed. | PR |
| `ci-gate` | Fails unless every job required for the event succeeded. | always |

## no-comments

Comments are banned in code. Agents justify shortcuts in comments ("quick hack, fix later", "we don't do Y here"), and those comments spread the hack. Put the reason in names, types, tests, or the PR description instead.

The lint is deterministic and only looks at lines added by the PR (`git diff base...HEAD`):

- Checked files: `.py .sh .bash .ts .tsx .js .jsx .mjs .cjs .mts .cts`. Markdown, YAML, and config files are not checked.
- Python uses the `tokenize` module, so `#` inside strings is not a comment.
- Shell lines starting with `#` are comments. JS and TS lines with `//`, `/*`, or a leading `*` are comments, except `//` right after `:` or a quote (URLs).
- Allowed: shebang lines and `SPDX-License-Identifier` lines.
- Suppression directives (`# type: ignore`, `// @ts-ignore`, `eslint-disable`) are comments and fail. Fix the type instead.

Known limit: `//` inside a JS string that is not a URL is flagged. Rewrite the string.

## agent-review

Needs the repo or org secret `AGENT_REVIEW_API_KEY` (OpenAI-compatible endpoint; default DeepSeek `deepseek-chat`, override with `AGENT_REVIEW_URL` and `AGENT_REVIEW_MODEL`). Without the secret the job fails closed. The comment carries the marker `<!-- aomi-agent-review:v1 -->` so a PR only ever has one review comment.

## Adopting in a repo

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  pull-requests: write
  issues: write
jobs:
  ci:
    uses: aomi-vn/.github/.github/workflows/baseline.yml@main
    with:
      verify-command: npm run verify
    secrets: inherit
```

The required check name is `ci / ci-gate`, which satisfies the ruleset's `ci-gate` context.
