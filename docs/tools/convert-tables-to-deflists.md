---
layout: default
title: convert-tables-to-deflists
nav_order: 14
---

# Convert Tables to Definition Lists

Converts AsciiDoc tables to definition list format:
- Column 1 becomes the term (with `::` suffix)
- Column 2 becomes the primary definition text
- Columns 3+ are appended as metadata lines with format: `{column_heading}: {value}`

Block titles (e.g., `.Properties that you can change`) are converted to lead-in sentences with colon punctuation. List-continuation markers (`+`) are preserved.

{: .note }
> **Related Tools**
>
> This tool converts **general tables** to definition lists. If your tables contain **callout explanations** (where the first column is `<1>`, `<2>`, etc.), use [convert-callouts-to-deflist](convert-callouts-to-deflist) instead—it automatically handles callout tables and provides additional features like "where:" prefix and multiple output formats.

## Overview

AsciiDoc tables are useful for structured data, but definition lists often provide cleaner formatting for term-definition pairs. This tool automates the conversion of tables to definition lists.

**Conversion:**
- Column 1 → Term (the definition list item with `::` suffix)
- Column 2 → Definition (the explanation text)
- Columns 3+ → Metadata lines (format: `Header: value`)

For tables where you want to use specific columns (ignoring metadata), use the `--columns` option.

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
- Detects and uses header rows for metadata column names

### Multi-Column Support

Tables with 2+ columns are converted by default:
- Columns 1 and 2 become term and definition
- Columns 3+ become metadata lines using the header name as a label

To use only specific columns (ignoring metadata columns):

```bash
# Use only columns 1 and 3 from a table
convert-tables-to-deflists --columns 1,3 .
```

### Block Title Conversion

Block titles are converted to lead-in sentences:

**Before:**
```asciidoc
.Properties that you can change
[cols="1,2"]
|===
...
```

**After:**
```asciidoc
Properties that you can change:

property.name::
...
```

### Bullet List Handling

Bullet lists in definitions are wrapped in open blocks (`--`) to ensure proper alignment of subsequent content:

```asciidoc
`quarkus.package.type` (deprecated)::
Deprecated.
+
--
* Use `quarkus.package.jar.type` to configure the JAR type.
* For native builds, set `quarkus.native.enabled` to `true`.
--
+
Type: string +
Default: `jar`
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

### Use Specific Columns Only

```bash
# Use column 1 as term, column 3 as definition (ignore other columns)
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
| `--columns TERM,DEF` | Column numbers to use (1-indexed, e.g., "1,3"). Ignores metadata columns. |
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

### Example 2: Multi-Column Table with Metadata

Tables with 3+ columns automatically include metadata from extra columns:

**Before:**
```asciidoc
[cols="35%,35%,15%,15%",options="header"]
|===
| Property
| Description
| Type
| Default

| `quarkus.native.enabled`
| Enables native image generation. When set to `true`, the application is compiled into a native executable.
| boolean
| `false`

| `quarkus.package.output-name`
| Specifies the name of the final build artifact.
| string
| _(none)_
|===
```

**After:**
```asciidoc
`quarkus.native.enabled`::
Enables native image generation. When set to `true`, the application is compiled into a native executable. +
Type: boolean +
Default: `false`

`quarkus.package.output-name`::
Specifies the name of the final build artifact. +
Type: string +
Default: _(none)_
```

### Example 3: Table with Bullet Lists

Definitions containing bullet lists are wrapped in open blocks for proper formatting:

**Before:**
```asciidoc
[cols="35%,35%,15%,15%",options="header"]
|===
| Property | Description | Type | Default

| `quarkus.package.type` (deprecated)
a| Deprecated.
* Use `quarkus.package.jar.type` to configure the JAR type.
* For native builds, set `quarkus.native.enabled` to `true`.
| string
| `jar`
|===
```

**After:**
```asciidoc
`quarkus.package.type` (deprecated)::
Deprecated.
+
--
* Use `quarkus.package.jar.type` to configure the JAR type.
* For native builds, set `quarkus.native.enabled` to `true`.
--
+
Type: string +
Default: `jar`
```

### Example 4: Using --columns to Ignore Metadata

Use `--columns` to specify exactly which columns to use (metadata columns are ignored):

**Command:**
```bash
convert-tables-to-deflists --columns 1,2 --apply file.adoc
```

**Before:**
```asciidoc
[cols="1,2,1,1",options="header"]
|===
|Property |Description |Type |Default
|database.hostname |The IP address of the database server. |string |localhost
|===
```

**After:**
```asciidoc
database.hostname::
The IP address of the database server.
```

### Example 5: Table with Block Title

Block titles are converted to lead-in sentences:

**Before:**
```asciidoc
. Add the properties that you want to change and save the file.
+
.Properties that you can change
+
[cols="1,2"]
|===
|property.name |Description of the property.
|===
```

**After:**
```asciidoc
. Add the properties that you want to change and save the file.
+
Properties that you can change:
+
property.name::
Description of the property.
```

### Example 6: Table with Conditional Directives

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

### Single-Column Tables

Tables with only 1 column are skipped (need at least 2 columns for term-definition pairs).

## Best Practices

1. **Always work in a git branch** before converting files
2. **Use dry-run first** (default) to preview what will be changed
3. **Review changes with `git diff`** before committing
4. **Test documentation builds** after converting
5. **For callout tables**, use `convert-callouts-to-deflist` instead
6. **Tables need header rows** for column 3+ metadata to work properly

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
3. Detect header rows and extract column names for metadata
4. Skip callout tables (first column is `<1>`, `<2>`, etc.)
5. Convert eligible tables to definition list format
6. Wrap bullet lists in open blocks (`--`) for proper alignment
7. Append columns 3+ as metadata lines using header names
8. Convert block titles to lead-in sentences
9. Preserve conditional directives and list-continuation markers

---

See the main [Tools Reference](index) for more documentation utilities.
