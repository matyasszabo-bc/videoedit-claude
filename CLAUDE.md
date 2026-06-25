# CLAUDE.md — BrokerChooser Video Production

This directory is the skill root for BC video post-production.
Project-specific files (sequences, footage, progress trackers) live in the **project folder**, not here.

---

## Reference files — what to read and when

| Situation | Read first |
|---|---|
| Starting a new session / overall workflow | [`SKILL.md`](SKILL.md) |
| Any animation work | [`phases/03-animations.md`](phases/03-animations.md) |
| Design tokens (colors, typography) | [`style/videostyle.md`](style/videostyle.md) |
| Figma access / BrokerChooser MCP | [`references/figma-workflow.md`](references/figma-workflow.md) |
| Naming files, sequences, tracks | [`references/naming-conventions.md`](references/naming-conventions.md) |
| Creating a translated version | [`references/translate.md`](references/translate.md) |
| Animation gotchas (rAF, MOGRT, inline-block) | [`references/de-render-lessons.md`](references/de-render-lessons.md) |

---

## Folder structure

### Skill root (this folder)
```
Vagas/
├── CLAUDE.md
├── SKILL.md
├── phases/
│   ├── 01-raw-cut.md
│   └── 03-animations.md
├── style/
│   └── videostyle.md
├── references/
│   ├── figma-workflow.md
│   ├── naming-conventions.md
│   ├── translate.md
│   └── de-render-lessons.md
├── commands/
│   ├── premierduplicate.md
│   ├── premiersilence.md
│   ├── premierpack.md
│   ├── premiergoshort.md
│   └── premierzoom.md
└── scripts/
    └── render-html-to-mov.py
```

### Project folder
```
<project>/
├── <project>.prproj
├── config.md                  ← copied from skill root, filled in
├── EDIT-PROGRESS.md           ← update after each animation
├── visual-instructions.md     ← generated during raw cut phase
└── animations/
    ├── ANIM-XX_name.html      ← HTML source (flat: html+mov together)
    ├── ANIM-XX_name.mov       ← rendered ProRes 4444
    └── <lang>/                ← translated versions (e.g. de/, fr/)
        ├── ANIM-XX_name.html
        └── ANIM-XX_name.mov
```

**Keep flat structure within each language folder.** Never move files mid-project — it breaks Premiere clip references.
