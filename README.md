# doc-utils

This repository contains standalone scripts designed to help technical writers with documentation tasks.

**Purpose:**
Each script in this repository is self-contained and documents its own purpose, usage instructions, and examples at the top of the script file. For details on how to use a script, open the script and read the initial docstring or comments, or see the corresponding Markdown help file.

## Current Scripts

- **check_scannability.py**  
  Checks the scannability of AsciiDoc (`.adoc`) files in the current directory. Reports sentences that are too long and paragraphs that contain too many sentences, based on configurable limits. See [check_scannability.md](check_scannability.md) for usage and examples.

- **archive_unused_files.py**  
  Scans `./modules` and `./assemblies` for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_files.md](archive_unused_files.md) for usage and examples.

- **archive_unused_images.py**  
  Scans `./modules` and `./assemblies` for image files (e.g., `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_images.md](archive_unused_images.md) for usage and examples.

## How to Use

1. Open the script you are interested in (for example, `check_scannability.py`).
2. Read the top of the script or the corresponding `.md` file for instructions, options, and examples.
3. Run the script from your terminal as described in the usage section.

## Running Tests

To run all tests, install the development requirements and run pytest from the project root:

```sh
pip install -r requirements-dev.txt
pytest
```

All tests and fixtures are located in the `tests/` directory. See `tests/README.md` for details.

---

*For licensing information, see [LICENSE](LICENSE).*
