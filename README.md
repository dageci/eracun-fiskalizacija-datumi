# eRačun Hrvatska — Datumi i porezna obveza

**Web stranica**: [dageci.github.io/eracun-fiskalizacija-datumi](https://dageci.github.io/eracun-fiskalizacija-datumi/) — formatirani prikaz s dijagramima i navigacijom, ne zahtijeva registraciju

> **Ovo je inicijalni prijedlog dokumentacije** — morali smo od nečeg početi.
>
> Svima nam je ovo novo — eRačuni su obvezni od 01.01.2026. i svi učimo u hodu. Dobijem 1000 ulaznih XML-ova i većina ih tretira datumske pojmove po zidarski — "tak je špaga vudrila". Ni mi koji kreiramo izlazne eRačune nismo sigurni da ih ispravno generiramo. Uključujući i mene.
>
> **Plan**: skupiti i razraditi primjere kao zajednica, a onda pozvati relevantnu osobu ili tim iz Porezne uprave koji su radili na Fiskalizacija 2.0 projektu da revidira dokument. Da imamo **jedan izvor istine** kojeg onda svi možemo koristiti — za korekcije softvera, izgradnju novih sustava i referenciranje u stručnim literaturama. Da porezni i financijski stručnjaci imaju sigurnost u automatskoj obradi i ulaznih i izlaznih XML eRačuna, i da svi radimo po istom principu.
>
> **Otvoreni poziv Poreznoj upravi**: Ovaj projekt rado prepuštamo u vlasništvo Poreznoj upravi ili Ministarstvu financija — logično je da službena dokumentacija o eRačunima živi pod službenim okriljem. GitHub omogućuje transparentno upravljanje dokumentacijom s verzioniranjem, obavijestima o promjenama i sudjelovanjem zajednice — pristup koji se koristi za EN16931 specifikacije na EU razini. Dodavanje sadržaja na web stranice s datumima u zagradama bez mogućnosti obavijesti i praćenja promjena napustilo se još u 90-tima — GitHub to rješava elegantno i besplatno.
>
> Ako je nešto krivo napisano — nemojte napadati, jednostavno ukažite, predložite ispravak i neka ostali glasaju. I da se što prije počnemo svi zajedno smijati kako početkom 2026. ovo nismo znali.
>
> *Prva inicijalna verzija objavljena: 24.03.2026. — Davor Geci*

## Zašto ovo postoji?

Od 01.01.2026. Hrvatska je prešla na obvezni eRačun (Fiskalizacija 2.0). U grupama i forumima se otvaraju beskonačna pitanja o istim temama:

- *"Koji datum određuje PDV — datum računa ili datum isporuke?"*
- *"Što je BT-7, a što BT-8 i mogu li oba biti u XML-u?"*
- *"Kako funkcionira obračun po naplati u eRačunu?"*
- *"Zašto mi validator odbija račun s TaxPointDate?"*
- *"Što znači DescriptionCode 432?"*

Cilj je da sva ta znanja budu **na jednom mjestu** — strukturirano, s primjerima, zakonskim temeljem i XML isječcima. Svatko može doprinijeti.

### Dokumentacija pokriva:

- **Datumska polja** u eRačunu (BT-2, BT-7, BT-8, BT-72, BT-73, BT-74, HR-BT-2, HR-BT-15) — što je što, kada se koristi, kako se međusobno isključuju
- **Schematron validacijska pravila** — koja kombinacija prolazi validator, a koja ne (sva su `flag="fatal"`)
- **Primjeri iz prakse** — konkretni scenariji s XML isječcima (isporuka u drugom mjesecu, predujam, odobrenje, kontinuirana usluga, obračun po naplati...)
- **Razliku između datuma za PDV i datuma u knjigovodstvu** — jer to nije isto i često se miješa
- **Zakonski temelj** — članci iz Zakona o PDV-u i Zakona o fiskalizaciji na koje se sve oslanja

## Sadržaj

### [eracun-datumi-poreza-workflow.md](eracun-datumi-poreza-workflow.md)

Glavni dokument koji pokriva:

1. **Pregled polja** — BT oznake, XML elementi, hrvatski nazivi, obaveznost
2. **Ključno pravilo BR-CO-03** — BT-7 i BT-8 su međusobno isključivi
   - Dozvoljene kombinacije
   - Što određuje datum poreza, a što NE (BT-73/BT-74 su samo informativni!)
   - Brojčanik računa i BT-2
   - Flowchart dijagrami (Mermaid) za oba scenarija
3. **Mogući kodovi za BT-8** — 3 (IssueDate), 35 (ActualDeliveryDate), 432 (datum plaćanja)
4. **Primjeri iz prakse**
   - A: Isporuka i račun isti dan
   - B: Isporuka u drugom mjesecu
   - C: Obračun po naplaćenoj naknadi (čl. 125.i)
   - D: Svi datumi u različitim mjesecima (5 potprimjera + usporedna tablica)
   - E: Račun izdan prije isporuke (čl. 30 st. 2)
   - F: Predujam / avansni račun (čl. 30 st. 5)
   - G: Odobrenje / CreditNote
5. **Datumi na eRačunu vs. datumi u knjigovodstvu** — razlika između PDV-a, rashoda, pretporeza i poreza na dobit
6. **XML struktura** — pozicija elemenata u UBL shemi
7. **Validacijska pravila** — Schematron pravila (sva `flag="fatal"`)
8. **Zakonski temelj** — Zakon o PDV-u, Zakon o fiskalizaciji, EN16931, HR CIUS 2025

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
