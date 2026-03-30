---
layout: default
title: "Referenca — XML, validacija, zakoni"
has_toc: true
nav_order: 6
---

# Referenca — XML struktura, validacija, zakonski temelj

Ova stranica sadrži tehničke reference — XML strukturu eRačuna, Schematron validacijska pravila i popis relevantnih zakona i propisa.

* TOC
{:toc}

---

## 6. XML struktura — pozicija elemenata

Redoslijed elemenata u UBL Invoice XML-u je strogo definiran shemom:

```xml
<!-- 1. Zaglavlje -->
<!-- 2. Datumi -->
<!-- 3. Reference -->
<!-- 4. InvoicePeriod (ako se koristi BT-8) -->
<!-- ... narudžbe, reference ... -->
<!-- 5. Isporuka -->
<!-- ... stavke, porezi, iznosi ... -->
<Invoice>
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:mfin.gov.hr:cius-2025:1.0...</cbc:CustomizationID>
  <cbc:ProfileID>P1</cbc:ProfileID>
  <cbc:ID>1/P1/2</cbc:ID>

  <cbc:IssueDate>2026-03-15</cbc:IssueDate>          <!-- BT-2:  OBAVEZNO -->
  <cbc:IssueTime>14:30:00</cbc:IssueTime>             <!-- HR-BT-2: OBAVEZNO (HR) -->
  <cbc:DueDate>2026-04-14</cbc:DueDate>               <!-- BT-9:  Rok plaćanja -->
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:Note>...</cbc:Note>
  <cbc:TaxPointDate>2026-03-10</cbc:TaxPointDate>     <!-- BT-7:  OPCIONALNO, NE uz BT-8! -->
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>

  <cbc:BuyerReference>...</cbc:BuyerReference>

  <cac:InvoicePeriod>
    <cbc:StartDate>2026-01-01</cbc:StartDate>          <!-- BT-73: opcionalno -->
    <cbc:EndDate>2026-06-30</cbc:EndDate>              <!-- BT-74: opcionalno -->
    <cbc:DescriptionCode>432</cbc:DescriptionCode>     <!-- BT-8:  NE uz BT-7! -->
  </cac:InvoicePeriod>

  <cac:Delivery>
    <cbc:ActualDeliveryDate>2026-03-10</cbc:ActualDeliveryDate>  <!-- BT-72 -->
  </cac:Delivery>

</Invoice>
```

---

## 7. Validacijska pravila za datume (Schematron)

> Sva pravila u tablici ispod su **`flag="fatal"`** — ako ih račun ne zadovolji,
> **Schematron validator odbija XML** i račun se ne može poslati posredniku.
> Pravila s prefiksom **HR-BR** dolaze iz HR CIUS 2025 schematrona (`HR-CIUS-EXT-EN16931-UBL.sch`),
> a pravila s prefiksom **BR-CO** iz europskog EN16931 schematrona (`EN16931-UBL-validation.xslt`).

| Pravilo | Izvor | Opis | Primjenjuje se na |
|---------|-------|------|-------------------|
| **HR-BR-2** | HR CIUS 2025 | Račun MORA imati HR-BT-2 / Vrijeme izdavanja (`cbc:IssueTime`) u formatu hh:mm:ss | `cbc:IssueTime` |
| **HR-BR-40** | HR CIUS 2025 | BT-2 / Datum izdavanja (`cbc:IssueDate`) mora biti >= 01.01.2026 i < 01.01.2100 | `cbc:IssueDate` |
| **HR-BR-41** | HR CIUS 2025 | BT-9 / Datum dospijeća (`cbc:DueDate`) mora biti >= 01.01.1900 i < 01.01.2100 | `cbc:DueDate` |
| **HR-BR-44** | HR CIUS 2025 | BT-72 / Stvarni datum isporuke (`cbc:ActualDeliveryDate`) mora biti >= 01.01.1900 i < 01.01.2100 | `cbc:ActualDeliveryDate` |
| **HR-BR-48** | HR CIUS 2025 | BT-7 / Datum nastanka obveze PDV-a (`cbc:TaxPointDate`) mora biti >= 01.01.1900 i < 01.01.2100 | `cbc:TaxPointDate` |
| **HR-BR-49** | HR CIUS 2025 | BT-73 / Početak obračunskog razdoblja (`cbc:StartDate`) mora biti >= 01.01.1900 i < 01.01.2100 | `cac:InvoicePeriod/cbc:StartDate` |
| **HR-BR-50** | HR CIUS 2025 | BT-74 / Kraj obračunskog razdoblja (`cbc:EndDate`) mora biti >= 01.01.1900 i < 01.01.2100 | `cac:InvoicePeriod/cbc:EndDate` |
| **BR-CO-03** | EN16931 | BT-7 / Datum nastanka obveze PDV-a (`cbc:TaxPointDate`) i BT-8 / Kod datuma PDV obveze (`cbc:DescriptionCode`) su međusobno isključivi | `cbc:TaxPointDate` vs `cac:InvoicePeriod/cbc:DescriptionCode` |

---

## 8. Zakonski temelj

| Propis | Članak | Relevantnost | Službeni izvor |
|--------|--------|-------------|----------------|
| **Zakon o PDV-u** | Čl. 30, st. 1 | "Oporezivi događaj i obveza obračuna PDV-a nastaju kada su dobra isporučena ili usluge obavljene." | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2013_06_73_1451.html" target="_blank">NN 73/13</a> |
| **Zakon o PDV-u** | Čl. 30, st. 2 | Za kontinuirane isporuke, smatra se da su isporučeni po isteku razdoblja na koje se računi odnose | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2013_06_73_1451.html" target="_blank">NN 73/13</a> |
| **Zakon o PDV-u** | Čl. 30, st. 5 | "Za primljene predujmove obveza obračuna PDV-a nastaje u trenutku primitka predujma." | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2013_06_73_1451.html" target="_blank">NN 73/13</a> |
| **Zakon o PDV-u** | Čl. 125.i | Obračun prema naplaćenoj naknadi — obveza obračuna PDV-a u trenutku primitka plaćanja | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2013_06_73_1451.html" target="_blank">NN 73/13</a> |
| **Zakon o fiskalizaciji** | Čl. 48, st. 1, t. 7 | eRačun mora sadržavati "datum isporuke dobara ili obavljenih usluga... ako se razlikuje od datuma izdavanja" | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2025_06_89_1233.html" target="_blank">NN 89/25</a> |
| **EN16931** | BR-CO-03 | BT-7 i BT-8 su međusobno isključivi | <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">GitHub</a> |
| **HR CIUS 2025** | HR-BR-2 | IssueTime obavezan u formatu hh:mm:ss | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/196" target="_blank">Specifikacija</a> |
| **HR CIUS 2025** | HR-BR-40 | IssueDate >= 01.01.2026 | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/196" target="_blank">Specifikacija</a> |
| **HR CIUS 2025** | HR-BR-48 | TaxPointDate >= 01.01.1900 i < 01.01.2100 | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/197" target="_blank">Validator</a> |

> **PU pojašnjenje (19.12.2025., pitanje 101/104)**: Zakon o fiskalizaciji odnosi se na eRačune **izdane** od 1.1.2026. — ključan je BT-2 (datum izdavanja), ne datum obavljene usluge.

> **PU pojašnjenje (19.12.2025., pitanje 155/157)**: Predujmovi iz 2025. se ne izdaju niti fiskaliziraju kao eRačun. Ni konačan račun koji se izdaje u 2026. za takav predujam ne podliježe Fiskalizaciji 2.0.

> **PU pojašnjenje (19.12.2025., pitanje 188)**: eIzvještavanje zamjenjuje OPZ-STAT-1 obrazac. Svi obveznici izdavanja i primanja eRačuna obvezni su provoditi eIzvještavanje, neovisno koriste li informacijskog posrednika ili mikroeRačun.

> **PU pojašnjenje (19.12.2025., pitanje 92)**: Fiskalizacija 1.0 (čl. 39 ZOF, gotovinski B2B do 700 EUR) i Fiskalizacija 2.0 (eRačun) su **međusobno isključivi** za isti račun — ne može se koristiti oboje.

> **Pročišćeni tekstovi zakona** (neslužbeni, ali lakši za čitanje):
> <a href="https://www.zakon.hr/z/1455/zakon-o-porezu-na-dodanu-vrijednost" target="_blank">Zakon o PDV-u — zakon.hr</a> ·
> <a href="https://www.zakon.hr/z/3960/zakon-o-fiskalizaciji" target="_blank">Zakon o fiskalizaciji — zakon.hr</a>

---

*Svi izvori navedeni u sekciji [8. Zakonski temelj](#8-zakonski-temelj).*
