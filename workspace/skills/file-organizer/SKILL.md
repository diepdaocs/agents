---
name: file-organizer
description: "Organize files and directories by moving, renaming, or sorting them into structured folders. Use when: user wants to clean up a directory, sort downloads, batch-rename files, or tidy a project folder. NOT for: deleting files (confirm first), cloud storage sync, or large recursive operations without explicit approval."
metadata:
  {
    "openclaw":
      {
        "emoji": "🗂️",
        "requires": { "bins": ["find", "mv", "mkdir"] },
      },
  }
---

# File Organizer Skill

Organize messy directories by sorting, renaming, or restructuring files.

## When to Use

✅ **USE this skill when:**

- "Clean up my Downloads folder"
- "Sort these files by type / date / project"
- "Rename all these screenshots to something sensible"
- "Move all PDFs into a folder called docs"
- "Tidy up this directory"

## When NOT to Use

❌ **DON'T use this skill when:**

- User wants to **delete** files — confirm explicitly before any `rm`
- The target directory has > 500 files — propose a plan first, then execute in batches
- Files are in cloud-synced folders (Dropbox, iCloud, Google Drive) — warn about sync conflicts

## Workflow

1. **Understand the goal** — ask if the request is ambiguous (what counts as "organized"?).
2. **Inspect the directory first** — `ls -la` or `find . -maxdepth 1` to see what's there.
3. **Propose a plan** — briefly describe what you'll do before moving anything.
4. **Execute** — use `mv`, `mkdir -p`, `find ... -exec mv`, etc.
5. **Summarize** — report what was moved/renamed and the resulting structure.

## Common Patterns

### Sort by extension
```bash
# Move all PDFs
find ~/Downloads -maxdepth 1 -name "*.pdf" -exec mv {} ~/Documents/pdfs/ \;

# Move all images
find ~/Downloads -maxdepth 1 \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) \
  -exec mv {} ~/Pictures/sorted/ \;
```

### Sort by date (year/month folders)
```bash
for f in ~/Downloads/*; do
  d=$(date -r "$f" +"%Y/%m")
  mkdir -p ~/Downloads/sorted/"$d"
  mv "$f" ~/Downloads/sorted/"$d"/
done
```

### Batch rename (add prefix / fix naming)
```bash
# Prepend date to files
for f in *.png; do mv "$f" "$(date +%Y%m%d)_$f"; done

# Lowercase all filenames
for f in *; do mv "$f" "${f,,}"; done
```

## Safety Rules

- Never delete without explicit confirmation.
- Always `mkdir -p` before `mv` to avoid errors.
- If a destination file already exists, report the conflict — don't silently overwrite.
- For large batches (> 50 files), show a dry-run preview first.
