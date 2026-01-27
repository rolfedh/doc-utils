#!/usr/bin/env python3
"""
Insert .Procedure block title above numbered steps in AsciiDoc procedure files.

This script finds AsciiDoc procedure files (those with :_mod-docs-content-type: PROCEDURE)
and inserts a .Procedure block title before the first numbered step if one is missing.

Usage:
    insert-procedure-title <file_or_directory> [options]

Examples:
    insert-procedure-title modules/proc_example.adoc
    insert-procedure-title modules/ --dry-run
    insert-procedure-title . --verbose
"""

import argparse
import os
import re
import sys
from pathlib import Path


def is_procedure_file(content: str) -> bool:
    """Check if file is a PROCEDURE content type."""
    return ':_mod-docs-content-type: PROCEDURE' in content


def find_first_numbered_step(lines: list[str]) -> int | None:
    """
    Find the line index of the first numbered step.

    Numbered steps can be:
    - `. Step text` (AsciiDoc implicit ordered list)
    - `1. Step text` (explicit numbered list)

    Returns None if no numbered steps found.
    """
    # Pattern for ordered list items:
    # - Starts with `. ` (implicit) or `<digit>. ` (explicit)
    # - Must not be a block title (block titles are `.Title` without space after dot)
    ordered_list_pattern = re.compile(r'^(\d+\.\s|\.(?!\w)\s)')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if ordered_list_pattern.match(stripped):
            return i
    return None


def has_procedure_title_before(lines: list[str], step_index: int) -> bool:
    """
    Check if there's a .Procedure block title before the numbered steps.

    Looks backward from the step index to find `.Procedure` on its own line.
    Continues past other block titles (like sub-section titles) until hitting
    a section heading (= or ==) or the start of the file.
    """
    for i in range(step_index - 1, -1, -1):
        stripped = lines[i].strip()
        if stripped == '.Procedure':
            return True
        # Stop searching if we hit a section heading
        if stripped.startswith('= ') or stripped.startswith('== '):
            return False
    return False


def find_insertion_point(lines: list[str], step_index: int) -> int:
    """
    Find the correct line index to insert .Procedure block title.

    The insertion point should be before the numbered steps, but after:
    - Prerequisites block
    - Introductory paragraphs
    - Blank lines

    Returns the line index where .Procedure should be inserted.
    """
    # Look backward from the step to find a good insertion point
    # We want to insert just before the numbered list starts
    insertion_point = step_index

    # Skip backward over any preceding blank lines to insert before them
    while insertion_point > 0 and lines[insertion_point - 1].strip() == '':
        insertion_point -= 1

    return insertion_point


def insert_procedure_title(content: str) -> tuple[str, bool]:
    """
    Insert .Procedure block title if missing.

    Returns:
        tuple: (modified_content, was_modified)
    """
    lines = content.split('\n')

    # Find the first numbered step
    step_index = find_first_numbered_step(lines)
    if step_index is None:
        return content, False

    # Check if .Procedure already exists before the steps
    if has_procedure_title_before(lines, step_index):
        return content, False

    # Find where to insert
    insertion_point = find_insertion_point(lines, step_index)

    # Insert .Procedure followed by blank line
    # If there's already a blank line before steps, just insert .Procedure
    if insertion_point < len(lines) and lines[insertion_point].strip() == '':
        lines.insert(insertion_point, '.Procedure')
        lines.insert(insertion_point + 1, '')
    else:
        lines.insert(insertion_point, '')
        lines.insert(insertion_point, '.Procedure')

    return '\n'.join(lines), True


def has_numbered_steps(content: str) -> bool:
    """Check if file has numbered steps."""
    lines = content.split('\n')
    return find_first_numbered_step(lines) is not None


def has_procedure_title(content: str) -> bool:
    """Check if file has a .Procedure block title."""
    for line in content.split('\n'):
        if line.strip() == '.Procedure':
            return True
    return False


def process_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> tuple[bool, bool]:
    """
    Process a single AsciiDoc file.

    Returns tuple: (was_modified, has_warning)
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return False, False

    # Only process PROCEDURE files
    if not is_procedure_file(content):
        if verbose:
            print(f"Skipping (not a procedure file): {filepath}")
        return False, False

    # If file already has .Procedure, no action needed
    # (handles cases where procedures use unordered lists instead of numbered steps)
    if has_procedure_title(content):
        if verbose:
            print(f"No changes needed (has .Procedure): {filepath}")
        return False, False

    # Check if file has numbered steps
    if not has_numbered_steps(content):
        print(f"Warning: Procedure file has no numbered steps and no .Procedure title: {filepath}")
        return False, True

    new_content, was_modified = insert_procedure_title(content)

    if was_modified:
        if dry_run:
            print(f"Would modify: {filepath}")
        else:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"Modified: {filepath}")
        return True, False
    else:
        if verbose:
            print(f"No changes needed: {filepath}")
        return False, False


def collect_adoc_files(path: Path) -> list[Path]:
    """Collect all .adoc files from path (file or directory)."""
    if path.is_file():
        if path.suffix == '.adoc':
            return [path]
        return []

    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.adoc'):
                files.append(Path(root) / filename)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description='Insert .Procedure block title above numbered steps in AsciiDoc procedure files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s modules/proc_example.adoc
  %(prog)s modules/ --dry-run
  %(prog)s . --verbose
        '''
    )
    parser.add_argument(
        'path',
        type=Path,
        help='File or directory to process'
    )
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show all files processed, including those not modified'
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)

    files = collect_adoc_files(args.path)

    if not files:
        print(f"No .adoc files found in: {args.path}")
        sys.exit(0)

    modified_count = 0
    warning_count = 0
    for filepath in files:
        was_modified, has_warning = process_file(filepath, dry_run=args.dry_run, verbose=args.verbose)
        if was_modified:
            modified_count += 1
        if has_warning:
            warning_count += 1

    print()
    if args.dry_run:
        print(f"Dry run complete. {modified_count} file(s) would be modified.")
    else:
        print(f"Complete. {modified_count} file(s) modified.")

    if warning_count > 0:
        print(f"Warnings: {warning_count} procedure file(s) have no numbered steps.")


if __name__ == '__main__':
    main()
