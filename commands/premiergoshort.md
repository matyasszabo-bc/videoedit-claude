# /premiergoshort

Cut a 9:16 vertical short from a time range of the current sequence.

## Usage

```
/premiergoshort 00:01:30 00:02:45
/premiergoshort 1:30 2:45 "Pepperstone review highlight"
```

Arguments:
1. Start timecode (required)
2. End timecode (required)
3. Short name/description (optional, used for naming)

## What it does

1. Creates a new sequence with 9:16 aspect ratio (1080×1920) and the same FPS as the source.
2. Copies all clips and layers from the source sequence that appear within the specified time range — including all video tracks (V1, V2, animations, etc.) and audio tracks.
3. Places them in the new sequence starting at 00:00:00, preserving their relative timing.
4. Names the new sequence: `<project_name> - Short - <description or timecode range>`.

## Notes

- Every layer that is visible in the source sequence during the time range is included: footage, animations, graphics, audio.
- Clips that start before the range but extend into it are trimmed to start at the range start.
- Clips that extend past the range end are trimmed at the range end.
- After creation, the new sequence opens as the active sequence.
- The source sequence is not modified.
