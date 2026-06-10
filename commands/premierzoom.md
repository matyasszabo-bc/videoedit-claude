# /premierzoom

Apply alternating zoom levels to footage clips on the main video track.

## Usage

```
/premierzoom
/premierzoom 55 70
/premierzoom 60
```

- No arguments: use `zoom_level_a` and `zoom_level_b` from `config.md` (default 55% and 66%).
- Two arguments: override both zoom levels.
- One argument: apply a single zoom level to all clips (no alternating).

## What it does

1. Gets all clips on the main footage track (V1) of the active sequence.
2. Applies zoom levels alternately: clip 1 → level A, clip 2 → level B, clip 3 → level A, ...
3. Zoom is applied via Premiere's Motion effect (`Scale` parameter). The anchor point stays centered.
4. Each clip gets a label comment showing the applied zoom level.

## Notes

- Only applies to clips on V1. Animation layers (V2+) are not affected.
- If a clip already has a non-default Scale value set, ask the user before overwriting.
- Zoom is applied uniformly (no keyframes). The effect is a static scale for the full clip duration.
