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

Traditional AsciiDoc callouts use numbered markers (`<1>`, `<2>`, etc.) in code blocks with corresponding explanations below. Explanations can be in two formats:
- **List format**: `<1> Explanation text` (traditional)
- **Table format**: Two-column tables with callout numbers and explanations (used in some documentation)

This tool automatically detects both formats and converts them to a cleaner definition list format that uses the actual code lines as terms.

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

### Example 4: Table Format Callouts (Automatic Detection)

The tool automatically detects and converts table-format callout explanations. Some documentation uses tables instead of list-format explanations. The tool supports both **2-column** and **3-column** table formats.

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

#### 3-Column Table Format (Item | Value | Description)

Some documentation (e.g., Debezium) uses a 3-column format with item number, value reference, and description. The tool automatically detects this format and combines the value and description columns.

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

**How It Works:**
- The tool automatically detects list-format (`<1> text`), 2-column table, and 3-column table callout explanations
- For 3-column tables, the tool combines the Value and Description columns using "Refers to `value`. Description..." format
- Header rows (with keywords like "Item", "Value", "Description") are automatically detected and skipped
- Table format is common in some documentation repositories (e.g., Debezium, integration guides)
- Conditional statements (`ifdef::`, `ifndef::`, `endif::`) in table cells are preserved
- No special flags needed - detection is automatic with priority: 3-column → 2-column → list format

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

**When to use each format:**
- **Definition list (`--format deflist`)**: Default choice, works well for most cases, provides semantic "where:" prefix
- **Bulleted list (`--format bullets`)**: Follows Red Hat style guide, preferred for YAML files and complex configurations
- **Inline comments (`--format comments`)**: Best for code examples where explanations are brief and fit naturally as comments

All formats support merged callouts, optional markers, and user-replaceable values.

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
- `--exclude-dir DIR` - Exclude directory (can be used multiple times)
- `--exclude-file FILE` - Exclude file (can be used multiple times)
- `--exclude-list FILE` - Load exclusion list from file
- `-h, --help` - Show help message

## Features

### Intelligent Value Extraction

The script extracts user-replaceable values from code:

1. **Primary Method**: Extracts angle-bracket enclosed replacement values (`<value>`) from the code line.
2. **Fallback**: If no replacement value found in code, extracts the line of code.
3. **Heredoc-aware**: Ignores heredoc syntax (`<<EOF`) and only captures user values

### Validation and Safety

The script validates callouts before converting:

- Ensures callout numbers in code match explanation numbers
- Skips blocks where numbers don't match (prevents false conversions)
- Preserves legitimate angle brackets (e.g., Java generics like `List<String>`)
- Non-destructive: Always test with `--dry-run` first

### Optional Markers

Preserves optional markers from explanations:

**Input:**
```asciidoc
<2> Optional. The name of the ConfigMap
```

**Output:**
```asciidoc
`<config-name>`::
Optional. The name of the ConfigMap
```

### Non-Sequential Callouts

Handles non-sequential callout numbers correctly:

```asciidoc
<1> First item
<3> Third item
<5> Fifth item
```

## Edge Cases Handled

1. **Multiple code blocks** - Processes each block independently
2. **Multiple callouts on same line** - Automatically merges explanations using AsciiDoc `+` continuation marker
3. **Non-sequential numbers** - Handles callouts like `<1>`, `<3>`, `<5>`
4. **Heredoc syntax** - Ignores `<<EOF` and similar patterns
5. **Legitimate angle brackets** - Skips Java generics, comparison operators, etc.
6. **Mixed content** - Preserves text before and after code blocks
7. **Different delimiters** - Supports both `----` and `....` code block delimiters
8. **No language specified** - Works with `[source]` blocks without language
9. **Callout mismatches** - Skips blocks where numbers don't align and displays a warning with file and line numbers
10. **Vale fixtures** - Automatically excludes `.vale` directory by default

### Callout Mismatch Warnings

When the tool detects a mismatch between callout numbers in code and their explanations, it displays a warning immediately and skips that code block:

```
WARNING: my-file.adoc lines 141-145: Callout mismatch: code has [1, 2], explanations have [1, 3]
```

At the end of processing, a summary of all warnings is displayed:

```
Processed 147 AsciiDoc file(s)
Would modify 3 file(s) with 3 code block conversion(s)

⚠️  2 Warning(s):
  WARNING: file1.adoc lines 15-19: Callout mismatch: code has [1, 2], explanations have [2, 3]
  WARNING: file2.adoc lines 141-145: Callout mismatch: code has [1, 2], explanations have [1, 3]
```

This prevents incorrect conversions when:
- Callout numbers are non-consecutive in the code but explanations use different numbers
- An explanation is missing for a callout in the code
- An explanation exists for a callout that's not in the code


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

### Pattern Matching

- **Code block detection**: `^\[source(?:,\s*(\w+))?\]` followed by `----` or `....`
- **Callout in code**: `<(\d+)>` (supports multiple callouts per line)
- **Callout explanation**: `^<(\d+)>\s+(.+)$`
- **User values**: `(?<!<)<([a-zA-Z][^>]*)>` (excludes heredoc syntax)

### Processing Algorithm

1. Parse document and identify all code blocks
2. For each code block:
   - Extract callout numbers and associated values from code
   - Group callouts that appear on the same code line
   - Extract callout explanations following the block
   - Validate that numbers match
   - If valid:
     - Remove callout markers from code
     - Create definition list from callout groups
     - For groups with multiple callouts, merge explanations with `+` continuation
     - Replace old explanations with definition list
3. Process blocks in reverse order to maintain line numbers

## Limitations

- Only processes AsciiDoc files
- Requires exact `<N>` format for callouts (numbers only)
- Callout explanations must immediately follow code blocks (with optional blank lines or `+` markers in between)
- Supports continuation lines within callout explanations, but explanations must start with the `<N>` pattern

## Testing

The repository includes a comprehensive test file: `test-callouts.adoc`

Run tests:
```bash
python3 convert-callouts-to-deflist.py test-callouts.adoc /tmp/output.adoc -v
```

The test file includes:
- Basic callouts
- Optional markers
- Complex examples with multiple values
- Non-sequential numbers
- Legitimate angle brackets (should be skipped)
- Mixed content scenarios
- Different code block delimiters
- Callout mismatches (should be skipped)

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
