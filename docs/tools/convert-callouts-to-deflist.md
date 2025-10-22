---
layout: default
title: convert-callouts-to-deflist
nav_order: 12
---

# Convert Callouts to Definition Lists

Converts AsciiDoc code blocks with callout-style annotations to a cleaner definition list format with "where:" prefix.

{: .note }
> **Choosing the Right Tool**
>
> This is the **batch conversion** tool - it processes all code blocks with a single target format. Use this when you want consistent formatting across all files or need to automate conversions in scripts.
>
> For **per-code-block control** where you choose the format for each individual code block interactively, see [convert-callouts-interactive](convert-callouts-interactive).
>
> **Quick Decision Guide:**
> - Same format for all blocks → Use this tool (`convert-callouts-to-deflist`)
> - Different formats per block → Use [`convert-callouts-interactive`](convert-callouts-interactive)
> - Automation/CI pipelines → Use this tool (`convert-callouts-to-deflist`)
> - Editorial review needed → Use [`convert-callouts-interactive`](convert-callouts-interactive)

## Overview

Traditional AsciiDoc callouts use numbered markers (`<1>`, `<2>`, etc.) in code blocks with corresponding explanations below. This tool converts them to cleaner formats: definition lists (default), bulleted lists, or inline comments.

**Supported Input Formats:**
- **List format**: `<1> Explanation text` (traditional callout style)
- **Multi-column tables**: 2-column and 3-column tables with callout explanations (used in some documentation like Debezium)

The tool automatically detects the input format and converts it to your chosen output format.

**Important:** This tool is designed to assist your conversion efforts. You must:
- **Carefully review all content changes** before committing them to ensure accuracy and readability
- **Pay special attention to merged callouts** - when multiple callouts appear on the same line, their explanations are automatically merged (see example below)
- Pay attention to any warnings displayed during processing
- Review the warning summary at the end and address any callout mismatches before re-running
- Test documentation builds after converting to verify correctness

## Installation

Install with the doc-utils package:

```bash
pipx install rolfedh-doc-utils
```

Then run directly as a command:

```bash
convert-callouts-to-deflist [options] [path]
```

The tool automatically processes all `.adoc` files recursively in the specified directory (or current directory by default).

## Features

### Automatic Format Detection

Automatically detects and processes multiple input formats:
- **List format**: Traditional `<1> Explanation` style
- **2-column tables**: Callout number | explanation
- **3-column tables**: Item number | value | description (Debezium style)
- **Conditional statements**: Preserves `ifdef::`/`ifndef::`/`endif::` in table cells

### Multiple Output Formats

Convert callouts to your preferred format:
- **Definition lists** (default): Uses "where:" prefix with AsciiDoc definition lists
- **Bulleted lists**: Follows Red Hat style guide format
- **Inline comments**: Embeds explanations as code comments with language-specific syntax

### Intelligent Value Extraction

Extracts user-replaceable values from code:
- **Primary method**: Extracts angle-bracket enclosed values (`<value>`) from code
- **Fallback**: Uses the entire line of code if no replacement value found
- **Heredoc-aware**: Ignores heredoc syntax (`<<EOF`) and only captures user values

### Smart Comment Handling

For inline comments format:
- Detects programming language from `[source,language]` attribute
- Uses appropriate comment syntax (40+ languages supported)
- Automatically falls back to definition list if comment exceeds `--max-comment-length` (default: 120 characters)
- Displays warnings for overly long comments

### Validation and Safety

- Validates callout numbers match between code and explanations
- Skips blocks with mismatched numbers and displays warnings
- Preserves legitimate angle brackets (e.g., Java generics like `List<String>`)
- Non-destructive: Always test with `--dry-run` first
- Automatically excludes `.vale` directory

### Advanced Capabilities

- **Merged callouts**: When multiple callouts appear on same line, automatically merges explanations using AsciiDoc `+` continuation
- **Optional markers**: Preserves "Optional." prefixes from explanations
- **Non-sequential callouts**: Handles callouts like `<1>`, `<3>`, `<5>`
- **Exclusion support**: Filter directories and files via CLI options or exclusion list file

## Usage

### Process All Files in Current Directory (Default)

```bash
convert-callouts-to-deflist
```

Automatically scans all `.adoc` files recursively in the current directory.

### Process Specific Directory

```bash
convert-callouts-to-deflist modules/
```

### Process Single File

```bash
convert-callouts-to-deflist assemblies/my-guide.adoc
```

### Preview Changes (Dry Run)

```bash
convert-callouts-to-deflist --dry-run
```

Shows what would be changed without modifying files.

### Choose Output Format

```bash
# Definition list format (default)
convert-callouts-to-deflist modules/

# Bulleted list format
convert-callouts-to-deflist --format bullets modules/

# Inline comments format
convert-callouts-to-deflist --format comments modules/
```

### Exclude Directories

```bash
convert-callouts-to-deflist --exclude-dir archive --exclude-dir temp
```

Excludes specified directories from processing. Note: `.vale` is excluded by default.

### Use Exclusion List File

```bash
convert-callouts-to-deflist --exclude-list .docutils-ignore
```

Example `.docutils-ignore` file:
```
# Directories to exclude
.vale/
archive/
temp/

# Specific files
test-file.adoc
```

### Verbose Mode

```bash
convert-callouts-to-deflist --verbose
```

Shows detailed processing information.

## Options

- `path` - File or directory to process (default: current directory)
- `-n, --dry-run` - Preview changes without modifying files
- `-v, --verbose` - Enable detailed logging
- `-f, --format {deflist,bullets,comments}` - Output format: "deflist" for definition list with "where:" (default), "bullets" for bulleted list per Red Hat style guide, "comments" for inline comments
- `--max-comment-length N` - Maximum comment length in characters (default: 120). For inline comments format, automatically falls back to definition list if comment exceeds this length
- `--exclude-dir DIR` - Exclude directory (can be used multiple times)
- `--exclude-file FILE` - Exclude file (can be used multiple times)
- `--exclude-list FILE` - Load exclusion list from file
- `-h, --help` - Show help message

## Output Formats

The tool supports three output formats, selectable via the `--format` option:

### Definition List Format (Default)

Uses AsciiDoc definition lists with "where:" prefix. This is the default format.

```bash
convert-callouts-to-deflist modules/
```

**Output:**
```asciidoc
where:

`<my-secret>`::
The secret name

`<my-key>`::
The secret key value
```

### Bulleted List Format

Uses AsciiDoc bulleted lists following the [Red Hat Style Guide](https://redhat-documentation.github.io/supplementary-style-guide/#explain-commands-variables-in-code-blocks) format. Best for explaining YAML structures or multi-line code blocks.

```bash
convert-callouts-to-deflist --format bullets modules/
```

**Output:**
```asciidoc
*   `<my-secret>`: The secret name

*   `<my-key>`: The secret key value
```

### Inline Comments Format

Converts callouts to inline comments within the code itself, using appropriate comment syntax for the code block's language. This removes the separate explanation section entirely.

```bash
convert-callouts-to-deflist --format comments modules/
```

**Output:**
```asciidoc
[source,yaml]
----
apiVersion: v1
kind: Secret
metadata:
  name: <my-secret> # The secret name
data:
  key: <my-key> # The secret key value
----
```

The tool automatically detects the programming language from the `[source,language]` attribute and uses the appropriate comment syntax:
- `//` for Java, JavaScript, TypeScript, C, C++, Go, Rust, etc.
- `#` for Python, Ruby, Bash, YAML, etc.
- `--` for SQL, Lua
- `<!--` for HTML, XML

**Smart Length Handling:** If an explanation exceeds `--max-comment-length` (default: 120 characters), the tool automatically falls back to definition list format for that block and displays a warning.

**When to use each format:**
- **Definition list (`--format deflist`)**: Default choice, works well for most cases, provides semantic "where:" prefix
- **Bulleted list (`--format bullets`)**: Follows Red Hat style guide, preferred for YAML files and complex configurations
- **Inline comments (`--format comments`)**: Best for code examples where explanations are brief and fit naturally as comments

All formats support merged callouts, optional markers, and user-replaceable values.

## Transformation Examples

### Example 1: Callouts with User-Replaceable Values

**Before (Callout Style):**
```asciidoc
[source,yaml]
----
apiVersion: v1
kind: Secret
metadata:
  name: <my-secret> <1>
data:
  key: <my-key> <2>
----
<1> The secret name
<2> The secret key value
```

**After (Definition List Style):**
```asciidoc
[source,yaml]
----
apiVersion: v1
kind: Secret
metadata:
  name: <my-secret>
data:
  key: <my-key>
----

where:

`<my-secret>`::
The secret name

`<my-key>`::
The secret key value
```

### Example 2: Callouts Explaining Code Lines

**Before (Callout Style):**
```asciidoc
[source,java]
----
httpSecurity
    .get("/public/*").permit() <1>
    .path("/admin/*").roles("admin") <2>
    .path("/forbidden").authorization().deny(); <3>
----
<1> Permits all GET requests to paths matching `/public/*` without authentication.
<2> Restricts access to users with the `admin` role.
<3> Denies all access to the `/forbidden` path.
```

**After (Definition List Style):**
```asciidoc
[source,java]
----
httpSecurity
    .get("/public/*").permit()
    .path("/admin/*").roles("admin")
    .path("/forbidden").authorization().deny();
----

where:

`.get("/public/*").permit()`::
Permits all GET requests to paths matching `/public/*` without authentication.

`.path("/admin/*").roles("admin")`::
Restricts access to users with the `admin` role.

`.path("/forbidden").authorization().deny();`::
Denies all access to the `/forbidden` path.
```

### Example 3: Multiple Callouts on Same Line (Merged Explanations)

**⚠️ REVIEW CAREFULLY:** When multiple callouts appear on the same code line, the tool automatically merges their explanations into a single definition list entry using AsciiDoc's list continuation marker (`+`). This behavior is correct for most cases, but you should verify that the merged explanations read naturally together.

**Before (Callout Style):**
```asciidoc
[source,java]
----
@Path("hello")
public class HelloResource {
    @BasicAuthentication <1> <2>
    @Path("basic")
    public String basicAuthMechanism() {
        return "basic";
    }
}
----
<1> Enables basic authentication for this endpoint.
<2> Authentication is required by default when using this annotation.
```

**After (Definition List Style - Merged):**
```asciidoc
[source,java]
----
@Path("hello")
public class HelloResource {
    @BasicAuthentication
    @Path("basic")
    public String basicAuthMechanism() {
        return "basic";
    }
}
----

where:

`@BasicAuthentication`::
Enables basic authentication for this endpoint.
+
Authentication is required by default when using this annotation.
```

**Why This Matters:**
- Both callouts reference the **same code element** (`@BasicAuthentication`)
- Their explanations are **semantically related** (the first explains what it does, the second adds important context)
- The merged format is cleaner and avoids duplicate terms in the definition list
- The `+` continuation marker properly connects the related explanations

**When to Review:**
- If the merged explanations feel redundant or repetitive
- If the explanations would read better as separate items (consider refactoring the callouts in the source)
- If the order of explanations affects understanding (they merge in callout number order)

### Example 4: Multi-Column Table Format (Automatic Detection)

The tool automatically detects and converts multi-column table format callout explanations used in some documentation (e.g., Debezium).

#### 2-Column Table Format (Callout | Explanation)

**Before (2-Column Table):**
```asciidoc
[source,sql]
----
ALTER TABLE inventory ADD COLUMN c1 INT; <1>
INSERT INTO myschema.inventory (id,c1) VALUES (100, 1); <2>
----

[cols="1,3"]
|===
|<1>
|Adds a new column to the inventory table.

|<2>
|Inserts a sample record with the new column value.
|===
```

**After (Definition List Style):**
```asciidoc
[source,sql]
----
ALTER TABLE inventory ADD COLUMN c1 INT;
INSERT INTO myschema.inventory (id,c1) VALUES (100, 1);
----

where:

`ALTER TABLE inventory ADD COLUMN c1 INT;`::
Adds a new column to the inventory table.

`INSERT INTO myschema.inventory (id,c1) VALUES (100, 1);`::
Inserts a sample record with the new column value.
```

#### 3-Column Table Format (Debezium Style)

Some documentation uses a 3-column format: item number | value | description. The tool detects this format and combines the value and description.

**Before (3-Column Table):**
```asciidoc
[source,sql]
----
INSERT INTO myschema.debezium_signal (id, type, data) // <1>
values ('ad-hoc-1',   // <2>
    'execute-snapshot',  // <3>
    '{"data-collections": ["schema1.table1"]}'); // <4>
----

.Descriptions of fields in a SQL command
[cols="1,2,6",options="header"]
|===
|Item |Value |Description

|1
|`myschema.debezium_signal`
|Specifies the fully-qualified name of the signaling table on the source database.

|2
|`ad-hoc-1`
|The `id` parameter specifies an arbitrary string that is assigned as the identifier for the signal request.

|3
|`execute-snapshot`
|The `type` parameter specifies the operation that the signal is intended to trigger.

|4
|`data-collections`
|A required component of the `data` field that specifies an array of table names.
|===
```

**After (Definition List Style):**
```asciidoc
[source,sql]
----
INSERT INTO myschema.debezium_signal (id, type, data)
values ('ad-hoc-1',
    'execute-snapshot',
    '{"data-collections": ["schema1.table1"]}');
----

where:

`myschema.debezium_signal`::
Refers to `myschema.debezium_signal`.
Specifies the fully-qualified name of the signaling table on the source database.

`ad-hoc-1`::
Refers to `ad-hoc-1`.
The `id` parameter specifies an arbitrary string that is assigned as the identifier for the signal request.

`execute-snapshot`::
Refers to `execute-snapshot`.
The `type` parameter specifies the operation that the signal is intended to trigger.

`data-collections`::
Refers to `data-collections`.
A required component of the `data` field that specifies an array of table names.
```

**Detection Details:**
- Automatic detection: list format, 2-column tables, or 3-column tables (no flags needed)
- For 3-column tables: Combines value and description columns
- Preserves conditional statements (`ifdef::`/`ifndef::`/`endif::`) in table cells
- Skips header rows automatically

## Edge Cases and Warnings

### Callout Mismatch Warnings

When the tool detects a mismatch between callout numbers in code and their explanations, it displays a warning immediately and skips that code block:

```
WARNING: my-file.adoc lines 141-145: Callout mismatch: code has [1, 2], explanations have [1, 3]
```

**Duplicate Callout Detection**: The warning now shows duplicate callout numbers in explanation tables:

```
WARNING: file.adoc lines 55-72: Callout mismatch: code has [1, 2, 3, 4, 5, 6, 7, 8, 9], explanations have [1, 2, 3, 4, 5, 7, 8, 8, 9]
```

In this example, the table has two rows with callout 8 and is missing callout 6.

This prevents incorrect conversions when:
- Callout numbers are non-consecutive in the code but explanations use different numbers
- An explanation is missing for a callout in the code
- An explanation exists for a callout that's not in the code
- A table has duplicate callout numbers (documentation error)

### Missing Explanations Warning

When the tool finds a code block with callouts but no explanations after it, it displays a warning:

```
WARNING: file.adoc line 211: Code block has callouts [1, 2, 3, 4] but no explanations found after it.
This may indicate: explanations are shared with another code block, explanations are in an unexpected
location, or documentation error (missing explanations). Consider reviewing this block manually.
```

This commonly occurs when:
- **Shared explanations**: Multiple code blocks share the same explanation table (e.g., in conditional sections like `ifdef::community[]` and `ifdef::product[]`)
- **Unexpected location**: Explanations are not immediately after the code block
- **Documentation error**: Explanations are genuinely missing

**Action Required**: Review these blocks manually to determine the appropriate handling.

### Warning Summary

At the end of processing, a summary of all warnings is displayed:

```
Processed 147 AsciiDoc file(s)
Would modify 3 file(s) with 3 code block conversion(s)

⚠️  3 Warning(s):
  WARNING: file1.adoc lines 15-19: Callout mismatch: code has [1, 2], explanations have [2, 3]
  WARNING: file2.adoc lines 141-145: Callout mismatch: code has [1, 2], explanations have [1, 3]
  WARNING: file3.adoc line 211: Code block has callouts [1, 2, 3, 4] but no explanations found after it.
  This may indicate: explanations are shared with another code block, explanations are in an unexpected
  location, or documentation error (missing explanations). Consider reviewing this block manually.

Suggestion: Fix the callout mismatches in the files above and rerun this command.
```


## Real-World Example

### Complex Secret Configuration

**Before:**
```asciidoc
[source,yaml]
----
cat <<EOF | oc -n {my-product-namespace} create -f -
apiVersion: v1
kind: Secret
metadata:
  name: <my-product-database-certificates-secrets> <1>
type: Opaque
stringData:
  postgres-ca.pem: |-
    -----BEGIN CERTIFICATE-----
    <ca-certificate-key> <2>
  postgres-key.key: |-
    -----BEGIN CERTIFICATE-----
    <tls-private-key> <3>
  postgres-crt.pem: |-
    -----BEGIN CERTIFICATE-----
    <tls-certificate-key> <4>
EOF
----
<1> Specifies the name of the certificate secret.
<2> Specifies the CA certificate key.
<3> Optional. Specifies the TLS private key.
<4> Optional. Specifies the TLS certificate key.
```

**After:**
```asciidoc
[source,yaml]
----
cat <<EOF | oc -n {my-product-namespace} create -f -
apiVersion: v1
kind: Secret
metadata:
  name: <my-product-database-certificates-secrets>
type: Opaque
stringData:
  postgres-ca.pem: |-
    -----BEGIN CERTIFICATE-----
    <ca-certificate-key>
  postgres-key.key: |-
    -----BEGIN CERTIFICATE-----
    <tls-private-key>
  postgres-crt.pem: |-
    -----BEGIN CERTIFICATE-----
    <tls-certificate-key>
EOF
----

where:

`<my-product-database-certificates-secrets>`::
Specifies the name of the certificate secret.

`<ca-certificate-key>`::
Specifies the CA certificate key.

`<tls-private-key>` Optional::
Specifies the TLS private key.

`<tls-certificate-key>` Optional::
Specifies the TLS certificate key.
```

## Technical Details

This tool uses the [`callout_lib`](https://github.com/rolfedh/doc-utils/tree/main/callout_lib) Python library for callout detection and conversion. See the [library README](https://github.com/rolfedh/doc-utils/blob/main/callout_lib/README.md) for detailed implementation information.

**Key Processing Steps:**
1. Scan for code blocks with `[source]` attributes
2. Extract callout numbers from code and group by line
3. Detect and extract explanations (list format or table format)
4. Validate callout numbers match between code and explanations
5. Convert to chosen output format (deflist, bullets, or comments)
6. Replace callout sections in document

**Supported Comment Syntax (for inline comments format):**
- C-style `//`: Java, JavaScript, TypeScript, C, C++, Go, Rust, Swift, Kotlin, etc.
- Hash `#`: Python, Ruby, Bash, YAML, Shell, Perl, R, etc.
- SQL `--`: SQL, PL/SQL, T-SQL, Lua
- HTML/XML `<!--`: HTML, XML, SVG
- Others: Lisp `;`, MATLAB/LaTeX `%`, etc. (40+ languages total)

## Best Practices

1. **Always work in a git branch** before converting files
2. **Use `--dry-run` first** to preview what will be changed
3. **Choose the appropriate format**:
   - Use `--format deflist` (default) for general documentation
   - Use `--format bullets` for YAML files and complex configurations (follows Red Hat style guide)
4. **Review changes with `git diff`** before committing
5. **Test documentation builds** after converting
6. **Start with a small batch** to verify behavior

## Example Workflow

```bash
# Create a feature branch
git checkout -b convert-callouts

# Preview changes on entire repository (.vale is excluded by default)
cd ~/rhbquarkus
convert-callouts-to-deflist --dry-run

# Example output:
# Found 292 AsciiDoc file(s) to process
# Would modify: asciidoc/logging.adoc (3 code block(s))
# Would modify: asciidoc/security-jwt.adoc (3 code block(s))
# ...
# Would modify 19 file(s) with 104 code block conversion(s)

# Process a specific directory
convert-callouts-to-deflist --dry-run asciidoc/

# Convert files
convert-callouts-to-deflist

# Review changes
git diff

# Test build
./scripts/build-docs.sh

# Commit changes
git add .
git commit -m "Convert callouts to definition list format"

# Or use bulleted list format for YAML files
convert-callouts-to-deflist --format bullets --dry-run deployment-guides/
convert-callouts-to-deflist --format bullets deployment-guides/
git commit -m "Convert YAML callouts to bulleted list format"
```

---

See the main [Tools Reference](index) for more documentation utilities.
