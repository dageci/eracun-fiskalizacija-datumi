---
layout: default
title: "Europska usporedba"
has_toc: true
nav_order: 7
---

# Europska usporedba — kako druge zemlje dokumentiraju eRačun

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## Zašto usporedba?

Hrvatska nije jedina zemlja koja se suočava s pitanjem kako povezati porezni zakon s XML elementima eRačuna. Sve EU zemlje imaju isti temelj (Direktiva 2006/112/EC, norma EN16931), ali svaka ima nacionalne specifičnosti. Neke su napravile izvrsnu dokumentaciju, neke minimalno — i iz toga možemo učiti.

---

## Usporedna tablica

| | Poljska | Njemačka | Italija | Francuska | Belgija | **Hrvatska** |
|---|---|---|---|---|---|---|
| **XML format** | Vlastiti (FA(3)) | UBL/CII (XRechnung) | Vlastiti (FatturaPA) | Factur-X / UBL / CII | Peppol BIS 3.0 | UBL + HR proširenje (HRFISK20Data) |
| **Centralni sustav** | KSeF (clearance) | Decentralizirano | SDI (clearance) | PPF + PDP (clearance) | Peppol mreža | Posrednici + eFiskalizacija |
| **Fiskalizacija u realnom vremenu** | DA | NE | DA | DA (od 09/2026) | NE | **DA** |
| **Izlazni račun → porezna** | **DA** — račun prolazi kroz KSeF prije dostave kupcu | NE | **DA** — račun prolazi kroz SDI | **DA** — prolazi kroz PPF/PDP | NE | **DA** — posrednik/PT šalje fiskalizacijsku poruku (`EvidentirajERacun`) |
| **Ulazni račun → porezna** | **DA** — KSeF automatski bilježi prijem | NE | **DA** — SDI automatski bilježi | **DA** — PPF bilježi | NE | **DA** — primatelj (ili PT) fiskalizira ulazni eRačun |
| **Izvještavanje o naplati** | NE (u planu) | NE | NE | NE | NE | **DA** — `EvidentirajNaplatu` (eIzvještavanje, čl. 53) |
| **Izvještavanje o odbijanju** | NE | NE | NE | NE | NE | **DA** — `EvidentirajOdbijanje` (eIzvještavanje) |
| **Obvezno od** | 02/2026 | 01/2025 (prijem) | 2019 (B2B) | 09/2026 | 01/2026 | 01/2026 |
| **Zakon + XML u jednom dokumentu?** | **DA** | Djelomično | Djelomično | NE | NE | **U izradi** |
| **Primjeri po scenarijima** | DA (ZIP s XML) | DA (GitHub test suite) | DA (6 primjera) | NE (plaćeni AFNOR standardi) | NE | **DA** (16 izdavatelj + 12 primatelj) |
| **Open source alati** | NE | **DA** (GitHub) | NE | NE | NE | **DA** (GitHub) |
| **Dva režima PDV-a** | DA | DA | DA | DA | DA | DA |
| **Kako označavaju "po naplati"** | Zaglavlje FA(3) | BT-8=432 | EsigibilitaIVA="D" | BT-8=432 | BT-8=432 | BT-8=432 **+ HR-BT-15** |

> **Hrvatska je jedina EU zemlja** koja od obveznika zahtijeva i **izvještavanje o naplati** i **izvještavanje o odbijanju** eRačuna prema Poreznoj upravi. U ostalim clearance modelima (Poljska, Italija, Francuska) porezna uprava vidi samo sam račun — ne i što se s njim dalje dogodilo (je li plaćen, odbijen, djelomično naplaćen).

---

## Poljska (KSeF) — zlatni standard dokumentacije
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Najbolja praksa</span></div>

Poljsko Ministarstvo financija objavilo je **"Broszura informacyjna"** — dokument koji za svaki XML element navodi:
- Opis i tip podatka
- **Referencu na članak poljskog Zakona o PDV-u**
- Primjer vrijednosti
- Napomene o uporabi

Ovo je **najbliže** onome što mi gradimo za Hrvatsku — jedan dokument koji spaja zakon i XML.

**Ključna razlika**: Poljska koristi **vlastiti XML format** (FA(3)), ne EN16931 UBL. Zato su elementi potpuno drugačiji (P_1, P_6 umjesto BT-2, BT-7). Nemaju problem s "EU norma vs nacionalno proširenje" jer je sve nacionalno.

**Fiskalizacija**: KSeF je clearance model — svaki račun prolazi kroz centralni sustav Ministarstva financija **prije** dostave kupcu. Sustav dodjeljuje jedinstveni KSeF broj. Nema posrednika u hrvatskom smislu.

**Označavanje "po naplati"**: U zaglavlju računa, bez zasebnog elementa poput HR-BT-15.

**Izvori:**
- <a href="https://ksef.podatki.gov.pl/media/4u1bmhx4/information-sheet-on-the-fa-3-logical-structure.pdf" target="_blank">FA(3) Information Sheet (engleski)</a>
- <a href="https://ksef.podatki.gov.pl/media/jknpcymf/broszura-informacyjna-dotyczaca-struktury-logicznej-fa-3-04032026.pdf" target="_blank">Broszura informacyjna (poljski, ažuriran 03/2026)</a>
- <a href="https://ksef.podatki.gov.pl/pliki-do-pobrania-ksef-20/" target="_blank">KSeF 2.0 — svi dokumenti za preuzimanje</a>

---

## Njemačka (XRechnung) — najbolji open-source ekosustav
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Najbolja praksa</span></div>

Njemačka koristi **UBL/CII** (iste BT oznake kao Hrvatska) i ima najrazvijeniji open-source ekosustav:

- **XRechnung CIUS specifikacija** — njemačka prilagodba EN16931
- **UStG-to-BT mapping tablica** — mapira članke njemačkog Zakona o PDV-u na BT oznake. Ovo je najbliže onome što mi radimo, ali je **zasebni dokument**, ne integrirano u primjere
- **GitHub repozitoriji** (sve javno):
  - Test suite s XML primjerima
  - Schematron pravila
  - Validator konfiguracija

**Ključna razlika**: Njemačka **nema** centralni clearance sustav ni fiskalizaciju u realnom vremenu. eRačuni se razmjenjuju decentralizirano (Peppol, email, portali). Nema ekvivalenta hrvatske eFiskalizacije.

**Označavanje "po naplati"**: Koriste BT-8=432, **bez** nacionalnog proširenja poput HR-BT-15.

**Izvori:**
- <a href="https://xeinkauf.de/xrechnung/" target="_blank">XRechnung portal (KoSIT)</a>
- <a href="https://github.com/itplr-kosit/xrechnung-testsuite" target="_blank">GitHub — XRechnung test suite</a>
- <a href="https://github.com/itplr-kosit/xrechnung-schematron" target="_blank">GitHub — XRechnung Schematron</a>

---

## Italija (FatturaPA / SDI) — najduže iskustvo

Italija je **pionir** EU eRačuna — B2G od 2014., B2B obvezno od 2019. Imaju 7+ godina iskustva.

- **SDI (Sistema di Interscambio)** — clearance model, svaki račun prolazi kroz SDI
- **FatturaPA** — vlastiti XML format (ne UBL), ali usklađen s EN16931
- **Tehnička specifikacija** — 71 stranica, element po element, s tabularnim prikazom

**Ključna razlika**: Italija ima **najelegantniji** pristup "po naplati" — jedan element `EsigibilitaIVA` s tri vrijednosti:
- `I` = Immediata (odmah po isporuci)
- `D` = Differita (po naplati)
- `S` = Split Payment (javna uprava plaća PDV direktno državi)

Nema ambigviteta — jedna oznaka, tri opcije. Za razliku od hrvatskog pristupa gdje imamo BT-8=432 iz EU norme **plus** HR-BT-15 iz nacionalnog proširenja za istu informaciju.

**Izvori:**
- <a href="https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fattura-elettronica/formato-fatturapa/" target="_blank">FatturaPA dokumentacija</a>
- <a href="https://www.fatturapa.gov.it/en/lafatturapa/esempi/" target="_blank">Primjeri XML datoteka</a>

---

## Francuska (Factur-X / PPF) — fragmentirano

Francuska uvodi obvezni eRačun u fazama od rujna 2026. Dokumentacija je **razasuta** po tri organizacije:
- **DGFiP** (porezna uprava) — regulatorna specifikacija
- **AFNOR** (tijelo za standarde) — tehničke norme (plaćene, nisu javne!)
- **FNFE-MPE** (industrijski forum) — Factur-X format specifikacija

**Ključna razlika**: Francuska podržava **tri formata** (Factur-X, UBL, CII) i ima clearance model (PPF + certificirane PDP platforme). Nema jednog dokumenta koji sve spaja — i AFNOR standardi se moraju kupiti.

**Označavanje "po naplati"**: Koriste BT-8=432, bez nacionalnog proširenja.

**Izvori:**
- <a href="https://www.impots.gouv.fr/specifications-externes-b2b" target="_blank">Specifications externes B2B (DGFiP)</a>
- <a href="https://fnfe-mpe.org/factur-x/factur-x_en/" target="_blank">Factur-X specifikacija</a>

---

## Belgija (Peppol) — minimalistički pristup

Belgija je uzela **najjednostavniji put** — koristi Peppol BIS 3.0 bez ikakve nacionalne prilagodbe. Nema CIUS-BE, nema nacionalnih proširenja, nema fiskalizacije u realnom vremenu.

**Nema** dokumenta koji spaja porezni zakon s XML elementima — oslanjaju se potpuno na Peppol dokumentaciju.

**Izvori:**
- <a href="https://www.peppolcheck.be/guidelines" target="_blank">Belgian B2B guidelines</a>

---

## Što Hrvatska može naučiti?

| Lekcija | Izvor | Primjena za HR |
|---------|-------|----------------|
| **Jedan dokument koji spaja zakon i XML** | Poljska (brošura) | Upravo to gradimo — ali za UBL format, ne vlastiti |
| **Open-source ekosustav na GitHubu** | Njemačka (KoSIT) | Već koristimo GitHub — dodati test suite i validator? |
| **Elegantan pristup "po naplati"** | Italija (EsigibilitaIVA I/D/S) | HR ima BT-8 + HR-BT-15 — složenije, ali je tako definirano |
| **Ne fragmentirati dokumentaciju** | Francuska (anti-primjer) | Držati sve na jednom mjestu, javno dostupno |
| **Minimalni pristup nije dovoljan** | Belgija (anti-primjer) | Bez primjera i objašnjenja, ostaje se na forumima |

> **Zaključak**: Ono što mi gradimo za Hrvatsku — dokument koji spaja Zakon o PDV-u, HR CIUS specifikaciju, EN16931 pravila i XML primjere — **ne postoji nigdje u EU za UBL-bazirani CIUS**. Poljska to ima za vlastiti format, Njemačka ima mapping tablicu, ali kompletni primjeri po poslovnim scenarijima s perspektivom i izdavatelja i primatelja — to je novo.

---

## Kompletna EU tablica — svih 23 zemlje

### Legenda

| Oznaka | Značenje |
|---|---|
| **Clearance** | Račun prolazi kroz sustav porezne uprave prije dostave kupcu |
| **Reporting** | Podaci o računu se šalju poreznoj, ali račun ide direktno kupcu |
| **Post-audit** | Porezna dobiva podatke naknadno (SAF-T, PDV prijava) |
| **Peppol** | Decentralizirana razmjena bez porezne u sredini |

### Tablica

| Zemlja | Format | Obvezno B2B | Model | Izlazni → PU | Ulazni → PU | Naplata → PU | Nacionalni CIUS |
|---|---|---|---|---|---|---|---|
| **Hrvatska** | UBL + HRFISK20Data | 01/2026 | Posrednici + eFiskalizacija | **DA** | **DA** | **DA** (eIzvještavanje) | HR CIUS 2025 |
| **Poljska** | FA(3) vlastiti | 02/2026 | Clearance (KSeF) | **DA** | **DA** (automatski) | NE | — (vlastiti format) |
| **Njemačka** | UBL/CII (XRechnung) | 01/2025 (prijem) | Decentralizirano | NE | NE | NE | XRechnung CIUS |
| **Italija** | FatturaPA vlastiti | 2019 | Clearance (SDI) | **DA** | **DA** (automatski) | NE | — (vlastiti format) |
| **Francuska** | Factur-X/UBL/CII | 09/2026 | Clearance (PPF+PDP) | **DA** | **DA** | NE | — |
| **Belgija** | Peppol BIS 3.0 | 01/2026 | Peppol | NE | NE | NE | — (koristi Peppol as-is) |
| **Španjolska** | SII XML / Verifactu | SII: 2017; Verifactu: 01/2026 | Reporting (SII) + Verifactu | **DA** (4 dana) | **DA** (4 dana) | **DA** ("Cobros") | — |
| **Rumunjska** | RO_CIUS (UBL) | 01/2024 | Clearance (e-Factura) | **DA** | **DA** (automatski) | NE | RO_CIUS |
| **Grčka** | myDATA XML/JSON | 03/2026 | Clearance (myDATA) | **DA** | **DA** (klasifikacija) | Djelomično | — |
| **Mađarska** | NAV XML v3.0 | RTIR: 2018 | Real-time reporting | **DA** (sve!) | NE | NE | — (vlastiti format) |
| **Slovačka** | UBL/Peppol | 01/2027 | 5-corner (Peppol + PU) | **DA** | **DA** | NE | EN16931 |
| **Danska** | OIOUBL / NemHandel BIS 4 | 01/2026 | Peppol (NemHandel) | NE | NE | NE | OIOUBL |
| **Nizozemska** | SI-UBL / NLCIUS | planirano 2030-2032 | Planirano Peppol | NE | NE | NE | NLCIUS |
| **Finska** | Finvoice 3.0 / Peppol | NE (pravo na eRačun) | Peppol | NE | NE | NE | Finvoice |
| **Austrija** | ebInterface / UBL | NE (samo B2G) | Portal (USP) | NE | NE | NE | ebInterface |
| **Slovenija** | e-SLOG 2.0 / UBL | 01/2028 (odgođeno) | Planirano Peppol | NE (odgođeno) | NE (odgođeno) | NE | e-SLOG |
| **Irska** | Peppol BIS 3.0 | 11/2028 | Planirano Peppol | **DA** (planirano) | **DA** (planirano) | NE | Peppol BIS 3.0 |
| **Estonija** | UBL / CII | 07/2025 (buyer-choice) | Post-audit (KMD INF) | Djelomično (KMD INF) | Djelomično (KMD INF) | NE | — |
| **Latvija** | UBL / Peppol | 01/2028 | Planirano reporting | **DA** (planirano) | **DA** (planirano) | NE | — |
| **Litva** | i.SAF (SAF-T) | NE (samo reporting) | Post-audit (i.SAF) | **DA** (i.SAF) | **DA** (i.SAF) | NE | i.SAF |
| **Portugal** | CIUS-PT / SAF-T | NE (samo B2G) | Post-audit (SAF-T) | **DA** (SAF-T mjesečno) | NE | NE | CIUS-PT |
| **Češka** | ISDOC / UBL | planirano 2035 | — | NE | NE | NE | ISDOC |
| **Švedska** | Peppol BIS 3.0 | NE (istraga pokrenuta) | — | NE | NE | NE | — |

### Ključni zaključci iz tablice

**Izvještavanje o naplati — samo Hrvatska i Španjolska:**

Samo dvije EU zemlje zahtijevaju od obveznika da izvještavaju o naplati eRačuna:
- **Hrvatska** — `EvidentirajNaplatu` kroz eIzvještavanje servis (čl. 53 Zakona o fiskalizaciji)
- **Španjolska** — "Cobros sobre facturas" kroz SII sustav (naplate na izdanim računima)

Nijedna druga zemlja — ni Italija, ni Poljska, ni Rumunjska — ne prati što se događa s računom **nakon** što je izdan/dostavljen.

**Izvještavanje o odbijanju — samo Hrvatska:**

Hrvatska je **jedina EU zemlja** koja zahtijeva formalno izvještavanje o odbijanju eRačuna (`EvidentirajOdbijanje`).

**Oba smjera (izlazni + ulazni) → porezna:**

| Zemlja | Izlazni | Ulazni | Kako |
|---|---|---|---|
| **Hrvatska** | DA | DA | eFiskalizacija — posrednik šalje fiskalizacijsku poruku |
| **Rumunjska** | DA | DA | Clearance — sve prolazi kroz e-Factura platformu |
| **Poljska** | DA | DA | Clearance — sve prolazi kroz KSeF |
| **Italija** | DA | DA | Clearance — sve prolazi kroz SDI |
| **Grčka** | DA | DA | Clearance + klasifikacija na myDATA |
| **Španjolska** | DA | DA | Post-audit — obe strane šalju u SII |
| **Litva** | DA | DA | Post-audit — i.SAF izvještaj (prodajne i nabavne knjige) |

**Zanimljive specifičnosti:**

- **Mađarska** — najširi opseg: **SVE** fakture (B2B + B2C + izvoz) u realnom vremenu, ali samo izdane
- **Danska** — pionir eRačuna od 2005., 20+ godina iskustva
- **Finska** — model "prava na eRačun" (kupac može zahtijevati od dobavljača)
- **Estonija** — "buyer-choice" model (kupac se registrira i forsira dobavljača)
- **Slovačka** — jedina zemlja s "5-corner" modelom (Peppol + PU kao peti kut)
- **Portugal** — ATCUD + QR kod na svakom računu (verifikacija od strane potrošača)
- **Španjolska** — 3 paralelna sustava (SII + Verifactu + TicketBAI) zbog regionalne autonomije

---

## EU-level resursi

| Izvor | Link |
|-------|------|
| EN16931 validacijski artefakti | <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">github.com/ConnectingEurope/eInvoicing-EN16931</a> |
| CEN/TC 434 tehnički odbor | <a href="https://github.com/CenPC434" target="_blank">github.com/CenPC434</a> |
| Peppol BIS Billing 3.0 | <a href="https://docs.peppol.eu/poacc/billing/3.0/bis/" target="_blank">docs.peppol.eu</a> |
| EU CIUS registar | <a href="https://ec.europa.eu/digital-building-blocks/sites/spaces/EINVCOMMUNITY/pages/48763623" target="_blank">EC — Registry of CIUS</a> |

---
