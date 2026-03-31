#!/usr/bin/env python3
"""
Analyzes scraped forum.hr posts for topics relevant to eRačun documentation project.
Groups posts by topic, extracts key findings, and outputs summaries.
"""

import json
import re
import sys
import os
from collections import Counter, defaultdict

INPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "forum_data", "all_posts.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "forum_data", "topics")

# Topic definitions: keyword patterns (case-insensitive) grouped by topic
TOPICS = {
    "datumi_bt7_bt8": {
        "name": "BT-7, BT-8, TaxPointDate — datum porezne obveze",
        "patterns": [
            r"BT-?7\b", r"BT-?8\b", r"TaxPointDate", r"DescriptionCode",
            r"datum(?:a)?\s+porezn", r"porezn[aei]\s+obvez[ae].*datum",
            r"datum(?:a)?\s+(?:za\s+)?PDV", r"ValueDate",
        ],
    },
    "datumi_bt72_isporuka": {
        "name": "BT-72, ActualDeliveryDate — datum isporuke",
        "patterns": [
            r"BT-?72\b", r"ActualDeliveryDate", r"datum\s+isporuk",
            r"DeliveryDate", r"isporuk[aeu].*datum",
        ],
    },
    "datumi_bt73_74_razdoblje": {
        "name": "BT-73/74, InvoicePeriod — obračunsko razdoblje",
        "patterns": [
            r"BT-?73\b", r"BT-?74\b", r"InvoicePeriod",
            r"obr[aã]?[cč]?unsk[oaie]\s+razdo",
            r"StartDate", r"EndDate",
            r"razdoblj[aeu]",
        ],
    },
    "hrbt15_po_naplati": {
        "name": "HR-BT-15, obračun po naplati",
        "patterns": [
            r"HR-?BT-?15", r"po\s+naplat", r"napl[aã]?[cč]?en[aoie]?\s+naknad",
            r"125\.?i", r"obr[aã]?[cč]?un.*naplat",
            r"PoNaplati", r"HRObracunPDV",
        ],
    },
    "bt9_duedate_rok": {
        "name": "BT-9, DueDate — rok plaćanja",
        "patterns": [
            r"BT-?9\b", r"DueDate", r"rok\s+pla[cć]anj",
            r"datum\s+dospij", r"dospije[cć]",
        ],
    },
    "indikator_kopije": {
        "name": "Indikator kopije / CopyIndicator",
        "patterns": [
            r"(?:indikator|indicator)\s+kopij", r"CopyIndicator",
            r"kopij[aeu]\s+ra[cč]un", r"[cč]l\.?\s*43",
            r"isprav[akci]+.*kopij",
        ],
    },
    "creditnote_odobrenje": {
        "name": "CreditNote / odobrenje / storno",
        "patterns": [
            r"CreditNote", r"odobrenje", r"storno",
            r"381", r"knji[zž]no\s+odobr",
            r"credit\s*note",
        ],
    },
    "schematron_validacija": {
        "name": "Schematron / validacija / BR pravila",
        "patterns": [
            r"[Ss]chematron", r"validacij", r"validator",
            r"BR-CO-\d+", r"HR-BR-\d+",
            r"fatal.*error", r"validation.*error",
            r"schematron.*pravil",
        ],
    },
    "posrednici_mer_pondi": {
        "name": "Posrednici — MER, PONDI, ePoslovanje, Moj-eRačun",
        "patterns": [
            r"\bMER\b", r"PONDI", r"ePoslovanje",
            r"Moj[\s-]?e[\s-]?[Rr]a[cč]un", r"MojEracun",
            r"posredni[kcčk]", r"pristupn[aieu]\s+to[cč]k",
            r"access\s*point", r"Adriasoft", r"Setcce",
            r"FINA\s+(?:posred|eR)", r"Fiscalis",
        ],
    },
    "fiskaplikacija": {
        "name": "FiskAplikacija — PU sustav",
        "patterns": [
            r"[Ff]isk[Aa]plikacij", r"FiskAplikacija",
            r"Fiskapl", r"aplikacij[aeu]\s+(?:PU|poreznr)",
            r"porezn[aie].*aplikacij",
        ],
    },
    "eizvjestavanje": {
        "name": "eIzvještavanje — naplata, odbijanje, isporuka",
        "patterns": [
            r"eIzvje[sš]tav", r"izvje[sš]tav",
            r"EvidentirajNaplat", r"EvidentirajOdbij",
            r"EvidentirajIsporuk",
            r"evidenti.*naplat", r"evidenti.*odbij",
            r"naplat[aeu].*izvje[sš]",
        ],
    },
    "fiskalizacijska_poruka": {
        "name": "Fiskalizacijska SOAP poruka / EvidentirajERacun",
        "patterns": [
            r"EvidentirajERacun", r"fiskalizacijs[ka].*poruk",
            r"SOAP.*fiskali", r"fiskali.*SOAP",
            r"fiskali.*XML", r"potpis.*fiskali",
            r"JIR\b", r"ZKI\b", r"za[sš]titn[iaoe]\s+kod",
        ],
    },
    "xml_ubl_format": {
        "name": "XML / UBL format / struktura",
        "patterns": [
            r"\bUBL\b", r"xmlns", r"cac:", r"cbc:",
            r"XML\s+(?:struktur|format|element|tag)",
            r"AccountingSupplierParty", r"AccountingCustomerParty",
            r"TaxTotal", r"LegalMonetaryTotal",
            r"InvoiceLine", r"AllowanceCharge",
        ],
    },
    "kpd_nkd": {
        "name": "KPD / NKD klasifikacija",
        "patterns": [
            r"\bKPD\b", r"\bNKD\b",
            r"klasifikacij.*djelatnost",
            r"djelatnost.*klasifikacij",
        ],
    },
    "certifikat_fina": {
        "name": "Certifikat / FINA / potpis",
        "patterns": [
            r"certifik", r"FINA.*cert", r"cert.*FINA",
            r"digitalni?\s+pot[pi]s", r"elektronski?\s+pot[pi]s",
            r"privatni?\s+klju[cč]", r"javni?\s+klju[cč]",
        ],
    },
    "demo_testiranje": {
        "name": "DEMO / testiranje / test okolina",
        "patterns": [
            r"\bDEMO\b", r"demo\s+okolin", r"test\s+okolin",
            r"testir[aeiou]", r"testno\s+",
            r"sandbox",
        ],
    },
    "greske_problemi": {
        "name": "Greške / problemi / padovi sustava",
        "patterns": [
            r"gre[sš]k[aei]", r"error\s+\d+", r"HTTP\s+\d{3}",
            r"ne\s+radi", r"ne\s+prolaz", r"odbij[aeiou].*ra[cč]un",
            r"pao?\s+(?:sustav|servis|server)",
            r"timeout", r"nedostupn",
        ],
    },
    "predujam_avans": {
        "name": "Predujam / avans / advance payment",
        "patterns": [
            r"predujam", r"avans", r"advance",
            r"386\b", r"predra[cč]un",
            r"unaprijed.*pla[cć]",
        ],
    },
    "popusti_allowance": {
        "name": "Popusti / AllowanceCharge / rabat",
        "patterns": [
            r"popust", r"AllowanceCharge", r"rabat",
            r"Allowance", r"Charge\s+(?:Reason|Amount)",
            r"skonto",
        ],
    },
    "zaokruzivanje_iznosi": {
        "name": "Zaokruživanje / iznosi / decimale",
        "patterns": [
            r"zaokru[zž]", r"decimal[aei]", r"rounding",
            r"PayableRoundingAmount",
            r"0[.,]01.*razlik", r"razlik.*0[.,]01",
            r"centin",
        ],
    },
    "specifikacija_dokumentacija": {
        "name": "HR CIUS specifikacija / dokumentacija PU",
        "patterns": [
            r"specifikacij[aeu]", r"HR\s*CIUS",
            r"EN\s*16931", r"(?:tehni[cč]k|funkcion)[aei].*(?:specif|dokument)",
            r"poreznr?\s+uprav.*dokument",
            r"Clearance", r"eDelivery",
        ],
    },
}


def matches_topic(text, patterns):
    """Check if text matches any of the topic patterns."""
    text_lower = text.lower()
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def analyze_posts(posts):
    """Categorize all posts by topic."""
    topic_posts = defaultdict(list)
    uncategorized = []

    for p in posts:
        content = p.get("content", "")
        matched = False
        for topic_id, topic_def in TOPICS.items():
            if matches_topic(content, topic_def["patterns"]):
                topic_posts[topic_id].append(p)
                matched = True
        if not matched:
            uncategorized.append(p)

    return topic_posts, uncategorized


def save_topic_posts(topic_posts, output_dir):
    """Save each topic's posts to separate JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    for topic_id, posts in topic_posts.items():
        out_file = os.path.join(output_dir, f"{topic_id}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)


def print_summary(topic_posts, uncategorized, total):
    """Print analysis summary."""
    print(f"\n{'='*70}")
    print(f"ANALIZA FORUM.HR POSTOVA — Fiskalizacija za developere")
    print(f"{'='*70}")
    print(f"Ukupno postova: {total}")
    print(f"Kategorizirano: {total - len(uncategorized)} (post može biti u više kategorija)")
    print(f"Nekategorizirano: {len(uncategorized)}")
    print(f"\n{'-'*70}")
    print(f"{'Tema':<55} {'Postova':>8}")
    print(f"{'-'*70}")

    sorted_topics = sorted(topic_posts.items(), key=lambda x: -len(x[1]))
    for topic_id, posts in sorted_topics:
        name = TOPICS[topic_id]["name"]
        print(f"  {name:<53} {len(posts):>6}")

    print(f"{'-'*70}")

    # Monthly distribution
    print(f"\nMjesečna distribucija:")
    monthly = Counter()
    for topic_id, posts in topic_posts.items():
        for p in posts:
            date = p.get("date", "")
            m = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", date)
            if m:
                monthly[f"{m.group(3)}-{m.group(2)}"] += 1
    for month, count in sorted(monthly.items()):
        print(f"  {month}: {count} topic-matched posts")


if __name__ == "__main__":
    with open(INPUT_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    print(f"Loading {len(posts)} posts from {INPUT_FILE}...")
    topic_posts, uncategorized = analyze_posts(posts)
    save_topic_posts(topic_posts, OUTPUT_DIR)
    print_summary(topic_posts, uncategorized, len(posts))

    # Save summary stats
    stats = {
        "total_posts": len(posts),
        "uncategorized": len(uncategorized),
        "topics": {
            tid: {
                "name": TOPICS[tid]["name"],
                "count": len(tposts),
                "authors": dict(Counter(p["author"] for p in tposts).most_common(5)),
            }
            for tid, tposts in sorted(topic_posts.items(), key=lambda x: -len(x[1]))
        }
    }
    with open(os.path.join(OUTPUT_DIR, "_summary.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"\nTopic files saved to {OUTPUT_DIR}/")
