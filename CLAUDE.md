# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

doc-utils is a collection of Python utilities and CLI tools designed to help technical writers maintain AsciiDoc documentation repositories. The tools help identify unused content, check document readability, and maintain clean documentation projects.

## Project Structure

```
doc-utils/
├── doc_utils/              # Core library modules
│   ├── __init__.py
│   ├── file_utils.py       # File operations and exclusion handling
│   ├── scannability.py     # Document readability checks
│   ├── topic_map_parser.py # Parse OpenShift-docs topic maps
│   ├── unused_adoc.py      # Find unused AsciiDoc files
│   ├── unused_attributes.py # Find unused attributes
│   └── unused_images.py    # Find unused images
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_*.py          # Test files
│   └── test_fixture_*.py  # Test fixtures
├── *.py                   # CLI entry point scripts
├── *.md                   # Documentation for each tool
├── setup.py              # Custom installation hooks
├── pyproject.toml         # Package configuration
├── requirements-dev.txt   # Development dependencies (pytest, PyYAML)
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # Contribution guidelines
└── CLAUDE.md            # This file

```

## Key Components

### CLI Tools

1. **find-unused-attributes** - Scans AsciiDoc files to find unused attribute definitions
2. **check-scannability** - Analyzes document readability by checking sentence/paragraph length
3. **archive-unused-files** - Finds and optionally archives unreferenced AsciiDoc files
4. **archive-unused-images** - Finds and optionally archives unreferenced image files
5. **format-asciidoc-spacing** - Standardizes AsciiDoc formatting (blank lines after headings and around includes)

### Core Modules

- `doc_utils/file_utils.py` - Core file scanning, archiving, and exclusion list parsing
- `doc_utils/topic_map_parser.py` - Parse OpenShift-docs style topic map YAML files
- `doc_utils/unused_attributes.py` - Logic for finding unused AsciiDoc attributes
- `doc_utils/unused_adoc.py` - Logic for finding unused AsciiDoc files (supports both topic maps and master.adoc)
- `doc_utils/unused_images.py` - Logic for finding unused images
- `doc_utils/scannability.py` - Document readability analysis

## Common Development Commands

### Installing for Development
```bash
# Clone and install in editable mode
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with verbose output  
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_file_utils.py
```

### Linting and Type Checking
```bash
# If ruff is available
ruff check .

# If mypy is configured
mypy doc_utils/
```

### Building Package
```bash
# Build distribution packages
python -m build
```

### Creating a New Release

Follow these exact steps to release a new version:

1. **Update version in `pyproject.toml`**
   ```bash
   # Edit pyproject.toml and change version = "X.Y.Z" to new version
   ```

2. **Update CHANGELOG.md**
   ```bash
   # Move items from [Unreleased] to new version section with date
   # Format: ## [X.Y.Z] - YYYY-MM-DD
   ```

3. **Run full test suite**
   ```bash
   python -m pytest tests/ -v --tb=short
   # Verify all tests pass (should show "XX passed")
   ```

4. **Stage and commit changes**
   ```bash
   git add -A
   git status  # Verify only pyproject.toml and CHANGELOG.md are changed
   git commit -am "Prepare release vX.Y.Z"
   ```

5. **Create annotated tag**
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z: Brief description of main changes"
   ```

6. **Push to GitHub**
   ```bash
   git push origin main --tags
   ```

7. **Automatic Publishing to PyPI and GitHub Release**
   - GitHub Action automatically:
     - Publishes package to PyPI
     - Creates GitHub Release (if not already created)
     - Uploads distribution files to the release
   - Monitor progress at: https://github.com/rolfedh/doc-utils/actions
   - Package will be available at: https://pypi.org/project/rolfedh-doc-utils/
   - GitHub Release will appear at: https://github.com/rolfedh/doc-utils/releases

8. **Manual GitHub Release (Optional)**
   If you want to create the release manually before the workflow runs:
   ```bash
   # Extract release notes from CHANGELOG.md for the new version
   # Create release using GitHub CLI
   gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "Release notes here"
   ```
   Note: The workflow will detect existing releases and only upload distribution files

**Example for releasing v0.1.7:**
```bash
# 1. Update pyproject.toml: version = "0.1.7"
# 2. Update CHANGELOG.md: Move unreleased items to ## [0.1.7] - YYYY-MM-DD
# 3. Test
python -m pytest tests/ -v --tb=short
# 4. Commit
git add -A && git commit -am "Prepare release v0.1.7"
# 5. Tag
git tag -a v0.1.7 -m "Release v0.1.7: Brief description"
# 6. Push (this triggers the workflow)
git push origin main --tags
# 7. Monitor the automated release at https://github.com/rolfedh/doc-utils/actions
```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Add docstrings to all public functions

### Testing
- Ensure new features have corresponding tests
- Test coverage focuses on core functionality and CLI entry points
- Current test suite: 66+ tests total (100% pass rate)
- Test fixtures are located in `tests/` directory
- Tests use pytest framework with fixtures for temporary directories

### Dependencies
- **PyYAML** (>=6.0): Required for parsing topic map files in OpenShift-docs repositories
- **pytest**: Development dependency for running tests

## Architecture Decisions

### Repository Type Detection
- Automatically detects repository style (OpenShift-docs vs traditional)
- OpenShift-docs: Looks for `_topic_maps/*.yml` files
- Traditional: Looks for `master.adoc` files
- Falls back to scanning `include::` directives in all cases

### File Scanning Strategy
- Uses `os.walk()` for recursive directory traversal
- Excludes symbolic links to prevent infinite loops
- Supports both file and directory exclusion patterns
- Normalizes all paths to absolute paths for reliable comparison

### CLI Design
- Each tool is a standalone script with a `main()` function
- Entry points are configured in `pyproject.toml` with `py-modules`
- All tools support common exclusion options (--exclude-dir, --exclude-file, --exclude-list)
- Exclusion list parsing is centralized in `file_utils.parse_exclude_list_file()`
- Consistent output format across tools
- Archive tools display safety warnings on execution

### Testing Approach
- Unit tests for core functionality (file_utils, unused_attributes)
- Integration tests for CLI commands
- Mock filesystem operations where appropriate
- Test both success and error conditions

## Known Issues and Limitations

1. ~~**Fixed Scan Directories**: Most tools have hardcoded scan paths~~ ✅ Fixed in v0.1.5 with auto-discovery
2. **Current Directory Execution**: Tools must be run from the documentation project root
3. **AsciiDoc Parsing**: Simple regex-based parsing may miss complex attribute usage

## Future Enhancements to Consider

### General Improvements
1. ~~**Configurable Scan Paths**: Allow users to specify which directories to scan~~ ✅ Implemented in v0.1.5
2. **Configuration File**: Support `.docutils.yml` for project-specific settings
3. **Performance Optimization**: Parallel file scanning for large repositories
4. **Extended Format Support**: Support for Markdown or other documentation formats
5. **Dry Run Mode**: Show what would be changed without making modifications (partially implemented - archive tools preview by default)

### format-asciidoc-spacing Specific Improvements
1. **Add Comprehensive Tests**
   - Create `tests/test_format_asciidoc_spacing.py` with unit tests
   - Test heading spacing logic
   - Test include directive spacing
   - Test edge cases (empty files, consecutive headings, etc.)

2. **Add Exclusion Options** (for consistency with other tools)
   - Add `--exclude-dir`, `--exclude-file`, `--exclude-list` options
   - Integrate with existing `file_utils.parse_exclude_list_file()` function

3. **Enhanced Features**
   - **Backup option**: Create `.bak` files before modifying
   - **Report mode**: Generate a summary report of changes made
   - **Config file support**: Allow `.formatrc` or similar for default settings
   - **Exit codes**: Return non-zero if changes were needed (useful for CI/CD)
   - **Progress bar**: Show progress for large file sets

4. **Safety Improvements**
   - Add confirmation prompt when not in dry-run mode
   - Check if running in a git repository and warn if uncommitted changes exist
   - Integrate with existing safety warning system

5. **Performance Optimization**
   - Parallel processing of files for large repositories
   - Compile regex patterns once and reuse them

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
- Safety warnings remind users to work in git branches

## Performance Considerations

- File scanning can be slow on large repositories
- Consider caching results for repeated operations
- Archive operations should batch file processing
- Regular expressions should be compiled once and reused

## Recent Improvements (Latest Refactoring)

### New AsciiDoc Spacing Formatter (v0.1.6)
1. **New CLI Tool**: `format-asciidoc-spacing` for standardizing AsciiDoc formatting
   - Automatically adds blank lines after headings (=, ==, ===, etc.)
   - Adds blank lines around include:: directives
   - Supports dry-run mode to preview changes
   - Verbose mode for detailed change tracking
   - Processes single files or entire directories recursively
2. **Python Implementation**: Written in Python with no external dependencies
3. **Integration**: Fully integrated with package installation via pyproject.toml

### Automatic Directory Discovery (v0.1.5)
1. **Auto-discovery of scan directories**: `archive-unused-files` now automatically finds all `modules` and `assemblies` directories
   - No longer requires hardcoded paths at repository root
   - Works with any repository structure (nested, multiple locations)
   - New `find_scan_directories()` function in `unused_adoc.py`
2. **New `--scan-dir` option**: Override auto-discovery with specific directories
3. **Transparent output**: Shows discovered directories for user visibility

### Symlink Handling Fix (v0.1.4)
1. **Fixed infinite loop**: Replaced recursive glob with os.walk that skips symlinks
2. **Prevents freezing**: Handles circular symbolic links in `.archive` directories
3. **Added tests**: Comprehensive symlink handling test coverage

### Safety Improvements
1. **Installation Safety Message**: Custom setup.py displays safety reminders after installation
2. **Runtime Warnings**: Archive tools show concise safety warning when executed
3. **Warning Message**: "⚠️  SAFETY: Work in a git branch! Run without --archive first to preview."

### OpenShift-docs Support (v0.1.3)
1. **Topic Map Support**: Added ability to parse OpenShift-docs style repositories
   - New `topic_map_parser.py` module for YAML parsing
   - Automatic detection of repository type
   - Supports nested topic structures
2. **Dual Repository Support**: `archive-unused-files` now works with both:
   - OpenShift-docs style (uses `_topic_maps/*.yml`)
   - Traditional AsciiDoc (uses `master.adoc` files)
3. **Backward Compatibility**: Existing functionality preserved for traditional repos

### Code Quality Improvements
1. **Eliminated Code Duplication**: Created `parse_exclude_list_file()` to centralize exclusion parsing logic
2. **Removed Dead Code**: 
   - Removed unused `re` import from `file_utils.py`
   - Removed legacy test runner files (`test_run_*.py`)
   - Removed `fixtures-README-legacy.txt`
3. **Improved Organization**: Moved test fixtures from root to `tests/` directory
4. **Enhanced Consistency**: Added exclusion support to `check-scannability` tool

### Testing Improvements
- Added comprehensive tests for `file_utils.py` functions (14 tests)
- Added tests for CLI entry points (15 tests)
- Added tests for the new `parse_exclude_list_file()` function
- Added tests for topic map parsing (9 tests)
- Fixed all failing tests related to substring matching and output expectations
- Total test coverage: 56 tests with 100% pass rate

### Key Functions to Know

#### `file_utils.parse_exclude_list_file(exclude_list_path)`
Parses an exclusion list file and returns tuple of (exclude_dirs, exclude_files).
- Supports comments (lines starting with #)
- Automatically detects directories vs files
- Returns empty lists if file doesn't exist

#### `file_utils.collect_files(scan_dirs, extensions, exclude_dirs=None, exclude_files=None)`
Core file collection function used by all tools.
- Handles symlink exclusion
- Implements parent directory exclusion logic
- Normalizes all paths to absolute paths
- Removes duplicates while preserving order

#### `topic_map_parser.detect_repo_type(base_path='.')`
Detects repository type (OpenShift-docs vs traditional).
- Returns 'topic_map', 'master_adoc', or 'unknown'
- Checks for `_topic_maps/*.yml` files
- Falls back to checking for `master.adoc` files

#### `topic_map_parser.get_all_topic_map_references(base_path='.')`
Extracts all .adoc file references from topic map YAML files.
- Parses all .yml files in `_topic_maps/` directory
- Handles nested topic structures
- Returns set of all referenced file paths