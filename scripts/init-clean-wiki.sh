#!/bin/bash
# Initialize a clean wiki by removing all example content
# Run from the repo root: ./scripts/init-clean-wiki.sh

set -e
cd "$(dirname "$0")/.."

echo "Cleaning example content..."

# Remove example pages from wiki subdirectories (preserve .gitkeep)
wiki_dirs="sources claims concepts methods entities syntheses questions controversies comparisons timelines hypotheses experiments results arguments chapters figures"
for dir in $wiki_dirs; do
  find "wiki/$dir" -name "*.md" -type f -delete 2>/dev/null
  touch "wiki/$dir/.gitkeep"
done

# Remove raw example papers (preserve .gitkeep)
find raw/papers -name "*.md" -type f -delete 2>/dev/null
touch raw/papers/.gitkeep

# Reset wiki special files to empty templates
cat > wiki/index.md << 'EOF'
---
type: index
updated:
---

# Wiki Index

## Sources

## Claims

## Concepts

## Methods

## Entities

## Syntheses

## Open Questions

## Controversies

## Comparisons

## Timelines

## Hypotheses

## Experiments

## Results

## Arguments

## Chapters

## Figures
EOF

cat > wiki/claims.md << 'EOF'
---
type: claims-index
updated:
---

# Tracked Claims

| Claim | Confidence | Evidence Level | Sources | Replication |
|-------|------------|----------------|---------|-------------|
EOF

cat > wiki/log.md << 'EOF'
---
type: log
---

# Wiki Log
EOF

cat > wiki/contradictions.md << 'EOF'
---
type: contradictions-index
updated:
---

# Active Contradictions

| Contradiction | Claims Involved | Sources | Status |
|--------------|-----------------|---------|--------|
EOF

cat > wiki/glossary.md << 'EOF'
---
type: glossary
updated:
---

# Glossary
EOF

cat > wiki/open-questions.md << 'EOF'
---
type: questions-index
updated:
---

# Open Questions

| Question | Priority | Related Claims |
|----------|----------|----------------|
EOF

cat > wiki/reading-queue.md << 'EOF'
---
type: reading-queue
updated:
---

# Reading Queue

Papers suggested based on identified gaps in the wiki.

## High Priority

## Medium Priority

## Low Priority
EOF

cat > wiki/thesis-progress.md << 'EOF'
---
type: thesis-progress
updated:
---

# Thesis Progress

## Working Title

## Research Questions

## Hypotheses Status

| Hypothesis | Status | Experiment | Result |
|------------|--------|------------|--------|

## Chapter Status

| Chapter | Type | Status | Word Count | Target |
|---------|------|--------|------------|--------|

## Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|

## Next Actions
EOF

cat > wiki/hypotheses-index.md << 'EOF'
---
type: hypotheses-index
updated:
---

# Hypotheses Tracker

| Hypothesis | Status | Derived From | Experiment | Graduated To |
|------------|--------|--------------|------------|--------------|
EOF

echo "✓ Wiki cleaned. Ready for your domain."
echo ""
echo "Next steps:"
echo "1. Open the project in Claude Code"
echo "2. Tell it: 'Initialize the wiki for [your domain]'"
echo "3. Start adding papers to raw/papers/"
