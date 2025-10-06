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

**NEW**: The tool now also replaces existing link macros with attribute references when matching attributes already exist, making it useful for both initial extraction and ongoing maintenance.

This tool is the complement to `replace-link-attributes`:
- **extract-link-attributes**: Creates attributes FROM link macros (this tool)
- **replace-link-attributes**: Replaces attributes IN link macros with resolved values

## Key Features

- **Auto-discovers** attribute files in your repository
- **Extracts** link/xref macros with attributes in their URLs
- **Creates** reusable attribute definitions
- **Handles** link text variations intelligently
- **Replaces** macros with attribute references (both new and existing)
- **Preserves** macro type (link vs xref)
- **Reuses** existing attributes on subsequent runs
- **Smart replacement** - replaces link macros with existing attributes when URLs match

## When to Use

Use this tool when you want to:
- **Centralize link management** - Move all links to a single attributes file
- **Improve maintainability** - Update URLs in one place instead of many
- **Ensure consistency** - All references to the same URL use the same attribute
- **Follow DRY principle** - Don't Repeat Yourself for link definitions
- **Clean up existing docs** - Replace verbose link macros with concise attribute references

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
The tool replaces macros with attribute references in two scenarios:

**A) New attributes created:**
```asciidoc
// Before:
See link:https://docs.example.com/{version}/guide.html[User Guide] for details.

// After (new attribute created):
See {link-docs-example-guide} for details.
```

**B) Existing attributes matched:**
```asciidoc
// Existing attribute in attributes.adoc:
:link-telemetry-micrometer-to-opente: link:{quarkusio-guides}/telemetry-micrometer-to-opentelemetry[Micrometer and OpenTelemetry extension]

// Before in your .adoc file:
For more information, see the {ProductName} link:{quarkusio-guides}/telemetry-micrometer-to-opentelemetry[Micrometer and OpenTelemetry extension] guide.

// After (existing attribute used):
For more information, see the {ProductName} {link-telemetry-micrometer-to-opente} guide.
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

### Validate Link Attributes

**NEW**: Validate URLs in link attributes before extraction to ensure they're not broken:

```bash
# Validate existing link-* attributes
extract-link-attributes --validate-links

# Exit if broken links are found
extract-link-attributes --validate-links --fail-on-broken

# Combine with non-interactive mode for CI/CD
extract-link-attributes \
  --validate-links \
  --fail-on-broken \
  --non-interactive
```

When validation finds issues:
```
Validating links in common-attributes.adoc...
✓ Validated 10 link attributes: 8 valid, 2 broken

⚠️  Broken link attributes found:
  Line 45: :link-old-api: https://api.example.com/v1/deleted
  Line 67: :link-deprecated: https://legacy.example.com/old

Stopping extraction due to broken links (--fail-on-broken)
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

### Process Specific Macro Types

```bash
# Process only link: macros (ignore xref:)
extract-link-attributes --macro-type link

# Process only xref: macros (ignore link:)
extract-link-attributes --macro-type xref

# Process both (default behavior)
extract-link-attributes --macro-type both
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
| `--validate-links` | Validate URLs in link-* attributes before extraction |
| `--fail-on-broken` | Exit extraction if broken links are found (requires --validate-links) |
| `--macro-type {link,xref,both}` | Type of macros to process: link, xref, or both (default: both) |
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

Successfully processed 3 link attributes:
  - Created 1 new attribute
  - Replaced macros using 2 existing attributes
```

### Example 3: Using Existing Attributes Only

```bash
# When no new attributes are needed (all URLs match existing ones)
$ extract-link-attributes --scan-dir modules/rn --attributes-file common/attributes.adoc

Loaded 394 existing attributes

Scanning for link and xref macros with attributes...
Found 14 link/xref macros with attributes
Grouped into 14 unique URLs

URL already has attribute {link-telemetry-micrometer-to-opente}: {quarkusio-guides}/telemetry-micrometer-to-opentelemetry
URL already has attribute {link-step-up-authentication}: {URL_OIDC_AUTHENTICATION}/#step-up-authentication
[... 12 more existing URLs ...]

Updated 9 files: 14 total replacements

Successfully replaced macros using 14 existing link attributes
```

### Example 4: Creating Attributes File

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
            --validate-links \
            --fail-on-broken \
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