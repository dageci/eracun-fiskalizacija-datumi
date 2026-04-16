---
layout: default
title: "Naknadno dospjeli računi"
has_toc: true
nav_order: 8
---

# Naknadno dospjeli računi — prijelazno razdoblje i granični slučajevi

Ova stranica pokriva situacije u kojima se eRačun izdaje **znatno nakon isporuke** — bilo zbog prijelaznog razdoblja 2025-2026, bilo zbog propusta, IOS usklađenja ili sudske presude. Za svaki slučaj analiziramo perspektivu izdavatelja i primatelja: koji datumi idu u XML, koji PDV period se primjenjuje, te kako fiskalizacija (F2) utječe na cijeli proces.

> **Ključno pravno načelo**: Za tuzemne isporuke u Hrvatskoj **ne postoji zakonski rok za izdavanje računa** (čl. 78 ZPDV propisuje rok samo za intra-EU isporuke — do 15. u mjesecu). Za domaće B2B transakcije, rok nije propisan — preporuka je "u najkraćem razumnom roku" (izvor: <a href="https://www.teb.hr/novosti/2024/u-kojem-roku-treba-izdati-racun/" target="_blank">TEB</a>). Međutim, **PDV obveza nastaje isporukom** (čl. 30 st. 1 ZPDV), neovisno o tome kad je račun izdan.

> **Napomena o HR-BT-15 (obračun po naplati)**: Sva analiza na ovoj stranici pretpostavlja **obračun po izdavanju** (čl. 30 ZPDV). Ako izdavatelj koristi **obračun po naplaćenoj naknadi** (čl. 125.i), PDV tretman se fundamentalno mijenja:
> - eRačun MORA sadržavati **HR-BT-15** (`HRObracunPDVPoNaplati`)
> - PDV obveza nastaje tek **po plaćanju**, ne po isporuci — BT-7 postaje datum plaćanja
> - Primatelj **ne smije** odbiti pretporez do plaćanja (čl. 125.i st. 3)
> - Kasno fakturiranje je **manje problematično** za PDV jer obveza ionako nastaje po plaćanju, ali eIzvještavanje o naplati ostaje obvezno
>
> Za detalje vidi [Pravila — specifičnost HR proširenja](pravila#specificnost-hr-prosirenja).

### Sadržaj {#sec-sadrzaj}
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.
</div>

---

## 1. Prijelazno razdoblje 2025. -> 2026. {#sec-prijelazno-razdoblje-2025-2026}
Zakon o fiskalizaciji (NN 89/25) uvodi obvezu eRačuna (fiskalizacija F2) od **01.01.2026.** (za obveznike PDV-a u B2B/B2G prometu). No poslovni događaji ne poštuju kalendarske granice — isporuka u prosincu 2025. može rezultirati računom u siječnju 2026., predujam iz 2025. može imati konačni račun u 2026., a odobrenje u 2026. može se odnositi na račun iz 2025.

Svaki od ovih slučajeva otvara pitanje: **primjenjuje li se F2 fiskalizacija, i kako se tretira PDV?**

---

### 1.1 Usluga u prosincu 2025., račun u siječnju 2026. {#sec-usluga-u-prosincu-2026}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Klasičan prijelazni slučaj: usluga je obavljena u prosincu 2025. (prije obveze eRačuna), ali račun se izdaje u siječnju 2026. (kad je eRačun obavezan).

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Datum izdavanja računa | 10.01.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 15.12.2025. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 15.12.2025. | BT-7 (`cbc:TaxPointDate`) — ili nema (default = BT-2) |
| F2 fiskalizacija | **DA** | Račun je IZDAN u 2026. |

> **Ključni uvid — F2 obaveza**: Račun se fiskalizira jer je **izdan** u 2026. (BT-2 = 10.01.2026.). Nije bitno kad je usluga obavljena — F2 obaveza ovisi o datumu izdavanja, ne o datumu isporuke. Ovo proizlazi iz PU pojašnjenja (pitanja 101/104).

> **PU pojašnjenje (pitanje 9)**: Računi poslani u 2025. ne podliježu obvezama iz Zakona o fiskalizaciji — ne treba raditi ni eIzvještavanje čak i ako je uplata u 2026.

**Perspektiva izdavatelja:**

| PDV period | F2 fiskalizacija | BT-7 | Napomena |
|:---:|:---:|:---:|---|
| **Prosinac 2025.** (ako navede BT-7=15.12.2025.) ili **Siječanj 2026.** (ako nema BT-7, default=BT-2) | **DA** — račun izdan u 2026. | Preporuka: navesti BT-7=15.12.2025. | Bez BT-7 PDV "klizi" u siječanj, a isporuka je bila u prosincu |

**Perspektiva primatelja:**

| Pretporez period | Rashod period | Napomena |
|:---:|:---:|---|
| **Prosinac 2025.** (ako BT-7=15.12.) ili **Siječanj 2026.** (ako nema BT-7) | **Prosinac 2025.** (BT-72=15.12.) | Pretporez ovisi o BT-7 i o tome kad primatelj primi račun — ako račun stigne u siječnju, a rok za PDV prijavu za prosinac 2025. je **20.01.2026.** (stari rok). Od PDV prijave za siječanj 2026. nadalje, rok je **zadnji dan u mjesecu** (dakle prijava za siječanj 2026. ima rok 28.02.2026.), primatelj mora imati račun u rukama prije roka |

> **Otvoreno pitanje**: Ako izdavatelj **ne navede BT-7** (jer nije bio obavezan u 2025. praksi), BT-2=10.01.2026. postaje default datum PDV obveze. Tada izdavatelj prijavljuje PDV u siječnju 2026. umjesto u prosincu 2025. — a primatelj nema osnovu za pretporez u prosincu. Ovo je **čest problem prijelaznog razdoblja** gdje izdavatelji ne navode BT-7 jer im "nije trebao" za stari sustav. Preporuka: **uvijek navesti BT-7** kad se isporuka i račun razlikuju.

---

### 1.2 Predujam iz 2025., konačni račun 2026. {#sec-predujam-iz-2025-2026}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Kupac je platio predujam u studenom 2025., izdavatelj je izdao avansni račun u studenom 2025. Isporuka je u veljači 2026. — izdaje se konačni račun.

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Predujam — datum izdavanja | 20.11.2025. | Izdan u 2025. — NIJE eRačun |
| Predujam — datum primitka uplate | 18.11.2025. | BT-7 na avansnom računu |
| **Storno predujma** — datum izdavanja | 05.02.2026. | Korektivni dokument za predujam |
| Konačni račun — datum izdavanja | 05.02.2026. | BT-2 (`cbc:IssueDate`) |
| Konačni račun — datum isporuke | 03.02.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| F2 fiskalizacija — predujam | **NE** | Izdan u 2025. |
| F2 fiskalizacija — storno predujma | **Iznimka — NE!** | Dokument koji mijenja račun iz 2025. |
| F2 fiskalizacija — konačni račun | **Iznimka — NE!** | PU pitanje 155/157 |

> **Kompletni ciklus predujma** (kad su predujam i isporuka u **različitim** poreznim razdobljima):
> 1. **Račun za predujam** — izdaje se kad novac stigne (studeni 2025.)
> 2. **Storno računa za predujam** — izdaje se kad je isporuka obavljena (veljača 2026.) — poništava avansni račun. Tri opcije:
>    - **381 (CreditNote, proces P9)** — ne zahtijeva KPD klasifikaciju (HR-BR-25 izuzetak) ✅
>    - **386 s negativnom količinom** — ne zahtijeva KPD (386 na listi izuzetaka) ✅
>    - **384 (korektivni, proces P10)** — **zahtijeva KPD!** Problematično za predujam jer nema artikala ⚠️
> 3. **Konačni račun** — izdaje se za puni iznos isporuke (veljača 2026.)
>
> **PU pojašnjenje (pitanja 3/4)**: PU preporučuje P10 s vrstom 384, ali izdavatelj samostalno određuje način. **Napomena**: 384 zahtijeva KPD klasifikaciju artikala (HR-BR-25), što je problematično za storno predujma. Preporučamo **381 ili 386 s negativnom količinom** jer su oslobođeni KPD obveze.

> **Ključni uvid — iznimka od F2**: Prema PU pojašnjenju (pitanja 155/157), **ni predujam, ni storno predujma, ni konačni račun ne idu kroz F2 fiskalizaciju** ako je predujam izdan u 2025. Logika: svi dokumenti čine jednu cjelinu — ako je predujam bio izvan sustava eRačuna (2025.), ostali dokumenti ga "nasljeđuju". Ovo je potvrđeno i PU odgovorom na pitanje o dokumentima koji mijenjaju račune iz 2025.: ne podliježu eRačun obvezi.

**Perspektiva izdavatelja:**

| Dokument | PDV period | F2? | Prihod | Napomena |
|----------|:---:|:---:|:---:|---|
| Predujam (studeni 2025.) | Studeni 2025. | NE | Ne priznaje se (primljeno sredstvo) | Izdan u 2025. |
| Storno predujma (veljača 2026.) | Poništava studeni 2025. | **NE** | — | Dokument koji mijenja račun iz 2025. |
| Konačni račun (veljača 2026.) | Veljača 2026. (puni iznos) | **NE** | Veljača 2026. (HSFI 15) | PU iznimka — cjelina s predujmom iz 2025. |

**Perspektiva primatelja:**

| Dokument | Pretporez period | Rashod period | Napomena |
|----------|:---:|:---:|---|
| Predujam (studeni 2025.) | Studeni 2025. | Ne priznaje se (dano sredstvo) | Pretporez odbijen u studenom |
| Storno predujma (veljača 2026.) | Poništava pretporez iz studenog | — | Negativni pretporez — umanjuje prethodno odbijeni iznos iz studenog. Ispravak PDV prijave za studeni ili uključenje u tekuću (veljačku) prijavu (čl. 33 st. 7) |
| Konačni račun (veljača 2026.) | Veljača 2026. | Veljača 2026. (BT-72) | Pretporez za **puni iznos** isporuke (ne samo razliku) — jer je storno poništio predujam |

> **Neto efekt predujam ciklusa za primatelja**: Pretporez iz studenog (predujam) se poništava stornom, a konačni račun daje pretporez za puni iznos u veljači. Krajnji rezultat: pretporez se "seli" iz studenog u veljaču. Rashod se priznaje tek u veljači (kad je isporuka obavljena, BT-72).

> **Otvoreno pitanje**: Što ako predujam **nije izdan** u 2025. (propust), ali je novac primljen u 2025.? Kupac je platio, izdavatelj nije izdao avansni račun, a sada u 2026. izdaje i avansni i konačni račun. Primjenjuje li se F2 na oba? PU pojašnjenje pokriva samo slučaj kad je predujam izdan u 2025. — što ako nije, ostaje nejasno.

> **PU pojašnjenje (pitanje 171)**: Ovo pravilo vrijedi i kada dolazi do prijenosa poslovanja (npr. obrt → d.o.o.) — ako je predujam primljen u 2025., konačni račun u 2026. (čak i pod novim OIB-om) ne podliježe F2.
>
> **PU pojašnjenje (pitanje 222)**: Porezni obveznik nije obvezan izdati račun za primljeni predujam ako je izdao račun za obavljenu isporuku do roka za podnošenje prijave PDV-a za razdoblje u kojem je primio predujam. Međutim, ako je predujam primljen u jednom razdoblju oporezivanja, a isporuka se obavi u drugom — račun za predujam se **mora** izdati.

---

### 1.3 Odobrenje u 2026. za račun iz 2025. {#sec-odobrenje-u-2026-2025}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Izvorni račun izdan je u studenom 2025. (nije bio F2 fiskaliziran). U veljači 2026. otkrivena je greška ili odobren popust — izdaje se CreditNote.

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Izvorni račun — datum izdavanja | 15.11.2025. | Izdan u 2025. — NIJE eRačun |
| CreditNote — datum izdavanja | 10.02.2026. | BT-2 (`cbc:IssueDate`) |
| Referenca na izvorni račun | BR-2025-1234 | BT-25 (`cbc:ID` u `BillingReference`) |
| F2 fiskalizacija — CreditNote | **?** | Otvoreno pitanje |

> **PU pojašnjenje**: Dokumenti koji mijenjaju račune iz 2025. **ne podliježu** obvezi izdavanja eRačuna niti fiskalizaciji u 2026. Storno ili odobrenje za izvorni račun iz 2025. prati pravila koja su važila kad je izvorni račun izdan.

> **Ključni uvid — otvoreno pitanje**: CreditNote je izdan u 2026. (BT-2=10.02.2026.), što bi po općem pravilu značilo obvezu F2 fiskalizacije. Ali se odnosi na račun iz 2025. koji **nije bio fiskaliziran**. Pitanje: mora li se CreditNote fiskalizirati ako izvorni račun nije bio u sustavu? PU pojašnjenja (pitanja 155/157) pokrivaju predujam, ali ne pokrivaju eksplicitno CreditNote za račune iz 2025.

**Perspektiva izdavatelja:**

| PDV period | F2? | Napomena |
|:---:|:---:|---|
| **Veljača 2026.** (umanjenje PDV-a) ili **retroaktivno studeni 2025.** (ispravak prijave) | **Nejasno** | Ovisi o tumačenju — je li odobrenje "novi račun" (2026., F2 obaveza) ili "ispravak starog" (2025., bez F2)? |

**Perspektiva primatelja:**

| Pretporez period | Rashod period | Napomena |
|:---:|:---:|---|
| Umanjenje pretporeza u **veljači 2026.** ili ispravak prijave za **studeni 2025.** | Ispravak rashoda — ovisi o materijalnosti (HSFI 5) | Senatex presuda ([C-518/14 (Senatex)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun)): pravo na retroaktivni ispravak pretporeza u period kad je nastala obveza, ali HR praksa nije potpuno usklađena |

> **EU kontekst — Senatex**: Presuda Suda EU ([C-518/14, Senatex](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun)) potvrđuje pravo na retroaktivni ispravak odbitka pretporeza u porezno razdoblje kad je nastala obveza, bez obzira kad je ispravak primljen. No u hrvatskom kontekstu, primjena ovog načela na prijelazno razdoblje 2025./2026. još nije razjašnjena.

---

## 2. Naknadno izdani računi (izvan prijelaznog razdoblja) {#sec-naknadno-izdani-racuni}
Ovi slučajevi nisu specifični za prijelazno razdoblje — događaju se i unutar 2026. i kasnije. Zajedničko im je da **račun kasni** za isporukom, ponekad mjesecima ili godinama.

---

### 2.1 Račun izdan mjesecima nakon isporuke {#sec-racun-izdan-mjesecima}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Usluga obavljena u ožujku 2026., ali račun izdan tek u lipnju 2026. — zbog administrativnog propusta, čekanja na odobrenje, ili jednostavno kasnog fakturiranja.

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Datum izdavanja računa | 15.06.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 20.03.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 20.03.2026. | BT-7 (`cbc:TaxPointDate`) |
| Obračunsko razdoblje | 01.03.–31.03.2026. | BT-73/BT-74 (opcionalno) |
| F2 fiskalizacija | **DA** — u lipnju | Račun izdan u lipnju |

> **Ključni uvid**: Čl. 78 st. 1 Zakona o PDV-u propisuje rok za izdavanje računa: **najkasnije 15. dana od kraja mjeseca** u kojem je obavljena isporuka (za domaće isporuke). Za isporuku 20.03. — rok je 15.04.2026. Račun izdan u lipnju je **kasno izdan račun** u smislu Zakona, ali to ne znači da je nevažeći — samo da je izdavatelj prekršio rok.

> **PU pojašnjenje (pitanje 146)**: "Zakonom o fiskalizaciji nije propisan rok za izdavanje računa" — potvrda da za tuzemne isporuke nema zakonskog roka.
>
> **Građevinske situacije (PU pitanja 43, 99)**: Građevinske privremene situacije su najčešći legitimni razlog za kasno fakturiranje (ovjera nadzornog inženjera može trajati i 45+ dana). Fiskalizacija se provodi istovremeno s izdavanjem. Između PDV obveznika primjenjuje se prijenos porezne obveze — PDV obveza nastaje kad je usluga obavljena, neovisno o ovjeri. Za ne-PDV primatelje, PDV nastaje istekom razdoblja u kojem je situacija ovjerena.

**Perspektiva izdavatelja:**

| PDV period | F2 datum | BT-7 | Napomena |
|:---:|:---:|:---:|---|
| **Ožujak 2026.** | **Lipanj 2026.** (kad je izdan) | 20.03.2026. | PDV obveza je nastala u ožujku (isporuka), ali F2 se fiskalizira kad je račun izdan. Izdavatelj mora ispraviti PDV prijavu za ožujak ako je inicijalno nije prijavio. |

**Perspektiva primatelja:**

| Pretporez period | Rashod period | Napomena |
|:---:|:---:|---|
| **Ožujak 2026.** — ako račun stigne prije roka za prijavu; inače **Lipanj 2026.** | **Ožujak 2026.** (BT-72) | Pretporez: dva uvjeta moraju biti ispunjena — (1) obveza PDV-a nastala (ožujak, BT-7) i (2) primatelj ima račun. Ako je rok za PDV prijavu za ožujak istekao (30.04. — od 2026. rok je zadnji dan u mjesecu), primatelj uključuje pretporez u prvi sljedeći period kad ima račun = lipanj. |

> **Otvoreno pitanje — ispravak prijave**: Primatelj primi račun u lipnju za isporuku iz ožujka. Može li retroaktivno ispraviti PDV prijavu za ožujak i uključiti pretporez u ožujak? U praksi, PU dopušta ispravak ako rok za prijavu za ožujak (30.04.) nije istekao u trenutku primitka računa — ali ako je istekao, primatelj pretporez uključuje u lipanj (kad je primio račun). Alternativno, neki porezni savjetnici preporučuju podnošenje ispravka za ožujak, pozivajući se na [Senatex presudu](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun) i [Wilo Salmson C-80/20](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun).

---

### 2.2 IOS usklađenje — otkriven nefakturirani posao {#sec-ios-uskladenje-otkriven}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Tijekom IOS (izvod otvorenih stavaka) usklađenja u lipnju 2026. otkriveno je da isporuka iz siječnja 2026. **nije fakturirana** — roba je isporučena, primka postoji kod kupca, ali račun nikad nije izdan.

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Datum izdavanja računa | 20.06.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke | 15.01.2026. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 15.01.2026. | BT-7 (`cbc:TaxPointDate`) |
| F2 fiskalizacija | **DA** — u lipnju | Račun izdan u lipnju |

> **Upozorenje**: Ako se tijekom IOS-a otkrije da isporuka nikad nije fakturirana, izdavatelj je **već trebao prijaviti PDV** u razdoblju isporuke (čl. 30 st. 1 — obveza nastaje isporukom, ne fakturiranjem). Naknadno izdavanje računa ne mijenja PDV obvezu — samo formalizira dokumentaciju. Neizdavanje računa je prekršaj s kaznom 3.980–66.360 EUR za pravne osobe.

> **Ključni uvid**: Ovo je teži slučaj od 2.1 jer **PDV obveza je nastala u siječnju** (čl. 30 — isporukom), ali izdavatelj uopće nije prijavio PDV za tu transakciju. Izdavanje računa u lipnju ne "pomiče" PDV obvezu — izdavatelj mora podnijeti **ispravak PDV prijave za siječanj** i prijaviti obvezu retroaktivno, zajedno s eventualnim zateznim kamatama.

**Perspektiva izdavatelja:**

| PDV period | F2 datum | Napomena |
|:---:|:---:|---|
| **Siječanj 2026.** (ispravak prijave!) | **Lipanj 2026.** | Obveza PDV-a nastala je isporukom u siječnju. Račun je kasno izdan — ali PDV nije vezan za datum računa nego za datum isporuke (BT-7). Izdavatelj podnosi ispravak za siječanj. |

**Perspektiva primatelja:**

| Pretporez period | Rashod period | Primka | Napomena |
|:---:|:---:|:---:|---|
| **Lipanj 2026.** (kad primi račun) | **Siječanj 2026.** (BT-72) | **Već knjižena u siječnju** | Primatelj je robu primio i proknjižio primku u siječnju. Rashod je priznat u siječnju (nastanak događaja). Pretporez: primatelj nije imao račun do lipnja — uključuje pretporez u lipanj. Prema [C-80/20 (Wilo Salmson)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun), obveznik ima pravo na ispravak prijave za izvorni mjesec. |

> **Otvoreno pitanje**: Primatelj je rashod proknjižio u siječnju na temelju primke (bez računa). Je li to ispravno? Po HSFI 16, rashod se priznaje kad nastane poslovni događaj — isporuka u siječnju. Ali bez računa, primatelj je morao koristiti procijenjeni iznos (razgraničenje). Kad račun stigne u lipnju, usklađuje se eventualna razlika. Za pretporez: ispravak prijave za siječanj je diskutabilan jer primatelj **nije imao račun** u siječnju — čl. 60 traži posjedovanje računa kao uvjet za pretporez.

---

### 2.3 Sudska presuda — naknadno izdavanje {#sec-sudska-presuda-naknadno-izdavanje}

<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

Sud naredi izdavatelju izdavanje računa za uslugu obavljenu u prošloj godini. Izdavatelj je odbijao izdati račun, kupac je pokrenuo spor, i sud je presudio.

**Ključni datumi:**

| Podatak | Vrijednost | XML element |
|---------|-----------|-------------|
| Datum izdavanja računa | 10.09.2026. | BT-2 (`cbc:IssueDate`) |
| Datum isporuke (iz presude) | 01.06.2025. | BT-72 (`cbc:ActualDeliveryDate`) |
| Datum nastanka obveze PDV-a | 01.06.2025. | BT-7 (`cbc:TaxPointDate`) |
| Datum pravomoćnosti presude | 15.08.2026. | Nije BT element — interni podatak |
| F2 fiskalizacija | **DA** — u rujnu 2026. | Račun izdan u 2026. |

> **Zastara potraživanja** (ZOO): B2B potraživanja zastarijevaju za **3 godine** (čl. 228 st. 1), sudski utvrđena za **10 godina**. Zastara potraživanja je odvojena od porezne obveze — čak i ako je potraživanje zastarjelo, porezna obveza za prijavu PDV-a u razdoblju isporuke ostaje.

> **Ključni uvid**: Najekstremniji slučaj — isporuka je bila prije **više od godine dana**, u razdoblju kad F2 fiskalizacija nije ni postojala. Ali račun se izdaje u 2026. i podliježe F2. PDV obveza je nastala u lipnju 2025. — izdavatelj mora podnijeti ispravak za lipanj 2025. Ovo otvara pitanje zastare i kamate, jer je prošlo više od 12 mjeseci.

**Perspektiva izdavatelja:**

| PDV period | F2 datum | Napomena |
|:---:|:---:|---|
| **Lipanj 2025.** (ispravak prijave) | **Rujan 2026.** | PDV obveza je nastala isporukom, bez obzira na to kad je račun izdan ili presuda donesena. Izdavatelj podnosi ispravak za lipanj 2025. — mogući su zatezne kamate za kašnjenje. |

**Perspektiva primatelja:**

| Pretporez period | Rashod period | Napomena |
|:---:|:---:|---|
| **Rujan 2026.** (kad primi račun) ili ispravak za **Lipanj 2025.** (Senatex) | **Lipanj 2025.** — ispravak rashoda ovisi o materijalnosti (HSFI 5) | Primatelj tek u rujnu 2026. dobiva račun. Po čl. 60 Zakona o PDV-u, pretporez može koristiti tek kad ima račun. Po [C-518/14 (Senatex)](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun) presudi, mogao bi tražiti retroaktivni ispravak za lipanj 2025. — ali u HR praksi to zahtijeva podnošenje ispravka prijave i obrazloženje PU-u. |

> **Otvoreno pitanje — PDV period isporuke iz 2025.**: Isporuka je bila u lipnju 2025. — prije sustava eRačuna. BT-7=01.06.2025. je "u prošlosti" iz perspektive novog sustava. Kako PU tretira ispravak za period koji je bio pod starim režimom (papirni računi, bez F2)? Ovo je granični slučaj koji PU pojašnjenja trenutno ne pokrivaju.

---

## 3. Ponašanje računovođe — izdavatelj {#sec-ponasanje-racunovode-izdavatelj}
Sumarni pregled svih scenarija iz perspektive izdavatelja:

| # | Situacija | BT-2 | BT-7 | BT-72 | F2? | PDV period | Prihod | Napomena |
|---|-----------|------|------|-------|:---:|------------|--------|----------|
| 1.1 | Usluga 12/2025., račun 01/2026. | 10.01.2026. | 15.12.2025. | 15.12.2025. | **DA** | Prosinac 2025. | Prosinac 2025. | Preporuka: navesti BT-7 |
| 1.2 | Predujam 2025., konačni 2026. | 05.02.2026. | — | 03.02.2026. | **NE** | Veljača 2026. (razlika) | Veljača 2026. | PU iznimka (pit. 155/157) |
| 1.3 | CreditNote 2026. za račun 2025. | 10.02.2026. | — | — | **?** | Veljača 2026. ili ispravak 11/2025. | Ispravak 11/2025. | Otvoreno pitanje |
| 2.1 | Račun 3 mj. nakon isporuke | 15.06.2026. | 20.03.2026. | 20.03.2026. | **DA** | Ožujak 2026. | Ožujak 2026. | Kasno izdan — ispravak prijave |
| 2.2 | IOS — nefakturirano | 20.06.2026. | 15.01.2026. | 15.01.2026. | **DA** | Siječanj 2026. (ispravak!) | Siječanj 2026. | Obveza nastala isporukom |
| 2.3 | Sudska presuda | 10.09.2026. | 01.06.2025. | 01.06.2025. | **DA** | Lipanj 2025. (ispravak!) | Lipanj 2025. | Moguće zatezne kamate |

> **Napomena o prihodu**: Prihod se uvijek priznaje po datumu isporuke (HSFI 15), ne po datumu računa. Čak i kad je račun izdan mjesecima kasnije, prihod se evidentira u razdoblju kad je isporuka obavljena (BT-72).

> **Obrazac**: U svim slučajevima, **F2 fiskalizacija se veže za BT-2** (datum izdavanja), a **PDV period se veže za BT-7** (datum nastanka obveze). Ova dva datuma mogu biti u potpuno različitim godinama. Izdavatelj mora fiskalizirati račun kad ga izda (F2), ali PDV prijaviti u period kad je nastala obveza (BT-7).

---

## 4. Ponašanje računovođe — primatelj {#sec-ponasanje-racunovode-primatelj}
Sumarni pregled svih scenarija iz perspektive primatelja:

| # | Situacija | Kad primi račun | Pretporez period | Rashod period | Ispravak prijave? | Napomena |
|---|-----------|:-:|:-:|:-:|:-:|---|
| 1.1 | Usluga 12/2025., račun 01/2026. | Siječanj 2026. | Prosinac 2025. (ako stigne prije roka) ili Siječanj 2026. | Prosinac 2025. | Možda — ovisi o roku | Provjeriti BT-7 |
| 1.2 | Predujam 2025., konačni 2026. | Veljača 2026. | Veljača 2026. | Veljača 2026. | NE | Standardni konačni račun |
| 1.3 | CreditNote 2026. za račun 2025. | Veljača 2026. | Veljača 2026. (umanjenje) ili ispravak 11/2025. | Ispravak — ovisi o materijalnosti | Možda ([Senatex](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun)) | Retroaktivni ispravak? |
| 2.1 | Račun 3 mj. nakon isporuke | Lipanj 2026. | Lipanj 2026. (propušten rok za ožujak) | Ožujak 2026. | Moguć ispravak za ožujak | Dva uvjeta za pretporez |
| 2.2 | IOS — nefakturirano | Lipanj 2026. | Lipanj 2026. | Siječanj 2026. (primka) | NE za pretporez, DA za rashod (usklađenje iznosa) | Rashod po primci, pretporez po računu |
| 2.3 | Sudska presuda | Rujan 2026. | Rujan 2026. ili ispravak 06/2025. ([Senatex](primjeri-primatelj#sudska-praksa-eu--pravo-na-odbitak-i-račun)) | Lipanj 2025. (ispravak) | DA — za rashod sigurno, za pretporez ovisi o pristupu | Najkompleksniji slučaj |

> **Napomena o rashodu**: Rashod se uvijek priznaje po datumu isporuke (HSFI 16), ne po datumu računa. Primatelj evidentira rashod kad nastane poslovni događaj (isporuka, BT-72), neovisno o tome kad račun stigne. Ako račun kasni, primatelj koristi procjenu (razgraničenje) i usklađuje kad račun stigne.

> **Obrazac za primatelja**: Rashod se uvijek veže za **BT-72 (datum isporuke)** — neovisno o tome kad račun stigne. Pretporez ovisi o **dva uvjeta**: (1) nastanak PDV obveze (BT-7) i (2) posjedovanje računa (čl. 60). Ako primatelj primi račun **nakon roka** za PDV prijavu za period iz BT-7, pretporez ide u period kad je primio račun — osim ako podnese ispravak prijave (što je dopušteno, ali zahtijeva obrazloženje).

---

## 5. Što eRačun mijenja {#sec-sto-eracun-mijenja}

> **Prije eRačuna**: papirni račun mogao je stići tjednima ili mjesecima nakon izdavanja. Primatelj često nije imao račun u rokovima za PDV prijavu, pa se pretporez "guralo" u kasniji period. Porezna uprava nije imala uvid u to kad je račun stvarno izdan, a kad primljen.

> **S eRačunom**: dostava je gotovo trenutna — posrednik isporučuje XML u roku sekundi ili minuta. Ali to **ne rješava sve probleme**: BT-2 (datum izdavanja) i dalje može biti daleko nakon isporuke (BT-72). eRačun ne sprječava kasno fakturiranje — samo osigurava da kad se račun izda, dostava bude brza.

> **Fiskalizacija čini kasno fakturiranje vidljivim**: Prije F2, PU nije znala kad je račun izdan vs kad je isporuka obavljena. S F2, PU vidi BT-2 (datum izdavanja) i BT-7/BT-72 (datum isporuke) — ako su mjesecima razmaknuti, to je signal za provjeru.

> **Fiskalizacija F2**: Porezna uprava sada vidi **oba kraja** transakcije — izlazni račun izdavatelja (F2 fiskalizacija) i ulazni račun primatelja (fiskalizacija zaprimanja). To znači da PU može detektirati:
> - Kasno fakturiranje (BT-72 daleko prije BT-2)
> - Nefakturirane isporuke (primka kod kupca, a nema F2 zapisa kod PU)
> - Neusklađenost između PDV prijava izdavatelja i primatelja
>
> Ovo je značajna promjena u odnosu na papirni sustav — ali **pravila o PDV-u se nisu promijenila**, samo je vidljivost veća. Kasno fakturiranje i dalje rezultira ispravkom PDV prijave, ali sada PU može proaktivno detektirati takve slučajeve umjesto da čeka inspekciju.

---

## Izvori {#sec-izvori}

| Izvor | Link |
|-------|------|
| TEB: U kojem roku treba izdati račun? | <a href="https://www.teb.hr/novosti/2024/u-kojem-roku-treba-izdati-racun/" target="_blank">teb.hr</a> |
| PU: Nastanak porezne obveze i odbitak PDV-a | <a href="https://porezna-uprava.gov.hr/Misljenja/Detaljno/1782" target="_blank">porezna-uprava.gov.hr</a> |
| PU: Pitanja i odgovori F2 | <a href="https://porezna-uprava.gov.hr/hr/izdavanje-i-primanje-eracuna-i-fiskalizacija-eracuna/8047" target="_blank">porezna-uprava.gov.hr</a> |
| PU: Primjeri postupanja za predujmove | <a href="https://porezna.gov.hr/fiskalizacija/bezgotovinski-racuni/bezgotovinski-racuni-novosti/o/primljeni-predujmovi" target="_blank">porezna.gov.hr</a> |
| Zastara kod prometa roba i usluga | <a href="https://sudovi.hr/sites/default/files/dokumenti/2019-10/Zastara_kod_ugovora_o_prometu_roba_i_usluga.pdf" target="_blank">sudovi.hr (PDF)</a> |
| Zakon o PDV-u (pročišćeni tekst) | <a href="https://www.zakon.hr/z/1455/zakon-o-porezu-na-dodanu-vrijednost" target="_blank">zakon.hr</a> |

---

*Zadnja izmjena: 2026-03-27*
