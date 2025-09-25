#!/usr/bin/env python3
"""
replace-link-attributes - Replace AsciiDoc attributes within link URLs with their actual values.

This script finds and replaces attribute references (like {attribute-name}) that appear
in the URL portion of AsciiDoc link macros (link: and xref:) with their resolved values
from attributes.adoc. Link text is preserved unchanged.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from doc_utils.replace_link_attributes import (
    find_attributes_files,
    load_attributes,
    resolve_nested_attributes,
    replace_link_attributes_in_file,
    find_adoc_files
)


def prompt_for_attributes_file(attributes_files: list[Path]) -> Optional[Path]:
    """Prompt user to select or specify attributes file."""
    if not attributes_files:
        print("No attributes.adoc files found in the repository.")
        response = input("Enter the path to your attributes.adoc file (or 'q' to quit): ").strip()
        if response.lower() == 'q':
            return None
        path = Path(response)
        if path.exists() and path.is_file():
            return path
        else:
            print(f"Error: File not found: {response}")
            return None

    if len(attributes_files) == 1:
        file_path = attributes_files[0]
        response = input(f"Found attributes file: {file_path}\nUse this file? (y/n/q): ").strip().lower()
        if response == 'y':
            return file_path
        elif response == 'q':
            return None
        else:
            response = input("Enter the path to your attributes.adoc file (or 'q' to quit): ").strip()
            if response.lower() == 'q':
                return None
            path = Path(response)
            if path.exists() and path.is_file():
                return path
            else:
                print(f"Error: File not found: {response}")
                return None

    # Multiple files found
    print("\nFound multiple attributes.adoc files:")
    for i, file_path in enumerate(attributes_files, 1):
        print(f"  {i}. {file_path}")
    print(f"  {len(attributes_files) + 1}. Enter custom path")

    while True:
        response = input(f"\nSelect option (1-{len(attributes_files) + 1}) or 'q' to quit: ").strip()
        if response.lower() == 'q':
            return None

        try:
            choice = int(response)
            if 1 <= choice <= len(attributes_files):
                return attributes_files[choice - 1]
            elif choice == len(attributes_files) + 1:
                response = input("Enter the path to your attributes.adoc file: ").strip()
                path = Path(response)
                if path.exists() and path.is_file():
                    return path
                else:
                    print(f"Error: File not found: {response}")
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(attributes_files) + 1}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    parser = argparse.ArgumentParser(
        description='Replace AsciiDoc attributes within link macros with their actual values.'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be changed without making actual modifications'
    )
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='.',
        help='Repository path to search (default: current directory)'
    )
    parser.add_argument(
        '--attributes-file', '-a',
        type=str,
        help='Path to attributes.adoc file (skips interactive selection)'
    )

    args = parser.parse_args()

    # Determine repository root
    repo_root = Path(args.path).resolve()

    if not repo_root.exists() or not repo_root.is_dir():
        print(f"Error: Directory not found: {repo_root}")
        sys.exit(1)

    print(f"{'DRY RUN MODE - ' if args.dry_run else ''}Searching in: {repo_root}")

    # Find or get attributes file
    if args.attributes_file:
        attributes_file = Path(args.attributes_file)
        if not attributes_file.exists():
            print(f"Error: Specified attributes file not found: {attributes_file}")
            sys.exit(1)
    else:
        print("\nSearching for attributes.adoc files...")
        attributes_files = find_attributes_files(repo_root)
        attributes_file = prompt_for_attributes_file(attributes_files)

        if not attributes_file:
            print("Operation cancelled.")
            sys.exit(0)

    print(f"\nLoading attributes from: {attributes_file}")
    attributes = load_attributes(attributes_file)

    if not attributes:
        print("No attributes found in the file.")
        sys.exit(1)

    print(f"Found {len(attributes)} attributes")

    # Resolve nested references
    print("Resolving nested attribute references...")
    attributes = resolve_nested_attributes(attributes)

    # Find all AsciiDoc files
    print(f"\nSearching for *.adoc files in {repo_root}")
    adoc_files = find_adoc_files(repo_root)

    # Exclude the attributes file itself
    adoc_files = [f for f in adoc_files if f != attributes_file]

    print(f"Found {len(adoc_files)} AsciiDoc files to process")

    if args.dry_run:
        print("\n*** DRY RUN MODE - No files will be modified ***\n")

    # Process each file
    total_replacements = 0
    files_modified = 0

    for file_path in adoc_files:
        replacements = replace_link_attributes_in_file(file_path, attributes, args.dry_run)
        if replacements > 0:
            rel_path = file_path.relative_to(repo_root)
            prefix = "[DRY RUN] " if args.dry_run else ""
            print(f"  {prefix}Modified {rel_path}: {replacements} replacements")
            total_replacements += replacements
            files_modified += 1

    # Summary
    print(f"\nSummary:")
    if args.dry_run:
        print(f"  Would modify {files_modified} files")
        print(f"  Would make {total_replacements} replacements")
        print("\nRun without --dry-run to apply changes.")
    else:
        print(f"  Total files modified: {files_modified}")
        print(f"  Total replacements: {total_replacements}")

        if total_replacements == 0:
            print("\nNo attribute references found within link macros.")
        else:
            print("\nReplacement complete!")


if __name__ == '__main__':
    main()