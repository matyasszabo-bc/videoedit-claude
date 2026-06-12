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

All animations are built as **standalone HTML files** and exported as:
- **ProRes 4444 MOV** (transparent alpha) for overlay animations
- **PNG** (transparent background) for static graphic inserts

Both files are saved directly to the project's `animations/` subfolder (no `out/` subdirectory).

### File structure

```
<project_folder>/
└── animations/
    ├── <AnimationName>.html    # Source animation (standalone, self-contained)
    └── <AnimationName>.mov     # Rendered ProRes 4444 output
```

### Rendering HTML → MOV

Use `scripts/render-html-to-mov.py` from the skill root. See [animation-technical.md](../video-skill/references/animation-technical.md) for full details and options.

```bash
python3 <skill_root>/scripts/render-html-to-mov.py \
  --input  "<project>/animations/<AnimationName>.html" \
  --output "<project>/animations/<AnimationName>.mov" \
  --duration 10.0
```

Default: 1920×1080, 30fps. Only pass `--width`/`--height`/`--fps` to override. Always use `--input`/`--output` named flags — positional args are not supported.

## Stale check

Before placing an animation on the timeline, check whether a `.mov` with the same name already exists in `animations/`. If the `.html` source is newer than the `.mov`, warn the user and ask whether to re-render before placing.

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
- Save the standalone HTML to `animations/<AnimationName>.html`
- Run `scripts/render-html-to-mov.py` to produce the MOV in `animations/out/`
- For static PNG: take a single screenshot with Playwright (`omit_background=True`) at the correct frame

### Step 5 — Place all animations

After all animations are rendered, place them on the timeline:
- Find the timecode for each animation from `visual-instructions.md`
- Check that the target track and position is empty before placing
- Use V2 or higher for animation layers (V1 = main footage)
- Name each clip after the animation

### Step 6 — Save

Save the Premiere project. Save the Figma file.

## HTML animation code pattern

Every animation HTML must follow this exact structure — no exceptions:

```js
// 1. Easing functions (easeOutCubic, easeOutBack, easeInOutCubic as needed)

// 2. Task scheduler
const tasks = [];
function at(startMs, durationMs, fn) { tasks.push({startMs, durationMs, fn}); }
function tick(elapsed) {
  for (const t of tasks) {
    if (elapsed < t.startMs) continue;
    t.fn(Math.min(1, (elapsed - t.startMs) / t.durationMs));
  }
}

// 3. Schedule all keyframes with at()
at(0, 900, p => { /* fade in */ });
at(1400, 1100, p => { /* flip */ });
// ...

// 4. RAF loop — time-driven, NOT frame-counted
let startTime = null, running = false;

function loop(ts) {
  if (!startTime) startTime = ts;
  const elapsed = ts - startTime;
  tick(elapsed);
  // continuous effects (pulse glow, etc.) go here
  if (running) requestAnimationFrame(loop);
}

// 5. Public start() — called by renderer and by click in browser preview
function start() {
  if (running) return;
  running = true;
  startTime = null;
  requestAnimationFrame(loop);
}

// Click-to-start for browser preview testing
document.addEventListener('click', () => { if (!running) start(); });
```

**Rules:**
- `start()` must exist as a named global function — the renderer calls it.
- Never auto-start on load (`start()` at the top level is forbidden).
- Never use `setInterval` — always `requestAnimationFrame` + elapsed time.
- All animation progress values `p` run 0→1; apply easing inside the callback.
- Transparent canvas: never set a solid `body` background — footage shows through.

## Animation timing

All animations must feel slow and deliberate — the viewer is watching on a large screen and needs time to read every value.

**Default durations (treat as minimums):**

| Event | Duration |
|---|---|
| Card / scene fade-in | 800–1000ms |
| Element slide-in / stagger step | 500–700ms |
| Value pop-in (easeOutBack) | 600–800ms |
| Flip / transform (easeInOutCubic) | 1000–1200ms |
| Stagger delay between siblings | 200–300ms |
| Hold on final state before loop ends | ≥2000ms |

**Total animation length:** aim for 8–10s of visible motion before the loop settles into the hold state. The renderer `--duration` flag should be set to at least `total motion time + 2s hold`.

Never rush element reveals. If something animates in under 400ms it will feel like a glitch, not a transition.

## Animation sizing

Animations do not need to be full screen. Use appropriate sizing:
- **Lower thirds / overlays**: bottom strip, partial width
- **Tables / comparison cards**: centered, sized to content
- **Full-screen graphics**: only when the instruction explicitly calls for it

## Naming

- Figma frames: `<AnimationType> - <Description>` (e.g. `BrokerTable - Pepperstone vs MEXEM`)
- Animation files: `<AnimationType>-<description>.tsx` / `.mov` / `.png`
- Premiere clips: same as animation file name
