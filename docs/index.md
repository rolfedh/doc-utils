---
layout: default
title: Home
nav_order: 1
description: "doc-utils is a comprehensive collection of Python utilities and CLI tools for maintaining AsciiDoc documentation repositories."
permalink: /
---

# doc-utils
{: .fs-9 }

A comprehensive collection of Python utilities and CLI tools designed to help technical writers maintain clean, consistent AsciiDoc documentation repositories.
{: .fs-6 .fw-300 }

[Get started now](#quick-start){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/rolfedh/doc-utils){: .btn .fs-5 .mb-4 .mb-md-0 }

---

{: .warning }
> **Safety First!**
> 
> These tools can modify or delete files in your documentation repository. Always:
> - Work in a git branch - Never run these tools on the main/master branch
> - Review all changes carefully - Use `git diff` or a pull request to verify modifications
> - Check your preview builds - Ensure no documentation errors were introduced

## Quick Start

### Installation

```bash
# Recommended: Install with pipx
pipx install rolfedh-doc-utils

# Alternative: Install with pip
pip install --user rolfedh-doc-utils
```

### Available Tools

#### 📝 format-asciidoc-spacing
Standardizes AsciiDoc formatting by ensuring proper spacing after headings and around include directives.

[Learn More →](tools/format-asciidoc-spacing){: .btn .btn-outline }

---

#### 🔍 check-scannability
Analyzes document readability by checking sentence and paragraph length against best practices.

[Learn More →](tools/check-scannability){: .btn .btn-outline }

---

#### 🗄️ archive-unused-files
Finds and optionally archives unreferenced AsciiDoc files in your documentation repository.

[Learn More →](tools/archive-unused-files){: .btn .btn-outline }

---

#### 🖼️ archive-unused-images
Identifies and archives image files that are no longer referenced in your documentation.

[Learn More →](tools/archive-unused-images){: .btn .btn-outline }

---

#### 🏷️ find-unused-attributes
Scans for AsciiDoc attribute definitions that are declared but never used in your documentation.

[Learn More →](tools/find-unused-attributes){: .btn .btn-outline }

## Key Features

- **🚀 Easy Installation** - Single package installation via pip or pipx
- **🔒 Safety First** - Built-in safety warnings and dry-run modes
- **📁 Smart Detection** - Automatically detects repository structure (OpenShift-docs or traditional)
- **🎯 Flexible Exclusions** - Exclude specific files or directories from processing
- **📊 Detailed Reports** - Clear output showing what was found and what actions were taken
- **🐍 Pure Python** - Cross-platform compatibility with minimal dependencies

## Documentation

- [**Getting Started**](getting-started) - Installation, setup, and your first commands
- [**Tools Reference**](tools/) - Detailed documentation for each tool
- [**Best Practices**](best-practices) - Safety guidelines and workflow recommendations
- [**Contributing**](contributing) - How to contribute to the project

## Latest Release

**Version 0.1.6** - Released September 10, 2025

### What's New
- ✨ New `format-asciidoc-spacing` tool for standardizing AsciiDoc formatting
- 🔧 Automatically adds blank lines after headings and around include directives
- 📝 Supports dry-run mode and verbose output

[View all releases →](https://github.com/rolfedh/doc-utils/releases)

## Resources

- [GitHub Repository](https://github.com/rolfedh/doc-utils)
- [PyPI Package](https://pypi.org/project/rolfedh-doc-utils/)
- [Issue Tracker](https://github.com/rolfedh/doc-utils/issues)
- [Changelog](https://github.com/rolfedh/doc-utils/blob/main/CHANGELOG.md)