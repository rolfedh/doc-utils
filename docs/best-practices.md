---
layout: default
title: Best Practices
nav_order: 13
---

# Best Practices for Using doc-utils

Following these best practices will help you safely and effectively use doc-utils to maintain your documentation.

## Safety First

### Always Work in a Git Branch

**Never run doc-utils tools on your main/master branch.** Always create a feature branch first:

```bash
# Create a new branch with today's date
git checkout -b doc-cleanup-$(date +%Y%m%d)

# Or create a descriptive branch
git checkout -b remove-unused-images
```

### Commit Before Running Tools

Save your current work before running any doc-utils commands:

```bash
git add -A
git commit -m "Save work before doc-utils cleanup"
```

### Use Preview Modes

Most tools have a preview or dry-run mode. Always use these first:

```bash
# Preview what would be formatted
format-asciidoc-spacing --dry-run modules/

# Preview what would be archived (default behavior)
archive-unused-files
archive-unused-images

# Only after reviewing, actually archive
archive-unused-files --archive
```

## Workflow Recommendations

### 1. Initial Assessment

Start by understanding the current state of your documentation:

```bash
# Check readability issues
check-scannability

# Find unused content (preview mode)
archive-unused-files
archive-unused-images

# Check for unused attributes
find-unused-attributes attributes.adoc
```

### 2. Plan Your Changes

Based on the assessment:
- Prioritize which issues to address
- Consider the impact on your documentation
- Plan to fix issues in logical groups

### 3. Execute Changes Incrementally

Don't try to fix everything at once:

```bash
# Format spacing first
format-asciidoc-spacing --dry-run .
format-asciidoc-spacing .
git add -A && git commit -m "Standardize AsciiDoc spacing"

# Then handle unused files
archive-unused-files --archive
git add -A && git commit -m "Remove unused AsciiDoc files"

# Finally, unused images
archive-unused-images --archive
git add -A && git commit -m "Remove unused images"
```

### 4. Verify Your Documentation

After each change:

```bash
# Review the changes
git diff HEAD~1

# Build your documentation
# (run your build command here)

# Test key pages manually
# (check important documentation pages)
```

## Exclusion Strategies

### Create a Project-Wide Exclusion File

Create a `.docutils-ignore` file in your repository root:

```
# Directories to always exclude
./archives/
./deprecated/
./work-in-progress/
./_build/
./node_modules/

# Specific files to exclude
./README.adoc
./CONTRIBUTING.adoc
./templates/*

# Temporary content
*-draft.adoc
*-backup.adoc
```

### Use Consistent Exclusion Patterns

Apply the same exclusions across all tools:

```bash
# Create an alias for common exclusions
alias docutils-clean='--exclude-list .docutils-ignore'

# Use consistently
check-scannability $docutils-clean
archive-unused-files $docutils-clean
```

## Repository-Specific Considerations

### OpenShift-docs Style Repositories

For repositories using topic maps:

1. Ensure `_topic_maps/*.yml` files are up to date
2. Validate YAML syntax before running tools
3. Consider topic map structure when reviewing unused files

### Traditional AsciiDoc Repositories

For repositories using master.adoc:

1. Verify all master.adoc files are tracked
2. Check include paths are correct
3. Consider modular documentation structure

## Performance Tips

### Process Directories Selectively

Instead of processing everything:

```bash
# Process specific directories
format-asciidoc-spacing modules/getting-started/

# Use --scan-dir for archive tools
archive-unused-files --scan-dir ./modules/api-reference
```

### Batch Similar Operations

Group similar changes together:

```bash
# Format all modules at once
format-asciidoc-spacing modules/

# Rather than one at a time
format-asciidoc-spacing modules/chapter1/
format-asciidoc-spacing modules/chapter2/
```

## Troubleshooting Common Issues

### "Command not found"

Add the installation directory to PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission Denied

Ensure scripts are executable:

```bash
chmod +x ~/.local/bin/format_asciidoc_spacing.py
```

### Unexpected File Deletion

If you accidentally delete files:

1. Check the `.archive` directory for backups
2. Use git to restore: `git checkout -- <file>`
3. Review the manifest file in the archive

### Build Failures After Cleanup

If documentation fails to build after using doc-utils:

1. Check for broken include references
2. Verify required files weren't marked as unused
3. Review the exclusion list for missing entries
4. Use git to revert problematic changes

## Integration with CI/CD

### Add Formatting Checks

Include formatting checks in your CI pipeline:

```yaml
# Example GitHub Actions workflow
- name: Check AsciiDoc formatting
  run: |
    format-asciidoc-spacing --dry-run .
    if [ $? -ne 0 ]; then
      echo "Documentation needs formatting"
      exit 1
    fi
```

### Regular Maintenance

Schedule regular documentation maintenance:

```yaml
# Monthly cleanup workflow
on:
  schedule:
    - cron: '0 0 1 * *'  # First day of each month
```

## Documentation Standards

### Establish Team Guidelines

Define standards for your team:

1. Maximum sentence length (e.g., 25 words)
2. Maximum paragraph length (e.g., 4 sentences)
3. Required spacing around elements
4. Image organization structure

### Document Your Decisions

Keep a record of:
- Why certain files are excluded
- Rationale for readability limits
- Archive retention policy
- Tool configuration choices

## Regular Maintenance Schedule

### Weekly Tasks
- Run `check-scannability` to monitor readability
- Review any new unused attributes

### Monthly Tasks
- Run `archive-unused-files` in preview mode
- Check for unused images
- Format new documentation with `format-asciidoc-spacing`

### Quarterly Tasks
- Actually archive unused content
- Review and update exclusion lists
- Assess tool configuration for improvements

## Getting Help

When you need assistance:

1. Check tool help: `<tool-name> --help`
2. Review error messages carefully
3. Test with a small subset of files first
4. [Open an issue](https://github.com/rolfedh/doc-utils/issues) with details

Remember: These tools are meant to help maintain documentation quality. Use them thoughtfully and always verify their output before committing changes.