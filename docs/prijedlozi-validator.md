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

## Pregled svih prijedloga

### Greške — `fatal` (račun se ODBIJA)

Validator odbija eRačun ako otkrije ovo pravilo. Jednoznačna logička kontradikcija ili nedostajući obavezni podatak.

| ID | Pravilo | Kategorija |
|----|---------|------------|
| **HR-BR-GECI-F01** | Ako BT-8=432, zahtijevaj HR-BT-15 | HR-BT-15 logika |
| **HR-BR-GECI-F02** | Ako HR-BT-15 postoji, BT-7 ne smije postojati (osim predujam 386) | HR-BT-15 logika |
| **HR-BR-GECI-F03** | HR-BT-15 postoji i BT-8 postoji ali NIJE 432 — kontradikcija | HR-BT-15 logika |
| **HR-BR-GECI-F04** | Ako BT-8=35, BT-72 (datum isporuke) mora postojati | Datumska logika |
| **HR-BR-GECI-F05** | BT-73 (StartDate) mora biti <= BT-74 (EndDate) | Datumska logika |
| **HR-BR-GECI-F06** | Vrijeme izdavanja (HR-BT-2) mora biti validno (sati 0-23, minute 0-59, sekunde 0-59) | Validacija formata |
| **HR-BR-GECI-F07** | BT-8 (DescriptionCode) smije biti samo 3, 35 ili 432 | Dozvoljeni kodovi |
| **HR-BR-GECI-F08** | Predujam (386) s HR-BT-15 mora imati BT-7 (datum plaćanja poznat) | HR-BT-15 logika |

### Upozorenja — `warning` (račun PROLAZI ali je sumnjiv)

Validator propušta eRačun ali izdaje upozorenje. Moguća programerska greška ili neuobičajena kombinacija koja zahtijeva provjeru.

| ID | Pravilo | Kategorija |
|----|---------|------------|
| **HR-BR-GECI-W01** | InvoicePeriod ima datume ali nema BT-7 ni BT-8 — PDV možda u krivom mjesecu | Datumska logika |
| **HR-BR-GECI-W02** | HR-BT-15 postoji bez BT-7 i bez BT-8=432 (osim CreditNote) — namjerno? | HR-BT-15 logika |
| **HR-BR-GECI-W03** | Datum dospijeća (BT-9) je prije datuma izdavanja (BT-2) — je li to namjerno? | Datumska logika |
| **HR-BR-GECI-W04** | Datum poreza (BT-7) je izvan obračunskog razdoblja (BT-73/BT-74) | Datumska logika |
| **HR-BR-GECI-W05** | Sadržaj HR-BT-15 nije standardni tekst "Obračun prema naplaćenoj naknadi" | HR-BT-15 logika |
| **HR-BR-GECI-W06** | Predujam (386) ima datum isporuke (BT-72) — isporuka još nije obavljena? | Poslovni kontekst |
| **HR-BR-GECI-W07** | Predujam (386) s HR-BT-15 koristi BT-8=432 umjesto BT-7 — datum plaćanja je poznat | HR-BT-15 logika |
| **HR-BR-GECI-W08** | BT-8=3 je redundantan — isti rezultat kao da nema ni BT-7 ni BT-8 | Datumska logika |

---

## Greške — fatal (račun se ODBIJA)

### F01: Ako BT-8=432, zahtijevaj HR-BT-15

**Što**: Ako eRačun sadrži `InvoicePeriod/DescriptionCode = 432` (obračun po naplaćenoj naknadi), tada `HRFISK20Data/HRObracunPDVPoNaplati` **mora postojati**.

**Zašto**: BT-8=432 označava da PDV obveza nastaje danom plaćanja (čl. 125.i). Posrednik iz HR-BT-15 generira fiskalizacijsku SOAP poruku za Poreznu upravu. Bez HR-BT-15, fiskalizacijska poruka neće sadržavati oznaku obračuna po naplati.

**Tip pravila**: `flag="fatal"` — jednoznačno, nema edge case-ova.

**Schematron primjer**:
```xml
<assert test="not(cac:InvoicePeriod/cbc:DescriptionCode = '432') or
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
  hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati)"
  flag="fatal"
  id="HR-BR-GECI-F01">
  Ako je BT-8 = 432, HR-BT-15 (HRObracunPDVPoNaplati) mora postojati.
</assert>
```

**Dokumentacija**: Vidi primjere [4.2.1–4.2.6](primjeri-izdavatelj#42-obračun-po-naplaćenoj-naknadi-čl-125i-zakona-o-pdv-u-po-naplati) — svi koriste BT-8=432 i svi imaju HR-BT-15.

---

### F02: Ako HR-BT-15 postoji, BT-7 ne smije postojati (osim predujam)

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
  id="HR-BR-GECI-F02">
  Obveznik po naplaćenoj naknadi ne smije imati TaxPointDate (BT-7),
  osim za predujam (vrsta dokumenta 386).
</assert>
```

**Dokumentacija**: Vidi primjer [4.2.4 Predujam](primjeri-izdavatelj#424-predujam--avansni-račun-po-naplati) — jedini slučaj po naplati s BT-7.

---

### F03: HR-BT-15 postoji i BT-8 postoji ali NIJE 432

**Što**: Ako eRačun sadrži `HRObracunPDVPoNaplati` (HR-BT-15), a istovremeno `DescriptionCode` (BT-8) postoji ali **nije** 432, odbiti kao **fatal**.

**Zašto**: BT-8=3 ili BT-8=35 kontradiktira HR-BT-15. Kod 3 znači "datum izdavanja", kod 35 znači "datum isporuke" — oba su nespojiva s obračunom po naplati koji zahtijeva kod 432 ("datum plaćanja"). Ovo je jednoznačna kontradikcija između dva polja u istom dokumentu.

**Tip pravila**: `flag="fatal"` — jednoznačna kontradikcija, nema edge case-ova.

**Schematron primjer**:
```xml
<assert test="not(
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
    hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) and
  exists(cac:InvoicePeriod/cbc:DescriptionCode) and
  not(cac:InvoicePeriod/cbc:DescriptionCode = '432'))"
  flag="fatal"
  id="HR-BR-GECI-F03">
  HR-BT-15 (obračun po naplati) je prisutan, ali BT-8 nije 432.
  BT-8 kod mora biti 432 (datum plaćanja) ili ne smije postojati.
</assert>
```

---

### F04: Ako BT-8=35, BT-72 mora postojati

**Što**: Ako eRačun sadrži `InvoicePeriod/DescriptionCode = 35` (PDV po datumu isporuke), tada `Delivery/ActualDeliveryDate` (BT-72) **mora postojati**.

**Zašto**: BT-8=35 znači "PDV po datumu isporuke" ali bez BT-72 sustav ne zna koji je datum isporuke. Primatelj (i knjigovodstvo) ne može odrediti u koji mjesec pada porezna obveza. Bez BT-72, jedina alternativa je BT-2 (datum izdavanja) — ali tada je BT-8=35 besmislen jer isto postiže i BT-8=3.

**Tip pravila**: `flag="fatal"` — bez BT-72, BT-8=35 je neizvršiv.

**Schematron primjer**:
```xml
<assert test="not(cac:InvoicePeriod/cbc:DescriptionCode = '35') or
  exists(cac:Delivery/cbc:ActualDeliveryDate)"
  flag="fatal"
  id="HR-BR-GECI-F04">
  BT-8 = 35 (datum poreza = datum isporuke), ali BT-72 (ActualDeliveryDate)
  ne postoji. Navedite datum isporuke ili promijenite BT-8 kod.
</assert>
```

---

### F05: BT-73 mora biti <= BT-74

**Što**: Ako obračunsko razdoblje ima oba datuma, početak mora biti prije ili jednak kraju.

**Zašto**: StartDate > EndDate je jednoznačna greška — nemoguće razdoblje.

**Tip pravila**: `flag="fatal"`

**Schematron primjer**:
```xml
<assert test="not(exists(cac:InvoicePeriod/cbc:StartDate) and
  exists(cac:InvoicePeriod/cbc:EndDate)) or
  xs:date(cac:InvoicePeriod/cbc:StartDate) &lt;= xs:date(cac:InvoicePeriod/cbc:EndDate)"
  flag="fatal"
  id="HR-BR-GECI-F05">
  BT-73 (StartDate) mora biti manji ili jednak BT-74 (EndDate).
</assert>
```

---

### F06: Vrijeme izdavanja mora biti validno

**Što**: HR-BR-2 provjerava format `hh:mm:ss` regexom, ali dozvoljava `99:99:99`. Treba provjera raspona.

**Zašto**: `25:61:99` prolazi regex ali nije validno vrijeme.

**Tip pravila**: `flag="fatal"`

**Schematron primjer**:
```xml
<assert test="not(exists(cbc:IssueTime)) or
  (number(substring(cbc:IssueTime,1,2)) >= 0 and
   number(substring(cbc:IssueTime,1,2)) &lt;= 23 and
   number(substring(cbc:IssueTime,4,2)) >= 0 and
   number(substring(cbc:IssueTime,4,2)) &lt;= 59 and
   number(substring(cbc:IssueTime,7,2)) >= 0 and
   number(substring(cbc:IssueTime,7,2)) &lt;= 59)"
  flag="fatal"
  id="HR-BR-GECI-F06">
  Vrijeme izdavanja (HR-BT-2) mora biti validno: sati 00-23, minute 00-59, sekunde 00-59.
</assert>
```

---

### F07: BT-8 dozvoljeni kodovi

**Što**: BT-8 (DescriptionCode) smije biti samo 3, 35 ili 432 prema UNTDID 2005.

**Zašto**: Bilo koji drugi kod (npr. 1, 100, 999) nema definirano značenje za PDV.

**Tip pravila**: `flag="fatal"` — napomena: moguće da EN16931 baza već pokriva; provjeriti prije implementacije.

**Schematron primjer**:
```xml
<assert test="not(exists(cac:InvoicePeriod/cbc:DescriptionCode)) or
  cac:InvoicePeriod/cbc:DescriptionCode = '3' or
  cac:InvoicePeriod/cbc:DescriptionCode = '35' or
  cac:InvoicePeriod/cbc:DescriptionCode = '432'"
  flag="fatal"
  id="HR-BR-GECI-F07">
  BT-8 (DescriptionCode) mora biti 3, 35 ili 432.
</assert>
```

---

### F08: Predujam po naplati mora imati BT-7

**Što**: Predujam (386) s HR-BT-15 mora imati BT-7 jer je datum plaćanja poznat (kupac je već platio).

**Zašto**: Bez BT-7, sustav ne zna datum porezne obveze. BT-8=432 na predujmu je besmislen jer datum plaćanja je poznat.

**Tip pravila**: `flag="fatal"`

**Schematron primjer**:
```xml
<assert test="not(
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
    hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) and
  cbc:InvoiceTypeCode = '386' and
  not(exists(cbc:TaxPointDate)))"
  flag="fatal"
  id="HR-BR-GECI-F08">
  Predujam (386) s obračunom po naplati (HR-BT-15) mora imati
  BT-7 (TaxPointDate) jer je datum plaćanja poznat.
</assert>
```

**Dokumentacija**: Vidi primjer [4.2.4](primjeri-izdavatelj#424-predujam-avansni-račun-po-naplati) — jedini slučaj po naplati s BT-7.

---

## Upozorenja — warning (račun PROLAZI ali je sumnjiv)

### W01: InvoicePeriod ima datume ali nema BT-7 ni BT-8

**Što**: Ako eRačun sadrži `InvoicePeriod` sa `StartDate` i/ili `EndDate`, ali nema ni `TaxPointDate` (BT-7) ni `DescriptionCode` (BT-8), izdati **upozorenje**.

**Zašto**: InvoicePeriod datumi su samo informativni — bez BT-7 ili BT-8, PDV se računa po datumu izdavanja (BT-2). Za kontinuirane usluge (čl. 30 st. 2) ovo je vjerojatno greška programera jer PDV završava u mjesecu računa umjesto u mjesecu završetka usluge.

**Tip pravila**: `flag="warning"` — nije nužno greška (InvoicePeriod može biti čisto informativan), ali je neuobičajeno i vrijedi upozoriti.

**Schematron primjer**:
```xml
<assert test="not(exists(cac:InvoicePeriod/cbc:StartDate) and
  not(exists(cbc:TaxPointDate)) and
  not(exists(cac:InvoicePeriod/cbc:DescriptionCode)))"
  flag="warning"
  id="HR-BR-GECI-W01">
  InvoicePeriod ima datume ali nema BT-7 ni BT-8.
  PDV se računa po datumu izdavanja — je li to namjerno?
</assert>
```

**Dokumentacija**: Vidi primjer [4.1.5a](primjeri-izdavatelj#415a-što-ako-izostavimo-bt-7-kod-kontinuirane-usluge-po-izdavanju) — PDV u krivom mjesecu.

---

### W02: HR-BT-15 postoji bez BT-7 i bez BT-8=432 (osim CreditNote)

**Što**: Ako eRačun sadrži `HRObracunPDVPoNaplati` (HR-BT-15), ali nema ni `TaxPointDate` (BT-7) ni `DescriptionCode = 432` (BT-8), i nije kreditna nota (381), izdati **upozorenje**.

**Zašto**: HR-BT-15 bez mehanizma za datum PDV-a znači da se primjenjuje default BT-2, što kontradiktira obračunu po naplati. Ako je obveznik stavio HR-BT-15, očekuje se da koristi BT-8=432 ili barem BT-7 (kod predujma). Bez ijednog, PDV se računa po datumu izdavanja — što je vjerojatno greška.

**Tip pravila**: `flag="warning"` — nije nužno greška (možda izdavatelj namjerno koristi BT-2), ali je neuobičajeno i vrijedi upozoriti.

**Schematron primjer**:
```xml
<assert test="not(
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
    hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) and
  not(exists(cbc:TaxPointDate)) and
  not(cac:InvoicePeriod/cbc:DescriptionCode = '432') and
  not(cbc:InvoiceTypeCode = '381'))"
  flag="warning"
  id="HR-BR-GECI-W02">
  HR-BT-15 (obračun po naplati) je prisutan, ali nema ni BT-7 ni BT-8=432.
  PDV se računa po datumu izdavanja (BT-2) — je li to namjerno?
</assert>
```

**Dokumentacija**: Vidi [pravila.md sekcija 3.1 tablica scenarija](pravila#31-scenariji-prema-vrsti-transakcije) — pregled kombinacija datumskih polja za razne scenarije.

---

### W03: DueDate prije IssueDate

**Što**: Datum dospijeća (BT-9) je prije datuma izdavanja (BT-2).

**Zašto**: Rok plaćanja prije datuma računa je neuobičajen — vjerojatno greška u datumu.

**Tip pravila**: `flag="warning"` — iznimno rijetko namjerno (npr. ispravak, storno).

**Schematron primjer**:
```xml
<assert test="not(exists(cbc:DueDate)) or
  xs:date(cbc:DueDate) >= xs:date(cbc:IssueDate)"
  flag="warning"
  id="HR-BR-GECI-W03">
  BT-9 (DueDate) je prije BT-2 (IssueDate). Je li to namjerno?
</assert>
```

---

### W04: BT-7 izvan obračunskog razdoblja

**Što**: Datum poreza (BT-7) je izvan raspona obračunskog razdoblja (BT-73/BT-74).

**Zašto**: Po čl. 30 st. 2, za kontinuirane usluge datum poreza = kraj razdoblja. BT-7 izvan razdoblja je sumnjiv.

**Tip pravila**: `flag="warning"` — postoje rubni slučajevi (vidi primjer 4.1.5b).

**Schematron primjer**:
```xml
<assert test="not(exists(cbc:TaxPointDate) and
  exists(cac:InvoicePeriod/cbc:StartDate) and
  exists(cac:InvoicePeriod/cbc:EndDate)) or
  (xs:date(cbc:TaxPointDate) >= xs:date(cac:InvoicePeriod/cbc:StartDate) and
   xs:date(cbc:TaxPointDate) &lt;= xs:date(cac:InvoicePeriod/cbc:EndDate))"
  flag="warning"
  id="HR-BR-GECI-W04">
  BT-7 (TaxPointDate) je izvan obračunskog razdoblja (BT-73 do BT-74).
</assert>
```

---

### W05: HR-BT-15 nestandardni tekst

**Što**: Sadržaj HR-BT-15 nije "Obračun prema naplaćenoj naknadi".

**Zašto**: Specifikacija (Tablica 52) propisuje taj tekst. Drugačiji tekst može zbuniti primatelja ili posrednika.

**Tip pravila**: `flag="warning"` — posrednik možda čita samo prisutnost elementa, ne sadržaj.

**Schematron primjer**:
```xml
<assert test="not(exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
  hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati)) or
  normalize-space(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
  hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) = 'Obračun prema naplaćenoj naknadi'"
  flag="warning"
  id="HR-BR-GECI-W05">
  HR-BT-15 tekst bi trebao biti 'Obračun prema naplaćenoj naknadi'.
</assert>
```

---

### W06: Predujam s datumom isporuke

**Što**: Predujam (386) ima BT-72 (ActualDeliveryDate) — isporuka se još nije dogodila.

**Zašto**: Predujam je uplata prije isporuke. BT-72 na predujmu je neuobičajen.

**Tip pravila**: `flag="warning"`

**Schematron primjer**:
```xml
<assert test="not(cbc:InvoiceTypeCode = '386' and
  exists(cac:Delivery/cbc:ActualDeliveryDate))"
  flag="warning"
  id="HR-BR-GECI-W06">
  Predujam (386) ima datum isporuke (BT-72) — isporuka obično još nije obavljena kod predujma.
</assert>
```

---

### W07: Predujam po naplati s BT-8=432

**Što**: Predujam (386) s HR-BT-15 koristi BT-8=432 umjesto BT-7.

**Zašto**: Kod predujma je kupac već platio — datum plaćanja je poznat. BT-8=432 ("datum plaćanja će se tek odrediti") je besmislen. Treba koristiti BT-7 s konkretnim datumom.

**Tip pravila**: `flag="warning"`

**Schematron primjer**:
```xml
<assert test="not(
  exists(ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/
    hrextac:HRFISK20Data/hrextac:HRObracunPDVPoNaplati) and
  cbc:InvoiceTypeCode = '386' and
  cac:InvoicePeriod/cbc:DescriptionCode = '432')"
  flag="warning"
  id="HR-BR-GECI-W07">
  Predujam (386) po naplati koristi BT-8=432 umjesto BT-7. Datum plaćanja
  je poznat — koristite BT-7 (TaxPointDate) s datumom primitka predujma.
</assert>
```

---

### W08: BT-8=3 je redundantan

**Što**: BT-8=3 znači "datum poreza = datum izdavanja" — isto kao default kad nema ni BT-7 ni BT-8.

**Zašto**: Nepotrebno korištenje BT-8. Nije greška, ali zauzima InvoicePeriod element bez razloga.

**Tip pravila**: `flag="warning"`

**Schematron primjer**:
```xml
<assert test="not(cac:InvoicePeriod/cbc:DescriptionCode = '3')"
  flag="warning"
  id="HR-BR-GECI-W08">
  BT-8=3 je redundantan — isti rezultat kao da nema BT-8.
  Datum poreza = BT-2 (IssueDate) je default ponašanje.
</assert>
```

---

## Što NE može u validator

Neke provjere su previše kontekstualne i validator ih ne može izvesti jer ne poznaje poslovni kontekst:

| Provjera | Zašto ne može |
|----------|---------------|
| "Ispravan" mjesec za PDV | Validator ne zna poslovni kontekst niti što je "ispravno" za konkretnu transakciju |
| BT-7 mora biti jednak BT-74 za kontinuirane usluge | Validator ne zna da je usluga kontinuirana — InvoicePeriod može biti i informativan |
| BT-7 mora biti jednak BT-72 za jednokratne isporuke | Validator ne zna je li isporuka jednokratna; postoje rubni slučajevi |
| Datum isporuke mora biti prije datuma računa | Kod predujma i avansa to nije slučaj — legitimno je (4.1.3) |
| BT-7 ne smije biti u budućnosti | Predujam s datumom uplate u budućnosti je rubno, ali moguće |
| Koji BT-8 kod koristiti (3 vs 35 vs 432) | Ovisi o odluci obveznika i vrsti transakcije |
| CreditNote mora referencirati postojeći račun | Validator nema pristup bazi računa |
| Datum isporuke mora odgovarati stvarnoj dostavi | Validator nema pristup logističkim podacima |

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
