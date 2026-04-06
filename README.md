# LLM SciWiki

A pattern for building scientific research knowledge bases with LLMs.

Inspired by [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted and specialized for scientific research. Where Karpathy's original pattern is domain-agnostic, LLM SciWiki adds evidence hierarchies, claim tracking, contradiction detection, and structured page types designed for working with academic literature.

## The Idea

Most researchers accumulate knowledge across dozens of papers, but the synthesis lives in their head (or scattered notes). SciWiki flips this: an LLM incrementally builds and maintains a persistent wiki from your sources. When you ingest a new paper, the LLM doesn't just summarize it. It extracts claims, checks them against existing knowledge, tracks evidence strength, flags contradictions, and maintains cross-references across the entire wiki.

The wiki is a **persistent, compounding artifact**. The cross-references are already there. The contradictions have already been flagged. The evidence hierarchy is tracked. Every paper you add makes the wiki richer.

You never write the wiki yourself. The LLM writes and maintains all of it. You curate sources, direct analysis, and ask good questions.

## What SciWiki Adds Over Generic LLM Wiki

| Generic LLM Wiki | LLM SciWiki |
|---|---|
| Flat source collection | Typed source taxonomy (papers, preprints, reviews, datasets, ...) |
| Generic wiki pages | 16 typed page templates (claim, method, entity, hypothesis, experiment, ...) |
| Implicit trust in sources | Evidence hierarchy (meta-analysis > RCT > observational > case > opinion) |
| No contradiction tracking | Active contradiction detection and tracking |
| No quantitative metadata | Sample sizes, effect sizes, p-values tracked |
| Generic health checks | Scientific lint (stale evidence, underpowered claims, citation imbalance) |
| No reading suggestions | LLM suggests next papers based on identified gaps |
| No thesis support | Full thesis lifecycle: hypotheses, experiments, results, arguments, chapters |

## Quick Start

### 1. Clone and explore

```bash
git clone https://github.com/leopierini/llm-sciwiki.git
cd llm-sciwiki
```

The repo comes ready to use with `raw/` and `wiki/` directories already set up, including three example papers and a working wiki showing the full pattern in action — including evidence evolution, contradiction detection, and confidence changes.

Browse `wiki/index.md` to see the current state. Read the synthesis at `wiki/syntheses/synthesis-sleep-spindles-and-memory.md` for the most complete picture.

### 2. Start fresh (optional)

If you want to start with a clean wiki for your own domain:

```bash
bash scripts/init-clean-wiki.sh
```

The wiki is now ready — start adding your papers.

### 3. Add a source

Drop a paper (PDF or markdown) into `raw/papers/` and tell the LLM to ingest it. Claude Code reads PDFs directly — no preprocessing required.

For archival conversion to markdown (so extracted text is version-controlled), use `python scripts/pdf-to-md.py paper.pdf -o raw/papers/author-year-keyword.md`. The [Obsidian Web Clipper](https://obsidian.md/clipper) is another option for converting web articles to markdown.

### 4. Ingest

Open the project in [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and tell it:

> Ingest the paper in raw/papers/your-paper.md

The LLM reads the `CLAUDE.md` schema and follows the scientific ingest workflow: extract metadata, identify claims, create source summary, update cross-references, flag contradictions, and suggest next reads.

**What to expect:** A single ingest typically creates 3-8 new wiki pages (source summary, claims, entities, concepts, methods) and updates 5-15 existing pages (index, log, claims table, related concepts, existing claims). The LLM will discuss key takeaways with you before filing.

### 5. Query, lint, synthesize

```
> What does the wiki say about [topic]? What's the evidence strength?
> Lint the wiki - what gaps or issues do you see?
> Synthesize everything we know about [topic]
```

**Query** answers questions using compiled wiki knowledge (not raw sources), with citations and confidence levels.

**Lint** health-checks the wiki: broken links, stale evidence, underpowered claims, orphan pages, citation imbalance.

**Synthesize** produces cross-cutting analysis across multiple claims and sources.

## Page Types

| Type | Purpose | Location |
|------|---------|----------|
| **Source Summary** | Detailed summary of one paper/source | `wiki/sources/` |
| **Claim** | Specific falsifiable claim with evidence chain | `wiki/claims/` |
| **Concept** | Scientific concept or theory | `wiki/concepts/` |
| **Method** | Experimental technique or analytical method | `wiki/methods/` |
| **Entity** | Person, institution, lab, organism, compound | `wiki/entities/` |
| **Synthesis** | Cross-source analysis on a topic | `wiki/syntheses/` |
| **Open Question** | Unanswered research question | `wiki/questions/` |
| **Controversy** | Disputed topic with structured arguments | `wiki/controversies/` |
| **Comparison** | Head-to-head comparison | `wiki/comparisons/` |
| **Timeline** | Chronological evolution of a field/idea | `wiki/timelines/` |
| **Hypothesis** | Testable prediction with lifecycle tracking | `wiki/hypotheses/` |
| **Experiment** | Experimental design and protocol | `wiki/experiments/` |
| **Result** | Outcome of a completed experiment | `wiki/results/` |
| **Argument** | Logical chain of claims forming a thesis argument | `wiki/arguments/` |
| **Chapter** | Thesis chapter outline and structure | `wiki/chapters/` |
| **Figure** | Figure or table tracking with data provenance | `wiki/figures/` |

Blank templates for each page type are available in `templates/`.

## Evidence Hierarchy

Every claim is rated by evidence strength:

| Level | Type | Example |
|-------|------|---------|
| **1** | Systematic review / meta-analysis | Pooled analysis of 20 RCTs |
| **2** | Randomized controlled trial | Double-blind, sham-controlled, n=200 |
| **3** | Controlled observational study | Prospective cohort with matched controls |
| **4** | Case series / qualitative | Small-N descriptive study |
| **5** | Expert opinion / theoretical | Review article, computational model |

The hierarchy adapts to non-biomedical fields — see `CLAUDE.md` for ML, physics, and social science mappings.

Claims also carry **confidence ratings** (strong / moderate / weak / contested) and **replication status**.

## Operations

- **Ingest**: Process a new source, extract claims, check for contradictions, update cross-references, suggest next reads
- **Query**: Ask questions with citations and confidence levels
- **Lint**: Health-check for stale evidence, underpowered claims, orphan pages, citation imbalance
- **Synthesize**: Cross-cutting analysis, gap identification, state-of-knowledge summaries
- **Thesis**: Formulate hypotheses, design experiments, record results, build arguments, draft chapters

## Included Example

The repo ships with three (fictional) neuroscience papers on sleep spindles and memory consolidation, demonstrating the full lifecycle of evidence:

1. **Chen (2023)** — Observational study (n=120) finding that spindle density correlates with memory consolidation. Creates initial claims with **weak** confidence.

2. **Rodriguez (2024)** — RCT (n=84) providing causal evidence that spindle stimulation improves memory. Upgrades the claim to **moderate** confidence.

3. **Kumar (2025)** — Pre-registered multi-site replication (n=204) that replicates the spindle enhancement but **fails to replicate the memory benefit**. Downgrades the claim to **contested**, triggers a controversy page, and demonstrates how the wiki handles contradicting evidence.

This three-paper arc shows the system's most important features:
- Evidence chains evolving over time
- Confidence upgrades AND downgrades
- Contradiction detection and tracking
- Controversy pages with structured arguments from both sides
- Comparison pages (protocol differences)
- Timeline pages (field evolution)

## Tooling

LLM SciWiki is intentionally minimal, just a schema (`CLAUDE.md`) and a ready-to-use directory structure. It works with:

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** as the LLM agent (reads `CLAUDE.md` automatically)
- **[Obsidian](https://obsidian.md)** as the visual frontend (graph view, wikilinks, Dataview plugin for queries)
- **Git** for version history

### Scripts

Install dependencies: `pip install -r scripts/requirements.txt`

| Script | Purpose |
|--------|---------|
| `scripts/lint.py` | Structural validation: frontmatter (with enum value checks), broken wikilinks, ambiguous links, index consistency, claims table, hypotheses index, orphan page detection, raw source validation. Runs automatically via the included GitHub Action. |
| `scripts/pdf-to-md.py` | Convert PDF papers to markdown for ingestion. Adds a YAML frontmatter stub for you to fill in. |
| `scripts/init-clean-wiki.sh` | Reset the wiki to a blank state for your own domain. |

### Obsidian Dataview Queries

If you use [Obsidian](https://obsidian.md) with the [Dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin, these queries are useful for navigating the wiki:

**All contested claims:**
````
```dataview
TABLE confidence, evidence_level, replication_status
FROM "wiki/claims"
WHERE confidence = "contested"
SORT updated DESC
```
````

**Claims by evidence level:**
````
```dataview
TABLE confidence, replication_status
FROM "wiki/claims"
SORT evidence_level ASC
```
````

**Recently updated pages:**
````
```dataview
TABLE type, updated
FROM "wiki"
SORT updated DESC
LIMIT 20
```
````

**Hypotheses by status:**
````
```dataview
TABLE status, derived_from, graduated_to
FROM "wiki/hypotheses"
SORT status ASC
```
````

**Sources by evidence level:**
````
```dataview
TABLE evidence_level, year, journal
FROM "raw"
SORT evidence_level ASC
```
````

### Other tools

- **[qmd](https://github.com/tobi/qmd)** — hybrid BM25/vector search for markdown files, useful as the wiki grows.

## Limitations

- **Single-user by default.** The wiki is designed for one researcher working with one LLM. Multi-user workflows would need git branching strategies and conflict resolution conventions not yet defined.
- **Text sources only.** The ingest workflow assumes markdown or text-extractable sources. Datasets, code repositories, and multimedia sources require manual preprocessing.
- **No automated search.** The LLM suggests papers to read, but doesn't fetch or download them. You curate all sources manually.
- **LLM context limits.** Very large wikis (hundreds of pages) may exceed LLM context windows during operations. The wiki is designed to be browsed via `index.md` and wikilinks, not loaded entirely at once.
- **Fictional example data.** The included papers are fictional. They demonstrate the pattern but are not real scientific findings.

## Philosophy

The tedious part of maintaining a scientific knowledge base is not reading papers or having ideas, it's the bookkeeping. Updating cross-references when new evidence arrives. Noting when paper B contradicts paper A. Keeping track of which claims rest on strong evidence and which are speculative. Tracking sample sizes and effect sizes across studies. Researchers abandon note systems because the maintenance burden grows faster than the value.

LLMs handle this effortlessly. They don't forget to update a cross-reference, and they can touch 20 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

Your job: curate sources, direct analysis, ask good questions, think about what it all means.
The LLM's job: everything else.

## Credits

This project builds on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The core architecture (raw sources -> wiki -> schema) is his idea. LLM SciWiki specializes it for scientific research by adding evidence tracking, typed pages, scientific lint, and domain-specific workflows.

## License

MIT
