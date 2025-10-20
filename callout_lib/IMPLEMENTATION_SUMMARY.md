# Callout Conversion Implementation Summary

## Overview

This document summarizes the implementation of a modular callout conversion system for AsciiDoc documentation, consisting of a shared library and two specialized utilities.

## Architecture

### Component Structure

```
doc-utils/
├── callout_lib/                           # Shared conversion library
│   ├── __init__.py                        # Package exports
│   ├── README.md                          # Library documentation
│   ├── detector.py                        # Callout detection engine
│   ├── converter_deflist.py              # Definition list converter
│   ├── converter_bullets.py              # Bulleted list converter
│   └── converter_comments.py             # Inline comments converter
│
├── convert_callouts_to_deflist.py        # Batch conversion utility
├── convert_callouts_interactive.py       # Interactive conversion utility
│
└── docs/tools/                            # GitHub Pages documentation
    ├── convert-callouts-to-deflist.md
    └── convert-callouts-interactive.md
```

## Implemented Features

### 1. Shared Library (`callout_lib/`)

#### Core Components

**detector.py** - Callout detection and extraction
- `CalloutDetector` class with methods for:
  - Finding code blocks in AsciiDoc files
  - Extracting callouts from code content
  - Extracting callout explanations
  - Validating callout number consistency
  - Removing callout markers from code

- Data classes:
  - `Callout` - Represents a callout with number, text, and optional flag
  - `CalloutGroup` - Groups multiple callouts on the same line
  - `CodeBlock` - Represents a code block with metadata

**converter_deflist.py** - Definition list conversion
- Converts callouts to AsciiDoc definition lists with "where:" prefix
- Handles user-replaceable values in angle brackets
- Merges multiple callouts on same line using `+` continuation
- Preserves optional markers

**converter_bullets.py** - Bulleted list conversion
- Converts to Red Hat style guide format
- Uses `*` bullets with proper indentation
- Supports multi-line explanations
- Preserves optional markers

**converter_comments.py** - Inline comments conversion
- Replaces callouts with inline comments in code
- Automatic language detection (40+ languages supported)
- Language-specific comment syntax:
  - `//` for Java, JavaScript, C, Go, etc.
  - `#` for Python, Ruby, YAML, Bash, etc.
  - `--` for SQL, Lua
  - `<!--` for HTML, XML
- Removes separate explanation sections

### 2. Batch Utility (`convert_callouts_to_deflist.py`)

**Purpose:** Non-interactive batch conversion with single target format

**Key Features:**
- Process entire directories recursively
- Three output formats via `--format` option:
  - `deflist` - Definition list (default)
  - `bullets` - Bulleted list
  - `comments` - Inline comments
- Dry-run mode for previewing changes
- Verbose logging
- File/directory exclusion support
- Warning collection and summary
- Validates callout consistency

**Usage Examples:**
```bash
# Process with default format
convert-callouts-to-deflist modules/

# Use specific format
convert-callouts-to-deflist --format bullets yaml-files/
convert-callouts-to-deflist --format comments code-examples/

# Preview changes
convert-callouts-to-deflist --dry-run --verbose
```

### 3. Interactive Utility (`convert_callouts_interactive.py`)

**Purpose:** Per-code-block interactive conversion with format choice

**Key Features:**
- Visual preview of each code block with context
- Color-coded output for better readability
- Per-block format selection:
  - Definition list
  - Bulleted list
  - Inline comments
  - Skip
- "Apply to all" option for batch processing remaining blocks
- Rich context display with configurable lines
- Progress tracking
- Validation and warnings
- Dry-run mode

**Interactive Workflow:**
1. Shows code block preview with file location and context
2. Highlights lines containing callouts
3. Displays callout explanations
4. Prompts for conversion choice
5. Confirms and moves to next block
6. Provides summary at completion

**Usage Examples:**
```bash
# Interactive conversion
convert-callouts-interactive modules/security/

# With more context
convert-callouts-interactive --context 5 myfile.adoc

# Preview mode
convert-callouts-interactive --dry-run modules/
```

## Design Principles

### 1. Separation of Concerns
- **Detection logic** (detector.py) is independent of conversion logic
- Each **converter** handles one output format
- **Utilities** orchestrate the workflow without reimplementing core logic

### 2. Code Reusability
- Both utilities use the same shared library
- No code duplication between batch and interactive modes
- Converters are pure functions (stateless)

### 3. Single Responsibility
- `detector.py` - Only detects and validates
- `converter_*.py` - Only converts to specific format
- Utilities - Only handle file I/O and user interaction

### 4. Extensibility
- Adding new formats requires only creating a new converter module
- No changes needed to detection logic or existing converters
- Clear interfaces using dataclasses and type hints

## Conversion Format Examples

### Input (Traditional Callouts)
```asciidoc
[source,yaml]
----
name: <my-secret> <1>
key: <my-key> <2>
----
<1> The secret name
<2> Optional. The secret key value
```

### Output: Definition List Format
```asciidoc
[source,yaml]
----
name: <my-secret>
key: <my-key>
----

where:

`<my-secret>`::
The secret name

`<my-key>`::
Optional. The secret key value
```

### Output: Bulleted List Format
```asciidoc
[source,yaml]
----
name: <my-secret>
key: <my-key>
----

*   `<my-secret>`: The secret name

*   `<my-key>`: Optional. The secret key value
```

### Output: Inline Comments Format
```asciidoc
[source,yaml]
----
name: <my-secret> # The secret name
key: <my-key> # Optional: The secret key value
----
```

## Use Case Recommendations

### Use Batch Utility When:
- Converting entire documentation sets
- Enforcing consistent format across all files
- Automating in CI/CD pipelines
- Processing hundreds of files
- Speed is priority over per-block control

### Use Interactive Utility When:
- Different blocks need different formats
- Editorial decisions required per block
- Selective modernization of docs
- Reviewing conversions before applying
- Mixed content types in same file

## Testing Results

All three conversion formats tested successfully:
- ✅ Definition list conversion
- ✅ Bulleted list conversion
- ✅ Inline comments conversion
- ✅ Multiple callouts on same line (merged)
- ✅ Optional marker preservation
- ✅ Language-specific comment syntax
- ✅ Callout validation and warnings

## Documentation

### GitHub Pages Documentation
- Updated `docs/tools/convert-callouts-to-deflist.md` with new `comments` format
- Created `docs/tools/convert-callouts-interactive.md` for interactive utility
- Includes examples, use cases, and workflow guidance

### Library Documentation
- Created `callout_lib/README.md` with:
  - Architecture overview
  - Module documentation
  - Usage examples
  - Extension guidelines

## File Summary

**Created Files:**
- `callout_lib/__init__.py` - Package initialization
- `callout_lib/detector.py` - Detection engine (230 lines)
- `callout_lib/converter_deflist.py` - Definition list converter (82 lines)
- `callout_lib/converter_bullets.py` - Bulleted list converter (102 lines)
- `callout_lib/converter_comments.py` - Comments converter (178 lines)
- `callout_lib/README.md` - Library documentation
- `convert_callouts_interactive.py` - Interactive utility (490 lines)
- `docs/tools/convert-callouts-interactive.md` - Interactive utility docs

**Modified Files:**
- `convert_callouts_to_deflist.py` - Refactored to use library, added `comments` format
- `docs/tools/convert-callouts-to-deflist.md` - Added `comments` format documentation

**Total Lines of Code:** ~1,500 lines (including documentation)

## Benefits Achieved

1. **Modularity** - Clean separation between detection and conversion
2. **Maintainability** - Single source of truth for core logic
3. **Flexibility** - Three output formats, two workflow modes
4. **Extensibility** - Easy to add new converters
5. **User Choice** - Batch mode for speed, interactive for control
6. **Code Quality** - Type hints, dataclasses, comprehensive docs
7. **Testing** - Verified with real AsciiDoc examples

## Future Enhancements

Potential additions:
- Unit tests for each converter module
- Configuration file support for format preferences
- Custom comment syntax mapping
- Undo/redo in interactive mode
- Diff preview before saving
- Integration with other doc-utils workflows
