---
layout: default
title: "Primjeri — izdavatelj eRačuna"
has_toc: true
nav_order: 3
---

# Primjeri iz prakse — izdavatelj eRačuna

Ova stranica pokriva perspektivu **izdavatelja** — koji XML element staviti za koji poslovni slučaj. Za perspektivu primatelja (pretporez, knjiženje troška, skladište) vidi [Primjeri — primatelj](primjeri-primatelj).

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

<a id="kako-citati-xml"></a>

### Kako čitati XML primjere

U primjerima ispod prikazujemo isječke XML koda eRačuna. Kod je **obojan** za lakše čitanje:

- <span style="color:#569cd6">**Plavo**</span> — nazivi XML elemenata (npr. `cbc:IssueDate`, `cac:InvoicePeriod`)
- **Bijelo** — vrijednosti i tekst (npr. `2026-03-15`, `432`)
- <span style="color:#6a9955">***Zeleno italic***</span> — **komentari** (`<!-- ... -->`) — ovo **NIJE dio XML-a**, služi samo kao objašnjenje za čitatelja. Komentari se ne šalju u stvarnoj XML datoteci.

---

> **PU pojašnjenje (19.12.2025., pitanje 155/157)**: Predujmovi iz 2025. se ne izdaju niti fiskaliziraju kao eRačun. Ni konačan račun koji se izdaje u 2026. za takav predujam ne podliježe Fiskalizaciji 2.0.

> **PU pojašnjenje (19.12.2025., pitanje 101/104)**: Zakon o fiskalizaciji odnosi se na eRačune **izdane** od 1.1.2026. — ključan je BT-2 (datum izdavanja), ne datum obavljene usluge.

---

### 4.1 Obračun po izdavanju (čl. 30 Zakona o PDV-u) <span class="badge-izdavanje">Po izdavanju</span>

#### 4.1.1 Isporuka i račun isti dan <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-03-15 |
| Datum isporuke dobara | BT-72 | `cbc:ActualDeliveryDate` | 2026-03-15 |

```xml
<!-- BT-2: Datum izdavanja računa -->
<!-- BT-7: NEMA — datum isporuke = datum izdavanja -->
<!-- BT-8: NEMA -->
<!-- BT-72: NEMA — datum isporuke = datum izdavanja -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<cbc:IssueTime>14:30:00</cbc:IssueTime>
```
> Porezna obveza: **15.03.2026** (= datum izdavanja, default po čl. 30 st. 1)

---

#### 4.1.2 Isporuka u drugom mjesecu od računa <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-04-05 |
| Datum isporuke dobara | BT-72 | `cbc:ActualDeliveryDate` | 2026-03-28 |
| Datum nastanka obveze PDV-a | BT-7 | `cbc:TaxPointDate` | 2026-03-28 |

```xml
<!-- BT-2: Datum izdavanja računa -->
<!-- BT-7: Datum nastanka obveze PDV-a = datum isporuke (čl. 30 st. 1) -->
<!-- BT-72: Stvarni datum isporuke -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-04-05</cbc:IssueDate>
<cbc:IssueTime>09:15:00</cbc:IssueTime>

<cbc:TaxPointDate>2026-03-28</cbc:TaxPointDate>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-03-28</cbc:ActualDeliveryDate>
</cac:Delivery>
```
> Porezna obveza: **28.03.2026** — PDV ulazi u **ožujak**, ne u travanj!
> Razlog: po čl. 30 st. 1 Zakona o PDV-u, obveza nastaje kad su dobra isporučena.

---

#### 4.1.3 Račun izdan prije isporuke (čl. 30 st. 2) <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> *"Ako je račun izdan prije nego su dobra isporučena ili usluge obavljene,*
> *obveza obračuna PDV-a nastaje na dan izdavanja računa."*
> — Čl. 30, st. 2 Zakona o PDV-u
>
> Ovo je **obrnuta situacija** od Primjera B — račun prethodi isporuci.
> Porezna obveza nastaje **danom izdavanja računa**, ne danom isporuke.

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-03-05 |
| Stvarni datum isporuke | BT-72 | `cbc:ActualDeliveryDate` | 2026-03-20 |

```xml
<!-- BT-7: NEMA — porezna obveza = datum izdavanja (čl. 30 st. 2) -->
<!-- BT-8: NEMA — default ponašanje je upravo to što nam treba -->
<!-- BT-72: Isporuka je nakon računa -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-03-05</cbc:IssueDate>
<cbc:IssueTime>10:00:00</cbc:IssueTime>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-03-20</cbc:ActualDeliveryDate>
</cac:Delivery>
```
> PDV ide u **ožujak** — ali po datumu računa (05.03.), ne po datumu isporuke (20.03.).
> Ne trebamo ni BT-7 ni BT-8 jer default (BT-2) je upravo ono što zakon traži.
> BT-72 je informativan — govori kupcu kad će roba biti isporučena.
>
> **Pozor**: Ako su račun i isporuka u **različitim mjesecima** (npr. račun 28.03., isporuka 05.04.),
> PDV i dalje ide u ožujak (datum računa). Ovo je jedini slučaj gdje datum izdavanja
> ima prednost nad datumom isporuke.

---

#### 4.1.4 Predujam / avansni račun (čl. 30 st. 5) <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> *"Za primljene predujmove obveza obračuna PDV-a na primljeni iznos*
> *nastaje u trenutku primitka predujma."*
> — Čl. 30, st. 5 Zakona o PDV-u
>
> Kupac plaća unaprijed. Isporuke još nema. Račun za predujam se izdaje nakon primitka uplate.

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-02-10 |
| Datum primitka predujma | BT-7 | `cbc:TaxPointDate` | 2026-02-05 |

```xml
<!-- BT-7: Datum primitka predujma — to je datum porezne obveze (čl. 30 st. 5) -->
<!-- BT-72: NEMA — isporuka se još nije dogodila -->
<!-- Vrsta dokumenta: 386 = predujam -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-02-10</cbc:IssueDate>
<cbc:IssueTime>08:30:00</cbc:IssueTime>

<cbc:TaxPointDate>2026-02-05</cbc:TaxPointDate>

<cbc:InvoiceTypeCode>386</cbc:InvoiceTypeCode>
```
> PDV ide u **veljaču** — po datumu primitka predujma (05.02.), ne po datumu računa (10.02.).
> BT-72 se ne koristi jer roba/usluga još nije isporučena.
> Vrsta dokumenta je **386** (predujam), ne 380 (standardni račun).
>
> **Važno**: Kod predujma, BT-7 je **datum primitka uplate**, ne datum isporuke.
> Ovo je poseban slučaj čl. 30 st. 5 gdje porezna obveza nastaje
> primanjem novca, a ne isporukom dobara.

> **PU pojašnjenje (19.12.2025., pitanje 222)**: Porezni obveznik nije obvezan izdati račun za primljeni predujam ako je izdao račun za obavljenu isporuku do roka za podnošenje prijave PDV-a za razdoblje u kojem je primio predujam. Međutim, ako je predujam primljen u jednom razdoblju oporezivanja, a isporuka se obavi u drugom — račun za predujam se **mora** izdati.

> **Kompletni ciklus predujma**: Ovaj primjer prikazuje samo **prvi korak** — račun za predujam. Kad isporuka bude obavljena (u drugom razdoblju), potrebno je izdati: (1) **storno računa za predujam** — preporučamo vrstu **381** (CreditNote) ili **386 s negativnom količinom** jer ne zahtijevaju KPD klasifikaciju (HR-BR-25); vrsta 384 zahtijeva KPD što je problematično za predujam — i (2) **konačni račun** za puni iznos (vrsta 380). Detaljan prikaz: [Naknadno dospjeli računi — predujam](naknadno-dospjeli-racuni#12-predujam-iz-2025-konačni-račun-2026).

---

#### 4.1.5 Kontinuirana usluga — obračunsko razdoblje (BT-73, BT-74) <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> IT podrška za razdoblje siječanj–ožujak 2026. Račun izdan u travnju.
> Ovo je primjer iz čl. 30 st. 2 Zakona o PDV-u: *"Za kontinuirane isporuke dobara*
> *ili usluge sa stalnim računima, smatra se da su isporučeni po isteku razdoblja*
> *na koje se računi odnose."*
>
> Kod kontinuiranih usluga nema jednog datuma isporuke — porezna obveza nastaje istekom
> razdoblja (čl. 30 st. 2). BT-73/BT-74 opisuju to razdoblje, ali **datum poreza i dalje
> određuje BT-7** koji se postavlja na kraj razdoblja (= BT-74).

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-04-05 |
| Početak obračunskog razdoblja | BT-73 | `cbc:StartDate` | 2026-01-01 |
| Kraj obračunskog razdoblja | BT-74 | `cbc:EndDate` | 2026-03-31 |
| Datum nastanka obveze PDV-a | BT-7 | `cbc:TaxPointDate` | 2026-03-31 |

```xml
<!-- BT-7: Datum nastanka obveze PDV-a = kraj obračunskog razdoblja -->
<!-- BT-73/BT-74: Obračunsko razdoblje — informacija o periodu usluge -->
<!-- BT-72: NEMA — kod kontinuiranih usluga nema jednog datuma isporuke -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-04-05</cbc:IssueDate>
<cbc:IssueTime>10:00:00</cbc:IssueTime>

<cbc:TaxPointDate>2026-03-31</cbc:TaxPointDate>

<cac:InvoicePeriod>
  <cbc:StartDate>2026-01-01</cbc:StartDate>
  <cbc:EndDate>2026-03-31</cbc:EndDate>
</cac:InvoicePeriod>
```
> PDV ide u **ožujak** — kraj obračunskog razdoblja (čl. 30 st. 2).
> BT-73/BT-74 opisuju razdoblje usluge (siječanj–ožujak).
> BT-7 je eksplicitno postavljen na kraj razdoblja (31.03.) jer tada nastaje porezna obveza.
> BT-72 se ne koristi jer nema jednog datuma isporuke — usluga je kontinuirana.
>
> **Važno**: BT-73 i BT-74 sami po sebi NE određuju datum poreza — oni su informativni.
> Datum poreza i dalje određuje BT-7 (ili BT-8). Ali za kontinuirane usluge, BT-7
> se postavlja na datum koji proizlazi iz čl. 30 st. 2 — kraj razdoblja.

#### 4.1.5a Što ako izostavimo BT-7 kod kontinuirane usluge? <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Isti slučaj kao D.4 (IT podrška sij–ožu, račun u travnju), ali **bez BT-7**.

```xml
<!-- BT-7: NEMA! -->
<!-- BT-8: NEMA! -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-04-05</cbc:IssueDate>
<cbc:IssueTime>10:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:StartDate>2026-01-01</cbc:StartDate>
  <cbc:EndDate>2026-03-31</cbc:EndDate>
</cac:InvoicePeriod>
```
> Bez BT-7 i BT-8, porezna obveza = BT-2 (datum izdavanja) = **travanj**.
> Ali po čl. 30 st. 2, obveza je nastala istekom razdoblja = **ožujak**.
> **PDV završava u krivom mjesecu!**
>
> BT-73/BT-74 su samo informativni — govore primatelju da se račun odnosi
> na razdoblje sij–ožu, ali sustav ih **ne koristi za određivanje datuma poreza**.
> Bez BT-7 ili BT-8, sustav uvijek uzima BT-2 kao datum porezne obveze.
>
> **Zaključak**: Za kontinuirane usluge BT-7 je **nužan** — bez njega PDV
> ide u mjesec izdavanja računa umjesto u mjesec završetka usluge.

#### 4.1.5b BT-7 različit od kraja razdoblja — je li to ispravno? <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Isti slučaj, ali BT-7 postavljen na veljaču umjesto na ožujak.

| Podatak | BT polje | Vrijednost |
|---------|----------|-----------|
| Datum izdavanja računa | BT-2 | 2026-04-05 |
| Početak obračunskog razdoblja | BT-73 | 2026-01-01 |
| Kraj obračunskog razdoblja | BT-74 | 2026-03-31 |
| Datum nastanka obveze PDV-a | BT-7 | **2026-02-15** |

```xml
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-04-05</cbc:IssueDate>
<cbc:TaxPointDate>2026-02-15</cbc:TaxPointDate>
<cac:InvoicePeriod>
  <cbc:StartDate>2026-01-01</cbc:StartDate>
  <cbc:EndDate>2026-03-31</cbc:EndDate>
</cac:InvoicePeriod>
```
> **Schematron validator**: prolazi — HR-BR-48 samo provjerava raspon datuma (1900–2100),
> ne provjerava logičku vezu između BT-7 i BT-73/BT-74.
>
> **Zakonski**: **neispravno** — po čl. 30 st. 2, za kontinuirane usluge porezna obveza
> nastaje istekom razdoblja (ožujak), ne u nekom proizvoljnom mjesecu unutar razdoblja.
> Porezna uprava bi mogla osporiti PDV prijavu jer je PDV prikazan u veljači
> umjesto u ožujku.
>
> **Zaključak**: Validator ne hvata sve zakonske nepravilnosti. Činjenica da XML prolazi
> validaciju ne znači da je porezno ispravan. BT-7 kod kontinuiranih usluga **mora biti
> jednak BT-74** (kraj obračunskog razdoblja) da bi bio usklađen s čl. 30 st. 2.

#### 4.1.6 BT-8=35 — automatska veza na datum isporuke <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Umjesto da eksplicitno upišemo datum u BT-7, kažemo sustavu:
> "datum porezne obveze = datum isporuke (BT-72)".
> Rezultat je isti kao D.1, ali mehanizam je drugačiji.

```xml
<!-- BT-7: NEMA — koristimo BT-8 umjesto eksplicitnog datuma -->
<!-- BT-8 = 35: porezna obveza = BT-72 ActualDeliveryDate -->
<!-- BT-72: Stvarni datum isporuke — sustav automatski koristi ovaj datum za PDV -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-03-10</cbc:IssueDate>
<cbc:IssueTime>09:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:DescriptionCode>35</cbc:DescriptionCode>
</cac:InvoicePeriod>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-01-25</cbc:ActualDeliveryDate>
</cac:Delivery>
```
> PDV ide u **siječanj** — isti rezultat kao D.1.
> Razlika: BT-7 eksplicitno piše datum, BT-8=35 govori sustavu "pogledaj BT-72".
> Prednost BT-8=35: garantira konzistentnost — nema rizika da BT-7 i BT-72 budu različiti.
> Nedostatak: ne možemo odvojiti datum poreza od datuma isporuke (vidi D.4).

#### 4.1.7 Odobrenje / CreditNote <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Odobrenje (knjižno odobrenje) umanjuje iznos prethodno izdanog računa.
> U UBL CreditNote XSD shemi BT-7 (`cbc:TaxPointDate`) i BT-8 (`cac:InvoicePeriod/cbc:DescriptionCode`) **postoje kao opcionalni elementi**, ali se za odobrenja u praksi obično ne koriste — porezna korekcija prati datum izdavanja odobrenja (BT-2).

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja odobrenja | BT-2 | `cbc:IssueDate` | 2026-04-10 |
| Referenca na izvorni račun | BT-25 | `cbc:ID` (BillingReference) | 147/1/1 |
| Datum izvornog računa | BT-26 | `cbc:IssueDate` (BillingReference) | 2026-03-15 |

```xml
<!-- Korijen: CreditNote, NE Invoice -->
<!-- BT-7: Postoji u CreditNote shemi ali se za odobrenja obično ne koristi -->
<!-- Vrsta dokumenta: 381 = odobrenje -->
<!-- BT-25/BT-26: Referenca na izvorni račun -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<CreditNote>
  <cbc:IssueDate>2026-04-10</cbc:IssueDate>
  <cbc:IssueTime>12:00:00</cbc:IssueTime>

  <cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>

  <cac:BillingReference>
    <cac:InvoiceDocumentReference>
      <cbc:ID>147/1/1</cbc:ID>
      <cbc:IssueDate>2026-03-15</cbc:IssueDate>
    </cac:InvoiceDocumentReference>
  </cac:BillingReference>
</CreditNote>
```
> PDV korekcija u praksi najčešće ide u **travanj** (datum izdavanja odobrenja). Međutim, prema pravomoćnoj presudi ECJ [C-518/14 (Senatex)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun), izdavatelj **ima pravo** na retroaktivni ispravak PDV-a u **ožujku** (mjesec izvornog računa 147/1/1) — i PU mu to ne smije uskratiti. Obveznik bira pristup.
> BT-7 i BT-8 **postoje** u UBL CreditNote XSD shemi kao opcionalni elementi, ali se za odobrenja u praksi ne koriste.
> Referenca na izvorni račun (BT-25/BT-26) povezuje odobrenje s originalnim računom i omogućuje retroaktivno knjiženje.
>
> **Napomena**: U praksi, knjigovođa odlučuje u koje porezno razdoblje ulazi
> korekcija PDV-a — to ovisi o internim pravilima i nije definirano XML-om.

---


#### 4.1.8 Svi datumi u različitim mjesecima — BT-7 eksplicitni datum <span class="badge-izdavanje">Po izdavanju</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Isporuka je bila u siječnju → porezna obveza nastala u siječnju.
> BT-7 eksplicitno upisuje datum isporuke kao datum porezne obveze.

```xml
<!-- BT-7: Eksplicitni datum nastanka obveze PDV-a = datum isporuke -->
<!-- BT-72: Stvarni datum isporuke -->
<!-- HR-BT-15: NEMA — obračun po izdavanju -->
<cbc:IssueDate>2026-03-10</cbc:IssueDate>
<cbc:IssueTime>09:00:00</cbc:IssueTime>

<cbc:TaxPointDate>2026-01-25</cbc:TaxPointDate>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-01-25</cbc:ActualDeliveryDate>
</cac:Delivery>
```
> PDV ide u **siječanj**. BT-7 i BT-72 imaju isti datum jer je
> porezna obveza vezana za isporuku (čl. 30 st. 1).

### 4.2 Obračun po naplaćenoj naknadi (čl. 125.i Zakona o PDV-u) <span class="badge-naplata">Po naplati</span>

#### 4.2.1 Isporuka i račun isti mjesec <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-03-15 |
| Stvarni datum isporuke | BT-72 | `cbc:ActualDeliveryDate` | 2026-03-10 |
| Kod datuma PDV obveze | BT-8 | `cbc:DescriptionCode` | 432 |
| Datum plaćanja | — | — | nije poznat u trenutku izdavanja |

```xml
<!-- BT-2: Datum izdavanja -->
<!-- BT-7: NEMA! (BR-CO-03 — ne smije biti uz BT-8) -->
<!-- BT-8 = 432: Porezna obveza nastaje danom plaćanja -->
<!-- BT-72: Datum isporuke -->
<!-- HR-BT-15: U HRFISK20Data bloku -->
<!-- ... ostali HR podaci ... -->
<cbc:IssueDate>2026-03-15</cbc:IssueDate>
<cbc:IssueTime>11:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:DescriptionCode>432</cbc:DescriptionCode>
</cac:InvoicePeriod>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-03-10</cbc:ActualDeliveryDate>
</cac:Delivery>

<ext:UBLExtensions>
  <ext:UBLExtension>
    <ext:ExtensionContent>
      <hrextac:HRFISK20Data>
        <hrextac:HRObracunPDVPoNaplati>
          Obračun prema naplaćenoj naknadi
        </hrextac:HRObracunPDVPoNaplati>
      </hrextac:HRFISK20Data>
    </ext:ExtensionContent>
  </ext:UBLExtension>
</ext:UBLExtensions>
```
> Porezna obveza: **nepoznata** — nastat će tek kada kupac plati račun

---

#### 4.2.2 Isporuka u drugom mjesecu od računa <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Isti podaci, ali obveznik koristi obračun po naplaćenoj naknadi.
> Ni isporuka ni izdavanje ne određuju datum poreza — samo plaćanje.

```xml
<!-- BT-7: NEMA — datum poreza nije poznat (BR-CO-03) -->
<!-- BT-8 = 432: porezna obveza nastaje danom plaćanja -->
<!-- BT-72: Stvarni datum isporuke — informativan, NE utječe na PDV -->
<cbc:IssueDate>2026-03-10</cbc:IssueDate>
<cbc:IssueTime>09:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:DescriptionCode>432</cbc:DescriptionCode>
</cac:InvoicePeriod>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-01-25</cbc:ActualDeliveryDate>
</cac:Delivery>

<!-- HR-BT-15: Obavezno za obračun po naplaćenoj naknadi -->
<ext:UBLExtensions>
  <ext:UBLExtension>
    <ext:ExtensionContent>
      <hrextac:HRFISK20Data>
        <hrextac:HRObracunPDVPoNaplati>
          Obračun prema naplaćenoj naknadi
        </hrextac:HRObracunPDVPoNaplati>
      </hrextac:HRFISK20Data>
    </ext:ExtensionContent>
  </ext:UBLExtension>
</ext:UBLExtensions>
```
> PDV ide u **travanj** — obveza nastaje tek plaćanjem 15.04.
> BT-72 (siječanj) je samo informativan za kupca.
> BT-2 (ožujak) je samo administrativni datum izdavanja.
> Ni jedan ni drugi ne utječe na poreznu obvezu.

#### 4.2.3 Račun izdan prije isporuke <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Račun izdan 05.03., isporuka planirana 20.03., kupac plaća 10.04.
> Kod obračuna po naplati, niti datum računa niti datum isporuke ne igraju ulogu — PDV nastaje isključivo plaćanjem.

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-03-05 |
| Stvarni datum isporuke | BT-72 | `cbc:ActualDeliveryDate` | 2026-03-20 |
| Kod datuma PDV obveze | BT-8 | `cbc:DescriptionCode` | 432 |

```xml
<!-- BT-7: NEMA (BR-CO-03) -->
<!-- BT-8 = 432: porezna obveza nastaje danom plaćanja -->
<!-- BT-72: informativan — ne utječe na PDV -->
<cbc:IssueDate>2026-03-05</cbc:IssueDate>
<cbc:IssueTime>10:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:DescriptionCode>432</cbc:DescriptionCode>
</cac:InvoicePeriod>

<cac:Delivery>
  <cbc:ActualDeliveryDate>2026-03-20</cbc:ActualDeliveryDate>
</cac:Delivery>

<!-- HR-BT-15: Obavezno za obračun po naplaćenoj naknadi -->
<ext:UBLExtensions>
  <ext:UBLExtension>
    <ext:ExtensionContent>
      <hrextac:HRFISK20Data>
        <hrextac:HRObracunPDVPoNaplati>
          Obračun prema naplaćenoj naknadi
        </hrextac:HRObracunPDVPoNaplati>
      </hrextac:HRFISK20Data>
    </ext:ExtensionContent>
  </ext:UBLExtension>
</ext:UBLExtensions>
```
> PDV ide u **travanj** — obveza nastaje plaćanjem 10.04. (čl. 125.i).
> Za razliku od obračuna po izdavanju (4.1.3) gdje bi PDV išao u ožujak po datumu računa,
> ovdje čak i datum računa ne igra ulogu.

#### 4.2.4 Predujam / avansni račun <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Kupac plaća unaprijed 05.02., račun za predujam izdan 10.02., isporuke još nema.
> Kod obračuna po naplati, predujam je poseban slučaj: kupac je **već platio** — dakle PDV obveza nastaje **odmah** pri primitku predujma, jednako kao kod obračuna po izdavanju (čl. 30 st. 5).

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja računa | BT-2 | `cbc:IssueDate` | 2026-02-10 |
| Datum primitka predujma/plaćanja | BT-7 | `cbc:TaxPointDate` | 2026-02-05 |

```xml
<!-- BT-7: datum primitka predujma = datum plaćanja = datum porezne obveze -->
<!-- BT-8: NEMA — koristimo BT-7 jer je datum plaćanja poznat -->
<!-- BT-72: NEMA — isporuka se još nije dogodila -->
<cbc:IssueDate>2026-02-10</cbc:IssueDate>
<cbc:IssueTime>08:30:00</cbc:IssueTime>

<cbc:TaxPointDate>2026-02-05</cbc:TaxPointDate>

<cbc:InvoiceTypeCode>386</cbc:InvoiceTypeCode>

<!-- HR-BT-15: Obavezno — obveznik koristi obračun po naplaćenoj naknadi -->
<ext:UBLExtensions>
  <ext:UBLExtension>
    <ext:ExtensionContent>
      <hrextac:HRFISK20Data>
        <hrextac:HRObracunPDVPoNaplati>
          Obračun prema naplaćenoj naknadi
        </hrextac:HRObracunPDVPoNaplati>
      </hrextac:HRFISK20Data>
    </ext:ExtensionContent>
  </ext:UBLExtension>
</ext:UBLExtensions>
```
> PDV ide u **veljaču** — predujam je primljen 05.02. (čl. 30 st. 5).
> Ovo je jedini slučaj kod obračuna po naplati gdje koristimo **BT-7 umjesto BT-8** — jer je datum plaćanja poznat (kupac je već platio), pa nema smisla stavljati BT-8=432 ("datum plaćanja će se odrediti u budućnosti").
>
> **HR-BT-15 je i dalje obavezan** — iako koristimo BT-7 umjesto BT-8, obveznik je registriran za obračun po naplaćenoj naknadi i ta informacija mora biti u HRFISK20Data bloku za fiskalizacijsku poruku prema Poreznoj upravi.
>
> **Zaključak**: Predujam kod obračuna po naplati koristi BT-7 (jer je datum plaćanja poznat), ali HR-BT-15 ostaje obavezan jer je to svojstvo obveznika, ne pojedinačnog računa.

> **PU pojašnjenje (19.12.2025., pitanje 222)**: Porezni obveznik nije obvezan izdati račun za primljeni predujam ako je izdao račun za obavljenu isporuku do roka za podnošenje prijave PDV-a za razdoblje u kojem je primio predujam. Međutim, ako je predujam primljen u jednom razdoblju oporezivanja, a isporuka se obavi u drugom — račun za predujam se **mora** izdati.

> **Kompletni ciklus predujma**: Ovaj primjer prikazuje samo **prvi korak** — račun za predujam. Kad isporuka bude obavljena, potrebno je izdati storno predujma + konačni račun. Sva tri dokumenta moraju imati HR-BT-15 jer je izdavatelj na sustavu po naplati. Detaljan prikaz: [Naknadno dospjeli računi — predujam](naknadno-dospjeli-racuni#12-predujam-iz-2025-konačni-račun-2026).

#### 4.2.5 Kontinuirana usluga s obračunskim razdobljem <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> IT podrška za razdoblje siječanj–ožujak, račun u travnju, kupac plaća u lipnju.
> Obveznik koristi obračun po naplaćenoj naknadi (čl. 125.i).

```xml
<!-- BT-7: NEMA — jer koristimo BT-8 (BR-CO-03) -->
<!-- BT-8 = 432 + BT-73/BT-74 zajedno u InvoicePeriod -->
<cbc:IssueDate>2026-04-05</cbc:IssueDate>
<cbc:IssueTime>10:00:00</cbc:IssueTime>

<cac:InvoicePeriod>
  <cbc:StartDate>2026-01-01</cbc:StartDate>
  <cbc:EndDate>2026-03-31</cbc:EndDate>
  <cbc:DescriptionCode>432</cbc:DescriptionCode>
</cac:InvoicePeriod>

<!-- HR-BT-15: Obavezno za obračun po naplaćenoj naknadi -->
<ext:UBLExtensions>
  <ext:UBLExtension>
    <ext:ExtensionContent>
      <hrextac:HRFISK20Data>
        <hrextac:HRObracunPDVPoNaplati>
          Obračun prema naplaćenoj naknadi
        </hrextac:HRObracunPDVPoNaplati>
      </hrextac:HRFISK20Data>
    </ext:ExtensionContent>
  </ext:UBLExtension>
</ext:UBLExtensions>
```
> PDV ide u **lipanj** — obveza nastaje tek plaćanjem (čl. 125.i).
> BT-73/BT-74 (sij–ožu) govore kupcu za koje razdoblje je račun.
> BT-8=432 govori sustavu da datum poreza ovisi o plaćanju.
> Sve tri informacije (razdoblje, način obračuna, datum plaćanja) su neovisne.
>
> **Važno**: BT-8 (DescriptionCode) i BT-73/BT-74 (StartDate/EndDate) mogu
> koegzistirati unutar istog `cac:InvoicePeriod` elementa — nisu međusobno isključivi.
> Međusobno isključivi su samo BT-7 i BT-8 (pravilo BR-CO-03).

#### 4.2.6 Odobrenje / CreditNote <span class="badge-naplata">Po naplati</span>
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Odobrenje za obveznika koji koristi obračun po naplaćenoj naknadi.
> Odobrenje umanjuje iznos prethodno izdanog računa 147/1/1 od 15.03.2026.

| Podatak | BT polje | XML element | Vrijednost |
|---------|----------|-------------|-----------|
| Datum izdavanja odobrenja | BT-2 | `cbc:IssueDate` | 2026-04-10 |
| Referenca na izvorni račun | BT-25 | `cbc:ID` (BillingReference) | 147/1/1 |
| Datum izvornog računa | BT-26 | `cbc:IssueDate` (BillingReference) | 2026-03-15 |

```xml
<!-- BT-7: Postoji u CreditNote shemi ali se za odobrenja obično ne koristi -->
<!-- BT-8=432: Mogao bi se koristiti za CreditNote po naplati (vidi napomenu ispod) -->
<!-- Korijen: CreditNote, NE Invoice -->
<CreditNote>
  <cbc:IssueDate>2026-04-10</cbc:IssueDate>
  <cbc:IssueTime>12:00:00</cbc:IssueTime>

  <cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>

  <cac:BillingReference>
    <cac:InvoiceDocumentReference>
      <cbc:ID>147/1/1</cbc:ID>
      <cbc:IssueDate>2026-03-15</cbc:IssueDate>
    </cac:InvoiceDocumentReference>
  </cac:BillingReference>

  <!-- HR-BT-15: Obavezno — obveznik koristi obračun po naplaćenoj naknadi -->
  <ext:UBLExtensions>
    <ext:UBLExtension>
      <ext:ExtensionContent>
        <hrextac:HRFISK20Data>
          <hrextac:HRObracunPDVPoNaplati>
            Obračun prema naplaćenoj naknadi
          </hrextac:HRObracunPDVPoNaplati>
        </hrextac:HRFISK20Data>
      </ext:ExtensionContent>
    </ext:UBLExtension>
  </ext:UBLExtensions>
</CreditNote>
```
> BT-7 i BT-8 **postoje** u UBL CreditNote XSD shemi kao opcionalni elementi. Za CreditNote po naplati,
> BT-8=432 bi se teoretski mogao koristiti kao signal obračuna po naplati — što znači da HR-BT-15
> **nije jedini** mogući signal za obračun po naplati u CreditNote. Ipak, **HR-BT-15 je obavezan** jer je obveznik
> registriran za obračun po naplaćenoj naknadi. `UBLExtensions` blok postoji i u CreditNote
> shemi — schematron pravila koriste `//` xpath koji pokriva i Invoice i CreditNote.
>
> Za razliku od primjera 4.1.7 (CreditNote po izdavanju) koji nema HR-BT-15,
> ovdje ga **moramo uključiti** jer posrednik iz njega generira fiskalizacijsku poruku
> s oznakom obračuna po naplaćenoj naknadi. Činjenica da bi se i BT-8=432 mogao koristiti
> u CreditNote dodatno pojačava pitanje je li HR-BT-15 zaista potreban kao zasebni element.
>
> Prema pravomoćnoj presudi ECJ [C-518/14 (Senatex)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun), izdavatelj ima pravo na retroaktivni ispravak PDV-a u mjesecu izvornog računa.

### Utjecaj BT-72 i BT-73/74 na prihod i otpremnicu (izdavatelj)
<div style="margin-top:-0.8rem;margin-bottom:1rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Izdavatelj mora razlikovati **PDV period** (BT-7/BT-8/BT-2) od **prihoda** (BT-72, HSFI 15) i **otpremnice** (BT-72).

| Scenarij | BT-2 (račun) | BT-72 (isporuka) | Prihod (HSFI 15) | Otpremnica | PDV period |
|---|---|---|---|---|---|
| Isti dan | 15.03. | 15.03. | Ožujak | 15.03. | Ožujak |
| Račun nakon isporuke | 05.04. | 28.03. | **Ožujak** (po isporuci) | 28.03. | Ožujak (BT-7) |
| Račun prije isporuke | 25.03. | 05.04. | **Travanj** (isporuka tek u 04) | 05.04. | Ožujak (BT-7=BT-2, čl. 30 st. 2) |
| Kontinuirana usluga | 05.04. | — | **Q1** (BT-73=01.01., BT-74=31.03.) | — (usluga) | Ožujak (BT-7=31.03.) |
| Predujam | 10.02. | — | Ne priznaje se (primljeno sredstvo) | — | Veljača (BT-7=05.02.) |

> **Ključni uvid za izdavatelja**: Prihod se UVIJEK priznaje po datumu isporuke (BT-72) ili po obračunskom razdoblju (BT-73/BT-74), ne po datumu računa (BT-2). PDV može biti u drugom mjesecu od prihoda — to nije greška nego normalan rad sustava.

### 4.3 Usporedba svih mehanizama za isti poslovni slučaj <span class="badge-usporedba">Usporedba</span>
<div style="margin-top:-0.8rem;margin-bottom:1rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

> Pregled: roba isporučena 25.01., račun izdan 10.03., kupac plaća 15.04.

| Mehanizam | Obračun | BT-7 | BT-8 | BT-72 | HR-BT-15 | PDV u mjesecu | Zakonski temelj |
|-----------|---------|:----:|:----:|:-----:|:--------:|:-------------:|-----------------|
| **Ni BT-7 ni BT-8** | <span class="badge-izdavanje">Po izdavanju</span> | — | — | 25.01. | — | **Ožujak** (datum računa) | Default |
| **BT-7 eksplicitno** | <span class="badge-izdavanje">Po izdavanju</span> | 25.01. | — | 25.01. | — | **Siječanj** (datum isporuke) | Čl. 30, st. 1 |
| **BT-8 = 35** | <span class="badge-izdavanje">Po izdavanju</span> | — | 35 | 25.01. | — | **Siječanj** (= BT-72) | Čl. 30, st. 1 |
| **BT-8 = 432** | <span class="badge-naplata">Po naplati</span> | — | 432 | 25.01. | DA | **Travanj** (datum plaćanja) | Čl. 125.i |
| **BT-8 = 3** | <span class="badge-izdavanje">Po izdavanju</span> | — | 3 | 25.01. | — | **Ožujak** (= BT-2) | Redundantno |

> Ista roba, isti datumi — pet različitih PDV tretmana ovisno o odabiru BT-7/BT-8.
> U praksi se za jednokratne isporuke koristi BT-7 (eksplicitno), a BT-8=432 za obračun po naplati.
> BT-8=35 je alternativa BT-7 koja garantira konzistentnost s BT-72.
> BT-8=3 je redundantan (isto kao default) i u praksi se ne koristi.

---
