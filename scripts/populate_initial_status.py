#!/usr/bin/env python3
"""
Generates initial docs/_data/review_status.json with ALL 190 segments.

- Segments marked as "autorsko" get status "izvan_revizije"
- All other segments get status "ceka"

This file is the starting point; GitHub Action review-sync.yml updates
individual segment statuses as Issues change state, but preserves the
full segment list.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
REVIEW_ISSUES_JSON = ROOT / "forum_data" / "review_issues.json"
OUTPUT = ROOT / "docs" / "_data" / "review_status.json"


def main():
    with open(REVIEW_ISSUES_JSON, encoding="utf-8") as f:
        raw_segments = json.load(f)

    segments = []
    counts = {"ceka": 0, "izvan_revizije": 0}

    for seg in raw_segments:
        status = "izvan_revizije" if seg["autorsko"] else "ceka"
        counts[status] += 1

        segments.append({
            "stranica": seg["stranica"],
            "sec_id": seg["sec_id"],
            "heading": seg["heading"],
            "tip": "autorsko" if seg["autorsko"] else seg["tip"],
            "status": status,
            "issue_number": 0,
            "url": seg["url"],
        })

    summary = {
        "total": len(segments),
        "izvan_revizije": counts["izvan_revizije"],
        "za_reviziju": counts["ceka"],
        "potvrdeno": 0,
        "u_reviziji": 0,
        "ceka_pu": 0,
        "trazi_izmjenu": 0,
        "ceka": counts["ceka"],
        "odbaceno": 0,
    }

    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "segments": segments,
        "summary": summary,
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Written: {OUTPUT}")
    print(f"  Total segments: {len(segments)}")
    print(f"  Izvan revizije: {counts['izvan_revizije']}")
    print(f"  Za reviziju:    {counts['ceka']}")


if __name__ == "__main__":
    main()
