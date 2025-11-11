---
layout: default
title: archive-unused-files
nav_order: 7
---

# Archive Unused AsciiDoc Files

> ⚠️ **WARNING: This Tool Can Delete Files**
> 
> **ALWAYS:**
> 1. **Create a git branch first**: `git checkout -b cleanup-unused-files`
> 2. **Run without `--archive` first** to preview what will be affected
> 3. **Review the list carefully** - ensure no files are incorrectly marked as unused
> 4. **Check your documentation build** after archiving to ensure nothing broke
> 5. **Keep the archive files** until you're certain the removal was correct

This tool automatically discovers and scans all `modules` and `assemblies` directories in your repository for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them.

**Auto-Discovery**: The tool recursively searches for all directories named `modules` or `assemblies` that contain `.adoc` files, regardless of their location in your repository structure. This works with:
- Standard structures (`./modules`, `./assemblies`)
- Nested structures (`./downstream/modules`, `./content/assemblies`)
- Multiple module directories in different locations

The tool automatically detects your repository type:
- **OpenShift-docs style**: Uses `_topic_maps/*.yml` files to determine file references
- **Traditional AsciiDoc**: Looks for `master.adoc` files and `include::` directives
- **Both**: The tool always scans for `include::` directives in addition to topic maps

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
- `--commented` — Include files that are referenced only in commented lines in the archive operation.
- `--scan-dir` — Specify a specific directory to scan (can be used multiple times). If not specified, auto-discovers all modules and assemblies directories.
- `--exclude-dir` — Directory to exclude (can be used multiple times).
- `--exclude-file` — File to exclude (can be used multiple times).
- `--exclude-list` — Path to a file containing directories or files to exclude, one per line.

## Commented References Behavior

**Default behavior (no flag):**
- Always scans for both uncommented and commented includes when scanning for references
- Files referenced only in commented lines are considered "used" and will NOT be archived
- Generates a detailed report of files referenced only in commented lines
- Report location: `./archive/commented-references-report.txt`

**With --commented flag:**
- Include files that are referenced only in commented lines in the archive operation
- These files will be treated as unused and archived along with other unused files

## Examples

### Basic Usage (Auto-Discovery)

Preview what would be archived (dry run):
```sh
archive-unused-files
# Automatically discovers all modules and assemblies directories
# Shows: Auto-discovered directories to scan:
#        - ./downstream/modules
#        - ./downstream/assemblies
```

Archive unused files:
```sh
archive-unused-files --archive
```

### Specifying Directories

Scan specific directories only:
```sh
archive-unused-files --scan-dir ./content/modules --scan-dir ./content/assemblies
```

### Exclusions

Exclude specific directories:
```sh
archive-unused-files --archive --exclude-dir ./modules/legacy --exclude-dir ./modules/wip
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

### Working with Commented References

Preview and generate report on commented-only references:
```sh
archive-unused-files
# This will:
# 1. Find unused files (not counting commented includes as "used")
# 2. Generate a report of files referenced only in commented lines
# 3. Save report to ./archive/commented-references-report.txt
```

Archive files including those with commented-only references:
```sh
archive-unused-files --archive --commented
# This will archive both:
# 1. Files with no references at all
# 2. Files referenced only in commented lines
```

## Output

- Prints unused files to the terminal.
- Creates a manifest file in the `archive/` directory.
- Optionally creates a zip archive of unused files.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
