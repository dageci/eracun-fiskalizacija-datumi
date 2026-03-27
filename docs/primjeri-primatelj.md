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

### Sadržaj
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.
</div>

---

## Kako primatelj određuje datume?

Kupac iz primljenog eRačun XML-a treba izvući tri neovisna datuma:

| Pitanje | Gdje gledati u XML-u | Propis |
|---------|----------------------|--------|
| **PDV (pretporez)** — u koje razdoblje ide odbitak? | BT-7 > BT-8 > BT-2 (hijerarhija iz [sekcije 2](eracun-datumi-poreza-workflow#2-ključno-pravilo-br-co-03)) + provjera HR-BT-15 za obračun po naplati | Čl. 57, 60 i 125.i Zakona o PDV-u |
| **Trošak/rashod** — u koje razdoblje se priznaje? | BT-72 (`ActualDeliveryDate`) ili BT-73/BT-74 (`StartDate`/`EndDate`) | HSFI 16, načelo nastanka događaja |
| **Skladište (primka)** — kad se knjiži ulaz robe? | BT-72 (`ActualDeliveryDate`) ili stvarni datum primitka robe | Interna pravila, usklađenje s otpremnicom |

> **Ključni uvid**: Ova tri datuma mogu biti u **različitim mjesecima ili čak godinama** za isti račun. To nije greška — to je normalan rad sustava gdje se PDV, trošak i skladište reguliraju različitim propisima. Detaljno objašnjenje: [sekcija 5 — Datumi na eRačunu vs. datumi u knjigovodstvu](eracun-datumi-poreza-workflow#5-datumi-na-eračunu-vs-datumi-u-knjigovodstvu).

### Pretporez kod obračuna po naplati — posebna pravila za kupca

Ako primljeni eRačun sadrži `BT-8=432` i/ili `HR-BT-15` (`HRObracunPDVPoNaplati`), to znači da izdavatelj koristi obračun po naplaćenoj naknadi (čl. 125.i). Za kupca to ima **direktnu posljedicu**:

> **Čl. 125.i, st. 3 Zakona o PDV-u**: Kupac koji prima račun od obveznika koji obračunava PDV po naplaćenoj naknadi, **pravo na odbitak pretporeza ima tek u trenutku kad plati račun**, ne u trenutku primitka računa.

To znači da kupac mora pratiti:
1. Datum primitka eRačuna (za evidenciju)
2. **Datum plaćanja** (za pretporez) — ovo je datum koji određuje PDV razdoblje

---

## P.1 Obračun po izdavanju (čl. 30) <span class="badge-izdavanje">Po izdavanju</span>

### P.1.1 Isporuka i račun isti dan
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.1](eracun-datumi-poreza-workflow#411-isporuka-i-račun-isti-dan-po-izdavanju)

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

> **Najjednostavniji slučaj** — svi datumi su u istom mjesecu. Pretporez, rashod i primka idu u ožujak. Nema BT-7 ni BT-8, pa je datum porezne obveze = BT-2 = 15.03. Kupac je primio račun isti dan, obveza PDV-a je nastala, oba uvjeta za pretporez su ispunjena (čl. 57 + čl. 60).

---

### P.1.2 Isporuka u drugom mjesecu od računa
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.2](eracun-datumi-poreza-workflow#412-isporuka-u-drugom-mjesecu-od-računa-po-izdavanju)

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

> **Pretporez ide u ožujak**, ne u travanj! Obveza PDV-a nastala je 28.03. (BT-7 = datum isporuke). Kupac je primio račun 05.04., ali rok za PDV prijavu za ožujak je 30.04.2026. — budući da je račun stigao **prije roka**, kupac može uključiti pretporez u prijavu za ožujak (čl. 57 + čl. 60, vidi [sekciju 5.3](eracun-datumi-poreza-workflow#53-pretporez-dva-uvjeta-i-nijanse-u-praksi)).
>
> Rashod se također priznaje u ožujku po BT-72 (datum isporuke = datum nastanka poslovnog događaja, HSFI 16).

---

### P.1.3 Račun izdan prije isporuke (čl. 30 st. 2)
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.3](eracun-datumi-poreza-workflow#413-račun-izdan-prije-isporuke-čl-30-st-2-po-izdavanju)

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
> **Za ERP sustav**: automatsko knjiženje mora razdvojiti PDV datum (BT-2 = 25.03.) od datuma rashoda (BT-72 = 05.04.).

---

### P.1.4 Predujam / avansni račun (čl. 30 st. 5)
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.4](eracun-datumi-poreza-workflow#414-predujam-avansni-račun-čl-30-st-5-po-izdavanju)

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
> **Prepoznavanje predujma u XML-u**: `InvoiceTypeCode = 386` i nepostojanje BT-72 (`ActualDeliveryDate`).

---

### P.1.5 Kontinuirana usluga — obračunsko razdoblje (BT-73/BT-74)
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.5](eracun-datumi-poreza-workflow#415-kontinuirana-usluga--obračunsko-razdoblje-bt-73-bt-74-po-izdavanju)

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
> - **Pretporez: ožujak** — BT-7 = 31.03. (kraj razdoblja = datum nastanka obveze po čl. 30 st. 2). Račun stigao 05.04., ali rok za PDV prijavu za ožujak je 30.04. — kupac može uključiti pretporez u prijavu za ožujak.
> - **Rashod: vremensko razgraničenje** — usluga je trajala od 01.01. do 31.03. (BT-73/BT-74). Prema HSFI 16, trošak se priznaje u razdoblju kad je usluga obavljena. Ukupni iznos se raspodjeljuje na siječanj, veljaču i ožujak (1/3 + 1/3 + 1/3) ili prema drugoj prikladnoj metodi.
> - **Primka**: nema — ovo je usluga, ne fizička roba.
>
> **Za ERP sustav**: BT-73/BT-74 daju informaciju za automatsko vremensko razgraničenje troškova. Bez tih polja, ERP bi trošak knjižio u mjesec računa (travanj) — što bi bilo krivo.

---

### P.1.6 BT-8=35 — automatska veza na datum isporuke
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.6](eracun-datumi-poreza-workflow#416-bt-835--automatska-veza-na-datum-isporuke-po-izdavanju)

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
> - **Pretporez: siječanj** — BT-8=35 upućuje sustav da koristi BT-72 = 25.01. Račun je stigao 10.03. — ali rok za PDV prijavu za siječanj je bio 28.02. Ako je taj rok **već prošao**, pretporez ide u **ožujak** (razdoblje primitka računa), ne u siječanj! Vidi [sekciju 5.3](eracun-datumi-poreza-workflow#53-pretporez-dva-uvjeta-i-nijanse-u-praksi).
> - **Rashod: siječanj** — BT-72 = 25.01., roba je isporučena u siječnju.
>
> **Važno za primatelja**: Kad je BT-8=35, primatelj NE treba tražiti BT-7 — datum poreza se automatski čita iz BT-72. Rezultat je isti kao kad izdavatelj koristi BT-7 eksplicitno (primjer P.1.2), samo je mehanizam drugačiji.

---

### P.1.7 Odobrenje / CreditNote
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.7](eracun-datumi-poreza-workflow#417-odobrenje--creditnote-po-izdavanju)

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

> **Primatelj mora ispraviti pretporez** u mjesecu primitka odobrenja.
>
> - **Pretporez: travanj** — BT-7 ne postoji u UBL CreditNote shemi. Datum porezne obveze = BT-2 = 10.04. Kupac u PDV prijavi za travanj smanjuje pretporez za iznos odobrenja.
> - **Rashod: travanj** — ispravak rashoda se također knjiži u travnju (datum primitka odobrenja).
> - **Skladište**: Ako se radi o povratu robe, kupac knjiži izdatnicu (izlaz iz skladišta). Ako je odobrenje za popust/razliku u cijeni, nema skladišnog prometa.
>
> **Prepoznavanje u XML-u**: Korijen dokumenta je `<CreditNote>`, ne `<Invoice>`, i tip je 381.

---

### P.1.8 Svi datumi u različitim mjesecima — BT-7 eksplicitni datum
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.1.8](eracun-datumi-poreza-workflow#418-svi-datumi-u-različitim-mjesecima--bt-7-eksplicitni-datum-po-izdavanju)

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
> - **Pretporez**: Obveza PDV-a nastala u siječnju (BT-7 = 25.01.), ali račun je stigao tek u ožujku. Rok za PDV prijavu za siječanj bio je 28.02. — taj rok je **prošao**. Kupac prema praksi Porezne uprave može pretporez uključiti tek u prijavu za **ožujak** (mjesec primitka računa). Vidi detaljno [sekciju 5.3](eracun-datumi-poreza-workflow#53-pretporez-dva-uvjeta-i-nijanse-u-praksi).
> - **Rashod: siječanj** — BT-72 = 25.01., roba je isporučena u siječnju. Po HSFI 16, trošak pripada siječnju.
> - **Primka: 25.01.** — roba je fizički zaprimljena u siječnju.
>
> **Za ERP sustav**: ovo zahtijeva **tri različita datuma** u istom dokumentu — PDV u ožujku, rashod u siječnju, primka 25.01. Automatsko knjiženje mora sve tri razlikovati.

---

## P.2 Obračun po naplaćenoj naknadi (čl. 125.i) <span class="badge-naplata">Po naplati</span>

### P.2.1 Isporuka i račun isti mjesec
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.1](eracun-datumi-poreza-workflow#421-isporuka-i-račun-isti-mjesec-po-naplati)

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

### P.2.2 Isporuka u drugom mjesecu od računa
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.2](eracun-datumi-poreza-workflow#422-isporuka-u-drugom-mjesecu-od-računa-po-naplati)

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

### P.2.3 Predujam / avansni račun
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.4](eracun-datumi-poreza-workflow#424-predujam-avansni-račun-po-naplati)

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

---

### P.2.4 Odobrenje / CreditNote
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Izdavateljeva perspektiva: [4.2.6](eracun-datumi-poreza-workflow#426-odobrenje--creditnote-po-naplati)

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
> - **Pretporez: travanj** — ispravak pretporeza se knjiži u mjesecu primitka odobrenja (10.04.). BT-7 ne postoji u CreditNote shemi.
> - **Rashod: travanj** — korekcija rashoda u mjesecu primitka.
> - **HR-BT-15 je prisutan** i u CreditNote jer je to svojstvo obveznika.
>
> **Otvoreno pitanje**: Ako je izvorni račun već plaćen i pretporez odbijen u ranijem mjesecu, treba li ispravak pretporeza ići retroaktivno u taj raniji mjesec ili u mjesec primitka odobrenja? U praksi se radi **u mjesecu primitka odobrenja**.

---

## Sažetak — algoritam za primatelja

Za automatsko knjiženje primljenog eRačuna, ERP sustav treba izvršiti sljedeće korake:

### Korak 1: Odredi datum nastanka porezne obveze

```
AKO postoji BT-7 (TaxPointDate)     → datum_poreza = BT-7
INAČE AKO postoji BT-8:
  AKO BT-8 = 3                      → datum_poreza = BT-2 (IssueDate)
  AKO BT-8 = 35                     → datum_poreza = BT-72 (ActualDeliveryDate)
  AKO BT-8 = 432                    → datum_poreza = datum_placanja (odgođeno!)
INAČE                                → datum_poreza = BT-2 (IssueDate)
```

### Korak 2: Odredi pretporez

```
AKO BT-8 = 432 ILI postoji HR-BT-15:
  → pretporez = mjesec u kojem kupac PLATI račun (čl. 125.i st. 3)
  → IZUZETAK: predujam (InvoiceTypeCode=386) → pretporez = BT-7
INAČE:
  → pretporez = mjesec datum_poreza iz Koraka 1
  → ALI: samo ako je račun primljen PRIJE roka za PDV prijavu tog mjeseca
  → AKO je rok prošao → pretporez = mjesec primitka računa
```

### Korak 3: Odredi rashod

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

### Korak 4: Odredi primku (ako je roba)

```
AKO postoji BT-72 I radi se o robi (ne usluzi):
  → primka = BT-72
AKO je predujam (InvoiceTypeCode=386):
  → nema primke
AKO je CreditNote s povratom robe:
  → izdatnica (izlaz iz skladišta) = datum primitka odobrenja
```

---

## Pretporez: dva uvjeta i nijanse u praksi
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Pravo na odbitak pretporeza kod obračuna po izdavanju reguliraju **dva članka** koji se nadopunjuju:

**Čl. 57, st. 1** (nastanak prava):
> *"Pravo na odbitak PDV-a (pretporeza) nastaje u trenutku kad nastane obveza obračuna PDV-a koji se može odbiti."*

Dakle **pravo nastaje** u trenutku isporuke (npr. prosinac 2025.).

**Čl. 60, st. 1, točka b)** (uvjet za ostvarivanje prava):
> *"...ima račun u vezi s isporukom dobara i usluga, izdan u skladu s odredbama članaka 78., 79., 80. i 81."*

Dakle za **ostvarivanje** tog prava kupac mora **imati račun**.

### Što znači "ima račun"?

"Ima račun" ne znači datum izdavanja računa (BT-2), nego datum kad kupac **stvarno ima račun** — kad ga primi u svoj sustav. Kod eRačuna to je trenutak kad posrednik isporuči XML kupcu; kod papirnog računa to je dan kad stigne poštom.

EU Direktiva 2006/112/EC koristi izraz **"hold an invoice"** (čl. 178) — "posjedovati račun", ne "kad je račun izdan".

### U koje razdoblje ide pretporez?

Prema praksi Porezne uprave, pravilo ovisi o tome **kad je račun stigao u odnosu na rok za PDV prijavu** (od 01.01.2026. rok je do **zadnjeg dana u mjesecu** za prethodni mjesec):

| Kad je račun stigao | Pretporez ide u | Primjer |
|---|---|---|
| **Prije roka** za PDV prijavu za mjesec isporuke | Razdoblje **isporuke** | Isporuka 15.12.2025., eRačun stigao 10.01.2026. (rok za prosinac: 31.01.2026.) → pretporez u **prosincu 2025.** |
| **Nakon roka** za PDV prijavu za mjesec isporuke | Razdoblje **primitka računa** | Isporuka 15.12.2025., račun stigao 05.02.2026. (rok za prosinac već prošao) → pretporez u **veljači 2026.** |

### eRačun ovo praktički eliminira

Kod eRačuna dostava se mjeri u sekundama/minutama. Izdavatelj kreira račun → posrednik ga odmah isporučuje kupcu. Razlika između datuma izdavanja i datuma primitka je zanemariva — uvijek unutar istog dana, uvijek unutar roka za PDV prijavu.

To znači da kod eRačuna pretporez u praksi **uvijek ide u razdoblje kad je nastala obveza PDV-a** — što je upravo ono što čl. 57 namjerava. Razdvajanje se događa samo kod zakašnjelih papirnih računa ili kad izdavatelj kasni s izdavanjem.

### Sudska praksa EU — pravo na odbitak i račun

Pred Europskim sudom pravde (CJEU) vodi se postupak **C-167/26** (revizija predmeta T-689/24) koji se bavi upravo ovim pitanjem. Opći sud EU utvrdio je da:

- "Hold an invoice" iz čl. 178 Direktive je **formalni uvjet** za **ostvarivanje** prava na odbitak
- Ali **nije uvjet** za **nastanak** tog prava (nastanak je po čl. 167 = kad nastane obveza obračuna)
- Odgoda odbitka pretporeza samo zato što račun još nije primljen **krši načelo neutralnosti PDV-a** i proporcionalnosti

Konačna odluka ECJ-a još nije donesena. Ako potvrdi ovo tumačenje, to bi moglo značiti da kupac ima pravo na pretporez **odmah kad nastane obveza** (prosinac), neovisno o tome kad primi račun.

Relevantne presude:
- **C-518/14 (Senatex)**: Ispravak računa ima retroaktivan učinak — pretporez se može odbiti za razdoblje u kojem je račun izvorno izdan, ne samo u razdoblju ispravka
- **C-80/20 (Wilo Salmson France)**: EU pravo zabranjuje odbijanje povrata PDV-a u određenom razdoblju samo zato što je PDV dospio u ranijem razdoblju, a račun izdan u kasnijem

---

## Vremensko razgraničenje u knjigovodstvu

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

---

## Usporedna tablica svih primjera

| Primjer | Način obračuna | Datum računa | Datum isporuke | Datum plaćanja | Pretporez | Rashod | Primka |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **P.1.1** | <span class="badge-izdavanje">Izdavanje</span> | 15.03. | 15.03. | — | Ožujak | Ožujak | 15.03. |
| **P.1.2** | <span class="badge-izdavanje">Izdavanje</span> | 05.04. | 28.03. | — | Ožujak | Ožujak | 28.03. |
| **P.1.3** | <span class="badge-izdavanje">Izdavanje</span> | 25.03. | 05.04. | — | Ožujak | **Travanj** | 05.04. |
| **P.1.4** | <span class="badge-izdavanje">Izdavanje</span> | 10.02. | — | 05.02. | Veljača | — | — |
| **P.1.5** | <span class="badge-izdavanje">Izdavanje</span> | 05.04. | — | — | Ožujak | **Q1 (razgraničenje)** | — |
| **P.1.6** | <span class="badge-izdavanje">Izdavanje</span> | 10.03. | 25.01. | — | Siječanj* | Siječanj | 25.01. |
| **P.1.7** | <span class="badge-izdavanje">Izdavanje</span> | 10.04. | — | — | Travanj | Travanj | — |
| **P.1.8** | <span class="badge-izdavanje">Izdavanje</span> | 10.03. | 25.01. | — | Siječanj ili ožujak* | Siječanj | 25.01. |
| **P.2.1** | <span class="badge-naplata">Naplata</span> | 20.03. | 10.03. | **15.05.** | **Maj** | Ožujak | 10.03. |
| **P.2.2** | <span class="badge-naplata">Naplata</span> | 10.03. | 25.01. | **15.04.** | **Travanj** | Siječanj | 25.01. |
| **P.2.3** | <span class="badge-naplata">Naplata</span> | 10.02. | — | 05.02. | Veljača | — | — |
| **P.2.4** | <span class="badge-naplata">Naplata</span> | 10.04. | — | — | Travanj | Travanj | — |

\* Ovisi o tome je li račun stigao prije roka za PDV prijavu — vidi [Pretporez: dva uvjeta](#pretporez-dva-uvjeta-i-nijanse-u-praksi) na ovoj stranici.

---

*Svi primjeri koriste iste poslovne slučajeve kao [glavna dokumentacija — sekcija 4](eracun-datumi-poreza-workflow#4-primjeri-iz-prakse). Zakonski temelj: [sekcija 8](eracun-datumi-poreza-workflow#8-zakonski-temelj).*
