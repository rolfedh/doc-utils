# replace-link-attributes

Replace AsciiDoc attributes within link URLs with their actual values.

## Purpose

This tool helps resolve Vale AsciiDocDITA style violations for the `LinkAttribute` rule:

> **LinkAttribute**: DITA 1.3 does not allow references to reusable content in link URLs. Remove attribute references from the link or replace the entire link macro with an attribute reference.

When converting AsciiDoc to DITA, link and xref macros cannot contain attribute references (like `{product-name}`) in their URL portions. This tool automatically finds and replaces these attribute references with their resolved values from your attributes file.

## What it does

- Finds all `link:` and `xref:` macros containing attribute references in URLs
- Replaces attribute references with their actual values from attributes files
- Preserves link text exactly as written (only modifies URLs)
- Resolves nested attribute references automatically
- Supports both `link:url[text]` and `xref:target[text]` formats

## Installation

```bash
pip install rolfedh-doc-utils
```

## Usage

### Basic usage (interactive mode)

```bash
replace-link-attributes
```

The tool will:
1. Search for `attributes.adoc` files in your repository
2. Present options if multiple files are found
3. Allow you to specify a custom file path if needed
4. Process all AsciiDoc files and replace attribute references in links

### Specify attributes file directly

```bash
replace-link-attributes --attributes-file path/to/attributes.adoc
```

### Dry run mode (preview changes)

```bash
replace-link-attributes --dry-run
```

### Process a different directory

```bash
replace-link-attributes --path /path/to/docs
```

## Examples

### Before and after

**attributes.adoc:**
```asciidoc
:product-name: Red Hat Enterprise Linux
:product-version: 9
:docs-url: https://docs.redhat.com
```

**Before:**
```asciidoc
For more information, see link:{docs-url}/rhel/{product-version}[{product-name} Documentation].

See xref:{product-name}-guide.adoc[Installation Guide].
```

**After:**
```asciidoc
For more information, see link:https://docs.redhat.com/rhel/9[{product-name} Documentation].

See xref:Red Hat Enterprise Linux-guide.adoc[Installation Guide].
```

Note: Link text is preserved as-is, including any attribute references.

### Handling custom attribute files

The tool can work with any attribute file, not just `attributes.adoc`:

```bash
# Use a specific file
replace-link-attributes -a common/shared-attributes.adoc

# Interactive mode will find all attributes.adoc files and offer custom path option
replace-link-attributes
```

## Command-line options

- `--dry-run`, `-n`: Preview changes without modifying files
- `--path`, `-p PATH`: Repository path to search (default: current directory)
- `--attributes-file`, `-a FILE`: Path to attributes file (skips interactive selection)
- `--help`, `-h`: Show help message

## Features

- **Automatic discovery**: Finds all `attributes.adoc` files in subdirectories
- **Interactive selection**: Choose from found files or specify custom paths
- **Nested resolution**: Handles attributes that reference other attributes
- **Safe operation**: Dry-run mode to preview changes before applying
- **Comprehensive**: Processes all `.adoc` files in the repository
- **Preserves formatting**: Only modifies URL portions, leaving link text unchanged

## Limitations

- Only processes `link:` and `xref:` macros
- Does not modify attribute references in other contexts
- Requires attribute definitions to follow standard AsciiDoc format (`:attribute-name: value`)

## Exit codes

- 0: Success (replacements made or no replacements needed)
- 1: Error (file not found, invalid directory, etc.)