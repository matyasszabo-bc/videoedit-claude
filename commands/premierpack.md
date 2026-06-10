# /premierpack

Package all files related to the current project into a single output folder. Similar to Premiere's Project Manager, but also includes HTML/React animation sources.

## What gets collected

| Source | Destination |
|---|---|
| All footage referenced in the sequence | `pack/footage/` |
| All exported animation files (`.mov`, `.png`) | `pack/animations/out/` |
| All animation source files (`animations/src/`) | `pack/animations/src/` |
| The Premiere project file (`.prproj`) | `pack/` |
| `config.md` | `pack/` |
| `visual-instructions.md` | `pack/` |
| `silence-log.txt` | `pack/` |

## Process

1. Read `config.md` to get `output_folder` and `project_name`.
2. Create `<output_folder>/<project_name>-pack/` if it does not exist.
3. Use BuzzRolls `get_project_items` to list all media referenced in the project.
4. Copy each file to its destination subfolder.
5. Copy animation sources and outputs.
6. Copy the project file and support docs.
7. After copying, verify that all referenced media in the `.prproj` can still be resolved from the new paths (relink if needed).
8. Report: total size, file count, any missing/unresolvable files.

## Notes

- Do not delete files from their original location until the user explicitly confirms the pack is complete.
- If a file is already in the output folder, skip it (do not overwrite without asking).
