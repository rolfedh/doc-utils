---
layout: default
title: fix-bare-urls
parent: Tools Reference
nav_order: 23
---

# fix-bare-urls

Converts bare URLs to explicit `link:` macros in AsciiDoc files. Transforms `https://url[text]` to `link:https://url[text]` for compatibility with downstream publishing pipelines such as DITA/Pantheon.

## Overview

In standard AsciiDoc, bare URLs with bracket link text (e.g., `https://example.com[Example]`) are valid implicit URL macros. However, some publishing pipelines require the explicit `link:` macro prefix. This tool automates that conversion across an entire documentation directory.

## Usage

### Dry-run (preview changes)

```bash
fix-bare-urls asciidoc/ --dry-run
```

### Apply conversions

```bash
fix-bare-urls asciidoc/
```

### Process a single file

```bash
fix-bare-urls asciidoc/langchain4j/anthropic-chat-model.adoc
```

### Quiet mode (summary only)

```bash
fix-bare-urls asciidoc/ --quiet
```

## What it converts

Bare HTTP/HTTPS URLs followed by bracket link text:

**Before:**
```asciidoc
Visit https://www.example.com[Example] for more information.
```

**After:**
```asciidoc
Visit link:https://www.example.com[Example] for more information.
```

## What it skips

The tool preserves URLs that are already handled by an AsciiDoc macro or are inside protected contexts:

### Already-prefixed URLs

URLs preceded by `link:`, `xref:`, `image:`, `image::`, `mailto:`, or `++` are not modified:

```asciidoc
link:https://example.com[Already prefixed]     // skipped
xref:https://example.com[Cross reference]      // skipped
image::https://example.com/img.png[Alt text]   // skipped
```

### Code blocks

URLs inside code block delimiters (`----`) are not modified:

```asciidoc
[source,yaml]
----
url: https://example.com[not modified]
----
```

### Passthrough blocks

URLs inside passthrough block delimiters (`++++`) are not modified.

### Literal blocks

URLs inside literal block delimiters (`....`) are not modified.

### Inline backtick code

URLs inside backtick-delimited inline code are not modified:

```asciidoc
Use `https://example.com[text]` in your config.
```

### AsciiDoc comments

Lines starting with `//` are not modified.

## Options

| Option | Description |
|--------|-------------|
| `path` | File or directory to process (default: current directory) |
| `-n`, `--dry-run` | Show what would be converted without making changes |
| `-q`, `--quiet` | Only show summary, not individual conversions |
| `-p`, `--pattern` | File pattern for directory scans (default: `**/*.adoc`) |

## Example output

```
$ fix-bare-urls asciidoc/langchain4j/ --dry-run
DRY RUN: Would convert 45 URL(s) in 28 file(s):

  anthropic-chat-model.adoc: 3 conversion(s)
    - Line 8: 1 URL(s) converted
    - Line 14: 1 URL(s) converted
    - Line 51: 1 URL(s) converted
  azure-openai-chat-model.adoc: 2 conversion(s)
    - Line 6: 1 URL(s) converted
    - Line 12: 1 URL(s) converted
  ...

Run without --dry-run to apply these conversions.
```

## CI/CD integration

The tool is designed to run as part of an upstream sync pipeline. Place it after cross-reference processing and before one-off replacement scripts:

```bash
# Pipeline ordering
python3 scripts/replace-xrefs.py          # 1. Convert xrefs to path-based links
python3 scripts/fix-bare-urls.py asciidoc/ # 2. Convert bare URLs to link: macros
python3 scripts/simple_replacement_list.py # 3. Apply one-off edge-case fixes
```

## Source

This tool lives in the RHBQ documentation repository at `scripts/fix-bare-urls.py` rather than in the doc-utils package, because it is tightly integrated with the upstream sync CI pipeline.
