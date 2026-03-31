# eRačun Hrvatska — Datumi i porezna obveza

### Gdje čitati?

| | Link | Za koga |
|---|---|---|
| **Web stranica** | [dageci.github.io/eracun-fiskalizacija-datumi](https://dageci.github.io/eracun-fiskalizacija-datumi/) | Za čitanje — formatirani prikaz s navigacijom, dijagramima i tooltipovima. Ne zahtijeva registraciju. |
| **GitHub repo** | [github.com/dageci/eracun-fiskalizacija-datumi](https://github.com/dageci/eracun-fiskalizacija-datumi) | Za sudjelovanje — povijest izmjena, rasprave, prijedlozi ispravaka, glasanje. Komentiranje zahtijeva besplatnu registraciju (2 min). |

Web stranica se automatski generira iz ovog repozitorija — sadržaj je isti, razlika je u prikazu i mogućnosti suradnje.

> **Ovo je inicijalni prijedlog dokumentacije** — morali smo od nečeg početi.
>
> Svima nam je ovo novo — eRačuni su obvezni od 01.01.2026. i svi učimo u hodu. Dobijem 1000 ulaznih XML-ova i većina ih tretira datumske pojmove po zidarski — "tak je špaga vudrila". Badava imate u kompaniji 20 pravnika i financijskih stručnjaka ako dobivate ulazne XML-e koji su popunjeni po tom principu — nemoguće je uspostaviti automatsko učitavanje eRačuna. Ni mi koji kreiramo izlazne eRačune nismo sigurni da ih ispravno generiramo. Uključujući i mene.
>
> **Plan**: skupiti i razraditi primjere kao zajednica, a onda pozvati relevantnu osobu ili tim iz Porezne uprave koji su radili na Fiskalizacija 2.0 projektu da revidira dokument. Da imamo **jedan izvor istine** kojeg onda svi možemo koristiti — za korekcije softvera, izgradnju novih sustava i referenciranje u stručnim literaturama. Da porezni i financijski stručnjaci imaju sigurnost u automatskoj obradi i ulaznih i izlaznih XML eRačuna, i da svi radimo po istom principu.
>
> **Otvoreni poziv Poreznoj upravi**: Ovaj projekt rado prepuštamo u vlasništvo Poreznoj upravi ili Ministarstvu financija — logično je da službena dokumentacija o eRačunima živi pod službenim okriljem. GitHub omogućuje transparentno upravljanje dokumentacijom s verzioniranjem, automatskim obavijestima o promjenama i sudjelovanjem zajednice — isti pristup koji EU koristi za [EN16931 specifikacije](https://github.com/ConnectingEurope/eInvoicing-EN16931). Besplatan je i otvoren za sve.
>
> Ako je nešto krivo napisano — nemojte napadati, jednostavno ukažite, predložite ispravak i neka ostali glasaju. I da se što prije počnemo svi zajedno smijati kako početkom 2026. ovo nismo znali.
>
> *Prva inicijalna verzija objavljena: 24.03.2026. — Davor Geci*

> [!CAUTION]
> **Ovo NIJE službena uputa.** Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. Dokument je prijedlog zajednice namijenjen za raspravu. **Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca** — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.
>
> Kad pojedini primjeri i zaključci budu službeno potvrđeni ili opovrgnuti, označit ćemo ih odgovarajućim statusom.

## Zašto ovo postoji?

Od 01.01.2026. Hrvatska je prešla na obvezni eRačun (Fiskalizacija 2.0). U grupama i forumima se otvaraju beskonačna pitanja o istim temama:

- *"Koji datum određuje PDV — datum računa ili datum isporuke?"*
- *"Što je BT-7, a što BT-8 i mogu li oba biti u XML-u?"*
- *"Kako funkcionira obračun po naplati u eRačunu?"*
- *"Zašto mi validator odbija račun s TaxPointDate?"*
- *"Što znači DescriptionCode 432?"*

Cilj je da sva ta znanja budu **na jednom mjestu** — strukturirano, s primjerima, zakonskim temeljem i XML isječcima. Svatko može doprinijeti.

### Konkretan primjer: HR-BT-15 vs BT-8=432

Obračun PDV-a po naplaćenoj naknadi (čl. 125.i) mora se označiti u eRačunu. Za to postoje **dva elementa** — `BT-8=432` iz EU norme i `HR-BT-15` iz HR proširenja — koji nose istu informaciju. BT-7 i BT-8 **postoje** u UBL CreditNote XSD shemi kao opcionalni elementi, ali se u praksi za odobrenja ne koriste. No nigdje nije eksplicitno objašnjeno moraju li se koristiti oba, samo jedan, ili je ovo nenamjerno dupliciranje.

**Upravo ovakva pitanja su razlog zašto je ovaj dokument nastao** — trebamo odgovor od radne skupine, Porezne uprave ili zakonodavca. Detaljna analiza: [sekcija 3.1 na stranici Pravila i mehanizmi](https://dageci.github.io/eracun-fiskalizacija-datumi/pravila#31-bt-8432-i-hr-bt-15--obračun-po-naplati-u-dva-elementa).

### Dokumentacija

| Stranica | Opis |
|----------|------|
| [Pravila i mehanizmi](https://dageci.github.io/eracun-fiskalizacija-datumi/pravila) | BT polja, BR-CO-03, flowcharti, HR-BT-15 specifičnost, koji datum čemu služi |
| [Primjeri — izdavatelj](https://dageci.github.io/eracun-fiskalizacija-datumi/primjeri-izdavatelj) | 16 primjera s XML isječcima — koji element staviti za koji slučaj |
| [Primjeri — primatelj](https://dageci.github.io/eracun-fiskalizacija-datumi/primjeri-primatelj) | 12 primjera — pretporez, rashod, skladišna primka + pretporez detaljno (čl. 57/60, CJEU) |
| [Europska usporedba](https://dageci.github.io/eracun-fiskalizacija-datumi/europska-usporedba) | 23 EU zemlje — modeli razmjene, izvještavanje prema poreznoj |
| [Prijedlozi za validator](https://dageci.github.io/eracun-fiskalizacija-datumi/prijedlozi-validator) | 16 pravila (HR-BR-GECI-F01–F08, W01–W08) |
| [Referenca](https://dageci.github.io/eracun-fiskalizacija-datumi/referenca) | XML struktura, Schematron pravila, zakonski temelj |

## Temelj dokumentacije

| Izvor | Verzija |
|-------|---------|
| [EN16931](https://ec.europa.eu/digital-building-blocks/sites/display/DIGITAL/EN16931) | UBL 2.1 |
| HR CIUS 2025 | Specifikacija osnovne uporabe eRačuna s proširenjima (12.03.2026) |
| HR Schematron | HRUBLSchematron_13032026-2 |
| Zakon o PDV-u | NN 73/13, zadnje izmjene NN 152/24 (primjena od 01.01.2026) |
| Zakon o fiskalizaciji | NN 89/25 (primjena od 01.01.2026) |
| Pravilnik o PDV-u | NN 79/13, zadnje izmjene NN 11/26 |

## Dijagrami

Dokument koristi [Mermaid](https://mermaid.js.org/) dijagrame. Za prikaz:
- **GitHub** — renderira Mermaid nativno
- **VS Code** — instalirajte extension "Markdown Preview Mermaid Support"
- **Online** — [mermaid.live](https://mermaid.live/)

## Licenca

[EUPL 1.2](LICENSE) — slobodno koristite, dijelite i prilagođavajte — ista licenca koju koristi i EU za EN16931 ekosustav.

## Doprinos

- [GITHUB-VODIC.md](GITHUB-VODIC.md) — **Što je GitHub, zašto ga koristimo i kako sudjelovati** (za početnike)
- [GITHUB-OBAVIJESTI.md](GITHUB-OBAVIJESTI.md) — **Kako dobivati obavijesti o promjenama na email** (Watch, filtriranje, primjeri po ulozi)
- [CONTRIBUTING.md](CONTRIBUTING.md) — Upute za rasprave, prijave grešaka i pull requestove

---

*Inicijalno kreirano: 2026-03-24*
*Autor: Davor Geci*
*Uz pomoć AI alata*
