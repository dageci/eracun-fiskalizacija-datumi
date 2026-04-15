---
layout: default
title: "Primjeri — primatelj eRačuna"
has_toc: true
nav_order: 4
---

# Primjeri iz prakse — primatelj eRačuna

Ova stranica pokriva perspektivu **primatelja (kupca)** — kako obraditi primljeni eRačun XML. Za perspektivu izdavatelja (koji XML element staviti) vidi [Primjeri — izdavatelj](primjeri-izdavatelj).

Svaki primjer koristi **isti poslovni slučaj** kao na stranici izdavatelja, ali iz perspektive kupca koji prima eRačun i treba ga proknjižiti.

> Za svaki primjer odgovaramo na tri pitanja:
> 1. **PDV (pretporez)**: U koje razdoblje ide odbitak pretporeza?
> 2. **Trošak/rashod**: U koje razdoblje se priznaje rashod?
> 3. **Skladište**: Kad se knjiži primka? (ako je primjenjivo)

### Sadržaj {#sec-sadrzaj}
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.
</div>

---

## Kako primatelj određuje datume? {#sec-kako-primatelj-odreduje-datume}
Kupac iz primljenog eRačun XML-a treba izvući tri neovisna datuma:

| Pitanje | Gdje gledati u XML-u | Propis |
|---------|----------------------|--------|
| **PDV (pretporez)** — u koje razdoblje ide odbitak? | BT-7 > BT-8 > BT-2 (hijerarhija iz [sekcije 2](pravila#2-ključno-pravilo-br-co-03)) + provjera HR-BT-15 za obračun po naplati | Čl. 57, 60 i 125.i Zakona o PDV-u |
| **Trošak/rashod** — u koje razdoblje se priznaje? | BT-72 (`ActualDeliveryDate`) ili BT-73/BT-74 (`StartDate`/`EndDate`) | HSFI 16, načelo nastanka događaja |
| **Skladište (primka)** — kad se knjiži ulaz robe? | BT-72 (`ActualDeliveryDate`) ili stvarni datum primitka robe | Interna pravila, usklađenje s otpremnicom |

> **Ključni uvid**: Ova tri datuma mogu biti u **različitim mjesecima ili čak godinama** za isti račun. To nije greška — to je normalan rad sustava gdje se PDV, trošak i skladište reguliraju različitim propisima. Detaljno objašnjenje: [sekcija 5 — Datumi na eRačunu vs. datumi u knjigovodstvu](#vremensko-razgraničenje-u-knjigovodstvu).

### Pretporez kod obračuna po naplati — posebna pravila za kupca {#sec-pretporez-kod-obracuna}
Ako primljeni eRačun sadrži `BT-8=432` i/ili `HR-BT-15` (`HRObracunPDVPoNaplati`), to znači da izdavatelj koristi obračun po naplaćenoj naknadi (čl. 125.i). Za kupca to ima **direktnu posljedicu**:

> **Čl. 125.i, st. 3 Zakona o PDV-u**: Kupac koji prima račun od obveznika koji obračunava PDV po naplaćenoj naknadi, **pravo na odbitak pretporeza ima tek u trenutku kad plati račun**, ne u trenutku primitka računa.

To znači da kupac mora pratiti:
1. Datum primitka eRačuna (za evidenciju)
2. **Datum plaćanja** (za pretporez) — ovo je datum koji određuje PDV razdoblje

> **PU pojašnjenje (19.12.2025., pitanje 17)**: Zakon o fiskalizaciji ne propisuje rok za prihvat (likvidaturu) računa, već propisuje rok za **fiskalizaciju zaprimanja** — 5 radnih dana od primitka. Ako nakon fiskalizacije zaprimanja tijekom likvidature dođe do potrebe odbijanja, o tome se izvještava Poreznu upravu do zadnjeg dana u mjesecu za prethodni mjesec.

---

## P.1 Obračun po izdavanju (čl. 30) <span class="badge-izdavanje">Po izdavanju</span> {#sec-p1-obracun-po}
### P.1.1 Isporuka i račun isti dan {#sec-p11-isporuka-i-dan}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.1](primjeri-izdavatelj#411-isporuka-i-račun-isti-dan-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 15.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 15.03.2026. | BT-72 (`cbc:ActualDeliveryDate`) — ili nema jer je isti kao BT-2 |
| Datum primitka eRačuna | 15.03.2026. | Posrednik isporučio isti dan |
| BT-7 / BT-8 | Nema — default = BT-2 | — |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Ožujak 2026.** | **Ožujak 2026.** | **15.03.2026.** |

> **Najjednostavniji slučaj** — svi datumi su u istom mjesecu. Pretporez, rashod i primka idu u ožujak. Nema BT-7 ni BT-8, pa je datum porezne obveze = BT-2 = 15.03. Kupac je primio račun isti dan, obveza PDV-a je nastala, oba uvjeta za pretporez su ispunjena (čl. 57 + čl. 60). HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.2 Isporuka u drugom mjesecu od računa {#sec-p12-isporuka-u}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.2](primjeri-izdavatelj#412-isporuka-u-drugom-mjesecu-od-računa-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 05.04.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 28.03.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 28.03.2026. | BT-7 (`cbc:TaxPointDate`) |
| Datum primitka eRačuna | 05.04.2026. | Posrednik isporučio isti dan kad je izdan |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Ožujak 2026.** | **Ožujak 2026.** | **28.03.2026.** |

> **Pretporez ide u ožujak**, ne u travanj! Obveza PDV-a nastala je 28.03. (BT-7 = datum isporuke). Kupac je primio račun 05.04., ali rok za PDV prijavu za ožujak je 30.04.2026. — budući da je račun stigao **prije roka**, kupac može uključiti pretporez u prijavu za ožujak (čl. 57 + čl. 60, vidi [sekciju 5.3](#pretporez-dva-uvjeta-i-nijanse-u-praksi)), potvrđeno presudom [C-80/20 (Wilo Salmson)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun).
>
> Rashod se također priznaje u ožujku po BT-72 (datum isporuke = datum nastanka poslovnog događaja, HSFI 16). HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.3 Račun izdan prije isporuke (čl. 30 st. 2) {#sec-p13-racun-izdan-2}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.3](primjeri-izdavatelj#413-račun-izdan-prije-isporuke-čl-30-st-2-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 25.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 05.04.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum primitka eRačuna | 25.03.2026. | Posrednik isporučio isti dan |
| BT-7 / BT-8 | Nema — default = BT-2 | Po čl. 30 st. 2 |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Ožujak 2026.** | **Travanj 2026.** | **05.04.2026.** |

> **Pretporez i rashod su u RAZLIČITIM mjesecima!** Ovo je čest izvor zabune.
>
> - **Pretporez: ožujak** — nema BT-7 ni BT-8, pa je datum porezne obveze = BT-2 = 25.03. (čl. 30 st. 2: ako je račun izdan prije isporuke, PDV obveza nastaje danom izdavanja). Kupac je primio račun u ožujku, oba uvjeta ispunjena.
> - **Rashod: travanj** — rashod se priznaje po načelu nastanka događaja (HSFI 16), a roba je stvarno isporučena 05.04. (BT-72). Trošak pripada travnju bez obzira na datum računa.
> - **Primka: 05.04.** — roba fizički stiže u skladište 05.04., tada se knjiži primka.
>
> **Za ERP sustav**: automatsko knjiženje mora razdvojiti PDV datum (BT-2 = 25.03.) od datuma rashoda (BT-72 = 05.04.). HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.4 Predujam / avansni račun (čl. 30 st. 5) {#sec-p14-predujam-avansni-5}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.4](primjeri-izdavatelj#414-predujam-avansni-račun-čl-30-st-5-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 10.02.2026. | BT-2 (`cbc:IssueDate`) |
| Datum primitka predujma | 05.02.2026. | BT-7 (`cbc:TaxPointDate`) |
| Vrsta dokumenta | 386 (predujam) | `cbc:InvoiceTypeCode` |
| Datum primitka eRačuna | 10.02.2026. | Posrednik isporučio isti dan |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Veljača 2026.** | **NE priznaje se** | **Nema primke** |

> **Predujam nije trošak** — to je dano sredstvo (potraživanje). Rashod se priznaje tek kad roba bude isporučena ili usluga obavljena (u budućnosti, kad dođe konačni račun).
>
> - **Pretporez: veljača** — BT-7 = 05.02. (datum primitka predujma), račun primljen 10.02., oba uvjeta ispunjena.
> - **Rashod**: ne priznaje se — predujam se knjiži kao dano sredstvo (aktiva), ne kao trošak. Tek po isporuci (konačni račun) se prebacuje u rashod.
> - **Primka**: nema — roba još nije stigla.
>
> **Prepoznavanje predujma u XML-u**: `InvoiceTypeCode = 386` i nepostojanje BT-72 (`ActualDeliveryDate`). HR-BT-15 nije prisutan (obračun po izdavanju).
>
> **Kompletni ciklus predujma**: Ovo je samo **prvi korak** iz perspektive primatelja. Kad isporuka bude obavljena, primatelj će zaprimiti storno predujma + konačni račun — tek tada prizna rashod i knjži primku. Detaljan prikaz: [Naknadno dospjeli računi — predujam](naknadno-dospjeli-racuni#12-predujam-iz-2025-konačni-račun-2026).

---

### P.1.5 Kontinuirana usluga — obračunsko razdoblje (BT-73/BT-74) {#sec-p15-kontinuirana-usluga-73}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.5](primjeri-izdavatelj#415-kontinuirana-usluga--obračunsko-razdoblje-bt-73-bt-74-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 05.04.2026. | BT-2 (`cbc:IssueDate`) |
| Početak obračunskog razdoblja | 01.01.2026. | BT-73 (`cbc:StartDate`) |
| Kraj obračunskog razdoblja | 31.03.2026. | BT-74 (`cbc:EndDate`) |
| Datum nastanka obveze PDV-a | 31.03.2026. | BT-7 (`cbc:TaxPointDate`) |
| Datum primitka eRačuna | 05.04.2026. | Posrednik isporučio isti dan |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Ožujak 2026.** | **Q1 (sij-ožu) — vremensko razgraničenje** | **Nema — usluga, ne roba** |

> **Rashod se raspodjeluje na cijelo razdoblje**, ne na mjesec računa!
>
> - **Pretporez: ožujak** — BT-7 = 31.03. (kraj razdoblja = datum nastanka obveze po čl. 30 st. 2). Račun stigao 05.04., ali rok za PDV prijavu za ožujak je 30.04. — kupac može uključiti pretporez u prijavu za ožujak ([C-80/20 Wilo Salmson](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun)).
> - **Rashod: vremensko razgraničenje** — usluga je trajala od 01.01. do 31.03. (BT-73/BT-74). Prema HSFI 16, trošak se priznaje u razdoblju kad je usluga obavljena. Ukupni iznos se raspodjeljuje na siječanj, veljaču i ožujak (1/3 + 1/3 + 1/3) ili prema drugoj prikladnoj metodi.
> - **Primka**: nema — ovo je usluga, ne fizička roba.
>
> **Za ERP sustav**: BT-73/BT-74 daju informaciju za automatsko vremensko razgraničenje troškova. Bez tih polja, ERP bi trošak knjižio u mjesec računa (travanj) — što bi bilo krivo. HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.6 BT-8=35 — automatska veza na datum isporuke {#sec-p16-bt-835}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.6](primjeri-izdavatelj#416-bt-835--automatska-veza-na-datum-isporuke-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 10.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 25.01.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Kod datuma PDV obveze | 35 | BT-8 (`cbc:DescriptionCode`) |
| Datum primitka eRačuna | 10.03.2026. | Posrednik isporučio isti dan |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Siječanj 2026.** | **Siječanj 2026.** | **25.01.2026.** |

> **BT-8=35 znači: datum porezne obveze = BT-72 (datum isporuke).**
>
> - **Pretporez: siječanj** — BT-8=35 upućuje sustav da koristi BT-72 = 25.01. Račun je stigao 10.03. — ali rok za PDV prijavu za siječanj je bio 28.02. Ako je taj rok **već prošao**, pretporez ide u **ožujak** (razdoblje primitka računa), ne u siječanj! Vidi [sekciju 5.3](#pretporez-dva-uvjeta-i-nijanse-u-praksi). Napomena: prema [C-80/20 (Wilo Salmson)](#sudska-praksa-eu--pravo-na-odbitak-i-račun), obveznik ima pravo podnijeti ispravak prijave za siječanj.
> - **Rashod: siječanj** — BT-72 = 25.01., roba je isporučena u siječnju.
>
> **Važno za primatelja**: Kad je BT-8=35, primatelj NE treba tražiti BT-7 — datum poreza se automatski čita iz BT-72. Rezultat je isti kao kad izdavatelj koristi BT-7 eksplicitno (primjer P.1.2), samo je mehanizam drugačiji. HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.7 Odobrenje / CreditNote {#sec-p17-odobrenje-creditnote}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.7](primjeri-izdavatelj#417-odobrenje--creditnote-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja odobrenja | 10.04.2026. | BT-2 (`cbc:IssueDate`) |
| Referenca na izvorni račun | 147/1/1 | BT-25 (`cbc:ID` u `BillingReference`) |
| Datum izvornog računa | 15.03.2026. | BT-26 (`cbc:IssueDate` u `BillingReference`) |
| Vrsta dokumenta | 381 (odobrenje) | `cbc:CreditNoteTypeCode` |

**Knjiženje kod primatelja:**

| PDV (pretporez) — ispravak | Trošak/rashod — ispravak | Skladište |
|:---:|:---:|:---:|
| **Travanj 2026.** | **Travanj 2026.** | Ovisi o vrsti odobrenja |

> **Pretporez:** Ispravak pretporeza se u praksi najčešće knjži u mjesecu primitka odobrenja (**travanj**). Međutim, prema pravomoćnoj presudi ECJ [C-518/14 (Senatex)](#sudska-praksa-eu--pravo-na-odbitak-i-račun), porezni obveznik **ima pravo** na retroaktivni ispravak u mjesecu izvornog računa (**ožujak**) — i država mu to ne smije uskratiti. Obveznik bira pristup. HR-BT-15 nije prisutan (obračun po izdavanju).
>
> - **Pretporez: travanj** (u praksi) ili retroaktivno u ožujak (Senatex pravo). Kupac je u ožujku odbio pretporez za puni iznos izvornog računa. CreditNote u travnju **umanjuje** taj pretporez za iznos odobrenja — to je negativni pretporez (ne novi pretporez, nego korekcija starog).
> - **Rashod: travanj** — ispravak rashoda se također knjiži u travnju (datum primitka odobrenja). Rashod iz ožujka se umanjuje za iznos odobrenja.
> - **Skladište**: Ako se radi o povratu robe, kupac knjiži izdatnicu (izlaz iz skladišta). Ako je odobrenje za popust/razliku u cijeni, nema skladišnog prometa.
>
> **Prepoznavanje u XML-u**: Korijen dokumenta je `<CreditNote>`, ne `<Invoice>`, i tip je 381. HR-BT-15 nije prisutan (obračun po izdavanju).

---

### P.1.8 Svi datumi u različitim mjesecima — BT-7 eksplicitni datum {#sec-p18-svi-datumi}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.8](primjeri-izdavatelj#418-svi-datumi-u-različitim-mjesecima--bt-7-eksplicitni-datum-po-izdavanju)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 10.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 25.01.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 25.01.2026. | BT-7 (`cbc:TaxPointDate`) |
| Datum primitka eRačuna | 10.03.2026. | Posrednik isporučio isti dan |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Siječanj ili ožujak 2026.** | **Siječanj 2026.** | **25.01.2026.** |

> **Svi datumi u različitim mjesecima** — ovo je najsloženiji slučaj za primatelja.
>
> - **Pretporez**: Obveza PDV-a nastala u siječnju (BT-7 = 25.01.), ali račun je stigao tek u ožujku. Rok za PDV prijavu za siječanj bio je 28.02. — taj rok je **prošao**. Kupac prema praksi Porezne uprave može pretporez uključiti tek u prijavu za **ožujak** (mjesec primitka računa). Vidi detaljno [sekciju 5.3](#pretporez-dva-uvjeta-i-nijanse-u-praksi). Prema [C-80/20 (Wilo Salmson)](#sudska-praksa-eu--pravo-na-odbitak-i-račun), obveznik ima pravo podnijeti ispravak prijave za siječanj.
> - **Rashod: siječanj** — BT-72 = 25.01., roba je isporučena u siječnju. Po HSFI 16, trošak pripada siječnju.
> - **Primka: 25.01.** — roba je fizički zaprimljena u siječnju.
>
> **Za ERP sustav**: ovo zahtijeva **tri različita datuma** u istom dokumentu — PDV u ožujku, rashod u siječnju, primka 25.01. Automatsko knjiženje mora sve tri razlikovati. HR-BT-15 nije prisutan (obračun po izdavanju).

---

## P.2 Obračun po naplaćenoj naknadi (čl. 125.i) <span class="badge-naplata">Po naplati</span> {#sec-p2-obracun-po}
### P.2.1 Isporuka i račun isti mjesec {#sec-p21-isporuka-i}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.1](primjeri-izdavatelj#421-isporuka-i-račun-isti-mjesec-po-naplati)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 20.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 10.03.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Kod datuma PDV obveze | 432 | BT-8 (`cbc:DescriptionCode`) |
| HR-BT-15 | "Obračun prema naplaćenoj naknadi" | `hrextac:HRObracunPDVPoNaplati` |
| Datum primitka eRačuna | 20.03.2026. | Posrednik isporučio isti dan |
| **Datum plaćanja** | **15.05.2026.** | Kupac plaća 15.05. |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **MAJ 2026.** — tek kad plati! | **Ožujak 2026.** | **10.03.2026.** |

> **Rashod i pretporez su u RAZLIČITIM mjesecima!** Ovo je najčešća zabuna kod obračuna po naplati.
>
> - **Pretporez: MAJ** — čl. 125.i st. 3 Zakona o PDV-u kaže da kupac pravo na odbitak pretporeza ima **tek kad plati račun**. Kupac plaća 15.05. → pretporez ide u PDV prijavu za **MAJ**.
> - **Rashod: ožujak** — rashod se priznaje po načelu nastanka događaja (HSFI 16). Roba je isporučena 10.03. (BT-72) → trošak pripada ožujku, neovisno o tome kad je račun plaćen.
> - **Primka: 10.03.** — roba je fizički zaprimljena 10.03.
>
> **Kako prepoznati obračun po naplati u XML-u**: Tražiti `BT-8=432` (`DescriptionCode`) i/ili `HR-BT-15` (`HRObracunPDVPoNaplati`). Ako su prisutni, kupac **mora pratiti datum plaćanja** za pretporez.

---

### P.2.2 Isporuka u drugom mjesecu od računa {#sec-p22-isporuka-u}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.2](primjeri-izdavatelj#422-isporuka-u-drugom-mjesecu-od-računa-po-naplati)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 10.03.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 25.01.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Kod datuma PDV obveze | 432 | BT-8 (`cbc:DescriptionCode`) |
| HR-BT-15 | "Obračun prema naplaćenoj naknadi" | `hrextac:HRObracunPDVPoNaplati` |
| **Datum plaćanja** | **15.04.2026.** | Kupac plaća 15.04. |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Travanj 2026.** — tek kad plati! | **Siječanj 2026.** | **25.01.2026.** |

> **Tri različita mjeseca** — pretporez u travnju, rashod u siječnju, račun izdan u ožujku.
>
> Kod obračuna po naplati, ni datum izdavanja (BT-2) ni datum isporuke (BT-72) ne utječu na PDV. Jedino što određuje pretporez je **datum plaćanja**. Rashod se i dalje priznaje po datumu isporuke (BT-72 = 25.01.).

---

### P.2.3 Predujam / avansni račun {#sec-p23-predujam-avansni-racun}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.4](primjeri-izdavatelj#424-predujam-avansni-račun-po-naplati)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja računa | 10.02.2026. | BT-2 (`cbc:IssueDate`) |
| Datum primitka predujma | 05.02.2026. | BT-7 (`cbc:TaxPointDate`) |
| HR-BT-15 | "Obračun prema naplaćenoj naknadi" | `hrextac:HRObracunPDVPoNaplati` |
| Vrsta dokumenta | 386 (predujam) | `cbc:InvoiceTypeCode` |

**Knjiženje kod primatelja:**

| PDV (pretporez) | Trošak/rashod | Skladište (primka) |
|:---:|:---:|:---:|
| **Veljača 2026.** | **NE priznaje se** | **Nema primke** |

> **Predujam kod obračuna po naplati** — jedini slučaj gdje je BT-7 prisutan uz HR-BT-15.
>
> - **Pretporez: veljača** — kupac je **već platio** (05.02.), stoga je uvjet iz čl. 125.i st. 3 odmah ispunjen. BT-7 = 05.02. Nema čekanja na plaćanje jer je predujam po definiciji plaćanje unaprijed.
> - **Rashod**: ne priznaje se — isto kao kod P.1.4, predujam je dano sredstvo.
> - **Primka**: nema — roba još nije stigla.
>
> **Kako prepoznati u XML-u**: Prisutan je **BT-7** (ne BT-8=432!) jer je datum plaćanja poznat. Ali **HR-BT-15 je također prisutan** jer je to svojstvo obveznika, ne pojedinačnog računa. Ovo je jedini primjer obračuna po naplati koji koristi BT-7 umjesto BT-8=432.
>
> **Kompletni ciklus predujma**: Ovo je samo **prvi korak**. Kad isporuka bude obavljena, primatelj će zaprimiti storno predujma + konačni račun (oba s HR-BT-15). Detaljan prikaz: [Naknadno dospjeli računi — predujam](naknadno-dospjeli-racuni#12-predujam-iz-2025-konačni-račun-2026).

---

### P.2.4 Odobrenje / CreditNote {#sec-p24-odobrenje-creditnote}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.6](primjeri-izdavatelj#426-odobrenje--creditnote-po-naplati)

| Podatak | Vrijednost | Izvor u XML-u |
|---------|-----------|---------------|
| Datum izdavanja odobrenja | 10.04.2026. | BT-2 (`cbc:IssueDate`) |
| Referenca na izvorni račun | 147/1/1 | BT-25 (`cbc:ID` u `BillingReference`) |
| Datum izvornog računa | 15.03.2026. | BT-26 (`cbc:IssueDate` u `BillingReference`) |
| HR-BT-15 | "Obračun prema naplaćenoj naknadi" | `hrextac:HRObracunPDVPoNaplati` |
| Vrsta dokumenta | 381 (odobrenje) | `cbc:CreditNoteTypeCode` |

**Knjiženje kod primatelja:**

| PDV (pretporez) — ispravak | Trošak/rashod — ispravak | Skladište |
|:---:|:---:|:---:|
| **Travanj 2026.** | **Travanj 2026.** | Ovisi o vrsti odobrenja |

> **Primatelj prima CreditNote od obveznika na sustavu po naplati** — treba stornirati dio pretporeza.
>
> - **Pretporez: travanj** (u praksi) ili retroaktivno u mjesec izvornog pretporeza (prema [Senatex C-518/14](#sudska-praksa-eu--pravo-na-odbitak-i-račun)). Obveznik bira pristup. CreditNote **umanjuje** prethodno odbijeni pretporez — to je negativni pretporez, ne novi.
> - **Rashod: travanj** — korekcija rashoda u mjesecu primitka. Rashod iz izvornog razdoblja se umanjuje.
> - **HR-BT-15 je prisutan** i u CreditNote jer je to svojstvo obveznika — primatelj iz njega zna da je riječ o obračunu po naplati.
>
> **Senatex pojašnjenje**: Prema pravomoćnoj presudi ECJ [C-518/14 (Senatex)](#sudska-praksa-eu--pravo-na-odbitak-i-račun), ako je izvorni račun već plaćen i pretporez odbijen u ranijem mjesecu, obveznik **ima pravo** na retroaktivni ispravak u tom ranijem mjesecu. U praksi se najčešće radi u mjesecu primitka odobrenja jer je jednostavnije (bez ispravka PDV prijave za ranije razdoblje), ali obje opcije su legalne.

---

## Sažetak — algoritam za primatelja {#sec-sazetak-algoritam-za-primatelja}
Za automatsko knjiženje primljenog eRačuna, ERP sustav treba izvršiti sljedeće korake:

### Korak 1: Odredi datum nastanka porezne obveze {#sec-korak-1-odredi}
```
AKO postoji HR-BT-15 (HRObracunPDVPoNaplati):
  → režim = "po naplati", datum_poreza = datum_plaćanja (čl. 125.i)
  → IZUZETAK: predujam (InvoiceTypeCode=386) → datum_poreza = BT-7
INAČE AKO postoji BT-7 (TaxPointDate)     → datum_poreza = BT-7
INAČE AKO postoji BT-8:
  AKO BT-8 = 3                      → datum_poreza = BT-2 (IssueDate)
  AKO BT-8 = 35                     → datum_poreza = BT-72 (ActualDeliveryDate)
  AKO BT-8 = 432                    → datum_poreza = datum_plaćanja (ovo bi trebalo
                                       biti pokriveno HR-BT-15 gore)
INAČE                                → datum_poreza = BT-2 (IssueDate)
```

### Korak 2: Odredi pretporez {#sec-korak-2-odredi-pretporez}
```
AKO BT-8 = 432 ILI postoji HR-BT-15:
  → pretporez = mjesec u kojem kupac PLATI račun (čl. 125.i st. 3)
  → IZUZETAK: predujam (InvoiceTypeCode=386) → pretporez = BT-7
INAČE:
  → pretporez = mjesec datum_poreza iz Koraka 1
  → ALI: samo ako je račun primljen PRIJE roka za PDV prijavu tog mjeseca
  → AKO je rok prošao → pretporez = mjesec primitka računa
  →   (ALI: prema C-80/20 Wilo Salmson, obveznik MOŽE podnijeti ispravak prijave za izvorni mjesec)
```

### Korak 3: Odredi rashod {#sec-korak-3-odredi-rashod}
```
AKO postoji BT-72 (ActualDeliveryDate):
  → rashod = mjesec BT-72
AKO postoji BT-73/BT-74 (obračunsko razdoblje):
  → rashod = raspodijeli na BT-73 do BT-74 (vremensko razgraničenje)
AKO je predujam (InvoiceTypeCode=386):
  → rashod se NE priznaje (dano sredstvo)
AKO je CreditNote:
  → ispravak rashoda = mjesec primitka odobrenja
INAČE:
  → rashod = mjesec BT-2 (IssueDate) kao zamjena
```

### Korak 4: Odredi primku (ako je roba) {#sec-korak-4-odredi}
```
AKO postoji BT-72 I radi se o robi (ne usluzi):
  → primka = BT-72
AKO je predujam (InvoiceTypeCode=386):
  → nema primke
AKO je CreditNote s povratom robe:
  → izdatnica (izlaz iz skladišta) = datum primitka odobrenja
```

---

## Pretporez: dva uvjeta i nijanse u praksi {#sec-pretporez-dva-uvjeta}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Pravo na odbitak pretporeza kod obračuna po izdavanju reguliraju **dva članka** koji se nadopunjuju:

**Čl. 57, st. 1** (nastanak prava):
> *"Pravo na odbitak PDV-a (pretporeza) nastaje u trenutku kad nastane obveza obračuna PDV-a koji se može odbiti."*

Dakle **pravo nastaje** u trenutku isporuke (npr. prosinac 2025.).

**Čl. 60, st. 1, točka b)** (uvjet za ostvarivanje prava):
> *"...ima račun u vezi s isporukom dobara i usluga, izdan u skladu s odredbama članaka 78., 79., 80. i 81."*

Dakle za **ostvarivanje** tog prava kupac mora **imati račun**.

### Što znači "ima račun"? {#sec-sto-znaci-ima-racun}
"Ima račun" ne znači datum izdavanja računa (BT-2), nego datum kad kupac **stvarno ima račun** — kad ga primi u svoj sustav. Kod eRačuna to je trenutak kad posrednik isporuči XML kupcu; kod papirnog računa to je dan kad stigne poštom.

EU Direktiva 2006/112/EC koristi izraz **"hold an invoice"** (čl. 178) — "posjedovati račun", ne "kad je račun izdan".

### U koje razdoblje ide pretporez? {#sec-u-koje-razdoblje}
Prema praksi Porezne uprave, pravilo ovisi o tome **kad je račun stigao u odnosu na rok za PDV prijavu** (od 01.01.2026. rok je do **zadnjeg dana u mjesecu** za prethodni mjesec):

| Kad je račun stigao | Pretporez ide u | Primjer |
|---|---|---|
| **Prije roka** za PDV prijavu za mjesec isporuke | Razdoblje **isporuke** | Isporuka 15.12.2025., eRačun stigao 10.01.2026. (rok za prosinac: 31.01.2026.) → pretporez u **prosincu 2025.** |
| **Nakon roka** za PDV prijavu za mjesec isporuke | Razdoblje **primitka računa** | Isporuka 15.12.2025., račun stigao 05.02.2026. (rok za prosinac već prošao) → pretporez u **veljači 2026.** |

> \* Prema [C-80/20 (Wilo Salmson)](#sudska-praksa-eu--pravo-na-odbitak-i-račun), obveznik ima pravo podnijeti ispravak PDV prijave za mjesec isporuke čak i ako je rok prošao — PU mu to ne smije uskratiti.

### eRačun ovo praktički eliminira {#sec-eracun-ovo-prakticki-eliminira}
Kod eRačuna dostava se mjeri u sekundama/minutama. Izdavatelj kreira račun → posrednik ga odmah isporučuje kupcu. Razlika između datuma izdavanja i datuma primitka je zanemariva — uvijek unutar istog dana, uvijek unutar roka za PDV prijavu.

To znači da kod eRačuna pretporez u praksi **uvijek ide u razdoblje kad je nastala obveza PDV-a** — što je upravo ono što čl. 57 namjerava. Razdvajanje se događa samo kod zakašnjelih papirnih računa ili kad izdavatelj kasni s izdavanjem.

### Sudska praksa EU — pravo na odbitak i račun {#sec-sudska-praksa-eu}
Pred Europskim sudom pravde (CJEU) vodi se postupak **C-167/26** (revizija predmeta T-689/24) koji se bavi upravo ovim pitanjem.

**Što se dogodilo:** Opći sud EU (General Court) donio je 11. veljače 2026. presudu u predmetu **T-689/24** (I. S.A. protiv Dyrektora Krajowej Informacji Skarbowej, Poljska) u kojoj je utvrdio:

- "Hold an invoice" iz čl. 178(a) Direktive o PDV-u je **formalni uvjet** za **ostvarivanje** prava na odbitak
- Ali **nije uvjet** za **nastanak** tog prava (nastanak je po čl. 167 = kad nastane obveza obračuna)
- Odgoda odbitka pretporeza samo zato što račun još nije primljen tijekom poreznog razdoblja **krši načelo neutralnosti PDV-a**, pod uvjetom da je račun primljen prije podnošenja PDV prijave za to razdoblje

**Što se sada događa:** Prvi opći odvjetnik (First Advocate General) pokrenuo je 14. ožujka 2026. postupak revizije pred Velikim vijećem ECJ-a (predmet **C-167/26 RX**). ECJ će ocijeniti može li presuda Općeg suda ugroziti koherentnost prava EU-a u području PDV-a, posebno tumačenje čl. 167, 168(a) i 178(a).

**Status (ožujak 2026.):** Postupak revizije je u ranoj fazi. **Konačna odluka nije donesena.** Ako ECJ potvrdi tumačenje Općeg suda, to bi moglo značiti da kupac ima pravo na pretporez **odmah kad nastane obveza** (prosinac), neovisno o tome kad primi račun — pod uvjetom da ga primi prije roka za PDV prijavu.

**Zašto je ovo važno za eRačun:** Ako presuda postane pravomoćna, razdvajanje pretporeza između razdoblja (sekcija iznad) postaje irelevantno za eRačune jer se eRačun dostavlja u sekundama — uvijek prije roka za PDV prijavu.

Izvor: <a href="https://www.vatupdate.com/2026/03/14/ecj-c-167-26-ecj-cjeu-will-review-case-egc-case-t-689-24-rx-vat-deduction-invoice-timing/" target="_blank">VATupdate — ECJ C-167/26 review</a>, <a href="https://www.vatupdate.com/2026/02/16/comments-on-ecg-t-689-24-confirms-incompatibility-of-polish-input-vat-deduction-rules-with-eu-law/" target="_blank">VATupdate — T-689/24 presuda</a>

**Relevantne pravomoćne presude:**

- **<a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62014CJ0518" target="_blank">C-518/14 (Senatex), 15.09.2016.</a>** — Senatex GmbH protiv Finanzamt Hannover-Nord (Njemačka). Ispravak računa ima **retroaktivan učinak** — pretporez se može odbiti za razdoblje u kojem je račun **izvorno izdan**, ne samo u razdoblju ispravka. EU pravo zabranjuje nacionalno zakonodavstvo koje sprječava retroaktivnu primjenu ispravaka računa.

  > **Što to znači u praksi:** Senatex daje poreznom obvezniku **pravo** (ne obvezu) na retroaktivni ispravak pretporeza. Država mu to **ne smije uskratiti**, ali on ne mora koristiti to pravo. U praksi postoje dva pristupa:
  >
  > | Pristup | Što radi | Posljedica | Temelj |
  > |---|---|---|---|
  > | **Retroaktivno** | Ispravak pretporeza u mjesecu **izvornog računa** | Ispravak (zamjenska) PDV prijave za to razdoblje putem ePorezna | Senatex C-518/14 — pravo obveznika |
  > | **Tekuće razdoblje** | Ispravak pretporeza u mjesecu **primitka odobrenja** | Bez ispravka ranije prijave, jednostavnije | Uobičajena praksa (čl. 33 st. 7 ZPDV dopušta odbitak u kasnijem razdoblju) |
  >
  > Obje opcije su legalne. Senatex samo kaže da država ne smije **zabraniti** retroaktivni pristup — ne kaže da je obvezan. Kod eRačuna, ispravci (CreditNote 381, korekcija 384) referenciraju izvorni račun putem BT-25/BT-26, što omogućuje automatsko povezivanje s izvornim razdobljem.

- **<a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:62020CJ0080" target="_blank">C-80/20 (Wilo Salmson France), 21.10.2021.</a>** — Wilo Salmson France SAS protiv ANAF (Rumunjska). EU pravo zabranjuje odbijanje povrata PDV-a u određenom razdoblju samo zato što je PDV dospio u ranijem razdoblju, a račun izdan u kasnijem. Poništenje i ponovna izdaja računa ne mijenja razdoblje za koje se može zatražiti povrat.

  > **Što to znači u praksi:** Usluga obavljena u prosincu, račun izdan u veljači. Porezna uprava ne smije reći "PDV je dospio u prosincu, ali račun je iz veljače, pa ne možete tražiti povrat za prosinac." Pravo na povrat slijedi poreznu obvezu (prosinac), ne datum računa. Ovo potvrđuje da je **BT-7 (datum porezne obveze) ključan** — ne BT-2 (datum izdavanja).

---

## Vremensko razgraničenje u knjigovodstvu {#sec-vremensko-razgranicenje-u-knjigovodstvu}
> Kad knjigovođa kaže *"ide u trošak za prošlu godinu"* — misli da je usluga obavljena u
> prošloj godini pa rashod pripada tamo (HSFI 16), čak i ako je račun stigao u siječnju
> nove godine. To se zove **vremensko razgraničenje**.
>
> Vremensko razgraničenje se rješava **interno u knjigovodstvu**, ne kroz eRačun XML.
> Ali eRačun XML **pomaže**: BT-72 (datum isporuke) i BT-73/BT-74 (razdoblje) daju
> knjigovođi/ERP sustavu informaciju potrebnu za automatsko razgraničenje — u koje
> razdoblje pripada trošak, neovisno o tome kad je račun stigao.
>
> Svih pet stavki iz primjera iznad mogu biti u **različitim mjesecima ili čak godinama** za isti poslovni događaj. To nije greška — to je normalan rad sustava gdje se PDV, trošak i porez na dobit reguliraju različitim propisima.

### BT-72 (datum isporuke) — utjecaj na trošak, prihod i skladište {#sec-bt-72-datum-sk}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Scenarij | BT-2 (račun) | BT-72 (isporuka) | Prihod (izdavatelj) | Rashod (primatelj) | Primka/Otpremnica | PDV |
|---|---|---|---|---|---|---|
| Isti dan | 15.03. | 15.03. | Ožujak | Ožujak | 15.03. | Ožujak |
| Račun nakon isporuke | 05.04. | 28.03. | **Ožujak** (HSFI 15 — po isporuci) | **Ožujak** (HSFI 16 — po nastanku) | 28.03. | Ožujak (BT-7) |
| Račun prije isporuke | 25.03. | 05.04. | **Travanj** (isporuka tek u 04) | **Travanj** (roba tek u 04) | 05.04. | Ožujak (default=BT-2 (bez BT-7), čl. 30 st. 2) |
| Bez BT-72 (usluga) | 05.04. | — | Prema BT-7 ili BT-2 | Prema BT-7 ili BT-2 | — (usluga) | BT-7 ili BT-2 |

> **Ključni uvid**: BT-72 je ključan za **knjiženje troška/prihoda i skladišno poslovanje** neovisno o PDV tretmanu. Čak i kad je PDV u jednom mjesecu (BT-7), trošak/prihod i primka mogu biti u drugom (BT-72). ERP sustavi koji automatski učitavaju eRačune moraju razdvojiti ove dvije logike.

### BT-73/BT-74 (obračunsko razdoblje) — razgraničenje troškova {#sec-bt-73bt-74}
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

| Scenarij | BT-2 | BT-73 | BT-74 | Račun za | Trošak primatelja | Prihod izdavatelja |
|---|---|---|---|---|---|---|
| Mjesečni najam | 05.04. | 01.03. | 31.03. | Najam za ožujak | **Ožujak** (razgraničenje) | **Ožujak** |
| Kvartalna usluga | 05.04. | 01.01. | 31.03. | IT podrška Q1 | **Raspodijeliti na 01-03** | **Raspodijeliti na 01-03** |
| Godišnja pretplata | 15.01. | 01.01. | 31.12. | Softver licence 2026 | **Raspodijeliti na 01-12** | **Raspodijeliti na 01-12** |

> **Ključni uvid**: BT-73/BT-74 daju ERP sustavu informaciju za **automatsko vremensko razgraničenje**. Bez tih polja, računovođa mora ručno rasporediti trošak po mjesecima. S njima, ERP može automatski knjižiti 1/3 troška u svaki mjesec kvartala (ili 1/12 za godišnju pretplatu).
>
> **Napomena**: BT-73/BT-74 **ne utječu na PDV** — PDV se određuje kroz BT-7/BT-8/BT-2. Obračunsko razdoblje je isključivo informativno za knjigovodstvene svrhe.

---

## Usporedna tablica svih primjera {#sec-usporedna-tablica-svih-primjera}
| Primjer | Način obračuna | HR-BT-15 | Datum računa | Datum isporuke | Datum plaćanja | Pretporez | Rashod | Primka |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **P.1.1** | <span class="badge-izdavanje">Izdavanje</span> | — | 15.03. | 15.03. | — | Ožujak | Ožujak | 15.03. |
| **P.1.2** | <span class="badge-izdavanje">Izdavanje</span> | — | 05.04. | 28.03. | — | Ožujak | Ožujak | 28.03. |
| **P.1.3** | <span class="badge-izdavanje">Izdavanje</span> | — | 25.03. | 05.04. | — | Ožujak | **Travanj** | 05.04. |
| **P.1.4** | <span class="badge-izdavanje">Izdavanje</span> | — | 10.02. | — | 05.02. | Veljača | — | — |
| **P.1.5** | <span class="badge-izdavanje">Izdavanje</span> | — | 05.04. | — | — | Ožujak | **Q1 (razgraničenje)** | — |
| **P.1.6** | <span class="badge-izdavanje">Izdavanje</span> | — | 10.03. | 25.01. | — | Siječanj* | Siječanj | 25.01. |
| **P.1.7** | <span class="badge-izdavanje">Izdavanje</span> | — | 10.04. | — | — | Travanj* | Travanj | — |
| **P.1.8** | <span class="badge-izdavanje">Izdavanje</span> | — | 10.03. | 25.01. | — | Siječanj ili ožujak* | Siječanj | 25.01. |
| **P.2.1** | <span class="badge-naplata">Naplata</span> | DA | 20.03. | 10.03. | **15.05.** | **Svibanj** | Ožujak | 10.03. |
| **P.2.2** | <span class="badge-naplata">Naplata</span> | DA | 10.03. | 25.01. | **15.04.** | **Travanj** | Siječanj | 25.01. |
| **P.2.3** | <span class="badge-naplata">Naplata</span> | DA | 10.02. | — | 05.02. | Veljača | — | — |
| **P.2.4** | <span class="badge-naplata">Naplata</span> | DA | 10.04. | — | — | Travanj* | Travanj | — |

\* Za P.1.x: ovisi o tome je li račun stigao prije roka za PDV prijavu — vidi [Pretporez: dva uvjeta](#pretporez-dva-uvjeta-i-nijanse-u-praksi). Za P.1.7 i P.2.4 (CreditNote): travanj u praksi, ali obveznik ima pravo na retroaktivni ispravak u mjesecu izvornog računa — vidi [Senatex C-518/14](#sudska-praksa-eu--pravo-na-odbitak-i-račun).

---

*Svi primjeri koriste iste poslovne slučajeve kao [glavna dokumentacija — sekcija 4](primjeri-izdavatelj). Zakonski temelj: [sekcija 8](referenca#8-zakonski-temelj).*
