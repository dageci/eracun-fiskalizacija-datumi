---
layout: default
title: "eRačun Hrvatska — Datumi i porezna obveza"
---

# eRačun Hrvatska — Datumi i porezna obveza

Dokumentacija o datumskim poljima u hrvatskom eRačunu (HR CIUS 2025 / EN16931) i njihovom utjecaju na nastanak obveze PDV-a.

## Zašto ovo postoji?

Datumi na eRačunu su jedno od najčešćih područja zabune kod ERP programera i knjigovođa u Hrvatskoj. Europska norma EN16931 definira više datumskih polja (BT-2, BT-7, BT-8, BT-72, BT-73, BT-74) koja se međusobno isključuju, nadopunjuju ili ignoriraju — ovisno o poslovnom scenariju.

Hrvatski CIUS 2025 dodaje vlastita pravila (HR-BR-2, HR-BR-40, HR-BR-48...) i HR ekstenzije (HR-BT-2, HR-BT-15) koje dalje kompliciraju situaciju.

## Dokumentacija

| Dokument | Opis |
|----------|------|
| [Datumi i porezna obveza — kompletni workflow](eracun-datumi-poreza-workflow) | Glavni dokument s dijagramima, primjerima i zakonskim temeljem |

## Što pokriva dokumentacija?

### Polja i pravila
- **BT-2** / Datum izdavanja računa (`cbc:IssueDate`) — obavezno
- **HR-BT-2** / Vrijeme izdavanja (`cbc:IssueTime`) — obavezno u HR
- **BT-7** / Datum nastanka obveze PDV-a (`cbc:TaxPointDate`) — eksplicitni datum
- **BT-8** / Kod datuma PDV obveze (`cbc:DescriptionCode`) — kod (3, 35, 432)
- **BT-72** / Stvarni datum isporuke (`cbc:ActualDeliveryDate`)
- **BT-73/BT-74** / Obračunsko razdoblje (`cbc:StartDate`/`cbc:EndDate`)
- **HR-BT-15** / Obračun po naplaćenoj naknadi (`hrextac:HRObracunPDVPoNaplati`)
- **BR-CO-03** — BT-7 i BT-8 su međusobno isključivi (`flag="fatal"`)

### Primjeri iz prakse
- Isporuka i račun isti dan
- Isporuka u drugom mjesecu od računa
- Obračun po naplaćenoj naknadi (čl. 125.i)
- Svi datumi u različitim mjesecima (5 potprimjera)
- Račun izdan prije isporuke (čl. 30 st. 2)
- Predujam / avansni račun (čl. 30 st. 5)
- Odobrenje / CreditNote
- Kontinuirana usluga s obračunskim razdobljem

### Dodatne teme
- Razlika između datuma za PDV i datuma za priznavanje rashoda u knjigovodstvu
- XML struktura — pozicija elemenata u UBL shemi
- Schematron validacijska pravila (sva `flag="fatal"`)
- Zakonski temelj — Zakon o PDV-u, Zakon o fiskalizaciji, EN16931

## Temelj dokumentacije

| Izvor | Verzija |
|-------|---------|
| EN16931 | UBL 2.1 |
| HR CIUS 2025 | Specifikacija osnovne uporabe eRačuna s proširenjima (12.03.2026) |
| HR Schematron | HRUBLSchematron_13032026-2 |
| Zakon o PDV-u | NN 73/13, zadnje izmjene NN 152/24 (primjena od 01.01.2026) |
| Zakon o fiskalizaciji | NN 89/25 (primjena od 01.01.2026) |
| Pravilnik o PDV-u | NN 79/13, zadnje izmjene NN 11/26 |

## Doprinos i rasprava

- [Što je GitHub i kako sudjelovati](https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/GITHUB-VODIC.md) — za početnike, besplatno
- [GitHub Discussions](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) — pitanja, prijedlozi, iskustva
- [Issues](https://github.com/dageci/eracun-fiskalizacija-datumi/issues) — prijava grešaka
- [Pull Requests](https://github.com/dageci/eracun-fiskalizacija-datumi/pulls) — doprinosi
- [CONTRIBUTING.md](https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/CONTRIBUTING.md) — upute za doprinos

Licenca: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — slobodno koristite, dijelite i prilagođavajte uz navođenje autora.
