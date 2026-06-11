# Phase 1 — Raw Cut

## Prerequisites

- Premiere Pro is open with the project loaded.
- BuzzRolls Bridge is running.
- A **transcript** has been generated inside Premiere Pro (BuzzRolls → Transcribe). This is required for timecode-accurate cuts.
- The **screenplay** has been uploaded to this session. If not, ask the user before proceeding.

## What counts as a cut

### Keep
- The **last good take** of any sentence or paragraph. If the narrator re-records a line, keep only the final version.
- All narration that matches the screenplay.

### Remove
- **Bad takes**: earlier versions of re-recorded lines.
- **Off-script content**: conversations between the camera operator and the narrator, false starts not retaken, coughs mid-sentence that break the line (cough-only clips are handled in Phase 2).
- **Long pauses between takes** that are clearly not part of the narration.

## Reading the screenplay

The screenplay contains both narration and visual instructions. Visual instructions are marked with keywords such as:

```
visual:, animation:, image:, table:, chart:, graphic:, lower third:, b-roll:
```

**Skip all visual instruction lines when cutting.** Only the narration lines matter for Phase 1. Visual instructions are used in Phase 3 (Animations).

Example screenplay block:
```
The best broker for beginners is Pepperstone.

[visual: broker table - Pepperstone vs MEXEM, overall score]

Their overall score is 4.4 out of 5.
```
→ Cut to: "The best broker for beginners is Pepperstone." → keep gap → "Their overall score is 4.4 out of 5."
→ The `[visual: ...]` line is logged for Phase 3 and skipped here.

## Process

1. Load the transcript from BuzzRolls (`get_transcript`). Save it to a local `.txt` file so it can be reused without re-fetching.
2. Parse the screenplay: separate narration lines from visual instruction lines. Store visual instructions with their associated timecodes for Phase 3.
3. Compare transcript timecodes against the screenplay narration. For each line:
   - Find all matching takes in the transcript.
   - Mark all but the last as cuts.
4. Identify off-script regions (transcript content that has no match in the screenplay narration).
5. Present the cut list to the user for review before applying.
6. Apply cuts via BuzzRolls (`ripple_delete` or equivalent).
7. Save the Premiere project after cutting.

## Output

- A cleaned timeline with only the final narration takes.
- A `visual-instructions.md` file saved to the project folder (parent directory of `premiere_project_path` from `config.md`), listing every visual instruction with its approximate timecode. This file is consumed in Phase 3.

## Naming

Name the sequence: `<project_name> - Raw Cut`
