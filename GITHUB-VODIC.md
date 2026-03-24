# Zašto GitHub i kako sudjelovati

## Što je GitHub?

GitHub je **besplatna platforma** za suradnju na dokumentima i kodu. Koriste ga milioni programera, tvrtki i organizacija diljem svijeta — uključujući Europsku komisiju za EN16931 specifikacije.

Ovaj projekt koristi GitHub jer:

- **Besplatan je** — za javne projekte nema nikakvih troškova, ni za autore ni za suradnike
- **Transparentan** — svaka promjena je vidljiva, s autorom i datumom
- **Otvoren** — svatko može pregledati dokumente bez registracije
- **Verzioniran** — svaka izmjena je sačuvana, moguće je vidjeti povijest i vratiti se na stariju verziju
- **Omogućuje suradnju** — komentari, rasprave, prijedlozi izmjena, glasanje
- **GitHub Pages** — automatski generira web stranicu iz dokumentacije

## Koliko košta?

**Ništa.** GitHub je besplatan za javne projekte. Čitanje dokumentacije, pregled povijesti izmjena i pristup web stranici ne zahtijeva ni registraciju.

Za aktivno sudjelovanje (komentare, rasprave, prijedloge) potrebna je **besplatna prijava koja kreira korisnički račun** — traje 2 minute na [github.com](https://github.com/signup).

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

Ako želite sami predložiti izmjenu:

1. Kliknite na datoteku koju želite izmijeniti
2. Kliknite ikonu olovke (Edit)
3. Napravite izmjenu
4. Kliknite "Propose changes"
5. GitHub automatski kreira Pull Request koji autor pregledava

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

Projekt koristi **CC BY-SA 4.0** licencu — slobodno koristite, dijelite i prilagođavajte uz:
- Navođenje autora
- Dijeljenje pod istim uvjetima

Puni tekst: [creativecommons.org/licenses/by-sa/4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

*Imate pitanje o korištenju GitHuba? Otvorite [Discussion](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) — rado ćemo pomoći.*
