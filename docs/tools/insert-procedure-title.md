---
layout: default
title: insert-procedure-title
parent: Tools Reference
nav_order: 17
---

# Insert Procedure Title

This tool ensures AsciiDoc procedure files have a `.Procedure` block title above the numbered steps. This block title is required for DITA task conversion, as enforced by the `AsciiDocDITA.TaskContents` Vale rule.

## What This Tool Does

The tool scans AsciiDoc procedure files and:

1. Identifies procedure files (those with `:_mod-docs-content-type: PROCEDURE`)
2. Skips files that already have a `.Procedure` block title (including those using unordered lists)
3. Finds the first numbered step (`. Step text` or `1. Step text`)
4. Checks if `.Procedure` already exists before the steps
5. Inserts the block title if missing
6. Warns if a procedure file has neither numbered steps nor a `.Procedure` title

### Before

```asciidoc
:_mod-docs-content-type: PROCEDURE
[id="proc_my-procedure"]

= My Procedure

[role="_abstract"]
This procedure explains how to configure the feature.

. Open the configuration file.
. Add the following property.
. Save and restart the application.
```

### After

```asciidoc
:_mod-docs-content-type: PROCEDURE
[id="proc_my-procedure"]

= My Procedure

[role="_abstract"]
This procedure explains how to configure the feature.

.Procedure

. Open the configuration file.
. Add the following property.
. Save and restart the application.
```

## Installation

Install with pipx (recommended):

```sh
pipx install rolfedh-doc-utils
```

Or with pip:

```sh
pip install rolfedh-doc-utils
```

## Usage

```sh
insert-procedure-title <path> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `path` | File or directory to process (required) |

### Options

| Option | Description |
|--------|-------------|
| `-n, --dry-run` | Show what would be changed without modifying files |
| `-v, --verbose` | Show all files processed, including those not modified |

## Examples

### Preview Changes (Dry Run)

```sh
# Preview what would be changed in modules directory
insert-procedure-title modules/ --dry-run

# Preview with verbose output
insert-procedure-title modules/ --dry-run -v
```

### Process Files

```sh
# Process all .adoc files in modules directory
insert-procedure-title modules/

# Process single file
insert-procedure-title modules/proc_my-procedure.adoc
```

## Output

The tool displays progress, modifications, and warnings:

```
Warning: Procedure file has no numbered steps and no .Procedure title: modules/proc_incomplete.adoc
Modified: modules/proc_configure-feature.adoc
Modified: modules/proc_install-component.adoc

Complete. 2 file(s) modified.
Warnings: 1 procedure file(s) have no numbered steps.
```

With `--dry-run`:

```
Warning: Procedure file has no numbered steps and no .Procedure title: modules/proc_incomplete.adoc
Would modify: modules/proc_configure-feature.adoc
Would modify: modules/proc_install-component.adoc

Dry run complete. 2 file(s) would be modified.
Warnings: 1 procedure file(s) have no numbered steps.
```

With `--verbose`:

```
Skipping (not a procedure file): modules/ref_api-reference.adoc
No changes needed (has .Procedure): modules/proc_uses-unordered-list.adoc
Warning: Procedure file has no numbered steps and no .Procedure title: modules/proc_incomplete.adoc
No changes needed: modules/proc_already-has-title.adoc
Would modify: modules/proc_configure-feature.adoc

Dry run complete. 1 file(s) would be modified.
Warnings: 1 procedure file(s) have no numbered steps.
```

## Use Cases

### Fix Vale AsciiDocDITA.TaskContents Warnings

When Vale reports `TaskContents` warnings like:

```
modules/proc_my-procedure.adoc:1:1: warning: The '.Procedure' block title is missing.
```

Run the tool to fix all procedure files at once:

```sh
insert-procedure-title modules/
```

### Find Incomplete Procedure Files

Use the tool to identify procedure files that are missing their numbered steps:

```sh
insert-procedure-title modules/ --dry-run
```

Files with the warning "Procedure file has no numbered steps" need content added.

### Pre-Migration DITA Preparation

Before migrating AsciiDoc content to DITA, ensure all procedure files have the required block title:

```sh
# Preview changes first
insert-procedure-title modules/ --dry-run

# Apply changes
insert-procedure-title modules/
```

## Resolving Warnings

When the tool warns about procedure files with no numbered steps, investigate each file manually. These warnings often reveal content issues that require editorial judgment.

### Stub Files Acting as Section Headings

**Problem:** A procedure file contains only a title and abstract, with no actual steps. It serves as a section heading in an assembly, with real procedures nested underneath at higher leveloffsets.

```asciidoc
// Assembly structure
include::modules/proc_configuring-developer-tools.adoc[leveloffset=+1]
include::modules/proc_configuring-registry-client.adoc[leveloffset=+2]
include::modules/proc_limiting-registry-catalog.adoc[leveloffset=+3]
```

**Solution:**

1. Evaluate whether the stub's content adds value
2. If useful, incorporate it into a child procedure's abstract
3. Delete the stub file
4. Flatten the hierarchy by adjusting leveloffsets (+2/+3 → +1/+2)

**Example:** In [MR !3236](https://gitlab.cee.redhat.com/quarkus-documentation/quarkus/-/merge_requests/3236), `proc_configuring-quarkus-developer-tools.adoc` contained only a bullet list of capabilities—content not relevant to the child procedures about registry configuration. The stub was deleted and the hierarchy flattened.

### Wrong Content Type

**Problem:** A file is marked as PROCEDURE but contains no procedure steps—it's actually conceptual or reference content.

**Solution:** Change the content type to match the actual content:

```asciidoc
// Before
:_mod-docs-content-type: PROCEDURE

// After (for conceptual content)
:_mod-docs-content-type: CONCEPT
```

Also rename the file to match the content type convention (e.g., `proc_` → `con_`).

**Example:** In [MR !3236](https://gitlab.cee.redhat.com/quarkus-documentation/quarkus/-/merge_requests/3236), `proc_quarkus-tracking-licenses.adoc` contained explanatory content about license tracking without any procedure steps. It was renamed to `con_quarkus-tracking-licenses.adoc` with the content type changed to CONCEPT.

### Incorporating Context from Deleted Stubs

**Problem:** A stub file contains useful context that should be preserved when the stub is deleted.

**Solution:** Incorporate the valuable information into the child procedure's abstract before deleting the stub.

**Example:** In [MR !3237](https://gitlab.cee.redhat.com/quarkus-documentation/quarkus/-/merge_requests/3237), `proc_advanced-configuration-mapping.adoc` had an abstract explaining that nested object configuration "is an extension specific to {ProductLongName} and outside of the MicroProfile Config specification." This context was incorporated into `proc_using-nested-object-configuration.adoc`'s abstract, then the stub was deleted and the leveloffset adjusted from +2 to +1.

### Procedure Steps in Wrong Format

**Problem:** A file has procedure steps, but they use an unordered list or a custom block title instead of `.Procedure` with numbered steps.

**Solution:** Restructure the procedure:

- Replace custom block titles (like `.Adding the dependency`) with `.Procedure`
- Convert bullet lists to numbered steps where order matters
- Use an open block (`--`) to group alternative methods under a single numbered step

**Example:** In [MR !3237](https://gitlab.cee.redhat.com/quarkus-documentation/quarkus/-/merge_requests/3237), `proc_quarkus-tracking-license-kubernetes.adoc` used `.Adding license tracking annotations manually` as a block title with bullet points. It was restructured to use `.Procedure` with a numbered step containing two methods in an open block.

## How It Works

The tool:

1. **Identifies procedure files** by checking for `:_mod-docs-content-type: PROCEDURE`
2. **Finds numbered steps** by looking for lines starting with `. ` (implicit ordered list) or `1. ` (explicit numbered list)
3. **Searches backward** from the first step to check if `.Procedure` exists
4. **Inserts `.Procedure`** before the steps if missing, with appropriate blank lines

The tool handles complex structures where other block titles (like method sub-headings) appear between `.Procedure` and the actual steps.

## Notes

- **Idempotent**: Running the tool multiple times won't add duplicate block titles
- **Safe**: Use `--dry-run` to preview changes before applying
- **Procedure files only**: Skips non-procedure content types (REFERENCE, CONCEPT, etc.)
- **Handles unordered lists**: Skips procedure files that already have `.Procedure` but use bullet lists instead of numbered steps
- **Warns about incomplete files**: Identifies procedure files that have neither numbered steps nor a `.Procedure` title
- Only processes `.adoc` files
- Skips symlinks during directory scanning

## Related Tools

- **[insert-abstract-role](insert-abstract-role)** - Add `[role="_abstract"]` for DITA short descriptions
- **[convert-callouts-to-deflist](convert-callouts-to-deflist)** - Convert callouts to definition lists for DITA compatibility

---

See the main [README.md](../../README.md) for more details on installation and usage as a package.
