# BrokerChooser Video Skill

Claude Code skill for end-to-end YouTube video production: prerequisites check → raw cut → silence removal → animations.

## Installation

Clone into your Claude plugins directory:

```bash
git clone git@github.com:brokerchooser/video-skill.git ~/.claude/plugins/video-skill
```

Then run the prerequisites check:

```bash
bash ~/.claude/plugins/video-skill/scripts/check-prerequisites.sh
```

## First use in a project

1. Copy `config.md` from the skill root into your Premiere Pro project folder.
2. Fill in the project-specific values (project name, paths, etc.).
3. Open a Claude Code session in that folder.
4. Claude will read `config.md` automatically and guide you through the workflow.

## Workflow

| Phase | What happens |
|---|---|
| 1. Raw cut | Remove bad takes and off-script content using the screenplay |
| 2. Silence removal | Detect and cut silences with ffmpeg, configurable threshold |
| 3. Animations | Build HTML/CSS animations from script instructions, render to ProRes MOV, place on timeline |

## Slash commands

| Command | What it does |
|---|---|
| `/premierpack` | Package all project files into a final output folder |
| `/premiersilence` | Run silence detection and removal on the active sequence |
| `/premierzoom` | Apply alternating zoom levels to footage clips |
| `/premierduplicate` | Duplicate the active sequence |
| `/premiergoshort` | Cut a 9:16 vertical short from a time range |

## Requirements

See [PREREQUISITES.md](PREREQUISITES.md) for the full list. Short version: Premiere Pro + BuzzRolls, ffmpeg, Python 3, BrokerChooser Private MCP, Figma MCP.
