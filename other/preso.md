# Claude for Technical Writers: From Tedious Tasks to Creative Partner

---

## Presentation Blurb

Technical writers spend too much time on repetitive, mechanical tasks—and not enough time crafting content that helps users succeed. In this session, you'll learn how to use Claude to automate the tedium, analyze large doc sets, and collaborate on content creation. Through real-world examples, we'll explore how to identify tasks ripe for automation, build and validate your own tools, and use Claude as a writing copilot without losing your editorial voice. Whether you're new to AI or already experimenting, you'll leave with practical techniques you can apply this week.

---

## About the Presenter

Rolfe Dlugy-Hegwer is a Technical Content Professional at IBM and former Principal Technical Writer at Red Hat. With 30 years in technical communication, he has documented enterprise Java platforms, cloud-native frameworks, and developer tools. Rolfe combines deep domain expertise in Quarkus and Java technologies with a passion for process improvement—building open-source tools that help documentation teams work smarter. He believes the future of technical writing lies not in fearing AI, but in harnessing it to focus on what humans do best: understanding users and crafting content that meets their needs.

---

## Presentation Outline (20 minutes)

---

## Opening: The Technical Writer's Dilemma (2 min)

- We spend significant time on repetitive, mechanical tasks
- Manual processes are error-prone and draining
- Time spent on tedium = time not spent on user-focused content
- **Thesis**: Claude can automate tedium, analyze at scale, and collaborate on content—freeing you to focus on users

---

## Part 1: Scratch Your Itch — Automating Repetitive Tasks (5 min)

### What Makes a Good Candidate

Look for tasks that are:
- **Frequent**: You do them weekly, daily, or per-document
- **Rule-based**: You can describe the logic in plain language
- **Broad**: They apply across many files
- **Recoverable**: Mistakes would be caught in review

**Examples from doc-utils:**
- `insert-abstract-role` — Adding required metadata to hundreds of files
- `convert-callouts-to-deflist` — Transforming markup patterns across a doc set

### Building Tools with Claude

1. **Start with a conversation**: Describe what you need in plain language
2. **Iterate in small steps**: Get one case working, then expand
3. **Test on real files**: Use your actual content, not hypotheticals
4. **Review the output**: Claude makes mistakes — verify before bulk runs
5. **Get peer review**: Have colleagues test on their content

**Demo**: Live walkthrough of creating `insert-procedure-title`—describe the Vale warning, show Claude generating the script, run it on a test file

---

## Part 2: Analysis and Reporting Tools (4 min)

### When Information Overload Hits

- Large doc sets become impossible to audit manually
- Patterns and problems hide in the noise
- Stakeholders want data, not guesswork

**Examples from doc-utils:**
- `find-duplicate-content` — Identifying reuse opportunities
- `find-unused-attributes` — Cleaning up cruft

### Building Analysis Tools

1. **Define what you're looking for**: Be specific about the pattern
2. **Start with a report**: Get visibility before automation
3. **Add filtering**: Reduce noise to find signal
4. **Make it actionable**: Output should tell you what to fix

---

## Part 3: Claude as Your Writing Copilot (6 min)

### Content Creation Workflows

**Example: Migration guide project** (`migration-from-java-ee-to-quarkus`)
- Research and synthesis: Gathering information from multiple sources
- Drafting: Getting a first pass on the page
- Restructuring: Reorganizing content for clarity
- Editing: Refining voice, tone, and precision

### Working Effectively with Claude

1. **Be specific**: "Fix this" → "Rewrite this paragraph to emphasize the user benefit"
2. **Provide context**: Share your style guide, audience, constraints
3. **Show examples**: "Write it like this example" beats abstract descriptions
4. **Work in chunks**: Draft section by section, not whole documents
5. **Iterate**: First response is a starting point—refine through conversation
6. **Use CLAUDE.md**: Store persistent context so you don't repeat yourself

### Know the Boundaries

**Claude excels at:**
- First drafts and brainstorming
- Summarizing technical content
- Rewriting for different audiences
- Addressing reviewer feedback

**You stay in control of:**
- Final editing for voice and brand
- Accuracy verification (Claude can confidently state incorrect information)
- Structural decisions for your specific users
- Anything requiring deep product knowledge

---

## Closing: Start Small, Think Big (1 min)

### Your First Steps

1. Pick one repetitive task this week
2. Describe it to Claude and see what happens
3. Test, iterate, and share what you learn

### The Bigger Picture

- AI won't replace technical writers
- AI will change what technical writing *is*
- The writers who thrive will be the ones who adapt their workflow

**Call to action**: What's the most tedious part of your week? That's where to start.

---

## Q&A / Discussion

**Possible discussion prompts:**
- What repetitive tasks do you wish you could automate?
- What concerns do you have about using AI in your workflow?
- How do you verify AI-generated content?

---

## Resources

- doc-utils repository: https://github.com/rdlugyhe/doc-utils
- Claude.ai (web interface): https://claude.ai
- Claude Code (CLI for tool building): https://docs.anthropic.com/claude-code
- Anthropic prompt engineering guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

---

## Notes for Presenter

**Target audience:**
Technical writers familiar with generative AI (ChatGPT, Claude, etc.) for basic tasks like drafting and editing, but who haven't yet used AI to build custom tools or scripts.

**Timing breakdown:**
- Opening: 2 min
- Part 1 (Automation): 5 min
- Part 2 (Analysis): 4 min
- Part 3 (Copilot): 6 min
- Closing: 1 min
- **Total: 18 min** (leaves 2 min buffer for transitions or Q&A)

**Demo plan:**
- Live demo: Create `insert-procedure-title` from a Vale warning
- Backup: Pre-recorded version if live demo fails
- Have test files ready in a clean directory

**Slide estimate: 10-12 slides**
- Title slide (1)
- Opening/thesis (1)
- Part 1: Automation (2-3, including demo screenshot)
- Part 2: Analysis (1-2)
- Part 3: Copilot (2-3)
- Closing + call to action (1)
- Resources (1)

---

## Concise Blurb

Technical writers spend too much time on repetitive tasks and not enough time helping users succeed. In this session, you'll learn how to use Claude to automate tedious work, analyze large doc sets, and collaborate on content—without losing your editorial voice. You'll leave with practical techniques you can apply this week.

---

## Concise Bio

Rolfe Dlugy-Hegwer is a Technical Content Professional at IBM and former Principal Technical Writer at Red Hat. Over 30 years, he has documented enterprise Java platforms and cloud-native frameworks while building open-source tools that help documentation teams work smarter. He believes the future of technical writing lies in harnessing AI to focus on what humans do best: understanding users.
