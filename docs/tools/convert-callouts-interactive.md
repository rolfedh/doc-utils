---
layout: default
title: convert-callouts-interactive
nav_order: 13
---

# Convert Callouts Interactively

Interactive tool for converting AsciiDoc code blocks with callouts. For each code block, you choose whether to convert to definition lists, bulleted lists, or inline comments.

{: .note }
> **Choosing the Right Tool**
>
> This is the **interactive conversion** tool - it prompts you to choose the format for each individual code block. Use this when different blocks need different formats or when you want to review each conversion decision.
>
> For **batch processing** with a single target format across all code blocks, see [convert-callouts-to-deflist](convert-callouts-to-deflist).
>
> **Quick Decision Guide:**
> - Same format for all blocks → Use [`convert-callouts-to-deflist`](convert-callouts-to-deflist)
> - Different formats per block → Use this tool (`convert-callouts-interactive`)
> - Automation/CI pipelines → Use [`convert-callouts-to-deflist`](convert-callouts-to-deflist)
> - Editorial review needed → Use this tool (`convert-callouts-interactive`)

## Overview

While [`convert-callouts-to-deflist`](convert-callouts-to-deflist) processes files in batch mode with a single target format, this interactive tool gives you fine-grained control over each individual code block. This is ideal when:

- Different code blocks in the same file need different formats
- You want to review each conversion before applying it
- You need to make editorial decisions based on context
- You're migrating documentation and want to selectively modernize callouts

The tool automatically detects **list-format** (`<1> Explanation`) and **multi-column table formats** (2-column and 3-column) for callout explanations, handling all formats transparently.

## Installation

Install with the doc-utils package:

```bash
pipx install rolfedh-doc-utils
```

Then run directly as a command:

```bash
convert-callouts-interactive [options] [path]
```

## Features

### Automatic Format Detection

Automatically detects and processes multiple input formats:
- **List format**: Traditional `<1> Explanation` style
- **Multi-column tables**: 2-column and 3-column table formats with callout explanations
- **Conditional statements**: Preserves `ifdef::`/`ifndef::`/`endif::` in table cells

### Per-Block Conversion Choices

For each code block with callouts, you can choose:
- **Definition list** - Uses "where:" prefix with AsciiDoc definition lists
- **Bulleted list** - Follows Red Hat style guide format
- **Inline comments** - Embeds explanations as code comments
- **Skip** - Leave the block unchanged

### Smart Comment Handling

For inline comments format:
- Detects programming language from `[source,language]` attribute
- Uses appropriate comment syntax (40+ languages supported)
- Interactive warning prompt if comment exceeds maximum length (default: 120 characters)
- Four options when comment is too long:
  - Shorten to first sentence
  - Fall back to definition list
  - Fall back to bulleted list
  - Skip the block

### Rich Preview Display

Before each conversion decision, you'll see:
- File name and line numbers
- Programming language (if specified)
- Context lines before and after the code block (adjustable with `--context`)
- The code block itself with callouts highlighted in color
- Callout explanations

### Batch Apply Option

Once you've chosen a format you like, you can apply it to all remaining code blocks in that file, speeding up the conversion process.

### Validation and Safety

- Validates callout numbers match between code and explanations
- Skips blocks with mismatched numbers and displays warnings
- Color-coded output for easy scanning
- Dry-run mode to preview all decisions
- Automatically excludes `.vale` directory

## Usage

### Process Single File

```bash
convert-callouts-interactive myfile.adoc
```

### Process Directory

```bash
convert-callouts-interactive modules/
```

The tool will scan all `.adoc` files and present each code block with callouts for your decision.

### Preview Mode (Dry Run)

```bash
convert-callouts-interactive --dry-run modules/
```

Make all your conversion choices and see what would be changed, but don't actually modify the files.

### Adjust Context Lines

```bash
convert-callouts-interactive --context 5 myfile.adoc
```

Show more or fewer context lines around each code block (default: 3).

### Exclude Directories

```bash
convert-callouts-interactive --exclude-dir archive --exclude-dir temp modules/
```

Excludes specified directories from processing. Note: `.vale` is excluded by default.

### Use Exclusion List File

```bash
convert-callouts-interactive --exclude-list .docutils-ignore modules/
```

Example `.docutils-ignore` file:
```
# Directories to exclude
.vale/
archive/
temp/

# Specific files
test-file.adoc
```

## Interactive Workflow

### Step 1: Code Block Preview

The tool displays a code block with:

```
================================================================================

File: modules/security/proc_configuring-auth.adoc
Code block at lines 15-25
Language: yaml

  ... context before ...
    12 | For example:
    13 |
    14 |
    15 | [source,yaml]
    16 | ----
    17 | apiVersion: v1
    18 | kind: Secret
    19 | metadata:
    20 |   name: <my-secret> <1>
    21 | data:
    22 |   key: <my-key> <2>
    23 | ----
    24 |
  ... callout explanations ...
    25 | <1> The secret name
    26 | <2> The secret key value
    27 |

```

Lines with callouts are highlighted to help you quickly identify what's being explained.

### Step 2: Choose Format

```
[Code block 1/3]

Choose conversion format:
  [d] Definition list (where:)
  [b] Bulleted list
  [c] Inline comments
  [s] Skip this block
  [a] Apply choice to All remaining blocks
  [q] Skip current file
  [Q] Quit script entirely (Ctrl+C)

Your choice [d/b/c/s/a/q/Q]:
```

### Step 3: Review and Continue

After each choice, the tool confirms your decision and moves to the next code block. At the end, you'll see a summary:

```
================================================================================

Summary:
  Files processed: 1
  Files modified: 1
  Total conversions: 3

================================================================================
```

## Conversion Format Examples

### Definition List Format

```asciidoc
[source,yaml]
----
name: <my-secret>
key: <my-key>
----

where:

`<my-secret>`::
The secret name

`<my-key>`::
The secret key value
```

### Bulleted List Format

```asciidoc
[source,yaml]
----
name: <my-secret>
key: <my-key>
----

*   `<my-secret>`: The secret name

*   `<my-key>`: The secret key value
```

### Inline Comments Format

```asciidoc
[source,yaml]
----
name: <my-secret> # The secret name
key: <my-key> # The secret key value
----
```

The original `<1>` and `<2>` explanation lines are removed when using inline comments format.

## Options

- `path` - File or directory to process (default: current directory)
- `-n, --dry-run` - Preview all changes without modifying files
- `-c, --context N` - Number of context lines to show (default: 3)
- `--max-comment-length N` - Maximum comment length in characters (default: 120). Shows interactive warning prompt if exceeded
- `--exclude-dir DIR` - Exclude directory (can be used multiple times)
- `--exclude-file FILE` - Exclude file (can be used multiple times)
- `--exclude-list FILE` - Load exclusion list from file
- `-h, --help` - Show help message

## When to Use Interactive vs Batch Mode

**Use `convert-callouts-interactive` when:**
- Different code blocks need different formats
- You want to review each conversion decision
- You're doing selective modernization of documentation
- Editorial judgment is needed for each code example

**Use `convert-callouts-to-deflist` when:**
- You want consistent formatting across all code blocks
- You're processing a large number of files with the same target format
- You want to automate the conversion in a script or CI pipeline
- Speed is more important than per-block control

## Example Workflow

```bash
# Create a feature branch
git checkout -b modernize-callouts

# Start interactive conversion
convert-callouts-interactive modules/security/

# For each code block, choose:
#   - [d] for YAML configurations (definition list)
#   - [b] for multi-value configs (bulleted list)
#   - [c] for short code snippets (inline comments)
#   - [s] to skip legacy examples

# After processing all blocks, review changes
git diff

# Test documentation build
./scripts/build-docs.sh

# Commit
git add modules/security/
git commit -m "Modernize security module callouts"
```

## Keyboard Shortcuts

During the conversion process:

- `d` - Convert to definition list
- `b` - Convert to bulleted list
- `c` - Convert to inline comments
- `s` - Skip this code block
- `a` - Apply same choice to all remaining blocks
- `q` - Skip current file (moves to next file)
- `Q` - Quit script entirely (immediate exit)
- `Ctrl+C` - Quit script entirely (immediate exit)

## Color-Coded Output

The tool uses colors to help you quickly identify different parts of the output:

- **Blue** - File metadata and code block location
- **Yellow** - Code block delimiters and [source] attributes
- **Magenta** - Lines containing callouts
- **Cyan** - Context lines and callout explanations
- **Green** - Success messages and summaries
- **Red** - Errors
- **Yellow** - Warnings (callout mismatches, etc.)

## Safety Features

- Always shows a preview before asking for conversion choice
- Validates that callout numbers in code match explanations
- Skips blocks with mismatched callouts (displays warnings)
- Supports dry-run mode to preview all decisions without modifying files
- Automatically excludes `.vale` directory
- Quit script entirely with `Q` (capital) or `Ctrl+C`
- Skip to next file with `q` (lowercase)

## Warnings and Edge Cases

### Callout Mismatch Warnings

The tool validates that callout numbers in code match the numbers in explanations. If there's a mismatch, it displays a warning and skips that block:

```
WARNING: file.adoc lines 55-72: Callout mismatch: code has [1, 2, 3, 4, 5, 6, 7, 8, 9],
explanations have [1, 2, 3, 4, 5, 7, 8, 8, 9]
```

**Duplicate Detection**: The warning shows duplicate callout numbers in tables (notice `8, 8` indicating two rows with callout 8).

Common causes:
- Missing callout in table (callout 6 in example above)
- Duplicate callout numbers in table (documentation error)
- Callouts renumbered in code but not in explanations

### Missing Explanations Warning

When a code block has callouts but no explanations are found after it:

```
WARNING: file.adoc line 211: Code block has callouts [1, 2, 3, 4] but no explanations found after it.
This may indicate: explanations are shared with another code block, explanations are in an unexpected
location, or documentation error (missing explanations). Consider reviewing this block manually.
```

This commonly occurs with:
- **Shared explanations** between conditional blocks (`ifdef::community[]` and `ifdef::product[]`)
- **Unexpected location** of explanations (not immediately after code block)
- **Missing explanations** (documentation error)

**Action**: Review these blocks manually to determine correct handling.

## Technical Details

This tool uses the same [`callout_lib`](https://github.com/rolfedh/doc-utils/tree/main/callout_lib) Python library as the batch converter, ensuring consistent output quality. See the [library README](https://github.com/rolfedh/doc-utils/blob/main/callout_lib/README.md) for detailed implementation information.

**Key Differences from Batch Tool:**
- Interactive prompts for format selection per code block
- Live preview with color-coded output
- Interactive warning prompts for long comments with multiple resolution options
- "Apply to all" option for remaining blocks
- Context-adjustable display

**Supported Comment Syntax (for inline comments format):**
- C-style `//`: Java, JavaScript, TypeScript, C, C++, Go, Rust, Swift, Kotlin, etc.
- Hash `#`: Python, Ruby, Bash, YAML, Shell, Perl, R, etc.
- SQL `--`: SQL, PL/SQL, T-SQL, Lua
- HTML/XML `<!--`: HTML, XML, SVG
- Others: Lisp `;`, MATLAB/LaTeX `%`, etc. (40+ languages total)

## Related Tools

- [`convert-callouts-to-deflist`](convert-callouts-to-deflist) - Batch converter for uniform format across files

---

See the main [Tools Reference](index) for more documentation utilities.
