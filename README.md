# eRačun Hrvatska — Datumi i porezna obveza

> **Ovo je inicijalni prijedlog dokumentacije** — morali smo od nečeg početi.
>
> Nismo stručnjaci sveznalice, niti se itko od nas rodio s ovim znanjem. Svima nam je ovo novo — eRačuni su obvezni od 01.01.2026. i svi učimo u hodu. Upravo zato je ova dokumentacija otvorena: da zajedno kao zajednica razradimo i posložimo ove teme na jednom mjestu.
>
> **Ako primijetite grešku — ukažite na nju.** Ako imate bolji primjer — predložite ga. Ako se ne slažete s nečim — pokrenite raspravu. Ostali neka glasaju i komentiraju. Možda se javi i netko iz Porezne uprave ili informacijskih posrednika da potvrdi ili ispravi — svaki takav doprinos je dragocjen.
>
> Ako je nešto krivo napisano — nemojte napadati, jednostavno ukažite na grešku, predložite ispravak i neka ostali glasaju ili komentiraju da li je ispravak valjan. Tako zajedno dolazimo do točnih odgovora.
>
> Cilj nije imati savršen dokument od prvog dana, nego imati **jedno mjesto** gdje možemo zajedno doći do ispravnih odgovora.
>
> *Prva inicijalna verzija objavljena: 24.03.2026.*

Dokumentacija o datumskim poljima u hrvatskom eRačunu (HR CIUS 2025 / EN16931) i njihovom utjecaju na nastanak obveze PDV-a.

## Zašto ovo postoji?

Od 01.01.2026. Hrvatska je prešla na obvezni eRačun (Fiskalizacija 2.0). Prijelaz je bio nagao — svi smo odjednom počeli i slati i primati XML račune u EN16931 formatu s hrvatskim proširenjima (HR CIUS 2025).

**Problem koji je odmah isplivao**: ulazni eRačuni od različitih izdavatelja dolaze s različitim postavkama datumskih polja. Jedni koriste BT-7, drugi BT-8, treći ni jedno. Neki stavljaju BT-72, neki ne. Neki imaju InvoicePeriod, neki nemaju. A svi ti datumi utječu na to **u koje porezno razdoblje ulazi PDV** — što je kritično za ispravnu PDV prijavu.

U Facebook grupama, na forumima i u razgovorima između ERP programera i knjigovođa otvaraju se **beskonačna pitanja i rasprave** o istim temama:
- *"Koji datum određuje PDV — datum računa ili datum isporuke?"*
- *"Što je BT-7, a što BT-8 i mogu li oba biti u XML-u?"*
- *"Kako funkcionira obračun po naplati u eRačunu?"*
- *"Zašto mi validator odbija račun s TaxPointDate?"*
- *"Što znači DescriptionCode 432?"*

**Cilj ovog repozitorija** je da sva ta znanja i odgovori budu **na jednom mjestu** — strukturirano, s primjerima, zakonskim temeljem i XML isječcima. Umjesto da se ista pitanja ponavljaju u 10 različitih grupa, možemo ih ovdje jednom riješiti i svi koristiti.

Ovo nije zatvoreni dokument jedne osobe — **svatko može doprinijeti**: ispraviti grešku, dodati primjer koji nedostaje, ukazati na slučaj koji nismo pokrili. Što više nas sudjeluje, to će dokumentacija biti potpunija i pouzdanija.

### Konkretno, dokumentacija pokriva:

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

[CC BY-SA 4.0](LICENSE) — slobodno koristite, dijelite i prilagođavajte uz navođenje autora i dijeljenje pod istim uvjetima.

## Doprinos

- [GITHUB-VODIC.md](GITHUB-VODIC.md) — **Što je GitHub, zašto ga koristimo i kako sudjelovati** (za početnike)
- [CONTRIBUTING.md](CONTRIBUTING.md) — Upute za rasprave, prijave grešaka i pull requestove

---

*Inicijalno kreirano: 2026-03-24*
*Autor: Davor Geci*
*Uz pomoć AI alata*
