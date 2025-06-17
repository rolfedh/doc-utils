# doc-utils

Python utilities and CLI scripts to help technical writers maintain Asciidoc repositories.

For more information: 
- https://pypi.org/project/rolfedh-doc-utils/
- https://github.com/rolfedh/doc-utils

## Installation

Install from PyPI:

```sh
pip install rolfedh-doc-utils
```

This will install the following CLI commands globally:
- `check-scannability`
- `archive-unused-files`
- `archive-unused-images`
- `find-unused-attributes`

You can then run these commands from any directory.

### PATH Setup (if needed)

These CLI tools are typically installed to:
```
$HOME/.local/bin
```
If this directory isn't in your `PATH`, running commands like `archive-unused-files` directly from the terminal won’t work. 
In that case, add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Then reload your shell:
```sh
source ~/.bashrc  # or ~/.zshrc
```

## Current Scripts

- **check_scannability.py**  
  Checks the scannability of AsciiDoc (`.adoc`) files in the current directory. Reports sentences that are too long and paragraphs that contain too many sentences, based on configurable limits. See [check_scannability.md](check_scannability.md) for usage and examples.

- **archive_unused_files.py**  
  Scans `./modules` and `./assemblies` for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_files.md](archive_unused_files.md) for usage and examples.

- **archive_unused_images.py**  
  Scans all directories for image files (e.g., `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_images.md](archive_unused_images.md) for usage and examples.

- **find_unused_attributes.py**  
  Scans a user-specified attributes file (e.g., `attributes.adoc`) for attribute definitions (e.g., `:version:`) and recursively scans all `.adoc` files in the current directory for usages (e.g., `{version}`). Reports any attribute that is defined but not used in any `.adoc` file as **NOT USED** in both the command line output and a timestamped output file. See [find_unused_attributes.md](find_unused_attributes.md) for usage and examples.

## How to Use

After installation, use the CLI commands directly, for example:

```sh
check-scannability --help
archive-unused-files --help
find-unused-attributes attributes.adoc
```

Or, if running from source:

```sh
python3 check_scannability.py
python3 archive_unused_files.py
python3 find_unused_attributes.py attributes.adoc
```

See each script's `.md` file for detailed usage and options.

---

*For licensing information, see [LICENSE](LICENSE).*
