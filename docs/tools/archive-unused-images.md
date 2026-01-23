---
layout: default
title: archive-unused-images
nav_order: 8
---

# Archive Unused Images

> ⚠️ **WARNING: This Tool Can Delete Files**
> 
> **ALWAYS:**
> 1. **Create a git branch first**: `git checkout -b cleanup-unused-images`
> 2. **Run without `--archive` first** to preview what will be affected
> 3. **Review the list carefully** - ensure no images are incorrectly marked as unused
> 4. **Check your documentation build** after archiving to ensure no broken image links
> 5. **Keep the archive files** until you're certain the removal was correct

This tool scans the current directory and all subdirectories for image files (e.g., `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them.

## Installation

After [installing the package](../getting-started.md), run the tool from anywhere:

```sh
archive-unused-images [options]
```

Or, if running from source:

```sh
python3 archive_unused_images.py [options]
```

## Usage

See the script's `--help` output or the docstring for all options. Common options include:

- `--archive` — Move the files to a dated zip in the archive directory.
- `--commented` — Include images that are referenced only in commented lines in the archive operation.
- `--exclude-dir` — Directory to exclude (can be used multiple times).
- `--exclude-file` — File to exclude (can be used multiple times).
- `--exclude-list` — Path to a file containing directories or files to exclude, one per line.

## Commented References Behavior

**Default behavior (no flag):**
- Always scans for both uncommented and commented image references when scanning for references
- Images referenced only in commented lines are considered "used" and will NOT be archived
- Generates a detailed report of images referenced only in commented lines
- Report location: `./archive/commented-image-references-report.txt`

**With --commented flag:**
- Include images that are referenced only in commented lines in the archive operation
- These images will be treated as unused and archived along with other unused images

## Examples

Archive unused images while excluding a directory:
```sh
archive-unused-images --archive --exclude-dir ./images/legacy
```

Dry run (see what would be archived without actually archiving):
```sh
archive-unused-images
```

Exclude multiple directories and files:
```sh
archive-unused-images --archive --exclude-dir ./images/icons --exclude-dir ./images/logos --exclude-file ./images/placeholder.png
```

Use an exclusion list file:
```sh
archive-unused-images --archive --exclude-list .docutils-ignore
```

### Working with Commented References

Preview and generate report on commented-only references:
```sh
archive-unused-images
# This will:
# 1. Find unused images (not counting commented references as "used")
# 2. Generate a report of images referenced only in commented lines
# 3. Save report to ./archive/commented-image-references-report.txt
```

Archive images including those with commented-only references:
```sh
archive-unused-images --archive --commented
# This will archive both:
# 1. Images with no references at all
# 2. Images referenced only in commented lines
```

## Output

- Prints unused images to the terminal.
- Creates a manifest file in the `archive/` directory.
- Optionally creates a zip archive of unused images.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
