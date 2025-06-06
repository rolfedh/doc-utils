"""
Scannability Checker for AsciiDoc Files

This script analyzes AsciiDoc (`.adoc`) files in the current directory to detect scannability issues that affect readability.

- Flags sentences that exceed 22 words (default, adjustable with -s)
- Flags paragraphs with more than 3 sentences (default, adjustable with -p)
- Excludes code blocks (delimited by ----, ...., or [source] blocks) from analysis

When using -o, the script prints the path to the report file; it does not attempt to open the file automatically. 

For full documentation, see check_scannability.md in this directory.
"""

import os
import re
import argparse
from datetime import datetime
import sys
import subprocess

BASE_SENTENCE_WORD_LIMIT = 22
BASE_PARAGRAPH_SENTENCE_LIMIT = 3

def count_words(sentence):
    return len(sentence.split())

def split_sentences(paragraph):
    # Simple sentence splitter (handles ., !, ?)
    # Note: This may not handle abbreviations or all edge cases.
    return re.split(r'(?<=[.!?])\s+', paragraph.strip())

def remove_code_blocks(content):
    """
    Remove AsciiDoc code blocks (----, ...., and [source]... blocks) from the content.
    """
    # Remove blocks delimited by ---- or ....
    content = re.sub(r'(?ms)^----$.*?^----$', '', content)
    content = re.sub(r'(?ms)^\.\.\.\.$.*?^\.\.\.\.$', '', content)
    # Remove [source] blocks (optionally with language)
    content = re.sub(r'(?ms)^\[source.*?^----$.*?^----$', '', content)
    content = re.sub(r'(?ms)^\[source.*?^\.\.\.\.$.*?^\.\.\.\.$', '', content)
    return content

def assess_file(filepath, sentence_word_limit, paragraph_sentence_limit):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]
    # Remove code blocks before splitting into paragraphs
    content = remove_code_blocks(content)
    # Track paragraph start line numbers
    lines = content.splitlines()
    paragraph_starts = []
    paragraph_texts = []
    current_paragraph = []
    start_line = 0
    for idx, line in enumerate(lines):
        if line.strip() == '':
            if current_paragraph:
                paragraph_starts.append(start_line + 1)  # 1-based line number
                paragraph_texts.append('\n'.join(current_paragraph))
                current_paragraph = []
            start_line = idx + 1
        else:
            if not current_paragraph:
                start_line = idx
            current_paragraph.append(line)
    if current_paragraph:
        paragraph_starts.append(start_line + 1)
        paragraph_texts.append('\n'.join(current_paragraph))
    issues = []
    for i, (para, para_line) in enumerate(zip(paragraph_texts, paragraph_starts), 1):
        sentences = split_sentences(para)
        if len(sentences) > paragraph_sentence_limit:
            issues.append(f"Line {para_line}: Paragraph {i}: Too many sentences ({len(sentences)})")
        for j, sent in enumerate(sentences, 1):
            word_count = count_words(sent)
            if word_count > sentence_word_limit:
                issues.append(f"Line {para_line}: Paragraph {i}, Sentence {j}: Too long ({word_count} words)")
    return issues

def print_help():
    print(__doc__)

def main():
    # Manual check for -h or --help to display the full docstring
    if '-h' in sys.argv or '--help' in sys.argv:
        print_help()
        sys.exit(0)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-s', type=int, default=0, help='Extra words allowed per sentence')
    parser.add_argument('-p', type=int, default=0, help='Additional sentences allowed per paragraph')
    parser.add_argument('-v', action='store_true', help='Verbose output')
    parser.add_argument('-o', action='store_true', help='Output the report to a timestamped txt file')
    # Do not add -h/--help to argparse, handled manually above
    args = parser.parse_args()

    sentence_word_limit = BASE_SENTENCE_WORD_LIMIT + args.s
    paragraph_sentence_limit = BASE_PARAGRAPH_SENTENCE_LIMIT + args.p

    adoc_files = sorted(f for f in os.listdir('.') if f.endswith('.adoc'))
    report_lines = []
    for adoc in adoc_files:
        issues = assess_file(adoc, sentence_word_limit, paragraph_sentence_limit)
        if issues or args.v:
            report_lines.append("")  # Blank line above each filename
            report_lines.append(f"{adoc}:")
            if issues:
                for issue in issues:
                    report_lines.append("  " + issue)
            else:
                report_lines.append("  No scannability issues found.")

    output = "\n".join(report_lines)
    if args.o:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        home_dir = os.path.expanduser("~")
        filename = os.path.join(home_dir, f"{timestamp}.txt")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pwd = os.getcwd()
        cmd = "python3 " + " ".join([sys.argv[0]] + sys.argv[1:])
        total_sentence_limit = sentence_word_limit
        total_paragraph_limit = paragraph_sentence_limit
        s_opt = f"-s {args.s}" if args.s else "0"
        p_opt = f"-p {args.p}" if args.p else "0"
        metadata = [
            "Scannability Report",
            "",
            f"Purpose: This report lists scannability issues in .adoc files in the current directory.",
            f"Directory: {pwd}",
            f"Date and Time: {now_str}",
            f"Sentence length limit: {total_sentence_limit} words (22 plus -s {args.s})",
            f"Paragraph sentence limit: {total_paragraph_limit} sentences (3 plus -p {args.p})",
            "See scannable.py for usage instructions and examples.",
            f"Command: {cmd}",
            "",
            "------------------------------------------------------------",
            "",
        ]
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(metadata))
            f.write(output.lstrip() + "\n")
        print(f"Report written to: {filename}")
    else:
        if output:
            print(output.lstrip())

if __name__ == "__main__":
    main()
