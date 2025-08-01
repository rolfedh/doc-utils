# Archive Unused AsciiDoc Files

> ⚠️ **WARNING: This Tool Can Delete Files**
> 
> **ALWAYS:**
> 1. **Create a git branch first**: `git checkout -b cleanup-unused-files`
> 2. **Run without `--archive` first** to preview what will be affected
> 3. **Review the list carefully** - ensure no files are incorrectly marked as unused
> 4. **Check your documentation build** after archiving to ensure nothing broke
> 5. **Keep the archive files** until you're certain the removal was correct

This tool scans `./modules`, `./modules/rn`, and `./assemblies` directories for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them.

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

## Examples

Archive unused files while excluding a directory:
```sh
archive-unused-files --archive --exclude-dir ./modules/legacy
```

Dry run (see what would be archived without actually archiving):
```sh
archive-unused-files
```

Use an exclusion list file:
```sh
archive-unused-files --archive --exclude-list .docutils-ignore
```

Example exclusion list file (`.docutils-ignore`):
```
# Directories to exclude
./modules/archived/
./modules/wip/

# Specific files to exclude
./assemblies/draft.adoc
```

## Output

- Prints unused files to the terminal.
- Creates a manifest file in the `archive/` directory.
- Optionally creates a zip archive of unused files.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
