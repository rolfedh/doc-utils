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

def find_unused_files(scan_dirs, archive_dir, archive=False):
    """
    Scans the specified directories for AsciiDoc files that are not included anywhere else.
    Optionally archives and deletes them.
    """
    # Collect all AsciiDoc files in the specified directories and subdirectories
    asciidoc_files = []
    for base_dir in scan_dirs:
        for root, _, files in os.walk(base_dir):
            for f in files:
                if f.endswith('.adoc'):
                    asciidoc_files.append(os.path.join(root, f))
    # Deduplicate asciidoc_files
    asciidoc_files = list(dict.fromkeys(asciidoc_files))

    # Search for include:: statements in all AsciiDoc files under the project
    include_pattern = re.compile(r'include::(.+?)\[')
    included_files = set()

    for root, dirs, files in os.walk('.'):
        # Skip symlinked directories
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
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
    args = parser.parse_args()

    # Configure which directories to scan and where to place the archive
    scan_dirs = ['./modules', './modules/rn', './assemblies']  # <-- Edit this list to change scan locations
    archive_dir = './archive'  # <-- Edit this to change the archive output directory

    find_unused_files(scan_dirs, archive_dir, args.archive)
