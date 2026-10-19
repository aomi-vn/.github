# Shared Aomi instructions

Before task work, read the canonical [aomi-mode guide](https://github.com/aomi-vn/aomi-plugins/blob/main/plugins/aomi/skills/aomi-mode/SKILL.md).
Resolve approved `main` to a full commit through an authorized GitHub reader.
Read `plugins/aomi/skills/aomi-mode/SKILL.md` and applicable linked files at that commit.
If an authorized `aomi-plugins` checkout is mounted, read the same commit there.
Set `AOMI_PLUGINS_CHECKOUT` to that checkout and `AOMI_MODE_SOURCE_SHA` to the verified commit.

```sh
git -C "$AOMI_PLUGINS_CHECKOUT" show "$AOMI_MODE_SOURCE_SHA:plugins/aomi/skills/aomi-mode/SKILL.md"
```
Record the source commit, path, and content hash in the ticket.
If the guide is unavailable, report the exact blocker before dependent work.
A URL is a read instruction, not automatic import or native skill activation.
Keep source-read, installed, and session-loaded evidence separate.
Do not install WIP, run retired init, or copy the shared playbook into this repository.

Then apply repository-specific instructions and applicable nested instruction files.
This sequence does not change the host's native instruction precedence.
Preserve local context, WIP, owner holds, and required approval gates.
