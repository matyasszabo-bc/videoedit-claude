# Phase 2 — Silence Removal

## Prerequisites

- Phase 1 (raw cut) is complete and approved.
- `config.md` values are set: `silence_threshold_db`, `silence_padding_frames`, `min_silence_duration_sec`, `min_audio_burst_in_silence`.
- ffmpeg is installed.

## Default values (from config.md)

| Setting | Default | Meaning |
|---|---|---|
| `silence_threshold_db` | -40 dBFS | Audio below this level is classified as silence |
| `silence_padding_frames` | 5 | Frames kept before and after each silence boundary |
| `min_silence_duration_sec` | 1.0 | Silences shorter than this are not cut |
| `min_audio_burst_in_silence` | 1.0 | Audio bursts inside a silence shorter than this are also removed |

## Why -40 dBFS

Spoken word in a controlled recording environment typically sits between -20 and -6 dBFS. Room noise and breath usually falls around -50 to -45 dBFS. -40 dBFS is a safe threshold that catches real silences without clipping soft words. Adjust upward (e.g. -35) for noisier recordings, downward (e.g. -45) for very quiet rooms.

## Process

### Step 1 — Export audio for analysis

Export the current audio track from the timeline as a WAV or AAC file using BuzzRolls or Premiere's export frame tools. This is the input for ffmpeg analysis.

### Step 2 — Detect silences

Run silence detection using ffmpeg's `silencedetect` filter:

```bash
ffmpeg -i <audio_file> -af "silencedetect=noise=<threshold>dB:duration=<min_silence>" -f null - 2>&1 | grep silence
```

Parse the output to extract silence start/end pairs. Convert timestamps to timeline timecodes using the sequence FPS from `config.md`.

### Step 3 — Apply padding

For each detected silence:
- Start of cut = silence_start + `silence_padding_frames` (keep audio before silence fades)
- End of cut = silence_end - `silence_padding_frames` (keep audio as it comes back)

### Step 4 — Filter short silences and bursts

- Discard any silence shorter than `min_silence_duration_sec`. These are natural pauses within sentences — do not cut them.
- For any audio burst inside a silence that is shorter than `min_audio_burst_in_silence`, include it in the cut (it is likely a cough, click, or breath).

### Step 5 — Verify cuts do not mid-sentence

Before applying, check each cut boundary against the transcript. A cut must not fall inside a word. If the silence detection lands mid-word, shift the cut boundary to the nearest inter-word gap.

### Step 6 — Present cut list

Show the user a summary:
```
Found 12 silences to remove.
Total time saved: 38 seconds.
Longest silence: 4.2s at 00:02:14
Shortest silence cut: 1.1s at 00:05:33
```

Ask for confirmation before applying.

### Step 7 — Apply

Apply cuts via BuzzRolls ripple delete. Save the project.

## Output

- Timeline with silences removed and natural inter-sentence pacing preserved.
- A `silence-log.txt` saved to the project folder (parent directory of `premiere_project_path` from `config.md`) with all detected silences, cut/kept decisions, and reasons.

## Naming

Name the resulting sequence: `<project_name> - Silence Removed`
