# Archive Unused AsciiDoc Files

This tool scans `./modules` and `./assemblies` for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them.

## Installation

After installing the package from PyPI:

```sh
pip install rolfedh-doc-utils
```

You can run the tool from anywhere using:

```sh
archive-unused-files [options]
```

Or, if running from source:

```sh
python3 archive_unused_files.py [options]
```

## Usage

See the script's `--help` output or the docstring for all options. Common options include:

- `--archive` — Move the files to a dated zip in the archive directory.
- `--exclude-dir` — Directory to exclude (can be used multiple times).
- `--exclude-file` — File to exclude (can be used multiple times).
- `--exclude-list` — Path to a file containing directories or files to exclude, one per line.

## Example

```sh
archive-unused-files --archive --exclude-dir ./modules/legacy
```

This will archive all unused AsciiDoc files, excluding those in `./modules/legacy`.

## Output

- Prints unused files to the terminal.
- Creates a manifest file in the `archive/` directory.
- Optionally creates a zip archive of unused files.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
