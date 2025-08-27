# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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