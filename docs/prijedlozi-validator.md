---
layout: default
title: "Prijedlozi za validator"
nav_order: 6
has_toc: true
---

# Prijedlozi za proširenje HR CIUS validatora

> **Ovo je inicijalni prijedlog** temeljen na primjerima iz dokumentacije o datumima i poreznoj obvezi.
> S više razrade i rasprave zajednice, vjerojatno bi se identificirale i dodatne provjere
> koje bi validator mogao uhvatiti već na ulazu/izlazu kod informacijskog posrednika.
>
> Cilj je pokrenuti raspravu — ne tvrdimo da su svi prijedlozi ispravni ili izvedivi.
> Komentari, ispravke i dodatni prijedlozi su dobrodošli kroz
> <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions" target="_blank">Discussions</a>.

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## Zašto proširiti validator?

Trenutni HR CIUS Schematron validator (`HR-CIUS-EXT-EN16931-UBL.sch`) provjerava datumska polja samo na razini **raspona** (datum >= 1900, < 2100) i **međusobne isključivosti** (BR-CO-03: BT-7 i BT-8 ne smiju koegzistirati).

Ali ne provjerava **logičku konzistentnost** između polja. To znači da XML koji prolazi validator može sadržavati kombinacije koje su:
- **Zakonski neispravne** — PDV u krivom mjesecu
- **Funkcionalno nekonzistentne** — nedostaje obavezan element za način obračuna
- **Vjerojatno greška programera** — neuobičajena kombinacija koju nitko ne bi namjerno napravio

Ako bi se ove provjere ugradile u validator, greške bi se hvatale **već na razini posrednika** — prije nego što nekonzistentan eRačun dođe do primatelja koji ga pokušava automatski učitati.

## Što validator danas provjerava (datumi)

| Pravilo | Što radi | Tip |
|---------|----------|-----|
| **HR-BR-2** | IssueTime mora postojati u formatu hh:mm:ss | Obaveznost + format |
| **HR-BR-40** | IssueDate >= 01.01.2026 i < 01.01.2100 | Raspon datuma |
| **HR-BR-41** | DueDate >= 01.01.1900 i < 01.01.2100 | Raspon datuma |
| **HR-BR-44** | ActualDeliveryDate >= 01.01.1900 i < 01.01.2100 | Raspon datuma |
| **HR-BR-48** | TaxPointDate >= 01.01.1900 i < 01.01.2100 | Raspon datuma |
| **HR-BR-49/50** | InvoicePeriod datumi >= 01.01.1900 i < 01.01.2100 | Raspon datuma |
| **BR-CO-03** | BT-7 i BT-8 su međusobno isključivi | Logička konzistentnost |

Sva pravila su `flag="fatal"` — XML koji ih ne zadovolji se odbija.

---

## Prijedlog 1: Ako BT-8=432, zahtijevaj HR-BT-15

**Što**: Ako eRačun sadrži `InvoicePeriod/DescriptionCode = 432` (obračun po naplaćenoj naknadi), tada `HRFISK20Data/HRObracunPDVPoNaplati` **mora postojati**.

**Zašto**: BT-8=432 označava da PDV obveza nastaje danom plaćanja (čl. 125.i). Posrednik iz HR-BT-15 generira fiskalizacijsku SOAP poruku za Poreznu upravu. Bez HR-BT-15, fiskalizacijska poruka neće sadržavati oznaku obračuna po naplati.

**Tip pravila**: `flag="fatal"` — jednoznačno, nema edge case-ova.

**Schematron primjer**:
```xml
<assert test="not(cac:InvoicePeriod/cbc:DescriptionCode = '432') or
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
  hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati)"
  flag="fatal"
  id="HR-BR-NEW-01">
  Ako je BT-8 = 432, HR-BT-15 (HRObracunPDVPoNaplati) mora postojati.
</assert>
```

**Dokumentacija**: Vidi primjere [4.2.1–4.2.6](eracun-datumi-poreza-workflow#42-obračun-po-naplaćenoj-naknadi-čl-125i-zakona-o-pdv-u-po-naplati) — svi koriste BT-8=432 i svi imaju HR-BT-15.

---

## Prijedlog 2: Ako HR-BT-15 postoji, BT-7 ne smije postojati (osim predujam)

**Što**: Ako eRačun sadrži `HRObracunPDVPoNaplati` (obveznik po naplati), tada `TaxPointDate` (BT-7) **ne smije postojati** — osim za vrstu dokumenta 386 (predujam).

**Zašto**: Kod obračuna po naplati, datum poreza nije poznat u trenutku izdavanja — ovisi o plaćanju. Stavljanje eksplicitnog BT-7 je kontradiktorno s BT-8=432. Jedina iznimka je predujam (386) jer je kupac već platio.

**Tip pravila**: `flag="fatal"` — jasna logička nekonzistentnost.

**Schematron primjer**:
```xml
<assert test="not(exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
  hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) and
  exists(cbc:TaxPointDate) and
  not(cbc:InvoiceTypeCode = '386'))"
  flag="fatal"
  id="HR-BR-NEW-02">
  Obveznik po naplaćenoj naknadi ne smije imati TaxPointDate (BT-7),
  osim za predujam (vrsta dokumenta 386).
</assert>
```

**Dokumentacija**: Vidi primjer [4.2.4 Predujam](eracun-datumi-poreza-workflow#424-predujam--avansni-račun-po-naplati) — jedini slučaj po naplati s BT-7.

---

## Prijedlog 3: Upozorenje ako InvoicePeriod ima datume ali nema BT-7 ni BT-8

**Što**: Ako eRačun sadrži `InvoicePeriod` sa `StartDate` i/ili `EndDate`, ali nema ni `TaxPointDate` (BT-7) ni `DescriptionCode` (BT-8), izdati **upozorenje**.

**Zašto**: InvoicePeriod datumi su samo informativni — bez BT-7 ili BT-8, PDV se računa po datumu izdavanja (BT-2). Za kontinuirane usluge (čl. 30 st. 2) ovo je vjerojatno greška programera jer PDV završava u mjesecu računa umjesto u mjesecu završetka usluge.

**Tip pravila**: `flag="warning"` — nije nužno greška (InvoicePeriod može biti čisto informativan), ali je neuobičajeno i vrijedi upozoriti.

**Schematron primjer**:
```xml
<assert test="not(exists(cac:InvoicePeriod/cbc:StartDate) and
  not(exists(cbc:TaxPointDate)) and
  not(exists(cac:InvoicePeriod/cbc:DescriptionCode)))"
  flag="warning"
  id="HR-BR-NEW-03">
  InvoicePeriod ima datume ali nema BT-7 ni BT-8.
  PDV se računa po datumu izdavanja — je li to namjerno?
</assert>
```

**Dokumentacija**: Vidi primjer [4.1.5a](eracun-datumi-poreza-workflow#415a-što-ako-izostavimo-bt-7-kod-kontinuirane-usluge-po-izdavanju) — PDV u krivom mjesecu.

---

## Što NE može u validator

Neke provjere su previše kontekstualne i validator ih ne može izvesti jer ne poznaje poslovni kontekst:

| Provjera | Zašto ne može |
|----------|---------------|
| "Ispravan" mjesec za PDV | Validator ne zna poslovni kontekst niti što je "ispravno" za konkretnu transakciju |
| BT-7 mora biti jednak BT-74 za kontinuirane usluge | Validator ne zna da je usluga kontinuirana — InvoicePeriod može biti i informativan |
| Datum isporuke mora biti prije datuma računa | Kod predujma i avansa to nije slučaj — legitimno je |
| Koji BT-8 kod koristiti | Ovisi o odluci obveznika i vrsti transakcije |

Ove provjere moraju raditi **ERP programeri** u svom softveru i **knjigovođe** pri pregledu — validator može uhvatiti samo formalna pravila.

---

## Kako predložiti pravilo

Ako imate ideju za novo validacijsko pravilo:

1. Otvorite <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions/new?category=prijedlozi" target="_blank">Discussion</a> s opisom pravila
2. Navedite: što se provjerava, zašto, koji primjer to ilustrira, da li je fatal ili warning
3. Ako možete, predložite Schematron assert izraz
4. Zajednica komentira i glasa

Kad skupimo dovoljno razrađenih prijedloga s konsenzusom, cilj je proslijediti ih timu Porezne uprave koji održava HR CIUS validator.

---

*Ova stranica je inicijalni prijedlog. S više primjera i rasprave, vjerojatno bi se identificirale dodatne provjere koje bi validator mogao uhvatiti na ulazu/izlazu kod posrednika.*
