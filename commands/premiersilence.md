# /premiersilence

Run silence detection and removal on the active sequence. This is a standalone command version of Phase 2.

## Usage

```
/premiersilence
/premiersilence threshold=-35
/premiersilence threshold=-45 padding=8
```

## Parameters

All parameters are optional. Defaults come from `config.md`.

| Parameter | Default | Description |
|---|---|---|
| `threshold` | `silence_threshold_db` from config | dBFS level below which audio is silence |
| `padding` | `silence_padding_frames` from config | Frames kept on each side of a silence |
| `min_silence` | `min_silence_duration_sec` from config | Minimum silence duration to cut |
| `min_burst` | `min_audio_burst_in_silence` from config | Minimum burst inside silence to keep |

## Process

Follows the full process described in [phases/02-silence-removal.md](../phases/02-silence-removal.md).

Always presents a summary and asks for confirmation before applying cuts.
