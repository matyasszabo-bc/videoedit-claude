# Animation Technical Reference

This document covers the exact technical steps for building and exporting animations. Read this alongside [phases/03-animations.md](../phases/03-animations.md).

## Animation source format

Animations are standalone HTML files — fully self-contained, no external dependencies. The HTML contains all CSS, JS, and assets inline (base64 or embedded). It runs the animation when the page loads and a trigger (e.g. a play button or auto-start) is activated.

The stage size is always **1920×1080**.

---

## Rendering HTML → ProRes 4444 MOV

Use `scripts/render-html-to-mov.py` from the skill root. It:
1. Opens the HTML in a headless Chromium (Playwright) at 1920×1080
2. Strips the page background color so the canvas is transparent
3. Starts the animation by calling `run()` (or clicking the play trigger)
4. Captures frames at the specified FPS with `omit_background=True`
5. Encodes them with ffmpeg into ProRes 4444 (alpha channel)

### Usage

```bash
python3 <skill_root>/scripts/render-html-to-mov.py \
  --input  "animations/<AnimationName>.html" \
  --output "animations/out/<AnimationName>.mov" \
  --duration 8.0 \
  --fps 30 \
  --width 1920 \
  --height 1080
```

| Flag | Default | Description |
|---|---|---|
| `--input` | required | Path to the source HTML file |
| `--output` | required | Path for the output `.mov` |
| `--duration` | `8.0` | Total capture duration in seconds |
| `--fps` | `30` | Frames per second |
| `--width` | `1920` | Viewport width |
| `--height` | `1080` | Viewport height |
| `--bg-color` | auto | If the page background is not `#faf9f5`, pass the actual hex to remove it |

### How to determine duration

Read the animation's JS to find the total sequence length. Typical pattern:

```js
const wait = ms => new Promise(r => setTimeout(r, ms));
async function run() {
  await wait(900);       // initial pause
  // ... animation steps with waits
  await wait(260);       // final step
}
```

Add all `wait()` calls plus CSS transition durations. Then **multiply the result by 2** — CSS transitions, easing tails, and pulse/glow animations extend well beyond the last explicit `wait()`. A too-short capture cuts off the ending; a too-long one just adds silent transparent frames that are trivially trimmed in Premiere.

**Default: if unsure, use `--duration 16.0`.**

### Background removal

The script removes the page's background color (default `#faf9f5` — BC off-white). If the animation uses a different page background, pass `--bg-color <hex>` to override which color gets stripped.

Elements with intentional dark backgrounds (e.g. the card at `rgba(10,15,30,0.7)`) are left untouched — only the top-level page background is removed.

---

## Rendering HTML → static PNG

For a single frame snapshot:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def render_png(html_path: str, output_path: str, width=1920, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file://{Path(html_path).resolve()}", wait_until="networkidle")
        page.wait_for_timeout(2000)
        # Remove page background
        page.evaluate("document.body.style.background = 'transparent'")
        page.screenshot(path=output_path, omit_background=True)
        browser.close()
```

---

## Prerequisites

```bash
pip install playwright
playwright install chromium
brew install ffmpeg   # if not already installed
```

Verify:
```bash
python3 -c "import playwright; print('ok')"
ffmpeg -version
```

---

## Placing in Premiere

After rendering:

1. Import the `.mov` or `.png` into Premiere via BuzzRolls `import_media`.
2. Find the timecode from `visual-instructions.md`.
3. Check that the target track (V2 or higher) is empty at that position.
4. Place with `add_to_timeline`.
5. For static PNGs: add a Push (Up) transition via `add_transition_to_clip` using `Effects/Video Transitions/Slide/Push`. Direction must be set manually in Effect Controls.

---

## Common issues

| Problem | Cause | Fix |
|---|---|---|
| White/colored background in output | Page background not stripped | Check `--bg-color`, or manually set `document.body.style.background = 'transparent'` |
| Animation not starting | `run()` not in global scope | Inspect the HTML for the actual trigger function name and call it in the Playwright evaluate step |
| Frames cut off before animation ends | `--duration` too short | Read the JS timing and recalculate; add 1s buffer |
| Dark card appears transparent | Alpha compositing issue in Premiere | Ensure the MOV is placed on V2+ with the footage on V1 |
| `omit_background` has no effect | Background set via CSS on a non-transparent element | Find which element carries the background color and strip it explicitly |
