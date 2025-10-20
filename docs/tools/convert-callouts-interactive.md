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

### Per-Block Conversion Choices

For each code block with callouts, you can choose:
- **Definition list** - Uses "where:" prefix with AsciiDoc definition lists
- **Bulleted list** - Follows Red Hat style guide format
- **Inline comments** - Embeds explanations as code comments
- **Skip** - Leave the block unchanged

### Rich Preview Display

Before each conversion decision, you'll see:
- File name and line numbers
- Programming language (if specified)
- Context lines before and after the code block
- The code block itself with callouts highlighted in color
- Callout explanations

### Batch Apply Option

Once you've chosen a format you like, you can apply it to all remaining code blocks in that file, speeding up the conversion process.

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
  [q] Quit

Your choice [d/b/c/s/a/q]:
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
- `--exclude-dir DIR` - Exclude directory (can be used multiple times)
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
- `q` or `Ctrl+C` - Quit without saving remaining changes

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
- Quit anytime with `q` or `Ctrl+C`

## Technical Details

The interactive converter uses the same conversion library as the batch tool, ensuring consistent output quality across both utilities. See [`convert-callouts-to-deflist`](convert-callouts-to-deflist#technical-details) for pattern matching and algorithm details.

## Related Tools

- [`convert-callouts-to-deflist`](convert-callouts-to-deflist) - Batch converter for uniform format across files

---

See the main [Tools Reference](index) for more documentation utilities.
