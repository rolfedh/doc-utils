---
layout: default
title: extract-link-attributes
parent: Tools Reference
nav_order: 7
---

# extract-link-attributes

Extract link and xref macros containing attributes into reusable attribute definitions.

## Overview

The `extract-link-attributes` tool finds all `link:` and `xref:` macros whose URLs contain AsciiDoc attributes (like `{version}` or `{base-url}`), creates attribute definitions for them, and replaces the macros with attribute references throughout your documentation.

This tool is the complement to `replace-link-attributes`:
- **extract-link-attributes**: Creates attributes FROM link macros (this tool)
- **replace-link-attributes**: Replaces attributes IN link macros with resolved values

## Key Features

- **Auto-discovers** attribute files in your repository
- **Extracts** link/xref macros with attributes in their URLs
- **Creates** reusable attribute definitions
- **Handles** link text variations intelligently
- **Replaces** macros with attribute references
- **Preserves** macro type (link vs xref)
- **Reuses** existing attributes on subsequent runs

## When to Use

Use this tool when you want to:
- **Centralize link management** - Move all links to a single attributes file
- **Improve maintainability** - Update URLs in one place instead of many
- **Ensure consistency** - All references to the same URL use the same attribute
- **Follow DRY principle** - Don't Repeat Yourself for link definitions

## How It Works

### 1. Scanning Phase
The tool scans all `.adoc` files for link and xref macros that contain attributes:

```asciidoc
// These would be extracted:
link:https://docs.example.com/{version}/guide.html[User Guide]
xref:{base-url}/api/overview.html[API Overview]

// These would be ignored (no attributes):
link:https://example.com/static.html[Static Link]
xref:chapter-1.adoc[Chapter 1]
```

### 2. Attribute Creation
For each unique URL, the tool:
- Generates a meaningful attribute name based on the URL
- Creates an attribute containing the complete macro
- Handles duplicate URLs intelligently

```asciidoc
// Generated attributes:
:link-docs-example-guide: link:https://docs.example.com/{version}/guide.html[User Guide]
:xref-api-overview: xref:{base-url}/api/overview.html[API Overview]
```

### 3. Link Text Variations
When the same URL appears with different link text:

**Interactive Mode (default):**
- Shows all text variations
- Lets you choose the preferred text
- Option to enter custom text

**Non-interactive Mode:**
- Automatically uses the most common text variation

### 4. Replacement
Replaces all occurrences with attribute references:

```asciidoc
// Before:
See link:https://docs.example.com/{version}/guide.html[User Guide] for details.

// After:
See {link-docs-example-guide} for details.
```

## Basic Usage

### Interactive Mode (Default)

```bash
# Auto-discover attribute files and process interactively
extract-link-attributes

# You'll be prompted for:
# - Which attribute file to use (if multiple found)
# - Which link text to use (if variations exist)
```

### Non-Interactive Mode

```bash
# Automatically use most common link text for variations
extract-link-attributes --non-interactive

# Specify attribute file directly
extract-link-attributes --attributes-file common-attributes.adoc --non-interactive
```

### Preview Changes

```bash
# See what would be changed without modifying files
extract-link-attributes --dry-run
```

## Advanced Usage

### Specify Directories

```bash
# Scan specific directories only
extract-link-attributes --scan-dir modules --scan-dir assemblies

# Combine with other options
extract-link-attributes \
  --scan-dir docs \
  --attributes-file attributes.adoc \
  --non-interactive
```

### Handling Reruns

The tool intelligently handles repeated execution:

1. **New files with existing URLs**: If you add a new file containing a link with a URL that already has an attribute, the tool will:
   - Skip creating a duplicate attribute
   - Replace the link with the existing attribute reference

2. **New URLs**: Creates new attributes only for URLs not already in the attributes file

3. **Idempotent**: Running multiple times is safe and won't create duplicates

Example scenario:
```bash
# First run: Creates attributes for all found links
extract-link-attributes

# Add new file with mix of existing and new URLs
echo "link:https://docs.example.com/{version}/guide.html[Setup]" > new-file.adoc
echo "link:https://new-site.com/{version}/help.html[Help]" >> new-file.adoc

# Second run: Reuses existing attribute for guide.html, creates new for help.html
extract-link-attributes
```

## Command Options

| Option | Description |
|--------|-------------|
| `--attributes-file FILE` | Path to attributes file (auto-discovered if not specified) |
| `--scan-dir DIR` | Directory to scan (can be used multiple times, default: current) |
| `--non-interactive` | Automatically use most common link text for variations |
| `--dry-run` | Preview changes without modifying files |
| `-v, --verbose` | Enable verbose output |
| `-h, --help` | Show help message |

## Examples

### Example 1: Initial Extraction

```bash
$ extract-link-attributes --dry-run

Using attribute file: common-attributes.adoc
Loaded 5 existing attributes

Scanning for link and xref macros with attributes...
Found 23 link/xref macros with attributes
Grouped into 12 unique URLs

Multiple link text variations found for URL: https://docs.redhat.com/{product-version}/guide.html
Please select the preferred text:

  1. "Installation Guide"
     Used in: modules/intro.adoc:45, modules/setup.adoc:12

  2. "Setup Guide"
     Used in: modules/config.adoc:78

  3. Enter custom text

Enter your choice (1-3): 1

Created attribute: :link-docs-redhat-guide: link:https://docs.redhat.com/{product-version}/guide.html[Installation Guide]
[... more attributes created ...]

[DRY RUN] Would add 12 attributes to common-attributes.adoc
[DRY RUN] Would update 15 files with attribute references
```

### Example 2: Processing New Files

```bash
# After adding new documentation files
$ extract-link-attributes --non-interactive

Loaded 17 existing attributes

Scanning for link and xref macros with attributes...
Found 8 link/xref macros with attributes
Grouped into 5 unique URLs

URL already has attribute {link-docs-redhat-guide}: https://docs.redhat.com/{product-version}/guide.html
URL already has attribute {link-support-portal}: https://access.redhat.com/{product}/support.html
Created attribute: :link-api-reference: link:https://api.example.com/{version}/ref.html[API Reference]

Added 1 attribute to common-attributes.adoc
Updated modules/new-chapter.adoc: 3 replacements
Updated assemblies/new-guide.adoc: 5 replacements

Successfully extracted 1 link attribute
```

### Example 3: Creating Attributes File

```bash
$ extract-link-attributes

No attribute files found.
Create common-attributes.adoc? (y/n): y

Scanning for link and xref macros with attributes...
Found 15 link/xref macros with attributes
[... continues with extraction ...]
```

## Best Practices

1. **Run regularly**: Execute after adding new documentation to maintain consistency
2. **Use version control**: Commit changes after running to track modifications
3. **Review generated names**: Check that auto-generated attribute names are meaningful
4. **Standardize link text**: Use interactive mode initially to standardize link text across docs
5. **Document attributes**: Add comments above attribute groups in your attributes file

```asciidoc
// Product documentation links
:link-install-guide: link:https://docs.example.com/{version}/install.html[Installation Guide]
:link-user-guide: link:https://docs.example.com/{version}/user.html[User Guide]

// Support resources
:link-support-portal: link:https://support.example.com/{product}[Support Portal]
:link-knowledge-base: link:https://kb.example.com/{product}/search[Knowledge Base]
```

## Integration with CI/CD

```yaml
# Example GitHub Action
name: Extract Link Attributes
on:
  push:
    paths:
      - '**.adoc'

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install doc-utils
        run: pip install rolfedh-doc-utils

      - name: Extract link attributes
        run: |
          extract-link-attributes \
            --attributes-file common-attributes.adoc \
            --non-interactive

      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add -A
          git diff --staged --quiet || git commit -m "Extract link attributes"
          git push
```

## Troubleshooting

### No macros found
- Ensure your links contain attributes (e.g., `{version}`)
- Check that you're scanning the right directories
- Verify `.adoc` file extensions

### Wrong link text selected
- Use interactive mode to manually select
- Or edit the attributes file after extraction

### Attribute names not meaningful
- The tool generates names from URLs
- You can manually rename attributes after extraction
- Just ensure you update all references

## Related Tools

- [replace-link-attributes](replace-link-attributes.md) - Replace attributes in URLs with resolved values
- [find-unused-attributes](find-unused-attributes.md) - Find attributes that aren't referenced