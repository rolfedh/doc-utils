---
layout: default
title: check-scannability
nav_order: 6
---

# Scannability Checker for AsciiDoc Files

> ⚠️ **IMPORTANT: Work in a Git Branch**
> 
> While this tool only reports issues and doesn't modify files, it's still recommended to:
> - Work in a feature branch when making documentation changes
> - Review all flagged issues carefully before making edits
> - Test your documentation build after making changes

This tool analyzes `.adoc` files in the current directory to flag scannability issues that can reduce readability.

## Installation

After [installing the package](../getting-started.md), run the tool from anywhere:

```sh
check-scannability [options]
```

Or, if running from source:

```sh
python3 check_scannability.py [options]
```

## What It Checks

- **Long sentences**  
  Sentences that exceed **22 words** (default; adjustable with `-s`/`--max-sentence-length`).

- **Dense paragraphs**  
  Paragraphs with more than **3 sentences** (default; adjustable with `-p`/`--max-paragraph-sentences`).

- **Line numbers**  
  The report output includes the line number where each paragraph starts, to help you quickly locate issues in your `.adoc` files.

## Usage

See the script's `--help` output or the docstring for all options. Common options include:

- `-s`, `--max-sentence-length` — Add extra words per sentence (default base: 22 words)
- `-p`, `--max-paragraph-sentences` — Add extra sentences per paragraph (default base: 3 sentences)
- `-v`, `--verbose` — Verbose mode (shows all files, even those without issues)
- `-o`, `--output` — Write results to a timestamped txt file in your home directory
- `--exclude-dir` — Directory to exclude (can be used multiple times)
- `--exclude-file` — File to exclude (can be used multiple times)
- `--exclude-list` — Path to a file containing directories or files to exclude, one per line

## Examples

Check with custom limits:
```sh
check-scannability -s 5 -p 2 -o
```
This will check for sentences longer than 27 words (22 + 5) and paragraphs longer than 5 sentences (3 + 2), and write the results to a file.

Exclude specific directories:
```sh
check-scannability --exclude-dir ./drafts --exclude-dir ./archive
```

Use an exclusion list file:
```sh
check-scannability --exclude-list .docutils-ignore
```

---

See the main [README.md](README.md) for more details on installation and usage as a package.
