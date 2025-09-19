# doc-utils

[![PyPI version](https://badge.fury.io/py/rolfedh-doc-utils.svg)](https://pypi.org/project/rolfedh-doc-utils/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/rolfedh/doc-utils)](https://github.com/rolfedh/doc-utils/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-brightgreen)](https://rolfedh.github.io/doc-utils/)

Python CLI tools for maintaining clean, consistent AsciiDoc documentation repositories.

📚 **[View Full Documentation](https://rolfedh.github.io/doc-utils/)** | 📦 **[PyPI Package](https://pypi.org/project/rolfedh-doc-utils/)** | 🐙 **[GitHub](https://github.com/rolfedh/doc-utils)**

## ⚠️ Safety First

These tools can modify or delete files. **Always:**
- Work in a git branch (never main/master)
- Review changes with `git diff`
- Test documentation builds after changes

## 🚀 Quick Start

### Install with pipx (Recommended)

```bash
# Install
pipx install rolfedh-doc-utils

# Upgrade to latest version
pipx upgrade rolfedh-doc-utils
```

### Alternative Installation

```bash
# With pip user flag
pip install --user rolfedh-doc-utils

# For development
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils
pip install -e .
```

## 🛠️ Available Tools

**Note:** Commands use hyphens (`-`), while Python files use underscores (`_`). After installing with pipx, use the hyphenated commands directly.

| Tool | Description | Usage |
|------|-------------|-------|
| **`format-asciidoc-spacing`** | Standardizes spacing after headings and around includes | `format-asciidoc-spacing --dry-run modules/` |
| **`check-scannability`** | Analyzes readability (sentence/paragraph length) | `check-scannability --max-words 25` |
| **`archive-unused-files`** | Finds and archives unreferenced .adoc files | `archive-unused-files` (preview)<br>`archive-unused-files --archive` (execute) |
| **`archive-unused-images`** | Finds and archives unreferenced images | `archive-unused-images` (preview)<br>`archive-unused-images --archive` (execute) |
| **`find-unused-attributes`** | Identifies unused attribute definitions | `find-unused-attributes attributes.adoc` |

## 📖 Documentation

Comprehensive documentation is available at **[rolfedh.github.io/doc-utils](https://rolfedh.github.io/doc-utils/)**

### OpenShift-docs Example

For OpenShift documentation repositories:

```bash
# Format spacing in specific directories
format-asciidoc-spacing modules/
format-asciidoc-spacing microshift_networking/

# Preview changes first
format-asciidoc-spacing --dry-run modules/networking/

# Process specific file
format-asciidoc-spacing modules/networking/about-networking.adoc
```

- [Getting Started Guide](https://rolfedh.github.io/doc-utils/getting-started)
- [Tools Reference](https://rolfedh.github.io/doc-utils/tools/)
- [Best Practices](https://rolfedh.github.io/doc-utils/best-practices)
- [Contributing](https://rolfedh.github.io/doc-utils/contributing)

## 💡 Common Workflows

### Clean Up Documentation

```bash
# 1. Create a branch
git checkout -b doc-cleanup

# 2. Preview what would change
format-asciidoc-spacing --dry-run .
archive-unused-files
archive-unused-images

# 3. Apply changes
format-asciidoc-spacing .
archive-unused-files --archive
archive-unused-images --archive

# 4. Review and commit
git diff
git add -A && git commit -m "Clean up documentation"
```

### Check Documentation Quality

```bash
# Check readability
check-scannability --max-words 30 --max-sentences 5

# Find unused attributes
find-unused-attributes attributes.adoc

# Save results
find-unused-attributes attributes.adoc --output unused.txt
```

## 🔧 Exclusions

All tools support excluding files and directories:

```bash
# Exclude specific directories
archive-unused-files --exclude-dir ./temp --exclude-dir ./drafts

# Exclude specific files
check-scannability --exclude-file ./README.adoc

# Use exclusion list file
echo "./deprecated/" > .docutils-ignore
archive-unused-images --exclude-list .docutils-ignore
```

## 🧪 Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_file_utils.py
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](https://rolfedh.github.io/doc-utils/contributing) for details.

Before submitting PRs:
- ✅ All tests pass
- ✅ Code follows PEP 8
- ✅ Documentation updated
- ✅ Changelog entry added

## 📊 Project Status

- **Latest Version**: 0.1.6
- **Python Support**: 3.8+
- **Test Coverage**: 66+ tests (100% passing)
- **Dependencies**: Minimal (PyYAML for OpenShift-docs support)

## 🔗 Resources

- [Documentation](https://rolfedh.github.io/doc-utils/)
- [PyPI Package](https://pypi.org/project/rolfedh-doc-utils/)
- [Issue Tracker](https://github.com/rolfedh/doc-utils/issues)
- [Changelog](https://github.com/rolfedh/doc-utils/blob/main/CHANGELOG.md)
- [License](https://github.com/rolfedh/doc-utils/blob/main/LICENSE)

## 📝 License

This project is licensed under the terms specified in the [LICENSE](https://github.com/rolfedh/doc-utils/blob/main/LICENSE) file.

---

Created by [Rolfe Dlugy-Hegwer](https://github.com/rolfedh) for technical writers everywhere.