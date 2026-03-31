---
layout: default
title: obsidian-to-pandoc
parent: Tools Reference
nav_order: 24
---

# obsidian-to-pandoc

Converts Obsidian wiki-links to pandoc-compatible markdown links so that internal heading references work in pandoc-generated PDFs and HTML.

## Overview

Obsidian uses a wiki-link syntax (`[[#Heading]]`) for internal heading links that pandoc does not recognize. This tool pre-processes an Obsidian markdown file, converting wiki-links to standard markdown anchor links (`[Heading](#heading)`) using pandoc's heading ID slugification algorithm.

## Usage

### Pipe directly into pandoc

```bash
python3 obsidian_to_pandoc.py input.md | pandoc -o output.pdf
```

### Write converted output to a file

```bash
python3 obsidian_to_pandoc.py input.md -o converted.md
```

### Read from stdin

```bash
cat input.md | python3 obsidian_to_pandoc.py
```

## What it converts

| Obsidian syntax | Converted output |
|-----------------|------------------|
| `[[#Heading Text\|display text]]` | `[display text](#heading-text)` |
| `[[#Heading Text]]` | `[Heading Text](#heading-text)` |

### Example

**Before:**
```markdown
See [[#Configuration Options|the config section]] for details.

Refer to [[#Getting Started]] for setup instructions.
```

**After:**
```markdown
See [the config section](#configuration-options) for details.

Refer to [Getting Started](#getting-started) for setup instructions.
```

## Slugification algorithm

The heading-to-anchor conversion follows pandoc's heading ID algorithm (documented in the pandoc manual under "Heading identifiers"):

1. Remove all non-alphanumeric characters except underscores, hyphens, and periods
2. Replace spaces and newlines with hyphens
3. Convert to lowercase
4. Remove leading non-letter characters

## Options

| Option | Description |
|--------|-------------|
| `infile` | Input markdown file (default: stdin) |
| `-o`, `--output` | Output file (default: stdout) |

## Source

`doc_utils/obsidian_to_pandoc.py`
