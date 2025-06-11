# Scannability Checker for AsciiDoc Files

This Python script analyzes `.adoc` files in the current directory to flag scannability issues that can reduce readability.

## What It Checks

- **Long sentences**  
  Sentences that exceed **22 words** (default; adjustable with `-s`/`--max-sentence-length`).

- **Dense paragraphs**  
  Paragraphs with more than **3 sentences** (default; adjustable with `-p`/`--max-paragraph-sentences`).

- **Line numbers**  
  The report output includes the line number where each paragraph starts, to help you quickly locate issues in your `.adoc` files.

## Customization

Use command-line options to adjust the default thresholds:

- `-s`, `--max-sentence-length` `<extra_words>` — Add extra words per sentence  
  _Example: `-s 5` or `--max-sentence-length 5` raises the limit to 27 words (22 + 5)_

- `-p`, `--max-paragraph-sentences` `<extra_sentences>` — Add extra sentences per paragraph  
  _Example: `-p 2` or `--max-paragraph-sentences 2` raises the limit to 5 sentences (3 + 2)_

## Output Options

- Print results directly to the terminal (default)
- Use `-o` to save a timestamped `.txt` report in your home directory  
  _Example: `~/20250605144341.txt`_
- Use `-v` for verbose mode (shows all files, even those without issues)

> **Note:** The script prints the path to the report file. It does not attempt to open the file automatically.

## Use Case

Ideal for **technical writers and editors** who want to review `.adoc` files for scannability before publishing.

## Usage

```bash
python3 ~/doc-utils/check_scannability.py [-s <extra_words>] [-p <extra_sentences>] [-v|--verbose] [-o|--output]
```

If your script is not in `~/doc-utils/`, replace the path above with the actual location of your check_scannability.py file.

### Options

| Option                                 | Description                                                             |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `-s <int>`, `--max-sentence-length <int>` | Extra words allowed per sentence (default: 0; base: 22)                  |
| `-p <int>`, `--max-paragraph-sentences <int>` | Extra sentences allowed per paragraph (default: 0; base: 3)             |
| `-v`, `--verbose`                      | Verbose mode — shows results for all files, even if no issues are found |
| `-o`, `--output`                       | Output results to a timestamped file in your home directory             |
| `-h`, `--help`                         | Show usage and exit                                                     |

## Examples

```bash
python3 ~/doc-utils/check_scannability.py
python3 ~/doc-utils/check_scannability.py -s 5
python3 ~/doc-utils/check_scannability.py --max-sentence-length 5
python3 ~/doc-utils/check_scannability.py -p 2
python3 ~/doc-utils/check_scannability.py --max-paragraph-sentences 2
python3 ~/doc-utils/check_scannability.py -s 3 -p 1
python3 ~/doc-utils/check_scannability.py -v
python3 ~/doc-utils/check_scannability.py --verbose
python3 ~/doc-utils/check_scannability.py -o
python3 ~/doc-utils/check_scannability.py --output
```

## Notes

* Only `.adoc` files in the **current working directory** are scanned.
* Sentence splitting uses a simple regex and may not handle edge cases (e.g., abbreviations).
* When using `-o`, the path to the report file is printed after generation.
* Code blocks (delimited by `----`, `....`, or `[source]` blocks) are excluded from analysis.
* The report output includes the line number where each paragraph starts.
