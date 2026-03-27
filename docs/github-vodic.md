---
layout: default
title: "Zašto GitHub"
nav_order: 3
has_toc: false
---

# Zašto GitHub i kako sudjelovati

## Što je GitHub?

GitHub je **besplatna platforma** za suradnju na dokumentima i kodu. Koriste ga milijuni programera, tvrtki i organizacija diljem svijeta — uključujući Europsku komisiju za EN16931 specifikacije.

Ovaj projekt koristi GitHub jer:

- **Besplatan je** — za javne projekte nema nikakvih troškova, ni za održavatelje ni za suradnike
- **Transparentan** — svaka promjena je vidljiva, s održavateljem i datumom
- **Otvoren** — svatko može pregledati dokumente bez registracije
- **Verzioniran** — svaka izmjena je sačuvana, moguće je vidjeti povijest i vratiti se na stariju verziju
- **Omogućuje suradnju** — komentari, rasprave, prijedlozi izmjena, glasanje
- **GitHub Pages** — automatski generira web stranicu iz dokumentacije

## Koliko košta?

**Ništa.** GitHub je besplatan za javne projekte. Čitanje dokumentacije, pregled povijesti izmjena i pristup web stranici ne zahtijeva ni registraciju.

Za aktivno sudjelovanje (komentare, rasprave, prijedloge) potrebna je **besplatna prijava koja kreira korisnički račun** — traje 2 minute na [github.com](https://github.com/signup).

## Tko još koristi GitHub za zakone i propise?

GitHub nije samo za programere — koriste ga državne institucije, porezne uprave i zakonodavci diljem svijeta za otvorenu suradnju na propisima i dokumentaciji.

### Europska unija

| Projekt | Opis | Link |
|---------|------|------|
| **EN16931 eInvoicing** | Specifikacije i schematron validatori za europski eRačun — isti standard koji i mi koristimo. Issues i rasprave su otvorene za sve. | [ConnectingEurope/eInvoicing-EN16931](https://github.com/ConnectingEurope/eInvoicing-EN16931) |
| **CEN/TC 434** | Tehnički odbor za elektroničko fakturiranje koji održava EN16931 normu. | [CenPC434](https://github.com/CenPC434) |
| **EU Digital Identity Wallet** | Arhitektura i referentni okvir za europski digitalni identitet — razvija se potpuno otvoreno. | [eu-digital-identity-wallet](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework) |
| **EU Open Source Strategy** | Strategija EU za otvoreni kod — "Towards European Open Digital Ecosystems". | [GitHub Blog](https://github.blog/news-insights/policy-news-and-insights/help-shape-the-future-of-open-source-in-europe/) |

### Porezne uprave

| Projekt | Opis | Link |
|---------|------|------|
| **IRS Direct File** | Američka porezna uprava (IRS) objavila besplatni softver za podnošenje poreznih prijava kao open source. | [IRS-Public/direct-file](https://github.com/IRS-Public/direct-file) |
| **IRS Fact Graph** | Američki porezni zakoni u strojno čitljivom formatu — deklarativni okvir za interpretaciju poreznih pravila. | [IRS-Public/fact-graph](https://github.com/IRS-Public/fact-graph) |

### Zakonodavci

| Projekt | Opis | Link |
|---------|------|------|
| **Washington DC** | Prvi zakonodavac na svijetu koji je objavio zakone na GitHubu i prihvatio izmjenu od građanina kroz Pull Request. | [DCCouncil/law-xml](https://github.com/DCCouncil/law-xml) |
| **Francuska (Legifrance)** | Francuski zakoni dostupni u strojno čitljivom formatu. | [Legifrance projekti](https://github.com/topics/legifrance) |
| **Government Open Source Policies** | Zbirka pristupa vlada diljem svijeta prema open source softveru. | [github/government-open-source-policies](https://github.com/github/government-open-source-policies) |

### Velike tvrtke

| Tvrtka | Opis | Link |
|--------|------|------|
| **Microsoft** | **Cjelokupna** dokumentacija (learn.microsoft.com) je na GitHubu — 800+ repozitorija. Svaki članak ima "Edit" gumb za predlaganje izmjena. | [MicrosoftDocs](https://github.com/MicrosoftDocs) |
| **Google** | Dokumentacija za Android, Kubernetes, TensorFlow, Go i stotine drugih projekata — sve otvoreno za doprinose. | [google](https://github.com/google) |
| **Meta (Facebook)** | React, React Native i ostala dokumentacija razvija se otvoreno na GitHubu. | [facebook](https://github.com/facebook) |

> **Poanta**: Ako Microsoft koristi GitHub za svu svoju dokumentaciju,
> američka porezna uprava za porezne zakone, a Europska komisija za
> eRačun specifikacije — onda je GitHub apsolutno prikladno mjesto
> za zajedničku dokumentaciju o hrvatskim eRačunima.

## Kako čitati dokumentaciju?

### Na web stranici (najjednostavnije)
Otvorite [dageci.github.io/eracun-fiskalizacija-datumi](https://dageci.github.io/eracun-fiskalizacija-datumi/) — formatirani prikaz s dijagramima, tablicama i navigacijom. Ne treba registracija.

### Na GitHubu
Otvorite [github.com/dageci/eracun-fiskalizacija-datumi](https://github.com/dageci/eracun-fiskalizacija-datumi) — GitHub automatski prikazuje Markdown datoteke s formatiranjem i Mermaid dijagramima. Ne treba registracija.

## Kako sudjelovati?

### 1. Rasprave (Discussions) — za pitanja i prijedloge

Najbolje mjesto za početak. Otvorite [Discussions](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) i:

- **Postavite pitanje** — ako nešto nije jasno u dokumentaciji
- **Predložite poboljšanje** — novi primjer, slučaj koji nije pokriven, ispravka
- **Podijelite iskustvo** — kako vaš ERP rješava ove scenarije
- **Glasajte** — koristite emoji reakcije (👍 👎 🤔) na postojećim prijedlozima

Za ovo trebate besplatnu prijavu na GitHub (kreira korisnički račun).

### 2. Prijava greške (Issues) — za konkretne probleme

Ako pronađete grešku (krivi članak zakona, netočan XML primjer, pogrešna BT oznaka):

1. Otvorite [Issues](https://github.com/dageci/eracun-fiskalizacija-datumi/issues)
2. Kliknite "New Issue"
3. Opišite što je krivo i što bi trebalo pisati
4. Navedite izvor (članak zakona, schematron pravilo, specifikacija)

### 3. Pull Request — za direktne izmjene teksta

**Najlakši način**: Na svakoj stranici dokumentacije postoji gumb **"✏️ Uredi ovu stranicu"** koji vas vodi direktno na GitHub editor za tu stranicu. Napravite izmjenu u tekstu i kliknite "Propose changes".

**Što se onda događa? Ništa se ne mijenja odmah!** Vaša izmjena NE ide direktno na stranicu — ona se šalje kao **prijedlog** (Pull Request) koji održavatelj mora pregledati i odobriti. Tek kad održavatelj klikne "Merge", izmjena postaje vidljiva na web stranici. Dakle slobodno predlažite — ne možete ništa pokvariti. U najgorem slučaju, održavatelj odbije prijedlog s obrazloženjem.

Koraci:

1. Kliknite **"✏️ Uredi ovu stranicu"** na web stranici (ili ikonu olovke na GitHubu)
2. GitHub vam otvori editor s tekstom stranice
3. Napravite izmjenu
4. Kliknite **"Propose changes"** i kratko opišite što ste promijenili
5. GitHub automatski kreira **Pull Request** — prijedlog izmjene
6. Održavatelj dobije obavijest, pregledava izmjenu, komentira ili odobrava
7. Tek kad održavatelj klikne **"Merge"** — izmjena postaje vidljiva na web stranici

Ili za naprednije korisnike:
1. Forkajte repo
2. Napravite promjene u svom forku
3. Otvorite Pull Request s opisom što ste promijenili i zašto

### 4. Samo čitanje — bez registracije

Ako samo želite čitati dokumentaciju, ne trebate ništa — otvorite web stranicu ili GitHub repo i čitajte.

## Tko može sudjelovati?

Svi koji rade s hrvatskim eRačunima:

- **ERP programeri** — koji implementiraju kreiranje eRačun XML-a
- **Knjigovođe** — koji moraju razumjeti kako datumi utječu na PDV
- **Informacijski posrednici** — koji procesiraju eRačune (MER, PONDI, Fina)
- **Porezni savjetnici** — koji poznaju zakonski okvir
- **Studenti** — koji uče o e-fakturiranju

## GitHub pojmovi na hrvatskom

Ako vam je GitHub sučelje na engleskom, evo što znače ključni pojmovi:

| GitHub pojam | Hrvatski | Što znači |
|---|---|---|
| **Star** | Zvjezdica | Označite projekt kao koristan — kao "sviđa mi se". Pomaže da projekt bude vidljiviji drugima. |
| **Watch** | Pratite | Pratite promjene — dobivate obavijesti o novim raspravama i izmjenama dokumentacije. |
| **Fork** | Kopija | Napravite svoju kopiju projekta na vašem računu, za predlaganje izmjena. |
| **Issue** | Prijava | Prijavite grešku ili problem u dokumentaciji. |
| **Pull Request** | Prijedlog izmjene | Predložite konkretnu izmjenu teksta koju održavatelj pregledava i prihvaća ili odbija. |
| **Discussion** | Rasprava | Otvorena rasprava — pitanja, prijedlozi, iskustva. |
| **New Issue** | Nova prijava | Gumb za kreiranje nove prijave greške. |
| **Propose changes** | Predloži izmjene | Gumb koji se pojavi kad editirate datoteku na GitHubu. |
| **Maintainer** | Održavatelj | Osoba koja pregledava prijedloge izmjena i upravlja projektom. |

## Što je Markdown?

Dokumentacija je napisana u **Markdown** formatu — jednostavan tekstualni format koji GitHub automatski prikazuje s formatiranjem (naslovi, tablice, linkovi, code blokovi). Ne trebate nikakav poseban softver — možete editirati u bilo kojem text editoru.

Primjer:
```
## Ovo je naslov
**Ovo je bold tekst**
- Ovo je lista
| Ovo | je | tablica |
```

## Što su Mermaid dijagrami?

Dokumentacija koristi [Mermaid](https://mermaid.js.org/) dijagrame za vizualizaciju workflow-a. GitHub ih automatski renderira. Ako koristite VS Code, instalirajte extension "Markdown Preview Mermaid Support".

## Licenca

Projekt koristi **EUPL 1.2** licencu — slobodno koristite, dijelite i prilagođavajte uz:
- Navođenje autora
- Dijeljenje pod istim uvjetima

Puni tekst: [joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)

---

*Imate pitanje o korištenju GitHuba? Otvorite [Discussion](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) — rado ćemo pomoći.*
