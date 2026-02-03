#!/usr/bin/env python3
"""
convert-id-attributes-to-ids - Convert :id: attribute definitions to AsciiDoc [id="..."] anchors.

This script recursively scans a directory for AsciiDoc files and replaces instances of
`:id: <id_value>` with `[id="<id_value>_{context}"]`.

Optionally, with --clean-up, it also removes related boilerplate lines:
- // define ID as an attribute
- // assign ID conditionally, followed by header
- include::{modules}/common/id.adoc[]
"""

import argparse
import os
import re
import sys
from pathlib import Path

from doc_utils.version_check import check_version_on_startup
from doc_utils.version import __version__
from doc_utils.spinner import Spinner


def find_adoc_files(directory: Path) -> list[Path]:
    """Recursively find all .adoc files in a directory."""
    adoc_files = []
    for root, dirs, files in os.walk(directory, followlinks=False):
        # Skip hidden directories and common non-content directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__')]
        for file in files:
            if file.endswith('.adoc'):
                adoc_files.append(Path(root) / file)
    return adoc_files


def convert_id_attributes(content: str, clean_up: bool = False) -> tuple[str, int, int]:
    """
    Convert :id: attributes to [id="..._{context}"] format.

    Args:
        content: The file content to process
        clean_up: If True, also remove boilerplate lines

    Returns:
        Tuple of (modified_content, id_replacements_count, cleanup_removals_count)
    """
    lines = content.split('\n')
    new_lines = []
    id_replacements = 0
    cleanup_removals = 0

    # Patterns for clean-up (flexible matching for variations)
    cleanup_patterns = [
        re.compile(r'^\s*//\s*define ID as an attribute', re.IGNORECASE),
        re.compile(r'^\s*//\s*assign.*ID conditionally', re.IGNORECASE),
        re.compile(r'^\s*include::\{modules\}/common/id\.adoc\[\]'),
    ]

    # Pattern to match :id: <value>
    id_pattern = re.compile(r'^:id:\s*(.+?)\s*$')

    for line in lines:
        # Check if this is an :id: line
        id_match = id_pattern.match(line)
        if id_match:
            id_value = id_match.group(1)
            new_line = f'[id="{id_value}_{{context}}"]'
            new_lines.append(new_line)
            id_replacements += 1
            continue

        # Check if clean-up is enabled and line matches cleanup patterns
        if clean_up:
            should_remove = False
            for pattern in cleanup_patterns:
                if pattern.search(line):
                    should_remove = True
                    cleanup_removals += 1
                    break
            if should_remove:
                continue

        new_lines.append(line)

    return '\n'.join(new_lines), id_replacements, cleanup_removals


def process_file(file_path: Path, dry_run: bool = False, clean_up: bool = False) -> tuple[int, int]:
    """
    Process a single AsciiDoc file.

    Returns:
        Tuple of (id_replacements, cleanup_removals)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Error reading {file_path}: {e}")
        return 0, 0

    new_content, id_replacements, cleanup_removals = convert_id_attributes(content, clean_up)

    if id_replacements > 0 or cleanup_removals > 0:
        if not dry_run:
            try:
                file_path.write_text(new_content, encoding='utf-8')
            except Exception as e:
                print(f"  Error writing {file_path}: {e}")
                return 0, 0

    return id_replacements, cleanup_removals


def main():
    # Check for updates (non-blocking)
    check_version_on_startup()

    parser = argparse.ArgumentParser(
        description='Convert :id: attribute definitions to AsciiDoc [id="..._{context}"] anchors.'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan for .adoc files (default: current directory)'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be changed without making actual modifications'
    )
    parser.add_argument(
        '--clean-up',
        action='store_true',
        help='Also remove ID-related boilerplate lines (comments and include directives)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for each file processed'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    # Resolve directory path
    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)

    mode_str = "DRY RUN MODE - " if args.dry_run else ""
    print(f"{mode_str}Scanning directory: {directory}")

    if args.clean_up:
        print("Clean-up mode enabled: will remove ID-related boilerplate lines")

    # Find all AsciiDoc files
    spinner = Spinner("Searching for .adoc files")
    spinner.start()
    adoc_files = find_adoc_files(directory)
    spinner.stop(f"Found {len(adoc_files)} .adoc files")

    if not adoc_files:
        print("No AsciiDoc files found.")
        sys.exit(0)

    if args.dry_run:
        print("\n*** DRY RUN MODE - No files will be modified ***\n")

    # Process each file
    total_id_replacements = 0
    total_cleanup_removals = 0
    files_modified = 0

    spinner = Spinner(f"Processing {len(adoc_files)} files")
    spinner.start()

    for file_path in adoc_files:
        id_replacements, cleanup_removals = process_file(file_path, args.dry_run, args.clean_up)

        if id_replacements > 0 or cleanup_removals > 0:
            files_modified += 1
            total_id_replacements += id_replacements
            total_cleanup_removals += cleanup_removals

            if args.verbose:
                rel_path = file_path.relative_to(directory)
                changes = []
                if id_replacements > 0:
                    changes.append(f"{id_replacements} ID conversion(s)")
                if cleanup_removals > 0:
                    changes.append(f"{cleanup_removals} line(s) removed")
                print(f"  {rel_path}: {', '.join(changes)}")

    spinner.stop(f"Processed {len(adoc_files)} files")

    # Summary
    print(f"\nSummary:")
    if args.dry_run:
        print(f"  Files that would be modified: {files_modified}")
        print(f"  :id: attributes that would be converted: {total_id_replacements}")
        if args.clean_up:
            print(f"  Boilerplate lines that would be removed: {total_cleanup_removals}")
        print("\nRun without --dry-run to apply changes.")
    else:
        print(f"  Files modified: {files_modified}")
        print(f"  :id: attributes converted: {total_id_replacements}")
        if args.clean_up:
            print(f"  Boilerplate lines removed: {total_cleanup_removals}")

        if total_id_replacements == 0:
            print("\nNo :id: attributes found to convert.")
        else:
            print("\nConversion complete!")


if __name__ == '__main__':
    main()
