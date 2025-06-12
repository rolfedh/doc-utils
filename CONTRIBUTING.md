# Contributing to doc-utils

Thank you for your interest in contributing! This guide is for developers and maintainers of the doc-utils project.

## Project Structure

- **`doc_utils/`**: Main Python package (all reusable logic)
- **CLI scripts**: Thin wrappers in the project root (e.g., `check_scannability.py`, `archive_unused_files.py`)
- **`tests/`**: Automated tests and test fixtures
- **Markdown docs**: Usage and help for each script (e.g., `check_scannability.md`)
- **`pyproject.toml`**: Packaging and metadata

## Modular Python Package

The core logic for all scripts is implemented in the `doc_utils/` package. You can import and reuse these utilities in your own scripts or tests:

- `doc_utils.file_utils` — file collection, manifest, and archiving utilities
- `doc_utils.unused_images` — logic for finding and archiving unused images
- `doc_utils.unused_adoc` — logic for finding and archiving unused AsciiDoc files
- `doc_utils.scannability` — logic for checking AsciiDoc scannability
- `doc_utils.unused_attributes` — logic for finding unused AsciiDoc attributes

## Getting Started

1. **Fork and clone the repository**
   ```sh
   git clone https://github.com/<your-username>/doc-utils.git
   cd doc-utils
   ```
2. **(Optional) Set up a virtual environment**
   ```sh
   python3 -m venv .venv
   . .venv/bin/activate
   python3 -m pip install -r requirements-dev.txt
   ```
3. **Install in editable mode for development**
   ```sh
   python3 -m pip install -e .
   ```

## Running and Adding Tests

- To run all tests:
  ```sh
  pip install -r requirements-dev.txt
  pytest
  ```
- Add or update test files in `tests/` (prefix with `test_`).
- Place reusable test data in `tests/fixtures/` if needed.
- See `tests/README.md` for more details.

## CLI Tool PATH Setup

After installing the package with pip, CLI tools are typically installed to:

```
$HOME/.local/bin
```

If this directory isn't in your `PATH`, running commands like `archive-unused-files` directly from the terminal won’t work.

Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:

```sh
source ~/.bashrc  # or ~/.zshrc
```

Or use the full path each time:

```sh
~/.local/bin/archive-unused-files
```

## Automated PyPI Publishing with GitHub Actions

This repository is configured to automatically build and publish new releases to PyPI using GitHub Actions.

**How it works:**

- Workflow file: `.github/workflows/pypi-publish.yml`.
- Trigger: push a new version tag (e.g., `v0.1.1`).
- Steps: checkout, set up Python, install build tools, build, upload to PyPI using your `PYPI_API_TOKEN` secret.

**What you need to do:**

1. Ensure your PyPI API token is set as a GitHub secret named `PYPI_API_TOKEN` in your repository settings.
2. Bump the version in `pyproject.toml`.
3. Commit and push your changes.
4. Create and push a new tag, e.g.:
   ```sh
   git tag v0.1.1
   git push origin v0.1.1
   ```
5. The workflow will run automatically and publish your new release to PyPI.

**Summary:**  
You are fully set up for automated PyPI publishing via GitHub Actions. Just push a new version tag and the rest is automatic!

## (Manual/Legacy) Publishing a Release to PyPI

Manual publishing is not required if you use the automated workflow above, but you can still do it as follows:

1. **Bump the version** in `pyproject.toml` (update the `version =` line to the next version, e.g., `0.1.1`).
2. **Remove old build artifacts:**
   ```sh
   rm -rf dist/ build/ *.egg-info
   ```
3. **Build the package:**
   ```sh
   python3 -m build
   ```
4. **Upload to PyPI:**
   ```sh
   python3 -m twine upload dist/*
   ```
   You will need a valid PyPI account and API token. If prompted, use your token as the password.

See the [PyPI documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for more details.

## Submitting Changes

- Open a pull request for your changes.
- Request review from maintainers.
- Ensure all tests pass and documentation is updated.

---

Thank you for helping improve doc-utils!
