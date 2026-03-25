---
layout: default
title: "eRačun Hrvatska — Datumi i porezna obveza"
---

# eRačun Hrvatska — Datumi i porezna obveza

> **Ovo je inicijalni prijedlog dokumentacije** — morali smo od nečeg početi.
>
> Nismo stručnjaci sveznalice, niti se itko od nas rodio s ovim znanjem. Svima nam je ovo novo — eRačuni su obvezni od 01.01.2026. i svi učimo u hodu. Upravo zato je ova dokumentacija otvorena: da zajedno kao zajednica razradimo i posložimo ove teme na jednom mjestu.
>
> **Ako primijetite grešku — ukažite na nju.** Ako imate bolji primjer — predložite ga. Ako se ne slažete s nečim — pokrenite raspravu. Ostali neka glasaju i komentiraju. Možda se javi i netko iz Porezne uprave ili informacijskih posrednika da potvrdi ili ispravi — svaki takav doprinos je dragocjen.
>
> Ako je nešto krivo napisano — nemojte napadati, jednostavno ukažite na grešku, predložite ispravak i neka ostali glasaju ili komentiraju da li je ispravak valjan. Tako zajedno dolazimo do točnih odgovora.
>
> Cilj nije imati savršen dokument od prvog dana, nego imati **jedno mjesto** gdje možemo zajedno doći do ispravnih odgovora. I da se što prije počnemo svi zajedno smijati kako početkom 2026. ovo nismo znali.
>
> *Prva inicijalna verzija objavljena: 24.03.2026. — Davor Geci*

## Zašto ovo postoji?

Od 01.01.2026. Hrvatska je prešla na obvezni eRačun (Fiskalizacija 2.0). Prijelaz je bio nagao — svi smo odjednom počeli i slati i primati XML račune u EN16931 formatu s hrvatskim proširenjima (HR CIUS 2025).

**Problem**: ulazni eRačuni od različitih izdavatelja dolaze s različitim postavkama datumskih polja. Jedni koriste BT-7, drugi BT-8, treći ni jedno. A svi ti datumi utječu na to **u koje porezno razdoblje ulazi PDV**. Ali nije samo problem ulaznih računa — ni mi koji kreiramo izlazne eRačune nismo sigurni da ih ispravno generiramo. Uključujući i mene — i zato sam pokrenuo ovaj repozitorij.

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

- **Besplatan** — za čitanje ne treba ni registracija, za komentiranje treba samo besplatna prijava koja kreira korisnički račun (2 min registracije)
- **Transparentan** — svaka promjena je vidljiva s autorom i datumom, ništa se ne može tiho promijeniti
- **Verzioniran** — svaka izmjena je trajno sačuvana, moguće je vidjeti cijelu povijest dokumenta
- **Rasprave i glasanje** — <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions" target="_blank">Discussions</a> omogućuju strukturirane rasprave s emoji glasanjem (👍 👎 🤔)
- **Koriste ga institucije i zakonodavci diljem svijeta**:
  - <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">EU / EN16931</a> — specifikacije i schematron validatori za europski eRačun koje i mi koristimo
  - <a href="https://github.com/IRS-Public/direct-file" target="_blank">IRS (američka porezna uprava)</a> — porezni softver i <a href="https://github.com/IRS-Public/fact-graph" target="_blank">strojno čitljivi porezni zakoni</a> na GitHubu
  - <a href="https://github.com/DCCouncil/law-xml" target="_blank">Washington DC</a> — prvi zakonodavac koji je prihvatio izmjenu zakona od građanina kroz Pull Request
  - <a href="https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework" target="_blank">EU Digital Identity Wallet</a> — arhitektura europskog digitalnog identiteta razvija se otvoreno na GitHubu

Ako niste sigurni kako GitHub funkcionira, pogledajte **<a href="https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/GITHUB-VODIC.md" target="_blank">Vodič za GitHub</a>** — objašnjeno je korak po korak, za potpune početnike. Tu se nalaze i <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/GITHUB-VODIC.md#tko-još-koristi-github-za-zakone-i-propise" target="_blank">dodatni primjeri institucija</a> koje koriste GitHub.

### Kako sudjelovati?

| Što želite? | Gdje? |
|-------------|-------|
| Postaviti pitanje ili pokrenuti raspravu | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions" target="_blank">Discussions</a> |
| Prijaviti grešku u dokumentaciji | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/issues" target="_blank">Issues</a> |
| Predložiti izmjenu teksta | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/pulls" target="_blank">Pull Requests</a> |
| Glasati za prijedlog | Emoji reakcije (👍 👎) na postojećim raspravama |
| Samo čitati | Upravo ste na pravom mjestu — registracija nije potrebna |

Detaljne upute: <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a>

## Licenca

<a href="https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12" target="_blank">EUPL 1.2</a> — slobodno koristite, dijelite i prilagođavajte — ista licenca koju koristi i EU za EN16931 ekosustav.
