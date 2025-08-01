# doc-utils

A set of Python utilities and CLI tools to help technical writers maintain AsciiDoc documentation repositories.

## Resources

- [PyPI: rolfedh-doc-utils](https://pypi.org/project/rolfedh-doc-utils/)
- [GitHub repository](https://github.com/rolfedh/doc-utils)

## Installation

### From PyPI

Install the package from PyPI:

```sh
pip install rolfedh-doc-utils
````

### For Development

If you're developing or testing locally, install the package in editable mode:

```sh
# Clone the repository
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils

# Install in editable mode
pip install -e .
```

The following CLI tools are installed:

* `check-scannability`
* `archive-unused-files`
* `archive-unused-images`
* `find-unused-attributes`

These tools can be run from any directory.

### Add to PATH (if needed)

By default, CLI tools install to:

```sh
$HOME/.local/bin
```

If this directory isn’t in your `PATH`, commands may not run. Append it to your shell configuration:

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # or ~/.zshrc
```

Then reload your shell:

```sh
source ~/.bashrc   # or ~/.zshrc
```

## CLI Tools Overview

### `check_scannability.py`

Scans `.adoc` files in the current directory to report:

* Sentences that exceed a length limit
* Paragraphs with too many sentences

➡️ See [`check_scannability.md`](https://github.com/rolfedh/doc-utils/blob/main/check_scannability.md) for details.

---

### `archive_unused_files.py`

Scans the `./modules` and `./assemblies` directories for `.adoc` files that are not referenced. Optionally archives and deletes them.

➡️ See [`archive_unused_files.md`](https://github.com/rolfedh/doc-utils/blob/main/archive_unused_files.md).

---

### `archive_unused_images.py`

Finds unused image files (e.g., `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) and optionally archives and deletes them.

➡️ See [`archive_unused_images.md`](https://github.com/rolfedh/doc-utils/blob/main/archive_unused_images.md).

---

### `find_unused_attributes.py`

Scans an attributes file (e.g., `attributes.adoc`) for unused attribute definitions across all `.adoc` files.

➡️ See [`find_unused_attributes.md`](https://github.com/rolfedh/doc-utils/blob/main/find_unused_attributes.md).

## Usage

To run the tools after installation:

```sh
check-scannability --help
archive-unused-files --help
find-unused-attributes attributes.adoc
```

Or run them directly from source:

```sh
python3 check_scannability.py
python3 archive_unused_files.py
python3 find_unused_attributes.py attributes.adoc
```

### Directory/File Exclusion

Most tools support excluding specific directories and files from scanning. You can use these options:

1. **`--exclude-dir`** - Exclude specific directories (can be used multiple times):
   ```sh
   archive-unused-files --exclude-dir ./modules/temp --exclude-dir ./modules/old
   ```

2. **`--exclude-file`** - Exclude specific files (can be used multiple times):
   ```sh
   check-scannability --exclude-file ./README.adoc --exclude-file ./test.adoc
   ```

3. **`--exclude-list`** - Point to a text file containing exclusions:
   ```sh
   archive-unused-images --exclude-list .docutils-ignore
   ```
   
   The exclusion file format:
   ```
   # Comments are supported
   ./modules/deprecated/
   ./assemblies/archive/
   ./images/temp/
   specific-file.adoc
   ```

**Note:** When you exclude a parent directory, all its subdirectories are automatically excluded. Symbolic links are never followed during scanning.

## Troubleshooting

### ModuleNotFoundError

If you see an error like `ModuleNotFoundError: No module named 'find_unused_attributes'`, this typically means:

1. The package isn't installed. Run:
   ```sh
   pip install rolfedh-doc-utils
   ```

2. You're trying to run the script directly without installation. Either:
   - Install the package first (see Installation section)
   - Run the script using Python directly:
     ```sh
     python3 find_unused_attributes.py attributes.adoc
     ```

### Command not found

If the command isn't found after installation, ensure `$HOME/.local/bin` is in your PATH (see "Add to PATH" section above).

## License

This project is licensed under the terms of the [LICENSE](https://github.com/rolfedh/doc-utils/blob/main/LICENSE).