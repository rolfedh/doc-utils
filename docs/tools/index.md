---
layout: default
title: Tools Reference
nav_order: 3
has_children: true
---

# Tools Reference

doc-utils provides six specialized CLI tools for maintaining AsciiDoc documentation repositories. Each tool is designed to handle a specific aspect of documentation maintenance.

## Available Tools

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
- Preview mode by default (requires --archive flag to delete)
- Creates timestamped archive with manifest

**Quick Usage:**
```bash
# Preview unused files
archive-unused-files

# Archive and remove unused files
archive-unused-files --archive
```

---

### 🖼️ [archive-unused-images](archive-unused-images)
Identifies and archives image files that are no longer referenced in your documentation.

**Key Features:**
- Supports multiple image formats (PNG, JPG, GIF, SVG)
- Scans all AsciiDoc files for image references
- Preview mode by default
- Creates organized archive structure

**Quick Usage:**
```bash
# Preview unused images
archive-unused-images

# Archive and remove unused images
archive-unused-images --archive
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
replace-link-attributes --help
format-asciidoc-spacing --help
check-scannability --help
archive-unused-files --help
archive-unused-images --help
find-unused-attributes --help
```