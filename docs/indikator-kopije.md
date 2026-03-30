---
layout: default
title: "Indikator kopije"
has_toc: true
nav_order: 9
---

# Indikator kopije (HR-BT-1) — ispravak nePDV podataka bez storna

Ova stranica pokriva element `CopyIndicator` (HR-BT-1) u eRačunu i `indikatorKopije` u fiskalizacijskoj/eIzvještavajućoj poruci. Suprotno intuitivnom nazivu, **ovo NIJE mehanizam za slanje klasične kopije računa** — to je mehanizam za **ispravak podataka koji ne utječu na obračun poreza**, pod istim brojem računa, bez potrebe za stornom i novim računom.

### Sadržaj
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.
</div>

---

## 1. Što je indikator kopije?
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Članak 43. Zakona o fiskalizaciji (NN 89/25) definira poseban mehanizam:

> *"Kada se ispravlja podatak na eRačunu koji ne utječe na obračun poreza, eRačun se može u istom razdoblju oporezivanja izdati pod istim brojem, uz obvezno navođenje podatka 'indikator kopije računa'."*

Ovo znači da `CopyIndicator` / `indikatorKopije` **nije** mehanizam za ponovno slanje identičnog računa (klasična kopija), nego je **mehanizam za ispravak nePDV podataka pod istim brojem računa** — alternativa postupku storniranja i izdavanja novog računa.

> **Ako kopija nije dopuštena** (promjena PDV podataka, drugo razdoblje), alternativa je storno + novi račun. Storno se može izvršiti na više načina:
> - **CreditNote 381** — financijsko odobrenje/storno (ne zahtijeva KPD, HR-BR-25 izuzetak) — **najčešći postupak**
> - **Korektivni račun 384** — korekcija s referencom na original (zahtijeva KPD!)
> - **Invoice 386 s negativnom količinom** — samo za **storno predujma** (386 = Prepayment invoice, ne generički storno)
>
> **Napomena o materijalnom/robnom storniranju**: CreditNote (381) je **oslobođen KPD klasifikacije** (HR-BR-25) — ali i dalje može sadržavati stavke s količinama u minusu. Ako je bitno da PU vidi i **koje stavke** se vraćaju (ne samo financijski iznos), postoje opcije:
> - **381 sa stavkama** (količina u minusu) — PU vidi artikle, ali bez KPD-a
> - **384 (korektivni račun)** — PU vidi artikle **s KPD-om** jer 384 zahtijeva KPD klasifikaciju
>
> Izbor ovisi o tome treba li PU evidencija sadržavati i robni aspekt storna ili samo financijski.

**Ključne točke:**

- To **NIJE klasična kopija** — Porezna uprava eksplicitno upozorava da se ne smije koristiti u svrhu klasične kopije računa
- To je **ispravak podataka koji ne utječu na obračun poreza** pod istim brojem računa
- To je **opcija, ne obveza** — alternativa je uvijek storno (CreditNote 381) + novi račun (Invoice 380)
- Vrijedi **samo u istom razdoblju oporezivanja** kao original
- Ispravljeni eRačun se mora **odmah fiskalizirati** s `indikatorKopije=true`

| Svojstvo | Vrijednost |
|----------|-----------|
| **HR-BT-1 / UBL element** | `cbc:CopyIndicator` |
| **Putanja Invoice** | `/Invoice/cbc:CopyIndicator` |
| **Putanja CreditNote** | `/CreditNote/cbc:CopyIndicator` |
| **Tip podatka** | `boolean` (`true` / `false`) |
| **Kardinalnost UBL** | 0..1 (opcionalan) |
| **Kardinalnost fiskalizacija** | 1..1 (**obavezan!**) |
| **Zakonski temelj** | Čl. 43 Zakona o fiskalizaciji (NN 89/25) |

> **UPOZORENJE Porezne uprave**: *"Mogućnost uz naznaku 'indikator kopije računa' propisana člankom 43. Zakona o fiskalizaciji NE može se koristiti u svrhu klasične kopije računa."*
>
> Izvor: <a href="https://porezna-uprava.gov.hr/hr/ispravci-eracuna-koji-ne-utjecu-na-obracun-poreza-i-statistika-fiskalizacije-2-0/8349" target="_blank">Porezna uprava — Ispravci eRačuna koji ne utječu na obračun poreza</a>

---

## 2. Što se SMIJE ispraviti kopijom?
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Čl. 43 dopušta ispravak samo **podataka koji ne utječu na obračun poreza**. Umjesto nabrajanja svih polja koja se smiju mijenjati (kojih ima stotine), praktičnije je definirati **što se NE SMIJE mijenjati** — sve ostalo je po logici čl. 43 dopušteno.

### Što se NE SMIJE mijenjati u kopiji

| Podatak | BT polje | Zašto ne |
|---|---|---|
| **Broj računa** | BT-1 | MORA biti isti — to je identifikator kopije |
| **OIB izdavatelja** | BT-31 | Promjena OIB-a = drugi izdavatelj = drugi račun |
| **OIB primatelja** | BT-48 | Promjena OIB-a = drugi kupac = drugi račun |
| **Datum izdavanja** | BT-2 | Utječe na PDV period (default datum), brojčanik |
| **Datum porezne obveze** | BT-7 | Direktno određuje PDV period |
| **Kod datuma PDV-a** | BT-8 | Mijenja mehanizam PDV datuma |
| **Datum isporuke** | BT-72 | Utječe na rashod/prihod (HSFI 15/16) i PDV |
| **Svi iznosi** | BT-106 do BT-119 | Mijenja poreznu osnovicu, PDV iznos |
| **PDV stope i kategorije** | BT-116 do BT-119, BT-151/152 | Direktno utječe na PDV |
| **HR-BT-15** | HRObracunPDVPoNaplati | Mijenja cijeli PDV režim |
| **Artikli, količine, cijene** | BG-25 stavke | Utječu na iznose → utječu na PDV |
| **Vrsta dokumenta** | BT-3 | Drugi tip = drugi dokument |

### Što je upitno (siva zona)
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Podatak | BT polje | Pitanje |
|---|---|---|
| **GLN kupca/prodavatelja** | BT-46/BT-29 | GLN identificira poslovnicu — promjena GLN-a može značiti drugu lokaciju. Utječe li to na PDV? |
| **Adresa kupca/prodavatelja** | BG-5/BG-8 | Ne utječe na PDV iznos, ali ako se OIB ne mijenja — je li to dopušteno? |
| **Datum dospijeća** | BT-9 | PU navodi "promjena podataka o plaćanju" kao dopuštenu (<a href="https://porezna-uprava.gov.hr/hr/ispravci-eracuna-koji-ne-utjecu-na-obracun-poreza-i-statistika-fiskalizacije-2-0/8349" target="_blank">izvor</a>) — ali BT-9 utječe na eIzvještavanje o naplati |
| **Naziv artikla/opis** | BT-153/BT-154 | Ne utječe na iznos ni PDV — ali mijenja li to identitet stavke? |
| **Barkod artikla** | BT-157 | Čisti identifikator, ne utječe na PDV — ali PU nije potvrdila |
| **VATEX kod** | BT-121 | VATEX određuje razlog oslobođenja od PDV-a (npr. reverse charge vs izvan opsega) — **direktno utječe na PDV tretman**. Neki proizvođači softvera navode da se smije ispraviti kopijom, ali PU to **nije eksplicitno potvrdila**. Smatramo da bi trebao biti u "NE SMIJE" kategoriji. |

> **Naše tumačenje**: Sve što **ne mijenja iznos, stopu, kategoriju PDV-a, niti identitet stranaka (OIB)** bi trebalo biti dopušteno za kopiju. Ali za siva zona polja — čekamo službenu potvrdu PU.

> **PU navodi kao primjere dopuštenih ispravaka**: "referenciranje na dokument, promjena podataka o plaćanju, operatera i slično" (izvor: <a href="https://porezna-uprava.gov.hr/hr/ispravci-eracuna-koji-ne-utjecu-na-obracun-poreza-i-statistika-fiskalizacije-2-0/8349" target="_blank">porezna-uprava.gov.hr</a>).

---

## 3. Uvjeti za korištenje kopije
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Sva **četiri** uvjeta moraju biti **istovremeno** ispunjena:

| # | Uvjet | Obrazloženje |
|---|-------|-------------|
| 1 | Originalni eRačun **mora biti fiskaliziran** | Bez fiskaliziranog originala u PU sustavu, kopija nema smisla — greška S012 |
| 2 | Ispravak se odnosi **SAMO** na podatke koji ne utječu na obračun poreza | Čl. 43 — eksplicitna zakonska odredba |
| 3 | Kopija se izdaje u **ISTOM razdoblju oporezivanja** kao original | Čl. 43 — isti obračunski period |
| 4 | Broj računa (BT-1) **MORA biti identičan** originalu | Logika kopije — isti dokument, ispravljen |

Ako **bilo koji** uvjet nije zadovoljen → storno (CreditNote 381) + novi račun (Invoice 380).

---

## 4. Fiskalizacija kopije
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Element `indikatorKopije` je **obavezan** u fiskalizacijskoj SOAP poruci (`EvidentirajERacunZahtjev`). Za svaku fiskalizaciju — i original i kopiju — mora se eksplicitno navesti vrijednost:

| Slučaj | `indikatorKopije` | Što PU sustav očekuje |
|--------|-------------------|----------------------|
| Original (prvi put) | `false` | Evidentiraj novi račun |
| Ispravak nePDV podataka (kopija) | `true` | Evidentiraj kao ispravak postojećeg računa |

### 4.1 Ponašanje PU sustava

- PU sustav **provjerava** da originalni račun **postoji** u evidenciji prema identifikatoru eRačuna i vrsti (ulazni/izlazni)
- Ako original ne postoji → greška **S012** ("Ne postoji evidentiran originalni eRačun")
- Ako se šalje račun s istim identifikatorom BEZ `indikatorKopije=true` → greška **S008** ("Već postoji fiskaliziran eRačun s istim identifikatorom")
- `CopyIndicator=true` signalizira PU sustavu da je to **namjerni ispravak** istog računa, ne duplikat greškom

> **Otvoreno pitanje — kompozitni ključ identifikatora**: Specifikacija navodi da se provjera jedinstvenosti provodi pomoću "identifikatora i vrste eRačuna", ali ne definira precizno od kojih polja se identifikator sastoji. Nejasno je:
> - Je li to **BT-1 (broj)** sam, ili **BT-1 + BT-2 (datum izdavanja) + OIB izdavatelja**?
> - Mora li BT-2 u kopiji biti **isti kao u originalu** (datum prvog izdavanja) ili **datum ponovnog slanja**?
> - Što je s HR-BT-2 (IssueTime) — ako je BT-2 isti ali vrijeme različito?
> - Ako se BT-2 mijenja u kopiji, to je formalno **novi identifikator** — PU sustav bi ga tretirao kao novi račun, ne kopiju
> - Zakon kaže "u istom razdoblju oporezivanja" — ali ne kaže "s istim datumom izdavanja"
>
> Bez službenog odgovora, preporučamo: **BT-2 u kopiji isti kao u originalu** (datum prvog izdavanja), samo HR-BT-2 (vrijeme) može biti novo. To osigurava da PU sustav prepozna istu transakciju.

> **Napomena o validaciji**: Schematron validator **ne može** provjeriti je li kopija legitimna jer vidi samo jedan dokument. **Posrednik** ima pristup oba dokumenta i mogao bi uspoređivati PDV-relevantna polja — ali ni to nije jednostavno jer ovisi o definiciji kompozitnog ključa.

### 4.2 Gdje postoji indikatorKopije

| Poruka | Element | Obavezan? |
|--------|---------|-----------|
| **eFiskalizacija** (`EvidentirajERacunZahtjev`) | `indikatorKopije` | **DA** (1..1) |
| **eIzvještavanje** (`EvidentirajIsporukuZaKojuNijeIzdanERacun`) | `indikatorKopije` | **DA** (1..1) |
| **EvidentirajNaplatu** | — | **NEMA** |
| **EvidentirajOdbijanje** | — | **NEMA** |

```xml
<!-- Fiskalizacijska SOAP poruka — original -->
<indikatorKopije>false</indikatorKopije>

<!-- Fiskalizacijska SOAP poruka — ispravak nePDV podataka -->
<indikatorKopije>true</indikatorKopije>
```

```xml
<!-- UBL eRačun — ispravak nePDV podataka -->
<cbc:ID>42/P1/2</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
```

---

## 5. Primjeri
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

### 5.1 Legitimna kopija — ispravak reference na narudžbu

**Situacija**: Izdavatelj je poslao eRačun 42/P1/2 s krivim brojem narudžbenice u BT-13 (napisao "NAR-100" umjesto "NAR-200"). Iznosi su ispravni, PDV je ispravan, isti mjesec.

**Ispravno**: Izdavatelj šalje isti račun s istim brojem, `CopyIndicator=true`, i ispravljenim BT-13:

```xml
<cbc:ID>42/P1/2</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
<!-- ... -->
<cac:OrderReference>
  <cbc:ID>NAR-200</cbc:ID>  <!-- ISPRAVLJENO (bilo NAR-100) -->
</cac:OrderReference>
<!-- ... svi iznosi i PDV identični originalu ... -->
```

Fiskalizacija: `<indikatorKopije>true</indikatorKopije>`

**Rezultat**: Kupac prima ispravljeni račun s točnom referencom. Iznosi i PDV nepromijenjeni.

---

### 5.2 Legitimna kopija — ispravak IBAN-a

**Situacija**: Na računu 42/P1/2 naveden je krivi IBAN primatelja uplate. Kupac ne može platiti. Isti mjesec.

**Ispravno**: `CopyIndicator=true`, ispravljeni IBAN u BG-16 (podaci o plaćanju), sve ostalo identično.

```xml
<cbc:ID>42/P1/2</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<!-- ... -->
<cac:PaymentMeans>
  <cac:PayeeFinancialAccount>
    <cbc:ID>HR1234567890123456789</cbc:ID>  <!-- ISPRAVLJENI IBAN -->
  </cac:PayeeFinancialAccount>
</cac:PaymentMeans>
```

Fiskalizacija: `<indikatorKopije>true</indikatorKopije>`

---

### 5.3 NEDOPUŠTENA kopija — promjena iznosa

**Situacija**: Izdavatelj je na računu 42/P1/2 naveo krivi iznos (10.000 EUR umjesto 8.000 EUR). Pokušava poslati "kopiju" s ispravljenim iznosom.

**KRIVO** — iznosi utječu na obračun poreza:
```xml
<cbc:ID>42/P1/2</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<cbc:PayableAmount currencyID="EUR">8000.00</cbc:PayableAmount>
<!-- ^^^ NEDOPUŠTENO! Promjena iznosa = utječe na PDV -->
```

**ISPRAVNO** — storno + novi račun:

1. **CreditNote 381** — stornira pogrešni original:
```xml
<cbc:ID>43/P1/2</cbc:ID>
<cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>42/P1/2</cbc:ID>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

2. **Novi Invoice 380** — s točnim iznosom:
```xml
<cbc:ID>44/P1/2</cbc:ID>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
<cbc:PayableAmount currencyID="EUR">8000.00</cbc:PayableAmount>
```

---

### 5.4 NEDOPUŠTENA kopija — drugo razdoblje oporezivanja

**Situacija**: Izdavatelj je u ožujku 2026. izdao račun s pogrešnom napomenom (BT-22). Napomena ne utječe na PDV, ali je sada travanj 2026. — drugo razdoblje oporezivanja.

**KRIVO** — čl. 43 vrijedi samo u istom razdoblju oporezivanja:
```xml
<!-- Travanj 2026. — pokušaj ispravka napomene s ožujskog računa -->
<cbc:ID>42/P1/2</cbc:ID>
<cbc:CopyIndicator>true</cbc:CopyIndicator>
<!-- ^^^ NEDOPUŠTENO! Drugo razdoblje oporezivanja -->
```

**ISPRAVNO** — storno + novi račun (jer je prošlo obračunsko razdoblje, mehanizam kopije iz čl. 43 se ne može primijeniti).

---

## 6. Razlika od EU norme
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

EU norma EN16931 **ne koristi** `CopyIndicator` — EU validator izdaje upozorenje **UBL-CR-004** (*"A UBL invoice should not include the CopyIndicator"*). Element postoji u UBL 2.1 XSD shemi, ali nije dio EN16931 semantičkog modela.

Hrvatska je uvela `CopyIndicator` kroz HR CIUS specifikaciju kao **HR-BT-1**, s posebnom svrhom definiranom u čl. 43 Zakona o fiskalizaciji. To nije klasična kopija u smislu UBL standarda, nego mehanizam specifičan za hrvatsku fiskalizaciju.

| Aspekt | EU norma (EN16931) | Hrvatska (HR CIUS) |
|--------|--------------------|--------------------|
| Element | Ne koristi se | HR-BT-1 (`cbc:CopyIndicator`) |
| Validator | UBL-CR-004 upozorenje | Dopušten |
| Svrha | — | Ispravak nePDV podataka (čl. 43) |
| Fiskalizacija | — | `indikatorKopije` obavezan (1..1) |
| Ekvivalent u drugim EU zemljama | **Nema** | Nijedna druga EU zemlja nema ovaj mehanizam u ovom obliku |

> **Napomena**: Upozorenje UBL-CR-004 treba u hrvatskom kontekstu tretirati kao informativno, ne kao zabranu — element je legitimno u upotrebi temeljem HR CIUS proširenja.

---

## 7. Otvorena pitanja

Sljedeća pitanja zahtijevaju službenu potvrdu Porezne uprave:

1. **Datum dospijeća (BT-9)**: Smije li se mijenjati kopijom? PU navodi "promjena podataka o plaćanju" kao dopuštenu (<a href="https://porezna-uprava.gov.hr/hr/ispravci-eracuna-koji-ne-utjecu-na-obracun-poreza-i-statistika-fiskalizacije-2-0/8349" target="_blank">izvor</a>) — ali BT-9 utječe na eIzvještavanje o naplati. Praktički nePDV podatak, ali posljedice za eIzvještavanje nisu jasne.
2. **Adresa kupca/prodavatelja**: Smije li se ispraviti adresa kopijom? Ne utječe na PDV, ali mijenja identifikaciju stranke.
3. **Drugo razdoblje — obaveza storna**: Čl. 43 eksplicitno ograničava kopiju na isto razdoblje oporezivanja. Za ispravke u drugom razdoblju, jedina opcija je storno + novi račun — postoji li iznimka?
4. **Zamjena u evidenciji PU**: Kako PU sustav tretira kopiju — zamjenjuje li original u evidenciji ili ga čuva uz bilješku o ispravku?
5. **Višestruki ispravci**: Može li se isti račun ispraviti kopijom više puta unutar istog razdoblja?
6. **QR kod / UUID**: Generira li kopija novi UUID ili koristi isti kao original?

---

## Izvori

| Izvor | Link |
|-------|------|
| Zakon o fiskalizaciji, čl. 43 (NN 89/25) | <a href="https://zakon.hr/z/2933/Zakon-o-fiskalizaciji" target="_blank">zakon.hr</a> |
| PU: Ispravci eRačuna koji ne utječu na obračun poreza | <a href="https://porezna-uprava.gov.hr/hr/ispravci-eracuna-koji-ne-utjecu-na-obracun-poreza-i-statistika-fiskalizacije-2-0/8349" target="_blank">porezna-uprava.gov.hr</a> |
| PU: Pitanja i odgovori (Q55, Q56) | <a href="https://porezna-uprava.gov.hr" target="_blank">porezna-uprava.gov.hr</a> |
| HR CIUS specifikacija (HR-BT-1) | <a href="https://porezna.gov.hr" target="_blank">porezna.gov.hr</a> |
| Tehnička specifikacija Fiskalizacija (Tablica 76) | <a href="https://porezna.gov.hr" target="_blank">porezna.gov.hr</a> |

---

## Povezane stranice

| Stranica | Relevantnost |
|----------|-------------|
| [Pravila i mehanizmi](pravila) | BT polja koja utječu na PDV — osnova za procjenu što se smije ispraviti kopijom |
| [Primjeri — izdavatelj](primjeri-izdavatelj) | Scenariji izdavanja eRačuna |
| [Prijedlozi za validator](prijedlozi-validator) | Predložena pravila za HR CIUS validator |
| [Referenca](referenca) | XML struktura, pozicija CopyIndicator elementa u dokumentu |
