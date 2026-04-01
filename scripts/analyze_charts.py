#!/usr/bin/env python3
"""
Extract aggregated chart data from input XML eRačun files.
Outputs ONLY aggregated numbers - no individual data, no OIBs, no names.
"""
import os
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

ns = {
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'inv': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
    'cn': 'urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2',
    'hrextac': 'urn:porezna-uprava.gov.hr:cius:2025:extension:components',
}

# Putanje nisu uključene u repo — pokrenuti lokalno s pravim putanjama
base = os.environ.get("ERACUN_XML_DIR", ".")
folders = os.environ.get("ERACUN_XML_FOLDERS", "A/XML,B/XML,C/XML").split(",")

# Aggregation buckets
by_month = defaultdict(lambda: {"total": 0, "has_bt7": 0, "has_bt72": 0, "has_bt8": 0, "has_hrbt15": 0, "has_bt9": 0})
bt7_offset_days = Counter()  # how many days BT-7 differs from BT-2
software_patterns = Counter()  # CustomizationID patterns (anonymized)
profile_by_month = defaultdict(Counter)
bt7_bt2_by_month = defaultdict(lambda: {"same": 0, "before": 0, "after": 0, "missing": 0})
line_count_dist = Counter()  # number of invoice lines
issuer_count = set()  # unique issuer OIBs (only count, not stored)

from datetime import datetime, timedelta

def parse_date(s):
    if not s: return None
    try:
        return datetime.strptime(s.strip()[:10], "%Y-%m-%d")
    except:
        return None

for folder in folders:
    path = os.path.join(base, folder)
    if not os.path.isdir(path):
        continue
    for fname in os.listdir(path):
        if not fname.lower().endswith('.xml'):
            continue
        fpath = os.path.join(path, fname)
        try:
            tree = ET.parse(fpath)
            root = tree.getroot()
        except:
            continue

        # Determine root type
        tag = root.tag.split('}')[-1] if '}' in root.tag else root.tag

        # IssueDate
        bt2_el = root.find('.//cbc:IssueDate', ns)
        bt2 = parse_date(bt2_el.text if bt2_el is not None else None)
        if not bt2:
            continue

        month_key = bt2.strftime("%Y-%m")

        # TaxPointDate (BT-7)
        bt7_el = root.find('.//cbc:TaxPointDate', ns)
        bt7 = parse_date(bt7_el.text if bt7_el is not None else None)

        # ActualDeliveryDate (BT-72)
        bt72_el = root.find('.//cac:Delivery/cbc:ActualDeliveryDate', ns)
        has_bt72 = bt72_el is not None

        # BT-8
        bt8_el = root.find('.//cac:InvoicePeriod/cbc:DescriptionCode', ns)
        has_bt8 = bt8_el is not None

        # BT-9 DueDate
        bt9_el = root.find('.//cbc:DueDate', ns)
        has_bt9 = bt9_el is not None

        # HR-BT-15
        hrbt15 = root.find('.//{urn:porezna-uprava.gov.hr:cius:2025:extension:components}HRObracunPDVPoNaplati') is not None

        # BT-73/74
        bt73_el = root.find('.//cac:InvoicePeriod/cbc:StartDate', ns)
        bt74_el = root.find('.//cac:InvoicePeriod/cbc:EndDate', ns)

        # Profile
        profile_el = root.find('.//cbc:ProfileID', ns)
        profile = profile_el.text.strip().split(':')[-1] if profile_el is not None else "unknown"
        # Normalize
        for p in ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11"]:
            if p in profile:
                profile = p
                break

        # Count invoice lines
        lines = root.findall('.//cac:InvoiceLine', ns) or root.findall('.//cac:CreditNoteLine', ns)
        line_bucket = len(lines)
        if line_bucket == 0: line_bucket = 1
        elif line_bucket <= 5: line_bucket = line_bucket
        elif line_bucket <= 10: line_bucket = 10
        elif line_bucket <= 20: line_bucket = 20
        elif line_bucket <= 50: line_bucket = 50
        else: line_bucket = 100

        # Issuer OIB (only count unique, never store)
        issuer_el = root.find('.//cac:AccountingSupplierParty//cbc:CompanyID', ns)
        if issuer_el is not None and issuer_el.text:
            issuer_count.add(issuer_el.text.strip())

        # Software / CustomizationID (anonymize - just count pattern types)
        cust_el = root.find('.//cbc:CustomizationID', ns)
        if cust_el is not None and cust_el.text:
            cid = cust_el.text.strip()
            if 'FinaInvoice' in cid or 'MojEracun' in cid:
                software_patterns['Stari format (pre-F2)'] += 1
            elif 'urn:cen.eu:en16931' in cid:
                software_patterns['EN 16931 (F2)'] += 1
            else:
                software_patterns['Ostalo'] += 1

        # === Aggregate ===
        by_month[month_key]["total"] += 1
        if bt7: by_month[month_key]["has_bt7"] += 1
        if has_bt72: by_month[month_key]["has_bt72"] += 1
        if has_bt8: by_month[month_key]["has_bt8"] += 1
        if hrbt15: by_month[month_key]["has_hrbt15"] += 1
        if has_bt9: by_month[month_key]["has_bt9"] += 1

        profile_by_month[month_key][profile] += 1
        line_count_dist[line_bucket] += 1

        # BT-7 offset
        if bt7 and bt2:
            delta = (bt7 - bt2).days
            if delta == 0:
                bt7_offset_days[0] += 1
                bt7_bt2_by_month[month_key]["same"] += 1
            elif delta < 0:
                bucket = delta if delta >= -5 else (-10 if delta >= -10 else (-30 if delta >= -30 else -60))
                bt7_offset_days[bucket] += 1
                bt7_bt2_by_month[month_key]["before"] += 1
            else:
                bt7_offset_days[delta if delta <= 5 else 10] += 1
                bt7_bt2_by_month[month_key]["after"] += 1
        elif not bt7:
            bt7_bt2_by_month[month_key]["missing"] += 1


# === Output aggregated results ===
print("=" * 60)
print("AGREGIRANI PODACI ZA GRAFOVE")
print("=" * 60)

print("\n1. PO MJESECIMA:")
for m in sorted(by_month.keys()):
    d = by_month[m]
    t = d["total"]
    print(f"  {m}: {t} racuna | BT-7: {d['has_bt7']} ({d['has_bt7']*100//t}%) | BT-72: {d['has_bt72']} ({d['has_bt72']*100//t}%) | HR-BT-15: {d['has_hrbt15']} | BT-9: {d['has_bt9']} ({d['has_bt9']*100//t}%)")

print(f"\n2. JEDINSTVENIH IZDAVATELJA: {len(issuer_count)}")

print("\n3. BT-7 OFFSET (dani razlike od BT-2):")
for k in sorted(bt7_offset_days.keys()):
    label = f"{k:+d}" if k != 0 else "0"
    print(f"  {label} dana: {bt7_offset_days[k]}")

print("\n4. BT-7 vs BT-2 PO MJESECIMA:")
for m in sorted(bt7_bt2_by_month.keys()):
    d = bt7_bt2_by_month[m]
    print(f"  {m}: isti={d['same']} prije={d['before']} nakon={d['after']} bez={d['missing']}")

print("\n5. PROFILI PO MJESECIMA:")
for m in sorted(profile_by_month.keys()):
    top = profile_by_month[m].most_common(5)
    parts = ", ".join(f"{p}: {c}" for p, c in top)
    print(f"  {m}: {parts}")

print("\n6. BROJ STAVKI NA RACUNU:")
for k in sorted(line_count_dist.keys()):
    label = f"{k}" if k <= 5 else f"{k}+"  if k < 100 else "50+"
    print(f"  {label} stavki: {line_count_dist[k]}")

print("\n7. FORMAT (CustomizationID):")
for k, v in software_patterns.most_common():
    print(f"  {k}: {v}")
