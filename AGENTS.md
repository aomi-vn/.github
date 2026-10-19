# Shared Aomi instructions

Before task work, identify the approved `aomi-vn/aomi-plugins` revision from existing acceptance evidence.
Resolve that approved revision to its full 40-character commit SHA through authorized GitHub metadata.
Confirm that exact SHA is approved and reachable from `main` before reading guide content.
Repository `aomi-vn/aomi-plugins`, branch `main`, and path `plugins/aomi/skills/aomi-mode/SKILL.md` are locators only.
Do not read the guide through a mutable branch URL.
Read the guide and applicable linked files in that repository only at the approved SHA.
For GitHub reads, replace `<approved-sha>` in `https://github.com/aomi-vn/aomi-plugins/blob/<approved-sha>/plugins/aomi/skills/aomi-mode/SKILL.md` with the verified full SHA.
If an authorized `aomi-plugins` checkout is mounted, read the same approved commit there.
Set `AOMI_PLUGINS_CHECKOUT` to that checkout and `AOMI_MODE_SOURCE_SHA` to the verified commit.

```sh
git -C "$AOMI_PLUGINS_CHECKOUT" show "$AOMI_MODE_SOURCE_SHA:plugins/aomi/skills/aomi-mode/SKILL.md"
```
Record the approval evidence, source commit, path, and content hash in the ticket.
If approval, the revision, or the guide is unavailable, report the exact blocker before dependent work.
A URL is a locator, not automatic import or native skill activation.
Keep source-read, installed, and session-loaded evidence separate.
Do not install WIP, run retired init, or copy the shared playbook into this repository.

Then apply repository-specific instructions and applicable nested instruction files.
This sequence does not change the host's native instruction precedence.
Preserve local context, WIP, owner holds, and required approval gates.
