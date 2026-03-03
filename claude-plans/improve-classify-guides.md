# Improve classify-guides.py Heuristics + Add Optional LLM Classification

## Context

`~/doc-utils/classify-guides.py` classifies Quarkus AsciiDoc guides by Diataxis type using structural heuristics. Current weaknesses: howto detection is weak (mostly LOW confidence), concept detection is narrow (title-keyword dependent), and mixed-type detection only catches tutorial+reference combos. The user wants improved heuristics and optional LLM integration for low-confidence fallback.

## Phase 1: Read `:diataxis-type:` Metadata (Highest Impact)

~60 upstream Quarkus guides already declare `:diataxis-type:` in their AsciiDoc headers. The script ignores this entirely.

- **`classify-guides.py` `analyze_adoc()`**: Extract `:diataxis-type:` attribute from file header via regex
- **`classify-guides.py` `classify()`**: Check metadata first, before any heuristic logic. If present and valid (`tutorial`, `howto`, `concept`, `reference`), return HIGH confidence immediately
- Add `source` field to all results: `"metadata"`, `"heuristic"`, `"llm"`, or `"heuristic+llm"`

## Phase 2: Improved Heuristics

### 2a. Better Howto Detection

New signals to track in `analyze_adoc()`:
- Procedure/task headings: "Procedure", "How to", "Setting up", "Adding", "Enabling", etc.
- Ordered list steps (`. Step` pattern)
- Imperative sentence openers outside code blocks ("Set", "Add", "Create", "Configure", etc.)
- Filename suffix `-howto.adoc`

Replace the current arbitrary-threshold howto classification with a **scoring system** where signals accumulate points.

### 2b. Better Concept Detection

New signals:
- Explanatory headings: "Overview", "What is", "How X works", "Architecture", "Key concepts"
- Explanatory prose patterns ("is based on", "consists of", "is designed")
- Diagram count (`image::`)
- High xref density + low code density ratio

### 2c. Expanded Mixed-Type Detection

Detect `mixed:howto+reference` and `mixed:concept+reference` in addition to the existing `mixed:tutorial+reference`.

### 2d. Refactor classify() to Scoring Architecture

Replace the linear if/elif cascade with per-type scoring functions that return `(score, reasons)` tuples. Highest score wins. Mixed types detected when top two scores both exceed threshold.

## Phase 3: Optional LLM Classification

### New module: `doc_utils/llm_classifier.py`

- Auto-detects available provider: Gemini API (free tier) → Anthropic API → Ollama (local) → none
- Uses `urllib.request` only (no new dependencies)
- Sends **structural summary** to LLM (title, headings, first paragraph, metrics), not full file content
- File-based cache at `~/.cache/doc-utils/llm-classifications/` to avoid redundant API calls
- Rate limiting: 1 req/sec default, retry once on 429

### CLI integration in `classify-guides.py`

New flags: `--llm`, `--llm-all`, `--llm-provider {auto,gemini,anthropic,ollama}`, `--llm-api-key`

### Merge strategy: LLM as weighted tiebreaker

- Heuristic HIGH confidence → trust heuristic, record LLM for comparison
- Both agree → boost to HIGH confidence
- Heuristic LOW/NONE + LLM confident → use LLM (capped at MEDIUM)
- Disagreement → report both

## Phase 4: Tests

New file: `tests/test_classify_guides.py`
- Unit tests for `analyze_adoc()` (metadata extraction, new signal detection)
- Unit tests for `classify()` (metadata precedence, scoring, mixed-type detection)
- Unit tests for `merge_classification()`
- Mocked LLM classifier tests

## Phase 5: Validation

Run against the full 185-guide corpus and compare results to the existing `guide-classifications.yaml` baseline.

## Implementation Order

| Step | Scope | Risk |
|------|-------|------|
| 1. Extract `:diataxis-type:` metadata | `classify-guides.py` | Very low |
| 2. Add metadata-first classification | `classify-guides.py` | Very low |
| 3. Add new howto/concept regex patterns | `classify-guides.py` | Low |
| 4. Track new signals in `analyze_adoc()` | `classify-guides.py` | Low |
| 5. Refactor `classify()` to scoring | `classify-guides.py` | Medium |
| 6. Add mixed-type combos | `classify-guides.py` | Low |
| 7. Create LLM classifier module | `doc_utils/llm_classifier.py` (new) | Medium |
| 8. Add `--llm` CLI flags | `classify-guides.py` | Low |
| 9. Add tests | `tests/test_classify_guides.py` (new) | Low |
| 10. Validate against corpus | Run + compare | None |

## Files

- **Modify**: `/home/rdlugyhe/doc-utils/classify-guides.py`
- **Create**: `/home/rdlugyhe/doc-utils/doc_utils/llm_classifier.py`
- **Create**: `/home/rdlugyhe/doc-utils/tests/test_classify_guides.py`
