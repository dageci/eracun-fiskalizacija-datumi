#!/usr/bin/env python3
"""
Adds blank lines after headings with {#sec-xxx} IDs when followed
directly by a table, list, code block or blockquote.

Reason: Kramdown requires blank line between block-level IAL attributes
and the following content.

Usage:
    python scripts/fix_blank_lines_after_headings.py           # dry run
    python scripts/fix_blank_lines_after_headings.py --apply
"""
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"


def process_file(path, apply=False):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    result = []
    changes = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)

        # Check if this is a heading with {#sec-xxx}
        if re.match(r"^#{1,6}\s+.+\{#[^}]+\}\s*$", line):
            # Check next non-empty-ish line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # If immediately followed by table, list, code, blockquote or another heading
                needs_blank = (
                    next_line.startswith("|")
                    or next_line.startswith("- ")
                    or next_line.startswith("* ")
                    or next_line.startswith("1. ")
                    or next_line.startswith("> ")
                    or next_line.startswith("```")
                    or next_line.startswith("<div")
                    or next_line.startswith("<table")
                    or (next_line and next_line[0] in "|-*>" )
                )
                if needs_blank and next_line.strip() != "":
                    result.append("")
                    changes += 1
        i += 1

    if changes and apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(result))

    return changes


def main():
    apply = "--apply" in sys.argv
    if not apply:
        print("DRY RUN — use --apply to write.\n")

    total = 0
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        changes = process_file(md_file, apply=apply)
        if changes:
            print(f"  {md_file.name}: {changes} blank lines to add")
            total += changes

    print(f"\nTotal: {total} blank lines to add")
    if not apply:
        print("Run with --apply to write.")


if __name__ == "__main__":
    main()
