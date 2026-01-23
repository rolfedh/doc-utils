---
layout: default
title: Content Reuse Assessment
nav_order: 5
---

# Content Reuse Assessment

Use these doc-utils tools to complete the **Pre-Migration Reuse Readiness Tasks** in the Content Reuse Assessment Worksheet.

| Worksheet Task | Tool |
|----------------|------|
| Remove unused attributes | `find-unused-attributes --remove` |
| Inventory conditionals | `inventory-conditionals` |
| Inventory reused modules | `find-duplicate-includes` |
| Inventory reused content blocks | `find-duplicate-content` |

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
```

Commit the reports to your repository and link them in your worksheet.
