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

After installing the package from PyPI:

```sh
pip install rolfedh-doc-utils
```

You can run the tool from anywhere using:

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
- `--exclude-dir` — Directory to exclude (can be used multiple times).
- `--exclude-file` — File to exclude (can be used multiple times).
- `--exclude-list` — Path to a file containing directories or files to exclude, one per line.

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

## Output

- Prints unused images to the terminal.
- Creates a manifest file in the `archive/` directory.
- Optionally creates a zip archive of unused images.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
