---
layout: default
title: validate-links
parent: Tools Reference
nav_order: 8
---

# validate-links

Validate links in AsciiDoc documentation, checking for broken URLs and missing references.

## Overview

The `validate-links` tool checks all links in your AsciiDoc documentation for validity, including external URLs, internal cross-references, and image paths. It features a powerful **transpose** option that allows you to validate against preview or staging environments before publication.

## Key Features

- **Comprehensive validation** - Checks link:, xref:, and image:: references
- **URL transposition** - Replace production URLs with preview/staging URLs for pre-publication validation
- **Attribute resolution** - Resolves AsciiDoc attributes in URLs before validation
- **Concurrent checking** - Validates multiple URLs in parallel for speed
- **Smart caching** - Avoids redundant checks with configurable cache
- **Flexible output** - Text, JSON, or JUnit formats for CI/CD integration
- **Retry logic** - Handles transient network issues gracefully

## When to Use

Use this tool to:
- **Validate before publishing** - Check links against preview environments
- **Find broken links** - Identify 404s and missing references
- **Verify after migrations** - Ensure links still work after site changes
- **CI/CD integration** - Automatically validate on pull requests
- **Check staging environments** - Validate against non-production URLs

## The Transpose Feature

The transpose feature is particularly useful when your documentation references production URLs, but you need to validate against preview or staging environments before publication.

### How It Works

1. You provide transposition rules in the format: `from_url--to_url`
2. The tool replaces matching URL prefixes before validation
3. Original URLs are preserved in the output for reference

### Example

```bash
# Your docs contain: link:https://docs.redhat.com/guide[Guide]
# But you want to check: https://preview.docs.redhat.com/guide

validate-links --transpose "https://docs.redhat.com--https://preview.docs.redhat.com"
```

## Basic Usage

### Simple Validation

```bash
# Validate all links in current directory
validate-links

# Validate specific directories
validate-links --scan-dir modules --scan-dir assemblies

# Use specific attributes file
validate-links --attributes-file common-attributes.adoc
```

### With URL Transposition

```bash
# Single transposition
validate-links --transpose "https://docs.example.com--https://preview.docs.example.com"

# Multiple transpositions
validate-links \
  --transpose "https://docs.redhat.com--https://preview.docs.redhat.com" \
  --transpose "https://access.redhat.com--https://stage.access.redhat.com" \
  --transpose "https://console.redhat.com--https://console.stage.redhat.com"
```

## Advanced Usage

### Full Configuration Example

```bash
validate-links \
  --transpose "https://docs.redhat.com--https://preview.docs.redhat.com" \
  --transpose "https://access.redhat.com--https://stage.access.redhat.com" \
  --attributes-file common-attributes.adoc \
  --scan-dir modules \
  --scan-dir assemblies \
  --timeout 15 \
  --retry 3 \
  --parallel 20 \
  --cache-duration 7200 \
  --exclude-domain localhost \
  --exclude-domain example.com \
  --verbose \
  --output validation-report.json \
  --format json
```

### CI/CD Integration

```bash
# Fail the build if broken links are found
validate-links \
  --transpose "$PROD_URL--$PREVIEW_URL" \
  --fail-on-broken \
  --format junit \
  --output test-results.xml
```

### No Cache Mode

```bash
# Force fresh validation (useful in CI)
validate-links --no-cache --transpose "https://prod.com--https://staging.com"
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--transpose URL` | Transpose URLs from production to preview/staging (format: from--to) | None |
| `--attributes-file FILE` | Path to AsciiDoc attributes file | Auto-detect |
| `--scan-dir DIR` | Directory to scan (can be used multiple times) | Current dir |
| `--timeout SECONDS` | Timeout for each URL check | 10 |
| `--retry COUNT` | Number of retries for failed URLs | 3 |
| `--parallel COUNT` | Number of concurrent URL checks | 10 |
| `--cache-duration SECONDS` | How long to cache results | 3600 |
| `--exclude-domain DOMAIN` | Domain to skip (can be used multiple times) | None |
| `--no-cache` | Disable result caching | False |
| `--output FILE` | Save results to file | Console |
| `--format FORMAT` | Output format: text, json, junit | text |
| `--verbose` | Show detailed output including warnings | False |
| `--fail-on-broken` | Exit with error code if broken links found | False |

## Output Examples

### Standard Output

```
Validating links in documentation...
Loading attributes from common-attributes.adoc

URL Transposition Rules:
  https://docs.redhat.com → https://preview.docs.redhat.com
  https://access.redhat.com → https://stage.access.redhat.com

Found 247 links to validate

SUMMARY:
✓ Valid: 235 links
✗ Broken: 8 links
⚠ Warnings: 4 redirects

BROKEN LINKS:

1. modules/install.adoc:45
   Original: https://docs.redhat.com/v2/guide.html
   Checked:  https://preview.docs.redhat.com/v2/guide.html
   Status: 404

2. modules/config.adoc:78
   URL: xref:../assemblies/missing.adoc[Configuration]
   Error: File not found
```

### JSON Output

```json
{
  "summary": {
    "total": 247,
    "valid": 235,
    "broken": 8,
    "warnings": 4,
    "skipped": 0
  },
  "transpositions": [
    {
      "from": "https://docs.redhat.com",
      "to": "https://preview.docs.redhat.com"
    }
  ],
  "broken_links": [
    {
      "file": "modules/install.adoc",
      "line": 45,
      "url": "https://docs.redhat.com/v2/guide.html",
      "transposed_url": "https://preview.docs.redhat.com/v2/guide.html",
      "status": 404,
      "error": "Not Found"
    }
  ]
}
```

## How It Works

### Link Extraction

The tool scans `.adoc` files for:
- **External links**: `link:https://example.com[Text]`
- **Cross-references**: `xref:file.adoc[Text]` or `xref:#anchor[Text]`
- **Images**: `image::path/to/image.png[Alt text]`

### Attribute Resolution

Before validation, the tool:
1. Loads attributes from the specified file
2. Resolves nested attributes recursively
3. Replaces `{attribute}` references with actual values

Example:
```asciidoc
:base-url: https://docs.example.com
:version: v2.0
:api-url: {base-url}/{version}/api

link:{api-url}/guide.html[API Guide]
// Resolves to: https://docs.example.com/v2.0/api/guide.html
```

### Validation Process

1. **Extract** - Find all links in .adoc files
2. **Resolve** - Replace attributes with values
3. **Transpose** - Apply URL transposition rules
4. **Validate** - Check each link:
   - External URLs: HTTP status check
   - Internal refs: File existence check
   - Images: Path verification
5. **Report** - Generate formatted output

## Performance Considerations

- **Parallel checking**: Default 10 concurrent checks (adjustable)
- **Caching**: Results cached for 1 hour by default
- **Retry logic**: Exponential backoff for transient failures
- **Timeout**: 10 seconds per URL (adjustable)

Cache is stored in `~/.cache/doc-utils/link-validation.json`

## Known Limitations

⚠️ **EXPERIMENTAL LIMITATIONS**:
- Anchor validation within files not yet implemented
- JUnit output format is planned but not yet available
- Rate limiting for specific domains not yet configurable
- No support for authentication-required URLs

## Troubleshooting

### Timeout Issues
Increase timeout for slow servers:
```bash
validate-links --timeout 30 --retry 5
```

### Too Many Parallel Connections
Some servers limit concurrent connections:
```bash
validate-links --parallel 5
```

### Cache Issues
Clear cache by disabling it:
```bash
validate-links --no-cache
```

### SSL/Certificate Issues
The tool uses standard Python urllib which respects system certificates.

## Integration Examples

### GitHub Actions

```yaml
name: Validate Documentation Links

on:
  pull_request:
    paths:
      - '**.adoc'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install doc-utils
        run: pip install rolfedh-doc-utils

      - name: Validate links against preview
        run: |
          validate-links \
            --transpose "${{ vars.PROD_URL }}--${{ vars.PREVIEW_URL }}" \
            --attributes-file common-attributes.adoc \
            --fail-on-broken
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating documentation links..."
validate-links \
  --transpose "https://docs.example.com--https://preview.docs.example.com" \
  --exclude-domain localhost \
  --fail-on-broken

if [ $? -ne 0 ]; then
  echo "❌ Broken links found. Please fix before committing."
  exit 1
fi
```

## Feedback

As this is an **EXPERIMENTAL** feature, your feedback is valuable:
- Report issues: [GitHub Issues](https://github.com/rolfedh/doc-utils/issues)
- Feature requests welcome
- Share your use cases

## Related Tools

- [extract-link-attributes](extract-link-attributes.md) - Extract links into reusable attributes
- [replace-link-attributes](replace-link-attributes.md) - Replace attributes in URLs with resolved values
- [find-unused-attributes](find-unused-attributes.md) - Find unused attribute definitions