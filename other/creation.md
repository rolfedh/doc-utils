---
layout: default
title: Creating Tools with Claude Code
nav_order: 5
---

# Creating Tools with Claude Code: A Walkthrough

This document shows how a technical writer can use Claude Code to build a documentation tool from scratch. We'll walk through the creation of `insert-procedure-title`, a tool that fixes Vale warnings by inserting `.Procedure` block titles in AsciiDoc files.

## The Starting Point

It began with a Vale warning. [Vale](https://vale.sh/) is a linter for prose that enforces style rules in documentation:

```
modules/proc_advanced-configuration-mapping.adoc
1:1  warning  The '.Procedure' block title is missing.  AsciiDocDITA.TaskContents
```

The goal: create a tool that automatically inserts `.Procedure` before numbered steps in procedure files.

## Step 1: Describe the Problem

The first prompt to Claude Code:

```
Look at proc_advanced-configuration-mapping.adoc.
Vale generated the following warning:

 modules/proc_advanced-configuration-mapping.adoc
 1:1  warning  The '.Procedure' block title is missing.    AsciiDocDITA.TaskContents

Read ~/doc-utils/CLAUDE.md and then create a script in ~/doc-utils that inserts
a .Procedure block title above the numbered steps in the target file.
```

**What worked well:**
- Pointed to the specific file with the problem
- Included the exact error message (copy-pasted from Vale output)
- Referenced CLAUDE.md for project context
- Described the desired outcome

**What could be better:**

```
Look at proc_advanced-configuration-mapping.adoc.
Vale generated the following warning:

 modules/proc_advanced-configuration-mapping.adoc
 1:1  warning  The '.Procedure' block title is missing.    AsciiDocDITA.TaskContents

Read ~/doc-utils/CLAUDE.md and then create a script in ~/doc-utils that inserts
a .Procedure block title above the numbered steps in the target file.

Also look at proc_adding-yaml-configuration-support.adoc as an example of a
procedure file that already has the correct .Procedure block title.
```

Adding an example of the *correct* format helps Claude understand the goal without guessing.

## Step 2: Claude Explores the Codebase

Before writing any code, Claude:

1. **Read the target file** to understand its structure
2. **Read CLAUDE.md** to learn project conventions (naming, structure, installation)
3. **Found other procedure files** to understand the pattern
4. **Examined files with `.Procedure`** to see the expected format

This exploration revealed:
- Procedure files have `:_mod-docs-content-type: PROCEDURE`
- Steps use AsciiDoc ordered list format (`. Step text`)
- `.Procedure` appears on its own line before the steps

## Step 3: First Draft

Claude created `insert_procedure_title.py` with:
- Detection of procedure files
- Finding numbered steps
- Checking for existing `.Procedure`
- Inserting the block title if missing
- Dry-run and verbose modes

## Step 4: Testing Revealed Issues

Running the script on the original file:

```
$ insert-procedure-title modules/proc_advanced-configuration-mapping.adoc --dry-run
No changes needed: modules/proc_advanced-configuration-mapping.adoc
```

The file had no numbered steps—it was incomplete. The script silently did nothing.

**The actual feedback given to Claude:**

```
modules/proc_advanced-configuration-mapping.adoc doesn't have any numbered steps.
In this case, the script should print a warning to stderr.
```

**What could be better:**

```
modules/proc_advanced-configuration-mapping.adoc doesn't have any numbered steps.
In this case, the script should:
1. Print a warning to stderr identifying the file
2. Continue processing other files
3. Summarize how many files had this issue at the end

This helps writers identify incomplete procedure files that need content added.
```

Being explicit about the desired behavior (warn but continue, summarize at end) saves a round of iteration.

## Step 5: Iterating on the Design

Claude updated the script to:
- Detect when a procedure file has no numbered steps
- Print a warning for incomplete files
- Track and summarize warnings at the end

New output:

```
Warning: Procedure file has no numbered steps: modules/proc_advanced-configuration-mapping.adoc

Complete. 0 file(s) modified.
Warnings: 1 procedure file(s) have no numbered steps.
```

## Step 6: Finding Edge Cases

Testing on a larger set of files revealed a false positive—a file that already had `.Procedure` was flagged for modification. The issue: the file had sub-headings between `.Procedure` and the actual steps.

Claude fixed the detection logic to continue searching backward past other block titles until hitting a section heading.

## Step 7: More Edge Cases During Validation

Running the tool on the full modules directory showed 12 warnings. Reviewing these revealed another pattern: some procedure files use unordered lists (`*` bullets) instead of numbered steps, but they already have `.Procedure`:

```asciidoc
.Procedure

* Use a method to access the value of a configuration property...
```

These files don't need modification—they're valid procedures, just using a different list style.

**The prompt:**

```
Update insert-procedure-title to ignore files that contain `.Procedure`.
In some cases, like this one, a procedure consists of an unordered list.
```

Claude updated the logic to check for an existing `.Procedure` title *before* warning about missing numbered steps. The warnings dropped from 12 to 4—the remaining files genuinely need attention.

**Key insight:** Validation doesn't end when the tool "works." Running it on real content at scale often reveals assumptions that don't hold. In this case, the assumption was that all procedures use numbered steps.

## Step 8: Installation and Integration

With the script working (the first time), the next prompt was simply:

```
install pipx
```

Claude knew from CLAUDE.md to run:

```bash
cd /home/rdlugyhe/doc-utils
rm -rf build/ *.egg-info
pipx install --force --editable .
```

When stale symlinks caused warnings, the follow-up was:

```
yes
```

(In response to Claude asking "Want me to clean those up?")

**What could be better:**

```
Add insert-procedure-title to pyproject.toml and install with pipx.
```

Being explicit about adding to pyproject.toml ensures Claude doesn't forget that step. In this case, Claude handled it correctly because CLAUDE.md documents the process.

## Step 9: Documentation

The prompt for documentation:

```
create user docs for insert-procedure-title in ~/doc-utils/docs
```

Claude:
1. Read an existing tool doc (`insert-abstract-role.md`) to match the format
2. Checked nav_order values to pick the next number
3. Created `docs/tools/insert-procedure-title.md` with examples and use cases
4. Updated `docs/tools/index.md` with the new tool entry

**What could be better:**

```
Create user docs for insert-procedure-title in ~/doc-utils/docs/tools/.
Follow the format of insert-abstract-role.md since it's a similar tool.
Include before/after examples showing the .Procedure insertion.
```

Pointing to a specific template and requesting examples helps Claude produce documentation that matches your style.

## Step 10: Validation at Scale

Validation isn't just about refining the tool—it's about completing the work that prompted you to create the tool in the first place. The goal is to resolve the specific Vale error or warning, then move on to the next one.

### Work Through the Warnings

When you run your new tool and see warnings, investigate each one:

```
Warning: Procedure file has no numbered steps and no .Procedure title: modules/proc_advanced-configuration-mapping.adoc
Warning: Procedure file has no numbered steps and no .Procedure title: modules/proc_configuring-quarkus-developer-tools.adoc
```

These warnings aren't failures—they're the tool doing its job. Each warning is a file that needs attention.

### Warnings Reveal Content Issues

In this case, investigating the warnings revealed **orphaned stub files**. The file `proc_advanced-configuration-mapping.adoc` contained only:

```asciidoc
:_mod-docs-content-type: PROCEDURE
[id="proc_advanced-configuration-mapping"]

= Advanced configuration mapping

[role="_abstract"]
The following advanced mapping procedure is an extension that is specific to {ProductLongName} and outside of the MicroProfile Config specification.
```

No actual procedure content—just a title and abstract. This stub was acting as a section heading in the assembly, with a real procedure nested under it at `leveloffset=+2`.

### Fix the Content, Not Just the Warning

Instead of adding an empty `.Procedure` section to silence the warning, we analyzed the assembly structure:

```asciidoc
include::modules/proc_advanced-configuration-mapping.adoc[leveloffset=+1]

include::modules/proc_using-nested-object-configuration.adoc[leveloffset=+2]
```

The stub was a parent heading with the actual content as a child. The fix:

1. **Incorporated useful context** from the stub's abstract into the child procedure
2. **Deleted the stub file**
3. **Adjusted the leveloffset** from `+2` to `+1`

The same pattern appeared with `proc_configuring-quarkus-developer-tools.adoc`—another stub with no content, nested procedures underneath. Same solution: evaluate whether to incorporate content, delete the stub, flatten the hierarchy.

### Enhance the Tool When Patterns Emerge

As you work through warnings, you might discover additional use cases:

- **Files with unordered lists** instead of numbered steps but already have `.Procedure`—the tool shouldn't warn about these
- **Stub files** that are technically PROCEDURE type but serve as section headings—these might warrant a different warning message

Each pattern can enhance the tool's accuracy. But don't get distracted perfecting the tool—complete the content work first, then circle back to tool improvements.

### Close the Loop with Vale

When you've finished running your utility and manually fixing any issues the utility can't address, rerun Vale on the same set of files. This confirms that your work has resolved every instance of the original issue:

```bash
vale modules/ 2>&1 | grep TaskContents
```

If the output is empty, you've cleared that Vale rule. Move on to the next one.

## The Role of CLAUDE.md

The `CLAUDE.md` file in the project root is crucial for consistent results. It tells Claude:

- **Project structure**: Where files go, naming conventions
- **Installation method**: Use pipx, how to upgrade in development
- **Entry points**: How to add new CLI commands to `pyproject.toml`
- **Documentation patterns**: Where docs live, what format to use
- **Testing approach**: How to run tests, what to test

Without CLAUDE.md, you'd need to explain these conventions in every prompt. With it, Claude follows project standards automatically.

**Example from doc-utils CLAUDE.md:**

```markdown
### CLI Tools

1. **validate-links** - Validates all links in documentation
2. **archive-unused-files** - Finds and archives unreferenced files
...

### Documentation Updates for New Features

When adding a new tool or feature:

1. Create tool documentation in `docs/tools/[tool-name].md`
2. Update `docs/tools/index.md`
3. Update README.md
4. Update CLAUDE.md (this file)
```

## Lessons for Technical Writers

### 1. Start with the Error Message

Real problems make the best prompts. "Fix this Vale warning" is clearer than "write a tool that might be useful someday."

### 2. Point Claude to Context

Reference specific files:
- The file with the problem
- Similar files that show the correct pattern
- Project documentation (CLAUDE.md, README)

### 3. Test Early, Iterate Often

Don't wait for a "perfect" script. Run it quickly on real files. Edge cases emerge from actual usage, not imagination.

### 4. Give Specific Feedback

Instead of "this doesn't work," explain:
- What you expected
- What actually happened
- Why that's wrong

**Weak feedback:**
```
This doesn't work right.
```

**Strong feedback:**
```
The script says "No changes needed" for proc_example.adoc, but that file
doesn't have a .Procedure title. Expected: a warning message explaining
that the file has no numbered steps.
```

### 5. Let Claude Explore

Claude's exploration phase—reading files, searching for patterns—often catches things you'd miss. Don't skip straight to "write the code."

### 6. Invest in CLAUDE.md

A well-maintained CLAUDE.md pays dividends every time you work with Claude on the project. See [The Role of CLAUDE.md](#the-role-of-claudemd) for what to include.

### 7. Short Prompts Work When Context Exists

Notice how later prompts got shorter:
- `install pipx`
- `yes`
- `create user docs for insert-procedure-title in ~/doc-utils/docs`

Once CLAUDE.md establishes context and Claude has read the relevant files, you can be terse. Early prompts should be detailed; later prompts can be conversational.

## The Complete Workflow

```
1. Identify problem (Vale warning, repetitive task, etc.)
     ↓
2. Describe to Claude with context (files, error messages, goals)
     ↓
3. Claude explores codebase and creates first draft
     ↓
4. Test on real files
     ↓
5. Report issues with specific feedback
     ↓
6. Claude iterates
     ↓
7. Repeat 4-6 until working
     ↓
8. Install and integrate
     ↓
9. Document
     ↓
10. Validate at scale → back to step 5 if needed
```

The last step is important: running the tool on a larger set of files often reveals assumptions that don't hold. In this case, validation after documentation led to another round of refinement.

## Try It Yourself

1. **Find a repetitive documentation task.** Good starting points include:
   - Fixing consistent formatting issues flagged by your linter
   - Validating file naming conventions across a directory
   - Generating link inventories or checking for broken references
   - Inserting required metadata or frontmatter into files
   - Converting between markup formats (Markdown to AsciiDoc, etc.)

2. **Create or update your project's CLAUDE.md** with naming conventions, directory structure, and common commands.

3. **Describe the task to Claude with specific examples**—include a file with the problem and a file showing the correct format.

4. **Test, give feedback, iterate.** Run on real files early. Report what you expected vs. what happened.

5. **Document what you built** so future you (and teammates) can use it.

The best way to learn is to build something you actually need.
