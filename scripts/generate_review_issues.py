#!/usr/bin/env python3
"""
Scans all docs/*.md files, extracts H2/H3 headings with stable IDs,
and prepares GitHub Issues for each segment (one per section).

Does NOT create issues directly — generates a JSON file that can be
reviewed and then processed by scripts/create_issues_from_json.py.

Usage:
    python scripts/generate_review_issues.py
"""
import os
import re
import json
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
OUTPUT_FILE = Path(__file__).parent.parent / "forum_data" / "review_issues.json"

BASE_URL = "https://dageci.github.io/eracun-fiskalizacija-datumi"

# Strukturni/navigacijski elementi koji se PRESKAČU potpuno (ni autorski)
SKIP_SECTION_IDS = {
    "sec-sadrzaj",  # Table of contents placeholder
}

# Autorski sadržaj (ne treba reviziju) — označit ćemo s tip:autorsko
AUTORSKE_SEKCIJE = {
    # Ključ: stranica, Vrijednost: skup ID-eva koji su autorski
    "index": {"sec-licenca"},
    "kako-doprinijeti": "ALL",  # cijela stranica
    "github-vodic": "ALL",
    "github-obavijesti": "ALL",
    "vodic-za-reviziju": "ALL",
}

# Stranice koje potpuno preskačemo
SKIP_FILES = {"404.md", "privatnost-statistika.md"}

# H2/H3 naslov s opcionalnim {#id}
HEADING_RE = re.compile(r'^(#{2,3})\s+(.+?)\s*\{#([^}]+)\}\s*$', re.MULTILINE)


def detect_tip(heading_text, next_lines):
    """Heuristic: detect content type from heading and following lines."""
    combined = (heading_text + " " + " ".join(next_lines)).lower()
    if "mermaid" in combined or "```mermaid" in combined:
        return "mermaid-graf"
    if "<?xml" in combined or "```xml" in combined:
        return "xml-primjer"
    if "ČL." in combined.upper() or "članak" in combined.lower() or "st. " in combined:
        return "citat-zakona"
    if combined.count("|") > 10:
        return "tablica"
    return "tekst"


def is_autorsko(stranica_slug, sec_id):
    """Check if section should be marked as authorial content."""
    rule = AUTORSKE_SEKCIJE.get(stranica_slug)
    if rule == "ALL":
        return True
    if rule and sec_id in rule:
        return True
    return False


def process_file(filepath):
    """Extract all segments from a markdown file."""
    stranica_slug = filepath.stem
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip frontmatter
    fm_end = 0
    if content.startswith('---\n'):
        fm_end = content.index('\n---\n', 4) + 5
    body = content[fm_end:]
    lines = body.split('\n')

    segments = []

    for line_idx, line in enumerate(lines):
        m = re.match(r'^(#{2,3})\s+(.+?)\s*\{#([^}]+)\}\s*$', line)
        if not m:
            continue

        level = len(m.group(1))
        heading = m.group(2).strip()
        sec_id = m.group(3).strip()

        # Skip structural elements (TOC, etc.)
        if sec_id in SKIP_SECTION_IDS:
            continue

        # Read next 5 lines for content type detection
        next_lines = lines[line_idx+1:line_idx+6]
        tip = detect_tip(heading, next_lines)

        autorsko = is_autorsko(stranica_slug, sec_id)

        segments.append({
            "stranica": stranica_slug,
            "sec_id": sec_id,
            "heading": heading,
            "level": level,
            "tip": tip,
            "autorsko": autorsko,
            "url": f"{BASE_URL}/{stranica_slug}#{sec_id}",
            "issue_title": f"[{stranica_slug}] {heading[:80]}",
            "labels": [
                f"stranica:{stranica_slug}",
                f"tip:{'autorsko' if autorsko else tip}",
                "status:izvan-revizije" if autorsko else "status:ceka",
            ],
        })

    return segments


def main():
    all_segments = []
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        if md_file.name in SKIP_FILES:
            continue
        segments = process_file(md_file)
        if segments:
            print(f"{md_file.name}: {len(segments)} segmenata "
                  f"({sum(1 for s in segments if s['autorsko'])} autorskih)")
            all_segments.extend(segments)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_segments, f, ensure_ascii=False, indent=2)

    # Summary
    total = len(all_segments)
    autorska = sum(1 for s in all_segments if s['autorsko'])
    po_reviziji = total - autorska

    print(f"\nUkupno: {total} segmenata")
    print(f"  Za reviziju: {po_reviziji}")
    print(f"  Autorski (izvan revizije): {autorska}")
    print(f"\nSaved: {OUTPUT_FILE}")
    print(f"\nSljedeći korak: pregledaj JSON, pa pokreni")
    print(f"  python scripts/create_issues_from_json.py")


if __name__ == "__main__":
    main()
