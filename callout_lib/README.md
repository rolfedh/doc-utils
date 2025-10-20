# Callout Library

Shared Python library for AsciiDoc callout conversion utilities.

## Overview

This library provides modular, reusable components for detecting and converting AsciiDoc callouts to various formats. It serves as the foundation for both batch and interactive conversion tools.

## Architecture

```
callout_lib/
├── __init__.py              # Package exports
├── detector.py              # Callout detection and extraction
├── converter_deflist.py     # Definition list converter
├── converter_bullets.py     # Bulleted list converter
└── converter_comments.py    # Inline comments converter
```

## Modules

### detector.py

**Purpose:** Detect code blocks with callouts and extract callout information from AsciiDoc files.

**Key Classes:**

- `Callout` - Represents a callout with its number, explanation text, and optional flag
- `CalloutGroup` - Represents one or more callouts sharing the same code line
- `CodeBlock` - Represents a code block with content and metadata
- `CalloutDetector` - Main detector class with methods for finding and extracting callouts

**Key Methods:**

```python
detector = CalloutDetector()

# Find all code blocks in a document
blocks = detector.find_code_blocks(lines)

# Extract callout groups from code block content
callout_groups = detector.extract_callouts_from_code(block.content)

# Extract callout explanations following a code block
explanations, end_line = detector.extract_callout_explanations(lines, block.end_line)

# Remove callout markers from code
cleaned_content = detector.remove_callouts_from_code(block.content)

# Validate callouts match between code and explanations
is_valid, code_nums, explanation_nums = detector.validate_callouts(callout_groups, explanations)
```

### converter_deflist.py

**Purpose:** Convert callouts to AsciiDoc definition list format with "where:" prefix.

**Usage:**

```python
from callout_lib import DefListConverter

output = DefListConverter.convert(callout_groups, explanations)
```

**Output Format:**

```asciidoc
where:

`<my-value>`::
Explanation text

`<another-value>`::
More explanation text
```

### converter_bullets.py

**Purpose:** Convert callouts to bulleted list format following Red Hat style guide.

**Usage:**

```python
from callout_lib import BulletListConverter

output = BulletListConverter.convert(callout_groups, explanations)
```

**Output Format:**

```asciidoc
*   `<my-value>`: Explanation text

*   `<another-value>`: More explanation text
```

### converter_comments.py

**Purpose:** Convert callouts to inline comments within code blocks.

**Usage:**

```python
from callout_lib import CommentConverter

# Convert with language detection
converted = CommentConverter.convert(code_content, callout_groups, explanations, language='java')
```

**Output Format:**

```java
public class Example {
    private String value; // This is the value field
    public void method() { // Main method implementation
        // ...
    }
}
```

**Supported Languages:**

The converter automatically detects comment syntax for 40+ languages:
- C-style (`//`): Java, JavaScript, TypeScript, C, C++, Go, Rust, Swift, Kotlin, etc.
- Hash (`#`): Python, Ruby, Bash, YAML, Shell, etc.
- SQL (`--`): SQL, PL/SQL, T-SQL, Lua
- HTML/XML (`<!--`): HTML, XML, SVG
- Others: Lisp (`;`), MATLAB/LaTeX (`%`), etc.

## Usage Examples

### Basic Conversion Workflow

```python
from callout_lib import CalloutDetector, DefListConverter

# Initialize detector
detector = CalloutDetector()

# Read file
with open('myfile.adoc', 'r') as f:
    lines = [line.rstrip('\n') for line in f]

# Find code blocks
blocks = detector.find_code_blocks(lines)

for block in blocks:
    # Extract callouts from code
    callout_groups = detector.extract_callouts_from_code(block.content)

    if not callout_groups:
        continue

    # Extract explanations
    explanations, end_line = detector.extract_callout_explanations(lines, block.end_line)

    # Validate
    is_valid, _, _ = detector.validate_callouts(callout_groups, explanations)

    if is_valid:
        # Convert to definition list
        output = DefListConverter.convert(callout_groups, explanations)

        # Replace in document
        # ... (implementation-specific)
```

### Using Different Converters

```python
from callout_lib import (
    CalloutDetector,
    DefListConverter,
    BulletListConverter,
    CommentConverter
)

detector = CalloutDetector()

# ... extract callout_groups and explanations ...

# Choose converter based on user preference
if format_choice == 'deflist':
    output = DefListConverter.convert(callout_groups, explanations)
elif format_choice == 'bullets':
    output = BulletListConverter.convert(callout_groups, explanations)
elif format_choice == 'comments':
    # For comments, we need the original code content and language
    output = CommentConverter.convert(
        code_content=block.content,
        callout_groups=callout_groups,
        explanations=explanations,
        language=block.language
    )
```

### Custom Language Comment Syntax

```python
from callout_lib import CommentConverter

# Get comment syntax for a language
opening, closing = CommentConverter.get_comment_syntax('java')
# Returns: ('//', '')

opening, closing = CommentConverter.get_comment_syntax('html')
# Returns: ('<!--', '-->')

# Format a comment manually
comment = CommentConverter.format_comment('This is a comment', opening, closing)
# For Java: '// This is a comment'
# For HTML: '<!-- This is a comment -->'
```

## Data Classes

### Callout

```python
@dataclass
class Callout:
    number: int              # Callout number (e.g., 1, 2, 3)
    lines: List[str]         # Explanation text lines
    is_optional: bool        # Whether marked as optional
```

### CalloutGroup

```python
@dataclass
class CalloutGroup:
    code_line: str                # Code line or user-replaceable value
    callout_numbers: List[int]    # Callout numbers on this line
```

When multiple callouts appear on the same code line, they are grouped together. For example:

```java
@BasicAuthentication <1> <2>
```

Creates a single `CalloutGroup` with `callout_numbers=[1, 2]`.

### CodeBlock

```python
@dataclass
class CodeBlock:
    start_line: int          # Starting line number in document
    end_line: int            # Ending line number in document
    delimiter: str           # '----' or '....'
    content: List[str]       # Code block content lines
    language: Optional[str]  # Language identifier (e.g., 'java', 'yaml')
```

## Pattern Matching

The library uses these regex patterns:

- **Code block start:** `^\[source(?:,\s*(\w+))?(?:[,\s]+[^\]]+)?\]`
- **Callout in code:** `<(\d+)>`
- **Callout explanation:** `^<(\d+)>\s+(.+)$`
- **User-replaceable value:** `(?<!<)<([a-zA-Z][^>]*)>` (excludes heredoc `<<`)

## Design Principles

1. **Separation of Concerns** - Detection logic is separate from conversion logic
2. **Reusability** - All converters use the same detector and data classes
3. **Single Responsibility** - Each converter handles one output format
4. **Immutability** - Converters are stateless static methods
5. **Type Safety** - Uses dataclasses and type hints throughout

## Extending the Library

### Adding a New Converter

To add a new conversion format:

1. Create a new file `converter_myformat.py`
2. Implement a static `convert()` method that accepts `callout_groups` and `explanations`
3. Return a `List[str]` representing the converted output
4. Export the converter in `__init__.py`

Example:

```python
# converter_myformat.py
from typing import List, Dict
from .detector import CalloutGroup, Callout

class MyFormatConverter:
    """Converts callouts to my custom format."""

    @staticmethod
    def convert(callout_groups: List[CalloutGroup],
                explanations: Dict[int, Callout]) -> List[str]:
        lines = []

        for group in callout_groups:
            # Process each callout group
            for callout_num in group.callout_numbers:
                explanation = explanations[callout_num]
                # Format according to your needs
                lines.append(f"Custom format: {group.code_line}")
                lines.extend(explanation.lines)

        return lines
```

## Testing

The library is tested via the parent utilities:

```bash
# Test with sample AsciiDoc files
cd /home/rdlugyhe/doc-utils
python3 convert_callouts_to_deflist.py --dry-run --verbose test_file.adoc

# Test each format
python3 convert_callouts_to_deflist.py --format deflist test_file.adoc
python3 convert_callouts_to_deflist.py --format bullets test_file.adoc
python3 convert_callouts_to_deflist.py --format comments test_file.adoc

# Test interactive mode
python3 convert_callouts_interactive.py test_file.adoc
```

## Version History

- **v1.0** - Initial release with three converters (deflist, bullets, comments)

## License

Same as parent doc-utils project.
