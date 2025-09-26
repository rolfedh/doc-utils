"""
Module for finding unused AsciiDoc attributes.

Functions:
- parse_attributes_file: Parse attribute names from an attributes.adoc file.
- find_adoc_files: Recursively find all .adoc files in a directory (ignoring symlinks).
- scan_for_attribute_usage: Find which attributes are used in a set of .adoc files.
- find_unused_attributes: Main function to return unused attributes.
- find_attributes_files: Find all potential attributes files in the repository.
"""

import os
import re
from pathlib import Path
from typing import Set, List, Optional

def parse_attributes_file(attr_file: str) -> Set[str]:
    attributes = set()

    # Check if file exists
    if not os.path.exists(attr_file):
        raise FileNotFoundError(f"Attributes file not found: {attr_file}")

    # Check if it's a file (not a directory)
    if not os.path.isfile(attr_file):
        raise ValueError(f"Path is not a file: {attr_file}")

    try:
        with open(attr_file, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^:([\w-]+):', line.strip())
                if match:
                    attributes.add(match.group(1))
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {attr_file}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Unable to read file (encoding issue): {attr_file}\n{str(e)}")

    return attributes

def find_adoc_files(root_dir: str) -> List[str]:
    adoc_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=False):
        for fname in filenames:
            if fname.endswith('.adoc'):
                full_path = os.path.join(dirpath, fname)
                if not os.path.islink(full_path):
                    adoc_files.append(full_path)
    return adoc_files

def scan_for_attribute_usage(adoc_files: List[str], attributes: Set[str]) -> Set[str]:
    used = set()
    attr_pattern = re.compile(r'\{([\w-]+)\}')
    for file in adoc_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                for match in attr_pattern.findall(line):
                    if match in attributes:
                        used.add(match)
    return used

def find_attributes_files(root_dir: str = '.') -> List[str]:
    """Find all attributes.adoc files in the repository."""
    attributes_files = []
    root_path = Path(root_dir)

    # Common attribute file patterns
    patterns = ['**/attributes.adoc', '**/attributes*.adoc', '**/*attributes.adoc', '**/*-attributes.adoc']

    for pattern in patterns:
        for path in root_path.glob(pattern):
            # Skip hidden directories and common build directories
            parts = path.parts
            if any(part.startswith('.') or part in ['target', 'build', 'node_modules', '.archive'] for part in parts):
                continue
            # Convert to string and avoid duplicates
            str_path = str(path)
            if str_path not in attributes_files:
                attributes_files.append(str_path)

    # Sort for consistent ordering
    attributes_files.sort()
    return attributes_files


def select_attributes_file(attributes_files: List[str]) -> Optional[str]:
    """Interactive selection of attributes file from a list."""
    if not attributes_files:
        return None

    if len(attributes_files) == 1:
        print(f"Found attributes file: {attributes_files[0]}")
        response = input("Use this file? (y/n): ").strip().lower()
        if response == 'y':
            return attributes_files[0]
        else:
            response = input("Enter the path to your attributes file: ").strip()
            if os.path.exists(response) and os.path.isfile(response):
                return response
            else:
                print(f"Error: File not found: {response}")
                return None

    # Multiple files found
    print("\nFound multiple attributes files:")
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
                response = input("Enter the path to your attributes file: ").strip()
                if os.path.exists(response) and os.path.isfile(response):
                    return response
                else:
                    print(f"Error: File not found: {response}")
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(attributes_files) + 1}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return None


def find_unused_attributes(attr_file: str, adoc_root: str = '.') -> List[str]:
    attributes = parse_attributes_file(attr_file)
    adoc_files = find_adoc_files(adoc_root)
    used = scan_for_attribute_usage(adoc_files, attributes)
    unused = sorted(attributes - used)
    return unused
