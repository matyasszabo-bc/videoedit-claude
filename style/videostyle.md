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

## Colors

| Token | Hex | Usage |
|---|---|---|
| `text-primary` | `#334155` | Broker names, data values |
| `text-secondary` | `#64748b` | Row labels, captions |
| `background-card` | `#ffffff` | Card and table background |
| `background-surface` | `#eff8ff` | Page/scene background |
| `shadow` | `rgba(0,0,0,0.10)` | Card drop shadow |

Background gradient for cards:
```
radial-gradient(circle at 100% 99%, #ffffff 0%, #eff8ff 100%)
```

---

## Spacing & Shape

| Token | Value |
|---|---|
| Card border radius | 64px |
| Logo box border radius | 10px |
| Logo box size | 120×120px |
| Logo image size inside box | 90×90px |
| Card padding | 40px |
| Row height | 86px |
| Gap between logo and broker name | 16px |
| Padding below broker name | 24px |

---

## Shadows

Logo box drop shadow:
```
0px 30px 45px -9px rgba(0,0,0,0.10), 0px 12px 18px -6px rgba(0,0,0,0.05)
```

---

## Table row alternating background

- Even rows (0-indexed): `background: white`, `border-radius: 24px 0 0 24px` (left column) / `0 24px 24px 0` (last column)
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
