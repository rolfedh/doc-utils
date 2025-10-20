# Callout Converter: Long Comment Handling - Testing Request

Hey team! 👋

I've just implemented a feature to handle callout descriptions that are too long to work well as inline comments. I'd love your feedback on the approach and which option you think works best.

## What's New

When converting callouts to **inline comments** format, the tool now detects when explanations are too long (default: 120 characters) and provides options for handling them.

### Current Implementation

**Batch Tool (`convert-callouts-to-deflist --format comments`)**
- Automatically falls back to definition list format when comments exceed max length
- Displays warning showing which callouts are too long
- New `--max-comment-length` parameter to adjust the threshold (default: 120)

Example:
```bash
convert-callouts-to-deflist --format comments modules/
# WARNING: myfile.adoc lines 15-25: Callout <1> explanation too long (145 chars)
# for inline comment (max: 120). Falling back to definition list format.
```

**Interactive Tool (`convert-callouts-interactive`)**
- Detects long comments before conversion
- Prompts with these options:
  - **[s] Shorten** - Use first sentence only
  - **[d] Definition list** - Use deflist format instead
  - **[b] Bulleted list** - Use bullets format instead
  - **[k] Skip** - Leave this block unchanged

Example interaction:
```
⚠️  WARNING: Long Comment Detected

  Callout <1>: 145 characters
  Text: This method initializes the database connection pool with the specified configuration parameters and...

This explanation is too long for a readable inline comment.

What would you like to do?
  [s] Use Shortened version (first sentence only)
  [d] Use Definition list format instead
  [b] Use Bulleted list format instead
  [k] Skip this block
  [q] Quit

Your choice [s/d/b/k/q]:
```

## Alternative Approaches Considered

I evaluated several options. Here's the full list with pros/cons:

### Option 1: Truncation with Ellipsis ❌
```java
public void method() { // This is a very long explanation that gets tru...
```
**Pros:** Simple, preserves inline format
**Cons:** Loses information, looks incomplete, not very professional

### Option 2: Multi-line Comments ⚠️
```java
/* This is a very long explanation that describes
   the method in detail and continues on multiple
   lines for better readability */
public void method() {
```
**Pros:** Preserves all text, readable
**Cons:** Disrupts code flow, takes up vertical space, not all languages support block comments well

### Option 3: Hybrid Approach ⚠️
Keep short explanations as inline, preserve long ones as definition lists:
```asciidoc
[source,java]
----
public void shortMethod() { // Brief explanation
public void complexMethod() { <1>
----
<1> This is a very long explanation that requires multiple sentences...
```
**Pros:** Best of both worlds
**Cons:** Inconsistent formatting within same code block, confusing

### Option 4: Smart Extraction (First Sentence) ✅
```java
public void method() { // Main method entry point.
```
Original: "Main method entry point. This method is called when the application starts and handles initialization..."

**Pros:** Clean, preserves key information, natural looking
**Cons:** Might lose context, author must write good first sentences

### Option 5: Interactive Warning + Skip ✅ **IMPLEMENTED**
Prompt user to choose for each long comment in interactive mode.

**Pros:** User control, context-aware decisions, flexible
**Cons:** Requires user interaction (not suitable for batch mode)

### Option 6: Automatic Fallback with Parameter ✅ **IMPLEMENTED**
Fall back to definition list when threshold exceeded, with configurable max length.

**Pros:** Automated, consistent, configurable
**Cons:** Less control than interactive, might surprise users

## What I'm Looking For

1. **Does the interactive workflow make sense?** Is the prompt clear about what each option does?

2. **Is 120 characters the right threshold?** Too strict? Too lenient?

3. **Should the batch tool offer more options?** Currently it just falls back to deflist. Should it:
   - Support auto-shortening (`--shorten-long-comments` flag)?
   - Allow choosing fallback format (`--long-comment-fallback {deflist|bullets|skip}`)?

4. **Is the "shorten" option useful?** Or should we just offer format fallbacks?

5. **Any other approaches** I should consider?

## Testing

I've created test files in `/home/rdlugyhe/doc-utils/`. You can test with:

```bash
# Test batch mode with comments
python3 convert_callouts_to_deflist.py --format comments --verbose test_file.adoc

# Test batch mode with custom threshold
python3 convert_callouts_to_deflist.py --format comments --max-comment-length 80 test_file.adoc

# Test interactive mode
python3 convert_callouts_interactive.py test_file.adoc
# Choose 'c' for comments format, and you'll get prompted if comments are too long
```

## Example Scenarios

**Scenario 1: YAML with brief descriptions**
```yaml
database:
  host: localhost <1>
  port: 5432 <2>
```
<1> Database hostname
<2> Database port number

→ **Works great as inline comments** (short, simple)

**Scenario 2: Java with detailed explanations**
```java
@BasicAuthentication <1>
public String endpoint() {
```
<1> Enables basic authentication for this endpoint. Authentication credentials are validated against the configured identity provider and the user's roles are checked against the method's security annotations.

→ **Too long for inline comment** (145 chars)
- Batch: Automatically falls back to definition list
- Interactive: Prompts user to choose

**Scenario 3: Shell script with technical details**
```bash
docker run -p 8080:8080 myimage <1>
```
<1> Maps container port 8080 to host port 8080, allowing external access to the application

→ **Borderline** (96 chars, under threshold)
- Currently converts to inline comment
- Readable but a bit long

## Questions for Discussion

1. Should we have different thresholds for different file types (e.g., longer for YAML, shorter for Java)?

2. For the interactive tool, should we show a preview of what the shortened version would look like before the user chooses?

3. Should we collect metrics on how often long comments occur to better set the default threshold?

Thanks for taking a look! Let me know your thoughts on which approach feels most natural for your workflow.

---

**Files changed:**
- `callout_lib/converter_comments.py` - Added length detection and shortening
- `convert_callouts_to_deflist.py` - Added `--max-comment-length` parameter
- `convert_callouts_interactive.py` - Added interactive long comment handling

**Documentation:**
- See `IMPLEMENTATION_SUMMARY.md` for technical details
