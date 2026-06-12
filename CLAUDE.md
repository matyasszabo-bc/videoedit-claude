# CLAUDE.md — BrokerChooser Video Production

This directory is the skill root for BC video post-production. Project-specific files (sequences, footage, progress trackers) live in the project folder, not here.

## References

Before starting any work, read:

- **[SKILL.md](SKILL.md)** — overall workflow, phases, slash commands
- **[phases/03-animations.md](phases/03-animations.md)** — animation pipeline, render rules, HTML→MOV pipeline ← always read this before any animation work
- **[style/videostyle.md](style/videostyle.md)** — design tokens (colors, typography, spacing)
- **[references/figma-workflow.md](references/figma-workflow.md)** — Figma access, BrokerChooser Private MCP usage

Do not duplicate content from those files here.

## Always

- After completing or placing any animation, update `EDIT-PROGRESS.md` in the project folder — mark the ANIM with `[x]` and update the "Utoljára frissítve" line.
- Before placing anything on the timeline, **always call `get_timeline_state` with a `rangeStart`/`rangeEnd` window around the target timecode** and verify V2 is empty at that position. Never assume a track is free — check every time, for every clip.
- All animations are standalone HTML files rendered to ProRes 4444 MOV via `scripts/render-html-to-mov.py` — never use Remotion CLI or TSX components.
- No hardcoded colors or sizes — always use tokens from `style/videostyle.md`.
