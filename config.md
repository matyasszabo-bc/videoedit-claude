# Project Config

Copy this file into your Premiere Pro project folder and fill in the values marked with `# REQUIRED`.
Claude reads this file at the start of every session.

Do not commit the filled-in version — it contains local paths specific to your machine.

---

## Project

```
project_name:            # REQUIRED — name of the Premiere project file without .prproj
premiere_project_path:   # REQUIRED — absolute path to the .prproj file
footage_folder:          # REQUIRED — absolute path to the raw footage folder
output_folder:           # REQUIRED — absolute path to the final export/delivery folder
```

## Main sequence

```
sequence_name:    # REQUIRED — name of the primary sequence (e.g. "Main - Final")
resolution:       1920x1080
fps:              match_source   # Claude reads FPS from the first footage clip
```

## Silence removal

```
silence_threshold_db:        -40     # Audio below this level is classified as silence (dBFS)
                                     # Adjust up (e.g. -35) for noisy recordings
                                     # Adjust down (e.g. -45) for very quiet rooms
silence_padding_frames:      5       # Frames to keep before and after each silence boundary
min_silence_duration_sec:    1.0     # Silences shorter than this are NOT cut
min_audio_burst_in_silence:  1.0     # Audio bursts inside silence shorter than this are removed
```

## Zoom

```
zoom_level_a:   55    # First alternating zoom level (%)
zoom_level_b:   66    # Second alternating zoom level (%)
```

## Design

```
figma_file_key:         TiTLnLU6yyOlOzSh0dfuuh
figma_reference_node:   1542-67
figma_project_page:     # Leave blank — Claude creates this automatically, named after project_name
```
