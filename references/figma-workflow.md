# Figma Workflow

## Authentication

Use the `design@brokerchooser.com` Figma account via the MCP configured in `~/.claude/mcp.json` (`figma-brokerchooser` entry). This account has full edit access to the BrokerChooser Figma workspace.

## Reference file

All video design references live in:
```
https://www.figma.com/design/TiTLnLU6yyOlOzSh0dfuuh/YouTube-video-content
```

Key pages:
- `node-id=1542-67` — Reference page: tables, broker cards, comparison layouts, lower thirds

Before building any animation, inspect this reference page to find the closest existing pattern. Build to match.

## Project page

Each Premiere project gets a dedicated Figma page named after the project file (e.g. `pepperstone-review`).

**Creating the project page:**
1. Check if a page with that name already exists.
2. If not, create it.
3. All animation designs for this project go on this page.
4. Name each frame: `<AnimationType> - <Description>` (see naming-conventions.md).

## Design before code

For every animation:
1. Create the design in Figma on the project page first.
2. Use components and styles from the BrokerChooser design system.
3. Reference `style/videostyle.md` for video-specific tokens.
4. Take a screenshot and confirm with the user before building the Remotion component.

This ensures animations match the brand and avoids wasted render time.

## Fetching broker data

When an animation references a broker, fetch data from the BrokerChooser Private MCP:

```
list-resource-records → find broker by name
view-resource-record  → get overall score, logo URL, full name
```

Download the logo as a PNG and save to `animations/public/<broker-slug>.png`.

## Saving designs

After creating or modifying a Figma frame:
- The frame must remain in the project Figma page (do not move or delete it).
- It serves as the editable source for future changes.
- If the animation needs to be updated later, the user edits the Figma frame and Claude re-renders.
