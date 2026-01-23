---
layout: default
title: Content Reuse Assessment
nav_order: 5
---

# Content Reuse Assessment

Before migrating documentation to a new content management system, you need to assess how content is reused across your documentation set. These tools automate the analysis, generating reports that you can link directly in your Content Reuse Assessment Worksheet.

Use these doc-utils tools to complete the **Pre-Migration Reuse Readiness Tasks**:

| Worksheet Task | Tool |
|----------------|------|
| Remove unused attributes | `find-unused-attributes --remove` |
| Inventory conditionals | `inventory-conditionals` |
| Inventory reused modules | `find-duplicate-includes` |
| Inventory reused content blocks | `find-duplicate-content` |
| Archive unused files | `archive-unused-files` |

## Task 1: Clean Up Attribute Files

```sh
find-unused-attributes --remove
```

> **Warning**: The `--remove` option modifies files in place. Always review the output of `find-unused-attributes` (without `--remove`) first, then test your documentation build after removing attributes.

See [find-unused-attributes](tools/find-unused-attributes.md) for details.

## Task 2: Inventory Conditionals

```sh
inventory-conditionals
```

Creates `./reports/conditionals-inventory_*.txt` listing every `ifdef`, `ifndef`, `ifeval`, and `endif` with locations.

See [inventory-conditionals](tools/inventory-conditionals.md) for details.

## Task 3: Inventory Reused Content

Run both tools to capture different types of reuse:

```sh
# Files included via include:: from multiple locations
find-duplicate-includes

# Similar notes, tables, steps, and code blocks
find-duplicate-content
```

Reports are written to `./reports/`.

See [find-duplicate-includes](tools/find-duplicate-includes.md) and [find-duplicate-content](tools/find-duplicate-content.md) for details.

## Task 4: Archive Unused Files

```sh
# Preview unused files (no changes made)
archive-unused-files

# Archive unused files to ./archive/
archive-unused-files --archive
```

Finds AsciiDoc files in `modules/` and `assemblies/` directories that are not referenced by any `include::` macro. Run without `--archive` first to review the list.

See [archive-unused-files](tools/archive-unused-files.md) for details.

## Quick Reference

```sh
# Review unused attributes first
find-unused-attributes

# Then remove (after verifying build works)
find-unused-attributes --remove

# Generate reuse inventory reports
inventory-conditionals
find-duplicate-includes
find-duplicate-content

# Find and archive unused files
archive-unused-files
archive-unused-files --archive
```

Commit the reports to your repository and link them in your worksheet.
