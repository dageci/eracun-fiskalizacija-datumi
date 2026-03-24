---
layout: default
title: "eRačun Hrvatska — Datumi i porezna obveza"
---

# eRačun Hrvatska — Datumi i porezna obveza

Dokumentacija o datumskim poljima u hrvatskom eRačunu (HR CIUS 2025 / EN16931) i njihovom utjecaju na nastanak obveze PDV-a.

## Zašto ovo postoji?

Od 01.01.2026. Hrvatska je prešla na obvezni eRačun (Fiskalizacija 2.0). Prijelaz je bio nagao — svi smo odjednom počeli i slati i primati XML račune u EN16931 formatu s hrvatskim proširenjima (HR CIUS 2025).

**Problem**: ulazni eRačuni od različitih izdavatelja dolaze s različitim postavkama datumskih polja. Jedni koriste BT-7, drugi BT-8, treći ni jedno. A svi ti datumi utječu na to **u koje porezno razdoblje ulazi PDV**.

U grupama i forumima se otvaraju beskonačna pitanja o istim temama. Cilj ovog repozitorija je da sva ta znanja budu **na jednom mjestu** — strukturirano, s primjerima i zakonskim temeljem. **Svatko može doprinijeti**: ispraviti grešku, dodati primjer, ukazati na slučaj koji nedostaje.

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

Ova dokumentacija je otvorena za sve — **svatko može komentirati, predložiti ispravku ili dodati primjer**. Upravo zato koristimo GitHub.

### Zašto GitHub?

- **Besplatan** — za čitanje ne treba ni registracija, za komentiranje treba samo besplatni račun (2 min registracije)
- **Transparentan** — svaka promjena je vidljiva s autorom i datumom, ništa se ne može tiho promijeniti
- **Verzioniran** — svaka izmjena je trajno sačuvana, moguće je vidjeti cijelu povijest dokumenta
- **Rasprave i glasanje** — [Discussions](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) omogućuju strukturirane rasprave s emoji glasanjem (👍 👎 🤔)
- **Koristi ga i Europska komisija** — EN16931 specifikacije i schematron validatori se razvijaju na GitHubu

Ako niste sigurni kako GitHub funkcionira, pogledajte **[Vodič za GitHub](https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/GITHUB-VODIC.md)** — objašnjeno je korak po korak, za potpune početnike.

### Kako sudjelovati?

| Što želite? | Gdje? |
|-------------|-------|
| Postaviti pitanje ili pokrenuti raspravu | [Discussions](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) |
| Prijaviti grešku u dokumentaciji | [Issues](https://github.com/dageci/eracun-fiskalizacija-datumi/issues) |
| Predložiti izmjenu teksta | [Pull Requests](https://github.com/dageci/eracun-fiskalizacija-datumi/pulls) |
| Glasati za prijedlog | Emoji reakcije (👍 👎) na postojećim raspravama |
| Samo čitati | Upravo ste na pravom mjestu — registracija nije potrebna |

Detaljne upute: [CONTRIBUTING.md](https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/CONTRIBUTING.md)

## Licenca

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — slobodno koristite, dijelite i prilagođavajte uz navođenje autora i dijeljenje pod istim uvjetima.
