---
layout: default
title: Contributing
nav_order: 14
---

# Contributing to doc-utils

Thank you for your interest in contributing to doc-utils! This guide will help you get started with contributing to the project.

## Ways to Contribute

### Report Bugs

Found a bug? Please [open an issue](https://github.com/rolfedh/doc-utils/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Any error messages or logs

### Suggest Features

Have an idea for improvement? [Open an issue](https://github.com/rolfedh/doc-utils/issues/new) with:
- Description of the feature
- Use case and benefits
- Examples of how it would work
- Any implementation ideas

### Improve Documentation

Documentation improvements are always welcome:
- Fix typos or clarify instructions
- Add examples and use cases
- Translate documentation
- Improve code comments

### Contribute Code

Ready to contribute code? Follow the development workflow below.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/doc-utils.git
cd doc-utils
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install in Development Mode

```bash
pip install -e .
pip install -r requirements-dev.txt
```

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## Development Guidelines

### Code Style

Follow PEP 8 Python style guidelines:

```bash
# Check code style with ruff (if available)
ruff check .

# Format code
black .  # if black is installed
```

Key style points:
- Use descriptive variable names
- Add type hints where appropriate
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Writing Tests

All new features must include tests:

```python
# tests/test_your_feature.py
import pytest
from doc_utils.your_module import your_function

def test_your_function():
    """Test that your_function works correctly."""
    result = your_function("input")
    assert result == "expected output"
```

Run tests:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=doc_utils

# Run specific test file
python -m pytest tests/test_your_feature.py
```

### Documentation

Update documentation for new features:

1. **Docstrings**: Add to all public functions
```python
def your_function(param: str) -> str:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param is invalid
    """
```

2. **User Documentation**: Update relevant .md files
3. **CHANGELOG.md**: Add entry under [Unreleased]
4. **README.md**: Update if adding new tools

## Making Changes

### 1. Implement Your Feature

```bash
# Make your changes
edit doc_utils/your_file.py

# Add/update tests
edit tests/test_your_feature.py

# Update documentation
edit relevant_docs.md
```

### 2. Test Your Changes

```bash
# Run tests
python -m pytest tests/ -v

# Test CLI tools manually
python your_new_tool.py --help

# Check for linting issues
ruff check .
```

### 3. Commit Your Changes

Write clear commit messages:

```bash
# Good commit messages
git commit -m "feat: Add support for Markdown files"
git commit -m "fix: Handle empty directories in file scanner"
git commit -m "docs: Clarify installation instructions"
git commit -m "test: Add tests for topic map parser"

# Use conventional commits:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# test: Test additions/changes
# refactor: Code refactoring
# style: Code style changes
# perf: Performance improvements
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then on GitHub:
1. Go to your fork
2. Click "Pull Request"
3. Fill in the PR template
4. Link related issues

## Pull Request Guidelines

### PR Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`python -m pytest tests/`)
- [ ] Code follows project style guidelines
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] CHANGELOG.md has an entry
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Existing tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Related Issues
Fixes #123
Relates to #456
```

## Project Structure

Understanding the project structure:

```
doc_utils/           # Core library modules
├── file_utils.py    # Shared file operations
├── scannability.py  # Readability checking
├── topic_map_parser.py  # YAML parsing
├── unused_adoc.py   # Unused file detection
├── unused_attributes.py # Attribute checking
└── unused_images.py # Image checking

tests/              # Test suite
├── test_*.py       # Test files
└── fixtures/       # Test data

*.py                # CLI entry points
docs/               # Documentation
```

## Adding a New Tool

To add a new CLI tool:

1. **Create the module** in `doc_utils/`:
```python
# doc_utils/your_tool.py
def process_files(files, options):
    """Core logic for your tool."""
    pass
```

2. **Create the CLI script**:
```python
# your_tool_cli.py
#!/usr/bin/env python3
import argparse
from doc_utils.your_tool import process_files

def main():
    parser = argparse.ArgumentParser()
    # Add arguments
    args = parser.parse_args()
    # Call your function
    process_files(args.files, args)

if __name__ == "__main__":
    main()
```

3. **Add to pyproject.toml**:
```toml
[project.scripts]
your-tool = "your_tool_cli:main"

[tool.setuptools]
py-modules = [..., "your_tool_cli"]
```

4. **Add tests**:
```python
# tests/test_your_tool.py
def test_your_tool():
    # Test your tool
    pass
```

5. **Add documentation**:
- Create `your_tool.md`
- Update README.md
- Add to docs/tools/

## Release Process

Maintainers follow this process for releases:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run full test suite
4. Create git tag
5. Push to GitHub
6. Create GitHub release
7. Package publishes automatically to PyPI

## Getting Help

Need help contributing?

- Check existing [issues](https://github.com/rolfedh/doc-utils/issues) and [PRs](https://github.com/rolfedh/doc-utils/pulls)
- Read the [development documentation](https://github.com/rolfedh/doc-utils/blob/main/CLAUDE.md)
- Ask questions in issues
- Review the test suite for examples

## Code of Conduct

Please note that this project follows a code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints
- Show empathy towards other contributors

## Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md entries
- Release notes

Thank you for contributing to doc-utils!