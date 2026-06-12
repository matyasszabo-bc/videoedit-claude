# BrokerChooser Video Style Guide

This file contains the design tokens and visual rules for BrokerChooser YouTube video animations. It is a subset of the full BrokerChooser design system — only properties relevant to video production are included here.

Hover states, focus rings, UX review elements, and other web-only properties are intentionally omitted.

**Source of truth**: The BrokerChooser design system and the Figma reference page:
`https://www.figma.com/design/TiTLnLU6yyOlOzSh0dfuuh/YouTube-video-content?node-id=1542-67`

Always verify token values against the Figma file before building an animation. If a value here conflicts with Figma, Figma wins.

---

## Typography

Font family: **IBM Plex Sans**

| Role | Weight | Size (1080p canvas) |
|---|---|---|
| Broker name / headline | 600 (SemiBold) | 36px |
| Score / data value | 500 (Medium) | 30px |
| Row label | 400 (Regular) | 30px |
| Caption / footnote | 400 (Regular) | 24px |

---

## Dark style — mandatory for all video animations

All animations use a **dark visual style**. The BC website is light — video overlays are dark so they contrast against talking-head footage.

### Scene / page background

The animation canvas is transparent. Never set a solid page background — the footage shows through.

### Cards and data panels (elements containing numbers, charts, tables)

| Rule | Value |
|---|---|
| Minimum background opacity | **66% (0.66)** — never more transparent than this |
| Base background | `rgba(10, 15, 30, 0.75)` — dark navy, 75% opacity |
| Border | `1px solid rgba(255,255,255,0.10)` |
| Border radius | **32px minimum** — prefer 40–48px; never use flat/square corners |
| Backdrop blur | `blur(12px)` on the card element |

Card background gradient (apply on top of the base rgba):
```css
background:
  linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.00) 60%),
  rgba(10, 15, 30, 0.75);
```

### Colors

| Token | Value | Usage |
|---|---|---|
| `text-primary` | `#f1f5f9` | Main values, headlines |
| `text-secondary` | `#94a3b8` | Labels, captions |
| `accent-green` | `#10b981` | Positive values, gains |
| `accent-red` | `#ef4444` | Negative values, losses, warnings |
| `accent-blue` | `#3b82f6` | Neutral highlights, links |
| `surface-dark` | `rgba(10, 15, 30, 0.75)` | Card / panel background |
| `border-subtle` | `rgba(255,255,255,0.10)` | Card borders |

Brand green (`#10b981`) and red (`#ef4444`) come from the BC design system — do not change them.

### Glow effects

Every card and prominent number must have a glow. Use `box-shadow` with the relevant accent color:

```css
/* Green glow — positive value panels */
box-shadow:
  0 0 40px rgba(16, 185, 129, 0.25),
  0 0 80px rgba(16, 185, 129, 0.10),
  0 20px 60px rgba(0, 0, 0, 0.50);

/* Red glow — negative / warning panels */
box-shadow:
  0 0 40px rgba(239, 68, 68, 0.25),
  0 0 80px rgba(239, 68, 68, 0.10),
  0 20px 60px rgba(0, 0, 0, 0.50);

/* Neutral blue glow — default / info panels */
box-shadow:
  0 0 40px rgba(59, 130, 246, 0.20),
  0 0 80px rgba(59, 130, 246, 0.08),
  0 20px 60px rgba(0, 0, 0, 0.50);
```

Large numbers (scores, profit values) get a `text-shadow` too:
```css
/* e.g. a green score number */
text-shadow: 0 0 30px rgba(16, 185, 129, 0.60);
```

### Gradients

Use accent-color gradients on decorative elements (arcs, halos, dividers):

```css
/* Background halo / arc behind card */
background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);

/* Divider line */
background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);

/* Score bar fill */
background: linear-gradient(90deg, #10b981, #34d399);
```

---

## Spacing & Shape

| Token | Value |
|---|---|
| Card border radius | **40px** (minimum 32px — never flat) |
| Inner element border radius | 20px |
| Logo box border radius | 16px |
| Logo box size | 120×120px |
| Logo image size inside box | 90×90px |
| Card padding | 40px |
| Row height | 86px |
| Gap between logo and broker name | 16px |
| Padding below broker name | 24px |

---

## Shadows

Card drop shadow (always dark and deep):
```css
0px 40px 80px rgba(0,0,0,0.60), 0px 16px 32px rgba(0,0,0,0.40)
```

Logo box shadow:
```css
0px 30px 45px -9px rgba(0,0,0,0.40), 0px 12px 18px -6px rgba(0,0,0,0.30)
```

---

## Table row alternating background

- Even rows (0-indexed): `background: rgba(255,255,255,0.05)`, `border-radius: 24px 0 0 24px` (left column) / `0 24px 24px 0` (last column)
- Odd rows: transparent background

---

## Animation canvas

All animations are built on a **1920×1080** transparent canvas unless the instruction specifies otherwise.

Animations do not need to fill the screen. Size to content and position appropriately:
- Lower thirds: bottom 25% of frame, full width or partial
- Tables / comparison cards: centered, natural width (~1100px for a 2-broker table)
- Full-screen: only when explicitly required

---

## Transitions

When adding an animation to the timeline, use Premiere's **Push (Up)** transition from `Effects > Video Transitions > Slide > Push` unless the screenplay specifies otherwise.
