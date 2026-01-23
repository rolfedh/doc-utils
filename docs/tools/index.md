---
layout: default
title: Tools Reference
nav_order: 3
---

# Tools Reference

doc-utils provides specialized CLI tools for maintaining AsciiDoc documentation repositories. Each tool is designed to handle a specific aspect of documentation maintenance.

## Available Tools

### 🔍 [validate-links](validate-links)
Validates all links in AsciiDoc documentation, checking for broken URLs and missing references.

**Key Features:**
- URL transposition for preview/staging validation
- Concurrent link checking with caching
- Resolves AsciiDoc attributes before validation
- Supports external URLs, internal refs, and images
- Multiple output formats (text, JSON, JUnit)

**Quick Usage:**
```bash
validate-links --transpose "https://docs.example.com--https://preview.docs.example.com"
```

---

### 🌐 [check-published-links](check-published-links)
Validates links on published HTML documentation pages using linkchecker.

**Key Features:**
- Checks actual rendered HTML output, not source files
- URL rewriting for platforms with path resolution issues
- Single URL and bulk validation modes
- Automatic handling of known false positives
- Detailed reports with error categorization

**Quick Usage:**
```bash
check-published-links https://docs.example.com/guide/
check-published-links --file urls-to-check.txt
```

---

### 🔗 [extract-link-attributes](extract-link-attributes)
Extracts link and xref macros containing attributes into reusable attribute definitions.

**Key Features:**
- Creates centralized link management in attributes files
- Handles link text variations intelligently
- Reuses existing attributes on subsequent runs
- Interactive and non-interactive modes
- Preserves macro type (link vs xref)
- **NEW**: Validates link attributes for broken URLs

**Quick Usage:**
```bash
extract-link-attributes --dry-run

# With link validation
extract-link-attributes --validate-links --fail-on-broken
```

---

### 🔗 [replace-link-attributes](replace-link-attributes)
Resolves Vale AsciiDocDITA LinkAttribute issues by replacing attribute references in link URLs with their actual values.

**Key Features:**
- Fixes Vale LinkAttribute rule: "DITA 1.3 does not allow references to reusable content in link URLs"
- Replaces attributes in link: and xref: macros
- Preserves link text unchanged
- Interactive attribute file selection
- Dry-run mode for previewing changes

**Quick Usage:**
```bash
replace-link-attributes --dry-run
```

---

### 📝 [format-asciidoc-spacing](format-asciidoc-spacing)
Standardizes AsciiDoc formatting by ensuring proper spacing after headings and around include directives.

**Key Features:**
- Adds blank lines after headings (=, ==, ===, etc.)
- Adds blank lines around include:: directives
- Dry-run mode for previewing changes
- Verbose mode for detailed output

**Quick Usage:**
```bash
format-asciidoc-spacing --dry-run modules/
```

---

### 🔍 [check-scannability](check-scannability)
Analyzes document readability by checking sentence and paragraph length against best practices.

**Key Features:**
- Configurable sentence length limits (default: 22 words)
- Configurable paragraph length limits (default: 3 sentences)
- Detailed reports showing specific issues
- Support for exclusion lists

**Quick Usage:**
```bash
check-scannability --max-words 25 --max-sentences 4
```

---

### 🗄️ [archive-unused-files](archive-unused-files)
Finds and optionally archives unreferenced AsciiDoc files in your documentation repository.

**Key Features:**
- Automatic detection of repository type (OpenShift-docs or traditional)
- Smart directory discovery
- **NEW**: Detects files referenced only in commented lines
- **NEW**: Generates detailed reports of commented-only references
- Preview mode by default (requires --archive flag to delete)
- Creates timestamped archive with manifest

**Quick Usage:**
```bash
# Preview unused files (generates report of commented-only references)
archive-unused-files

# Archive including files with commented-only references
archive-unused-files --archive --commented
```

---

### 🖼️ [archive-unused-images](archive-unused-images)
Identifies and archives image files that are no longer referenced in your documentation.

**Key Features:**
- Supports multiple image formats (PNG, JPG, GIF, SVG)
- Scans all AsciiDoc files for image references
- **NEW**: Detects images referenced only in commented lines
- **NEW**: Generates detailed reports of commented-only references
- Preview mode by default
- Creates organized archive structure

**Quick Usage:**
```bash
# Preview unused images (generates report of commented-only references)
archive-unused-images

# Archive including images with commented-only references
archive-unused-images --archive --commented
```

---

### 🏷️ [find-unused-attributes](find-unused-attributes)
Scans for AsciiDoc attribute definitions that are declared but never used in your documentation.

**Key Features:**
- Analyzes attribute definition files
- Searches entire repository for attribute usage
- Detailed output showing unused attributes
- Option to save results to file

**Quick Usage:**
```bash
find-unused-attributes attributes.adoc
find-unused-attributes attributes.adoc --output unused.txt
```

---

### 📋 [inventory-conditionals](inventory-conditionals)
Creates a timestamped inventory of all AsciiDoc conditional directives (`ifdef`, `ifndef`, `endif`, `ifeval`) in your documentation.

**Key Features:**
- Scans all `.adoc` files recursively
- Reports line numbers for each conditional
- Summarizes directive counts and unique conditions
- Helps audit conditional usage before refactoring

**Quick Usage:**
```bash
# Scan current directory
inventory-conditionals

# Scan specific directory with custom output location
inventory-conditionals ~/gitlab/quarkus -o ~/reports/
```

---

### 🔄 [convert-callouts-to-deflist](convert-callouts-to-deflist)
Converts AsciiDoc code blocks with callout-style annotations to cleaner definition list format.

**Key Features:**
- Converts callouts (`<1>`, `<2>`) to definition lists with "where:" prefix
- Automatically scans all `.adoc` files recursively
- Intelligent value extraction from code and explanations
- Preserves optional markers and non-sequential callouts
- Validation ensures callout numbers match
- Exclusion list support for directories and files
- Heredoc-aware pattern matching

**Quick Usage:**
```bash
# Process current directory (.vale excluded by default)
convert-callouts-to-deflist --dry-run

# Process specific directory with additional exclusions
convert-callouts-to-deflist --dry-run --exclude-dir archive modules/
```

---

### 📊 [convert-tables-to-deflists](convert-tables-to-deflists)
Converts AsciiDoc 2-column tables to definition list format.

**Key Features:**
- Converts 2-column tables by default (column 1 → term, column 2 → definition)
- Multi-column support with `--columns` option (e.g., `--columns 1,3`)
- Automatically skips callout tables (use convert-callouts-to-deflist for those)
- Detects and handles header rows
- Preserves conditional directives (`ifdef::`/`endif::`)
- Dry-run mode by default for safe preview

**Quick Usage:**
```bash
# Preview changes (dry-run mode)
convert-tables-to-deflists .

# Apply changes to 2-column tables
convert-tables-to-deflists --apply .

# Convert 3-column tables using columns 1 and 3
convert-tables-to-deflists --columns 1,3 --apply modules/
```

---

### 📝 [insert-abstract-role](insert-abstract-role)
Inserts `[role="_abstract"]` above the first paragraph after the document title for DITA short description support.

**Key Features:**
- Fixes Vale `AsciiDocDITA.ShortDescription` warnings
- Idempotent - safe to run multiple times
- Dry-run mode for previewing changes
- Processes single files or entire directories

**Quick Usage:**
```bash
# Preview changes
insert-abstract-role --dry-run modules/

# Apply changes
insert-abstract-role modules/
```

## Common Options

All tools support these common options for excluding files and directories:

### Exclusion Options

```bash
# Exclude specific directories
--exclude-dir ./modules/temp --exclude-dir ./modules/old

# Exclude specific files
--exclude-file ./README.adoc --exclude-file ./test.adoc

# Use an exclusion list file
--exclude-list .docutils-ignore
```

### Exclusion List File Format

Create a `.docutils-ignore` file:

```
# Comments are supported
./modules/deprecated/
./assemblies/archive/
./images/temp/
specific-file.adoc
```

## Repository Type Detection

doc-utils automatically detects your repository structure:

### OpenShift-docs Style
- Looks for `_topic_maps/*.yml` files
- Parses YAML topic maps for file references
- Supports nested topic structures

### Traditional AsciiDoc
- Looks for `master.adoc` files
- Follows include:: directives
- Supports standard AsciiDoc structure

## Safety Features

All archive tools include built-in safety features:

1. **Preview by Default** - Tools show what would be affected without making changes
2. **Explicit Archive Flag** - Deletion requires `--archive` flag
3. **Timestamped Backups** - Archives include timestamp and manifest
4. **Clear Warnings** - Tools display safety warnings when running

## Best Practices

1. **Always work in a git branch** before running any tools
2. **Use preview/dry-run modes first** to understand what will change
3. **Review changes with `git diff`** before committing
4. **Test your documentation builds** after making changes
5. **Keep exclusion lists updated** for files that should never be processed

## Getting Help

Each tool has a built-in help command:

```bash
validate-links --help
check-published-links --help
extract-link-attributes --help
replace-link-attributes --help
format-asciidoc-spacing --help
check-scannability --help
archive-unused-files --help
archive-unused-images --help
find-unused-attributes --help
inventory-conditionals --help
convert-callouts-to-deflist --help
convert-tables-to-deflists --help
insert-abstract-role --help
```