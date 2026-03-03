---
layout: default
title: classify-guides
nav_order: 22
---

# Classify Guides by Diataxis Type

This tool classifies AsciiDoc documentation guides by [Diataxis](https://diataxis.fr/) content type (tutorial, how-to, concept, reference) using structural heuristics and optional LLM-assisted classification.

## Installation

This is a standalone script (not a registered CLI entry point). Run it directly from the `doc-utils` directory:

```sh
python3 classify-guides.py [options]
```

## How It Works

Classification uses three sources, checked in order:

1. **Metadata** — If a file declares `:diataxis-type:` in its AsciiDoc header, that value is used immediately with HIGH confidence.
2. **Structural heuristics** — The file is scanned for structural signals (headings, code blocks, prose patterns, config tables, etc.) and each Diataxis type receives a score. The highest-scoring type wins.
3. **LLM fallback** (optional) — For guides that heuristics cannot confidently classify, an LLM analyzes a structural summary of the file and provides a classification.

### Heuristic Signals

| Type | Signals detected |
|------|-----------------|
| **Tutorial** | "Prerequisites", "Creating the Maven project", "Running the application" headings; `include::{includes}/devtools/` includes; "step by step" language |
| **How-to** | "Procedure", "Setting up", "Configuring" headings; ordered list steps (`. Step`); imperative sentence openers ("Create", "Configure", "Enable"); `-howto.adoc` filename suffix |
| **Reference** | "Configuration Reference" headings; `include::{generated-dir}/config/` includes; `[cols=` config tables; "reference" or "configuration" in title |
| **Concept** | "Overview", "What is", "How X works", "Architecture" headings; explanatory prose patterns; `image::` diagrams; high xref density with low code density |

### Mixed-Type Detection

When two types both score above a threshold, the guide is classified as mixed (e.g., `mixed:tutorial+reference`). For `tutorial+reference` combinations, the output includes approximate split-point line numbers.

## Usage

```sh
# Scan current directory for .adoc files
python3 classify-guides.py

# Scan a specific directory
python3 classify-guides.py --adoc-dir /path/to/docs

# Use a quarkus.yaml metadata file (classifies all guides)
python3 classify-guides.py --yaml-file /path/to/quarkus.yaml --all

# Write results to a specific file
python3 classify-guides.py --output my-results.yaml
```

### Options

| Option | Description |
|--------|-------------|
| `--adoc-dir DIR` | Directory containing `.adoc` guide files (default: current directory) |
| `--yaml-file FILE` | Path to `quarkus.yaml` metadata (optional; without it, scans `--adoc-dir` directly) |
| `--output FILE` | Output YAML file (default: `guide-classifications.yaml`) |
| `--all` | Classify all guides, not just `type:guide` entries (only relevant with `--yaml-file`) |
| `--llm` | Use LLM classification for low-confidence or unclassified guides |
| `--llm-all` | Use LLM classification for all guides |
| `--llm-provider PROVIDER` | LLM provider: `auto`, `gemini`, `anthropic`, `ollama` (default: `auto`) |
| `--llm-api-key KEY` | API key for the LLM provider (default: read from environment) |

## LLM Configuration

The `--llm` flag enables LLM-assisted classification for guides that heuristics classify with LOW or no confidence. The `--llm-all` flag runs LLM classification on every guide.

### Provider Auto-Detection

With `--llm-provider auto` (the default), the tool checks for available providers in this order:

1. **Google Gemini** — if `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set
2. **Anthropic Claude** — if `ANTHROPIC_API_KEY` is set
3. **Ollama (local)** — if an Ollama server is running at `http://localhost:11434`

If no provider is available, a warning is printed and classification continues with heuristics only.

### Google Gemini (free tier)

Gemini offers a free tier with 60 requests per minute, sufficient for classifying large documentation sets.

1. Get an API key at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Set the environment variable:

```sh
export GEMINI_API_KEY="your-api-key-here"
```

3. Run with LLM enabled:

```sh
python3 classify-guides.py --all --llm
```

The tool uses the `gemini-2.0-flash` model by default.

### Anthropic Claude

1. Get an API key at [https://console.anthropic.com/](https://console.anthropic.com/).
2. Set the environment variable:

```sh
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

3. Run with LLM enabled:

```sh
python3 classify-guides.py --all --llm
# or explicitly:
python3 classify-guides.py --all --llm --llm-provider anthropic
```

The tool uses `claude-haiku-4-5` for fast, low-cost classification.

### Ollama (local, fully offline)

Ollama runs models locally with no API key or internet connection required.

1. Install Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Pull a model:

```sh
ollama pull llama3.2
```

3. Start the Ollama server (if not already running):

```sh
ollama serve
```

4. Run with LLM enabled:

```sh
python3 classify-guides.py --all --llm --llm-provider ollama
```

### Passing an API Key Directly

Instead of using environment variables, you can pass the API key on the command line:

```sh
python3 classify-guides.py --llm --llm-provider gemini --llm-api-key "your-key"
```

### LLM Caching

LLM results are cached in `~/.cache/doc-utils/llm-classifications/` so that repeated runs do not re-classify the same guides. To clear the cache:

```sh
rm -rf ~/.cache/doc-utils/llm-classifications/
```

### How LLM Results Are Merged

The LLM does not override heuristic results. Instead, it acts as a weighted tiebreaker:

| Scenario | Result |
|----------|--------|
| Heuristic is HIGH confidence | Heuristic wins. LLM result recorded for comparison. |
| Both agree | Confidence boosted to HIGH. |
| Heuristic is LOW/NONE, LLM is confident | LLM result used, capped at MEDIUM confidence. |
| Disagreement at MEDIUM confidence | Heuristic kept. Both results recorded. |

The output YAML includes `llm_type` and `llm_agrees` fields when LLM classification is used.

## Output Format

The tool writes a YAML file with two sections:

### `classified` — Per-guide results

```yaml
classified:
- url: /guides/security-architecture
  filename: security-architecture.adoc
  title: Quarkus Security architecture
  current_type: guide
  suggested_type: concept
  confidence: high
  reason: "explicit :diataxis-type: concept attribute in file header"
  source: metadata
  lines: 112
  code_blocks: 0
  sections: 8
```

The `source` field indicates where the classification came from:

| Value | Meaning |
|-------|---------|
| `metadata` | From `:diataxis-type:` attribute in the file header |
| `heuristic` | From structural pattern analysis |
| `llm` | From LLM classification (heuristic was low confidence) |
| `heuristic+llm` | Both heuristic and LLM agreed |
| `error` | File could not be read |

### `summary` — Aggregate counts

```yaml
summary:
  total_analyzed: 268
  by_type:
    concept: 26
    howto: 40
    tutorial: 15
    reference: 30
    mixed:tutorial+reference: 22
    guide: 18
  by_confidence:
    high: 214
    medium: 26
    low: 9
    none: 19
  by_source:
    metadata: 57
    heuristic: 210
    error: 1
```

## Examples

Classify all guides and review the summary:

```sh
python3 classify-guides.py --all
```

Find guides that need manual review (low confidence or unclassified):

```sh
python3 classify-guides.py --all --output results.yaml
python3 -c "
import yaml
with open('results.yaml') as f:
    data = yaml.safe_load(f)
for g in data['classified']:
    if g['confidence'] in ('low', 'none'):
        print(f\"{g['confidence']:6s}  {g['suggested_type']:20s}  {g['filename']}\")
"
```

Use LLM to resolve low-confidence classifications:

```sh
export GEMINI_API_KEY="your-key"
python3 classify-guides.py --all --llm --output results-with-llm.yaml
```

Compare heuristic vs. LLM classifications:

```sh
python3 -c "
import yaml
with open('results-with-llm.yaml') as f:
    data = yaml.safe_load(f)
for g in data['classified']:
    if 'llm_type' in g and not g.get('llm_agrees', True):
        print(f\"DISAGREE: {g['filename']}\")
        print(f\"  Heuristic: {g['suggested_type']} ({g['confidence']})\")
        print(f\"  LLM:       {g['llm_type']}\")
"
```

---

See the main [README.md](../getting-started.md) for installation and general usage.
