---
layout: default
title: find-duplicate-includes
nav_order: 11
---

# Find Duplicate Includes

Scans AsciiDoc files for `include::` macros and identifies files that are included from multiple locations. This helps you find opportunities for content reuse or identify potential maintenance issues where the same content is being pulled into multiple places.

## What This Tool Detects

The tool finds files that are referenced by `include::` macros in more than one location:

```asciidoc
// In getting-started.adoc
include::modules/common-prereqs.adoc[]

// In troubleshooting.adoc (same file included again)
include::modules/common-prereqs.adoc[]
```

## Common Files

By default, the tool excludes "common" files that are expected to be included multiple times:

- `attributes.adoc`
- `_attributes.adoc`
- `common/attributes.adoc`
- `common/revision-info.adoc`

Use `--include-common` to include these files in the results.

## Installation

After [installing the package](../getting-started.md), run the tool from anywhere:

```sh
find-duplicate-includes [directory] [options]
```

Or run from source:

```sh
python3 find_duplicate_includes.py [directory] [options]
```

## Options

| Option | Description |
|--------|-------------|
| `directory` | Directory to scan (default: current directory) |
| `--include-common` | Include common files (attributes.adoc, etc.) in results |
| `-e, --exclude-dir DIR` | Directory to exclude (can be repeated) |
| `--exclude-file FILE` | File to exclude (can be repeated) |
| `--no-output` | Do not write report file (stdout only) |
| `--format FORMAT` | Output format: `txt` (default), `csv`, `json`, `md` |

## Examples

```sh
# Scan current directory
find-duplicate-includes

# Scan a specific directory
find-duplicate-includes ./docs

# Include common files in results
find-duplicate-includes --include-common

# Exclude specific directories
find-duplicate-includes -e archive -e drafts

# Generate CSV report for spreadsheet analysis
find-duplicate-includes --format csv

# Display only, no report file
find-duplicate-includes --no-output
```

## Output

By default, the tool writes a report to `./reports/duplicate-includes_YYYY-MM-DD_HH-MM-SS.txt`. Use `--format` to change the output format or `--no-output` to skip file generation.

### Sample Text Report

```
Command: find-duplicate-includes
Directory: /home/user/my-docs
Files scanned: 142

Found 3 files included more than once:
  (2 common files excluded; use --include-common to see all)

======================================================================

[1] modules/common-prereqs.adoc
    Included 4 times:
--------------------------------------------------
    - assemblies/getting-started.adoc:12
    - assemblies/installation-guide.adoc:8
    - assemblies/troubleshooting.adoc:15
    - assemblies/quickstart.adoc:6

[2] modules/support-statement.adoc
    Included 2 times:
--------------------------------------------------
    - assemblies/overview.adoc:45
    - assemblies/release-notes.adoc:78
```

### CSV Format

```csv
Included File,Inclusion Count,Is Common,Source File,Line Number,Raw Include Path
"modules/common-prereqs.adoc",4,False,"assemblies/getting-started.adoc",12,"../modules/common-prereqs.adoc"
"modules/common-prereqs.adoc",4,False,"assemblies/installation-guide.adoc",8,"../modules/common-prereqs.adoc"
```

## Use Cases

### Identify Refactoring Opportunities

Files included multiple times may be candidates for:

1. **Shared modules**: Move frequently-included content to a dedicated shared location
2. **Conditional includes**: Use `ifdef`/`ifndef` to include content based on context
3. **Attributes**: Extract repeated short content into attributes

### Audit Content Reuse

Track which files are reused across your documentation to:

- Understand documentation architecture
- Identify high-impact files (changes affect multiple outputs)
- Plan content updates that touch shared resources

### Detect Unintentional Duplication

Sometimes the same content gets included multiple times by accident, leading to:

- Duplicated content in output
- Maintenance burden when updates are needed
- Build performance issues

## Differences from find-duplicate-content

| Feature | find-duplicate-includes | find-duplicate-content |
|---------|------------------------|------------------------|
| **What it finds** | Files included via `include::` | Similar text blocks |
| **Matching** | Exact file references | Similarity-based |
| **Scope** | Include macros only | Notes, tables, steps, code |
| **Use case** | Audit file reuse | Find copy-pasted content |

Use both tools together for comprehensive content analysis.

## Limitations

- Only detects `include::` macros at the start of lines
- Does not resolve attribute references in include paths
- Does not detect includes within ifdef/ifndef blocks differently

## Notes

- Only `.adoc` files are scanned
- Symlinks are ignored
- Default excluded directories: `.git`, `.archive`, `target`, `build`, `node_modules`
- The tool does not modify any files

---

See the main [README.md](../README.md) for installation and usage details.
