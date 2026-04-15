#!/usr/bin/env python3
"""
Adds stable {#sec-xxx} IDs to all H2/H3 headings in docs/*.md files.

Purpose: Headings can be renamed without breaking anchor links.
Issue/PR references use the stable ID instead of the auto-generated slug.

Usage:
    python scripts/add_section_ids.py              # dry-run preview
    python scripts/add_section_ids.py --apply      # apply changes
"""
import os
import re
import sys
import unicodedata
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# Match H2 and H3 headings that don't already have a {#id}
HEADING_RE = re.compile(r'^(#{2,3})\s+(.+?)(\s*\{#[^}]+\})?\s*$', re.MULTILINE)

# Skip files that are meta/nav (no review needed)
SKIP_FILES = {
    "404.md",
    "privatnost-statistika.md",
}


def slugify(text):
    """Convert heading text to a stable slug ID."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove markdown formatting
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'`', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove leading numbering like "3.1" or "3.1."
    text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', text)
    # Normalize Croatian diacritics
    replacements = {
        'č': 'c', 'Č': 'c', 'ć': 'c', 'Ć': 'c',
        'š': 's', 'Š': 's', 'ž': 'z', 'Ž': 'z',
        'đ': 'd', 'Đ': 'd',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Keep only alphanumeric and replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    # Limit length
    return text[:50].rstrip('-')


def short_id(slug):
    """Shorten very long slugs to key words."""
    words = slug.split('-')
    if len(words) <= 4:
        return slug
    # Keep first 3 + last if numeric
    keep = words[:3]
    if words[-1].isdigit() or (len(words[-1]) <= 3 and words[-1].isalpha()):
        keep.append(words[-1])
    return '-'.join(keep)


def process_file(filepath, apply=False):
    """Add stable IDs to all H2/H3 headings in a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip frontmatter
    fm_end = 0
    if content.startswith('---\n'):
        fm_end = content.index('\n---\n', 4) + 5

    body = content[fm_end:]

    # Track used IDs per file to avoid collisions
    used_ids = set()
    # Pre-scan existing IDs
    for m in re.finditer(r'\{#([^}]+)\}', body):
        used_ids.add(m.group(1))

    changes = []

    def replace_heading(match):
        level = match.group(1)
        heading_text = match.group(2).strip()
        existing_id = match.group(3)

        # Skip if already has an ID
        if existing_id:
            return match.group(0)

        # Only process H2 and H3
        if len(level) not in (2, 3):
            return match.group(0)

        # Generate slug
        slug = slugify(heading_text)
        if not slug:
            return match.group(0)

        sec_id = f"sec-{short_id(slug)}"

        # Ensure uniqueness
        base_id = sec_id
        counter = 2
        while sec_id in used_ids:
            sec_id = f"{base_id}-{counter}"
            counter += 1

        used_ids.add(sec_id)
        changes.append((heading_text, sec_id))
        return f"{level} {heading_text} {{#{sec_id}}}"

    new_body = HEADING_RE.sub(replace_heading, body)
    new_content = content[:fm_end] + new_body

    if changes and apply:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return changes


def main():
    apply = '--apply' in sys.argv
    if not apply:
        print("DRY RUN — no files will be modified. Use --apply to write.\n")

    total_changes = 0
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        if md_file.name in SKIP_FILES:
            continue

        changes = process_file(md_file, apply=apply)
        if changes:
            print(f"{md_file.name}: {len(changes)} headings")
            for heading, sec_id in changes[:5]:
                print(f"  + {sec_id}  <- {heading[:60]}")
            if len(changes) > 5:
                print(f"  ... and {len(changes) - 5} more")
            total_changes += len(changes)

    print(f"\nTotal: {total_changes} headings to update")
    if not apply:
        print("Run with --apply to write changes.")


if __name__ == "__main__":
    main()
