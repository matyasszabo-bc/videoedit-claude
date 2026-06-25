# Animation Technical Gotchas

Lessons learned from production — apply these to all animations, not just translations.

---

## setInterval / setTimeout — do not use for animation progress

### The problem
Playwright's headless event loop runs much faster than real time. `setInterval` / `setTimeout` fire many times per rendered frame:

- `setInterval(fn, 100)` animation: renders ~5–10× too fast
- `async/await wait(ms)` pattern: the whole animation completes in the first frame

### The rule
> **Use `requestAnimationFrame` + elapsed time — never `setInterval` or `setTimeout` for animation progress.**
> See [`phases/03-animations.md`](../phases/03-animations.md) for the canonical code pattern.

### Fix — rewrite to rAF

```js
// ❌ Wrong
const iv = setInterval(() => {
  f++;
  // animation logic
}, 100);

// ✅ Correct
function tick() {
  f++;
  // animation logic
  if (!done) requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
```

The render script's deterministic rAF driver also handles `setInterval`/`setTimeout` via a fake clock, so `async/await wait()` patterns are safe — but explicit rAF is still preferred.

### Check before rendering
```bash
grep -n "setInterval\|setTimeout" animations/ANIM-XX_*.html
```
If there's a hit: convert to rAF, or confirm the fake clock covers it (async/await case).

---

## MOGRT text clips — cannot be edited via API

### The problem
Premiere's UXP API exposes MOGRT (`ComponentChain`) text parameters as `keyframesSupported: false`. Calling `createKeyframe()` throws "Illegal Parameter type". Text in MOGRTs **cannot be changed programmatically**.

### The fix — replace MOGRT with an HTML animation

**1. List all MOGRT clips in the sequence**

MOGRTs are `.aegraphic` project items. They can appear on multiple tracks (V3, V4, etc.). Check all video tracks:

```
get_timeline_state → iterate all videoTrack clips → filter media path for ".aegraphic"
```

**2. For each MOGRT clip, note:**
- `startTime` (seconds)
- `dur` (seconds)
- track (`V3`, `V4`, etc.)
- text content (from screenshot or user)

**3. Build an HTML animation as replacement**

Text card template:
- Position: `left:50%; top:50%; transform:translate(-50%,-50%); text-align:center`
- Font: IBM Plex Sans SemiBold 600, 140–160px, white
- One word per `LINES` entry — **never put two words in one string** (inline-block spaces collapse, words run together)
- For multi-word lines: use `margin-right: 0.3em` on the span

**4. Render and place**

```bash
python3 scripts/render-html-to-mov.py \
  --input animations/TEXT-XX_name.html \
  --output animations/TEXT-XX_name.mov \
  --duration 4 --bg-color ""
```

Place on a track above the MOGRT (V3 → use V4, etc.). Always check track state first:
```
get_timeline_state → confirm target track is free → insert_clip overwrite
```

**Track index mapping** (trackIndex in insert_clip):

| Premiere track | trackIndex |
|---|---|
| V1 | 0 |
| V2 | 1 |
| V3 | 2 |
| V4 | 3 |
| V5 | 4 |

Note: verify the actual track name from `get_timeline_state` — trackIndex and track name can diverge if there are empty tracks in the sequence.

---

## Inline-block space collapse bug

When building text animations with `inline-block` spans, trailing spaces inside `textContent` collapse and words run together.

```js
// ❌ Wrong — trailing space collapses in inline-block
sp.textContent = word + ' ';

// ✅ Fix A — one word per line (recommended)
const LINES = [['Versteckte'], ['Gebühren']];

// ✅ Fix B — multiple words on one line: use margin-right
sp.style.cssText = '...;margin-right:0.3em;';
```
