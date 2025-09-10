---
layout: home
title: doc-utils - AsciiDoc Documentation Utilities
---

# doc-utils

A comprehensive collection of Python utilities and CLI tools designed to help technical writers maintain clean, consistent AsciiDoc documentation repositories.

<div class="warning-box">
⚠️ <strong>IMPORTANT: Safety First</strong><br>
These tools can modify or delete files in your documentation repository. Always:
<ul>
  <li>Work in a git branch - Never run these tools on the main/master branch</li>
  <li>Review all changes carefully - Use <code>git diff</code> or a pull request to verify modifications</li>
  <li>Check your preview builds - Ensure no documentation errors were introduced</li>
</ul>
</div>

## Quick Start

### Installation

```bash
# Recommended: Install with pipx
pipx install rolfedh-doc-utils

# Alternative: Install with pip
pip install --user rolfedh-doc-utils
```

### Available Tools

<div class="tools-grid">
  <div class="tool-card">
    <h3>📝 format-asciidoc-spacing</h3>
    <p>Standardizes AsciiDoc formatting by ensuring proper spacing after headings and around include directives.</p>
    <a href="tools/format-asciidoc-spacing" class="btn">Learn More →</a>
  </div>

  <div class="tool-card">
    <h3>🔍 check-scannability</h3>
    <p>Analyzes document readability by checking sentence and paragraph length against best practices.</p>
    <a href="tools/check-scannability" class="btn">Learn More →</a>
  </div>

  <div class="tool-card">
    <h3>🗄️ archive-unused-files</h3>
    <p>Finds and optionally archives unreferenced AsciiDoc files in your documentation repository.</p>
    <a href="tools/archive-unused-files" class="btn">Learn More →</a>
  </div>

  <div class="tool-card">
    <h3>🖼️ archive-unused-images</h3>
    <p>Identifies and archives image files that are no longer referenced in your documentation.</p>
    <a href="tools/archive-unused-images" class="btn">Learn More →</a>
  </div>

  <div class="tool-card">
    <h3>🏷️ find-unused-attributes</h3>
    <p>Scans for AsciiDoc attribute definitions that are declared but never used in your documentation.</p>
    <a href="tools/find-unused-attributes" class="btn">Learn More →</a>
  </div>
</div>

## Key Features

- **🚀 Easy Installation** - Single package installation via pip or pipx
- **🔒 Safety First** - Built-in safety warnings and dry-run modes
- **📁 Smart Detection** - Automatically detects repository structure (OpenShift-docs or traditional)
- **🎯 Flexible Exclusions** - Exclude specific files or directories from processing
- **📊 Detailed Reports** - Clear output showing what was found and what actions were taken
- **🐍 Pure Python** - Cross-platform compatibility with minimal dependencies

## Documentation

<div class="nav-cards">
  <a href="getting-started" class="nav-card">
    <h3>Getting Started</h3>
    <p>Installation, setup, and your first commands</p>
  </a>
  
  <a href="tools/" class="nav-card">
    <h3>Tools Reference</h3>
    <p>Detailed documentation for each tool</p>
  </a>
  
  <a href="best-practices" class="nav-card">
    <h3>Best Practices</h3>
    <p>Safety guidelines and workflow recommendations</p>
  </a>
  
  <a href="contributing" class="nav-card">
    <h3>Contributing</h3>
    <p>How to contribute to the project</p>
  </a>
</div>

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

---

<div class="footer">
  <p>Made with ❤️ for technical writers by <a href="https://github.com/rolfedh">Rolfe Dlugy-Hegwer</a></p>
  <p>Licensed under the terms specified in the <a href="https://github.com/rolfedh/doc-utils/blob/main/LICENSE">LICENSE</a> file.</p>
</div>