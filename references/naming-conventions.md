# Naming Conventions

Every file, sequence, layer, Figma frame, and animation must have a descriptive name. Never leave Premiere defaults (Sequence 01, Video 1, etc.).

## Premiere project bins

Every project must have these bins at the top level:

| Bin | Contents |
|---|---|
| `Footage` | All raw camera clips |
| `Animations` | All imported animation MOVs |
| `Sound & Music` | Music tracks, SFX, any audio-only files |

Create them at the start of the project. Import files directly into the matching bin — never leave clips loose in the project root.

---

## Sequences

| Type | Pattern | Example |
|---|---|---|
| Main edit | `<project> - Main` | `Pepperstone Review - Main` |
| After raw cut | `<project> - Raw Cut` | `Pepperstone Review - Raw Cut` |
| After silence removal | `<project> - Silence Removed` | `Pepperstone Review - Silence Removed` |
| Duplicate | `<original> - <suffix>` | `Pepperstone Review - Main - Color Grade` |
| Short (9:16) | `<project> - Short - <description>` | `Pepperstone Review - Short - Intro` |

## Premiere tracks

| Track | Content |
|---|---|
| V1 | Main footage |
| V2 | Overlay animations, graphics |
| V3+ | Additional layers (b-roll, titles) |
| A1 | Main narration audio |
| A2 | Background music |

## Animation files

| Type | Pattern | Example |
|---|---|---|
| HTML source | `ANIM-<number>_<kebab-description>.html` | `ANIM-15_swap-calendar.html` |
| Rendered video | `ANIM-<number>_<kebab-description>.mov` | `ANIM-15_swap-calendar.mov` |
| Variant | `ANIM-<number><letter>_<kebab-description>.html/.mov` | `ANIM-16B_positive-swap.html` |
| Translated | `<lang>/ANIM-<number>_<kebab-description>.html/.mov` | `de/ANIM-15_swap-calendar.html` |

Use lowercase with hyphens for filenames. No spaces.

## Figma frames

| Pattern | Example |
|---|---|
| `<Type> - <Description>` | `BrokerTable - Pepperstone vs MEXEM` |
| `LowerThird - <Text>` | `LowerThird - Best for beginners` |

## Figma pages

Each Premiere project gets its own Figma page, named after the project file:

```
<project_name>
```

For example, if the Premiere project is `pepperstone-review.prproj`, the Figma page is `pepperstone-review`.

## Footage clips on the timeline

When clips are placed or renamed in Premiere, use the format:
```
<content description> [<take or version if relevant>]
```

Example: `Intro narration`, `Broker comparison narration`, `Outro`.
