"""
Archive Unused Image Files

Scans './modules' and './assemblies' for image files (e.g., .png, .jpg, .jpeg, .gif, .svg) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them.

For full documentation and usage examples, see archive_unused_files.md in this directory.
"""

import os
import re
import argparse
from datetime import datetime
import zipfile

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}


def find_unused_images(scan_dirs, archive_dir, archive=False, exclude_dirs=None, exclude_files=None):
    """
    Scans the specified directories for image files that are not referenced in any AsciiDoc file.
    Optionally archives and deletes them.
    Excludes directories and files as specified.
    """
    exclude_dirs = set(os.path.normpath(d) for d in (exclude_dirs or []))
    exclude_files = set(os.path.normpath(f) for f in (exclude_files or []))

    # Collect all image files in the specified directories and subdirectories, ignoring symlinks and excluded dirs/files
    image_files = []
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
                ext = os.path.splitext(f)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    image_files.append(file_path)
    image_files = list(dict.fromkeys(image_files))

    # Collect all AsciiDoc files in the project, ignoring symlinks and excluded dirs/files
    adoc_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d)) and os.path.normpath(os.path.join(root, d)) not in exclude_dirs]
        for f in files:
            file_path = os.path.normpath(os.path.join(root, f))
            if os.path.islink(file_path):
                continue
            if any(file_path == ex or file_path.endswith(os.sep + ex) for ex in exclude_files):
                continue
            if f.endswith('.adoc'):
                adoc_files.append(file_path)

    # Search for image references in all AsciiDoc files
    referenced_images = set()
    image_ref_pattern = re.compile(r'(?i)image::([^\[]+)\[|image:([^\[]+)\[|"([^"\s]+\.(?:png|jpg|jpeg|gif|svg))"')
    for adoc_file in adoc_files:
        try:
            with open(adoc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in image_ref_pattern.findall(content):
                    for group in match:
                        if group:
                            referenced_images.add(os.path.basename(group))
        except Exception as e:
            print(f"Warning: could not read {adoc_file}: {e}")

    # Identify image files that are not referenced
    unused_images = [f for f in image_files if os.path.basename(f) not in referenced_images]
    unused_images = list(dict.fromkeys(unused_images))

    if not unused_images:
        print("No unused image files found. No manifest or ZIP archive created.")
        return

    now = datetime.now()
    datetime_str = now.strftime('%Y-%m-%d_%H%M%S')
    output_file = f'unused-images-{datetime_str}.txt'
    os.makedirs(archive_dir, exist_ok=True)
    manifest_path = os.path.join(archive_dir, output_file)
    with open(manifest_path, 'w') as f:
        for file in unused_images:
            print(file)
            f.write(file + '\n')

    if archive:
        zip_path = os.path.join(archive_dir, f"unused-images-{datetime_str}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in unused_images:
                arcname = os.path.relpath(file)
                print(f"Archiving: {file} -> {zip_path} ({arcname})")
                zipf.write(file, arcname)
                os.remove(file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive unused image files.')
    parser.add_argument('--archive', action='store_true', help='Move the files to a dated zip in the archive directory.')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Directory to exclude (can be used multiple times).')
    parser.add_argument('--exclude-file', action='append', default=[], help='File to exclude (can be used multiple times).')
    parser.add_argument('--exclude-list', type=str, help='Path to a file containing directories or files to exclude, one per line.')
    args = parser.parse_args()

    # Scan all directories from the project root
    scan_dirs = ['.']
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

    find_unused_images(scan_dirs, archive_dir, args.archive, exclude_dirs, exclude_files)
