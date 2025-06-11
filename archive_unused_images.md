# Archive Unused Image Files

This script scans all directories in your project (including subdirectories) for image files (such as `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) that are *not* referenced in any AsciiDoc (`.adoc`) file within the project.

## What It Does

- **Identifies unused image files**
  - Finds image files anywhere in the project that are not referenced by any `.adoc` file (via `image::`, `image:`, or direct filename references).
- **Generates a manifest**
  - Prints the list of unused image files to the console and writes their paths to a manifest file named `unused-images-<YYYY-MM-DD_HHMMSS>.txt` in the `./archive` directory.
- **Optionally archives and deletes**
  - With `--archive`, creates a zip archive in `./archive` containing all unused image files and the manifest, then deletes the originals.
- **Supports exclusions**
  - You can exclude specific directories or files from scanning using command-line options or a list file (see below).

## Use Case

Ideal for **documentation maintainers** who want to clean up orphaned or unused images in large AsciiDoc projects.

## Usage

To identify unused image files:
```sh
python3 ~/doc-utils/archive_unused_images.py
```

To identify and archive unused image files:
```sh
python3 ~/doc-utils/archive_unused_images.py --archive
```

To exclude specific directories or files:
```sh
python3 ~/doc-utils/archive_unused_images.py --exclude-dir <directory_path> --exclude-file <file_path>
```

To use a file containing exclusions (one per line):
```sh
python3 ~/doc-utils/archive_unused_images.py --exclude-list <file_name>
```

> **Note:** Run this script from the root of your project repository. The archive zip and manifest will be placed in the `./archive` directory.

## Options

| Option            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `--archive`       | Move unused image files to a dated zip in the archive directory and delete originals |
| `--exclude-dir`   | Directory to exclude from scanning (can be used multiple times)              |
| `--exclude-file`  | File to exclude from scanning (can be used multiple times). Must match the full path or relative path, not just the filename. |
| `--exclude-list`  | Path to a file containing directories or files to exclude, one per line      |
| `-h`, `--help`    | Show usage and exit                                                          |

## Examples

Identify unused image files only:
```sh
python3 ~/doc-utils/archive_unused_images.py
```

Identify and archive unused image files:
```sh
python3 ~/doc-utils/archive_unused_images.py --archive
```

Exclude a directory and a file:
```sh
python3 ~/doc-utils/archive_unused_images.py --exclude-dir ./icons --exclude-file ./images/unused1.png
```

Use a file with exclusions:
```sh
python3 ~/doc-utils/archive_unused_images.py --exclude-list exclude.txt
```

## Notes

- The script scans all directories in your project by default. You can change this by editing the `scan_dirs` variable in the script.
- The script skips symlinked directories and files.
- The manifest file is always created in the archive directory, even if no files are archived.
- The script is safe to run multiple times; it will not archive or delete files that are already gone.
- The `--exclude-file` option matches the full or relative path you provide, not just the filename. If you want to exclude all files with a certain name in any directory, specify each path or adjust the script logic.
- The `--exclude-list` file can contain both directories and files, one per line. Lines starting with `#` are ignored as comments.
