---
layout: default
title: "Datumi i knjigovodstvo"
has_toc: true
nav_order: 5
---

# Datumi na eRačunu vs. datumi u knjigovodstvu
<div style="margin-top:-0.8rem;margin-bottom:1rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

### Sadržaj
{: .no_toc }

- TOC
{:toc}

---

Datumi na eRačunu služe za **više različitih svrha** — PDV, priznavanje rashoda, materijalno/skladišno poslovanje — i regulirani su različitim propisima. Česta zabuna je poistovjećivati ih.

### 5.1 Koji datum čemu služi?

| BT polje | XML element | Služi za | Propis |
|----------|-------------|----------|--------|
| **BT-2** | `cbc:IssueDate` | Brojčanik računa, rok za fiskalizaciju, default datum PDV-a | Zakon o fiskalizaciji čl. 8-9 |
| **BT-7** | `cbc:TaxPointDate` | Eksplicitni datum nastanka obveze PDV-a | Čl. 30 Zakona o PDV-u |
| **BT-8** | `cbc:DescriptionCode` | Kod za određivanje datuma PDV-a (3, 35, 432) | EN16931 / BR-CO-03 |
| **BT-9** | `cbc:DueDate` | Rok plaćanja — za likvidaturu, cash flow, eIzvještavanje | Čl. 53 Zakona o fiskalizaciji |
| **BT-72** | `cbc:ActualDeliveryDate` | Datum isporuke — za PDV, ali i za **priznavanje rashoda/prihoda**, **skladišno poslovanje**, **garancije** | HSFI 16, čl. 30 Zakona o PDV-u |
| **BT-73/74** | `cbc:StartDate`/`cbc:EndDate` | Obračunsko razdoblje — za **periodične usluge**, **razgraničenje troškova**, **pretplate** | HSFI 16, računovodstvena praksa |

> **BT-72 (ActualDeliveryDate)** nije samo "informativan" — on je ključan za:
> - **Računovodstvo**: priznavanje rashoda/prihoda po načelu nastanka događaja (HSFI 16) — trošak se priznaje kad je usluga obavljena, ne kad je račun izdan
> - **Skladišno poslovanje**: primitak robe u skladište, usklađivanje s primkom/otpremnicom
> - **Garancije**: početak garantnog roka od datuma isporuke
> - **PDV**: ako se razlikuje od BT-2, kroz BT-7 ili BT-8=35 određuje datum porezne obveze
>
> **BT-73/BT-74 (StartDate/EndDate)** su ključni za:
> - **Vremensko razgraničenje troškova**: najam za Q1 se knjizi kao trošak Q1, čak i ako račun stiže u Q2
> - **Pretplate i pretplatničke usluge**: za koji period vrijedi usluga
> - **Kontinuirane isporuke**: komunalne usluge, telekomunikacije, zakup

### 5.2 Primjer: svi datumi u igri

IT podrška obavljena u prosincu 2025., račun izdan u siječnju 2026., plaćen u veljači 2026.

**Ako prodavatelj koristi obračun po izdavanju (čl. 30):** <span class="badge-izdavanje">Po izdavanju</span>

| Pitanje | Odgovor | Razdoblje | Propis |
|---------|---------|-----------|--------|
| Kad se **priznaje rashod** (trošak)? | Kad je usluga obavljena (BT-72) | **Prosinac 2025.** | HSFI 16, načelo nastanka događaja |
| Kad nastaje **obveza PDV-a** izdavatelju? | Kad je usluga obavljena | **Prosinac 2025.** (BT-7) | Čl. 30, st. 1 Zakona o PDV-u |
| Kad kupac ima **pravo na pretporez**? | Vidi 5.3 — ovisi o datumu primitka računa | **Prosinac 2025. ili Siječanj 2026.** | Čl. 57 + čl. 60 Zakona o PDV-u |
| Kad se rashod priznaje za **porez na dobit**? | U godini kad je nastao | **2025.** | Čl. 5 i 11 Zakona o porezu na dobit |

**Ako prodavatelj koristi obračun po naplaćenoj naknadi (čl. 125.i):** <span class="badge-naplata">Po naplati</span>

| Pitanje | Odgovor | Razdoblje | Propis |
|---------|---------|-----------|--------|
| Kad se **priznaje rashod** (trošak)? | Kad je usluga obavljena (BT-72) | **Prosinac 2025.** | HSFI 16, načelo nastanka događaja |
| Kad nastaje **obveza PDV-a** izdavatelju? | Kad kupac plati | **Veljača 2026.** (BT-8=432) | Čl. 125.i Zakona o PDV-u |
| Kad kupac ima **pravo na pretporez**? | Tek kad plati račun | **Veljača 2026.** | Čl. 125.i, st. 3 Zakona o PDV-u |
| Kad se rashod priznaje za **porez na dobit**? | U godini kad je nastao | **2025.** | Čl. 5 i 11 Zakona o porezu na dobit |

> **Ključna razlika**: Kod obračuna po naplati, kupac **ne smije odbiti pretporez pri primitku računa** — mora čekati do plaćanja. PDV obveza prodavatelja i pravo na pretporez kupca nastaju u istom trenutku: danom plaćanja.

### 5.3 Pretporez: dva uvjeta i nijanse u praksi
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span></div>

Pravo na odbitak pretporeza kod obračuna po izdavanju reguliraju **dva članka** koji se nadopunjuju:

**Čl. 57, st. 1** (nastanak prava):
> *"Pravo na odbitak PDV-a (pretporeza) nastaje u trenutku kad nastane obveza obračuna PDV-a koji se može odbiti."*

Dakle **pravo nastaje** u prosincu 2025. (kad je usluga obavljena).

**Čl. 60, st. 1, točka b)** (uvjet za ostvarivanje prava):
> *"...ima račun u vezi s isporukom dobara i usluga, izdan u skladu s odredbama članaka 78., 79., 80. i 81."*

Dakle za **ostvarivanje** tog prava kupac mora **imati račun**.

#### Što znači "ima račun"?

"Ima račun" ne znači datum izdavanja računa (BT-2), nego datum kad kupac **stvarno ima račun** — kad ga primi u svoj sustav. Kod eRačuna to je trenutak kad posrednik isporuči XML kupcu; kod papirnog računa to je dan kad stigne poštom.

EU Direktiva 2006/112/EC koristi izraz **"hold an invoice"** (čl. 178) — "posjedovati račun", ne "kad je račun izdan".

#### U koje razdoblje ide pretporez?

Prema praksi Porezne uprave, pravilo ovisi o tome **kad je račun stigao u odnosu na rok za PDV prijavu** (od 01.01.2026. rok je do **zadnjeg dana u mjesecu** za prethodni mjesec):

| Kad je račun stigao | Pretporez ide u | Primjer |
|---|---|---|
| **Prije roka** za PDV prijavu za mjesec isporuke | Razdoblje **isporuke** | Isporuka 15.12.2025., eRačun stigao 10.01.2026. (rok za prosinac: 31.01.2026.) → pretporez u **prosincu 2025.** |
| **Nakon roka** za PDV prijavu za mjesec isporuke | Razdoblje **primitka računa** | Isporuka 15.12.2025., račun stigao 05.02.2026. (rok za prosinac već prošao) → pretporez u **veljači 2026.** |

#### eRačun ovo praktički eliminira

Kod eRačuna dostava se mjeri u sekundama/minutama. Izdavatelj kreira račun → posrednik ga odmah isporučuje kupcu. Razlika između datuma izdavanja i datuma primitka je zanemariva — uvijek unutar istog dana, uvijek unutar roka za PDV prijavu.

To znači da kod eRačuna pretporez u praksi **uvijek ide u razdoblje kad je nastala obveza PDV-a** — što je upravo ono što čl. 57 namjerava. Razdvajanje se događa samo kod zakašnjelih papirnih računa ili kad izdavatelj kasni s izdavanjem.

#### Sudska praksa EU — pravo na odbitak i račun

Pred Europskim sudom pravde (CJEU) vodi se postupak **C-167/26** (revizija predmeta T-689/24) koji se bavi upravo ovim pitanjem. Opći sud EU utvrdio je da:

- "Hold an invoice" iz čl. 178 Direktive je **formalni uvjet** za **ostvarivanje** prava na odbitak
- Ali **nije uvjet** za **nastanak** tog prava (nastanak je po čl. 167 = kad nastane obveza obračuna)
- Odgoda odbitka pretporeza samo zato što račun još nije primljen **krši načelo neutralnosti PDV-a** i proporcionalnosti

Konačna odluka ECJ-a još nije donesena. Ako potvrdi ovo tumačenje, to bi moglo značiti da kupac ima pravo na pretporez **odmah kad nastane obveza** (prosinac), neovisno o tome kad primi račun.

Relevantne presude:
- **C-518/14 (Senatex)**: Ispravak računa ima retroaktivan učinak — pretporez se može odbiti za razdoblje u kojem je račun izvorno izdan, ne samo u razdoblju ispravka
- **C-80/20 (Wilo Salmson France)**: EU pravo zabranjuje odbijanje povrata PDV-a u određenom razdoblju samo zato što je PDV dospio u ranijem razdoblju, a račun izdan u kasnijem

### 5.4 Vremensko razgraničenje u knjigovodstvu

> Kad knjigovođa kaže *"ide u trošak za prošlu godinu"* — misli da je usluga obavljena u
> prošloj godini pa rashod pripada tamo (HSFI 16), čak i ako je račun stigao u siječnju
> nove godine. To se zove **vremensko razgraničenje**.
>
> Vremensko razgraničenje se rješava **interno u knjigovodstvu**, ne kroz eRačun XML.
> Ali eRačun XML **pomaže**: BT-72 (datum isporuke) i BT-73/BT-74 (razdoblje) daju
> knjigovođi/ERP sustavu informaciju potrebnu za automatsko razgraničenje — u koje
> razdoblje pripada trošak, neovisno o tome kad je račun stigao.
>
> Svih pet stavki iz tablice iznad mogu biti u **različitim mjesecima ili čak godinama** za isti poslovni događaj. To nije greška — to je normalan rad sustava gdje se PDV, trošak i porez na dobit reguliraju različitim propisima.

---
