# Shared Aomi instructions

Before task work, identify the approved `aomi-vn/aomi-plugins` revision, expected guide SHA-256, and expected hashes for applicable linked repository files from existing acceptance evidence.
Resolve that approved revision to its full 40-character commit SHA through authorized GitHub metadata.
Confirm that exact SHA is approved and reachable from `main` before reading guide content.
Repository `aomi-vn/aomi-plugins`, branch `main`, and path `plugins/aomi/skills/aomi-mode/SKILL.md` are locators only.
Use only an authorized GitHub reader for the guide and applicable linked repository files.
The guide URL must use the verified full SHA in `https://github.com/aomi-vn/aomi-plugins/blob/<approved-sha>/plugins/aomi/skills/aomi-mode/SKILL.md`.
Retrieve complete guide bytes only at that approved commit and exact repository path.
Verify the commit, path, and actual SHA-256 against the approved values before following the guide's instructions.
For each applicable linked repository file, obtain its expected hash before retrieval; bind the complete bytes to the approved commit and exact path, and verify its hash before following it.
Missing hashes, inaccessible bytes, truncated output, and mismatches stop dependent work. Report the exact blocker.
Record the approval evidence, source commit, paths, and expected and actual hashes in the ticket.
A URL is a locator, not automatic import or native skill activation.
Keep source-read, installed, and session-loaded evidence separate.
Do not install WIP, run retired init, or copy the shared playbook into this repository.

Then apply repository-specific instructions and applicable nested instruction files.
This sequence does not change the host's native instruction precedence.
Preserve local context, WIP, owner holds, and required approval gates.
