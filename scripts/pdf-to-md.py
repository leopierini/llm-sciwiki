#!/usr/bin/env python3
"""
Convert a PDF paper to markdown for ingestion into LLM SciWiki.

Usage:
    python scripts/pdf-to-md.py path/to/paper.pdf [--output raw/papers/author-year-keyword.md]

If --output is omitted, prints to stdout so you can review before saving.

Requires: pymupdf4llm (pip install pymupdf4llm)
"""

import argparse
import sys

try:
    import pymupdf4llm
except ImportError:
    print(
        "ERROR: pymupdf4llm is required.\n"
        "Install with: pip install pymupdf4llm\n"
        "Or install all script dependencies: pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(2)


FRONTMATTER_STUB = """\
---
title: ""
authors: []
year:
journal: ""
doi: ""
type: paper
evidence_level:
peer_reviewed: true
tags: []
methods: []
---

"""


def convert(pdf_path: str) -> str:
    """Convert a PDF file to markdown text."""
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return FRONTMATTER_STUB + md_text


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF paper to markdown for SciWiki ingestion."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--output", "-o",
        help="Output markdown file path (default: print to stdout)",
    )
    args = parser.parse_args()

    md = convert(args.pdf)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Written to {args.output}", file=sys.stderr)
        print("Remember to fill in the YAML frontmatter fields.", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main()
