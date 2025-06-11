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


def find_unused_images(scan_dirs, archive_dir, archive=False):
    """
    Scans the specified directories for image files that are not referenced in any AsciiDoc file.
    Optionally archives and deletes them.
    """
    # Collect all image files in the specified directories and subdirectories, ignoring symlinks
    image_files = []
    for base_dir in scan_dirs:
        for root, dirs, files in os.walk(base_dir):
            # Skip symlinked directories
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
            for f in files:
                file_path = os.path.join(root, f)
                if os.path.islink(file_path):
                    continue
                ext = os.path.splitext(f)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    image_files.append(file_path)
    image_files = list(dict.fromkeys(image_files))

    # Collect all AsciiDoc files in the project, ignoring symlinks
    adoc_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.islink(file_path):
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
    args = parser.parse_args()

    # Scan all directories from the project root
    scan_dirs = ['.']  # <-- Scan all directories
    archive_dir = './archive'  # <-- Edit this to change the archive output directory

    find_unused_images(scan_dirs, archive_dir, args.archive)
