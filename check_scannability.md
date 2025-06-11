# Scannability Checker for AsciiDoc Files

This tool analyzes `.adoc` files in the current directory to flag scannability issues that can reduce readability.

## Installation

After installing the package from PyPI:

```sh
pip install rolfedh-doc-utils
```

You can run the tool from anywhere using:

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

- `-s`, `--max-sentence-length` — Add extra words per sentence
- `-p`, `--max-paragraph-sentences` — Add extra sentences per paragraph
- `-v`, `--verbose` — Verbose mode (shows all files, even those without issues)
- `-o`, `--output` — Write results to a timestamped txt file in your home directory

## Example

```sh
check-scannability -s 5 -p 2 -o
```

This will check for sentences longer than 27 words and paragraphs longer than 5 sentences, and write the results to a file.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
