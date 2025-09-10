---
layout: page
title: format-asciidoc-spacing
---

# AsciiDoc Spacing Formatter

A Python utility script that ensures proper spacing in AsciiDoc files by adding blank lines after headings and around `include::` directives.

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

Adds blank lines before and after `include::` directives to separate them from surrounding content.

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

## Usage

### Basic Usage

```bash
# Process current directory
./format-asciidoc-spacing.py

# Process specific directory
./format-asciidoc-spacing.py modules/

# Process single file
./format-asciidoc-spacing.py assemblies/my-guide.adoc
```

### Options

```bash
./format-asciidoc-spacing.py [OPTIONS] [PATH]

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
./format-asciidoc-spacing.py --dry-run modules/
```

**Process with detailed output:**
```bash
./format-asciidoc-spacing.py --verbose assemblies/
```

**Process all .adoc files recursively:**
```bash
./format-asciidoc-spacing.py .
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
./format-asciidoc-spacing.py --dry-run --verbose

# Apply changes
./format-asciidoc-spacing.py --verbose

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
./format-asciidoc-spacing.py --dry-run . && echo "Formatting is correct" || echo "Files need formatting"
```

## Edge Cases Handled

### Consecutive Elements
- **Consecutive headings**: No blank line added between them
- **Consecutive includes**: Proper spacing maintained between each
- **Mixed content**: Smart handling of headings followed by includes

### File Boundaries
- **Beginning of file**: No blank line added before first heading
- **End of file**: No trailing blank lines added unnecessarily
- **Empty files**: Handled gracefully without errors

### Special Cases
- **Comments**: AsciiDoc comments are preserved and don't interfere with spacing
- **Code blocks**: Content within code blocks is never modified
- **Existing spacing**: Multiple existing blank lines are preserved

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
chmod +x format-asciidoc-spacing.py

# Check directory permissions
ls -la target-directory/
```

### File Processing Issues
```bash
# Use verbose mode to identify problematic files
./format-asciidoc-spacing.py --verbose --dry-run problematic-file.adoc

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