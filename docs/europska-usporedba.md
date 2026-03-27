---
layout: default
title: "Europska usporedba"
has_toc: true
nav_order: 7
---

# Europska usporedba — eRačun sustavi u EU

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## Zašto usporedba?

Hrvatska nije jedina zemlja koja se suočava s pitanjem kako povezati porezni zakon s XML elementima eRačuna. Sve EU zemlje imaju isti temelj (Direktiva 2006/112/EC, norma EN16931), ali svaka ima nacionalne specifičnosti — u formatu, modelu razmjene, izvještavanju prema poreznoj i kvaliteti dokumentacije.

### Legenda

| Oznaka | Značenje | Tok računa |
|---|---|---|
| **Clearance** | Račun prolazi kroz sustav porezne uprave **prije** dostave kupcu — porezna ga vidi u realnom vremenu | Izdavatelj → **Porezna uprava** → Kupac |
| **Reporting** | Račun ide direktno kupcu, ali se podaci **paralelno** šalju poreznoj (obično u roku nekoliko dana) | Izdavatelj → Kupac + Izdavatelj → **Porezna uprava** |
| **Post-audit** | Porezna dobiva podatke **naknadno** kroz periodične izvještaje (SAF-T, PDV prijava) — ne u realnom vremenu | Izdavatelj → Kupac (porezna vidi tek kroz izvještaje) |
| **Peppol** | Decentralizirana razmjena kroz certificirane pristupne točke — porezna uprava **nije** u samom toku razmjene, ali neke zemlje dodaju paralelni kanal prema PU (Slovačka 5-corner, Hrvatska fiskalizacija) | Izdavatelj → AP → AP → Kupac |
| **eDelivery 4-corner + fiskalizacija** | Hrvatski hibridni model: razmjena eRačuna ide CEF eDelivery AS4 protokolom u 4-corner topologiji (AP ↔ AP), a posrednik **paralelno** šalje fiskalizacijsku poruku Poreznoj upravi za svaki izlazni i ulazni eRačun, plus eIzvještavanje o naplati i odbijanju. **Napomena:** ovo NIJE Peppol mreža — Hrvatska koristi CEF eDelivery AS4 v1.15 s nacionalnim profilom (eRačun-AS4), ne Peppol AS4 profil. | Izdavatelj → AP →→ AP → Kupac, **istovremeno** AP → **Porezna uprava** |
| **5-corner** | Proširenje Peppol modela gdje je porezna uprava **peti sudionik** — sve transakcije automatski vidljive PU kroz mrežu | Izdavatelj → AP → **PU** → AP → Kupac |
| **PU** | Kratica za **Poreznu upravu** (ili ekvivalent u drugoj zemlji — ANAF, AEAT, NAV, SDI...) | — |
| **AP** | Kratica za **pristupnu točku** (Access Point) — certificirani posrednik za razmjenu eRačuna | — |
| **CIUS** | Core Invoice Usage Specification — nacionalna prilagodba EU norme EN16931 | — |

---

## Usporedna tablica — svih 23 EU zemlje

| Zemlja | Format | Obvezno B2B | Model | Izlazni → PU | Ulazni → PU | Naplata → PU | Nacionalni CIUS |
|---|---|---|---|---|---|---|---|
| **Hrvatska** | UBL + HRFISK20Data | 01/2026 | eDelivery 4-corner + fiskalizacija (mikroeRačun besplatan za ne-PDV obveznike) | **DA** | **DA** | **DA** (eIzvještavanje) | HR CIUS 2025 |
| **Španjolska** | SII XML / Verifactu | SII: 2017; Verifactu: 01/2026 | Reporting (SII) + Verifactu | **DA** (4 dana) | **DA** (4 dana) | **DA** ("Cobros") | — |
| **Rumunjska** | RO_CIUS (UBL) | 01/2024 | Clearance (e-Factura) | **DA** | **DA** (automatski) | NE | RO_CIUS |
| **Poljska** | FA(3) vlastiti | 02/2026 | Clearance (KSeF) | **DA** | **DA** (automatski) | NE | — (vlastiti format) |
| **Italija** | FatturaPA vlastiti | 2019 | Clearance (SDI) | **DA** | **DA** (automatski) | NE | — (vlastiti format) |
| **Grčka** | myDATA XML/JSON | 03/2026 | Clearance (myDATA) | **DA** | **DA** (klasifikacija) | Djelomično | — |
| **Francuska** | Factur-X/UBL/CII | 09/2026 | Clearance (PPF+PDP) | **DA** | **DA** | NE | — |
| **Mađarska** | NAV XML v3.0 | RTIR: 2018 | Real-time Reporting | **DA** (sve!) | NE | NE | — (vlastiti format) |
| **Slovačka** | UBL/Peppol | 01/2027 | 5-corner (Peppol + PU) | **DA** | **DA** | NE | EN16931 |
| **Njemačka** | UBL/CII (XRechnung) | 01/2025 (prijem) | Decentralizirano | NE | NE | NE | XRechnung CIUS |
| **Danska** | OIOUBL / NemHandel BIS 4 | 01/2026 | Peppol (NemHandel) | NE | NE | NE | OIOUBL |
| **Belgija** | Peppol BIS 3.0 | 01/2026 | Peppol | NE | NE | NE | — |
| **Litva** | i.SAF (SAF-T) | NE (samo Reporting) | Post-audit (i.SAF) | **DA** (i.SAF) | **DA** (i.SAF) | NE | i.SAF |
| **Estonija** | UBL / CII | 07/2025 (buyer-choice) | Post-audit (KMD INF) | Djelomično | Djelomično | NE | — |
| **Portugal** | CIUS-PT / SAF-T | NE (samo B2G) | Post-audit (SAF-T) | **DA** (SAF-T) | NE | NE | CIUS-PT |
| **Latvija** | UBL / Peppol | 01/2028 | Planirano Reporting | **DA** (planirano) | **DA** (planirano) | NE | — |
| **Irska** | Peppol BIS 3.0 | 11/2028 | Planirano Peppol | **DA** (planirano) | **DA** (planirano) | NE | Peppol BIS 3.0 |
| **Slovenija** | e-SLOG 2.0 / UBL | 01/2028 (odgođeno) | Planirano Peppol | NE (odgođeno) | NE (odgođeno) | NE | e-SLOG |
| **Nizozemska** | SI-UBL / NLCIUS | planirano 2030-2032 | Planirano Peppol | NE | NE | NE | NLCIUS |
| **Finska** | Finvoice 3.0 / Peppol | NE (pravo na eRačun) | Peppol | NE | NE | NE | Finvoice |
| **Austrija** | ebInterface / UBL | NE (samo B2G) | Portal (USP) | NE | NE | NE | ebInterface |
| **Češka** | ISDOC / UBL | planirano 2035 | — | NE | NE | NE | ISDOC |
| **Švedska** | Peppol BIS 3.0 | NE (istraga pokrenuta) | — | NE | NE | NE | — |

---

## Ključni zaključci

### Izvještavanje o naplati — samo Hrvatska i Španjolska

Samo dvije EU zemlje zahtijevaju od obveznika da izvještavaju o naplati eRačuna:
- **Hrvatska** — `EvidentirajNaplatu` kroz eIzvještavanje servis (čl. 53 Zakona o fiskalizaciji)
- **Španjolska** — "Cobros sobre facturas" kroz SII sustav (naplate na izdanim računima)

Nijedna druga zemlja — ni Italija, ni Poljska, ni Rumunjska — ne prati što se događa s računom **nakon** što je izdan/dostavljen.

### Izvještavanje o odbijanju — samo Hrvatska

Hrvatska je **jedina EU zemlja** koja zahtijeva formalno izvještavanje o odbijanju eRačuna (`EvidentirajOdbijanje`).

### Oba smjera (izlazni + ulazni) → porezna uprava

| Zemlja | Kako | Automatski? |
|---|---|---|
| **Hrvatska** | Posrednik šalje fiskalizacijsku poruku za oba smjera | NE — posrednik/obveznik inicira |
| **Rumunjska** | Sve prolazi kroz e-Factura platformu | DA — Clearance |
| **Poljska** | Sve prolazi kroz KSeF | DA — Clearance |
| **Italija** | Sve prolazi kroz SDI | DA — Clearance |
| **Grčka** | Clearance + klasifikacija na myDATA | DA — ali primatelj mora klasificirati |
| **Španjolska** | Obje strane šalju u SII (Post-audit) | NE — obveznik šalje u roku 4 dana |
| **Litva** | i.SAF izvještaj (prodajne i nabavne knjige) | NE — Post-audit, periodični izvještaj |

### Zanimljive specifičnosti po zemljama

| Zemlja | Specifičnost |
|---|---|
| **Hrvatska** | Jedina zemlja koja ima besplatni državni sustav (mikroeRačun) ali ga ograničava na ne-PDV obveznike; PDV obveznici moraju koristiti komercijalnog posrednika |
| **Mađarska** | Najširi opseg: **SVE** fakture (B2B + B2C + izvoz) u realnom vremenu — ali samo izdane, ne primljene |
| **Danska** | Pionir eRačuna od 2005., 20+ godina iskustva, migracija na NemHandel BIS 4 do 2029. |
| **Finska** | Model "prava na eRačun" — kupac može zahtijevati od dobavljača da šalje eRačun |
| **Estonija** | "Buyer-choice" model — kupac se registrira i forsira dobavljača |
| **Slovačka** | Jedina zemlja s "5-corner" modelom (Peppol 4 kutna + porezna uprava kao 5. kut) |
| **Portugal** | ATCUD + QR kod na svakom računu — potrošač može verificirati račun |
| **Španjolska** | 3 paralelna sustava (SII + Verifactu + TicketBAI) zbog regionalne autonomije Baskije i Navarre |
| **Rumunjska** | e-Transport sustav za praćenje kretanja robe — povezan s e-Factura |

---

## Detaljnije o ključnim zemljama

### Poljska (KSeF) — zlatni standard dokumentacije
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Najbolja praksa</span></div>

Poljsko Ministarstvo financija objavilo je **"Broszura informacyjna"** — dokument koji za svaki XML element navodi opis, tip podatka, **referencu na članak Zakona o PDV-u**, primjer i napomene. Ovo je **najbliže** onome što mi gradimo za Hrvatsku.

**Ključna razlika**: Vlastiti XML format (FA(3)), ne UBL. Nema problem "EU norma vs proširenje". KSeF je clearance — račun prolazi kroz sustav Ministarstva financija **prije** dostave kupcu.

**Izvori:**
- <a href="https://ksef.podatki.gov.pl/media/4u1bmhx4/information-sheet-on-the-fa-3-logical-structure.pdf" target="_blank">FA(3) Information Sheet (engleski)</a>
- <a href="https://ksef.podatki.gov.pl/media/jknpcymf/broszura-informacyjna-dotyczaca-struktury-logicznej-fa-3-04032026.pdf" target="_blank">Broszura informacyjna (poljski, 03/2026)</a>
- <a href="https://ksef.podatki.gov.pl/pliki-do-pobrania-ksef-20/" target="_blank">KSeF 2.0 — svi dokumenti</a>

### Njemačka (XRechnung) — najbolji open-source ekosustav
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Najbolja praksa</span></div>

Koristi **UBL/CII** (iste BT oznake kao HR). Ima UStG-to-BT mapping tablicu i kompletni GitHub ekosustav (test suite, schematron, validator). **Nema** clearance ni fiskalizaciju.

**Izvori:**
- <a href="https://xeinkauf.de/xrechnung/" target="_blank">XRechnung portal (KoSIT)</a>
- <a href="https://github.com/itplr-kosit/xrechnung-testsuite" target="_blank">GitHub — test suite</a>
- <a href="https://github.com/itplr-kosit/xrechnung-schematron" target="_blank">GitHub — Schematron</a>

### Italija (FatturaPA / SDI) — najduže iskustvo, najelegantniji pristup "po naplati"

Pionir EU eRačuna — B2B obvezno od 2019. Clearance model (SDI). **Najelegantniji** pristup obračunu po naplati: jedan element `EsigibilitaIVA` s tri vrijednosti (`I`=odmah, `D`=po naplati, `S`=split payment). Nema ambigviteta — za razliku od HR pristupa s BT-8=432 + HR-BT-15.

**Izvori:**
- <a href="https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/" target="_blank">FatturaPA dokumentacija</a>
- <a href="https://www.fatturapa.gov.it/en/lafatturapa/esempi/" target="_blank">Primjeri XML datoteka</a>

### Španjolska (SII / Verifactu) — jedina osim HR s izvještavanjem o naplati

Tri paralelna sustava: SII (velike tvrtke od 2017.), Verifactu (ostali od 01/2026), TicketBAI (Baskija). SII zahtijeva izvještavanje u roku 4 dana — i za izdane i za primljene račune. **"Cobros"** sustav prati naplate na izdanim računima — jedini osim HR koji to radi.

### Mađarska (NAV RTIR) — najširi opseg izvještavanja

**SVE** fakture (B2B + B2C + izvoz) se prijavljuju u realnom vremenu — najširi opseg u EU. Ali samo izdane, ne primljene. NAV objavljuje XSD, API, test okruženje — odlična dokumentacija.

**Izvor:** <a href="https://onlineszamla.nav.gov.hu/dokumentaciok" target="_blank">NAV Online Számla dokumentacija</a>

---

## Što Hrvatska može naučiti?

| Lekcija | Izvor | Primjena za HR |
|---------|-------|----------------|
| **Jedan dokument koji spaja zakon i XML** | Poljska (brošura) | Upravo to gradimo — ali za UBL format, ne vlastiti |
| **Open-source ekosustav na GitHubu** | Njemačka (KoSIT) | Već koristimo GitHub — dodati test suite i validator? |
| **Elegantan pristup "po naplati"** | Italija (EsigibilitaIVA) | HR ima BT-8 + HR-BT-15 — složenije, ali je tako definirano |
| **Ne fragmentirati dokumentaciju** | Francuska (anti-primjer) | Držati sve na jednom mjestu, javno dostupno |
| **Minimalni pristup nije dovoljan** | Belgija (anti-primjer) | Bez primjera i objašnjenja, ostaje se na forumima |

> **Zaključak**: Ono što gradimo za Hrvatsku — dokumentacija koja spaja Zakon o PDV-u, HR CIUS specifikaciju, EN16931 pravila i XML primjere iz perspektive i izdavatelja i primatelja — **ne postoji nigdje u EU za UBL-bazirani CIUS**. Poljska to ima za vlastiti format, Njemačka ima mapping tablicu, ali kompletni primjeri po poslovnim scenarijima — to je novo.

---

## EU-level resursi

| Izvor | Link |
|-------|------|
| EN16931 validacijski artefakti | <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">github.com/ConnectingEurope/eInvoicing-EN16931</a> |
| CEN/TC 434 tehnički odbor | <a href="https://github.com/CenPC434" target="_blank">github.com/CenPC434</a> |
| Peppol BIS Billing 3.0 | <a href="https://docs.peppol.eu/poacc/billing/3.0/bis/" target="_blank">docs.peppol.eu</a> |
| EU CIUS registar | <a href="https://ec.europa.eu/digital-building-blocks/sites/spaces/EINVCOMMUNITY/pages/48763623" target="_blank">EC — Registry of CIUS</a> |

---
