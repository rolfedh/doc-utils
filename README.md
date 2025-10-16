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

# Verify installation
doc-utils --version

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

### Quick Reference

Run `doc-utils` to see all available tools and their descriptions:

```bash
doc-utils --help     # Show comprehensive help
doc-utils --list     # List all tools
doc-utils --version  # Show version
```

### Individual Tools

**Note:** Commands use hyphens (`-`), while Python files use underscores (`_`). After installing with pipx, use the hyphenated commands directly.

| Tool | Description | Usage |
|------|-------------|-------|
| **`validate-links`** | Validates all links in documentation, with URL transposition for preview environments | `validate-links --transpose "https://prod--https://preview"` |
| **`extract-link-attributes`** | Extracts link/xref macros with attributes into reusable definitions | `extract-link-attributes --dry-run` |
| **`replace-link-attributes`** | Resolves Vale LinkAttribute issues by replacing attributes in link URLs | `replace-link-attributes --dry-run` |
| **`format-asciidoc-spacing`** | Standardizes spacing after headings and around includes | `format-asciidoc-spacing --dry-run modules/` |
| **`check-scannability`** | Analyzes readability (sentence/paragraph length) | `check-scannability --max-words 25` |
| **`archive-unused-files`** | Finds and archives unreferenced .adoc files | `archive-unused-files` (preview)<br>`archive-unused-files --archive` (execute) |
| **`archive-unused-images`** | Finds and archives unreferenced images | `archive-unused-images` (preview)<br>`archive-unused-images --archive` (execute) |
| **`find-unused-attributes`** | Identifies unused attribute definitions | `find-unused-attributes attributes.adoc` |
| **`convert-callouts-to-deflist`** | Converts callout-style annotations to definition list format | `convert-callouts-to-deflist --dry-run modules/` |

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

- **Latest Version**: 0.1.16 (with automatic update notifications)
- **Python Support**: 3.8+
- **Test Coverage**: 112+ tests (100% passing)
- **Dependencies**: Minimal (PyYAML for OpenShift-docs support)

### 🔔 Update Notifications

All tools automatically check for updates and notify you when a new version is available. The notification will recommend the appropriate upgrade command based on how you installed the package:

```
📦 Update available: 0.1.19 → 0.1.20
   Run: pipx upgrade rolfedh-doc-utils
```

To disable update checks, set the environment variable:
```bash
export DOC_UTILS_NO_VERSION_CHECK=1
```

Update checks are cached for 24 hours to minimize network requests.

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