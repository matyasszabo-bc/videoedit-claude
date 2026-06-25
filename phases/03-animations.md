# Phase 3 — Animations

## Prerequisites

- Phase 2 (silence removal) is complete and approved.
- `visual-instructions.md` exists in the project folder.
- `style/videostyle.md` is loaded.
- Figma MCP is accessible (`figma-brokerchooser` entry in `~/.claude/mcp.json`).
- BrokerChooser Private MCP is connected.

---

## Folder structure

```
<project>/animations/
  ANIM-XX_name.html   ← HTML source (always save this alongside the MOV)
  ANIM-XX_name.mov    ← rendered ProRes 4444
```

Keep flat — HTML and MOV live next to each other. Never move files mid-project; it breaks Premiere clip references.

---

## Design rules

All animations must follow these sources (priority order):
1. **[style/videostyle.md](../style/videostyle.md)** — colors, typography, spacing, corner radius, shadow
2. **Figma reference page** (`node-id=1542-67`) — visual patterns
3. **Figma project page** — per-project designs

Never hardcode colors, font sizes, or spacing.

**Card background:** always `rgba(10,15,30,0.75–0.85)` — never white or light. White backgrounds show as opaque rectangles over footage.

---

## HTML animation code pattern

Every animation HTML must follow this exact structure:

```js
// 1. Easing functions
function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
function easeOutBack(t) {
  const c1 = 1.70158, c3 = c1 + 1;
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
}
function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// 2. Task scheduler
const tasks = [];
function at(startMs, durationMs, fn) { tasks.push({ startMs, durationMs, fn }); }
function tick(elapsed) {
  for (const t of tasks) {
    if (elapsed < t.startMs) continue;
    t.fn(Math.min(1, (elapsed - t.startMs) / t.durationMs));
  }
}

// 3. Schedule all keyframes with at()
// ← see Timing section below for gap rules

// 4. RAF loop — time-driven, NOT frame-counted
let startTime = null, running = false;

function loop(ts) {
  if (!startTime) startTime = ts;
  const elapsed = ts - startTime;
  tick(elapsed);
  // continuous effects (pulse glow, etc.) go here
  if (running) requestAnimationFrame(loop);
}

// 5. Public start() — called by renderer and click in browser preview
function start() {
  if (running) return;
  running = true;
  startTime = null;
  requestAnimationFrame(loop);
}

document.addEventListener('click', () => { if (!running) start(); });
```

### Rules
- `start()` must exist as a named global — the renderer tries `run()`, `start()`, `play()` in that order. Use `start()` as the convention.
- **Never auto-start on load.** No `start()` at top level or in `DOMContentLoaded`.
- **Use `requestAnimationFrame` + elapsed time** — never `setInterval` or `setTimeout` for animation progress. In headless Playwright, `setInterval` fires multiple times per rendered frame, making the animation 2–3× too fast.
- Transparent canvas: `background: transparent` on `body`, never solid.
- `omit_background=True` in Playwright is required — already handled by the render script.

---

## Animation timing

**The most important rule: every phase needs breathing room before the next one starts.**

Minimum gap between phases: **600–800ms** after the previous phase completes.
If phases fire immediately back-to-back, the animation feels rushed even at the correct speed.

### Duration minimums

| Event | Duration |
|---|---|
| Card / scene fade-in | 700–900ms |
| Element slide-in / stagger step | 500–700ms |
| Value pop-in (easeOutBack) | 600–800ms |
| Flip / transform (easeInOutCubic) | 1000–1400ms |
| Stagger delay between siblings | 250–350ms |
| Gap between phases | 600–800ms |
| Hold on final state | ≥ 2500ms |

### How to calculate `at()` offsets

Work phase by phase. After each phase ends, add the gap before the next:

```
Phase A: at(0, 800, ...)           → ends at 800ms
Gap:     800ms
Phase B: at(1600, 1200, ...)       → ends at 2800ms
Gap:     700ms
Phase C: at(3500, 600, ...)        → ends at 4100ms
Hold:    2500ms
Total:   6600ms → use --duration 10
```

---

## Rendering HTML → MOV

### Command

```bash
python3 <skill_root>/scripts/render-html-to-mov.py \
  --input  "<project>/animations/ANIM-XX_name.html" \
  --output "<project>/animations/ANIM-XX_name.mov" \
  --duration <seconds>
```

Default: 1920×1080, 30fps. Only pass `--width`/`--height`/`--fps` to override.

### Duration formula

```
--duration = (last_at_start_ms + last_at_duration_ms) / 1000 + 3
```

Round up to the nearest whole second. The +3s gives a clean hold on the final state.
The script default is `16s` — safe for most animations. Only calculate explicitly if the animation is longer or shorter than 13s.

### How the renderer works (important)

The script injects a **deterministic rAF driver** into the page before `start()` is called:
- Overrides `performance.now()` with a fake counter
- Overrides `requestAnimationFrame` with a manually driven queue
- Each frame: `__tickFrame(33ms)` advances the fake clock and fires all pending rAF callbacks synchronously
- Screenshot is taken after the callbacks complete

**Result:** MOV speed is identical to browser preview, regardless of screenshot overhead. This is why `requestAnimationFrame` + elapsed time is mandatory — the fake rAF driver controls the timestamps.

### Stale check

Before rendering, check if a `.mov` with the same name already exists and the `.html` is newer. If so, warn the user and confirm re-render.

---

## Versioning

- B/C/D variants: `ANIM-16B_positive-swap.html` / `.mov`
- **Never overwrite the A version** with a B version
- Place the requested version on the timeline; keep all versions in `animations/`

---

## Premiere placement

1. Call `get_timeline_state` with `rangeStart`/`rangeEnd` around the target timecode — verify the track is empty.
2. Use `insert_clip` with `mode: overwrite`, `noAudio: true`, `trackIndex: 1` (V2).
3. After placing, update `EDIT-PROGRESS.md`.

---

## Process

### Step 1 — Parse visual instructions

Read `visual-instructions.md`. For each instruction:
- Identify animation type (table, broker card, lower third, chart, etc.)
- Extract mentioned data (broker names, metric names, values)
- Note the associated narration timecode

### Step 2 — Fetch missing data

For any instruction that references a broker or metric without a value, fetch from the BrokerChooser Private MCP.

### Step 3 — Design in Figma first

Before writing code:
- Create the design in Figma on the project page
- Use components and styles from the design system
- Follow visual patterns from reference page (`node-id=1542-67`)
- Get screenshot approval from user before building

### Step 4 — Build & render

For each animation:
1. Save HTML to `animations/ANIM-XX_name.html`
2. Test in browser preview (click to start)
3. Run renderer → `animations/ANIM-XX_name.mov`

### Step 5 — Place on timeline

After rendering, place on the timeline per the Premiere placement rules above.

### Step 6 — Save

Save the Premiere project.

---

## Naming

- HTML + MOV: `ANIM-<number>_<kebab-description>` (e.g. `ANIM-15_swap-calendar`)
- Variants: `ANIM-16B_positive-swap`
- Premiere clips: same as file name
