---
layout: default
title: find-duplicate-content
nav_order: 10
---

# Find Duplicate Content

> **Review Before Refactoring**
>
> This tool identifies duplicate and similar content that may be candidates for refactoring into reusable components. Before making changes:
> 1. Review each duplicate carefully — some repetition is intentional
> 2. Consider context — similar content might need different wording for different audiences
> 3. Plan your refactoring strategy — decide whether to use includes, attributes, or shared modules
> 4. Test your documentation build after consolidating content

## What This Tool Detects

- **Admonition blocks**: `NOTE:`, `TIP:`, `WARNING:`, `IMPORTANT:`, `CAUTION:` (both inline and delimited)
- **Tables**: Content between `|===` delimiters
- **Step sequences**: Ordered lists (numbered procedures)
- **Code blocks**: Content between `----` or `....` delimiters

## Installation

After installing the package:

```sh
pip install rolfedh-doc-utils
```

Run the tool:

```sh
find-duplicate-content [directory] [options]
```

Or run from source:

```sh
python3 find_duplicate_content.py [directory] [options]
```

## Options

| Option | Description |
|--------|-------------|
| `directory` | Directory to scan (default: current directory) |
| `-t, --type TYPE` | Block types to search for (can be repeated). Choices: `note`, `tip`, `warning`, `important`, `caution`, `table`, `steps`, `code` |
| `-s, --similarity THRESHOLD` | Minimum similarity threshold (0.0-1.0). Default: 0.8 |
| `-m, --min-length CHARS` | Minimum content length to consider. Default: 50 |
| `--exact-only` | Only find exact duplicates |
| `-e, --exclude-dir DIR` | Directory to exclude (can be repeated) |
| `--no-content` | Hide content preview in output |
| `--no-output` | Do not write report file |
| `--format FORMAT` | Output format: `txt` (default), `csv`, `json`, `md` |

## Examples

```sh
# Scan current directory for all types of duplicates
find-duplicate-content

# Scan a specific directory
find-duplicate-content ./docs/modules

# Find only notes, tables, and tips
find-duplicate-content -t note -t table -t tip

# Find exact duplicates only
find-duplicate-content --exact-only

# Find content with 70% or greater similarity
find-duplicate-content -s 0.7

# Exclude specific directories
find-duplicate-content -e archive -e drafts

# Write CSV report for spreadsheet analysis
find-duplicate-content --format csv

# Display results only, no report file
find-duplicate-content --no-output
```

## Output

By default, the tool writes a report to `./reports/duplicate-content_YYYY-MM-DD_HH-MM-SS.txt`. Use `--format` to change the output format or `--no-output` to skip file generation.

### Sample Text Report

```
✓ Found 3 groups of duplicate content

Command: find-duplicate-content -t note -t table
Directory: /home/user/my-docs

Found 3 groups of duplicate/similar content

======================================================================

[1] NOTE (EXACT) - 4 occurrences
--------------------------------------------------
  Content preview:
    For more information about configuring SSL/TLS, see the
    Security Guide.

  Locations:
    - modules/getting-started/pages/configuration.adoc:45
    - modules/security/pages/overview.adoc:23
    - modules/deployment/pages/kubernetes.adoc:112
    - modules/reference/pages/troubleshooting.adoc:78

[2] TABLE (85% similar) - 2 occurrences
--------------------------------------------------
  Content preview:
    |===
    | Property | Default | Description
    | quarkus.http.port | 8080 | The HTTP port
    ...

  Locations:
    - modules/configuration/pages/http.adoc:34
    - modules/reference/pages/properties.adoc:156
```

### CSV Format

```csv
Block Type,Similarity,Occurrences,File Path,Line Number,Content Preview
"note","exact",4,"modules/getting-started/pages/configuration.adoc",45,"For more information about..."
"table","0.85",2,"modules/configuration/pages/http.adoc",34,"|=== | Property | Default..."
```

## Understanding Similarity

The tool uses word-based Jaccard similarity to compare content blocks:

| Similarity | Meaning |
|------------|---------|
| 1.0 (100%) | Exact duplicates (identical content after normalizing whitespace) |
| 0.8-0.99 | Very similar content with minor differences |
| 0.7-0.79 | Similar structure with some different wording |
| Below 0.7 | Generally different content (not reported by default) |

Adjust the `-s` threshold based on your needs:
- `--exact-only` for identical content only
- `-s 0.9` for very similar content
- `-s 0.7` for a broader search including paraphrased content

## Refactoring Strategies

After identifying duplicates, consider these approaches:

### Create Reusable Includes

For content that should be identical everywhere:

```asciidoc
// In _partials/ssl-note.adoc
NOTE: For more information about configuring SSL/TLS, see the Security Guide.

// In your documentation files
\include::_partials/ssl-note.adoc[]
```

### Use Attributes for Variable Content

For content that differs slightly:

```asciidoc
// In attributes.adoc
:ssl-note: For more information about configuring SSL/TLS, see the Security Guide.

// In your documentation files
NOTE: {ssl-note}
```

### Create Shared Modules

For larger blocks of content (procedures, tables):

```asciidoc
// In shared/procedures/terminal-setup.adoc
. Open your terminal.
. Navigate to your project directory.
. Run the following command:

// In your documentation files
\include::shared::procedures/terminal-setup.adoc[]
```

## Limitations

- **Context sensitivity**: The tool cannot determine if similar content serves different purposes in different contexts
- **Semantic similarity**: Word-based comparison may miss semantically similar content with different wording
- **Large files**: Very large files may take longer to process
- **Nested structures**: Complex nested structures may not be parsed perfectly

## Notes

- Only `.adoc` files are scanned
- Symlinks are ignored
- Default excluded directories: `.git`, `.archive`, `target`, `build`, `node_modules`
- The tool does not modify any files

---

See the main [README.md](../README.md) for installation and usage details.
