# CLAUDE.md — BrokerChooser Video Production

This directory is the skill root for BC video post-production. Project-specific files (sequences, footage, progress trackers) live in the project folder, not here.

## References

Before starting any work, read:

- **[SKILL.md](SKILL.md)** — overall workflow, phases, slash commands
- **[phases/03-animations.md](phases/03-animations.md)** — animation pipeline, render rules, Remotion structure ← always read this before any animation work
- **[style/videostyle.md](style/videostyle.md)** — design tokens (colors, typography, spacing)
- **[references/figma-workflow.md](references/figma-workflow.md)** — Figma access, BrokerChooser Private MCP usage

Do not duplicate content from those files here.

## Always

- After completing or placing any animation, update `EDIT-PROGRESS.md` in the project folder — mark the ANIM with `[x]` and update the "Utoljára frissítve" line.
- Before placing anything on the timeline, check for free space dynamically (`get_timeline_state` or `list_sequence_tracks`) — do not pre-assign track numbers.
- All animations must be Remotion TSX components — never Playwright/HTML renders.
- No hardcoded colors or sizes — always use tokens from `style/videostyle.md`.
