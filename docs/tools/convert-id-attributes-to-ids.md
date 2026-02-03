---
layout: default
title: convert-id-attributes-to-ids
parent: Tools Reference
nav_order: 19
---

# convert-id-attributes-to-ids

Convert `:id:` attribute definitions to standard AsciiDoc `[id="..._{context}"]` anchors.

## Purpose

This tool helps migrate AsciiDoc files that use a custom ID attribute pattern to standard AsciiDoc anchor syntax with context suffixes. It is particularly useful when transitioning from documentation systems that use conditional ID assignment via include files to direct ID anchors.

The tool converts:
```asciidoc
:id: my-section-id
```

To:
```asciidoc
[id="my-section-id_{context}"]
```

## What it does

- Recursively scans directories for `.adoc` files
- Converts `:id: <value>` attribute definitions to `[id="<value>_{context}"]` anchors
- Optionally removes related boilerplate comments and include directives with `--clean-up`

### Clean-up mode

With `--clean-up`, the tool also removes these common boilerplate lines:

- `// define ID as an attribute` (and variations)
- `// assign ID conditionally` or `// assign the ID conditionally` (and variations)
- `include::{modules}/common/id.adoc[]`

## Installation

```bash
pipx install rolfedh-doc-utils
```

## Usage

### Preview changes (recommended first step)

```bash
convert-id-attributes-to-ids --dry-run /path/to/docs
```

### Basic conversion

```bash
convert-id-attributes-to-ids /path/to/docs
```

### Conversion with boilerplate cleanup

```bash
convert-id-attributes-to-ids --clean-up /path/to/docs
```

### Verbose output

```bash
convert-id-attributes-to-ids --clean-up --verbose /path/to/docs
```

## Examples

### Before and after

**Before:**
```asciidoc
:_mod-docs-content-type: PROCEDURE
// include attributes via conditional logic
include::common.adoc[]
// define ID as an attribute - make it succinct for URL brevity
:id: proc-viewing-remediation-plans
// assign the ID conditionally - the logic decides whether a context is needed
include::{modules}/common/id.adoc[]
= Viewing remediation plans

The **Remediation Plan** view provides an overview...
```

**After (with --clean-up):**
```asciidoc
:_mod-docs-content-type: PROCEDURE
// include attributes via conditional logic
include::common.adoc[]
[id="proc-viewing-remediation-plans_{context}"]
= Viewing remediation plans

The **Remediation Plan** view provides an overview...
```

### Processing a single directory

```bash
# Preview what would change
convert-id-attributes-to-ids --dry-run modules/

# Apply changes
convert-id-attributes-to-ids modules/
```

### Full cleanup with detailed output

```bash
convert-id-attributes-to-ids --clean-up --verbose ~/docs/modules
```

Output:
```
Scanning directory: /home/user/docs/modules
Clean-up mode enabled: will remove ID-related boilerplate lines
✓ Found 42 .adoc files
  proc_viewing_plans.adoc: 1 ID conversion(s), 3 line(s) removed
  proc_creating_plans.adoc: 1 ID conversion(s), 3 line(s) removed
  ref_plan_fields.adoc: 1 ID conversion(s), 3 line(s) removed
✓ Processed 42 files

Summary:
  Files modified: 3
  :id: attributes converted: 3
  Boilerplate lines removed: 9

Conversion complete!
```

## Command-line options

| Option | Description |
|--------|-------------|
| `directory` | Directory to scan for .adoc files (default: current directory) |
| `--dry-run`, `-n` | Preview changes without modifying files |
| `--clean-up` | Remove ID-related boilerplate lines (comments and include directives) |
| `--verbose`, `-v` | Show detailed output for each file processed |
| `--version` | Show version number |
| `--help`, `-h` | Show help message |

## Features

- **Recursive scanning**: Processes all `.adoc` files in subdirectories
- **Safe operation**: Dry-run mode to preview changes before applying
- **Flexible pattern matching**: Handles variations in boilerplate comments
- **Detailed reporting**: Shows exactly what changes were made to each file
- **Skips hidden directories**: Ignores `.git`, `.vale`, and similar directories

## Boilerplate patterns removed (with --clean-up)

The `--clean-up` option removes lines matching these patterns:

1. **ID attribute definition comments:**
   - `// define ID as an attribute`
   - `// define ID as an attribute - make it succinct...` (with additional text)

2. **Conditional assignment comments:**
   - `// assign ID conditionally`
   - `// assign the ID conditionally`
   - `// assign ID conditionally - the logic decides...` (with additional text)

3. **ID include directives:**
   - `include::{modules}/common/id.adoc[]`

Pattern matching is case-insensitive for comment text.

## Exit codes

- 0: Success (changes made or no changes needed)
- 1: Error (directory not found, not a directory, etc.)

## Best practices

1. **Always use `--dry-run` first** to preview what will change
2. **Work in a git branch** so you can easily review and revert changes
3. **Use `--verbose`** to see exactly which files are modified
4. **Review changes with `git diff`** before committing
5. **Test your documentation build** after making changes
