# Phase 3 — Animations

## Prerequisites

- Phase 2 (silence removal) is complete and approved.
- `visual-instructions.md` exists in the project folder (generated in Phase 1).
- `style/videostyle.md` is loaded.
- The Figma reference page is accessible: `https://www.figma.com/design/TiTLnLU6yyOlOzSh0dfuuh/YouTube-video-content?node-id=1542-67`
- BrokerChooser Private MCP is connected.
- Node.js and Remotion are installed.

## Design rules

All animations must follow these sources in order of priority:

1. **[style/videostyle.md](../style/videostyle.md)** — colors, typography, spacing, corner radius, shadow
2. **Figma reference page** (`node-id=1542-67`) — visual patterns for tables, broker cards, lower thirds
3. **Figma project page** — the page named after this project (created if missing)

Never hardcode colors, font sizes, or spacing. Always reference the design tokens from `videostyle.md`.

## Broker data

When an animation instruction references a broker but does not include specific data (e.g. `overall score`, `logo`, `name`), fetch it from the BrokerChooser Private MCP:
- Broker name, overall score, logo URL → `list-resource-records` / `view-resource-record`

## Animation format

All animations are built as **Remotion React components** and exported as:
- **ProRes 4444 MOV** (transparent alpha) for overlay animations
- **PNG** (transparent background) for static graphic inserts

Both files are saved to the project's `animations/` subfolder.

### Remotion project structure

```
<project_folder>/
└── animations/
    ├── src/
    │   ├── index.tsx
    │   ├── Root.tsx
    │   └── <AnimationName>.tsx    # One file per animation
    ├── public/
    │   └── <logos, images>
    └── out/
        └── <AnimationName>.mov / .png
```

Each animation component gets its own `.tsx` file. `Root.tsx` registers all compositions.

## Stale check

Before placing an animation on the timeline, check whether:
1. A file with the same name already exists in `animations/out/`.
2. The corresponding `.tsx` source file has been modified more recently than the output file.

If the source is newer: warn the user and ask whether to re-render before placing.

## Process

### Step 1 — Parse visual instructions

Read `visual-instructions.md`. For each instruction:
- Identify animation type (table, broker card, lower third, chart, etc.)
- Extract mentioned data (broker names, metric names)
- Note the associated narration timecode

### Step 2 — Fetch missing data

For any instruction that references a broker or metric without providing a value, fetch from BrokerChooser Private MCP.

### Step 3 — Design in Figma first

Before writing code, create the design in Figma on the project page:
- Use components and styles from the design system
- Follow visual patterns from the reference page (`node-id=1542-67`)
- Name each Figma frame after the animation (e.g. `BrokerTable - Pepperstone vs MEXEM`)
- Get screenshot approval from user before building

### Step 4 — Build all animations

Build every animation component. Do not place any on the timeline yet.

For each animation:
- Create `<AnimationName>.tsx` in `animations/src/`
- Register in `Root.tsx`
- Export: `remotion still` for PNG, `remotion render --codec prores --prores-profile 4444` for MOV

### Step 5 — Place all animations

After all animations are rendered, place them on the timeline:
- Find the timecode for each animation from `visual-instructions.md`
- Check that the target track and position is empty before placing
- Use V2 or higher for animation layers (V1 = main footage)
- Name each clip after the animation

### Step 6 — Save

Save the Premiere project. Save the Figma file.

## Animation sizing

Animations do not need to be full screen. Use appropriate sizing:
- **Lower thirds / overlays**: bottom strip, partial width
- **Tables / comparison cards**: centered, sized to content
- **Full-screen graphics**: only when the instruction explicitly calls for it

## Naming

- Figma frames: `<AnimationType> - <Description>` (e.g. `BrokerTable - Pepperstone vs MEXEM`)
- Animation files: `<AnimationType>-<description>.tsx` / `.mov` / `.png`
- Premiere clips: same as animation file name
