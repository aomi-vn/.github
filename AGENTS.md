Source of truth: `shared/AGENTS.shared.md` in [aomi-vn/aomi-agents-core](https://github.com/aomi-vn/aomi-agents-core). Do not edit the shared block here. Edit the master, then run `scripts/sync-agents-md.sh` in that repository.

# AGENTS.md: .github

<!-- BEGIN SHARED -->
## Shared rules for every Aomi agent

Version v1.1.0. These rules apply to every agent and every repository: Codex, Cursor, Cursor cloud agents, and Grok Bot. The full process is in [Aomi SDLC Workflow v1.3.0](https://app.notion.com/p/3faa1698f36c81e4b6ecf8de479ce8e4). If this file and the workflow disagree, the workflow is correct.

### Who is who

- Aomi has one human: Tien, the founder and product owner. Refer to Tien as "she" or "her". Do not use informal titles such as "em" or "anh".
- All other members are agents. Agents on Cursor and Codex do the engineering and testing work.
- The Product Lead (PL) locks what to build and why. The Engineering Lead opens the Linear issues and is the only merger.

### How you work

- Act first. Think one step ahead. Find the dependencies, risks, and next steps before you start.
- If a task is authorized, do it to the end. Do not wait for step-by-step guidance.
- After each change, verify the result.
- Give short answers with verified results, proof, and clear next steps.
- If a summary is for Tien in Vietnamese, keep it short and factual.

### Risk levels

1. R0 (read only) and R1 (work on an isolated branch): do these yourself.
2. R2 (merge, deploy, external message): get authorization and a verified rollback step first.
3. R3 (credentials, data deletion, payments): get explicit approval from Tien first.

- If the same error fails 3 times, stop and write up the blocker with proof.
- Do not run endless retry loops. They waste tokens.

### Plan structural work with `/architect`

For a complex task or a structural change, do these phases in sequence:

1. Ground. Read the surrounding system and build a model of it.
2. Sketch. Define the types, interfaces, and boundaries before you write logic.
3. Agree. Check the design against the constraints.
4. Implement. Replace the sketch with real logic that meets the contract.
5. Scrap. If the design causes friction, delete the sketch and design again.

### Use industry standards

- Use standard repository layouts, Conventional Commits, strict SemVer, and Diátaxis docs.
- Do not invent a custom mechanism when a standard exists. Extend a standard only for a recorded Aomi gap.

### Writing

- Write every doc, PR, commit, ticket, and message with the `technical-writing` skill and the `asd-ste100` skill.
- Write for Tien first. Use clear, simple English, active voice, and commands for instructions.
- Keep instructions under 20 words. Keep other sentences under 25 words.
- Do not use filler, buzzwords, or emoji unless Tien asks. Do not use em dashes.
- Write human-facing times in ICT (UTC+7).

### Tickets and branches

1. Track each task in a Linear ticket in team `AOM` (https://linear.app/aomi-vn).
2. Write `Created by: <bot name>` as the first line of each ticket description.
3. Give one ticket to one agent. That agent sets the ticket to In Progress and opens one PR.
4. Push a branch in the same repository. Do not use a fork.
5. Do not review your own PR.
6. On a release ping, run `/release-pipeline` and complete every checkbox before Done.

### Merge rules

- Do not merge. Bots never merge. Only the Engineering Lead merges.
- The Engineering Lead merges only when all of these are true for the final head SHA:
  - CI is green.
  - `@codex review` and `@codex security review` are complete.
  - No open P0 or P1 finding has no written reason.
  - For a merge into `main`, the PL accept and the Tien GO name that SHA.
- If you push to the PR head, the earlier CI, Codex, PL accept, and Tien GO become stale.
- If the Codex app is down, do not merge. A local `codex review` does not count.
- A merge by anyone other than the Engineering Lead is an incident. Open a revert PR.

### What Codex review must check

- No text that deploys to production before the merge to `main`, or that auto-merges.
- No merge tool or merge credential in a bot config.
- No secret value in the diff.
- The same-repository CI guard is present.
- The change matches its Linear ticket and keeps every stated requirement.

### Deploy rules

- Production deploys only from `main`, after the merge.
- Only the pipeline deploy step publishes production. Do not upload to Cloudflare by hand. Do not run `wrangler` against production.
- If production is down (P0), the Engineering Lead rolls back to the last good deployment.

### Done means synced

A task is Done only when all of these are true:

1. One tip commit SHA exists on the remote branch.
2. The local clone is clean.
3. The local `HEAD` equals that remote tip SHA.
4. The required checks ran and passed on that SHA.

- Report the verified SHA and the test result. Do not report only file paths.
- If an API or MCP wrote to the remote, sync the local clone in the same turn.
- If you cannot sync, report "Done with gap" and name the exact blocker.
- Do not report Done or pushed when the tree is dirty or the branch has diverged.

### Files and secrets

- Keep one source of truth for each config file. Do not use symbolic links across config boundaries.
- If a tool needs the file on disk, keep identical real files.
- If text is out of date, delete it and write it again. Do not keep `.bak` or `.backup` files. Git keeps the history.
- Keep working trees free of temporary files.
- Do not commit secret values, tokens, or credentials to a repository or a log. Record only the secret name in the secrets inventory (`secrets/inventory.md` in `aomi-agents-core`).
- Do not add new spend without approval from Tien.
- Attach proof to every blocker report: a log line, an error message, a link, or a screenshot.

### Slack and the OA chat

- F·COS is the only bridge from the Foundation team to Slack and to the OA chat.
- If you are another F bot, send each Slack or OA need to F·COS with `SendToAgent`.
- Do not run a Slack event routine.

### Where things live

- Code is in GitHub organization `aomi-vn`. Tasks are in Linear. Long documents are in Notion.
- Keep only runtime state on a box or a VM.
<!-- END SHARED -->

## This repository

This repository holds org-wide templates and community health files only. It has no build, no tests, and no CI.

- Before you open a PR, run `git diff --check`.
