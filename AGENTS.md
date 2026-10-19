# Shared Aomi instructions

Before task work, identify the approved `aomi-vn/aomi-plugins` revision and expected guide SHA-256 from existing acceptance evidence.
Resolve that approved revision to its full 40-character commit SHA through authorized GitHub metadata.
Confirm that exact SHA is approved and reachable from `main` before reading guide content.
Repository `aomi-vn/aomi-plugins`, branch `main`, and path `plugins/aomi/skills/aomi-mode/SKILL.md` are locators only.
Do not read the guide through a mutable branch URL.
Retrieve the guide bytes only from the approved immutable object and verify their SHA-256 before following its instructions.
If an authorized `aomi-plugins` checkout is mounted, set `AOMI_PLUGINS_CHECKOUT` to it and `AOMI_MODE_SOURCE_SHA` to the verified commit.
Calculate the guide digest without displaying its content:

```sh
git -C "$AOMI_PLUGINS_CHECKOUT" show "$AOMI_MODE_SOURCE_SHA:plugins/aomi/skills/aomi-mode/SKILL.md" | sha256sum
```
Compare that digest with the approved expected SHA-256. Stop on a mismatch.
Only after it matches, read the guide and applicable linked files in that repository at the approved SHA:

```sh
git -C "$AOMI_PLUGINS_CHECKOUT" show "$AOMI_MODE_SOURCE_SHA:plugins/aomi/skills/aomi-mode/SKILL.md"
```
For another authorized GitHub reader, use the same approval and digest checks before following guide instructions.
Its guide URL must use the verified full SHA in `https://github.com/aomi-vn/aomi-plugins/blob/<approved-sha>/plugins/aomi/skills/aomi-mode/SKILL.md`.
Record the approval evidence, expected and actual digests, source commit, and path in the ticket.
If approval, the revision, the expected digest, or the guide is unavailable, report the exact blocker before dependent work.
A URL is a locator, not automatic import or native skill activation.
Keep source-read, installed, and session-loaded evidence separate.
Do not install WIP, run retired init, or copy the shared playbook into this repository.

Then apply repository-specific instructions and applicable nested instruction files.
This sequence does not change the host's native instruction precedence.
Preserve local context, WIP, owner holds, and required approval gates.
