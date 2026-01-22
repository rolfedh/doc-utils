---
layout: default
title: inventory-conditionals
parent: Tools Reference
nav_order: 15
---

# Inventory AsciiDoc Conditionals

This tool scans AsciiDoc files for conditional directives (`ifdef`, `ifndef`, `endif`, `ifeval`) and creates a timestamped inventory file documenting their usage across your documentation repository.

## What This Tool Detects

The tool searches for these AsciiDoc conditional directives:

| Directive | Purpose |
|-----------|---------|
| `ifdef::attribute[]` | Include content if attribute is defined |
| `ifndef::attribute[]` | Include content if attribute is NOT defined |
| `endif::attribute[]` | End of conditional block |
| `ifeval::[expression]` | Include content if expression evaluates to true |

## Installation

Install with pipx (recommended):

```sh
pipx install rolfedh-doc-utils
```

Or with pip:

```sh
pip install rolfedh-doc-utils
```

Run the tool from anywhere:

```sh
inventory-conditionals [directory] [-o OUTPUT_DIR]
```

Or, if running from source:

```sh
python3 inventory_conditionals.py [directory] [-o OUTPUT_DIR]
```

### Options

| Option | Description |
|--------|-------------|
| `directory` | Directory to scan for `.adoc` files (default: current directory) |
| `-o, --output-dir` | Directory to write the inventory file (default: current directory) |

## Output

The tool creates a timestamped file named `inventory-YYYYMMDD-HHMMSS.txt` containing:

1. **Per-file listings** - Each file with conditionals is listed with line numbers
2. **Summary statistics** - Total counts for each directive type
3. **Unique conditions** - All condition names used with occurrence counts

### Example Output

```
AsciiDoc Conditionals Inventory
Generated: 2026-01-22 15:47:58
Directory: /home/user/docs
================================================================================

File: modules/proc_creating-project.adoc
------------------------------------------------------------
  Line    12: ifdef::rh-only[]
  Line    18: endif::rh-only[]
  Line    25: ifndef::no-feature-x[]
  Line    31: endif::no-feature-x[]

File: assemblies/assembly_getting-started.adoc
------------------------------------------------------------
  Line     3: ifdef::context[:parent-context: {context}]
  Line    96: ifdef::parent-context[:context: {parent-context}]
  Line    97: ifndef::parent-context[:!context:]

================================================================================
SUMMARY
================================================================================

Total .adoc files scanned: 245
Files with conditionals: 131

Directive counts:
  endif: 3562
  ifdef: 2766
  ifeval: 23
  ifndef: 1137
  Total: 7488

================================================================================
UNIQUE CONDITIONS USED
================================================================================

  ibm-only: 331 occurrences
  rh-only: 30 occurrences
  parent-context: 14 occurrences
  context: 7 occurrences
```

## Examples

### Scan Current Directory

```sh
# Create inventory in current directory
inventory-conditionals
```

### Scan Specific Directory

```sh
# Scan a documentation repository
inventory-conditionals ~/gitlab/quarkus
```

### Specify Output Location

```sh
# Scan docs but save inventory elsewhere
inventory-conditionals ~/gitlab/quarkus -o ~/reports/
```

## Use Cases

### Audit Conditional Usage

Before refactoring conditionals or consolidating attributes, generate an inventory to understand:

- Which conditions are used most frequently
- Which files contain conditional logic
- Where specific conditions like `rh-only` or `ibm-only` appear

### Track Build Variations

For documentation with multiple output targets (e.g., upstream/downstream), the inventory shows which files have conditional content and what conditions control their inclusion.

### Clean Up Unused Conditions

Cross-reference the inventory with your attributes file to identify:

- Conditions that are defined but never used
- Conditions that are used but not documented
- Inconsistent naming patterns

### Migration Planning

When migrating between documentation platforms or consolidating repositories, the inventory provides a clear picture of conditional complexity to address.

## Notes

- Only `.adoc` files are scanned
- Scans recursively through all subdirectories
- Symlinks are followed during scanning
- The tool is read-only and does not modify any files
- Output file is UTF-8 encoded

## Related Tools

- **[find-unused-attributes](find-unused-attributes)** - Find attribute definitions that are never used
- **[archive-unused-files](archive-unused-files)** - Find and archive unreferenced AsciiDoc files

---

See the main [README.md](../../README.md) for more details on installation and usage as a package.
