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
│   ├── format_asciidoc_spacing.py # AsciiDoc spacing formatter logic
│   ├── replace_link_attributes.py # Link attribute replacement logic
│   ├── scannability.py     # Document readability checks
│   ├── topic_map_parser.py # Parse OpenShift-docs topic maps
│   ├── unused_adoc.py      # Find unused AsciiDoc files
│   ├── unused_attributes.py # Find unused attributes
│   └── unused_images.py    # Find unused images
├── callout_lib/            # Callout conversion library
│   ├── __init__.py
│   ├── detector.py         # Callout detection and extraction
│   ├── converter_deflist.py # Definition list converter
│   ├── converter_bullets.py # Bulleted list converter
│   ├── converter_comments.py # Inline comments converter
│   ├── README.md          # Library documentation
│   └── IMPLEMENTATION_SUMMARY.md # Implementation overview
├── docs/                   # GitHub Pages documentation
│   ├── tools/             # Tool-specific documentation
│   │   ├── convert-callouts-to-deflist.md
│   │   ├── convert-callouts-interactive.md
│   │   ├── replace-link-attributes.md
│   │   ├── format-asciidoc-spacing.md
│   │   └── ...
│   ├── getting-started.md
│   └── index.md
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_*.py          # Test files
│   └── test_fixture_*.py  # Test fixtures
├── .archive/              # Archived/reference files
│   └── SLACK_NOTE_FOR_TESTER.md # Testing documentation
├── *.py                   # CLI entry point scripts
├── convert_callouts_to_deflist.py   # Batch callout converter
├── convert_callouts_interactive.py  # Interactive callout converter
├── setup.py              # Custom installation hooks
├── pyproject.toml         # Package configuration
├── requirements-dev.txt   # Development dependencies (pytest, PyYAML)
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # Contribution guidelines
└── CLAUDE.md            # This file

```

## Key Components

### CLI Tools

1. **validate-links** [EXPERIMENTAL] - Validates all links in documentation with URL transposition for preview environments
2. **extract-link-attributes** - Extracts link/xref macros with attributes into reusable attribute definitions
3. **replace-link-attributes** - Resolves Vale LinkAttribute issues by replacing attributes in link URLs
4. **find-unused-attributes** - Scans AsciiDoc files to find unused attribute definitions (now with auto-discovery)
5. **check-scannability** - Analyzes document readability by checking sentence/paragraph length
6. **archive-unused-files** - Finds and optionally archives unreferenced AsciiDoc files
7. **archive-unused-images** - Finds and optionally archives unreferenced image files
8. **format-asciidoc-spacing** [EXPERIMENTAL] - Standardizes AsciiDoc formatting (blank lines after headings and around includes)
9. **convert-callouts-to-deflist** - Converts AsciiDoc callouts to definition lists, bulleted lists, or inline comments (batch mode)
10. **convert-callouts-interactive** - Interactively converts AsciiDoc callouts with per-block format selection

### Core Modules

- `doc_utils/file_utils.py` - Core file scanning, archiving, and exclusion list parsing
- `doc_utils/topic_map_parser.py` - Parse OpenShift-docs style topic map YAML files
- `doc_utils/validate_links.py` - Logic for validating links with URL transposition [EXPERIMENTAL]
- `doc_utils/extract_link_attributes.py` - Logic for extracting link/xref macros into attributes
- `doc_utils/replace_link_attributes.py` - Logic for replacing attributes in link URLs
- `doc_utils/format_asciidoc_spacing.py` - Logic for formatting AsciiDoc spacing [EXPERIMENTAL]
- `doc_utils/unused_attributes.py` - Logic for finding unused AsciiDoc attributes
- `doc_utils/unused_adoc.py` - Logic for finding unused AsciiDoc files (supports both topic maps and master.adoc)
- `doc_utils/unused_images.py` - Logic for finding unused images
- `doc_utils/scannability.py` - Document readability analysis
- `callout_lib/` - Modular library for AsciiDoc callout conversion
  - `detector.py` - Callout detection and extraction
  - `converter_deflist.py` - Definition list converter
  - `converter_bullets.py` - Bulleted list converter
  - `converter_comments.py` - Inline comments converter with length detection

## Installation Preferences

### For Users: Always Recommend pipx
When writing documentation, examples, or user-facing instructions, **always recommend pipx as the primary installation method**:

```bash
# Recommended for users
pipx install rolfedh-doc-utils
pipx upgrade rolfedh-doc-utils
```

**Why pipx:**
- Isolated environment prevents dependency conflicts
- Automatic PATH management
- Cleaner upgrades and uninstalls
- Best practice for CLI tools
- The `detect_install_method()` function in `version_check.py` detects pipx and shows the correct upgrade command

**Only mention pip as alternative:**
- For users who can't install pipx
- For development installations (pip install -e .)
- In troubleshooting sections

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

### Documentation Updates for New Features

When adding a new tool or feature:

1. **Create tool documentation** in `docs/tools/[tool-name].md` with Jekyll front matter:
   ```yaml
   ---
   layout: default
   title: tool-name
   parent: Tools Reference
   nav_order: X
   ---
   ```

2. **Update `docs/tools/index.md`**:
   - Update tool count in description
   - Add tool entry with icon, description, and quick usage
   - Add to help commands list

3. **Update `docs/getting-started.md`**:
   - Add to verify installation section
   - Add usage example section

4. **Update README.md**:
   - Add to tools table with description and usage

5. **Update CLAUDE.md** (this file):
   - Add to CLI Tools list
   - Add to Core Modules if new module created
   - Add to Recent Improvements section
   - Update Project Structure if needed

### Creating a New Release

Follow these exact steps to release a new version:

1. **Update version in `pyproject.toml`**
   ```bash
   # Edit pyproject.toml and change version = "X.Y.Z" to new version
   ```

2. **Update CHANGELOG.md** ⚠️ **IMPORTANT - DO NOT FORGET!**
   ```bash
   # Add new version section with date
   # Format: ## [X.Y.Z] - YYYY-MM-DD
   # Document all changes under appropriate categories:
   #   ### Added - New features
   #   ### Changed - Changes in existing functionality
   #   ### Enhanced - Improvements to existing features
   #   ### Fixed - Bug fixes
   #   ### Documentation - Documentation changes
   #   ### Removed - Removed features
   # Include detailed descriptions with specific changes made
   ```
   **Claude Code Reminder:** Always update CHANGELOG.md when releasing! Check git log since last release to ensure nothing is missed.

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

7. **Monitor GitHub Actions Workflow**
   ```bash
   # Check workflow status
   gh run list --workflow=pypi-publish.yml --limit 1

   # Wait for completion (usually 20-30 seconds)
   sleep 20 && gh run list --workflow=pypi-publish.yml --limit 1
   ```
   - Package will be available at: https://pypi.org/project/rolfedh-doc-utils/
   - GitHub Release should appear at: https://github.com/rolfedh/doc-utils/releases

8. **Verify Release Status**
   ```bash
   # IMPORTANT: First check if GitHub Release already exists
   gh release view vX.Y.Z 2>/dev/null && echo "Release exists" || echo "Release not found"

   # If release doesn't exist (workflow may have failed), create it manually:
   gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "See CHANGELOG.md for details"

   # Verify the release is marked as "Latest"
   gh release list --limit 1

   # Verify PyPI package is available
   pip index versions rolfedh-doc-utils | head -5
   ```

   **Note for Claude:** Always check if the release exists before attempting to create it. The GitHub Actions workflow usually creates the release automatically as of v0.1.9, but if you get a "tag already exists" error, it means the release was already created successfully.

**Example for releasing v0.1.11:**
```bash
# 1. Update pyproject.toml: version = "0.1.11"
# 2. Update CHANGELOG.md: Move unreleased items to ## [0.1.11] - YYYY-MM-DD
# 3. Test
python -m pytest tests/ -v --tb=short
# 4. Commit
git add -A && git commit -am "Prepare release v0.1.11"
# 5. Tag
git tag -a v0.1.11 -m "Release v0.1.11: Brief description"
# 6. Push (this triggers the workflow)
git push origin main --tags

# 7. Wait for workflow to complete
sleep 20 && gh run list --workflow=pypi-publish.yml --limit 1

# 8. Check if release exists before creating
gh release view v0.1.11 2>/dev/null
if [ $? -ne 0 ]; then
    # Only create if it doesn't exist
    gh release create v0.1.11 --title "Release v0.1.11" --notes "See CHANGELOG.md"
fi

# 9. Verify the release
gh release list --limit 1  # Should show v0.1.11 with "Latest" label
pip index versions rolfedh-doc-utils | head -3  # Should show v0.1.11 as latest
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

### Release Process Issues

#### GitHub Release Creation Fails (403 Error)
**Problem:** The GitHub Actions workflow fails at the "Create GitHub Release" step with a 403 (Forbidden) error, but PyPI publishing succeeds.

**Cause:** The GITHUB_TOKEN permissions are insufficient for the softprops/action-gh-release@v1 action.

**Solution:** Always manually create the GitHub release after the workflow completes:
```bash
# After workflow completes (check with: gh run list --workflow=pypi-publish.yml --limit 1)
gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "Release notes here"
```

**Prevention:** Consider updating the workflow to use the GitHub CLI directly or adjusting token permissions in repository settings.

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

### Callout Conversion Utilities (In Development)
1. **New Modular Callout Library**: Created `callout_lib/` package with reusable conversion components
   - Shared detector module for finding and extracting callouts from AsciiDoc code blocks
   - **Table parser module** for parsing AsciiDoc tables (supports both callout tables and general table conversion)
   - Detector automatically handles both **list-format** (`<1> text`) and **table-format** callout explanations
   - Support for conditional statements (ifdef/ifndef/endif) in table cells
   - Three converter modules: definition lists, bulleted lists, and inline comments
   - Proper separation of concerns with dataclasses for type safety
2. **New convert-callouts-to-deflist Tool**: Batch conversion utility
   - Converts callouts to three formats: definition lists (default), bulleted lists, or inline comments
   - `--format` option to choose output format
   - `--max-comment-length` parameter (default: 120) for inline comments
   - Automatic fallback to definition list when comments exceed length threshold
   - Comprehensive warning system for long comments and callout mismatches
   - Full exclusion support (--exclude-dir, --exclude-file, --exclude-list)
3. **New convert-callouts-interactive Tool**: Interactive conversion utility
   - Per-code-block format selection with visual preview
   - Color-coded output for better readability
   - Interactive warning prompts for long comments with 4 options:
     - Shorten to first sentence
     - Fall back to definition list
     - Fall back to bulleted list
     - Skip the block
   - "Apply to all" option for batch processing remaining blocks
   - Context-aware display with adjustable context lines
4. **Long Comment Handling**: Smart detection and handling of overly long explanations
   - Automatic length detection in `CommentConverter.check_comment_lengths()`
   - First-sentence extraction with `shorten_comment()` method
   - Batch tool: Automatic fallback with warnings
   - Interactive tool: User choice with preview of long text
5. **Architecture**: Clean separation between batch and interactive workflows
   - Both tools share same `callout_lib` for consistency
   - Different user personas (automated vs editorial)
   - Complementary use cases documented
6. **Documentation**: Comprehensive GitHub Pages documentation
   - Tool comparison guide for choosing between batch/interactive
   - Cross-references between related tools
   - Examples for all three output formats
   - Technical details in library README

### Ignored Configuration Attributes (v0.1.18)
1. **AsciiDoc Configuration Attributes**: Enhanced `find-unused-attributes` to ignore processor configuration attributes
   - Added IGNORED_ATTRIBUTES set in `unused_attributes.py`
   - Automatically skips attributes like `:idprefix:`, `:doctype:`, `:experimental:`, `:icons:`, etc.
   - Prevents false positives for attributes that configure AsciiDoc processor behavior
   - Configuration attributes don't appear in content but are essential for correct rendering
   - Documentation updated with examples and warnings about these critical attributes

### Enhanced find-unused-attributes Tool (v0.1.11-dev)
1. **Auto-discovery Feature**: Added automatic attributes file discovery
   - Tool now works without specifying a file: just run `find-unused-attributes`
   - Interactive file selection when multiple attributes files are found
   - Searches for common patterns: `**/attributes.adoc`, `**/*attributes.adoc`, etc.
   - Backward compatible: can still specify file directly
   - Better error handling with helpful messages for missing files

### New validate-links Tool [EXPERIMENTAL] (v0.1.11-dev)
1. **New CLI Tool**: `validate-links` for validating all documentation links
   - **EXPERIMENTAL**: This feature is under active development and may change
   - URL transposition feature for validating against preview/staging environments
   - Concurrent link checking with configurable parallelism
   - Resolves AsciiDoc attributes before validation
   - Validates external URLs, internal xrefs, and image paths
   - Smart caching and retry logic for transient failures
   - Multiple output formats (text, JSON, JUnit planned)
   - `--fail-on-broken` option for CI/CD integration

### New extract-link-attributes Tool (v0.1.10)
1. **New CLI Tool**: `extract-link-attributes` for creating reusable link attributes
   - Extracts link: and xref: macros containing attributes into attribute definitions
   - Handles link text variations with interactive selection
   - Reuses existing attributes on subsequent runs (idempotent)
   - Generates meaningful attribute names from URLs
   - Supports both interactive and non-interactive modes
   - Preserves macro type (link vs xref) in attribute values
   - Dry-run mode for previewing changes

### New replace-link-attributes Tool (v0.1.9)
1. **New CLI Tool**: `replace-link-attributes` for resolving Vale LinkAttribute issues
   - Replaces attribute references in link: and xref: macro URLs with resolved values
   - Preserves link text unchanged
   - Interactive attribute file selection with auto-discovery
   - Supports custom attribute file paths via --attributes-file option
   - Resolves nested attribute references automatically
   - Dry-run mode for previewing changes
2. **Refactored format-asciidoc-spacing**: Now follows project architecture pattern
   - Core logic moved to `doc_utils/format_asciidoc_spacing.py` module
   - CLI script imports from module (separation of concerns)
3. **Documentation Updates**:
   - Added comprehensive documentation to GitHub Pages at `/tools/replace-link-attributes`
   - Updated getting-started guide with new tool examples
   - Fixed Jekyll front matter for proper GitHub Pages rendering

### New AsciiDoc Spacing Formatter [EXPERIMENTAL] (v0.1.6)
1. **New CLI Tool**: `format-asciidoc-spacing` for standardizing AsciiDoc formatting
   - **EXPERIMENTAL**: Formatting rules may evolve based on user feedback
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