---
layout: default
title: find-unused-attributes
nav_order: 9
---

# Find Unused AsciiDoc Attributes

> ⚠️ **IMPORTANT: Work in a Git Branch**
>
> While this tool only reports unused attributes and doesn't modify files, when cleaning up attributes:
> 1. **Create a git branch first**: `git checkout -b cleanup-attributes`
> 2. **Review the report carefully** - some attributes may be used in ways the tool cannot detect
> 3. **Search for each attribute** before removing it from your attributes file
> 4. **Test your documentation build** after removing attributes
> 5. **Check preview builds** to ensure no broken attribute references

This tool scans an attributes file for attribute definitions (e.g., `:version: 1.1`). It then recursively scans all `.adoc` files in the current directory (ignoring symlinks) for usages of those attributes.

**NEW: Auto-discovery Feature** - If no attributes file is specified, the tool will automatically search for attributes files in your repository and let you choose one interactively.

Any attribute defined in the attributes file but not used in any `.adoc` file is reported as **NOT USED** in both the command line output and a timestamped output file (if requested).

## What This Tool Detects

The tool searches for attributes used in two ways:

1. **Attribute references**: `{attribute-name}` - used for text substitution
2. **Conditional directives**: `ifdef::attribute[]`, `ifndef::attribute[]`, `endif::attribute[]` - used for conditional content inclusion/exclusion

## Installation

After installing the package from PyPI:

```sh
pip install rolfedh-doc-utils
```

You can run the tool from anywhere using:

```sh
# With auto-discovery (NEW)
find-unused-attributes [-o|--output] [-c|--comment-out]

# With explicit path (backward compatible)
find-unused-attributes attributes.adoc [-o|--output] [-c|--comment-out]
```

Or, if running from source:

```sh
# With auto-discovery
python3 find_unused_attributes.py [-o|--output] [-c|--comment-out]

# With explicit path
python3 find_unused_attributes.py attributes.adoc [-o|--output] [-c|--comment-out]
```

### Options

- `-o, --output`: Write results to a timestamped txt file in your home directory
- `-c, --comment-out`: Comment out unused attributes in the attributes file with "// Unused" prefix (requires confirmation)

## Auto-discovery Feature

When you run `find-unused-attributes` without specifying a file:

1. **Single file found**: The tool will show the found file and ask for confirmation:
   ```
   Found attributes file: modules/attributes.adoc
   Use this file? (y/n):
   ```

2. **Multiple files found**: The tool presents an interactive menu:
   ```
   Found multiple attributes files:
     1. modules/attributes.adoc
     2. common-attributes.adoc
     3. Enter custom path

   Select option (1-3) or 'q' to quit:
   ```

3. **No files found**: The tool will inform you and suggest manual specification:
   ```
   No attributes files found in the repository.
   You can specify a file directly: find-unused-attributes <path-to-attributes-file>
   ```

The auto-discovery searches for common patterns like:
- `**/attributes.adoc`
- `**/attributes*.adoc`
- `**/*attributes.adoc`
- `**/*-attributes.adoc`

It automatically excludes hidden directories and build directories (`.archive`, `target`, `build`, `node_modules`).

## Examples

### Example 1: Attribute References

Suppose `attributes.adoc` contains:

```
:version: 1.1
:product: MyApp
:unused: something
```

And your `.adoc` files use `{version}` and `{product}` but not `{unused}`. The output will be:

```
Unused attributes:
:unused:  NOT USED
```

### Example 2: Conditional Directives

Suppose `attributes.adoc` contains:

```
:downstream:
:rh-only:
:no-feature-x:
:truly-unused:
```

And your `.adoc` files contain:

```asciidoc
ifdef::downstream[]
This content only appears in downstream builds.
endif::downstream[]

ifndef::no-feature-x[]
Documentation for Feature X.
endif::no-feature-x[]
```

The output will be:

```
Unused attributes:
:truly-unused:  NOT USED
```

The attributes `:downstream:`, `:rh-only:`, and `:no-feature-x:` are correctly recognized as used because they appear in conditional directives.

### Output File

If you use `-o`, a file like `~/unused_attributes_20250611123456.txt` will be created with the same content.

## Comment Out Feature

The `--comment-out` option allows you to automatically comment out unused attributes in your attributes file. This is safer than deleting them, as you can easily uncomment them if needed.

### Usage

```sh
find-unused-attributes common/attributes.adoc --comment-out
```

The tool will:
1. Show you the list of unused attributes
2. Ask for confirmation before modifying the file
3. Comment out each unused attribute with `// Unused` prefix

### Example

Before:
```asciidoc
:version: 1.0
:product: MyApp
:unused-attr: some value
:rh-only:
```

After running with `--comment-out`:
```asciidoc
:version: 1.0
:product: MyApp
// Unused :unused-attr: some value
:rh-only:
```

### Safety Features

- **Confirmation prompt**: You must confirm before any changes are made
- **Preserves formatting**: All other lines, comments, and blank lines remain unchanged
- **Non-destructive**: Commented-out attributes can be easily restored by removing the `// Unused` prefix
- **Git-friendly**: Work in a git branch so you can easily revert if needed

## AsciiDoc Configuration Attributes

Some AsciiDoc attributes control how the documentation processor works rather than appearing directly in your content. These attributes may be reported as unused by the tool, but they are critical to your documentation build.

**Examples from a typical attributes file:**

```asciidoc
// AsciiDoc settings
:data-uri!:
:doctype: book
:experimental:
:idprefix:
:imagesdir: resources/images
:includes: resources/snippets
:sectanchors!:
:sectlinks:
:source-highlighter: highlightjs
:linkattrs:
:toclevels: 3
:idseparator: -
:icons: font
:iconsdir: images/icons/
:generated-dir: _generated
:code-examples: _generated/examples
:doc-guides:
:quarkusio-guides: {url-quarkusio-guides}
:doc-examples: examples
:includes: _includes
```

**What these do:**
- `:idprefix:` - Removes underscore prefix from auto-generated section IDs (e.g., `startup-checks` instead of `_startup-checks`)
- `:idseparator: -` - Uses hyphens in auto-generated IDs
- `:doctype: book` - Sets document structure type
- `:experimental:` - Enables keyboard shortcuts and UI macros
- `:icons: font` - Uses font-based icons instead of images
- `:source-highlighter:` - Configures code syntax highlighting
- `:toclevels:` - Controls table of contents depth
- `:sectlinks:` - Makes section headings clickable
- `:linkattrs:` - Allows attributes in link text

**⚠️ Important**: Never comment out or remove these attributes without testing your documentation build. They don't appear in content files but are essential for correct rendering. Always review preview builds after making changes.

## Notes

- Only `.adoc` files in the current directory and its subdirectories are scanned.
- Symlinks are ignored.
- The tool detects attributes used in:
  - Text substitution: `{attribute-name}`
  - Conditional directives: `ifdef::attribute[]`, `ifndef::attribute[]`, `endif::attribute[]`
- The script does not modify any files (unless you use `--comment-out`).
- This tool does not currently support file/directory exclusions.
- **Known limitation**: AsciiDoc configuration attributes (e.g., `:doctype:`, `:experimental:`, `:icons:`) may be reported as unused since they configure the processor itself rather than being referenced in content. See the section above for details.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
