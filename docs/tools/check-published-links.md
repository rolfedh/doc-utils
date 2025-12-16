---
layout: default
title: check-published-links
nav_order: 12
---

# check-published-links

Validates links on published HTML documentation pages using linkchecker.

## Overview

The `check-published-links` tool uses [linkchecker](https://linkchecker.github.io/linkchecker/) to validate all links on published HTML documentation. Unlike `validate-links` which checks AsciiDoc source files, this tool checks the actual rendered HTML output—catching issues that only appear after publication.

## Key Features

- **Published HTML validation** - Checks actual rendered documentation, not source files
- **URL rewriting** - Corrects misresolved paths for platforms with URL routing issues
- **Single and bulk modes** - Check one URL or a list of documentation pages
- **False positive handling** - Automatically filters known issues (host:port placeholders, Maven Central 403s)
- **Detailed reporting** - Generates comprehensive reports with error categorization
- **Timeout detection** - Identifies slow responses separately from broken links

## When to Use

Use this tool when you need to:
- **Validate after publishing** - Verify links work on the live site
- **Check rendered output** - Catch issues in generated HTML (relative paths, image references)
- **Validate documentation platforms** - Handle platforms with URL routing that causes path resolution issues
- **Bulk check documentation** - Validate multiple guides in a single run
- **Generate audit reports** - Document link health for compliance or quality assurance

## URL Rewriting

Some documentation platforms use URL routing that causes linkchecker to resolve relative paths incorrectly. The `--rewrite-pattern` and `--rewrite-replacement` options let you correct these paths automatically.

### How It Works

1. Linkchecker reports an error for a misresolved URL
2. The tool checks if the URL matches a rewrite pattern
3. If matched, it verifies the resource exists at the corrected path
4. Verified paths are counted as valid (not errors)

### Example

```bash
# Your docs serve from /docs/en/product/
# But images resolve to /docs/en/PRODUCT_CODE_1.0/images/

check-published-links https://docs.example.com/product/guide \
    --rewrite-pattern "/docs/en/product/" \
    --rewrite-replacement "/docs/en/PRODUCT_CODE_1.0/"
```

## Basic Usage

### Single URL

```bash
# Check a single documentation page
check-published-links https://docs.example.com/guide/index.html

# With increased timeout for slow sites
check-published-links https://docs.example.com/guide/ --timeout 60
```

### Bulk Validation

Create a file with URLs to check (one per line):

```
# urls-to-check.txt
https://docs.example.com/guide1/
https://docs.example.com/guide2/
https://docs.example.com/guide3/
```

```bash
check-published-links --file urls-to-check.txt
```

### With URL Rewriting

```bash
# Single rewrite rule
check-published-links https://docs.example.com/product/guide \
    --rewrite-pattern "/docs/en/product/" \
    --rewrite-replacement "/docs/en/PROD_V1.0/"

# Multiple rewrite rules
check-published-links https://docs.example.com/product/guide \
    --rewrite-pattern "/docs/en/product/images/" \
    --rewrite-replacement "/docs/en/PROD_V1.0/images/" \
    --rewrite-pattern "/docs/en/product/resources/" \
    --rewrite-replacement "/docs/en/PROD_V1.0/resources/"
```

### With Custom Ignore Patterns

```bash
# Ignore URLs matching a regex pattern
check-published-links https://docs.example.com/guide/ \
    --ignore-pattern "^https?://internal\.example\.com" \
    --ignore-pattern "^https?://staging\."
```

### Using a Configuration File

```bash
# Use explicit config file
check-published-links https://docs.example.com/guide/ --config linkcheck.conf

# Or place .check-published-links.conf in the current directory (auto-loaded)
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `URL` | Single URL to check | - |
| `--file`, `-f` | File containing URLs to check (one per line) | - |
| `--timeout`, `-t` | Timeout for each link check in seconds | 15 |
| `--rewrite-pattern` | URL pattern to match for rewriting (can be used multiple times) | None |
| `--rewrite-replacement` | Replacement for matched pattern (must match --rewrite-pattern count) | None |
| `--ignore-pattern` | Regex pattern for URLs to ignore (can be used multiple times) | None |
| `--config`, `-c` | Configuration file path | `.check-published-links.conf` |
| `--reports-dir` | Directory for report files | `reports/` |

## Output Examples

### Successful Check

```
═══════════════════════════════════════════════════════════════
  Documentation Link Checker
═══════════════════════════════════════════════════════════════

ℹ URL: https://docs.example.com/guide/
ℹ Guide: guide
ℹ Timeout: 15 seconds
ℹ Report: reports/link-check-report_2024-01-15_10-30-45.txt

✓ PASS - 127 links checked

✓ All documentation links are valid!
```

### Check with False Positives

```
✓ PASS - All errors were false positives
  Note: 3 path(s) verified at corrected location
  Note: 2 known issues (host:port) - safe to ignore
```

### Failed Check

```
✗ FAIL - 5 errors found
  Note: 2 path(s) verified at corrected location (not counted)
  Error: 1 path(s) NOT FOUND at corrected location
  Note: 1 known issues (host:port) - safe to ignore
  TIMEOUT: 1 links exceeded timeout limit

Link check found issues. Review the report for details.
```

### Bulk Mode Output

```
═══════════════════════════════════════════════════════════════
  Documentation Link Checker - Bulk Mode
═══════════════════════════════════════════════════════════════

ℹ URL List: urls-to-check.txt
ℹ Total URLs: 15
ℹ Timeout: 15 seconds
ℹ Report: reports/link-check-report_2024-01-15_10-30-45.txt

[1/15] Checking: Getting Started...
  ✓ PASS - 89 links
[2/15] Checking: Configuration Guide...
  ✓ PASS - 156 links [2 rewritten OK]
[3/15] Checking: Security Guide...
  ✗ FAIL - 3 errors found

═══════════════════════════════════════════════════════════════
  Results
═══════════════════════════════════════════════════════════════

  Total:  15 guides
  Pass:   14
  Fail:   1
  Rate:   93.3%
```

## Known Issues Handled

The tool automatically handles these common false positives:

### 1. Host:Port Placeholders
URLs like `https://host:port/auth` are documentation placeholders and are safe to ignore.

### 2. Comma-Separated URL Lists
Examples like `http://www.example.com,http://localhost:3000` showing configuration format are filtered out.

### 3. Maven Central 403 Errors
Maven Central blocks automated access with 403 Forbidden. These links work in browsers.

### 4. Misresolved Paths (with rewrite rules)
When rewrite rules are configured, the tool verifies resources at corrected paths and doesn't count verified paths as errors.

## Reports

Reports are saved to the `reports/` directory with timestamps:

```
reports/link-check-report_2024-01-15_10-30-45.txt
```

### Report Contents

- Summary of all guides checked
- Statistics (total errors, known issues, timeouts)
- Detailed error information for failed guides
- URL, parent URL, and result for each error

## Configuration File

You can save ignore patterns and rewrite rules in a configuration file to avoid repeating them on the command line.

### File Location

The tool automatically loads `.check-published-links.conf` from the current directory if it exists. You can also specify a custom path with `--config`.

### File Format

```ini
# General settings
[settings]
timeout = 30
reports-dir = ./build/link-reports/

# Ignore patterns (one regex per line)
[ignore-patterns]
^https?://internal\.example\.com
^https?://staging\.
^https?://private-api\.

# Rewrite rules (pattern = replacement)
[rewrite-rules]
/docs/en/product/ = /docs/en/PRODUCT_V1.0/
/docs/en/product/images/ = /docs/en/PRODUCT_V1.0/images/
```

### Configuration Sections

| Section | Description |
|---------|-------------|
| `[settings]` | General settings like `timeout` and `reports-dir` |
| `[ignore-patterns]` | Regex patterns for URLs to skip (one per line) |
| `[rewrite-rules]` | URL path corrections (pattern = replacement) |

### Settings Options

| Setting | Description | Default |
|---------|-------------|---------|
| `timeout` | Timeout for each link check in seconds | 15 |
| `reports-dir` | Directory for report files | `reports/` |

### Precedence

Options are resolved in this order (CLI overrides config file):

**For timeout and reports-dir:**
1. Command-line option (if specified)
2. Configuration file value (if present)
3. Default value

**For ignore patterns and rewrite rules:**
1. Default ignore patterns (localhost, example.com, etc.)
2. Configuration file patterns (added to defaults)
3. Command-line options (added to above)

This allows you to extend the defaults without replacing them.

## Prerequisites

This tool requires [linkchecker](https://github.com/linkchecker/linkchecker) to be installed:

```bash
# Install with pipx (recommended)
pipx install linkchecker

# Or with pip
pip install linkchecker
```

For more information about linkchecker, see the [linkchecker documentation](https://linkchecker.github.io/linkchecker/).

The check-published-links tool wraps linkchecker to add URL rewriting for misresolved paths, automatic filtering of known false positives, and structured reporting with error categorization.

## Performance Considerations

- **Timeout**: Default is 15 seconds per link. Increase for slow servers.
- **External links**: All external links are checked, which can be slow for large documentation sets.
- **Rate limiting**: Some servers may rate-limit automated checks. Consider running during off-peak hours.

## Troubleshooting

### Timeout Issues

If many links are timing out:

```bash
check-published-links https://docs.example.com/guide/ --timeout 60
```

### SSL Certificate Issues

Linkchecker uses system certificates. Ensure your system's CA certificates are up to date.

### Too Many False Positives

Add custom ignore patterns via CLI or configuration file:

```bash
# Via CLI
check-published-links https://docs.example.com/guide/ \
    --ignore-pattern "^https?://known-flaky-server\.com"

# Via config file (.check-published-links.conf)
[ignore-patterns]
^https?://known-flaky-server\.com
^https?://internal\.example\.com
```

## Related Tools

- [validate-links](validate-links.md) - Validates links in AsciiDoc source files
- [extract-link-attributes](extract-link-attributes.md) - Extract links into reusable attributes

## Comparison: validate-links vs check-published-links

| Feature | validate-links | check-published-links |
|---------|---------------|----------------------|
| **Input** | AsciiDoc source files | Published HTML URLs |
| **When to use** | Before publishing | After publishing |
| **Attribute resolution** | Yes | N/A |
| **Cross-reference checking** | Yes (xref:) | N/A |
| **Rendered output checking** | No | Yes |
| **Image path verification** | Source paths | Rendered paths |
| **URL transposition** | Yes | Via rewrite rules |
| **Requires** | Python only | linkchecker |

**Use both tools together:**
1. `validate-links` during development to catch issues early
2. `check-published-links` after publishing to verify the rendered output
