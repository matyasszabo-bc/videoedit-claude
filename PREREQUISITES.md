# Prerequisites

Run `scripts/check-prerequisites.sh` to automatically verify all tools. The script will print what is missing and where to get it.

## Required tools

| Tool | Purpose | How to install |
|---|---|---|
| **Adobe Premiere Pro** | Timeline editing, export | https://www.adobe.com/products/premiere.html |
| **BuzzRolls MCP** | Premiere Pro MCP bridge (transcript, timeline control) | https://buzzrolls.studio — install the CEP panel, start the bridge before each session |
| **ffmpeg** | Audio analysis, silence detection, ProRes render | `brew install ffmpeg` |
| **Node.js ≥ 18** | Remotion renderer | https://nodejs.org |
| **Remotion** | React-to-video animation renderer | `npm install -g remotion` (or per-project) |
| **BrokerChooser Private MCP** | Broker data: names, scores, logos | Internal — configured in `~/.claude/mcp.json` |
| **Figma MCP** | Design reference and asset export | Configured in `~/.claude/mcp.json` with `design@brokerchooser.com` PAT |
| **Python 3** | Silence detection helper script | `brew install python3` |

## MCP configuration

The following entries must be present in `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "figma-brokerchooser": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp",
      "headers": {
        "Authorization": "Bearer <design@brokerchooser.com PAT>"
      }
    },
    "brokerchooser-private": {
      "...": "internal config"
    }
  }
}
```

## BuzzRolls setup

1. Install the BuzzRolls CEP panel in Premiere Pro.
2. Open Premiere Pro and open your project.
3. Go to **Window → Extensions → BuzzRolls Studio**.
4. Click **Start Bridge** before each session. Without this, all MCP timeline calls will time out.

## Checking the setup

```bash
bash scripts/check-prerequisites.sh
```

The script checks: ffmpeg, node, remotion, python3, and whether the MCP entries exist in `~/.claude/mcp.json`.
