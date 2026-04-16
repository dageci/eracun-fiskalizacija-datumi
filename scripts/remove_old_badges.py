#!/usr/bin/env python3
"""
Removes old manual "Čeka potvrdu" HTML badges from documentation.

These are now replaced by dynamic JS-injected badges in default.html
that read from docs/_data/review_status.json.

Usage:
    python scripts/remove_old_badges.py           # dry run
    python scripts/remove_old_badges.py --apply
"""
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# Patterns to remove — whole div containing a single standalone badge
# Used old format: <div style="..."><span ...>Čeka potvrdu</span></div>
PATTERNS = [
    # Standalone div with single badge + optional trailing whitespace
    re.compile(
        r'<div style="margin-top:-?\d*\.?\d+rem;[^"]*">'
        r'\s*<span[^>]*>Čeka potvrdu</span>'
        r'\s*</div>\n?',
        re.IGNORECASE
    ),
]


def process_file(path, apply=False):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    original = content
    removed = 0

    for pat in PATTERNS:
        new_content, n = pat.subn('', content)
        content = new_content
        removed += n

    # Also clean up triple+ blank lines left behind
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    if removed and apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return removed


def main():
    apply = "--apply" in sys.argv
    if not apply:
        print("DRY RUN — use --apply to write.\n")

    total = 0
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        removed = process_file(md_file, apply=apply)
        if removed:
            print(f"  {md_file.name}: {removed} badges removed")
            total += removed

    print(f"\nTotal: {total} badges removed")
    if not apply:
        print("Run with --apply to write.")


if __name__ == "__main__":
    main()
