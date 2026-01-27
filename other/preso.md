# Claude.ai for Technical Writers: From Tedious Tasks to Creative Partner

---

## Presentation Blurb

Technical writers spend too much time on repetitive, mechanical tasks—and not enough time crafting content that helps users succeed. In this session, you'll learn how to use Claude.ai to automate the tedium, analyze large doc sets, and collaborate on content creation. Through real-world examples, we'll explore how to identify tasks ripe for automation, build and validate your own tools, and use Claude as a writing copilot without losing your editorial voice. Whether you're new to AI or already experimenting, you'll leave with practical techniques you can apply this week.

---

## About the Presenter

Rolfe Dlugy-Hegwer is a Technical Content Professional at IBM and former Principal Technical Writer at Red Hat. With 30 years in technical communication, he has documented enterprise Java platforms, cloud-native frameworks, and developer tools. Rolfe combines deep domain expertise in Quarkus and Java technologies with a passion for process improvement—building open-source tools that help documentation teams work smarter. He believes the future of technical writing lies not in fearing AI, but in harnessing it to focus on what humans do best: understanding users and crafting content that meets their needs.

---

## Presentation Outline (20 minutes)

---

## Opening: The Technical Writer's Dilemma (2 min)

- We spend significant time on repetitive, mechanical tasks
- Manual processes are error-prone and soul-crushing
- Time spent on tedium = time not spent on user-focused content
- **Thesis**: Claude can handle the boring stuff so you can focus on what matters

---

## Part 1: Scratch Your Itch — Automating Repetitive Tasks (5 min)

### Identify the Pain Points

- Tasks you do repeatedly (weekly, daily, per-document)
- Tasks with clear rules but tedious execution
- Pattern-based transformations

**Examples from doc-utils:**
- `insert_abstract_role.py` — Adding required metadata to hundreds of files
- `convert_callouts_to_deflist.py` — Transforming markup patterns across a doc set
- `check_source_directives.py` — Validating consistency

### How to Identify Good Candidates

1. **Frequency**: Do you do this task often?
2. **Rules**: Can you describe the logic in plain language?
3. **Scope**: Does it need to work across many files?
4. **Risk**: Would mistakes be caught in review?

### Building and Validating Tools

1. **Start with a conversation**: Describe what you need in plain language
2. **Iterate in small steps**: Get one case working, then expand
3. **Test on real files**: Use your actual content, not hypotheticals
4. **Review the output**: Claude makes mistakes — verify before bulk runs
5. **Get peer review**: Have colleagues test on their content

**Demo idea**: Show a quick example of describing a task → getting code → testing it

---

## Part 2: Analysis and Reporting Tools (4 min)

### When Information Overload Hits

- Large doc sets become impossible to audit manually
- Patterns and problems hide in the noise
- Stakeholders want metrics, not vibes

**Examples from doc-utils:**
- `find_duplicate_content.py` — Identifying reuse opportunities
- `find_duplicate_includes.py` — Catching redundant includes
- `find_unused_attributes.py` — Cleaning up cruft
- `check_published_links.py` — Validating external references

### Building Analysis Tools

1. **Define what you're looking for**: Be specific about the pattern
2. **Start with a report**: Get visibility before automation
3. **Add filtering**: Reduce noise to find signal
4. **Make it actionable**: Output should tell you what to fix

---

## Part 3: Claude as Your Writing Copilot (5 min)

### Content Creation Workflows

**Example: Migration guide project** (`migration-from-java-ee-to-quarkus`)
- Research and synthesis: Gathering information from multiple sources
- Drafting: Getting a first pass on the page
- Restructuring: Reorganizing content for clarity
- Editing: Refining voice, tone, and precision

### Effective Copilot Patterns

1. **Research first**: Ask Claude to summarize sources before writing
2. **Outline together**: Collaborate on structure before prose
3. **Draft in chunks**: Work section by section, not whole documents
4. **Iterate on feedback**: Use Claude to address reviewer comments
5. **Stay in control**: You make the decisions, Claude does the legwork

### When Copilot Mode Works Best

- First drafts and brainstorming
- Summarizing technical content
- Rewriting for different audiences
- Generating variations and alternatives

### When to Stay Hands-On

- Final editing for voice and brand
- Accuracy verification (Claude hallucinates)
- Structural decisions for your specific users
- Anything requiring deep product knowledge

---

## Part 4: Speaking Claude — Prompting for Success (3 min)

### Getting Better Results

1. **Be specific**: "Fix this" → "Rewrite this paragraph to emphasize the user benefit"
2. **Provide context**: Share your style guide, audience, constraints
3. **Show examples**: "Write it like this example" beats abstract descriptions
4. **Iterate**: First response is a starting point, not the answer

### Common Mistakes to Avoid

- **Trusting blindly**: Always verify facts and code output
- **Vague requests**: "Make this better" gets vague results
- **One-shot thinking**: The best results come from conversation
- **Forgetting constraints**: Tell Claude about word limits, format requirements, etc.

### Power Moves

- Use system prompts or CLAUDE.md for persistent context
- Save successful prompts as templates
- Break complex tasks into steps
- Ask Claude to explain its reasoning

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

- doc-utils repository: [link to your repo]
- Claude Code documentation: https://docs.anthropic.com/claude-code
- Anthropic prompt engineering guide: https://docs.anthropic.com/claude/docs/prompt-engineering

---

## Notes for Presenter

**Timing breakdown:**
- Opening: 2 min
- Part 1 (Automation): 5 min
- Part 2 (Analysis): 4 min
- Part 3 (Copilot): 5 min
- Part 4 (Prompting): 3 min
- Closing: 1 min
- **Total: 20 min** (leaves buffer for transitions)

**Demo options:**
- Live demo of creating a simple script with Claude
- Before/after of a content piece refined with Claude
- Walkthrough of an analysis tool's output

**Potential slides:**
- Title slide
- 1 slide per main section header
- Code/output screenshots for examples
- Summary slide with key takeaways

---

## Concise Blurb

Technical writers spend too much time on repetitive tasks and not enough time helping users succeed. In this session, you'll learn how to use Claude.ai to automate tedious work, analyze large doc sets, and collaborate on content—without losing your editorial voice. You'll leave with practical techniques you can apply this week.

---

## Concise Bio

Rolfe Dlugy-Hegwer is a Technical Content Professional at IBM and former Principal Technical Writer at Red Hat. Over 30 years, he has documented enterprise Java platforms and cloud-native frameworks while building open-source tools that help documentation teams work smarter. He believes the future of technical writing lies in harnessing AI to focus on what humans do best: understanding users.
