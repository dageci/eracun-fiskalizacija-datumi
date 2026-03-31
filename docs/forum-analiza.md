---
layout: default
title: "Analiza forum.hr diskusija"
has_toc: true
nav_order: 12
---

# Analiza forum.hr diskusija — Fiskalizacija za developere

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo su mišljenja i iskustva developera, ne službene upute</strong><br>
Sve navedeno proizlazi iz forum.hr rasprava i predstavlja praktična iskustva programera. Navodi NE predstavljaju službeno stajalište Porezne uprave, posrednika niti zakonodavca. Tamo gdje postoji službeni izvor, naveden je.
</div>

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## 1. O analizi

| Parametar | Vrijednost |
|-----------|-----------|
| **Izvor** | [Fiskalizacija za developere — forum.hr](https://www.forum.hr/showthread.php?t=1040421) |
| **Analizirane stranice** | 100–232 (od ukupno 232) |
| **Broj postova** | **2.657** |
| **Razdoblje postova** | 27.11.2025. – 31.03.2026. |
| **Datum analize** | 31.03.2026. |
| **Ostali forumi** | Reddit, bug.hr, jabucnjak.hr, misljenja.hr — provjereni, bez relevantnog developer sadržaja |

### Top autori po broju postova

| Autor | Postova | Autor | Postova |
|-------|:-------:|-------|:-------:|
| ceha | 326 | PBDudek | 85 |
| zoranb | 286 | idelovski | 73 |
| Denis365 | 162 | Novi12 | 62 |
| trnac | 158 | partyelite | 54 |
| AyV4n | 140 | vvrbane | 48 |
| zac1608 | 136 | dzidaaaa | 44 |
| tkralj | 114 | salk | 43 |

### Tematska distribucija

| Tema | Postova |
|------|:-------:|
| Posrednici (MER, PONDI, ePoslovanje) | 1.075 |
| Greške / problemi / padovi sustava | 662 |
| Schematron / validacija / BR pravila | 535 |
| XML / UBL format / struktura | 485 |
| DEMO / testiranje | 290 |
| CreditNote / odobrenje / storno | 257 |
| eIzvještavanje | 192 |
| HR CIUS specifikacija / dokumentacija | 180 |
| Fiskalizacijska SOAP poruka | 164 |
| Predujam / avans | 144 |
| Popusti / AllowanceCharge | 137 |
| Certifikat / FINA / potpis | 136 |
| FiskAplikacija | 135 |
| Indikator kopije | 83 |
| BT-7/BT-8 datumska polja | 52 |
| BT-72 datum isporuke | 50 |
| BT-9 DueDate | 41 |
| BT-73/74 razdoblje | 39 |
| Zaokruživanje / decimale | 30 |
| HR-BT-15 po naplati | 16 |

> **Napomena:** Jedan post može spadati u više kategorija. Nekategorizirano: 545 postova (opći razgovori, off-topic).

---

## 2. Datumska polja — najvažniji nalaz iz prakse

### 2.1. TaxPointDate (BT-7) se NE šalje u fiskalizacijsku SOAP poruku

<div style="background: #fef3cd; border-left: 5px solid #f39c12; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong>Kritični nalaz</strong><br>
TaxPointDate (BT-7) — datum nastanka obveze PDV-a — <strong>ne prenosi se</strong> u fiskalizacijsku SOAP poruku (EvidentirajERacunZahtjev). Porezna uprava ga doslovno <strong>nema u tehničkoj specifikaciji fiskalizacije</strong>. Jedini datumski element u fiskalizaciji je ActualDeliveryDate (BT-72).
</div>

> *"TaxPointDate čak i ne ide u Fisk-poruku."*
> — Novi12 ([#2879](https://www.forum.hr/showpost.php?p=110619187&postcount=2879)), referira [webinar PU](https://youtu.be/aH76g9mWdnA) (40:50)

> *"Za svo neuparivanje, odgovor ti je u teh.specs fiskalizacije računa. A tamo nema TaxPointDate, već isključivo ADT (ActualDeliveryDate)."*
> — Novi12 ([#4284](https://www.forum.hr/showpost.php?p=111005535&postcount=4284))

> *"U fisk aplikaciji nigdje ne bilježi TaxPointDate kao da nije bitan, a bitan je..."*
> — salk ([#4293](https://www.forum.hr/showpost.php?p=111008933&postcount=4293))

### 2.2. Posrednici različito mapiraju datume

Ovo je potvrđeno iz prakse — **isti eRačun** daje **različit datum** na FiskAplikaciji ovisno koji posrednik ga šalje:

| Posrednik | Što koristi za fiskalizaciju | Što koristi za filtriranje |
|-----------|------------------------------|---------------------------|
| **MER** | Samo ActualDeliveryDate (BT-72) | — |
| **FINA** | — | TaxPointDate (BT-7) > BT-8 > IssueDate |
| **e-racuni.com** | TaxPointDate (BT-7) | — |

> *"MER uopće ne gleda TaxPointDate kada šalje podatke na fiskalizaciju već samo isključivo ActualDeliveryDate. Skužili smo kada je kupac bio na e-racuni.com (posrednik) pa MER TaxPointDate nije uzeo u obzir prilikom fiskalizacije dok e-racuni.com je uzeo taj datum u obzir i gle čuda, došlo je do odstupanja."*
> — salk ([#4281](https://www.forum.hr/showpost.php?p=111004685&postcount=4281))

### 2.3. FINA filtrira ulazne račune po TaxPointDate, ne po IssueDate

<div style="background: #fef3cd; border-left: 5px solid #f39c12; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong>Praktična posljedica za ERP sustave</strong><br>
ERP-ovi koji dohvaćaju ulazne račune filtrirajući po <em>datumu izdavanja</em> mogu "izgubiti" račune jer ih FINA filtrira po potpuno drugom datumu.
</div>

> *"Tražilica na FINA servisu radi ovako:*
> *1. Filtrira se po TaxPointDate ako postoji.*
> *2. Ako TaxPointDate ne postoji onda gleda DescriptionCode i ovisno o toj šifri filtrira po: 3=datum izdavanja, 35=datum isporuke, 432=datum plaćanja*
> *3. Ako u UBL-u nema niti TaxPointDate niti DescriptionCode tek tada filtrira po IssueDate"*
> — tkralj ([#2888](https://www.forum.hr/showpost.php?p=110620493&postcount=2888))

### 2.4. FINA koristi TaxPointDate za brojevni slijed

> *"FINA kao godinu računa gleda godinu iz TaxPointDate (ako je datum postavljen) inače iz IssueDate. Ako bismo izdali račun (IssueDate) u 2026. godini koji se odnosi na 2025. godinu (i postavili TaxPointDate) sa numeričkim slijedom iz 2026., FINA bi prilikom slanja odbila takav račun sa greškom da račun sa istim brojem već postoji unutar iste godine."*
> — partyelite ([#2866](https://www.forum.hr/showpost.php?p=110616749&postcount=2866))

### 2.5. Praktično rješenje developera

Na temelju svih ovih problema, većina iskusnih developera je došla do pragmatičnog rješenja — **slati i BT-7 i BT-72 s istim datumom**:

> *"TaxPointDate je u većini slučajeva = Datum izdavanja dokumenta i nije obavezan podatak, ali ja ga stalno postavljam jer je bitan ako je manji od datuma izdavanja dokumenta (...) U fiskalizaciji eRačuna datumIsporuke je obavezan podatak i oni nisu ciljali na ActualDeliveryDate nego upravo na TaxPointDate."*
> — zac1608 ([#2486](https://www.forum.hr/showpost.php?p=110484979&postcount=2486))

| Preporuka developera | Obrazloženje |
|---------------------|--------------|
| **Uvijek slati BT-72** (ActualDeliveryDate) | Jedini datum koji fiskalizacija koristi |
| **Slati i BT-7** (TaxPointDate) kada ≠ BT-2 | Za ispravno filtriranje kod FINE i porezno razdoblje |
| **BT-72 = BT-7** u većini slučajeva | Pokriva razlike među posrednicima |
| **BT-7 i BT-8 ne smiju biti zajedno** | BR-CO-03 — međusobno se isključuju |

### 2.6. BT-8=432 — obračun PDV-a po naplati

Za firme s obračunom PDV-a po naplaćenoj naknadi (čl. 125.i ZPDV):

> *Za obveznike po naplati slati: HRObracunPDVPoNaplati s tekstom "Obračun prema naplaćenim naknadama" (u HR ekstenzijama) + DescriptionCode = 432 (BT-8). NE slati TaxPointDate jer se BT-7 i BT-8 isključuju.*
> — AyV4n ([#3768](https://www.forum.hr/showpost.php?p=110842451&postcount=3768))

### 2.7. BT-9 (DueDate) — CreditNote problem

HR-BR-4 pravilo zahtijeva DueDate za pozitivan PayableAmount. Problem: **Schematron množi CreditNote iznos s -1**, pa negativni CreditNote postaje "pozitivan" i trigera HR-BR-4 — ali CreditNote nema BT-9 polje u XSD shemi.

> *"Validiram credit note i dobijem: [HR-BR-4]... DAKLE KAKAV DATUM DOSPIJEĆA ZA ODOBRENJE"*
> — salk ([#3328](https://www.forum.hr/showpost.php?p=110734865&postcount=3328))

> CreditNote **NE treba** DueDate. Ako validator javlja grešku, **ne valja validator**.
> — zoranb ([#3333](https://www.forum.hr/showpost.php?p=110736749&postcount=3333))

### 2.8. FiskAplikacija ne prikazuje TaxPointDate

Konkretan dokaz iz prakse — poslan XML samo s TaxPointDate (bez ActualDeliveryDate):

> *"Na Fiskaplikaciji porezna ne prikazuje TaxPointDate kao datum obveze za PDV... Kada smo poslali XML samo sa tim datumom i datum izdavanja (ako su datumi bili različiti) nije se moglo shvatiti na koje se porezno razdoblje odnosi taj račun. Zbog toga smo postavili da se uvijek šalje ActualDeliveryDate."*
> — samiloti ([#4634](https://www.forum.hr/showpost.php?p=111474791&postcount=4634))

---

## 3. Schematron validacija — "kupus" u praksi

### 3.1. Greške u službenom Schematronu PU

| Pravilo | Greška | Posljedica |
|---------|--------|------------|
| **HR-BR-27** | Poduplani XPath u liniji 87: `hrextac:HRLegalMonetaryTotal/hrextac:HRLegalMonetaryTotal` | TaxExclusiveAmount u HR ekstenziji se **uopće ne provjerava** — može biti bilo koji iznos |
| **HR-BR-32** | Gleda HR-BT-16 umjesto BT-131 | Neoporezivi iznos se krivo računa |
| **HR-BR-31** | Brisano iz Specifikacije ali ostalo u nekim Schematronima | Lažni fatal error |

> *Detaljna analiza:* zoranb ([#2309](https://www.forum.hr/showpost.php?p=110428807&postcount=2309), [#2379](https://www.forum.hr/showpost.php?p=110449997&postcount=2379), [#2685](https://www.forum.hr/showpost.php?p=110552305&postcount=2685))

### 3.2. Posrednici koriste različite validatore

Isti XML može **proći** na jednom posredniku a **pasti** na drugom:

> *"FINA i MER koriste različite validatore"*
> — Denis365 ([#2167](https://www.forum.hr/showpost.php?p=110356845&postcount=2167))

> *"MER ne koristi službeni schematron — 100% siguran. Kučna radinost."*
> — zac1608 ([#2871](https://www.forum.hr/showpost.php?p=110618395&postcount=2871))

### 3.3. MER prebacio fatal u warning

MER je 30.12.2025. poslao email partnerima da prebacuje više HR-BR pravila iz `fatal` u `warning` na ulaznoj strani:

> *"...jer druge pristupne točke šalju XML-ove koji nemaju implementirana sva poslovna pravila"*

Pravila degradirana u warning: HR-BR-30, HR-BR-09, HR-BR-27, HR-BR-26, HR-BR-31, HR-BR-32.

> *"Koja je to logika?! Kako dobivamo račune koji nisu ispravni, ugasit ćemo provjeru pa će se činiti kao jesu ispravni."*
> — zoranb ([#2685](https://www.forum.hr/showpost.php?p=110552305&postcount=2685))

Puni tekst emaila: ceha ([#2678](https://www.forum.hr/showpost.php?p=110550029&postcount=2678))

### 3.4. MER mijenja sadržaj UBL-a

MER zamjenjuje `CustomizationID` i `ProfileID` u primljenim računima (npr. "MojEracunInvoice"), briše fiskalizacijske podatke i dodaje namespace-ove:

> *"Replacea sa MojEracunInvoice, izbaci moju fiskalizaciju, pobriše mi model iz poziva na broj"*
> — tkralj ([#2966](https://www.forum.hr/showpost.php?p=110636757&postcount=2966))

> Ovo je kršenje EU Direktive 2006/112/EZ o cjelovitosti sadržaja.
> — Denis365 ([#2976](https://www.forum.hr/showpost.php?p=110639915&postcount=2976))

### 3.5. Primjeri PU ne prolaze vlastiti validator

> *"Ovi primjeri naravno ne prolaze na MER validatoru"*
> — plastic.ono ([#2251](https://www.forum.hr/showpost.php?p=110379079&postcount=2251))

> *"Niti jedan primjer ne prolazi zadnje Schematron sheme"*
> — vvrbane ([#2271](https://www.forum.hr/showpost.php?p=110399131&postcount=2271))

### 3.6. Karusel verzija Specifikacije

Od studenog do prosinca 2025. objavljeno 5+ verzija Specifikacije, neke s neoznačenim promjenama:

| Verzija | Datum | Ključna promjena |
|---------|-------|-----------------|
| v1.2 | 23.06.2025. | HR-BT-4/HR-BT-5 obavezni |
| v1.4 | 12.12.2025. | HR-BT-4/HR-BT-5 **neobavezni**, BR-E-1 ispravljen |
| v1.5 | 15.12.2025. | HR-BR-35 brisan, BR-O-2/3/4 ispravljeni |
| v1.5 | 18.12.2025. | HR-BT-4/HR-BT-5 **OPET obavezni** (bez napomene!) |
| v1.6 | 12.03.2026. | Nova pravila HR-BR-41/44, provjera OIB kontrolne znamenke |

> *Analiza promjena:* zoranb ([#2246](https://www.forum.hr/showpost.php?p=110378269&postcount=2246), [#2277](https://www.forum.hr/showpost.php?p=110408157&postcount=2277), [#2368](https://www.forum.hr/showpost.php?p=110447719&postcount=2368))

### 3.7. Najčešće validacijske greške

| Greška | Opis | Rješenje |
|--------|------|----------|
| **HR-BR-33** | Nedostaje IssueTime | Dodati `<cbc:IssueTime>HH:MM:SS</cbc:IssueTime>` bez timezone |
| **HR-BR-2** | Nedostaje OIB operatera | HR-BT-4 obavezan od v1.5 (18.12.) |
| **HR-BR-25** | Nedostaje KPD | Obavezan za 380/Invoice, NE za 381/CreditNote i 386/predujam |
| **BR-CO-14/15** | Zaokruživanje PDV-a | PDV računati po stavkama, ne na ukupni iznos |
| **BR-E-01** | Kategorija E (oslobođeno) | Samo jedna raspodjela s kodom E; tekst mora biti identičan svuda |
| **IssueTime format** | C# dodaje timezone offset | Regex: ukloniti `+HH:MM` iz `<cbc:IssueTime>` |
| **Datum sa "Z"** | `2026-01-05Z` pada na fiskalizaciji | Format mora biti `YYYY-MM-DD` (točno 10 znakova) |

> *IssueTime regex workaround:* hori ([#2213](https://www.forum.hr/showpost.php?p=110370963&postcount=2213))
> *Datum "Z" analiza:* vvrbane ([#3005](https://www.forum.hr/showpost.php?p=110645819&postcount=3005))

### 3.8. Neovisni validatori koje developeri koriste

| Validator | Autor | URL | Napomena |
|-----------|-------|-----|----------|
| ff-infing.hr | BorF | [link](https://www.ff-infing.hr/xml_validator/validator.html) | Koristi PU Schematron |
| ecosio (phax) | — | [link](https://ecosio.com/en/peppol-e-invoice-document-validator/) | Peppol + HR CIUS |
| ervalidator | s0g | [link](https://ervalidator.dev-urandom.org/) | Rust, ima REST API, provjerava i gramatiku |
| MER validate-demo | MER | — | Samo validator br. 2 je ispravan |

---

## 4. CreditNote / odobrenje / storno

### 4.1. CreditNote s pozitivnim iznosima — kontraintuitivno

UBL CreditNote zahtijeva **pozitivne iznose** (jer je sam dokument po definiciji negativan). Većina developera to smatra kontraintuitivnim:

> *"Taj tko je odobrenja odvojio od računa, i postavio da to ide s pozitivnim iznosima, nema veze s vezom. A naročito s računovodstvom."*
> — Novi12 ([#2192](https://www.forum.hr/showpost.php?p=110362047&postcount=2192))

**Praktično rješenje**: Interno u ERP-u voditi minus, pri slanju CreditNote konvertirati u plus.

> *"Ja ga vodim u računima sa minusom pa onda na slanju konverzija u plus"*
> — salk ([#2202](https://www.forum.hr/showpost.php?p=110369391&postcount=2202))

### 4.2. Tip dokumenta za storno

PU daje **tri različita načina** za storno predujma, što stvara konfuziju:

| Pristup | Tip | PP | Izvor |
|---------|:---:|:--:|-------|
| Korektivni račun | 384 | P10 | PU primjeri |
| CreditNote odobrenje | 381 | P10 | PU primjeri |
| Invoice u minus | 386 | P4 | Praksa developera |

> *"1. Radiš predujam (386) - nema reference; 2. Radiš storno predujma (384) - referenca na predujam; 3. Radiš račun - referenca na storno predujma."*
> — tkralj ([#2146](https://www.forum.hr/showpost.php?p=110351419&postcount=2146))

### 4.3. KPD na odobrenjima — prazan element vs. bez elementa

HR-BR-25 kaže da KPD **nije obavezan** za odobrenja (381) i predujme (386). Ali postoji kvaka:

> *"Upravo sam probao poslati Odobrenje (381/P9) bez KPD i meni ne prolazi račun"*

Rješenje — **potpuno ukloniti** element, ne ostaviti prazan:

> *"Upravo probao poslati Odobrenje bez KPD-a (maknuo sam prazan element) i uredno je prošlo"*
> — skijam ([#3310](https://www.forum.hr/showpost.php?p=110731841&postcount=3310))

### 4.4. MER validator ne podržava CreditNote ispravno

MER-ov XSLT validator očekuje root element `<Invoice>` — za `<CreditNote>` javlja "Root element is missing":

> PBDudek ([#1995](https://www.forum.hr/showpost.php?p=110229643&postcount=1995))

### 4.5. BillingReference (BT-25) — pravila po tipu dokumenta

| Tip | BillingReference | OrderReference |
|-----|:----------------:|:--------------:|
| 380 (račun) | Opcionalno | DA |
| 381 (odobrenje P9) | DA (referenca na račun) | NE |
| 384 (storno P10) | **OBAVEZNO** | **ZABRANJENO** |
| 386 (predujam P4) | NE | DA |
| 386 (storno predujma) | DA (referenca na predujam) | NE |

> *Kompletni pregled:* AyV4n ([#2136](https://www.forum.hr/showpost.php?p=110350415&postcount=2136))

---

## 5. Indikator kopije (CopyIndicator)

### 5.1. Radi SAMO nakon odbijanja primatelja

U praksi, `CopyIndicator=true` funkcionira **isključivo** ako je primatelj prethodno **odbio** račun:

| Scenarij | Rezultat |
|----------|----------|
| Primatelj NIJE odbio račun | ❌ Greška: "Broj računa već postoji" |
| Primatelj JE odbio račun | ✅ Kopija uspješno prolazi |
| Nikad poslan račun s tim brojem | ❌ Greška: "Nije pronađen dokument istog broja" |

> Denis365 ([#3847](https://www.forum.hr/showpost.php?p=110851933&postcount=3847))

### 5.2. Kvaka-22 situacija

Račun poslan s neispravnim OIB-om operatera. Posrednik ga validirao, ali fiskalizacija nije prošla. Ponovno slanje s `CopyIndicator=true` daje grešku "Ne postoji evidentiran originalni eRačun":

> darach ([#3186](https://www.forum.hr/showpost.php?p=110683647&postcount=3186))

### 5.3. MER validator ne podržava CopyIndicator

> *"Meni CopyIndicator u XML ne prolazi validator MER-a (barem ovaj testni)"*
> — ceha ([#3839](https://www.forum.hr/showpost.php?p=110851097&postcount=3839))

### 5.4. Mišljenje developera

Većina developera smatra CopyIndicator **beskorisnim** za realne scenarije (resend neuspjelog slanja, ispravak grešaka). Koristan je samo u uskom scenariju čl. 43 ZOF — ispravak neporeznih podataka nakon što primatelj eksplicitno odbije račun.

---

## 6. Prijelaz godine 2025/2026 — datumski problemi

Intenzivna tema oko prijeloma godine. Ključni primjer iz prakse:

**PBZ račun:**
```xml
<cbc:ID>64896/7/1/2025</cbc:ID>
<cbc:IssueDate>2026-01-02</cbc:IssueDate>
<cbc:TaxPointDate>2025-12-31</cbc:TaxPointDate>
```

PBZ je izdao račun 02.01.2026. s TaxPointDate 31.12.2025. i brojem iz 2025. — izazvalo raspravu je li ispravno.

> *"Ne možeš retroaktivno izdavati račune u F2. IssueDate & IssueTime = now()!, TaxPointDate staviš unazad i tjt."*
> — zac1608 ([#2870](https://www.forum.hr/showpost.php?p=110618135&postcount=2870))

> *"Računi koji se rade u 2026. i šalju na fiskalizaciju a datumski spadaju u 2025. moraju imati brojevni krug 2026. IssueDate=5.1.2026., TaxPointDate=31.12.2025."*
> — spikezg ([#2487](https://www.forum.hr/showpost.php?p=110485249&postcount=2487))

---

## 7. Stav zajednice

> *"Gotovo sam uvjeren da u P.U. ne postoji osoba koja zna kako TOČNO treba izgledati ispravna XML datoteka"*
> — zoranb ([#2265](https://www.forum.hr/showpost.php?p=110389051&postcount=2265))

> *"Da, jako je važan [TaxPointDate]. Sami su to stavili u Zakon, a onda s druge strane realizacija..."*
> — zac1608 ([#4297](https://www.forum.hr/showpost.php?p=111010741&postcount=4297))

### Sistemski problemi koje developeri identificiraju

1. **Nedostaje jedinstven, ispravan, javni validator** — svaki posrednik koristi svoj, s različitim rezultatima
2. **Nedostaje standardizirani API za posrednike** — MER, PONDI, ePoslovanje imaju potpuno različite API-je
3. **Specifikacija se mijenja bez adekvatnog verzioniranja** — promjene obaveznosti polja bez bilješke u povijesti verzija
4. **Primjeri PU ne prolaze vlastiti validator** — developeri moraju sami zaključivati što je ispravno
5. **FiskAplikacija ne prikazuje ključne podatke** — TaxPointDate se ne vidi, a bitan je za porezno razdoblje
6. **Posrednici mijenjaju sadržaj XML-a** — kršenje EU Direktive o cjelovitosti
7. **Developer zajednica de facto obavlja QA** za sustav koji je trebao biti gotov mjesecima ranije

---

## 8. Posrednici — MER, FINA, PONDI

### 8.1. Kronologija problema s MER-om

| Datum | Problem | Izvor |
|-------|---------|-------|
| 05.12.2025. | Demo okolina nestabilna — "jedan dan radi ovako, drugi dan onako" | zagimir [#2078](https://www.forum.hr/showpost.php?p=110304143&postcount=2078) |
| 10.12.2025. | API parsanje grešaka "noćna mora" — svaki tip greške ima svoj JSON format | Denis365 [#2170](https://www.forum.hr/showpost.php?p=110357449&postcount=2170) |
| 24.12.2025. | Božić — provjera fiskalizacije vraća random rezultate | tkralj [#2568](https://www.forum.hr/showpost.php?p=110494909&postcount=2568) |
| 01.01.2026. | MPS server FORMAT_ERROR na produkciji | RandomDev321 [#2733](https://www.forum.hr/showpost.php?p=110567877&postcount=2733) |
| 02.01.2026. | UBL errori na produkciji — "Invoice namespace budalastine" | zac1608 [#2760](https://www.forum.hr/showpost.php?p=110574735&postcount=2760) |
| 01.2026. | Računi FINA→MER "nestaju u limbu" — poslani i fiskalizirani ali kod MER-a nema ih | Denis365 [#2885](https://www.forum.hr/showpost.php?p=110620043&postcount=2885) |
| 03.2026. | Korisnici gube pristup bez pojašnjenja — "User does not have rights" | AyV4n [#4636](https://www.forum.hr/showpost.php?p=111477847&postcount=4636) |

### 8.2. MER mijenja XML sadržaj

MER zamjenjuje `ProfileID` u `MojEracunInvoice`, `CustomizationID` u stari format, briše fiskalizacijske podatke i dodaje namespace-ove. Na upit developera, MER odgovara da je to "standardni postupak":

> *"Replacea sa MojEracunInvoice, izbaci moju fiskalizaciju, pobriše mi model iz poziva na broj"*
> — tkralj ([#2966](https://www.forum.hr/showpost.php?p=110636757&postcount=2966))

> MER-ov odgovor: *"napomena da je redovna praksa napraviti traženu izmjenu XML-a obzirom da je to standardni postupak"*
> — tkralj ([#2934](https://www.forum.hr/showpost.php?p=110630439&postcount=2934))

HT d.d. šalje eRačune 02.01.2026. s potpuno starim formatom (`urn:invoice.hr:ubl-2.1-customizations:FinaInvoice`) — 2 dana nakon što je novi format obvezan:
> Denis365 ([#2891](https://www.forum.hr/showpost.php?p=110624017&postcount=2891))

### 8.3. MER lokalni AMS — ručno dodavanje subjekata

MER ne koristi službeni AMS za lookup primatelja, već vlastitu bazu u koju subjekte **ručno dodaje**:

> MER-ov odgovor: subjekte ručno dodaju u svoju bazu. OPG-ovi i novi subjekti ne mogu primiti račune dok ih MER ručno ne doda.
> — AyV4n ([#3093](https://www.forum.hr/showpost.php?p=110664319&postcount=3093))

> *"Delusions of grandeur — na najjače."*
> — ceha ([#3095](https://www.forum.hr/showpost.php?p=110664365&postcount=3095))

### 8.4. Usporedba posrednika

| Aspekt | MER | FINA | PONDI (ePoslovanje) |
|--------|-----|------|---------------------|
| **Dokumentacija** | Na engleskom, šalje se na zahtjev | Kasna, ali kompletna | Odlična, OpenAPI |
| **API kvaliteta** | Kaotičan (random JSON formati) | Kompliciraniji (certifikati) ali konzistentan | "Med i mlijeko" |
| **Validacija** | 2 od 3 validatora ne rade ispravno | Pouzdanija | Konzistentna |
| **Podrška** | Ne odgovaraju na mailove | Spora | Brza, na hrvatskom |
| **Potpis XML-a** | Dodaje svoj, ne dira originalni | Čuva originalni potpis | Gazi originalni potpis |
| **Percepcija developera** | Negativna (~60% diskusije) | Mješovita (~25%) | Pozitivna (~10%) |

> *"EPoslovanje sam riješio unutar 2 radna dana uključujući testiranje. Dokumentacija je odlična, OpenAPI..."*
> — zac1608 ([#2019](https://www.forum.hr/showpost.php?p=110237729&postcount=2019))

### 8.5. Sigurnosni problem — autentifikacija

> *"Kod slanja e-računa... na neki endpoint pošalješ zahtjev u kome je kod MER-a username i password u body-ju... svaki knjigovođa kojem dođe žuta minuta može bilo kome odati te podatke... F2 trebalo izvesti kao i F1, svakom svoj certifikat."*
> — PBDudek ([#2008](https://www.forum.hr/showpost.php?p=110232275&postcount=2008))

### 8.6. Poziv na bojkot (08.01.2026.)

```csharp
throw new Exception("NEMA slanja eRačuna dok se posrednici i država ne dogovore sami sa sobom!
Nemojte me zvati, zovite Marka Primorca. Ja odo na skijanje.");
```
> — Denis365 ([#3097](https://www.forum.hr/showpost.php?p=110664507&postcount=3097))

---

## 9. FiskAplikacija i eIzvještavanje

### 9.1. FiskAplikacija — što prikazuje, a što ne

FiskAplikacija koristi podatke iz **fiskalizacijske SOAP poruke** (EvidentirajERacunZahtjev), ne iz originalnog UBL XML-a. Prikazuje:
- Fiskalizirane račune (izlazne/ulazne)
- Status uparivanja (Uparen/Neuparen/Odstupanje)
- Nefiskalizirane račune
- Greške validacije (G004–G014)

**Ne prikazuje**: TaxPointDate (BT-7), a prikazuje samo ActualDeliveryDate ako je posrednik konvertirao.

**Bug**: Zamjena izdavatelja/primatelja na ekranu:
> *"Izlazni prodavatelj → kupac OK, ulazni obrnuto. Kao da je FINA izokrenula kupca dobavljača u fiskalizacijskoj poruci."*
> — Denis365 ([#2774](https://www.forum.hr/showpost.php?p=110575461&postcount=2774))

### 9.2. eIzvještavanje — kaos 20. u mjesecu

Rok za eIzvještavanje o naplatama je 20. u mjesecu za prethodni mjesec. 20.02.2026. bio je kaos:
- Bulk slanje vraća samo prvu grešku bez broja računa
- CSV limit ~99 zapisa
- Posrednici kasno implementirali API

### 9.3. eIzvještavanje — BT-115 pravilo i parcijalna plaćanja

**Službeno**: Prijavljuje se samo kada je BT-115 (PayableAmount) > 0.

**Problem**: FiskAplikacija odmah označava "Naplaćeno" čim primi BILO KAKVU uplatu (i 50 od 100 EUR). Nema kontrole iznosa — može se poslati i 150.000 EUR za račun od 100 EUR. Nema brisanja, samo "storniranje" negativnim iznosom.

### 9.4. Odbijanje računa — dizajnerski propust

Odbijanje zahtijeva dvostruku radnju (i kod posrednika i u FiskAplikaciji). **Izdavatelj ne zna za odbijanje** ako su na različitim posrednicima — dizajnerski propust u sustavu.

---

## 10. Fiskalizacijska SOAP poruka

### 10.1. Koja UBL polja idu u SOAP poruku

| UBL polje | U SOAP poruci? | Napomena |
|-----------|:--------------:|---------|
| IssueDate (BT-2) | **DA** | Obavezno |
| IssueTime | **DA** | Obavezno za F2 |
| **TaxPointDate (BT-7)** | **NE** | Nema u XSD shemi fiskalizacijske poruke |
| **ActualDeliveryDate (BT-72)** | **DA** | Jedini datum isporuke u fisk. poruci |
| OIB izdavatelja/primatelja | **DA** | — |
| Porezni podaci (stope, iznosi) | **DA** | — |
| KPD klasifikacija | **DA** | — |
| Način plaćanja | **DA** | — |
| Stavke računa | **DA** | — |

### 10.2. F1 vs F2 razlike

| Aspekt | F1 (stari) | F2 (eRačun) |
|--------|-----------|-------------|
| Certifikat | Poslovni (FINA) | Aplikacijski ili poslovni |
| ZKI algoritam | SHA1withRSA | SHA1withRSA (ostalo isto!) |
| OIB operatera | Obavezan | Obavezan od v1.5 (18.12.) |
| Potpis | Software potpisuje | Posrednik potpisuje UBL (SHA256) |

### 10.3. Greške — šifre bez objašnjenja

> Fiskalizacija vraća **praznu šifru greške** — `<SifraGreske></SifraGreske>` — bez ikakve poruke.
> Greška S001 bez detalja — *"Greška prilikom parsiranja UBL računa"* kada je pravi problem nedostupan posrednik primatelja.

---

## 11. Predujam / avans

### 11.1. Ciklus od 3 dokumenta

| Korak | Dokument | Tip | PP | BillingReference | KPD |
|:-----:|----------|:---:|:--:|:----------------:|:---:|
| 1 | Račun za predujam | 386 | P4 | NE | NE |
| 2 | Storno predujma | 386 (neg.) | P10 | DA → korak 1 | NE |
| 3 | Konačni račun | 380 | P1 | DA → korak 2 | DA |

> *"1. Radiš predujam (386) — nema reference; 2. Radiš storno predujma (384) — referenca na predujam; 3. Radiš račun — referenca na storno predujma."*
> — tkralj ([#2146](https://www.forum.hr/showpost.php?p=110351419&postcount=2146))

### 11.2. Konfuzija — PU daje tri različita načina za storno predujma

| Pristup | Tip | Izvor |
|---------|:---:|-------|
| 386 s negativnim iznosima | Invoice | Praksa developera |
| 384 (korektivni račun) | Invoice | PU primjeri |
| 381 (CreditNote) | CreditNote | PU primjeri |

> *"Račun za predujam na PP 386. A storno računa za predujam može i kao odobrenje na 381 ali i kao 384 korektivni račun. Ma bravo!!"*
> — Novi12 ([#2643](https://www.forum.hr/showpost.php?p=110543349&postcount=2643))

**Problem s 384**: Zahtijeva KPD, ali storno predujma ne bi trebao imati KPD. Rješenje: koristiti 386 s negativnim iznosima.

### 11.3. PrepaidAmount na konačnom računu

Iznos predujma na konačnom računu ide u `PrepaidAmount` (BT-113), **ne** u `AllowanceTotalAmount`:
> gecmali ([#2241](https://www.forum.hr/showpost.php?p=110378153&postcount=2241))

---

## 12. Popusti i zaokruživanje

### 12.1. AllowanceCharge — tekst mora biti IDENTIČAN

MER validator testira da tekst razloga oslobođenja u HR raspodjeli i trošku bude **potpuno identičan** — jedan razmak razlike i račun se odbija:

> *"Jedan hebeni RAZMAK"*
> — Denis365/PBDudek ([#2489](https://www.forum.hr/showpost.php?p=110486351&postcount=2489), [#2490](https://www.forum.hr/showpost.php?p=110486547&postcount=2490))

### 12.2. POVNAK + PP + popust = bug u Schematronu

Račun s povratnom naknadom (POVNAK) i porezom na potrošnju (PP) **ne može** imati popust — Schematron baca error:

> *"Kada se doda popust, Schematron baca error U OBA SLUČAJA... mislim da je ovo veliki problem tj. da neki obveznici UOPĆE neće moći izdati račune s tim kombinacijama"*
> — zac1608 ([#2860](https://www.forum.hr/showpost.php?p=110615587&postcount=2860))

### 12.3. PDV izračun — sumarno po stopama, ne po stavkama

Razlika može biti 0.01–0.02 EUR ovisno o pristupu:

> *"Jedini ispravan način za izračun PDV-a je sumarno po tarifnim brojevima (stopama)"*
> — zac1608 ([#2333](https://www.forum.hr/showpost.php?p=110437849&postcount=2333))

Primjer (zoranb [#2343](https://www.forum.hr/showpost.php?p=110438569&postcount=2343)): 6 stavaka s 25% PDV-om — po stavkama = 63.60 EUR, sumarno = 63.62 EUR.

### 12.4. Banker's rounding u MikroERačun

> *"Smrdi mi na banker rounding koji radi po principu half to even: 12.5 => 12, 13.5 => 14"*
> — Denis365 ([#2929](https://www.forum.hr/showpost.php?p=110630141&postcount=2929))

MikroERačun prikazuje 12 EUR umjesto 12.50 EUR!

---

*Analiza provedena 31.03.2026. automatskim scrapingom 2.657 postova (stranice 100–232) i AI kategorizacijom po temama.*

*Skripta za scraping i analizu: [scripts/scrape\_forum.py](https://github.com/dageci/eracun-fiskalizacija-datumi/tree/forum-analysis/scripts/scrape_forum.py)*
