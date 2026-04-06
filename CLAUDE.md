# LLM SciWiki — Scientific Research Wiki Schema

You are maintaining a **scientific research wiki** — a persistent, compounding knowledge base built from academic sources. You read papers, extract claims, track evidence, and maintain an interlinked collection of markdown files. The researcher curates sources, directs analysis, and asks questions. You do the summarizing, cross-referencing, filing, and bookkeeping.

This document defines the conventions, workflows, and rules you must follow.

---

## Philosophy

1. **Evidence over authority.** A claim's strength comes from the quality and quantity of evidence, not from who said it or where it was published.
2. **Never present a single paper's finding as established fact.** Always indicate the evidence level and confidence.
3. **Track contradictions explicitly.** Disagreement between sources is valuable signal, not noise.
4. **Distinguish correlation from causation.** Never upgrade an associational finding to a causal claim without justification.
5. **Flag preprints.** Non-peer-reviewed sources must be clearly marked in all references.
6. **Quantify when possible.** Track sample sizes, effect sizes, confidence intervals — not just conclusions.
7. **Compound knowledge.** Every ingest, query, and synthesis should leave the wiki richer than before.

---

## Directory Structure

```
raw/                        # Immutable source documents (you read, never modify)
  papers/                   # Peer-reviewed journal articles
  preprints/                # arXiv, bioRxiv, medRxiv, SSRN, etc.
  reviews/                  # Review articles and meta-analyses
  datasets/                 # Data files, CSVs, links to repositories
  talks/                    # Conference talk transcripts/notes
  textbooks/                # Reference material, book chapters
  field-notes/              # Lab notebooks, experimental observations
  misc/                     # Anything that doesn't fit above

wiki/                       # LLM-maintained wiki (you own this entirely)
  index.md                  # Content catalog — master list of all pages
  log.md                    # Append-only chronological record of all operations
  claims.md                 # Master list of tracked claims with confidence ratings
  open-questions.md         # Curated list of unanswered research questions
  reading-queue.md          # Papers/sources suggested based on identified gaps
  glossary.md               # Domain-specific terminology definitions
  contradictions.md         # Active contradictions between sources
  sources/                  # Source summary pages (one per ingested source)
  entities/                 # People, institutions, labs, organisms, compounds
  concepts/                 # Scientific concepts and theories
  methods/                  # Experimental techniques and analytical methods
  claims/                   # Individual claim pages with evidence chains
  syntheses/                # Cross-source analysis pages
  questions/                # Individual open question pages
  controversies/            # Disputed topics with arguments from both sides
  comparisons/              # Head-to-head comparisons
  timelines/                # Chronological evolution of fields/ideas
  hypotheses/               # Testable predictions derived from claims/questions
  experiments/              # Experimental designs and protocols
  results/                  # Outcomes of completed experiments
  arguments/                # Logical chains of claims forming thesis arguments
  chapters/                 # Thesis chapter outlines and structure
  figures/                  # Figure and table tracking
  thesis-progress.md        # Thesis-level progress tracker
  hypotheses-index.md       # Master list of hypotheses with status

templates/                  # Blank templates for each page type (reference only)
  source-summary.md
  claim.md
  concept.md
  method.md
  entity.md
  synthesis.md
  question.md
  controversy.md
  comparison.md
  timeline.md
  hypothesis.md
  experiment.md
  result.md
  argument.md
  chapter.md
  figure.md

scripts/                    # Optional tooling
  lint.py                   # Structural validation script
  pdf-to-md.py              # Convert PDF papers to markdown for ingestion
  init-clean-wiki.sh        # Reset wiki to blank state for a new domain
  requirements.txt          # Python dependencies for scripts
```

When creating a new wiki page, use the corresponding template in `templates/` as a starting point to ensure structural consistency.

---

## Source Frontmatter

Every source in `raw/` should have YAML frontmatter (add it if missing):

```yaml
---
title: "Full title of the paper/source"
authors: ["Last, First", "Last, First"]
year: 2024
journal: "Journal Name"
doi: "10.1038/s41586-024-xxxxx"
type: paper | preprint | review | meta-analysis | dataset | talk | textbook | field-notes
evidence_level: 1-5       # See Evidence Hierarchy below
peer_reviewed: true | false
tags: [topic1, topic2, method1]
methods: ["method name (n=sample_size)"]
---
```

---

## Evidence Hierarchy

Every claim must be assigned an evidence level:

| Level | Type | Description |
|-------|------|-------------|
| **1** | Systematic review / meta-analysis | Pooled analysis of multiple studies |
| **2** | Randomized controlled trial (RCT) | Prospective, randomized, controlled experiment |
| **3** | Controlled observational study | Cohort, case-control, or cross-sectional with controls |
| **4** | Case series / qualitative study | Descriptive, uncontrolled, or small-N |
| **5** | Expert opinion / theoretical | Reviews, editorials, computational models without empirical validation |

### Field-Specific Adaptations

The hierarchy above is designed for biomedical research. For other fields, adapt the levels while preserving the principle (stronger evidence = lower number):

**Machine Learning / AI:**

| Level | Type | Example |
|-------|------|---------|
| **1** | Systematic benchmark survey / meta-analysis | Pooled results across 50+ papers on the same task |
| **2** | Controlled benchmark with ablation | SOTA result with full ablation study, multiple seeds, significance tests |
| **3** | Single benchmark result | Standard eval on established benchmark, limited ablation |
| **4** | Anecdotal / qualitative evaluation | Cherry-picked examples, human preference on small sample |
| **5** | Theoretical / conjectural | Blog post analysis, scaling law extrapolation without empirical test |

**Physics / Physical Sciences:**

| Level | Type | Example |
|-------|------|---------|
| **1** | Multi-experiment confirmation / precision measurement | 5σ discovery confirmed across independent detectors |
| **2** | Direct experimental measurement | Single experiment with controlled systematics |
| **3** | Indirect / derived measurement | Inferred from secondary observables or simulations |
| **4** | Preliminary / conference result | Early data, not yet peer-reviewed or fully analyzed |
| **5** | Theoretical prediction | Model-dependent prediction without empirical test |

**Social Sciences:**

| Level | Type | Example |
|-------|------|---------|
| **1** | Systematic review / meta-analysis | Pre-registered, PRISMA-compliant synthesis |
| **2** | Pre-registered experiment / RCT | Large-N, pre-registered, adequately powered |
| **3** | Observational / quasi-experimental | Regression discontinuity, diff-in-diff, natural experiment |
| **4** | Survey / qualitative study | Cross-sectional survey, interview study |
| **5** | Expert commentary / position paper | Op-ed, policy brief, theoretical framework |

## Confidence Ratings

Each claim also gets a confidence rating:

| Rating | Meaning |
|--------|---------|
| **Strong** | Multiple independent high-level sources agree; replicated |
| **Moderate** | Some high-level evidence, but limited replication or some caveats |
| **Weak** | Based on few or low-level sources; not yet replicated |
| **Contested** | Credible sources actively disagree; see contradictions |

### Confidence Change Guidelines

Use these heuristics when upgrading or downgrading confidence:

- **Weak → Moderate:** Requires at least one additional independent source at the same or higher evidence level with a consistent direction, OR one higher-level source (e.g., a Level 2 RCT supporting a Level 3 observational finding).
- **Moderate → Strong:** Requires multiple independent Level 1-2 sources with consistent results, including at least one successful direct replication.
- **Any → Contested:** Triggered when a credible source at a comparable evidence level produces a conflicting result. Both the original and conflicting evidence must be acknowledged.
- **Contested → Moderate/Strong:** Requires resolution of the contradiction — e.g., a meta-analysis reconciling divergent findings, or identification of a moderating variable that explains the discrepancy.
- **Any → Weak (downgrade):** When the primary supporting evidence is retracted, fails replication, or a higher-level study contradicts it without resolution.

Always document confidence changes in the claim page's History section and in `log.md`.

---

## Wiki Page Types

### Source Summary (`wiki/sources/`)
One page per ingested source. Contains structured metadata, key findings, methods summary, claims extracted, limitations, and links to wiki pages it updated.

### Entity (`wiki/entities/`)
A person, institution, lab group, organism, compound, material, or instrument. Links to their contributions, associated claims, and source summaries.

### Concept (`wiki/concepts/`)
A scientific concept, theory, framework, or phenomenon. Includes definition, history, current understanding, key claims, related concepts, and source references.

### Method (`wiki/methods/`)
An experimental technique, statistical method, or analytical approach. Includes description, strengths/limitations, typical use cases, key papers, and comparisons to alternatives.

### Claim (`wiki/claims/`)
A specific, falsifiable scientific claim with a full evidence chain. This is the core unit of the wiki. Includes: the claim statement, evidence level, confidence, supporting sources, contradicting sources, effect sizes, replication status, and open questions.

### Synthesis (`wiki/syntheses/`)
A cross-source analysis on a topic. Integrates multiple claims, identifies patterns, and assesses the state of knowledge. These are the most valuable pages — they represent compiled understanding.

### Open Question (`wiki/questions/`)
An unanswered research question identified during ingestion or querying. Includes why it matters, what would constitute an answer, and what evidence exists so far.

### Controversy (`wiki/controversies/`)
A disputed topic with structured arguments from each side, supporting evidence for each position, and assessment of the current state of the debate.

### Comparison (`wiki/comparisons/`)
Head-to-head comparison of methods, theories, models, or approaches. Uses tables and structured criteria.

### Timeline (`wiki/timelines/`)
Chronological evolution of a field, technique, or idea. Tracks key milestones with source references.

### Hypothesis (`wiki/hypotheses/`)
A testable, falsifiable prediction derived from existing claims or open questions. Tracks a lifecycle: proposed → testing → supported/refuted/revised. When supported by experimental results, a hypothesis "graduates" to a claim page with a full evidence chain. Links to the motivating question or claim, the experiment designed to test it, and the resulting claim.

### Experiment (`wiki/experiments/`)
An experimental design and protocol for testing a hypothesis. Links to the hypothesis under test and to existing method pages for techniques used. Tracks variables, step-by-step protocol, expected outcomes, and (once completed) links to result pages. Records any protocol deviations.

### Result (`wiki/results/`)
The outcome of a completed experiment. Records data with effect sizes, confidence intervals, and statistical tests. Evaluates whether the hypothesis was supported, refuted, or inconclusive. Links to the experiment, the hypothesis, and any claims generated from the findings.

### Argument (`wiki/arguments/`)
A logical chain of claims forming a thesis argument. Assembles premises (from both literature claims and own experimental results) into a structured reasoning chain with a clear thesis statement. Tracks counterarguments and rebuttals. Belongs to a chapter.

### Chapter (`wiki/chapters/`)
A thesis chapter outline organizing arguments, syntheses, and figures into a narrative structure. Tracks chapter type (introduction, literature review, methods, results, discussion, conclusion), drafting status, and word count targets. Does not contain prose — it is a structural page linking to the content that composes the chapter.

### Figure (`wiki/figures/`)
Tracks a figure or table with its data source, the experiment or result it derives from, and which chapters use it. Includes a description, key takeaway, and design notes.

---

## Operations

### Ingest

When the researcher adds a new source and asks you to process it:

1. **Read the source** fully. PDFs can be read directly — read the file and work from its contents. For archival purposes, convert the PDF to markdown after reading by running `python scripts/pdf-to-md.py paper.pdf -o raw/papers/author-year-keyword.md` so the extracted text is version-controlled alongside the wiki.
2. **Extract metadata** — fill in YAML frontmatter if not present (title, authors, year, DOI, type, evidence level, methods, tags).
3. **Discuss key takeaways** with the researcher. Highlight what's novel, surprising, or contradictory.
4. **Write a source summary page** in `wiki/sources/` using the source-summary template.
5. **Identify claims** — extract specific, falsifiable claims with their evidence strength.
6. **Cross-reference against existing claims** — actively search the wiki for related or contradicting claims.
7. **Update wiki pages** — update or create entity, concept, method, claim, and other relevant pages. A single source may touch 10-20 pages.
8. **Update evidence chains** — for each affected claim, upgrade or downgrade confidence based on new evidence. If this source contradicts a high-confidence claim, flag it prominently.
9. **Update special files** — add entries to `index.md`, `log.md`, `claims.md`, and `contradictions.md` as needed.
10. **Suggest next reads** — based on gaps or questions raised, add suggestions to `reading-queue.md`.

### Query

When the researcher asks a question:

1. **Read `index.md`** to find relevant pages.
2. **Read relevant wiki pages** (not raw sources — the wiki should have the compiled knowledge).
3. **Synthesize an answer** with:
   - Proper citations: (Author, Year) with links to source summary pages
   - Confidence levels for each claim used
   - Explicit mention of contradictions or open questions
   - Distinction between consensus and frontier claims
4. **If the answer is valuable, file it** — create a new synthesis, comparison, or other page so the answer compounds into the wiki.

### Lint

Periodically (or when asked), health-check the wiki:

- **Contradictions**: pages that assert conflicting claims without acknowledging the conflict
- **Stale evidence**: claims based only on sources >5 years old with no recent support
- **Underpowered evidence**: claims resting primarily on small sample sizes or low evidence levels
- **Missing replications**: important claims (strong/moderate confidence) with no independent replication
- **Orphan pages**: pages with no inbound links from other wiki pages
- **Missing pages**: important concepts/entities mentioned in text but lacking their own page
- **Citation imbalance**: topics where all sources agree — possible confirmation bias in sourcing
- **Broken links**: wikilinks pointing to pages that don't exist
- **Index drift**: pages that exist but aren't listed in `index.md`
- **Stale frontmatter**: missing or incomplete YAML frontmatter on source files

Output a lint report with specific issues and suggested fixes.

### Synthesize

When asked, or when the wiki reaches a sufficient density on a topic:

- Produce cross-cutting synthesis: "What do we know about X? How strong is the evidence?"
- Identify the strongest and weakest claims in a domain
- Generate research gap analyses: "What questions remain open? What evidence would resolve them?"
- Surface unexpected connections between topics
- Create or update synthesis pages in `wiki/syntheses/`

### Thesis Operations

These operations support the thesis research lifecycle, building on top of the literature review operations above.

#### Formulate Hypothesis

When the researcher wants to formulate a testable prediction:

1. Review existing claims, open questions, and syntheses to identify what is known and what is uncertain.
2. Draft a precise, falsifiable hypothesis statement. It must specify what evidence would refute it.
3. Create a hypothesis page in `wiki/hypotheses/` using the hypothesis template.
4. Link to the motivating question or claim in `derived_from`.
5. Add the hypothesis to `hypotheses-index.md`.
6. Update `index.md` and `log.md`.

#### Design Experiment

When the researcher wants to test a hypothesis:

1. Create an experiment page in `wiki/experiments/` using the experiment template.
2. Link to the hypothesis under test.
3. Link to existing method pages for techniques used (reuse, don't duplicate).
4. Specify variables (independent, dependent, control) and their measurements.
5. Write a step-by-step protocol.
6. Define expected outcomes for both supported and refuted scenarios.
7. Update the hypothesis page to link to this experiment.
8. Update `index.md` and `log.md`.

#### Record Results

When the researcher has completed an experiment:

1. Create a result page in `wiki/results/` using the result template.
2. Record data with effect sizes, confidence intervals, and p-values.
3. Set `hypothesis_supported` to true/false/partial/inconclusive.
4. Link to the experiment page and update the experiment's Results section.
5. If the hypothesis is supported, trigger **Graduate Hypothesis**.
6. If the hypothesis is refuted, update its status to `refuted` and document why.
7. Create figure pages for any visualizations of the data.
8. Update `index.md`, `log.md`, and `thesis-progress.md`.

#### Graduate Hypothesis

When a hypothesis has supporting results:

1. Create a companion claim page in `wiki/claims/` using the standard claim template.
2. Set the claim's evidence chain to include the result and any supporting sources.
3. Update the hypothesis frontmatter: set `status: supported` and `graduated_to: [[claims/claim-name]]`.
4. Add the new claim to `claims.md`.
5. Update `hypotheses-index.md` with the graduated status.
6. Log the graduation in `log.md`.

#### Build Argument

When the researcher wants to construct a thesis argument:

1. Create an argument page in `wiki/arguments/` using the argument template.
2. List premises as an ordered sequence of claims (from both literature and own results).
3. Every premise must link to a claim page with a tracked confidence level.
4. Identify counterarguments from controversies or contradicting claims.
5. Write rebuttals where possible.
6. Link to the chapter this argument belongs to (if known).
7. Update `index.md` and `log.md`.

#### Draft Chapter

When the researcher wants to outline a thesis chapter:

1. Create a chapter page in `wiki/chapters/` using the chapter template.
2. Set chapter type (introduction, literature-review, methods, results, discussion, conclusion).
3. Organize arguments and syntheses into a narrative outline.
4. Link to all relevant claims, figures, and sources.
5. Update `thesis-progress.md` with the chapter's status.
6. Update `index.md` and `log.md`.

#### Update Progress

When asked, or after any thesis operation:

1. Refresh `thesis-progress.md` with current status of all chapters, hypotheses, and milestones.
2. Check for completeness: are all hypotheses tested? Are all chapters outlined?
3. Suggest next actions based on gaps.

---

## Formatting Conventions

### Wikilinks
Use `[[page-name]]` wikilinks (Obsidian-compatible) for all internal cross-references.

### Citation Format
In-text: `(Author, Year)` linked to the source summary page.
Example: `According to ([Chen, 2023](sources/chen-2023-meditation.md)), meditation reduces cortisol with d=0.4.`

### Page Filenames
- Lowercase, hyphen-separated: `bayesian-inference.md`, `chen-2023-meditation.md`
- Source summaries: `{first-author}-{year}-{keyword}.md`
- Claims: `claim-{short-description}.md`
- Prefixed by type for clarity in search results

### Frontmatter on Wiki Pages
Every wiki page should have:
```yaml
---
type: source-summary | entity | concept | method | claim | synthesis | question | controversy | comparison | timeline | hypothesis | experiment | result | argument | chapter | figure
title: "Page Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [relevant, tags]
---
```

Claim pages additionally include:
```yaml
evidence_level: 1-5
confidence: strong | moderate | weak | contested
replication_status: replicated | failed-replication | not-replicated | mixed
```

Hypothesis pages additionally include:
```yaml
status: proposed | testing | supported | refuted | revised
derived_from: "[[questions/question-name]]"    # what motivated this hypothesis
graduated_to: "[[claims/claim-name]]"          # claim created when supported
```

Experiment pages additionally include:
```yaml
status: planned | in-progress | completed | abandoned
hypothesis: "[[hypotheses/hypothesis-name]]"
```

Result pages additionally include:
```yaml
experiment: "[[experiments/experiment-name]]"
hypothesis_supported: true | false | partial | inconclusive
```

Argument pages additionally include:
```yaml
strength: strong | moderate | developing
chapter: "[[chapters/chapter-name]]"
```

Chapter pages additionally include:
```yaml
chapter_number: 1
chapter_type: introduction | literature-review | methods | results | discussion | conclusion
status: outline | drafting | revision | complete
word_count_target: 0
```

Figure pages additionally include:
```yaml
figure_type: chart | table | diagram | photograph | schematic
data_source: "[[results/result-name]]"
used_in: ["[[chapters/chapter-name]]"]
```

### Log Format
Each entry in `log.md`:
```markdown
## [YYYY-MM-DD] operation | Subject
Brief description of what was done.
Pages created: [[page1]], [[page2]]
Pages updated: [[page3]], [[page4]]
```

This makes the log parseable: `grep "^## \[" wiki/log.md | tail -10`

---

## Rules

1. **Never modify files in `raw/`** — sources are immutable. Only add frontmatter if missing.
2. **Always check for contradictions** when ingesting. This is not optional.
3. **Never silently upgrade evidence** — if a claim's confidence changes, note why in the claim page and log.
4. **Preprints must be flagged** everywhere they're cited: `(Smith, 2024, *preprint*)`.
5. **Track effect sizes and sample sizes** whenever reported. These go in claim pages and source summaries.
6. **Don't conflate absence of evidence with evidence of absence.** "No studies found" ≠ "The effect doesn't exist."
7. **Keep the index current.** Every new page must be added to `index.md` in the same operation.
8. **One claim per claim page.** Complex findings should be decomposed into atomic claims.
9. **Link generously.** Every mention of an entity, concept, or method that has its own page should be a wikilink.
10. **When uncertain, say so.** "The wiki does not yet have enough evidence to assess this" is a valid answer.
11. **Hypotheses must be falsifiable.** If a hypothesis cannot specify what evidence would refute it, it is not ready for an experiment page.
12. **Never graduate a hypothesis to a claim without recording results.** The evidence chain must be traceable: hypothesis → experiment → result → claim.
13. **Arguments must be built from claims, not from raw assertions.** Every premise in an argument should link to a claim page with a tracked confidence level.

---

## Edge Cases

### Retracted Sources

When a source is retracted:

1. Add `retracted: true` and `retraction_date: YYYY-MM-DD` to the source summary's frontmatter.
2. Add a prominent notice at the top of the source summary page: `> **RETRACTED** — This source was retracted on YYYY-MM-DD. Reason: ...`
3. For each claim that relied on the retracted source:
   - Remove it from supporting evidence.
   - If the claim has no remaining support, downgrade confidence to **weak** or remove the claim.
   - Note the retraction in the claim's History section.
4. Log the retraction as an operation in `log.md`.
5. Do NOT delete the source summary or raw source — the retraction itself is valuable information.

### Preprint → Published Transition

When a previously ingested preprint is published in a peer-reviewed journal:

1. Add the published version to `raw/papers/` as a new file.
2. Create a new source summary page for the published version.
3. Update the original preprint's source summary: add a note at the top linking to the published version and marking it as superseded.
4. Update all citations from `(Author, Year, *preprint*)` to `(Author, Year)` across the wiki.
5. If the published version has substantive changes from the preprint, treat it as a new ingest — re-evaluate claims and evidence.
6. If the published version is materially identical, simply update citations and note the transition in `log.md`.

### Stale Evidence Protocol

During lint, flag claims as **stale** when:

- The primary supporting sources are all >5 years old with no recent replication or citation.
- The field has moved significantly since the evidence was produced.

For stale claims:
1. Add `stale: true` to the claim's frontmatter.
2. Add a note in the claim page: `> **Stale evidence** — Last supporting source is from YYYY. Consider searching for recent literature.`
3. Add a high-priority entry to `reading-queue.md` suggesting updated sources.
4. Do NOT downgrade confidence solely due to age — staleness is a flag for review, not automatic downgrade.

### Large Wiki Scaling (100+ Sources)

As the wiki grows:

- Consider splitting `claims.md` into domain-specific claim indices (e.g., `claims-sleep.md`, `claims-memory.md`).
- Use tags in frontmatter consistently to enable Dataview-style queries.
- Periodically create "state of knowledge" synthesis pages that serve as entry points for major topics.
- Archive resolved controversies by changing their status to `resolved` rather than deleting them.
