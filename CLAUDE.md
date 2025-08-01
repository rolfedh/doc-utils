# CLAUDE.md - AI Assistant Context for doc-utils

## Project Overview

doc-utils is a collection of Python utilities and CLI tools designed to help technical writers maintain AsciiDoc documentation repositories. The tools help identify unused content, check document readability, and maintain clean documentation projects.

## Key Components

### CLI Tools

1. **find-unused-attributes** - Scans AsciiDoc files to find unused attribute definitions
2. **check-scannability** - Analyzes document readability by checking sentence/paragraph length
3. **archive-unused-files** - Finds and optionally archives unreferenced AsciiDoc files
4. **archive-unused-images** - Finds and optionally archives unreferenced image files

### Core Modules

- `doc_utils/file_utils.py` - Core file scanning and archiving functionality
- `doc_utils/unused_attributes.py` - Logic for finding unused AsciiDoc attributes
- `doc_utils/unused_adoc.py` - Logic for finding unused AsciiDoc files
- `doc_utils/unused_images.py` - Logic for finding unused images
- `doc_utils/scannability.py` - Document readability analysis

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Add docstrings to all public functions

### Testing
- Run tests with: `python -m pytest tests/`
- Ensure new features have corresponding tests
- Test coverage focuses on core functionality and CLI entry points

### Common Tasks

#### Running Linting and Type Checking
The project uses standard Python linting tools. Run these commands to check code quality:
```bash
# If ruff is available
ruff check .

# If mypy is configured
mypy doc_utils/
```

#### Installing for Development
```bash
# Clone and install in editable mode
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils
pip install -e .
pip install -r requirements-dev.txt
```

#### Creating a New Release
1. Update version in `pyproject.toml`
2. Create a git tag: `git tag v0.1.2`
3. Push tags: `git push origin --tags`
4. The GitHub Action will automatically publish to PyPI

## Architecture Decisions

### File Scanning Strategy
- Uses `os.walk()` for recursive directory traversal
- Excludes symbolic links to prevent infinite loops
- Supports both file and directory exclusion patterns
- Normalizes all paths to absolute paths for reliable comparison

### CLI Design
- Each tool is a standalone script with a `main()` function
- Entry points are configured in `pyproject.toml`
- Common exclusion options (--exclude-dir, --exclude-file, --exclude-list)
- Consistent output format across tools

### Testing Approach
- Unit tests for core functionality (file_utils, unused_attributes)
- Integration tests for CLI commands
- Mock filesystem operations where appropriate
- Test both success and error conditions

## Known Issues and Limitations

1. **Fixed Scan Directories**: Most tools have hardcoded scan paths (e.g., `./modules`, `./assemblies`)
2. **Current Directory Execution**: Tools must be run from the documentation project root
3. **AsciiDoc Parsing**: Simple regex-based parsing may miss complex attribute usage

## Future Enhancements to Consider

1. **Configurable Scan Paths**: Allow users to specify which directories to scan
2. **Configuration File**: Support `.docutils.yml` for project-specific settings
3. **Performance Optimization**: Parallel file scanning for large repositories
4. **Extended Format Support**: Support for Markdown or other documentation formats
5. **Dry Run Mode**: Show what would be changed without making modifications

## Debugging Tips

### Module Import Errors
If you encounter `ModuleNotFoundError`, ensure:
1. The package is installed: `pip install -e .`
2. You're in the correct virtual environment
3. The `py-modules` configuration in `pyproject.toml` includes all CLI scripts

### File Path Issues
- Always use absolute paths internally
- Be aware of the current working directory
- Test on both Linux/macOS and Windows for path compatibility

### Exclusion Not Working
- Check that paths are normalized (absolute paths)
- Verify parent directory exclusion logic in `file_utils.py`
- Remember that excluding a parent excludes all children

## Contributing

When contributing to this project:
1. Ensure all tests pass before submitting changes
2. Add tests for new functionality
3. Update documentation as needed
4. Follow the existing code style and patterns
5. Test CLI commands manually in addition to unit tests

## Security Considerations

- Never process files outside the project directory without explicit user permission
- Be cautious with file deletion operations (always require --archive flag)
- Validate all file paths to prevent directory traversal attacks
- Don't follow symbolic links to avoid security issues

## Performance Considerations

- File scanning can be slow on large repositories
- Consider caching results for repeated operations
- Archive operations should batch file processing
- Regular expressions should be compiled once and reused