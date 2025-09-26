---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started with doc-utils

This guide will help you install and start using doc-utils to maintain your AsciiDoc documentation repositories.

## Prerequisites

- Python 3.8 or higher
- pip or pipx package manager
- Git (for version control safety)

## Installation

### Method 1: Using pipx (Recommended)

[pipx](https://pypa.github.io/pipx/) is ideal for installing CLI tools in isolated environments:

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install doc-utils
pipx install rolfedh-doc-utils

# Upgrade to latest version
pipx upgrade rolfedh-doc-utils
```

### Method 2: Using pip with --user flag

```bash
pip install --user rolfedh-doc-utils
```

### Method 3: Development Installation

For contributing or testing:

```bash
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils
pip install -e .
pip install -r requirements-dev.txt
```

## Verify Installation

After installation, verify the tools are available:

```bash
# Check individual tools
extract-link-attributes --help
replace-link-attributes --help
format-asciidoc-spacing --help
check-scannability --help
archive-unused-files --help
archive-unused-images --help
find-unused-attributes --help
```

## Add to PATH (if needed)

If commands aren't found, add the installation directory to your PATH:

```bash
# Add to your shell configuration (~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Reload your shell
source ~/.bashrc
```

## Your First Commands

### 1. Check Document Readability

Analyze your documentation for readability issues:

```bash
# Check all .adoc files in current directory
check-scannability

# Check with custom limits
check-scannability --max-words 30 --max-sentences 5
```

### 2. Format AsciiDoc Spacing

Standardize spacing in your AsciiDoc files:

```bash
# Preview changes without modifying files
format-asciidoc-spacing --dry-run modules/

# Apply formatting with verbose output
format-asciidoc-spacing --verbose modules/
```

### 3. Find Unused Content

Identify unused files and images:

```bash
# Find unused AsciiDoc files (preview mode)
archive-unused-files

# Find unused images (preview mode)
archive-unused-images

# Actually archive unused files (be careful!)
archive-unused-files --archive
```

### 4. Find Unused Attributes

Check for unused attribute definitions:

```bash
find-unused-attributes attributes.adoc
```

### 5. Extract Links to Attributes

Create reusable attribute definitions from link and xref macros:

```bash
# Preview what would be extracted
extract-link-attributes --dry-run

# Extract links interactively
extract-link-attributes

# Non-interactive extraction
extract-link-attributes --non-interactive

# Use specific attributes file and directories
extract-link-attributes \
  --attributes-file common-attributes.adoc \
  --scan-dir modules \
  --scan-dir assemblies
```

### 6. Fix Vale LinkAttribute Issues

Replace attribute references in link URLs for DITA compliance:

```bash
# Preview changes
replace-link-attributes --dry-run

# Apply changes interactively
replace-link-attributes

# Use specific attributes file
replace-link-attributes --attributes-file common/attributes.adoc
```

## Safety Best Practices

### Always Work in a Git Branch

Before using any doc-utils tools:

```bash
# Create a new branch
git checkout -b doc-cleanup-$(date +%Y%m%d)

# Commit any pending changes
git add -A
git commit -m "Save work before cleanup"
```

### Use Preview/Dry-Run Modes First

Most tools support preview modes:

```bash
# Preview what would be changed
format-asciidoc-spacing --dry-run .
archive-unused-files  # No --archive flag means preview only
```

### Review Changes Before Committing

After running tools:

```bash
# Review all changes
git diff

# Check your documentation still builds
# (run your build command here)

# If everything looks good, commit
git add -A
git commit -m "Clean up documentation with doc-utils"
```

## Excluding Files and Directories

All tools support exclusion options:

### Exclude Specific Directories

```bash
archive-unused-files --exclude-dir ./modules/temp --exclude-dir ./modules/old
```

### Exclude Specific Files

```bash
check-scannability --exclude-file ./README.adoc --exclude-file ./test.adoc
```

### Use an Exclusion List File

Create a `.docutils-ignore` file:

```
# Comments are supported
./modules/deprecated/
./assemblies/archive/
./images/temp/
specific-file.adoc
```

Then use it:

```bash
archive-unused-images --exclude-list .docutils-ignore
```

## Next Steps

- Explore the [Tools Reference](/doc-utils/tools/) for detailed documentation
- Read [Best Practices](/doc-utils/best-practices) for workflow recommendations
- Check the [Contributing Guide](/doc-utils/contributing) if you want to help improve doc-utils

## Getting Help

- [Open an issue](https://github.com/rolfedh/doc-utils/issues) on GitHub
- Check existing [documentation](https://github.com/rolfedh/doc-utils#readme)
- Review the [changelog](https://github.com/rolfedh/doc-utils/blob/main/CHANGELOG.md) for recent changes