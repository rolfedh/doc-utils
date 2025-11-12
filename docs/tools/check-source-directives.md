# check-source-directives

Detects code blocks (delimited by `----`) that are missing the `[source]` directive in AsciiDoc files. This helps prevent AsciiDoc-to-DocBook XML conversion errors that commonly occur when code blocks lack proper source directives.

## Installation

```bash
pipx install rolfedh-doc-utils
```

## Usage

### Basic scanning

Scan the current directory for missing source directives:

```bash
check-source-directives
```

Scan a specific directory:

```bash
check-source-directives asciidoc
```

### Auto-fix mode

Automatically insert `[source]` directives where they're missing:

```bash
check-source-directives --fix
```

Fix issues in a specific directory:

```bash
check-source-directives --fix asciidoc
```

## What it detects

The tool flags code blocks like this:

```asciidoc
If you add these properties on the command line, ensure the `"` character is escaped properly:
----
-Dquarkus.log.category.\"org.hibernate\".level=TRACE
----
```

**Fix:** Add `[source]` (or `[source, bash]`, `[source, properties]`, etc.) before the code block:

```asciidoc
If you add these properties on the command line, ensure the `"` character is escaped properly:
[source, bash]
----
-Dquarkus.log.category.\"org.hibernate\".level=TRACE
----
```

## What it ignores (valid patterns)

The tool intelligently skips these valid patterns:

### 1. Code blocks with [source] directive
```asciidoc
[source, java]
----
public class Example {
}
----
```

### 2. Code blocks with [source] and title
```asciidoc
[source, java]
.Example with title
----
public class Example {
}
----
```

### 3. Code blocks after attribute blocks
```asciidoc
[id=example-id]
----
Example content
----
```

### 4. Code blocks after continuation markers
```asciidoc
Some text
+
----
Example
----
```

### 5. Code blocks in admonitions
```asciidoc
NOTE: This is a note
----
Example
----
```

## Output

### Detection mode (default)

```
Scanning for code blocks missing [source] directive in: asciidoc
================================================================

File: asciidoc/logging.adoc
  Line 276: Code block without [source] directive
    Previous line (275): If you add these properties on the command line...

================================================================
Found 1 code block(s) missing [source] directive in 1 file(s)

Run with --fix to automatically fix these issues
```

### Fix mode (--fix)

```
Fixing code blocks missing [source] directive in: asciidoc
================================================================

File: asciidoc/logging.adoc
  Line 276: Code block without [source] directive
    Previous line (275): If you add these properties on the command line...

  ✓ Fixed 1 issue(s)

================================================================
Fixed 1 code block(s) in 1 file(s)
```

## Exit codes

- **0**: No issues found, or all issues successfully fixed
- **1**: Issues found (detection mode only)

## Why this matters

Missing `[source]` directives can cause:

1. **XML conversion errors**: AsciiDoc-to-DocBook XML conversion may fail
2. **Build failures**: Jenkins and other CI systems may reject the documentation
3. **Rendering issues**: Code blocks may not render correctly in final output

Common error message:
```
attributes construct error
```

This typically indicates Javadoc `{@link}` patterns or other content in code blocks without proper `[source]` directives.

## Integration with CI/CD

Add to your CI pipeline to catch missing `[source]` directives:

### GitLab CI
```yaml
check-source-directives:
  script:
    - pipx install rolfedh-doc-utils
    - check-source-directives asciidoc
  allow_failure: false
```

### GitHub Actions
```yaml
- name: Check source directives
  run: |
    pipx install rolfedh-doc-utils
    check-source-directives asciidoc
```

## Recommended workflow

1. **Preview issues first** (recommended):
   ```bash
   check-source-directives asciidoc
   ```

2. **Review the output** to understand what will be changed

3. **Fix automatically**:
   ```bash
   check-source-directives --fix asciidoc
   ```

4. **Review the changes** in your version control system

5. **Refine language specifiers** if needed:
   - Change generic `[source]` to `[source, bash]`, `[source, properties]`, etc.

## Language specifiers

After auto-fixing, you may want to add specific language identifiers:

- **Shell commands**: `[source, bash]`
- **Configuration**: `[source, properties]` or `[source, yaml]`
- **Java code**: `[source, java]`
- **XML**: `[source, xml]`
- **Plain text/output**: `[source, text]`
- **HTTP responses**: `[source, http]`

## False positives

The tool is designed to minimize false positives by checking:
- Whether `[source]` exists in the previous 3 lines
- Whether the previous line is a valid AsciiDoc structural element
- Whether the code block follows standard AsciiDoc patterns

If you encounter a false positive, please report it as an issue on the [doc-utils GitHub repository](https://github.com/rolfedh/doc-utils).

## See also

- [format-asciidoc-spacing](format-asciidoc-spacing.md) - Format AsciiDoc spacing
- [archive-unused-files](archive-unused-files.md) - Find unused AsciiDoc files
- [find-unused-attributes](find-unused-attributes.md) - Find unused attributes
