#!/usr/bin/env python3
"""
Deep analysis of input XML eRačun files for interesting patterns.
Outputs ONLY aggregated numbers - no individual data, no OIBs, no names.
"""
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime

ns = {
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'hrextac': 'urn:porezna-uprava.gov.hr:cius:2025:extension:components',
}

base = "."
folders = ["A/XML", "B/XML", "C/XML"]

def parse_date(s):
    if not s: return None
    try: return datetime.strptime(s.strip()[:10], "%Y-%m-%d")
    except: return None

def safe_float(s):
    if not s: return 0.0
    try: return float(s.strip())
    except: return 0.0

def safe_text(el):
    return el.text.strip() if el is not None and el.text else ""

# ===== Aggregation structures =====

# PDV stope
tax_rates = Counter()
tax_rate_combos = Counter()  # koliko racuna ima jednu vs vise stopa
tax_categories = Counter()  # S, E, O, AE, K, G...

# Valute
currencies = Counter()

# Načini plaćanja (PaymentMeansCode)
payment_means = Counter()

# Broj attachmenta (EmbeddedDocumentBinaryObject)
has_attachment = 0
attachment_mimetypes = Counter()

# Veličina računa (file size)
size_buckets = Counter()

# Poziv na broj (PaymentID / BT-83)
has_payment_id = 0

# OrderReference (BT-13)
has_order_ref = 0

# ContractReference (BT-12)
has_contract_ref = 0

# BillingReference (BT-25) na Invoice
has_billing_ref_invoice = 0
has_billing_ref_credit = 0

# Discount (AllowanceCharge)
has_doc_allowance = 0  # dokument level popust
has_doc_charge = 0     # dokument level trošak (POVNAK, PP)
has_line_allowance = 0 # stavka level popust

# HR ekstenzije
has_hr_extensions = 0
hr_tax_exempt_reasons = Counter()

# IssueTime prisutnost i format
has_issue_time = 0
issue_time_with_tz = 0

# Broj stavki (detaljniji)
line_counts = []

# Dan u tjednu izdavanja
weekday_dist = Counter()

# Iznosi
amount_buckets = Counter()

# Dan u mjesecu izdavanja
day_of_month = Counter()

# Broj različitih PDV stopa po računu
tax_rate_count_per_invoice = Counter()

# Top VATEX kodovi
vatex_codes = Counter()

# ProfileID distribucija
profiles = Counter()

# Napomene (BT-22 Note)
has_note = 0

# AccountingCost (BT-19)
has_accounting_cost = 0

# BuyerReference (BT-10)
has_buyer_ref = 0

total = 0
credit_notes = 0

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

        tag = root.tag.split('}')[-1] if '}' in root.tag else root.tag
        bt2_el = root.find('.//cbc:IssueDate', ns)
        bt2 = parse_date(safe_text(bt2_el))
        if not bt2 or bt2.year < 2020:
            continue

        total += 1
        is_credit = 'CreditNote' in tag

        if is_credit:
            credit_notes += 1

        # File size
        fsize = os.path.getsize(fpath)
        if fsize < 5000: size_buckets['<5 KB'] += 1
        elif fsize < 10000: size_buckets['5-10 KB'] += 1
        elif fsize < 20000: size_buckets['10-20 KB'] += 1
        elif fsize < 50000: size_buckets['20-50 KB'] += 1
        elif fsize < 100000: size_buckets['50-100 KB'] += 1
        else: size_buckets['>100 KB'] += 1

        # Currency
        cur_el = root.find('.//cbc:DocumentCurrencyCode', ns)
        currencies[safe_text(cur_el) or 'nepoznato'] += 1

        # Profile
        prof_el = root.find('.//cbc:ProfileID', ns)
        prof = safe_text(prof_el)
        for p in ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11"]:
            if p in prof:
                profiles[p] += 1
                break
        else:
            profiles['ostalo'] += 1

        # IssueTime
        time_el = root.find('.//cbc:IssueTime', ns)
        if time_el is not None and time_el.text:
            has_issue_time += 1
            if '+' in time_el.text or 'Z' in time_el.text:
                issue_time_with_tz += 1

        # Day of week & day of month
        weekday_dist[bt2.strftime('%A')] += 1
        day_of_month[bt2.day] += 1

        # PaymentMeansCode
        pm_el = root.find('.//cac:PaymentMeans/cbc:PaymentMeansCode', ns)
        payment_means[safe_text(pm_el) or 'nema'] += 1

        # PaymentID (BT-83 poziv na broj)
        pid_el = root.find('.//cac:PaymentMeans/cbc:PaymentID', ns)
        if pid_el is not None and pid_el.text:
            has_payment_id += 1

        # OrderReference
        or_el = root.find('.//cac:OrderReference/cbc:ID', ns)
        if or_el is not None and or_el.text:
            has_order_ref += 1

        # ContractDocumentReference
        cr_el = root.find('.//cac:ContractDocumentReference/cbc:ID', ns)
        if cr_el is not None and cr_el.text:
            has_contract_ref += 1

        # BillingReference
        br_el = root.find('.//cac:BillingReference', ns)
        if br_el is not None:
            if is_credit:
                has_billing_ref_credit += 1
            else:
                has_billing_ref_invoice += 1

        # Note (BT-22)
        note_el = root.find('.//cbc:Note', ns)
        if note_el is not None and note_el.text and len(note_el.text.strip()) > 0:
            has_note += 1

        # BuyerReference (BT-10)
        bref_el = root.find('.//cbc:BuyerReference', ns)
        if bref_el is not None and bref_el.text:
            has_buyer_ref += 1

        # AccountingCost (BT-19)
        ac_el = root.find('.//cbc:AccountingCost', ns)
        if ac_el is not None and ac_el.text:
            has_accounting_cost += 1

        # Attachments
        att_els = root.findall('.//cac:AdditionalDocumentReference', ns)
        for att in att_els:
            bin_el = att.find('.//cbc:EmbeddedDocumentBinaryObject', ns)
            if bin_el is not None:
                has_attachment += 1
                mt = bin_el.get('mimeCode', 'unknown')
                attachment_mimetypes[mt] += 1
                break  # count per invoice, not per attachment

        # AllowanceCharge at document level
        for ac in root.findall('./cac:AllowanceCharge', ns):
            ci_el = ac.find('cbc:ChargeIndicator', ns)
            if ci_el is not None:
                if ci_el.text.strip().lower() == 'false':
                    has_doc_allowance += 1
                    break
                elif ci_el.text.strip().lower() == 'true':
                    has_doc_charge += 1
                    break

        # AllowanceCharge at line level
        line_tag = './/cac:CreditNoteLine' if is_credit else './/cac:InvoiceLine'
        inv_lines = root.findall(line_tag, ns)
        line_count = len(inv_lines)
        if line_count > 0:
            line_counts.append(line_count)

        for line in inv_lines:
            lac = line.find('cac:AllowanceCharge', ns)
            if lac is not None:
                has_line_allowance += 1
                break

        # Tax rates and categories
        tax_subtotals = root.findall('.//cac:TaxTotal/cac:TaxSubtotal', ns)
        rates_this = []
        cats_this = []
        for ts in tax_subtotals:
            pct_el = ts.find('.//cbc:Percent', ns)
            cat_el = ts.find('.//cac:TaxCategory/cbc:ID', ns)
            if pct_el is not None:
                rate = safe_float(pct_el.text)
                rates_this.append(rate)
                tax_rates[rate] += 1
            if cat_el is not None:
                cat = safe_text(cat_el)
                cats_this.append(cat)
                tax_categories[cat] += 1

            # VATEX
            reason_el = ts.find('.//cac:TaxCategory/cbc:TaxExemptionReasonCode', ns)
            if reason_el is not None and reason_el.text:
                vatex_codes[reason_el.text.strip()] += 1

        tax_rate_count_per_invoice[len(set(rates_this))] += 1
        if rates_this:
            combo = "+".join(f"{r:.0f}%" for r in sorted(set(rates_this)))
            tax_rate_combos[combo] += 1

        # HR extensions
        hr_ext = root.find('.//{urn:porezna-uprava.gov.hr:cius:2025:extension:components}HRFISK20Data')
        if hr_ext is not None:
            has_hr_extensions += 1

        # Amount bucket
        payable_el = root.find('.//cac:LegalMonetaryTotal/cbc:PayableAmount', ns)
        amt = safe_float(safe_text(payable_el))
        if amt <= 0: amount_buckets['<= 0 EUR'] += 1
        elif amt < 10: amount_buckets['0-10 EUR'] += 1
        elif amt < 50: amount_buckets['10-50 EUR'] += 1
        elif amt < 100: amount_buckets['50-100 EUR'] += 1
        elif amt < 500: amount_buckets['100-500 EUR'] += 1
        elif amt < 1000: amount_buckets['500-1000 EUR'] += 1
        elif amt < 5000: amount_buckets['1000-5000 EUR'] += 1
        elif amt < 10000: amount_buckets['5000-10000 EUR'] += 1
        else: amount_buckets['>10000 EUR'] += 1


# ===== Output =====
print("=" * 60)
print(f"DUBOKA ANALIZA — {total} racuna od {len(folders)} komitenata")
print("=" * 60)

print(f"\n=== OSNOVNI PODACI ===")
print(f"  Ukupno: {total} | CreditNote: {credit_notes} ({credit_notes*100//total}%)")
print(f"  Jedinstvenih izdavatelja: (izracunato ranije - 244)")

print(f"\n=== IZNOSI (PayableAmount) ===")
order = ['<= 0 EUR','0-10 EUR','10-50 EUR','50-100 EUR','100-500 EUR','500-1000 EUR','1000-5000 EUR','5000-10000 EUR','>10000 EUR']
for k in order:
    if k in amount_buckets:
        print(f"  {k}: {amount_buckets[k]} ({amount_buckets[k]*100//total}%)")

print(f"\n=== PDV STOPE ===")
for r, c in tax_rates.most_common():
    print(f"  {r:.1f}%: {c} pojavljivanja")

print(f"\n=== PDV KATEGORIJE ===")
for cat, c in tax_categories.most_common():
    print(f"  {cat}: {c}")

print(f"\n=== BROJ STOPA PO RACUNU ===")
for k in sorted(tax_rate_count_per_invoice.keys()):
    print(f"  {k} stopa: {tax_rate_count_per_invoice[k]} racuna")

print(f"\n=== TOP KOMBINACIJE STOPA ===")
for combo, c in tax_rate_combos.most_common(10):
    print(f"  {combo}: {c}")

print(f"\n=== VATEX KODOVI (razlog oslobodenja) ===")
for code, c in vatex_codes.most_common(10):
    print(f"  {code}: {c}")

print(f"\n=== NACIN PLACANJA ===")
for pm, c in payment_means.most_common():
    print(f"  {pm}: {c}")

print(f"\n=== VALUTA ===")
for cur, c in currencies.most_common():
    print(f"  {cur}: {c}")

print(f"\n=== PROFILI ===")
for p, c in profiles.most_common():
    print(f"  {p}: {c} ({c*100//total}%)")

print(f"\n=== REFERENCIJE I METAPODACI ===")
print(f"  Poziv na broj (BT-83): {has_payment_id} ({has_payment_id*100//total}%)")
print(f"  Narudžbenica (BT-13): {has_order_ref} ({has_order_ref*100//total}%)")
print(f"  Ugovor (BT-12): {has_contract_ref} ({has_contract_ref*100//total}%)")
print(f"  BillingRef na Invoice: {has_billing_ref_invoice}")
print(f"  BillingRef na CreditNote: {has_billing_ref_credit}")
print(f"  Napomena (BT-22): {has_note} ({has_note*100//total}%)")
print(f"  BuyerReference (BT-10): {has_buyer_ref} ({has_buyer_ref*100//total}%)")
print(f"  AccountingCost (BT-19): {has_accounting_cost} ({has_accounting_cost*100//total}%)")

print(f"\n=== POPUSTI I TROSKOVI ===")
print(f"  Dokument-level popust: {has_doc_allowance} ({has_doc_allowance*100//total}%)")
print(f"  Dokument-level trosak (POVNAK/PP): {has_doc_charge} ({has_doc_charge*100//total}%)")
print(f"  Stavka-level popust: {has_line_allowance} ({has_line_allowance*100//total}%)")

print(f"\n=== PRILOZI (ATTACHMENTS) ===")
print(f"  Racuni s prilogom: {has_attachment} ({has_attachment*100//total}%)")
for mt, c in attachment_mimetypes.most_common():
    print(f"    {mt}: {c}")

print(f"\n=== HR EKSTENZIJE ===")
print(f"  Ima HRFISK20Data: {has_hr_extensions} ({has_hr_extensions*100//total}%)")

print(f"\n=== ISSUETIME ===")
print(f"  Ima IssueTime: {has_issue_time} ({has_issue_time*100//total}%)")
print(f"  S timezone: {issue_time_with_tz}")

print(f"\n=== VELICINA DATOTEKE ===")
size_order = ['<5 KB','5-10 KB','10-20 KB','20-50 KB','50-100 KB','>100 KB']
for k in size_order:
    if k in size_buckets:
        print(f"  {k}: {size_buckets[k]}")

print(f"\n=== BROJ STAVKI ===")
if line_counts:
    from statistics import median, mean
    print(f"  Min: {min(line_counts)}, Max: {max(line_counts)}, Medijan: {median(line_counts):.0f}, Prosjek: {mean(line_counts):.1f}")
    buckets = Counter()
    for lc in line_counts:
        if lc == 1: buckets['1'] += 1
        elif lc <= 3: buckets['2-3'] += 1
        elif lc <= 5: buckets['4-5'] += 1
        elif lc <= 10: buckets['6-10'] += 1
        elif lc <= 20: buckets['11-20'] += 1
        elif lc <= 50: buckets['21-50'] += 1
        else: buckets['50+'] += 1
    for k in ['1','2-3','4-5','6-10','11-20','21-50','50+']:
        if k in buckets:
            print(f"  {k} stavki: {buckets[k]} ({buckets[k]*100//total}%)")

print(f"\n=== DAN U TJEDNU ===")
for d in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
    if d in weekday_dist:
        print(f"  {d}: {weekday_dist[d]} ({weekday_dist[d]*100//total}%)")

print(f"\n=== DAN U MJESECU (top 10) ===")
for d, c in day_of_month.most_common(10):
    print(f"  {d}.: {c}")
