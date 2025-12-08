---
layout: default
title: convert-tables-to-deflists
nav_order: 14
---

# Convert Tables to Definition Lists

Converts AsciiDoc 2-column tables to definition list format. For tables with more than 2 columns, use `--columns` to specify which columns to use as term and definition.

{: .note }
> **Related Tools**
>
> This tool converts **general tables** to definition lists. If your tables contain **callout explanations** (where the first column is `<1>`, `<2>`, etc.), use [convert-callouts-to-deflist](convert-callouts-to-deflist) instead—it automatically handles callout tables and provides additional features like "where:" prefix and multiple output formats.

## Overview

AsciiDoc tables are useful for structured data, but definition lists often provide cleaner formatting for term-definition pairs. This tool automates the conversion of 2-column tables to definition lists.

**Conversion:**
- First column → Term (the definition list item)
- Second column → Definition (the explanation)

For tables with more than 2 columns, use the `--columns` option to specify which columns to use.

## Installation

Install with the doc-utils package:

```bash
pipx install rolfedh-doc-utils
```

Then run directly as a command:

```bash
convert-tables-to-deflists [options] [path]
```

## Features

### Automatic Table Detection

- Finds all tables in AsciiDoc files
- Automatically skips callout tables (use `convert-callouts-to-deflist` for those)
- Detects and skips header rows

### Multi-Column Support

By default, only 2-column tables are converted. For tables with more columns:

```bash
# Use columns 1 and 3 from a 3-column table
convert-tables-to-deflists --columns 1,3 .
```

### Safety Features

- **Dry-run mode by default** - Preview changes without modifying files
- **Exclusion support** - Skip directories and files
- **Callout protection** - Callout tables are automatically skipped

### Conditional Directive Handling

Preserves `ifdef::`/`ifndef::`/`endif::` directives when converting tables.

## Usage

### Process All Files (Dry Run)

```bash
convert-tables-to-deflists .
```

Preview what would be changed without modifying files.

### Apply Changes

```bash
convert-tables-to-deflists --apply .
```

### Process Single File

```bash
convert-tables-to-deflists --apply path/to/file.adoc
```

### Process Specific Directory

```bash
convert-tables-to-deflists --apply modules/
```

### Convert 3-Column Tables

```bash
# Use column 1 as term, column 3 as definition
convert-tables-to-deflists --columns 1,3 --apply .
```

### Skip Tables with Headers

```bash
convert-tables-to-deflists --skip-header-tables --apply .
```

### Include Callout Tables

By default, callout tables are skipped. To include them:

```bash
convert-tables-to-deflists --include-callout-tables --apply .
```

### Exclude Directories

```bash
convert-tables-to-deflists --exclude-dir archive --exclude-dir temp --apply .
```

### Use Exclusion List File

```bash
convert-tables-to-deflists --exclude-list .docutils-ignore --apply .
```

## Options

| Option | Description |
|--------|-------------|
| `path` | File or directory to process (default: current directory) |
| `--apply` | Apply changes (default is dry-run mode) |
| `-v, --verbose` | Show detailed output |
| `--columns TERM,DEF` | Column numbers to use (1-indexed, e.g., "1,3") |
| `--skip-header-tables` | Skip tables that have header rows |
| `--include-callout-tables` | Include callout tables (normally skipped) |
| `--exclude-dir DIR` | Exclude directory (can be used multiple times) |
| `--exclude-file FILE` | Exclude file (can be used multiple times) |
| `--exclude-list FILE` | Load exclusion list from file |
| `--version` | Show version number |
| `-h, --help` | Show help message |

## Transformation Examples

### Example 1: Basic 2-Column Table

**Before:**
```asciidoc
[cols="1,3"]
|===
|database.hostname
|The IP address or hostname of the database server.

|database.port
|The port number of the database server (default: 5432).

|database.user
|The username to connect to the database.
|===
```

**After:**
```asciidoc
database.hostname::
The IP address or hostname of the database server.

database.port::
The port number of the database server (default: 5432).

database.user::
The username to connect to the database.
```

### Example 2: 3-Column Table with --columns

**Before:**
```asciidoc
[cols="1,2,3"]
|===
|Property |Default |Description

|database.hostname |localhost |The IP address of the database server.

|database.port |5432 |The port number.

|database.user |admin |The username.
|===
```

**Command:**
```bash
convert-tables-to-deflists --columns 1,3 --apply file.adoc
```

**After:**
```asciidoc
database.hostname::
The IP address of the database server.

database.port::
The port number.

database.user::
The username.
```

### Example 3: Inline Cell Format

Tables with cells on a single line are also supported:

**Before:**
```asciidoc
[cols="1,2"]
|===
|Term1 |Definition1
|Term2 |Definition2
|===
```

**After:**
```asciidoc
Term1::
Definition1

Term2::
Definition2
```

### Example 4: Table with Conditional Directives

Conditional directives are preserved during conversion:

**Before:**
```asciidoc
[cols="1,2"]
|===
ifdef::product[]
|product.name
|The product name for enterprise deployments.
endif::[]

|common.setting
|A setting that applies to all versions.
|===
```

**After:**
```asciidoc
ifdef::product[]
product.name::
The product name for enterprise deployments.
endif::[]

common.setting::
A setting that applies to all versions.
```

## Tables That Are Skipped

The tool automatically skips certain tables:

### Callout Tables

Tables where the first column contains callout numbers (`<1>`, `<2>`, etc.) are skipped by default because they should be processed with `convert-callouts-to-deflist`:

```asciidoc
[cols="1,3"]
|===
|<1>
|First explanation

|<2>
|Second explanation
|===
```

Use `--include-callout-tables` to include these tables.

### Tables with More Than 2 Columns

Tables with 3+ columns are skipped unless you specify `--columns`:

```asciidoc
[cols="1,2,3"]
|===
|Col1 |Col2 |Col3
|A |B |C
|===
```

Use `--columns 1,3` (or any valid column pair) to process these tables.

### Tables with Header Rows (Optional)

Tables with detected header rows are converted by default (header row is excluded from output). Use `--skip-header-tables` to skip them entirely.

## Best Practices

1. **Always work in a git branch** before converting files
2. **Use dry-run first** (default) to preview what will be changed
3. **Review changes with `git diff`** before committing
4. **Test documentation builds** after converting
5. **For callout tables**, use `convert-callouts-to-deflist` instead

## Example Workflow

```bash
# Create a feature branch
git checkout -b convert-tables

# Preview changes
convert-tables-to-deflists .

# Example output:
# DRY RUN MODE - No files will be modified
#   Skipping table at line 45: callout table (use convert-callouts-to-deflist)
# Would modify: modules/config.adoc (2 table(s))
# Would modify: modules/setup.adoc (1 table(s))
#
# Processed 50 file(s)
# Tables converted: 3
# Files would be modified: 2

# Apply changes
convert-tables-to-deflists --apply .

# Review changes
git diff

# Test build
./scripts/build-docs.sh

# Commit changes
git add .
git commit -m "Convert configuration tables to definition lists"
```

## Technical Details

This tool uses the `TableParser` class from the [`callout_lib`](https://github.com/rolfedh/doc-utils/tree/main/callout_lib) library for table detection and parsing.

**Key Processing Steps:**
1. Scan for AsciiDoc tables (`|===` delimiters)
2. Parse table attributes (`[cols="..."]`) to determine column count
3. Detect header rows by checking for common header keywords
4. Skip callout tables (first column is `<1>`, `<2>`, etc.)
5. Convert eligible tables to definition list format
6. Preserve conditional directives

---

See the main [Tools Reference](index) for more documentation utilities.
