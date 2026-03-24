# eRačun Hrvatska — Datumi i porezna obveza

Dokumentacija o datumskim poljima u hrvatskom eRačunu (HR CIUS 2025 / EN16931) i njihovom utjecaju na nastanak obveze PDV-a.

## Zašto ovo postoji?

Datumi na eRačunu su jedno od najčešćih područja zabune kod ERP programera i knjigovođa u Hrvatskoj. Europska norma EN16931 definira više datumskih polja (BT-2, BT-7, BT-8, BT-72, BT-73, BT-74) koja se međusobno isključuju, nadopunjuju ili ignoriraju — ovisno o poslovnom scenariju.

Hrvatski CIUS 2025 dodaje vlastita pravila (HR-BR-2, HR-BR-40, HR-BR-48...) i HR ekstenzije (HR-BT-2, HR-BT-15) koje dalje kompliciraju situaciju.

Ovaj dokument nastoji sve to objasniti na jednom mjestu, s primjerima iz prakse.

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

Pogledajte [CONTRIBUTING.md](CONTRIBUTING.md) za upute o raspravama, prijavama grešaka i pull requestovima.

---

*Inicijalno kreirano: 2026-03-24*
*Autor: Davor Geci*
*Uz pomoć AI alata*
