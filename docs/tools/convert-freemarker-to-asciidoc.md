---
layout: default
title: convert-freemarker-to-asciidoc
nav_order: 13
---

# convert-freemarker-to-asciidoc

A Python utility that converts FreeMarker-templated AsciiDoc files to standard AsciiDoc format. This tool is designed for converting documentation that uses FreeMarker Template Language (FTL) embedded in AsciiDoc, such as Keycloak documentation, to plain AsciiDoc that can be used with other documentation toolchains.

## Purpose

Some documentation projects use FreeMarker templates embedded in AsciiDoc files to generate documentation at build time. This allows for:
- Conditional content based on product editions
- Reusable templates for common patterns
- Dynamic cross-references between documents
- Auto-generated command examples

However, this FreeMarker syntax is not standard AsciiDoc and cannot be processed by standard AsciiDoc toolchains like Asciidoctor or Antora. This tool converts FreeMarker-templated content to standard AsciiDoc.

## Patterns That ARE Converted

The following FreeMarker patterns are reliably converted to standard AsciiDoc:

### Structure Patterns

| Pattern | Conversion |
|---------|------------|
| `<#import "..." as ...>` | Removed |
| `<@tmpl.guide title="..." summary="...">` | `= Title` + summary paragraph |
| `<@template.guide title="..." summary="...">` | `= Title` + summary paragraph |
| `</@tmpl.guide>` | Removed |
| `</@template.guide>` | Removed |

### Link Macros → AsciiDoc xref

| Pattern | Conversion |
|---------|------------|
| `<@links.server id="hostname"/>` | `xref:server/hostname.adoc[]` |
| `<@links.ha id="intro"/>` | `xref:high-availability/intro.adoc[]` |
| `<@links.observability id="metrics"/>` | `xref:observability/metrics.adoc[]` |
| `<@links.securingapps id="client"/>` | `xref:securing-apps/client.adoc[]` |
| `<@links.gettingstarted id="docker"/>` | `xref:getting-started/docker.adoc[]` |
| `<@links.operator id="install"/>` | `xref:operator/install.adoc[]` |
| `<@links.migration id="quarkus"/>` | `xref:migration/quarkus.adoc[]` |

Anchors are also supported: `<@links.server id="hostname" anchor="section"/>` → `xref:server/hostname.adoc#section[]`

### Command Macros → Code Blocks

| Pattern | Conversion |
|---------|------------|
| `<@kc.start parameters="--hostname x"/>` | Code block: `bin/kc.sh start --hostname x` |
| `<@kc.startdev parameters="..."/>` | Code block: `bin/kc.sh start-dev ...` |
| `<@kc.build parameters="--db postgres"/>` | Code block: `bin/kc.sh build --db postgres` |
| `<@kc.export parameters="--dir <dir>"/>` | Code block: `bin/kc.sh export --dir <dir>` |
| `<@kc.import parameters="--file <file>"/>` | Code block: `bin/kc.sh import --file <file>` |
| `<@kc.updatecompatibility parameters="..."/>` | Code block: `bin/kc.sh update-compatibility ...` |
| `<@kc.admin parameters="..."/>` | Code block: `bin/kcadm.sh ...` |
| `<@kc.bootstrapadmin parameters="..."/>` | Code block: `bin/kc.sh bootstrap-admin ...` |

### Conditional Blocks

| Pattern | Conversion |
|---------|------------|
| `<@profile.ifCommunity>...</@profile.ifCommunity>` | Content kept (default) or removed with `--product` |
| `<@profile.ifProduct>...</@profile.ifProduct>` | Content removed (default) or kept with `--product` |

### Other Patterns

| Pattern | Conversion |
|---------|------------|
| `<#noparse>...</#noparse>` | Tags removed, content preserved |
| `<@opts.*>` macros | Replaced with placeholder comment |
| `<@features.table .../>` | Replaced with placeholder comment |

## Patterns That CANNOT Be Converted

The following patterns require dynamic content generation and cannot be reliably converted to static AsciiDoc. They are marked with `// TODO:` comments for manual review:

| Pattern | Reason |
|---------|--------|
| `<#list ...>...</#list>` | Dynamic loops for generating navigation or repeated content |
| `<#if ...>...</#if>` | Conditional logic that depends on build-time context |
| `<#else>` | Part of conditional blocks |
| `<#assign ...>` | Build-time variable assignment |
| `<@kc.*>` without `parameters=""` | Non-standard command syntax |

### Example of Marked Content

After conversion, unconvertible patterns look like this:

```asciidoc
// TODO: Manual conversion required - FreeMarker list loop
// <#list ctx.guides as guide>

include::${guide.template}[leveloffset=+1]
// </#list>
```

## Usage

### Installation

```bash
# Install with pipx for global availability
pipx install rolfedh-doc-utils

# Or upgrade existing installation
pipx upgrade rolfedh-doc-utils
```

### Basic Usage

```bash
# Process all .adoc files in current directory (full conversion)
convert-freemarker-to-asciidoc

# Process specific directory
convert-freemarker-to-asciidoc docs/guides/

# Process single file
convert-freemarker-to-asciidoc docs/guides/server/hostname.adoc
```

### Options

```bash
convert-freemarker-to-asciidoc [OPTIONS] [PATH]

OPTIONS:
    -h, --help           Show help message
    -n, --dry-run        Show what would be changed without modifying files
    -v, --verbose        Show detailed output for each file
    --structure-only     Only convert imports and guide blocks; leave inline macros
    --product            Keep product content in profile blocks (default: community)
    --base-path PATH     Base path prefix for xref links (e.g., "guides")
    --only-freemarker    Only process files containing FreeMarker markup
    --version            Show version information

ARGUMENTS:
    PATH                 File or directory to process (default: current directory)
```

### Examples

**Preview changes without modifying files:**
```bash
convert-freemarker-to-asciidoc --dry-run docs/guides/
```

**Process with detailed output:**
```bash
convert-freemarker-to-asciidoc --verbose docs/guides/
```

**Only convert structure, leave inline macros:**
```bash
convert-freemarker-to-asciidoc --structure-only docs/guides/
```

**Keep product content instead of community:**
```bash
convert-freemarker-to-asciidoc --product docs/guides/
```

**Add base path to xref links:**
```bash
convert-freemarker-to-asciidoc --base-path guides docs/guides/
# Results in: xref:guides/server/hostname.adoc[]
```

**Only process files with FreeMarker content:**
```bash
convert-freemarker-to-asciidoc --only-freemarker docs/
```

## Output Examples

### Dry-run Mode
```
DRY RUN MODE - No files will be modified

Would modify: docs/guides/server/hostname.adoc
Would modify: docs/guides/server/caching.adoc
Would modify: docs/guides/getting-started/index.adoc

Processed 127 AsciiDoc file(s)
Would modify 125 file(s)
  (257 import(s), 97 guide block(s), 261 link(s) -> xref, 120 command(s) -> code,
   42 profile block(s), 24 noparse block(s), 17 opts macro(s), 6 features macro(s),
   57 directive(s) marked, 15 other macro(s))

FreeMarker to AsciiDoc conversion complete!
```

### Verbose Mode
```
Processing: docs/guides/server/hostname.adoc
  Removed 3 FreeMarker import(s)
  Converted guide block to AsciiDoc title/summary
  Removed closing guide tag
  Converted 5 <@links.*> macro(s) to xref
  Converted 12 <@kc.*> macro(s) to code blocks
Modified: docs/guides/server/hostname.adoc

Processed 1 AsciiDoc file(s)
Modified 1 file(s)
  (3 import(s), 1 guide block(s), 5 link(s) -> xref, 12 command(s) -> code)

FreeMarker to AsciiDoc conversion complete!
```

## Conversion Examples

### Guide Block Conversion

**Before:**
```ftl
<#import "/templates/guide.adoc" as tmpl>
<#import "/templates/kc.adoc" as kc>
<#import "/templates/links.adoc" as links>

<@tmpl.guide
title="Configuring {project_name} for production"
summary="Prepare {project_name} for use in production."
includedOptions="">

== TLS for secure communication
...content...

</@tmpl.guide>
```

**After:**
```asciidoc
= Configuring {project_name} for production

Prepare {project_name} for use in production.

== TLS for secure communication
...content...
```

### Link Macro Conversion

**Before:**
```ftl
For details, see <@links.server id="hostname"/>.
See the <@links.ha id="introduction" anchor="overview"/> guide.
```

**After:**
```asciidoc
For details, see xref:server/hostname.adoc[].
See the xref:high-availability/introduction.adoc#overview[] guide.
```

### Command Macro Conversion

**Before:**
```ftl
<@kc.start parameters="--hostname my.keycloak.org"/>
<@kc.export parameters="--dir /backup"/>
```

**After:**
```asciidoc
[source,bash]
----
bin/kc.sh start --hostname my.keycloak.org
----

[source,bash]
----
bin/kc.sh export --dir /backup
----
```

### Profile Block Conversion

**Before:**
```ftl
<@profile.ifCommunity>
This content is for the community edition.
</@profile.ifCommunity>
<@profile.ifProduct>
This content is for the product edition.
</@profile.ifProduct>
```

**After (default - keep community):**
```asciidoc
This content is for the community edition.
```

## Best Practices

### Before Running

1. **Work in a git branch** - Create a feature branch before converting
2. **Commit pending changes** - Ensure your working directory is clean
3. **Use dry-run mode** - Preview changes before applying
4. **Test on sample files** - Start with a single file to verify behavior

### Recommended Workflow

```bash
# Create feature branch
git checkout -b convert-freemarker-docs

# Preview changes
convert-freemarker-to-asciidoc --dry-run --verbose docs/guides/

# Apply changes
convert-freemarker-to-asciidoc --verbose docs/guides/

# Review changes
git diff

# Find items needing manual review
grep -r "// TODO:" docs/guides/

# Commit if satisfied
git add -A
git commit -m "Convert FreeMarker templates to standard AsciiDoc"
```

### Post-Conversion Steps

After running the conversion:

1. **Search for TODO comments** - `grep -r "// TODO:" docs/` to find items needing manual review
2. **Verify xref paths** - Ensure cross-references point to correct files
3. **Check code blocks** - Verify command syntax is correct
4. **Review conditional content** - Ensure correct edition content was kept
5. **Handle index files** - Files with `<#list>` loops need manual conversion
6. **Validate AsciiDoc** - Run through Asciidoctor to check for syntax errors
7. **Update build scripts** - Remove FreeMarker processing from your build pipeline

## Troubleshooting

### Files Not Being Converted

Check if files actually contain FreeMarker markup:
```bash
grep -l '<#import\|<@\w\+\.' docs/guides/*.adoc
```

### Encoding Issues

The tool expects UTF-8 encoded files. Check file encoding:
```bash
file docs/guides/server/hostname.adoc
```

### Unexpected Changes

Use dry-run and verbose mode together:
```bash
convert-freemarker-to-asciidoc --dry-run --verbose single-file.adoc
```

### Wrong Edition Content

By default, community content is kept. Use `--product` to keep product content instead:
```bash
convert-freemarker-to-asciidoc --product docs/guides/
```

### Finding Unconverted Patterns

After conversion, find all items needing manual attention:
```bash
grep -rn "// TODO:" docs/guides/
```

## Related Tools

This tool complements other doc-utils:
- **format-asciidoc-spacing**: Standardize spacing after conversion
- **find-unused-attributes**: Find unused attributes after converting
- **archive-unused-files**: Clean up after documentation restructuring

## Contributing

When contributing improvements:
1. Test with real-world FreeMarker-templated files
2. Preserve all standard AsciiDoc content
3. Handle edge cases gracefully
4. Update examples in this documentation
5. Follow existing code patterns
