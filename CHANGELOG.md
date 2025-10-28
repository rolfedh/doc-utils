# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.33] - 2025-10-28

### Fixed
- **Callout detection** - Fixed false positives with Java generics and angle-bracket syntax
  - Removed user-replaceable value extraction from both `detector.py` and `converter_deflist.py`
  - Java generics like `CrudRepository<MyEntity, Integer>` no longer incorrectly extracted
  - Full code lines now preserved in definition list terms
  - Fixes issue where `<MyEntity, Integer>` was extracted instead of the complete code line
- **Callout detection** - Fixed semicolon removal bug in Java/C/C++/JavaScript code
  - Removed semicolon (;) from CALLOUT_WITH_COMMENT regex pattern
  - Semicolons now correctly preserved as statement terminators
  - Example: `Optional<String> name; <1>` now correctly becomes `Optional<String> name;`
  - Semicolon was being treated as comment marker (Lisp-style) causing false removal
- **Interactive tool** - Fixed quit/exit behavior and added explicit quit option
  - Ctrl+C now immediately exits script (was continuing to summary)
  - Added 'Q' (capital) option to quit script entirely at any prompt
  - Clarified 'q' (lowercase) as "Skip current file" instead of ambiguous "Quit"
  - All lowercase options now case-insensitive for better user experience

### Documentation
- **GitHub Pages** - Updated convert-callouts-to-deflist.md to reflect removal of angle-bracket extraction
  - Changed "Intelligent Value Extraction" to "Code Line Extraction" section
  - Updated examples to show full code lines in definition list terms
- **GitHub Pages** - Updated convert-callouts-interactive.md keyboard shortcuts
  - Documented distinction between 'q' (skip file) and 'Q' (quit script)
  - Added Ctrl+C immediate exit behavior
- **CLAUDE.md** - Added pipx installation and upgrade procedures
  - Documented full upgrade procedure with build artifact cleaning
  - Added key phrase "upgrade doc-utils" for Claude automation
  - Explained why cleaning build artifacts is critical before reinstalling

## [0.1.32] - 2025-10-22

### Fixed
- **Version reporting** - Fixed version.py not synced with pyproject.toml
  - Updated doc_utils/version.py from 0.1.30 to match current release
  - Now properly reports v0.1.32 instead of outdated v0.1.30

### Added
- **CLI tools** - Added `--version` option to callout conversion tools
  - `convert-callouts-to-deflist --version` now displays version information
  - `convert-callouts-interactive --version` now displays version information
  - Both tools import version from doc_utils.version for consistency

## [0.1.31] - 2025-10-22

### Added
- **convert-callouts-to-deflist** - Added `--force` option to strip callouts despite warnings
  - Allows conversion to proceed when callout warnings are present (missing explanations or mismatches)
  - Strips callouts from blocks with missing explanations without creating explanation lists
  - Converts blocks with callout mismatches using available explanations
  - Requires confirmation prompt before proceeding (skipped in dry-run mode)
  - Useful for intentionally shared explanations between conditional blocks
  - Documented in warnings report and GitHub Pages with comprehensive examples

- **Warnings Report** - Automatic generation of structured AsciiDoc warnings report
  - Enabled by default, generates `callout-warnings-report.adoc` in current directory
  - Reduces console spam by showing minimal summary: "⚠️ 4 Warning(s) - See callout-warnings-report.adoc for details"
  - Report includes summary by warning type, recommended actions, and force mode documentation
  - Callout mismatch analysis detects duplicates, missing callouts, extra callouts, and off-by-one errors
  - Missing explanations section lists possible causes (shared explanations, unexpected location, missing)
  - Command-line options: `--warnings-report` (default), `--no-warnings-report`, `--warnings-file=<path>`
  - Can be committed to git to track warning resolution progress

- **convert-callouts-to-deflist** - Warning for code blocks with callouts but no explanations
  - Detects when code block has callouts but no explanation table or list found
  - Provides helpful diagnostic message with possible causes
  - Suggests manual review for shared explanations or documentation errors

### Enhanced
- **Table parser** - Improved detection of callout explanations in tables
  - Now handles cell type specifiers without leading pipe (e.g., `a|` at start of line)
  - Accepts both `|cell` and `a|cell` formats for AsciiDoc cell type specifiers
  - Recognizes all cell type specifiers: a, s, h, d, m, e, v
  - Fixed issue where code block closing delimiter (`----`) was incorrectly treated as new code block start
  - Added logic to skip closing delimiter before searching for callout table

- **Table parser** - Support for plain number callouts in tables (in addition to angle-bracket format)
  - Tables can now use plain numbers (1, 2, 3) instead of angle-bracket format (`<1>`, `<2>`, `<3>`)
  - Unified detection via `_is_callout_or_number()` method accepting both formats
  - Increased detection rate: 58% more files detected, 130% more code blocks found
  - Example: First column can be `1` or `<1>`, both are recognized as callout references

- **Validation warnings** - Show duplicate callout numbers in explanations
  - Warnings now preserve duplicates: `[1, 2, 3, 4, 5, 7, 8, 8, 9]` instead of deduplicated `[1, 2, 3, 4, 5, 7, 8, 9]`
  - Added `get_table_callout_numbers()` method to extract raw callout numbers from tables
  - Updated `validate_callouts()` to return lists instead of sets to preserve duplicates
  - Helps identify table rows with incorrect callout numbering

- **User guidance** - Added suggestion messages when warnings occur
  - Console shows: "Suggestion: Review and fix the callout issues listed in [report], then rerun this command."
  - Warnings report includes "Recommended Actions" section with 4-step workflow
  - Clear guidance on when to use force mode and how to review changes

### Fixed
- **CRITICAL** - Preserve content between code block and explanations
  - Fixed bug where converter deleted `endif::` directives, continuation markers (`+`), and paragraph text
  - Now uses `detector.last_table.start_line` to accurately find where explanations begin
  - Preserves slice `new_lines[content_end + 1:explanation_start_line]` containing critical AsciiDoc directives
  - Applies to both comments format and definition list/bullets formats
  - Prevents corruption of conditional compilation blocks in documentation

### Documentation
- **convert-callouts-to-deflist.md** - Documented force mode option
  - Added `--force` option to Options section with "USE WITH CAUTION" warning
  - Added "Force Mode" subsection with confirmation prompt example
  - Documented what force mode does for missing explanations and callout mismatches
  - Included 6-step recommended workflow
  - Provided real-world example of appropriate force mode usage (shared explanations in conditionals)

- **Warnings Report** - Documented warnings report feature
  - Added "Warnings Report File" section explaining enabled-by-default behavior
  - Documented command-line options for controlling report generation
  - Listed benefits: clean console output, structured format, git tracking, AsciiDoc rendering

## [0.1.30] - 2025-10-22

### Fixed
- **convert-callouts-to-deflist/interactive** - Fixed support for AsciiDoc table cells with `a|` type specifier
  - Recognize `a|` on its own line as cell separator with type specifier, not just a cell content marker
  - `a|` now correctly starts a new cell rather than modifying the current cell type
  - Preserve blank lines as content within `a|` (AsciiDoc) cells instead of treating them as row separators
  - Parse `cols` attribute (e.g., `[cols="1,7a"]`) to determine expected number of columns per row
  - Auto-finalize rows when column count is reached, enabling proper multi-row table parsing

- **convert-callouts-to-deflist/interactive** - Fixed handling of conditionals in table cells
  - Keep conditional directives (ifdef::/ifndef::/endif::) inline with cell content instead of extracting to separate lists
  - Insert continuation markers (`+`) before conditionals in definition lists to prevent list breakout
  - Insert continuation markers to bridge blank lines in explanations
  - Prevents invalid AsciiDoc where blank lines would break definition list structure
  - Conditionals within `a|` cells are now preserved correctly across blank lines

### Enhanced
- **Table parser** - Improved conditional handling logic
  - Check if currently building a cell (`current_cell_lines` not empty) when processing conditionals
  - Conditionals are added to cell content when inside a cell, rather than to row-level conditional lists
  - Preserve conditional context across blank lines in `a|` cells

### Technical
- Added `_parse_column_count()` method to extract column count from table `cols` attribute
- Added `_finalize_row_if_complete()` method to auto-finalize rows based on column count
- Updated conditional detection to handle cells being built vs cells already saved
- Tested on Debezium documentation repository (70 files, 12 files with callouts detected, 27 code blocks would convert)

## [0.1.29] - 2025-10-21

### Fixed
- **format-asciidoc-spacing** - Fixed conditional block cohesion to prevent unwanted blank lines
  - Tool no longer inserts blank line between conditional directives (ifdef::/ifndef::/endif::) and their enclosed content
  - Conditional directives and their content now stay "glued" together as a logical unit
  - Prevents breaking block titles that immediately follow conditional directives
  - Example: `ifndef::foo[]` followed by `.Additional resources` no longer gets a blank line inserted between them

- **format-asciidoc-spacing** - Fixed list continuity across conditional blocks
  - Tool no longer inserts blank line after endif:: when next line is a list item
  - Supports all list formats: bulleted (*), dashed (-), dotted (., ..), and numbered (1., 2., etc.)
  - Supports list continuation marker (+)
  - Ensures lists that span conditional blocks remain unbroken

### Enhanced
- **version_check.py** - Updated install method detection to default to pipx
  - Version update notifications now show `pipx upgrade` command by default
  - Improved detection for pipx installations including editable installs
  - Made sys.prefix check case-insensitive for better compatibility
  - Aligns with project guidelines to always recommend pipx as the preferred installation method

### Documentation
- **convert-callouts-to-deflist.md** - Comprehensive documentation improvements
  - Standardized section ordering for consistency with interactive tool documentation
  - Fixed terminology: replaced "two-column" with "multi-column" throughout
  - Restructured overly long examples section for better readability
  - Enhanced Features section with better organization and Smart Comment Handling details
  - Added Technical Details section with links to callout_lib library

- **convert-callouts-interactive.md** - Added missing content and improved organization
  - Added Automatic Format Detection feature section
  - Added Smart Comment Handling feature with interactive warning details
  - Added Validation and Safety feature section
  - Added exclusion examples (--exclude-dir, --exclude-file, --exclude-list)
  - Added missing CLI options to Options section (--max-comment-length, --exclude-file, --exclude-list)
  - Added Technical Details section with library links and supported comment syntax

### Added
- **doc_utils_cli.py** - Added convert-callouts-interactive to help output
  - Tool now appears in `doc-utils --help` and `doc-utils --list` output
  - Updated convert-callouts-to-deflist description to clarify it's batch mode
  - Both callout conversion tools now clearly documented with their use cases

## [0.1.28] - 2025-10-21

### Fixed
- **callout_lib/converter_deflist.py** - Fixed whitespace handling in definition list terms
  - Code lines now have leading and trailing whitespace stripped before wrapping in backticks
  - Previously terms like `` `    'execute-snapshot',` `` would preserve indentation from code blocks
  - Now properly formatted as `` `'execute-snapshot',` `` without extra whitespace

- **callout_lib/converter_bullets.py** - Fixed whitespace handling in bulleted list terms
  - Applied same whitespace stripping fix as definition list converter
  - Ensures consistent clean formatting across all output formats

- **callout_lib/table_parser.py** - Fixed critical table parsing bug with multi-cell header rows
  - Multi-cell lines (e.g., `|Item |Field name |Description`) now properly complete a row
  - Previously, header and first data row would merge into a single 6-cell row
  - Caused first item in 3-column tables to be skipped during extraction
  - Now correctly parses header as separate row, allowing all data rows to be processed

### Changed
- **callout_lib/detector.py** - Updated 3-column table explanation format
  - Changed from verbose "Refers to `value`." pattern to simple label `` `value`: ``
  - More concise and cleaner output while maintaining clarity
  - Format: `` `op`: `` instead of `For `op`:` or `Refers to `op`.`
  - Follows minimal label pattern that clearly identifies field being explained

## [0.1.27] - 2025-10-20

### Fixed
- **convert-callouts-to-deflist** - Fixed bug where table-format callout explanations were not removed when converting to inline comments format
  - Previously, only the callout numbers were converted to comments while the explanation table remained in the document
  - Now properly skips over the entire table when converting to comments format

### Added
- **callout_lib/table_parser.py** - Support for 3-column table format (Item | Value | Description) used in Debezium documentation
  - Added `is_3column_callout_table()` method to detect 3-column callout tables
  - Added `extract_3column_callout_explanations()` method to extract data from 3-column tables
  - Added header row detection with automatic skipping using keyword matching
  - Added inline cell separator parsing for tables with multiple cells on same line (e.g., `|Cell1 |Cell2 |Cell3`)
  - Updated `find_callout_table_after_code_block()` to detect both 2-column and 3-column tables

- **callout_lib/detector.py** - Enhanced to handle 3-column table format
  - Added `_extract_from_3column_table()` method
  - Detection priority: 3-column table → 2-column table → list format
  - Combines value and description columns into meaningful explanations: "Refers to `value`. Description..."

### Testing
- Tested with real Debezium documentation from GitLab repository
- All 153 tests pass with new 3-column table support

### Documentation
- Updated GitHub Pages documentation for both convert-callouts tools with 3-column table examples
- Updated CLAUDE.md to reflect full 3-column table support

## [0.1.26] - 2025-10-20

### Added
- **callout_lib/table_parser.py** - New AsciiDoc table parser module
  - Parses two-column tables with callout numbers and explanations
  - Detects callout explanation tables automatically with `is_callout_table()` method
  - Extracts callout explanations from table format: `extract_callout_explanations_from_table()`
  - Finds callout tables after code blocks: `find_callout_table_after_code_block()`
  - Converts tables to definition lists: `convert_table_to_deflist()`
  - Converts tables to bulleted lists: `convert_table_to_bullets()`
  - Preserves conditional statements (ifdef/ifndef/endif) within table cells
  - Designed for reusability - supports future utilities for general table conversion
  - Comprehensive test coverage with 15 unit tests

### Enhanced
- **callout_lib/detector.py** - Now supports both list-format and table-format callout explanations
  - Automatically detects callout explanation format (list vs table)
  - Tries table format first, falls back to list format if not found
  - Smart prioritization: list format closer to code block takes precedence over distant tables
  - Prevents false positives by stopping search when encountering list-format explanations
  - Integration tests verify mixed documents with both formats work correctly

- **convert-callouts-to-deflist** and **convert-callouts-interactive** - Transparent table format support
  - Both tools now automatically handle table-format callout explanations
  - No CLI changes required - enhancement is transparent to users
  - Supports conditional statements in table cells (ifdef/ifndef/endif)
  - Converts table callouts to all three output formats: definition lists, bulleted lists, inline comments

### Documentation
- Updated callout_lib/README.md with table parser documentation
  - Added table_parser.py to architecture diagram and module list
  - Documented table parser API with usage examples
  - Explained conditional statement support in tables
  - Noted future use cases for general table conversion utilities
  - Updated version history to v1.1
- Updated CLAUDE.md with table format support in recent improvements section
- Created comprehensive test fixtures with realistic examples based on Debezium documentation patterns

### Testing
- Added tests/test_table_parser.py with 15 tests covering table parsing functionality
- Added tests/test_table_callout_conversion.py with 6 integration tests for end-to-end conversion workflows
- All 153 tests pass (100% success rate)

## [0.1.25] - 2025-10-20

### Added
- **callout_lib** - New modular library for AsciiDoc callout conversion
  - `detector.py` - Shared module for detecting and extracting callouts from code blocks
  - `converter_deflist.py` - Definition list converter module
  - `converter_bullets.py` - Bulleted list converter module
  - `converter_comments.py` - Inline comments converter with language-specific comment syntax
  - Supports 40+ programming languages with automatic comment syntax detection
  - Includes `LongCommentWarning` system for detecting overly long explanations
  - Proper separation of concerns with dataclasses for type safety

- **convert-callouts-interactive** - New interactive callout conversion tool
  - Per-code-block format selection with visual preview
  - Color-coded output for better readability (highlights callouts, shows context)
  - Choose format for each code block individually: definition list, bulleted list, or inline comments
  - Interactive warning prompts for long comments with 4 options:
    - Shorten to first sentence
    - Fall back to definition list format
    - Fall back to bulleted list format
    - Skip the block
  - "Apply to all" option for batch processing remaining blocks
  - Context-aware display with configurable context lines (--context parameter)
  - Full exclusion support (--exclude-dir)
  - Dry-run mode for previewing all changes

- **convert-callouts-to-deflist** - New `--format comments` option for inline comments
  - Converts callouts to inline comments within the code itself
  - Automatically detects programming language from [source,language] attribute
  - Uses appropriate comment syntax: // for Java/C/Go, # for Python/YAML/Bash, <!-- for HTML/XML, etc.
  - Removes separate explanation section entirely
  - New `--max-comment-length` parameter (default: 120 characters)
  - Automatic fallback to definition list when comments exceed length threshold
  - Displays warnings showing which callouts are too long with character counts
  - Best for code examples where explanations are brief and fit naturally as comments

### Enhanced
- **convert-callouts-to-deflist** - Refactored to use new callout_lib modules
  - Core conversion logic now in shared library for code reusability
  - Both batch and interactive tools share same conversion engine
  - Improved code organization with clear separation of concerns
  - More maintainable architecture with modular converters

### Documentation
- Added comprehensive documentation for convert-callouts-interactive tool
- Updated convert-callouts-to-deflist documentation with new comments format
  - Added inline comments format section with examples
  - Added language support details (40+ languages)
  - Updated options and examples
- Added decision guide callouts at top of both tool docs to help users choose the right tool
  - Quick decision matrix: batch vs interactive, automation vs editorial review
  - Cross-references between related tools
- Created callout_lib/README.md with library architecture and usage examples
- Updated CLAUDE.md with callout conversion utilities section
  - Added tools to CLI Tools list
  - Added callout_lib to Core Modules
  - Updated project structure diagram
  - Added detailed "Callout Conversion Utilities" to Recent Improvements

## [0.1.24] - 2025-10-16

### Added
- **convert-callouts-to-deflist** - New `--format` option to choose output format
  - `--format deflist` (default): Definition list with "where:" prefix
  - `--format bullets`: Bulleted list following Red Hat style guide format
  - Bulleted format uses `* \`element\`: explanation` syntax with proper indentation
  - Both formats support all existing features (merged callouts, optional markers, etc.)
  - See: https://redhat-documentation.github.io/supplementary-style-guide/#explain-commands-variables-in-code-blocks

### Enhanced
- **Documentation** - Improved navigation visibility on GitHub Pages
  - All 9 tool pages now visible at top level of navigation (not hidden under collapsed section)
  - Tools grouped together immediately after "Tools Reference" overview page
  - Navigation order: Home → Getting Started → Tools Reference → 9 tool pages → Best Practices → Contributing
  - Better discoverability and user experience

### Documentation
- Added "Output Formats" section with examples of both deflist and bullets formats
- Added guidance on when to use each format
- Updated Options, Best Practices, and Example Workflow sections

## [0.1.23] - 2025-10-16

### Added
- **convert-callouts-to-deflist** - Automatic merging of multiple callouts on same line
  - When multiple callouts appear on one line (e.g., `@BasicAuthentication <1> <2>`), their explanations are now merged
  - Uses AsciiDoc list continuation marker (`+`) to combine related explanations
  - Results in cleaner, more semantic output without duplicate definition list terms
  - Follows AsciiDoc best practices for merging related list items

### Fixed
- **convert-callouts-to-deflist** - Fixed detection of all callouts when multiple appear on one line
  - Previously only detected the last callout, causing warnings like "code has [2, 3, 4], explanations have [1, 2, 3, 4]"
  - Updated regex pattern from `<(\d+)>\s*$` to `<(\d+)>` to match all callouts
  - Modified `extract_callouts_from_code()` to use `finditer()` for finding all matches
  - Enhanced `remove_callouts_from_code()` to strip trailing whitespace after removing multiple callouts

### Enhanced
- **convert-callouts-to-deflist** - Complete refactoring to support callout grouping
  - Added `CalloutGroup` dataclass to group callouts by their source code line
  - Modified `extract_callouts_from_code()` to return `List[CalloutGroup]` instead of `Dict[int, str]`
  - Updated `create_definition_list()` to merge explanations for grouped callouts
  - Updated `validate_callouts()` to work with `CalloutGroup` structure

### Documentation
- Added Example 3 showing multiple callouts being merged with continuation markers
- Added prominent ⚠️ REVIEW CAREFULLY warnings about merged callouts
- Added "Why This Matters" and "When to Review" sections
- Updated Edge Cases, Technical Details, and Processing Algorithm sections
- Clarified Limitations about multi-line explanation support

## [0.1.22] - 2025-10-16

### Added
- **convert-callouts-to-deflist** - New tool for converting AsciiDoc callouts to definition list format
  - Converts code blocks with callout-style annotations (`<1>`, `<2>`, etc.) to cleaner definition list format
  - Uses "where:" prefix for semantic clarity
  - Automatically extracts user-replaceable values from code (e.g., `<my-secret>`)
  - Falls back to using actual code lines when no replaceable values found
  - Validates that callout numbers in code match explanation numbers
  - Supports optional markers ("Optional." or "(Optional)")
  - Handles non-sequential callout numbers
  - Preserves legitimate angle brackets (Java generics, heredoc syntax)
  - Processes all `.adoc` files recursively by default
  - Supports exclusion lists for directories and files
  - Dry-run mode for previewing changes
  - Displays warnings for callout mismatches with file and line numbers
  - Automatically excludes `.vale` directory by default

### Documentation
- Added comprehensive documentation for convert-callouts-to-deflist tool
- Includes transformation examples, usage patterns, and edge cases
- Updated Tools Reference index with new tool

## [0.1.21] - 2025-10-13

### Enhanced
- **format-asciidoc-spacing** - Now adds blank lines between consecutive includes within conditional blocks
  - Previously, includes inside `ifdef::`/`ifndef::` blocks were left untouched
  - Now adds visual separation between includes enclosed in conditionals
  - Improves readability and maintains consistency with non-conditional includes
  - Example: Consecutive includes in `ifdef::openshift-rosa[]` blocks now have blank lines between them

### Changed
- **Documentation** - Removed `[EXPERIMENTAL]` tags from tools now considered stable
  - `validate-links` - No longer marked as experimental
  - `format-asciidoc-spacing` - No longer marked as experimental
  - Updated all documentation, README, and CLI help text

### Fixed
- **GitHub Pages** - Navigation now keeps "Tools Reference" section expanded by default
  - Added `nav_fold: false` configuration for better user experience
  - All 8 tools visible in left navigation without clicking to expand

## [0.1.20] - 2025-10-13

### Added
- **New `doc-utils` command** - Main CLI hub for discovering and accessing all tools
  - `doc-utils --help` shows comprehensive help with all tools listed
  - `doc-utils --list` displays quick list of available tools
  - `doc-utils --version` shows package version
  - Provides single entry point for users to discover functionality
- **Version flag support** - All 8 CLI tools now support `--version` flag
  - Centralized version management in `doc_utils/version.py`
  - Version synchronized with `pyproject.toml`
  - Example: `find-unused-attributes --version` → `find-unused-attributes 0.1.20`

### Enhanced
- **Smart upgrade notifications** - Update notifications now detect installation method
  - Automatically detects whether package was installed with `pipx` or `pip`
  - Recommends appropriate upgrade command (`pipx upgrade` or `pip install --upgrade`)
  - Respects user's chosen installation method
  - Detection checks `sys.prefix` and `PIPX_HOME` environment variable

### Added
- **Test coverage** - Added 12 new tests for version checking functionality
  - Tests for installation method detection
  - Tests for version parsing and comparison
  - Tests for notification display logic
  - Total test count increased from 120 to 132 tests (100% passing)

## [0.1.19] - 2025-10-09

### Enhanced
- **format-asciidoc-spacing** - Significant improvements to spacing logic based on modular-docs templates
  - Now adds blank lines between consecutive include statements for better visual separation
  - Comments preceding includes stay together as a logical unit (no blank line between comment and include)
  - Comments preceding conditional blocks (ifdef/ifndef) stay together without intervening blank lines
  - Added support for comment block spacing (blank line after closing `////` delimiter)
  - Added support for block title spacing (blank line before `.Title` blocks like `.Prerequisites`)
  - Role blocks (`[role="..."]`) are now recognized and handled appropriately
  - Improved handling of heading spacing (no blank line added when followed by comment block)
  - All spacing rules now align with Red Hat modular documentation templates

### Fixed
- **format-asciidoc-spacing** - Fixed edge cases in spacing logic
  - Standalone comments and attributes now handled correctly
  - Block titles no longer add extra spacing when preceded by role blocks
  - Better detection of logical groupings (comment+include, comment+conditional)

## [0.1.18] - 2025-10-08

### Added
- Initial release tracking (version sync fix)

## [0.1.17] - 2025-10-08

### Fixed
- **find-unused-attributes** - Fixed critical bug where conditional attributes were misidentified as unused
  - Now detects attributes used in `ifdef::attr[]`, `ifndef::attr[]`, and `endif::attr[]` directives
  - Previously only detected `{attribute}` text substitution references
  - Fixes false positives for conditional attributes like `:rh-only:`, `:downstream:`, `:no-*:`
  - Reduces incorrect "unused" reports by correctly identifying attributes used for conditional content inclusion/exclusion

### Added
- **find-unused-attributes** - New `--comment-out` option to safely mark unused attributes
  - Comments out unused attributes with `// Unused` prefix instead of deleting them
  - Interactive confirmation prompt before modifying files
  - Preserves all formatting, comments, and blank lines
  - Non-destructive approach allows easy restoration by removing comment prefix
  - Git-friendly workflow for managing attribute cleanup

### Enhanced
- Added comprehensive test coverage for conditional directive detection (5 new tests)
- Added test coverage for comment-out functionality (3 new tests)
- Updated documentation with examples for both conditional directives and comment-out feature
- All 120 tests pass

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