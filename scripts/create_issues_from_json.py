#!/usr/bin/env python3
"""
Creates GitHub Issues from review_issues.json via gh CLI.

Usage:
    python scripts/create_issues_from_json.py              # dry-run
    python scripts/create_issues_from_json.py --apply      # actually create
    python scripts/create_issues_from_json.py --apply --limit 5  # create only first 5
"""
import json
import subprocess
import sys
import time
from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "forum_data" / "review_issues.json"
REPO = "dageci/eracun-fiskalizacija-datumi"

BODY_TEMPLATE = """## Segment dokumentacije

**Stranica:** `{stranica}`
**ID sekcije:** `{sec_id}`
**Poveznica na segment:** {url}

---

## Poziv na reviziju

Ovaj Issue je otvoren za svaki segment dokumentacije kako bismo omogućili strukturirani pregled i potvrdu sadržaja. Stručnu javnost — programere, računovođe, porezne savjetnike i predstavnike Porezne uprave — ljubazno molimo da sudjeluju.

**Načini doprinosa:**

- **Potvrda ispravnosti** — komentar u stilu: *"Potvrđujemo, sadržaj odgovara važećim propisima i praksi."*
- **Prijedlog izmjene** — opišite što biste promijenili i zašto, uz navođenje izvora (zakon, specifikacija, praksa).
- **Zahtjev za pojašnjenje** — postavite pitanje u komentaru; autor ili zajednica će pokušati odgovoriti.

Nakon postizanja konsenzusa u raspravi, izmjene se primjenjuju kroz Pull Request koji referencira ovaj Issue, čime se osigurava trajan audit trail.

---

## Tip sadržaja: `{tip}`

{autorska_napomena}

---

*Issue automatski generiran skriptom `generate_review_issues.py` radi strukturiranog pregleda dokumentacije.*
"""

AUTORSKO_TEKST = (
    "> **Napomena:** Ovo je autorski sadržaj (uvod, poruka zajednici, tehnički vodič). "
    "Po defaultu ne traži reviziju. Ako netko želi predložiti izmjenu, "
    "molimo uklonite label `status:izvan-revizije` i dodajte `status:ceka`."
)

NORMAL_TEKST = (
    "Ovaj segment je dio tehničke, pravne ili praktične dokumentacije i traži "
    "reviziju od strane stručne osobe (programer, računovođa, predstavnik Porezne uprave)."
)


def create_issue(segment, dry_run=True):
    """Create a single GitHub Issue for a segment."""
    body = BODY_TEMPLATE.format(
        stranica=segment["stranica"],
        sec_id=segment["sec_id"],
        url=segment["url"],
        tip=segment["tip"],
        autorska_napomena=AUTORSKO_TEKST if segment["autorsko"] else NORMAL_TEKST,
    )

    title = segment["issue_title"]
    labels = ",".join(segment["labels"])

    if dry_run:
        print(f"  [DRY] {title}")
        print(f"        Labels: {labels}")
        return None

    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", labels,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        url = result.stdout.strip()
        print(f"  OK  {title[:60]} -> {url}")
        return url
    except subprocess.CalledProcessError as e:
        print(f"  ERR {title[:60]}")
        print(f"      stderr: {e.stderr.strip()}")
        return None


def main():
    apply = "--apply" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])

    with open(INPUT_FILE, encoding="utf-8") as f:
        segments = json.load(f)

    if limit:
        segments = segments[:limit]
        print(f"Limited to first {limit} segments")

    if not apply:
        print(f"DRY RUN — would create {len(segments)} issues. Use --apply to execute.\n")
    else:
        print(f"Creating {len(segments)} issues on {REPO}...\n")

    created = 0
    failed = 0
    for i, seg in enumerate(segments, 1):
        print(f"[{i}/{len(segments)}] {seg['stranica']}/{seg['sec_id']}")
        url = create_issue(seg, dry_run=not apply)
        if apply:
            if url:
                created += 1
            else:
                failed += 1
            # Rate limiting — be polite
            time.sleep(0.5)

    print(f"\n{'-' * 50}")
    if apply:
        print(f"Created: {created}")
        print(f"Failed: {failed}")
    else:
        print(f"Would create: {len(segments)}")
        print("Run with --apply to create for real.")


if __name__ == "__main__":
    main()
