"""
Archive Unused Image Files

Scans './modules' and './assemblies' for image files (e.g., .png, .jpg, .jpeg, .gif, .svg) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them.

For full documentation and usage examples, see archive_unused_files.md in this directory.
"""

import os
import argparse
from doc_utils.unused_images import find_unused_images

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive unused image files.')
    parser.add_argument('--archive', action='store_true', help='Move the files to a dated zip in the archive directory.')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Directory to exclude (can be used multiple times).')
    parser.add_argument('--exclude-file', action='append', default=[], help='File to exclude (can be used multiple times).')
    parser.add_argument('--exclude-list', type=str, help='Path to a file containing directories or files to exclude, one per line.')
    args = parser.parse_args()

    scan_dirs = ['.']
    archive_dir = './archive'

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
