---
layout: default
title: "Indikator kopije"
has_toc: true
nav_order: 9
---

# Indikator kopije (CopyIndicator)

Ova stranica pokriva element `CopyIndicator` u eRacunu i `indikatorKopije` u fiskalizacijskoj/eIzvjestavajucoj poruci: sto znaci, kada se smije koristiti, koja polja se ne smiju mijenjati u kopiji, te kako se kopija tretira u fiskalizaciji i eIzvjestavanju.

### Sadrzaj
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE sluzbena uputa</strong><br>
Sve sto je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. <strong>Nijedan zakljucak nema sluzbenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadrzaj treba tretirati iskljucivo kao polaznu tocku za diskusiju, ne kao uputu za implementaciju.
</div>

---

## 1. Sto je indikator kopije?

`CopyIndicator` je UBL 2.1 element koji oznacava radi li se o **kopiji** dokumenta (`true`) ili **originalu** (`false` / odsutan).

| Svojstvo | Vrijednost |
|----------|-----------|
| **UBL element** | `cbc:CopyIndicator` |
| **XML putanja (Invoice)** | `/Invoice/cbc:CopyIndicator` |
| **XML putanja (CreditNote)** | `/CreditNote/cbc:CopyIndicator` |
| **Tip podatka** | `boolean` (`true` / `false`) |
| **Kardinalnost u UBL XSD** | 0..1 (opcionalan) |
| **Pozicija u XML-u** | Odmah nakon `cbc:ID`, prije `cbc:UUID` |
| **Fiskalizacijski element** | `indikatorKopije` (obavezan, `xsd:boolean`) |
| **eIzvjestavanje element** | `indikatorKopije` (obavezan, `xsd:boolean`) |

**Vazna razlika EU vs. HR**: U EU normi EN16931, `CopyIndicator` se **ne koristi** — EU validator izdaje upozorenje `UBL-CR-004` ("A UBL invoice should not include the CopyIndicator"). Medutim, Hrvatska je kroz fiskalizacijsku shemu (`eFiskalizacijaSchema.xsd`) i shemu eIzvjestavanja uvela `indikatorKopije` kao **obavezan element** u SOAP poruci prema Poreznoj upravi. To znaci da je za svaku fiskalizaciju potrebno poslati `indikatorKopije` — u vecini slucajeva s vrijednoscu `false`.

```xml
<!-- UBL eRacun — samo ako je kopija -->
<cbc:ID>2026-001-00042</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<cbc:IssueTime>14:30:00</cbc:IssueTime>
```

```xml
<!-- Fiskalizacijska SOAP poruka — uvijek prisutan -->
<indikatorKopije>false</indikatorKopije>
<!-- ili za kopiju: -->
<indikatorKopije>true</indikatorKopije>
```

### Gdje zivi indikatorKopije u fiskalizacijskoj shemi

Element `indikatorKopije` je dio `ERacun` kompleksnog tipa unutar `EvidentirajERacunZahtjev` SOAP poruke. Definicija iz `eFiskalizacijaSchema.xsd`:

```xml
<xsd:element name="indikatorKopije" type="xsd:boolean">
    <xsd:annotation>
        <xsd:documentation>Indikator kopije racuna koji pokazuje radi li
        se o kopiji racuna (true) ili ne (false).</xsd:documentation>
    </xsd:annotation>
</xsd:element>
```

Isti element postoji i u `eIzvjestavanjeSchema.xsd` unutar strukture za eIzvjestavanje o naplacenim racunima.

---

## 2. Kada se smije koristiti indikator kopije?
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumacenje koje jos nije sluzbeno potvrdeno od Porezne uprave. Sadrzaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Ceka potvrdu</span></div>

Kopija se smije koristiti **iskljucivo** kada se **isti racun** salje ponovo — npr. jer ga je kupac izgubio, doslo je do greske u prijenosu, ili je kupac zatrazio ponovni primitak. Kopija znaci: "ovo je isti dokument koji ste vec primili, bez ikakve izmjene".

**Legitimni razlozi za kopiju:**
- Kupac nije zaprimio original (greska u sustavu posrednika)
- Kupcev sustav je izgubio/ostecen i trazi ponovni primitak
- Tehnicki problem u prijenosu — posrednik potvrdjuje da original nije isporucen

**Sto kopija NIJE:**
- Ispravljeni racun s promijenjenim iznosom, datumom ili PDV-om — to je **korekcija** (CreditNote 381 + novi Invoice 380)
- Racun s promijenjenim brojem dokumenta — to je **novi racun**, ne kopija
- Racun poslan drugom kupcu — to je **novi racun**

### Osnovno pravilo

> **Kopija MORA biti identicna originalu.** Ako se bilo koje polje koje utjece na PDV razlikuje od originala, radi se o korekciji ili novom racunu — ne o kopiji.

---

## 3. Koja polja utjecu na PDV? (ne smiju se mijenjati u kopiji)
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumacenje koje jos nije sluzbeno potvrdeno od Porezne uprave. Sadrzaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Ceka potvrdu</span></div>

Sljedeca tablica klasificira polja po utjecaju na PDV. Polja oznacena s **DA** se nikada ne smiju razlikovati u kopiji od originala — promjena tih polja znaci da dokument **nije kopija**.

| BT | Polje | XML element | Utjece na PDV? | Ako se promijeni = |
|---|---|---|---|---|
| **BT-1** | Broj racuna | `cbc:ID` | **MORA biti isti** | Nije kopija — novi dokument |
| **BT-2** | Datum izdavanja | `cbc:IssueDate` | **DA** | Nova fiskalizacija, novi PDV period |
| **BT-7** | Datum nastanka obveze PDV-a | `cbc:TaxPointDate` | **DA** | Mijenja datum porezne obveze |
| **BT-8** | Kod datuma PDV obveze | `cac:InvoicePeriod/cbc:DescriptionCode` | **DA** | Mijenja mehanizam datuma |
| **BT-9** | Datum dospijeca | `cbc:DueDate` | NE (ali utjece na eIzvjestavanje) | Moguca kopija* |
| **BT-72** | Datum isporuke | `cac:Delivery/cbc:ActualDeliveryDate` | **DA** (rashod/prihod) | Nova fiskalizacija |
| **BT-106** | Ukupan iznos stavki | `cbc:LineExtensionAmount` | **DA** | Korekcija, ne kopija |
| **BT-109** | Ukupan iznos bez PDV-a | `cbc:TaxExclusiveAmount` | **DA** | Korekcija, ne kopija |
| **BT-110** | Ukupan iznos PDV-a | `cbc:TaxAmount` | **DA** | Korekcija, ne kopija |
| **BT-112** | Ukupan iznos s PDV-om | `cbc:TaxInclusiveAmount` | **DA** | Korekcija, ne kopija |
| **BT-115** | Iznos za uplatu | `cbc:PayableAmount` | **DA** | Korekcija, ne kopija |
| **BT-116** | PDV kategorija | `cac:TaxSubtotal/.../cbc:ID` | **DA** | Korekcija, ne kopija |
| **BT-118** | Osnovica poreza | `cbc:TaxableAmount` | **DA** | Korekcija, ne kopija |
| **BT-119** | Iznos poreza kategorije | `cac:TaxSubtotal/cbc:TaxAmount` | **DA** | Korekcija, ne kopija |
| **HR-BT-15** | Obracun po naplacenom | `hrextac:HRObracunPDVPoNaplati` | **DA** | Mijenja PDV rezim |
| **BT-25** | Referenca preth. racuna | `cac:BillingReference/.../cbc:ID` | NE | Moguca kopija* |
| **BT-26** | Datum preth. racuna | `cac:BillingReference/.../cbc:IssueDate` | NE | Moguca kopija* |

\* Polja oznacena "Moguca kopija" ne utjecu izravno na PDV, ali je upitno zasto bi se razlikovala od originala. Promjena bilo kojeg polja tehnickih dovodi u pitanje je li dokument zaista kopija ili nova verzija.

> **Preporuka**: Kopija bi trebala biti **bitovno identicna** originalu, s jedinom razlikom da sadrzi `<cbc:CopyIndicator>true</cbc:CopyIndicator>`. Svaka druga promjena otvara pitanja o integritetu dokumenta.

---

## 4. Fiskalizacija kopije
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumacenje koje jos nije sluzbeno potvrdeno od Porezne uprave. Sadrzaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Ceka potvrdu</span></div>

### 4.1 Fiskalizira li se kopija ponovo?

**Da** — kopija se salje Poreznoj upravi kroz isti `EvidentirajERacunZahtjev` SOAP servis, ali s `indikatorKopije` postavljenim na `true`. Porezna uprava time zna da je rijec o ponovnom slanju istog racuna, a ne o novom racunu.

Iz sheme `eFiskalizacijaSchema.xsd`, element `indikatorKopije` je **obavezan** (`xsd:boolean` bez `minOccurs="0"`), sto znaci da se za svaku fiskalizaciju — i original i kopiju — mora eksplicitno navesti je li rijec o kopiji ili ne:

| Slucaj | `indikatorKopije` | Sto PU sustav ocekuje |
|--------|-------------------|----------------------|
| Original (prvi put) | `false` | Evidentiraj novi racun |
| Kopija (ponovo) | `true` | Evidentiraj kao kopiju postojeceg racuna |

### 4.2 Sto sustav PU radi s kopijom?

Ovo je **otvoreno pitanje** na koje trenutno nemamo sluzbeni odgovor:

- Da li PU sustav provjerava postoji li vec evidentirani racun s istim brojem dokumenta (BT-1)?
- Da li PU sustav usporeduje sadrzaj kopije s originalom?
- Da li kopija generira novi QR kod / UUID ili koristi isti kao original?
- Da li kopija ulazi u porezne evidencije ponovo ili se samo biljezi kao "ponovo poslan"?

### 4.3 Primjenjuje li se eIzvjestavanje na kopije?

Element `indikatorKopije` postoji i u `eIzvjestavanjeSchema.xsd`, sto sugerira da se i eIzvjestavanje o naplati salje s oznakom kopije. Logicno bi bilo da Porezna uprava **ne broji kopiju kao novu naplatu** — ali sluzbena potvrda ne postoji.

---

## 5. Primjeri
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumacenje koje jos nije sluzbeno potvrdeno od Porezne uprave. Sadrzaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Ceka potvrdu</span></div>

### 5.1 Legitimna kopija

**Situacija**: Kupac javlja da njegov sustav nije zaprimio eRacun 2026-001-00042 zbog tehnickog problema kod posrednika. Trazi ponovni primitak.

**Ispravno**: Izdavatelj ponovo salje **identican XML**, ali dodaje `CopyIndicator`:

```xml
<cbc:ID>2026-001-00042</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<cbc:IssueTime>14:30:00</cbc:IssueTime>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
<!-- ... svi ostali elementi IDENTIČNI originalu ... -->
```

Fiskalizacijska poruka:
```xml
<indikatorKopije>true</indikatorKopije>
```

Rezultat: Kupac prima isti racun, sustav prepoznaje da je kopija, ne knjizi duplicirani troskak.

---

### 5.2 Nedopustena "kopija" — zapravo korekcija

**Situacija**: Izdavatelj primijeti da je na racunu 2026-001-00042 krivi iznos (10.000 EUR umjesto 8.000 EUR). Pokusava ponovo poslati "ispravljeni" racun s `CopyIndicator=true`.

**KRIVO**:
```xml
<cbc:ID>2026-001-00042</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<!-- ... -->
<cbc:PayableAmount currencyID="EUR">8000.00</cbc:PayableAmount>
<!-- ^^^ Razlicito od originala (bio 10000.00) — OVO NIJE KOPIJA! -->
```

**ISPRAVNO**: Izdavatelj mora izdati CreditNote (381) za pogresni racun i novi Invoice (380) s tocnim iznosom:

1. **CreditNote 381** — stornira original:
```xml
<cbc:ID>2026-001-00043</cbc:ID>
<cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>
<!-- Referenca na pogresni racun -->
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>2026-001-00042</cbc:ID>
    <cbc:IssueDate>2026-03-15</cbc:IssueDate>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

2. **Novi Invoice 380** — s tocnim iznosom:
```xml
<cbc:ID>2026-001-00044</cbc:ID>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
<cbc:PayableAmount currencyID="EUR">8000.00</cbc:PayableAmount>
```

---

### 5.3 Promjena nePDV polja — siva zona

**Situacija**: Izdavatelj primijeti tipfelera u adresi kupca (npr. "Ilica 1" umjesto "Ilica 10"). Zeli ponovo poslati racun s ispravkom i `CopyIndicator=true`.

**Problem**: Adresa kupca ne utjece na PDV iznose, ali dokument **nije identican** originalu. Je li to kopija?

| Pristup | Argument za | Argument protiv |
|---------|-------------|-----------------|
| **DA, kopija** | Adresa ne utjece na PDV, iznosi su isti, BT-1 je isti | Dokument nije identican — integritet je narusen |
| **NE, novi racun** | Svaka promjena znaci da to nije isti dokument | Pretjerano strogo za tipfeler u adresi |

> **Preporuka**: Iz opreza tretirajte svaku promjenu kao novi racun (CreditNote + novi Invoice), osim ako Porezna uprava eksplicitno potvrdi da su promjene nePDV polja dopustene u kopiji. Razlog: ako sustav PU usporeduje sadrzaj kopije s originalom, razlicita adresa moze prouzrociti odbijanje.

---

## 6. Validator prijedlozi za kopiju
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumacenje koje jos nije sluzbeno potvrdeno od Porezne uprave. Sadrzaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Ceka potvrdu</span></div>

### Postojeca validacija

Trenutno niti HR CIUS Schematron (`HR-CIUS-EXT-EN16931-UBL.sch`) niti EU EN16931 Schematron nemaju **fatal** pravila za `CopyIndicator`. Jedino sto postoji:

| Pravilo | Izvor | Tip | Sto radi |
|---------|-------|-----|----------|
| **UBL-CR-004** | EN16931 | `warning` | "A UBL invoice should not include the CopyIndicator" |

Ovo EU upozorenje postoji jer EN16931 ne koristi `CopyIndicator` u svom modelu podataka. Medutim, Hrvatska ga koristi kroz fiskalizacijsku shemu, pa ovo upozorenje treba tumaciti u HR kontekstu kao informativno, ne kao zabranu.

### Prijedlog novog pravila

| ID | Pravilo | Tip | Obrazlozenje |
|----|---------|-----|--------------|
| **HR-BR-GECI-W11** | Ako `CopyIndicator=true`, izdaj upozorenje: "Racun je oznacen kao kopija — provjerite da je identican originalu" | `warning` | Kopija je neuobicajena situacija. Upozorenje podsijeca posrednika i primatelja da provjere je li dokument zaista identican originalu ili se radi o nedopustenoj promjeni s oznakom kopije. |

**Schematron primjer**:
```xml
<assert test="not(cbc:CopyIndicator = 'true')"
  flag="warning"
  id="HR-BR-GECI-W11">
  [HR-BR-GECI-W11] - Racun je oznacen kao kopija (CopyIndicator=true).
  Kopija mora biti identicna originalu — provjerite da se nijedan
  iznos, datum ni PDV podatak ne razlikuje od prvog slanja.
</assert>
```

---

## 7. Otvorena pitanja

Sljedeca pitanja zahtijevaju sluzbenu potvrdu Porezne uprave:

1. **Usporedba sadrzaja**: Da li PU sustav usporeduje sadrzaj kopije s originalom, ili samo biljezi da je kopija poslana?
2. **QR kod / UUID**: Generira li kopija novi QR kod ili mora koristiti isti UUID kao original?
3. **Granica kopije**: Smiju li se u kopiji mijenjati polja koja ne utjecu na PDV (adresa, napomena, referenca na narudzbu)?
4. **Vremensko ogranicenje**: Postoji li rok do kojeg se kopija moze poslati nakon originala?
5. **eIzvjestavanje kopije**: Ako se kopija salje s `indikatorKopije=true` u eIzvjestavanju, broji li se kao nova naplata ili se ignorira?
6. **Visestruke kopije**: Moze li se isti racun kopirati vise puta (npr. kupac trazi ponovni primitak tri puta)?
7. **Posrednik i kopija**: Tko inicira kopiju — izdavatelj, primatelj ili posrednik? Da li posrednik moze autonomno ponovo poslati eRacun bez izdavateljeve suglasnosti?

---

## Povezane stranice

| Stranica | Relevantnost |
|----------|-------------|
| [Pravila i mehanizmi](pravila) | BT polja koja utjecu na PDV — osnova za procjenu sto se smije mijenjati u kopiji |
| [Primjeri — izdavatelj](primjeri-izdavatelj) | Scenariji izdavanja eRacuna — svaki se moze pojaviti i kao kopija |
| [Prijedlozi za validator](prijedlozi-validator) | Sva predlozena pravila za HR CIUS validator, ukljucujuci HR-BR-GECI-W11 |
| [Referenca](referenca) | XML struktura, pozicija CopyIndicator elementa u dokumentu |
