---
layout: default
title: format-asciidoc-spacing [EXPERIMENTAL]
parent: Tools Reference
nav_order: 2
---

# format-asciidoc-spacing [EXPERIMENTAL]

⚠️ **EXPERIMENTAL FEATURE**: This tool is under active development. The formatting rules and behavior may change in future versions based on user feedback.

A Python utility script that ensures proper spacing in AsciiDoc files by intelligently adding blank lines after headings and around `include::` directives, with special handling for attributes, comments, conditionals, and admonition blocks.

## Purpose

This tool standardizes whitespace formatting in AsciiDoc documentation to improve readability and maintain consistent style across documentation repositories.

## Formatting Rules

### 1. Blank Lines After Headings

Ensures there's a blank line after each heading (=, ==, ===, etc.) when followed by content.

**Before:**
```asciidoc
== This is a heading
In the beginning...
```

**After:**
```asciidoc
== This is a heading

In the beginning...
```

### 2. Blank Lines Around Include Directives

Adds blank lines before and after `include::` directives to separate them from surrounding content. This includes adding blank lines between consecutive include statements.

**Before:**
```asciidoc
This is text.
include::modules/ref_12345.adoc[]
include::modules/ref_4567.adoc[]
More text follows.
```

**After:**
```asciidoc
This is text.

include::modules/ref_12345.adoc[]

include::modules/ref_4567.adoc[]

More text follows.
```

### 3. Special Handling for Attribute Includes

Attribute includes near the document header (H1) only get a single blank line after the heading, not additional lines around the include.

**Before:**
```asciidoc
= Document Title
include::_attributes/common-attributes.adoc[]
:context: my-context
```

**After:**
```asciidoc
= Document Title

include::_attributes/common-attributes.adoc[]
:context: my-context
```

### 4. Comments and Attributes with Includes

Comments and attributes directly above includes are kept together as a unit with the include. When a comment precedes an include, blank lines are added before the comment (to separate from previous content), but not between the comment and the include.

**Before:**
```asciidoc
include::modules/first.adoc[leveloffset=+1]
// This comment describes the second include
include::modules/second.adoc[leveloffset=+1]
include::modules/third.adoc[leveloffset=+1]

Another paragraph.
:FeatureName: Multi-network policies
include::snippets/technology-preview.adoc[]
```

**After:**
```asciidoc
include::modules/first.adoc[leveloffset=+1]

// This comment describes the second include
include::modules/second.adoc[leveloffset=+1]

include::modules/third.adoc[leveloffset=+1]

Another paragraph.

:FeatureName: Multi-network policies
include::snippets/technology-preview.adoc[]
```

### 5. Conditional Blocks

Conditional blocks (ifdef/ifndef/endif) are treated as single units with blank lines around the entire block. Comments preceding conditional blocks are kept together as a logical unit.

**Before:**
```asciidoc
Some content here.
// This module does not apply to OSD/ROSA
ifndef::openshift-rosa[]
include::modules/standard-features.adoc[]
endif::openshift-rosa[]
More content.
```

**After:**
```asciidoc
Some content here.

// This module does not apply to OSD/ROSA
ifndef::openshift-rosa[]
include::modules/standard-features.adoc[]
endif::openshift-rosa[]

More content.
```

### 6. Comment Blocks and Block Titles

Comment blocks (delimited by `////`) and block titles (like `.Prerequisites`, `.Additional resources`) receive proper spacing.

**Before:**
```asciidoc
////
This is a comment block explaining the following content.
////
.Prerequisites

* Item 1
* Item 2

[role="_additional-resources"]
.Additional resources
////
Optional section for additional links.
////
* link:https://example.com[Example]
```

**After:**
```asciidoc
////
This is a comment block explaining the following content.
////

.Prerequisites

* Item 1
* Item 2

[role="_additional-resources"]
.Additional resources
////
Optional section for additional links.
////

* link:https://example.com[Example]
```

## Usage

### Installation with pipx (Recommended)

```bash
# Install with pipx for global availability
pipx install rolfedh-doc-utils

# After installation, run directly (no .py extension, use hyphens not underscores):
format-asciidoc-spacing modules/
```

### Basic Usage

```bash
# Process current directory
format-asciidoc-spacing

# Process specific directory (e.g., OpenShift-docs structure)
format-asciidoc-spacing modules/
format-asciidoc-spacing microshift_networking/

# Process single file
format-asciidoc-spacing modules/networking/about-networking.adoc
```

### Manual Script Usage (if not using pipx)

```bash
# Make executable first
chmod +x format_asciidoc_spacing.py

# Then run
./format_asciidoc_spacing.py modules/
```

### Options

```bash
format-asciidoc-spacing [OPTIONS] [PATH]

OPTIONS:
    -h, --help     Show help message
    -n, --dry-run  Show what would be changed without modifying files
    -v, --verbose  Show detailed output

ARGUMENTS:
    PATH          File or directory to process (default: current directory)
```

### Examples

**Preview changes without modifying files:**
```bash
format-asciidoc-spacing --dry-run modules/
```

**Process with detailed output:**
```bash
format-asciidoc-spacing --verbose modules/
```

**Process all .adoc files recursively:**
```bash
format-asciidoc-spacing .
```

## Features

### Smart Processing
- **Preserves existing spacing** where appropriate
- **Handles edge cases** like consecutive headings or includes
- **Maintains file structure** and original content
- **Processes only .adoc files** automatically

### Safety Features
- **Dry-run mode** to preview changes before applying
- **Backup handling** through temporary files
- **Error handling** for file operations
- **Verbose output** to track changes made

### Performance
- **Efficient processing** of large documentation repositories
- **Recursive directory scanning** for .adoc files
- **Minimal memory usage** through line-by-line processing
- **Progress reporting** for large file sets

## Best Practices

### Before Running
1. **Work in a git branch** - Never run on main/master branch
2. **Commit pending changes** first
3. **Use dry-run mode** to preview changes
4. **Test on small files** first if unsure

### Recommended Workflow
```bash
# Create feature branch
git checkout -b fix-asciidoc-spacing

# Preview changes
format-asciidoc-spacing --dry-run --verbose

# Apply changes
format-asciidoc-spacing --verbose

# Review changes
git diff

# Commit if satisfied
git add -A
git commit -m "Standardize AsciiDoc spacing"
```

### Integration with CI/CD
The script can be integrated into documentation workflows:

```bash
# Check if files need formatting (returns non-zero if changes needed)
format-asciidoc-spacing --dry-run . && echo "Formatting is correct" || echo "Files need formatting"
```

## Edge Cases Handled

### Consecutive Elements
- **Consecutive headings**: No blank line added between them
- **Consecutive includes**: Blank lines added between each include statement
- **Mixed content**: Smart handling of headings followed by includes
- **Duplicate blank lines**: Consolidates multiple blank lines that would be inserted into a single blank line
- **Comments with conditionals**: Comments directly preceding conditional blocks stay together as a unit
- **Comments with includes**: Comments directly preceding includes stay together as a unit

### File Boundaries
- **Beginning of file**: No blank line added before first heading
- **End of file**: No trailing blank lines added unnecessarily
- **Empty files**: Handled gracefully without errors

### Special Cases
- **Admonition blocks**: Block delimiters (====, ----, ...., ____) are not treated as headings
- **Comment blocks**: Comment blocks (`////`) get blank line after closing delimiter
- **Block titles**: Block titles (`.Title`) get blank line before them, unless preceded by a role block
- **Role blocks**: Role blocks (`[role="..."]`) are recognized but don't add extra spacing
- **Comments with includes**: Comments directly above includes are kept together as a unit
- **Attributes with includes**: Attributes directly above includes are kept together as a unit
- **Conditional blocks**: ifdef/ifndef/endif blocks are treated as units with spacing around the entire block
- **Comments with conditionals**: Comments directly preceding conditionals stay together without intervening blank lines
- **Attribute includes near H1**: Special handling for common-attributes.adoc includes at document start

## Output Examples

### Dry-run Mode
```
DRY RUN MODE - No files will be modified
Would modify: modules/con_overview.adoc
Would modify: assemblies/main-guide.adoc
Processed 15 AsciiDoc file(s)
AsciiDoc spacing formatting complete!
```

### Verbose Mode
```
Processing: modules/con_overview.adoc
  Added blank line after heading: == Overview
  Added blank line before include: include::snippets/note.adoc[]
Modified: modules/con_overview.adoc
Processed 1 AsciiDoc file(s)
ASciiDoc spacing formatting complete!
```

## Requirements

- **Python 3.6+**
- **Standard library only** (no external dependencies)
- **UTF-8 file encoding support**
- **File system access** to target directory

## Limitations

- **AsciiDoc files only** - Processes .adoc files exclusively
- **Simple pattern matching** - Uses regex for heading and include detection
- **No syntax validation** - Doesn't verify AsciiDoc syntax correctness
- **Line-based processing** - Complex multi-line constructs may need manual review

## Troubleshooting

### Permission Issues
```bash
# Ensure script is executable
chmod +x format_asciidoc_spacing.py

# Check directory permissions
ls -la target-directory/
```

### File Processing Issues
```bash
# Use verbose mode to identify problematic files
format-asciidoc-spacing --verbose --dry-run problematic-file.adoc

# Check file encoding (script expects UTF-8)
file problematic-file.adoc
```

### Unexpected Results
- **Review with git diff** to understand changes made
- **Use dry-run first** to preview modifications
- **Process single files** to isolate issues
- **Check for binary files** in .adoc extensions

## Related Tools

This tool complements other doc-utils:
- **archive-unused-files**: Remove unused documentation files
- **check-scannability**: Analyze sentence and paragraph length
- **find-unused-attributes**: Identify unused AsciiDoc attributes

## Contributing

When contributing improvements:
1. **Test edge cases** thoroughly
2. **Maintain backward compatibility**
3. **Update examples** in this documentation
4. **Add appropriate error handling**
5. **Follow existing code style**