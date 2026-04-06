#!/usr/bin/env python3
"""
LLM SciWiki structural linter.

Validates wiki structure: frontmatter, wikilinks, index consistency, and claim tracking.
Run from the repo root: python scripts/lint.py
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

WIKI_DIR = Path("wiki")
RAW_DIR = Path("raw")
TEMPLATES_DIR = Path("templates")

REQUIRED_FRONTMATTER = {"type", "title", "created", "updated", "tags"}
CLAIM_FRONTMATTER = {"evidence_level", "confidence", "replication_status"}
HYPOTHESIS_FRONTMATTER = {"status", "derived_from"}
EXPERIMENT_FRONTMATTER = {"status", "hypothesis"}
RESULT_FRONTMATTER = {"experiment", "hypothesis_supported"}
ARGUMENT_FRONTMATTER = {"strength", "chapter"}
CHAPTER_FRONTMATTER = {"chapter_number", "chapter_type", "status", "word_count_target"}
FIGURE_FRONTMATTER = {"figure_type", "data_source", "used_in"}
VALID_PAGE_TYPES = {
    "source-summary", "entity", "concept", "method", "claim",
    "synthesis", "question", "controversy", "comparison", "timeline",
    "hypothesis", "experiment", "result", "argument", "chapter", "figure",
}
VALID_SPECIAL_TYPES = {
    "index", "log", "claims-index", "questions-index",
    "reading-queue", "glossary", "contradictions-index",
    "thesis-progress", "hypotheses-index",
}
VALID_TYPES = VALID_PAGE_TYPES | VALID_SPECIAL_TYPES

# Allowed enum values per CLAUDE.md
VALID_EVIDENCE_LEVELS = {1, 2, 3, 4, 5}
VALID_CONFIDENCE = {"strong", "moderate", "weak", "contested"}
VALID_REPLICATION_STATUS = {"replicated", "failed-replication", "not-replicated", "mixed"}
VALID_HYPOTHESIS_STATUS = {"proposed", "testing", "supported", "refuted", "revised"}
VALID_EXPERIMENT_STATUS = {"planned", "in-progress", "completed", "abandoned"}
VALID_CHAPTER_STATUS = {"outline", "drafting", "revision", "complete"}
VALID_HYPOTHESIS_SUPPORTED = {True, False, "partial", "inconclusive"}
VALID_STRENGTH = {"strong", "moderate", "developing"}
VALID_CHAPTER_TYPE = {"introduction", "literature-review", "methods", "results", "discussion", "conclusion"}
VALID_FIGURE_TYPE = {"chart", "table", "diagram", "photograph", "schematic"}
SPECIAL_FILES = {"index.md", "log.md", "claims.md", "open-questions.md",
                 "reading-queue.md", "glossary.md", "contradictions.md",
                 "thesis-progress.md", "hypotheses-index.md"}


def extract_frontmatter(path: Path) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter fields from a markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code so wikilinks inside them are ignored."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def find_wikilinks(path: Path) -> List[str]:
    """Find all [[wikilinks]] in a markdown file (ignoring code blocks)."""
    text = path.read_text(encoding="utf-8")
    text = _strip_code_blocks(text)
    links = re.findall(r"\[\[([^\]]+)\]\]", text)
    # Strip Obsidian display-text syntax: [[page|Display Text]] → page
    return [link.split("|")[0] for link in links]


def get_wiki_pages() -> List[Path]:
    """Get all wiki markdown files (excluding special files)."""
    pages = []
    for p in WIKI_DIR.rglob("*.md"):
        if p.name not in SPECIAL_FILES:
            pages.append(p)
    return pages


def lint_frontmatter(pages: List[Path]) -> List[str]:
    """Check that all wiki pages have required frontmatter fields."""
    issues = []
    for page in pages:
        fm = extract_frontmatter(page)
        if fm is None:
            issues.append(f"MISSING FRONTMATTER: {page}")
            continue
        missing = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing:
            issues.append(f"MISSING FIELDS in {page}: {', '.join(sorted(missing))}")
        if "type" in fm:
            page_type = str(fm["type"]).strip()
            if page_type not in VALID_PAGE_TYPES:
                issues.append(f"INVALID TYPE in {page}: '{page_type}' (valid: {', '.join(sorted(VALID_PAGE_TYPES))})")
            # Check type-specific required frontmatter
            type_checks = {
                "claim": ("CLAIM", CLAIM_FRONTMATTER),
                "hypothesis": ("HYPOTHESIS", HYPOTHESIS_FRONTMATTER),
                "experiment": ("EXPERIMENT", EXPERIMENT_FRONTMATTER),
                "result": ("RESULT", RESULT_FRONTMATTER),
                "argument": ("ARGUMENT", ARGUMENT_FRONTMATTER),
                "chapter": ("CHAPTER", CHAPTER_FRONTMATTER),
                "figure": ("FIGURE", FIGURE_FRONTMATTER),
            }
            if page_type in type_checks:
                label, required = type_checks[page_type]
                type_missing = required - set(fm.keys())
                if type_missing:
                    issues.append(f"MISSING {label} FIELDS in {page}: {', '.join(sorted(type_missing))}")

            # Validate source_type on source-summary pages
            if page_type == "source-summary" and "source_type" in fm:
                if fm["source_type"] not in VALID_SOURCE_TYPES:
                    issues.append(f"INVALID SOURCE_TYPE in {page}: '{fm['source_type']}' (valid: {', '.join(sorted(VALID_SOURCE_TYPES))})")

            # Validate enum values
            enum_checks = {
                "evidence_level": ("evidence_level", VALID_EVIDENCE_LEVELS),
                "confidence": ("confidence", VALID_CONFIDENCE),
                "replication_status": ("replication_status", VALID_REPLICATION_STATUS),
                "strength": ("strength", VALID_STRENGTH),
                "figure_type": ("figure_type", VALID_FIGURE_TYPE),
                "chapter_type": ("chapter_type", VALID_CHAPTER_TYPE),
                "hypothesis_supported": ("hypothesis_supported", VALID_HYPOTHESIS_SUPPORTED),
            }
            # Status field has different valid values depending on page type
            if page_type == "hypothesis":
                enum_checks["status"] = ("status", VALID_HYPOTHESIS_STATUS)
            elif page_type == "experiment":
                enum_checks["status"] = ("status", VALID_EXPERIMENT_STATUS)
            elif page_type == "chapter":
                enum_checks["status"] = ("status", VALID_CHAPTER_STATUS)

            for field, (field_name, valid_values) in enum_checks.items():
                if field in fm:
                    val = fm[field]
                    if val not in valid_values:
                        issues.append(f"INVALID {field_name.upper()} in {page}: '{val}' (valid: {', '.join(str(v) for v in sorted(valid_values, key=str))})")
    return issues


def lint_special_files() -> List[str]:
    """Check that special wiki files have valid frontmatter types."""
    issues = []
    for name in SPECIAL_FILES:
        path = WIKI_DIR / name
        if not path.exists():
            issues.append(f"MISSING SPECIAL FILE: {path}")
            continue
        fm = extract_frontmatter(path)
        if fm is None:
            issues.append(f"MISSING FRONTMATTER in special file: {path}")
            continue
        if "type" in fm:
            page_type = str(fm["type"]).strip()
            if page_type not in VALID_SPECIAL_TYPES:
                issues.append(f"INVALID SPECIAL TYPE in {path}: '{page_type}' (valid: {', '.join(sorted(VALID_SPECIAL_TYPES))})")
    return issues


def lint_wikilinks(pages: List[Path]) -> List[str]:
    """Check that all wikilinks resolve to existing files."""
    issues = []
    all_rel_paths = set()
    stem_to_paths: Dict[str, List[str]] = {}
    for p in WIKI_DIR.rglob("*.md"):
        rel = str(p.relative_to(WIKI_DIR).with_suffix(""))
        all_rel_paths.add(rel)
        stem_to_paths.setdefault(p.stem, []).append(rel)

    # Warn about ambiguous stems (same filename in different directories)
    for stem, paths in stem_to_paths.items():
        if len(paths) > 1:
            issues.append(f"AMBIGUOUS STEM '{stem}' matches multiple files: {', '.join(sorted(paths))}")

    all_pages = list(WIKI_DIR.rglob("*.md"))
    for page in all_pages:
        links = find_wikilinks(page)
        for link in links:
            link_clean = link.replace(".md", "")
            # Resolve by relative path first, then by stem
            if link_clean not in all_rel_paths:
                # Try stem-based resolution
                if link_clean not in stem_to_paths:
                    issues.append(f"BROKEN LINK in {page}: [[{link}]]")
                elif len(stem_to_paths[link_clean]) > 1:
                    issues.append(f"AMBIGUOUS LINK in {page}: [[{link}]] matches {', '.join(stem_to_paths[link_clean])}")
    return issues


def lint_index_consistency() -> List[str]:
    """Check that all wiki pages are listed in index.md."""
    issues = []
    index_path = WIKI_DIR / "index.md"
    if not index_path.exists():
        issues.append("MISSING: wiki/index.md")
        return issues

    index_text = index_path.read_text(encoding="utf-8")
    index_links = set(re.findall(r"\[\[([^\]]+)\]\]", index_text))

    pages = get_wiki_pages()
    for page in pages:
        rel = str(page.relative_to(WIKI_DIR).with_suffix(""))
        # Check if the page is referenced in the index
        if rel not in index_links and page.name not in SPECIAL_FILES:
            issues.append(f"NOT IN INDEX: {page}")
    return issues


RAW_REQUIRED_FIELDS = {"title", "authors", "year", "type", "evidence_level", "peer_reviewed"}
VALID_SOURCE_TYPES = {"paper", "preprint", "review", "meta-analysis", "dataset", "talk", "textbook", "field-notes"}


def lint_raw_sources() -> List[str]:
    """Check that raw sources have complete frontmatter per CLAUDE.md spec."""
    issues = []
    for p in RAW_DIR.rglob("*.md"):
        fm = extract_frontmatter(p)
        if fm is None:
            issues.append(f"RAW SOURCE MISSING FRONTMATTER: {p}")
            continue
        missing = RAW_REQUIRED_FIELDS - set(fm.keys())
        if missing:
            issues.append(f"RAW SOURCE MISSING FIELDS in {p}: {', '.join(sorted(missing))}")
        if "type" in fm and fm["type"] not in VALID_SOURCE_TYPES:
            issues.append(f"RAW SOURCE INVALID TYPE in {p}: '{fm['type']}' (valid: {', '.join(sorted(VALID_SOURCE_TYPES))})")
        if "evidence_level" in fm and fm["evidence_level"] not in VALID_EVIDENCE_LEVELS:
            issues.append(f"RAW SOURCE INVALID EVIDENCE LEVEL in {p}: '{fm['evidence_level']}' (valid: 1-5)")
    return issues


def lint_claims_table() -> List[str]:
    """Check that claims.md references all claim pages."""
    issues = []
    claims_path = WIKI_DIR / "claims.md"
    if not claims_path.exists():
        issues.append("MISSING: wiki/claims.md")
        return issues

    claims_text = claims_path.read_text(encoding="utf-8")
    claims_links = set(re.findall(r"\[\[([^\]]+)\]\]", claims_text))

    claims_dir = WIKI_DIR / "claims"
    if claims_dir.exists():
        for p in claims_dir.glob("*.md"):
            rel = f"claims/{p.stem}"
            if rel not in claims_links:
                issues.append(f"CLAIM NOT IN CLAIMS TABLE: {p}")
    return issues


def lint_hypotheses_index() -> List[str]:
    """Check that hypotheses-index.md references all hypothesis pages."""
    issues = []
    index_path = WIKI_DIR / "hypotheses-index.md"
    if not index_path.exists():
        issues.append("MISSING: wiki/hypotheses-index.md")
        return issues

    index_text = index_path.read_text(encoding="utf-8")
    index_links = set(re.findall(r"\[\[([^\]]+)\]\]", index_text))

    hyp_dir = WIKI_DIR / "hypotheses"
    if hyp_dir.exists():
        for p in hyp_dir.glob("*.md"):
            rel = f"hypotheses/{p.stem}"
            if rel not in index_links:
                issues.append(f"HYPOTHESIS NOT IN INDEX: {p}")
    return issues


def lint_orphan_pages() -> List[str]:
    """Check for wiki pages with no inbound wikilinks from other pages."""
    issues = []
    # Collect all inbound links across the entire wiki
    inbound: Dict[str, int] = {}
    all_pages = list(WIKI_DIR.rglob("*.md"))
    for p in all_pages:
        rel = str(p.relative_to(WIKI_DIR).with_suffix(""))
        inbound.setdefault(rel, 0)

    for p in all_pages:
        links = find_wikilinks(p)
        source_rel = str(p.relative_to(WIKI_DIR).with_suffix(""))
        for link in links:
            link_clean = link.replace(".md", "")
            # Count as inbound for the target (try full path, then stem)
            if link_clean in inbound:
                inbound[link_clean] += 1
            else:
                # Try stem-based match
                for rel in inbound:
                    if rel.endswith("/" + link_clean) or rel == link_clean:
                        inbound[rel] += 1
                        break

    for rel, count in inbound.items():
        path = WIKI_DIR / (rel + ".md")
        if path.name in SPECIAL_FILES:
            continue
        if count == 0:
            issues.append(f"ORPHAN PAGE (no inbound links): {path}")
    return issues


def main():
    all_issues = []
    pages = get_wiki_pages()

    print("LLM SciWiki Lint Report")
    print("=" * 50)

    # Run all checks
    checks = [
        ("Frontmatter", lint_frontmatter(pages)),
        ("Special files", lint_special_files()),
        ("Wikilinks", lint_wikilinks(pages)),
        ("Index consistency", lint_index_consistency()),
        ("Raw sources", lint_raw_sources()),
        ("Claims table", lint_claims_table()),
        ("Hypotheses index", lint_hypotheses_index()),
        ("Orphan pages", lint_orphan_pages()),
    ]

    for name, issues in checks:
        if issues:
            print(f"\n## {name} ({len(issues)} issues)")
            for issue in issues:
                print(f"  - {issue}")
            all_issues.extend(issues)
        else:
            print(f"\n## {name}: OK")

    print(f"\n{'=' * 50}")
    total = len(all_issues)
    if total == 0:
        print("All checks passed.")
    else:
        print(f"{total} issue(s) found.")

    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
