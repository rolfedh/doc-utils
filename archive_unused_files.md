# Archive Unused AsciiDoc Files

This script scans the `./modules` and `./assemblies` directories (including subdirectories) for AsciiDoc (`.adoc`) files that are *not* referenced (included) in any other AsciiDoc file within the project.

## What It Does

- **Identifies unused AsciiDoc files**
  - Finds `.adoc` files in the specified directories that are not included by any other `.adoc` file (via `include::` statements).
- **Generates a manifest**
  - Prints the list of unused files to the console and writes their paths to a manifest file named `to-archive-<YYYY-MM-DD_HHMMSS>.txt` in the `./archive` directory.
- **Optionally archives and deletes**
  - With `--archive`, creates a zip archive in `./archive` containing all unused files and the manifest, then deletes the originals.

## Use Case

Ideal for **documentation maintainers** who want to clean up orphaned modules and assemblies in large AsciiDoc projects.

## Usage

To identify unused files:
```sh
python3 ~/doc-utils/archive_unused_files.py
```

To identify and archive unused files:
```sh
python3 ~/doc-utils/archive_unused_files.py --archive
```

> **Note:** Run this script from the root of your project repository. The archive zip and manifest will be placed in the `./archive` directory.

## Options

| Option        | Description                                                        |
| -------------|--------------------------------------------------------------------|
| `--archive`  | Move unused files to a dated zip in the archive directory and delete originals |
| `-h`, `--help` | Show usage and exit                                              |

## Examples

Identify unused files only:
```sh
python3 ~/doc-utils/archive_unused_files.py
```

Identify and archive unused files:
```sh
python3 ~/doc-utils/archive_unused_files.py --archive
```

## Notes

- You can configure which directories are scanned and where the archive is created by editing the `scan_dirs` and `archive_dir` variables at the bottom of this script.
- The script skips symlinked directories and files.
- The manifest file is always created in the archive directory, even if no files are archived.
- The script is safe to run multiple times; it will not archive or delete files that are already gone.
