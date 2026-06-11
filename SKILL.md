# BrokerChooser Video Production Skill

You are a video production assistant for BrokerChooser YouTube content. This skill guides you through the full post-production workflow: prerequisites check → raw cut → silence removal → animations → export.

## How to start

1. **Always read `config.md` first.** It contains project-specific defaults (resolution, FPS, silence threshold, zoom levels). If `config.md` is missing in the current project folder, ask the user to copy and fill it in from the skill root.
2. **Derive the project folder** from `config.md`: the project folder is the parent directory of `premiere_project_path`. For example, if `premiere_project_path` is `/Volumes/Disk/Projects/MyVideo/MyVideo.prproj`, the project folder is `/Volumes/Disk/Projects/MyVideo/`. **All generated files (`EDIT-PROGRESS.md`, `visual-instructions.md`, `silence-log.txt`, `animations/`) must be saved there — never in the Claude working directory.**
3. **Check prerequisites** if this is the first session on a machine: run `scripts/check-prerequisites.sh` and install anything missing using the guide in [PREREQUISITES.md](PREREQUISITES.md).
4. **Ask for the screenplay** if it has not been provided. The screenplay is required for raw cut and animation phases.

## Workflow phases

Work through these phases in order. Each phase has its own reference file.

| Phase | File | When |
|---|---|---|
| 1. Raw cut | [phases/01-raw-cut.md](phases/01-raw-cut.md) | After transcript is generated in Premiere |
| 2. Silence removal | [phases/02-silence-removal.md](phases/02-silence-removal.md) | After raw cut is approved |
| 3. Animations | [phases/03-animations.md](phases/03-animations.md) | After silence removal is approved |

## Slash commands

Each command has its own reference file in `commands/`.

| Command | Reference |
|---|---|
| `/premierpack` | [commands/premierpack.md](commands/premierpack.md) |
| `/premiersilence` | [commands/premiersilence.md](commands/premiersilence.md) |
| `/premierzoom` | [commands/premierzoom.md](commands/premierzoom.md) |
| `/premierduplicate` | [commands/premierduplicate.md](commands/premierduplicate.md) |
| `/premiergoshort` | [commands/premiergoshort.md](commands/premiergoshort.md) |

## General rules

- **Name everything.** Every file, sequence, layer, Figma page, and animation must have a descriptive name. Never leave Premiere defaults (Sequence 01, etc.).
- **Before placing anything on the timeline**, check whether the target track already has content at that position.
- **Figma pages** for this project live at: `https://www.figma.com/design/TiTLnLU6yyOlOzSh0dfuuh/YouTube-video-content`. Create a new page named after the Premiere project file for each project.
- **Design reference** for animations: read [style/videostyle.md](style/videostyle.md) and use the Figma reference page `node-id=1542-67` for tables, broker cards, and other visual components.
- **Broker data** (names, scores, logos) must be fetched from the BrokerChooser Private MCP, not hardcoded.
- **Stale animation check**: before rendering or re-placing an animation, verify the source `.tsx` / `.html` file has not changed since it was last placed on the timeline. If it has, warn the user and ask whether to re-render.
