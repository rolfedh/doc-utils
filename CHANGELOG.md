# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.16] - 2025-10-07

### Added
- **Automatic update notifications** - All CLI tools now check for updates on PyPI
  - Non-blocking check that won't interfere with tool operation
  - Shows notification when a newer version is available
  - Caches check results for 24 hours to minimize network requests
  - Can be disabled with `DOC_UTILS_NO_VERSION_CHECK=1` environment variable
  - Automatically skipped in CI environments or non-terminal contexts

### Enhanced
- Added `version_check.py` module with intelligent caching and error handling
- Update notifications use stderr to avoid interfering with tool output

## [0.1.15] - 2025-10-07

### Fixed
- **extract-link-attributes** - Fixed critical bug where attributes files would become self-referencing
  - Previously, the tool would replace attribute values with self-references (e.g., `:link-foo: {link-foo}`)
  - Now automatically excludes ALL attributes files from being scanned/modified
  - Shows which attributes files are being excluded when multiple exist
  - Prevents any attributes file from having its link/xref macros replaced

- **replace-link-attributes** - Enhanced to exclude ALL attributes files from processing
  - Previously only excluded the selected attributes file
  - Now excludes all discovered attributes files to prevent unwanted modifications
  - Shows exclusion list when multiple attributes files exist
  - Ensures attributes files are treated as definition files, not content files

### Enhanced
- Both tools now follow consistent safety principles for handling attributes files
- Improved user feedback showing which files are being excluded from processing

## [0.1.14] - 2025-10-06

### Added
- **Macro type filtering** - Both `extract-link-attributes` and `replace-link-attributes` now support `--macro-type` option
  - New `--macro-type {link,xref,both}` option to limit operations to specific macro types
  - Process only `link:` macros with `--macro-type link`
  - Process only `xref:` macros with `--macro-type xref`
  - Process both (default) with `--macro-type both`
  - Useful when you need to handle external links vs internal cross-references differently

### Enhanced
- Added comprehensive test coverage for macro type filtering
  - New tests for `find_link_macros()` with macro_type parameter
  - New tests for `replace_link_attributes_in_file()` with macro_type parameter
  - All 112 tests passing

### Documentation
- Updated GitHub Pages documentation for both tools with macro type filtering examples
- Added usage examples for `--macro-type` option

## [0.1.13] - 2025-09-29

### Enhanced
- **extract-link-attributes** - Now replaces link macros with existing attribute references
  - Previously only created new attributes and skipped existing ones
  - Now replaces link macros even when matching attributes already exist
  - Useful for cleaning up existing documentation
  - Provides clear feedback on created vs reused attributes
  - Makes the tool more useful for ongoing maintenance

## [0.1.12] - 2025-09-26

### Added
- Link validation feature for `extract-link-attributes` tool
  - New `--validate-links` option to validate URLs in link-* attributes before extraction
  - New `--fail-on-broken` option to exit if broken links are found
  - Validates both existing link attributes and newly created attributes
  - Reports broken links with line numbers for easy fixing
  - Useful for CI/CD pipelines to ensure link quality

- Visual progress indicators (spinners) for all tools
  - Added animated spinners to show progress during long operations
  - Provides better user feedback when processing many files
  - Thread-based implementation for smooth performance
  - Shows success/failure indicators when operations complete

### Enhanced
- `find-unused-attributes` auto-discovery improvements
  - Better error messages for troubleshooting
  - Clearer output when no attributes files are found

### Fixed
- Improved error handling across all tools
- Fixed display issues with spinner output clearing
- Replaced "abort/aborting" terminology with "exit/stopping" throughout codebase

### Documentation
- Added comprehensive documentation for link validation feature
- Updated GitHub Pages with validation examples
- Enhanced CI/CD integration examples with validation flags

## [0.1.11] - 2025-09-26

### Added
- New `validate-links` tool [EXPERIMENTAL] for validating all documentation links
  - URL transposition feature for validating against preview/staging environments
  - Format: `--transpose "https://prod.com--https://preview.com"`
  - Concurrent link checking with configurable parallelism
  - Resolves AsciiDoc attributes before validation
  - Validates external URLs, internal xrefs, and image paths
  - Smart caching and retry logic for transient failures
  - Multiple output formats (text, JSON, JUnit planned)
  - `--fail-on-broken` option for CI/CD integration
  - Marked as EXPERIMENTAL - interface and behavior may change

### Enhanced
- `find-unused-attributes` tool now includes auto-discovery feature
  - Can run without specifying file: just use `find-unused-attributes`
  - Interactive file selection when multiple attributes files are found
  - Searches for common patterns: `**/attributes.adoc`, `**/*attributes.adoc`, etc.
  - Backward compatible: can still specify file directly
  - Better error handling with helpful messages for missing files
  - Consistent with `replace-link-attributes` discovery behavior

- `format-asciidoc-spacing` tool marked as [EXPERIMENTAL]
  - Added experimental warning to documentation
  - Formatting rules may evolve based on user feedback

### Fixed
- Improved error handling in `find-unused-attributes` for missing or invalid files
  - Now provides clear error messages instead of Python tracebacks
  - Validates file existence and permissions before processing

### Documentation
- Added comprehensive documentation for `validate-links` tool
- Updated `find-unused-attributes` documentation with auto-discovery examples
- Marked experimental features clearly in all documentation
- Updated release process in CLAUDE.md to avoid duplicate GitHub release errors

## [0.1.10] - 2025-09-26

### Added
- New `extract-link-attributes` tool for creating reusable link attribute definitions
  - Extracts link: and xref: macros containing attributes into attribute definitions
  - Handles link text variations with interactive selection mode
  - Reuses existing attributes on subsequent runs (idempotent operation)
  - Generates meaningful attribute names from URLs
  - Supports both interactive and non-interactive modes
  - Preserves macro type (link vs xref) in attribute values
  - Automatically discovers attribute files or allows custom specification
  - Dry-run mode to preview changes before applying
  - Replaces original macros with attribute references throughout documentation
  - Complementary tool to `replace-link-attributes` for complete link management workflow

### Documentation
- Added comprehensive documentation for `extract-link-attributes` tool
- Updated all documentation to include the new tool
- Enhanced tool descriptions and usage examples

## [0.1.9] - 2025-09-25

### Added
- New `replace-link-attributes` tool for resolving Vale AsciiDocDITA LinkAttribute issues
  - Replaces attribute references in link: and xref: macro URLs with their resolved values
  - Preserves link text unchanged (only modifies URLs)
  - Automatically discovers all attributes.adoc files in repository
  - Interactive mode for selecting or specifying custom attribute files
  - Supports any attribute file name/path via --attributes-file option
  - Resolves nested attribute references automatically
  - Dry-run mode to preview changes before applying
  - Helps fix Vale LinkAttribute rule: "DITA 1.3 does not allow references to reusable content in link URLs"

### Changed
- Refactored `format-asciidoc-spacing` to follow project architecture pattern
  - Core logic moved to `doc_utils/format_asciidoc_spacing.py` module
  - CLI script now imports from module (separation of concerns)

## [0.1.8] - 2025-09-19

### Documentation
- Added pipx upgrade instructions to README.md and getting-started.md
- Fixed incorrect Python file name references in documentation
- Improved release procedure in CLAUDE.md with better error handling and recovery steps
- Enhanced documentation based on user feedback

## [0.1.7] - 2025-09-11

### Enhanced
- Major improvements to `format-asciidoc-spacing` tool:
  - Special handling for attribute includes near H1 headings (e.g., common-attributes.adoc)
  - Ignores admonition block delimiters (====, ----, ...., ____) instead of treating them as headings
  - Keeps comments directly above includes together as a unit with the include
  - Keeps attributes directly above includes together as a unit with the include
  - Treats conditional blocks (ifdef/ifndef/endif) as single units with proper spacing
  - Consolidates multiple consecutive blank lines that would be inserted into a single blank line
  - Improved detection of headings (requires space after = signs)

### Changed
- Cleaned up repository structure by archiving duplicate documentation files from root directory
- Documentation for tools now centralized in `/docs/tools/` for GitHub Pages site

## [0.1.6] - 2025-09-10

### Added
- New `format-asciidoc-spacing` tool for standardizing AsciiDoc formatting
  - Ensures blank lines after headings (=, ==, ===, etc.)
  - Adds blank lines around include:: directives
  - Supports dry-run mode to preview changes
  - Verbose mode for detailed change tracking
  - Processes single files or entire directories recursively
  - Implemented in Python with no external dependencies

## [0.1.5] - 2025-08-27

### Added
- Automatic directory discovery for `archive-unused-files` tool
  - Recursively finds all `modules` and `assemblies` directories containing `.adoc` files
  - Works with any repository structure (nested, multiple locations, etc.)
  - New `--scan-dir` option to override auto-discovery with specific directories
  - Shows discovered directories in output for transparency

### Changed
- `archive-unused-files` no longer requires hardcoded directory paths
  - Previously required `./modules` and `./assemblies` at root level
  - Now works from any repository root regardless of structure
  - Backwards compatible: `--scan-dir` option allows specifying custom paths

## [0.1.4] - 2025-08-27

### Added
- Safety warnings displayed when running archive utilities
- Post-installation message reminding users about safety practices
- Comprehensive tests for symlink handling

### Fixed
- Fixed infinite loop/freeze when `archive-unused-files` encounters circular symbolic links
  - Replaced recursive glob with os.walk that explicitly skips symlink directories
  - Prevents freezing when repositories contain circular symlinks (e.g., in .archive directories)

## [0.1.3] - 2025-08-01

### Added
- Support for OpenShift-docs style repositories that use topic maps instead of master.adoc files
- New `topic_map_parser.py` module for parsing `_topic_maps/*.yml` files
- Automatic repository type detection (topic maps vs traditional master.adoc)
- PyYAML dependency for parsing topic map YAML files
- 9 new tests for topic map parsing functionality

### Changed
- `archive-unused-files` tool now works with both OpenShift-docs and traditional AsciiDoc repositories
- Updated documentation to explain dual repository type support
- Improved installation instructions to include pipx and --user options

## [0.1.2] - 2025-08-01

### Added
- Comprehensive test coverage for core functionality
  - Added 14 tests for `file_utils.py` covering file collection and archiving
  - Added 15 tests for CLI entry points
  - Added 3 tests for exclusion list parsing
  - Total test coverage increased to 47 tests with 100% pass rate
- New `parse_exclude_list_file()` function in `file_utils.py` for centralized exclusion list parsing
- Exclusion support (--exclude-dir, --exclude-file, --exclude-list) added to `check-scannability` tool
- `CLAUDE.md` file for AI assistant context and development guidelines

### Changed
- Refactored exclusion list parsing to eliminate code duplication across CLI tools
- Improved module import handling with `py-modules` configuration in `pyproject.toml`
- Moved test fixtures from root directory to `tests/` directory for better organization
- Updated README.md with:
  - Development installation instructions
  - Comprehensive troubleshooting section for ModuleNotFoundError
  - Directory/file exclusion documentation

### Fixed
- Fixed ModuleNotFoundError when running CLI commands without proper installation
- Fixed substring matching issues in tests that were causing false failures
- Corrected test expectations for check-scannability output behavior

### Removed
- Removed unused `re` import from `file_utils.py`
- Removed legacy test runner files (`test_run_*.py`)
- Removed obsolete `fixtures-README-legacy.txt`

## [0.1.0] - Previous release
- Initial release with basic functionality