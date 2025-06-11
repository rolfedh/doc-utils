"""
Archive Unused AsciiDoc Files

Scans './modules' and './assemblies' for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them.

For full documentation and usage examples, see archive_unused_files.md in this directory.
"""

import os
import re
import argparse
from datetime import datetime
import shutil
import zipfile

def find_unused_files(scan_dirs, archive_dir, archive=False, exclude_dirs=None, exclude_files=None):
    """
    Scans the specified directories for AsciiDoc files that are not included anywhere else.
    Optionally archives and deletes them.
    Excludes directories and files as specified.
    """
    exclude_dirs = set(os.path.normpath(d) for d in (exclude_dirs or []))
    exclude_files = set(os.path.normpath(f) for f in (exclude_files or []))

    # Collect all AsciiDoc files in the specified directories and subdirectories, ignoring symlinks and excluded dirs/files
    asciidoc_files = []
    for base_dir in scan_dirs:
        for root, dirs, files in os.walk(base_dir):
            # Skip symlinked and excluded directories
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d)) and os.path.normpath(os.path.join(root, d)) not in exclude_dirs]
            for f in files:
                file_path = os.path.normpath(os.path.join(root, f))
                if os.path.islink(file_path):
                    continue
                if any(file_path == ex or file_path.endswith(os.sep + ex) for ex in exclude_files):
                    continue
                if f.endswith('.adoc'):
                    asciidoc_files.append(file_path)
    asciidoc_files = list(dict.fromkeys(asciidoc_files))

    # Search for include:: statements in all AsciiDoc files under the project, ignoring symlinks and excluded dirs/files
    include_pattern = re.compile(r'include::(.+?)\[')
    included_files = set()
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d)) and os.path.normpath(os.path.join(root, d)) not in exclude_dirs]
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))
            if os.path.islink(file_path):
                continue
            if any(file_path == ex or file_path.endswith(os.sep + ex) for ex in exclude_files):
                continue
            if file.endswith('.adoc'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        includes = include_pattern.findall(content)
                        included_files.update(os.path.basename(include) for include in includes)
                except Exception as e:
                    print(f"Warning: could not read {file_path}: {e}")

    # Identify files that are not included in any other files
    unused_files = [f for f in asciidoc_files if os.path.basename(f) not in included_files]
    # Deduplicate unused_files
    unused_files = list(dict.fromkeys(unused_files))

    # If no unused files, skip manifest and archive creation
    if not unused_files:
        print("No unused files found. No manifest or ZIP archive created.")
        return

    # Output to console and write to manifest file
    now = datetime.now()
    datetime_str = now.strftime('%Y-%m-%d_%H%M%S')
    output_file = f'to-archive-{datetime_str}.txt'  # Use date and time for manifest

    # Ensure the archive directory exists before writing the manifest
    os.makedirs(archive_dir, exist_ok=True)
    manifest_path = os.path.join(archive_dir, output_file)
    with open(manifest_path, 'w') as f:
        for file in unused_files:
            print(file)
            f.write(file + '\n')

    # Archive if requested
    if archive:
        zip_path = os.path.join(archive_dir, f"to-archive-{datetime_str}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add unused files to the zip and remove them
            for file in unused_files:
                arcname = os.path.relpath(file)
                print(f"Archiving: {file} -> {zip_path} ({arcname})")
                zipf.write(file, arcname)
                os.remove(file)
        # Do NOT move or delete the manifest file; it stays in the archive directory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive unused AsciiDoc files.')
    parser.add_argument('--archive', action='store_true', help='Move the files to a dated zip in the archive directory.')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Directory to exclude (can be used multiple times).')
    parser.add_argument('--exclude-file', action='append', default=[], help='File to exclude (can be used multiple times).')
    parser.add_argument('--exclude-list', type=str, help='Path to a file containing directories or files to exclude, one per line.')
    args = parser.parse_args()

    scan_dirs = ['./modules', './modules/rn', './assemblies']
    archive_dir = './archive'

    # Gather exclusions from file if provided
    exclude_dirs = list(args.exclude_dir)
    exclude_files = list(args.exclude_file)
    if args.exclude_list:
        with open(args.exclude_list, 'r', encoding='utf-8') as excl:
            for line in excl:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if os.path.isdir(line):
                    exclude_dirs.append(line)
                else:
                    exclude_files.append(line)

    find_unused_files(scan_dirs, archive_dir, args.archive, exclude_dirs, exclude_files)
