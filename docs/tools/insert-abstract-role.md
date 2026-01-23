---
layout: default
title: insert-abstract-role
parent: Tools Reference
nav_order: 16
---

# Insert Abstract Role

This tool ensures AsciiDoc files have the `[role="_abstract"]` attribute above the first paragraph after the document title. This attribute is required for DITA short description conversion, as enforced by the `AsciiDocDITA.ShortDescription` Vale rule.

## What This Tool Does

The tool scans AsciiDoc files and:

1. Finds the document title (level 1 heading: `= Title`)
2. Locates the first paragraph after the title
3. Checks if `[role="_abstract"]` already exists
4. Inserts the attribute if missing

### Before

```asciidoc
:_mod-docs-content-type: REFERENCE
[id="my-doc"]
= My Document Title

This is the first paragraph that describes the topic.

== First Section
```

### After

```asciidoc
:_mod-docs-content-type: REFERENCE
[id="my-doc"]
= My Document Title

[role="_abstract"]
This is the first paragraph that describes the topic.

== First Section
```

## Installation

Install with pipx (recommended):

```sh
pipx install rolfedh-doc-utils
```

Or with pip:

```sh
pip install rolfedh-doc-utils
```

## Usage

```sh
insert-abstract-role [path] [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `path` | File or directory to process (default: current directory) |

### Options

| Option | Description |
|--------|-------------|
| `-n, --dry-run` | Show what would be changed without modifying files |
| `-v, --verbose` | Show detailed output |
| `--exclude-dir DIR` | Directory to exclude (can be specified multiple times) |
| `--exclude-file FILE` | File to exclude (can be specified multiple times) |
| `--exclude-list FILE` | Path to file containing list of files/directories to exclude |
| `--version` | Show program version |

## Examples

### Preview Changes (Dry Run)

```sh
# Preview what would be changed in current directory
insert-abstract-role --dry-run

# Preview with verbose output
insert-abstract-role --dry-run -v modules/
```

### Process Files

```sh
# Process all .adoc files in current directory
insert-abstract-role

# Process specific directory
insert-abstract-role modules/rn/

# Process single file
insert-abstract-role modules/rn/ref_my-release-note.adoc
```

### With Exclusions

```sh
# Exclude archive directories
insert-abstract-role --exclude-dir .archive --exclude-dir old modules/

# Use exclusion list file
insert-abstract-role --exclude-list .docutils-ignore modules/
```

## Output

The tool displays progress and results:

```
DRY RUN MODE - No files will be modified
Modified: modules/rn/ref_rn-feature-one.adoc
Modified: modules/rn/ref_rn-feature-two.adoc
Processed 66 AsciiDoc file(s)
Would modify 2 file(s)
Insert abstract role complete!
```

With `--verbose`:

```
Processing: modules/rn/ref_rn-feature-one.adoc
  Adding [role="_abstract"] before line 5: In the current release...
Processing: modules/rn/ref_rn-feature-two.adoc
  [role="_abstract"] already present
  No changes needed for: modules/rn/ref_rn-feature-two.adoc
```

## Use Cases

### Fix Vale AsciiDocDITA.ShortDescription Warnings

When Vale reports `ShortDescription` warnings like:

```
modules/rn/ref_rn-my-topic.adoc:5:1: warning: Missing role="_abstract"
```

Run the tool to fix all files at once:

```sh
insert-abstract-role modules/rn/
```

### Pre-Migration DITA Preparation

Before migrating AsciiDoc content to DITA, ensure all files have the abstract role for proper short description extraction:

```sh
# Preview changes first
insert-abstract-role --dry-run

# Apply changes
insert-abstract-role
```

### Batch Processing New Content

When adding multiple new files that need the abstract role:

```sh
# Process only new files in a specific directory
insert-abstract-role modules/new-features/
```

## How It Works

The tool identifies the first paragraph by skipping:

- Empty lines
- Attribute definitions (lines starting with `:`)
- Comments (lines starting with `//`)
- Block attributes (lines starting with `[`)
- Include directives (`include::`)
- Other headings (`==`, `===`, etc.)

The first non-empty line that doesn't match these patterns is considered the first paragraph.

## Notes

- **Idempotent**: Running the tool multiple times won't add duplicate attributes
- **Safe**: Use `--dry-run` to preview changes before applying
- **Read-only by default**: Files are only modified when not using `--dry-run`
- Only processes `.adoc` files
- Skips symlinks during directory scanning

## Related Tools

- **[convert-callouts-to-deflist](convert-callouts-to-deflist)** - Convert callouts to definition lists for DITA compatibility
- **[replace-link-attributes](replace-link-attributes)** - Fix Vale LinkAttribute warnings for DITA

---

See the main [README.md](../../README.md) for more details on installation and usage as a package.
