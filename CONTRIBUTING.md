# Contributing to doc-utils

Thank you for your interest in contributing! This guide is for developers and maintainers of the doc-utils project.

## Project Structure

- **`doc_utils/`**: Main Python package (all reusable logic)
- **CLI scripts**: Thin wrappers in the project root (e.g., `check_scannability.py`, `archive_unused_files.py`)
- **`tests/`**: Automated tests and test fixtures
- **Markdown docs**: Usage and help for each script (e.g., `check_scannability.md`)
- **`pyproject.toml`**: Packaging and metadata

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

## Running and Testing

- Run tests with:
  ```sh
  pytest
  ```
- Add or update test files in `tests/` (prefix with `test_`).
- Place reusable test data in `tests/fixtures/` if needed.

## CLI Tool Installation and PATH Setup

After installing the package with pip, CLI tools are typically installed to:

```
$HOME/.local/bin
```

If this directory isn't in your `PATH`, running commands like `archive-unused-files` directly from the terminal won’t work unless you:

**Option 1: Add to PATH (Recommended)**

Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

**Option 2: Run with full path**

Use the full path each time:

```bash
~/.local/bin/archive-unused-files
```

## Submitting Changes

- Open a pull request for your changes.
- Request review from maintainers.
- Ensure all tests pass and documentation is updated.

---

Thank you for helping improve doc-utils!
