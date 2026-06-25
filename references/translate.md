# Translation workflow — creating a new language version

Read this whenever a new language version needs to be created from an existing one.

---

## Principles

- **Every animation contains text** — there is no ANIM or TEXT clip that can be reused without changes. Check every file.
- **No MOGRTs** in the sequence — those have already been replaced with HTML animations.
- **Folder structure:** each language gets its own subfolder inside `animations/`:
  ```
  animations/
  ├── ANIM-XX_name.html      ← source language (flat)
  ├── ANIM-XX_name.mov
  └── <lang>/                ← translated version (e.g. de/, fr/)
      ├── ANIM-XX_name.html
      └── ANIM-XX_name.mov
  ```
  `<lang>` is lowercase: `de`, `fr`, `es`, etc.

---

## Steps

### 1. Duplicate the sequence

Duplicate the source language sequence with the new name:

```
Final_DE → duplicate → Final_FR
```

The duplicate still points to the source language files — replace them in the following steps.

### 2. Map all texts

Before rendering anything, **read all source HTML files** and list every translatable string. Grep helper:

```bash
grep -n "LINES\|textContent\|label\|title\|text" animations/de/ANIM-*.html \
  | grep -v "//\|style\|class\|font\|color\|px\|transform"
```

Build a table: `file | source text | target translation` — and **ask the user for the translations**. Do not translate automatically.

### 3. Copy HTML files and replace text

Copy each source HTML to the new language folder, then update the strings:

```bash
cp animations/de/ANIM-01_name.html animations/fr/ANIM-01_name.html
```

**Rules:**
- **LINES array:** one word per entry, never `['word1 word2']` in a single string — inline-block spans collapse spaces. Use `['word1', 'word2']` on one line, or separate entries.
- **Spaces between words on the same line:** use `margin-right: 0.3em` on the span (not `textContent = w + ' '`).
- **No setInterval / setTimeout:** grep before rendering:
  ```bash
  grep -n "setInterval\|setTimeout" animations/fr/ANIM-XX_*.html
  ```
  If there's a hit, convert to rAF. See [`references/de-render-lessons.md`](de-render-lessons.md).

### 4. Render

```bash
python3 scripts/render-html-to-mov.py \
  --input animations/fr/ANIM-XX_name.html \
  --output animations/fr/ANIM-XX_name.mov \
  --duration <sec>
```

`--duration`: `(last at() start + duration) / 1000 + 3` seconds minimum.

Always **save the HTML before rendering** — a MOV without its HTML source cannot be edited later.

### 5. Swap clips in the target sequence

Replace each source language MOV with the corresponding target language MOV:

```
① get_timeline_state → identify clip position and track
② relink_media or insert_clip (overwrite mode)
③ get_timeline_state again → verify the swap is correct
```

**Never assume a track is free** — always query first.

### 6. Verify

- [ ] No references to the source language folder remain in the target sequence
- [ ] All clips load from `animations/<lang>/`
- [ ] Texts are correct in preview
- [ ] EDIT-PROGRESS.md updated

---

## Common errors

| Error | Cause | Fix |
|---|---|---|
| Words run together (`FraisForex`) | `textContent = w + ' '` in inline-block | `margin-right: 0.3em` or separate LINES entries |
| Animation is already complete on frame 1 | `setInterval` before fake clock | Convert to rAF |
| Clip cuts its neighbour | Insert without checking track | `get_timeline_state` with rangeStart/End first |
| Missing animations | Only checked TEXT files | **Every ANIM file also contains text** |

---

## References

- Animation rules: [`phases/03-animations.md`](../phases/03-animations.md)
- Technical gotchas (rAF, MOGRT, inline-block): [`references/de-render-lessons.md`](de-render-lessons.md)
- Design tokens: [`style/videostyle.md`](../style/videostyle.md)
