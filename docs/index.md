---
layout: default
title: "eRačun Hrvatska — Datumi i porezna obveza"
---

# eRačun Hrvatska — Datumi i porezna obveza

> **Ovo je inicijalni prijedlog dokumentacije** — morali smo od nečeg početi.
>
> Svima nam je ovo novo — eRačuni su obvezni od 01.01.2026. i svi učimo u hodu. Dobijem 1000 ulaznih XML-ova i većina ih tretira datumske pojmove po zidarski — "tak je špaga vudrila". Badava imate u kompaniji 20 pravnika i financijskih stručnjaka ako dobivate ulazne XML-e koji su popunjeni po tom principu — nemoguće je uspostaviti automatsko učitavanje eRačuna. Ni mi koji kreiramo izlazne eRačune nismo sigurni da ih ispravno generiramo. Uključujući i mene.
>
> **Plan**: skupiti i razraditi primjere kao zajednica, a onda pozvati relevantnu osobu ili tim iz Porezne uprave koji su radili na Fiskalizacija 2.0 projektu da revidira dokument. Da imamo **jedan izvor istine** kojeg onda svi možemo koristiti — za korekcije softvera, izgradnju novih sustava i referenciranje u stručnim literaturama. Da svi koji rade s eRačunima — programeri, računovođe, porezni savjetnici — imaju sigurnost u automatskoj obradi i ulaznih i izlaznih XML eRačuna, i da svi radimo po istom principu.
>
> **Otvoreni poziv Poreznoj upravi**: Ovaj projekt rado prepuštamo u vlasništvo Poreznoj upravi ili Ministarstvu financija — logično je da službena dokumentacija o eRačunima živi pod službenim okriljem. GitHub omogućuje transparentno upravljanje dokumentacijom s verzioniranjem, automatskim obavijestima o promjenama i sudjelovanjem zajednice — isti pristup koji EU koristi za [EN16931 specifikacije](https://github.com/ConnectingEurope/eInvoicing-EN16931). Besplatan je i otvoren za sve. Prednost nad klasičnim web stranicama: svaka izmjena dokumenta je automatski vidljiva s datumom i autorom, zainteresirani se mogu pretplatiti na obavijesti, i svatko može predložiti ispravak — bez čekanja na sljedeću objavu.
>
> Ako je nešto krivo napisano — nemojte napadati, jednostavno ukažite, predložite ispravak i neka ostali glasaju. I da se što prije počnemo svi zajedno smijati kako početkom 2026. ovo nismo znali.
>
> *Prva inicijalna verzija objavljena: 24.03.2026. — Davor Geci*

### Sadržaj {#sec-sadrzaj}
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. Dokument je prijedlog zajednice namijenjen za raspravu. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.<br><br>
Kad pojedini primjeri i zaključci budu službeno potvrđeni ili opovrgnuti, označit ćemo ih odgovarajućim statusom: <span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Potvrđeno</span> <span style="display:inline-block;background:#e74c3c;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Opovrgnuto</span> <span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span>
</div>

---

## Konkretan primjer: zašto ovo postoji {#sec-konkretan-primjer-zasto}
Obračun PDV-a po naplaćenoj naknadi (čl. 125.i) mora se označiti u eRačunu. Za to postoje **dva elementa** — `BT-8=432` iz EU norme i `HR-BT-15` iz HR proširenja — koji nose istu informaciju. Iz primjera u dokumentaciji vidljivo je da je HR-BT-15 uvijek prisutan (svojstvo obveznika), dok BT-8=432 nije uvijek korišten u praksi (npr. predujam koristi BT-7 umjesto BT-8). Napomena: i BT-7 i BT-8 **postoje** u UBL CreditNote XSD shemi kao opcionalni elementi, ali se u primjerima iz specifikacije za odobrenja ne koriste — za CreditNote po naplati, BT-8=432 bi se teoretski mogao koristiti, što znači da HR-BT-15 nije nužno jedini signal za obračun po naplati. No nigdje u specifikaciji nije eksplicitno objašnjeno moraju li se koristiti oba, samo jedan, ili je ovo nenamjerno dupliciranje.

Upravo ovakva pitanja — na koja **samo Porezna uprava ili radna skupina** mogu dati konačan odgovor — su razlog nastanka ovog dokumenta. Detaljna analiza s XML primjerima: [sekcija 3.1 na stranici Pravila i mehanizmi](pravila#31-bt-8432-i-hr-bt-15--obračun-po-naplati-u-dva-elementa).

---

## Dokumentacija {#sec-dokumentacija}
| Stranica | Opis | Tko čita |
|----------|------|----------|
| [Pravila i mehanizmi](pravila) | BT polja, BR-CO-03, flowcharti, kodovi za BT-8, koji datum čemu služi | Svi |
| [Primjeri — izdavatelj](primjeri-izdavatelj) | 16 primjera s XML isječcima — koji element staviti za koji slučaj | Programeri, izdavatelji |
| [Primjeri — primatelj](primjeri-primatelj) | 12 primjera — pretporez, rashod, skladišna primka + pretporez detaljno (čl. 57/60, CJEU) | Računovođe, primatelji |
| [Referenca — XML, validacija, zakoni](referenca) | XML struktura, Schematron pravila, zakonski temelj | Programeri, svi |
| [Europska usporedba](europska-usporedba) | 23 EU zemlje — modeli razmjene, izvještavanje prema poreznoj, dokumentacija | Svi |
| [Naknadno dospjeli računi](naknadno-dospjeli-racuni) | Prijelazno razdoblje 2025→2026, kasno fakturiranje, IOS, sudske presude | Računovođe, svi |
| [Prijedlozi za validator](prijedlozi-validator) | 21 pravilo koje bi validator mogao uhvatiti na razini posrednika | Programeri, posrednici |
| [Indikator kopije](indikator-kopije) | CopyIndicator / indikatorKopije — kada se smije koristiti, koja polja se ne smiju mijenjati | Programeri, svi |
| [Analiza ulaznih XML-ova](analiza-ulaznih) | 1.283 eRačuna iz prakse — statistika polja, pronađeni problemi, HR-BT-15 potvrda | Svi |

## Službeni izvori i zakoni {#sec-sluzbeni-izvori-i-zakoni}
| Izvor | Link |
|-------|------|
| Zakon o PDV-u (pročišćeni tekst) | <a href="https://www.zakon.hr/z/1455/zakon-o-porezu-na-dodanu-vrijednost" target="_blank">zakon.hr</a> |
| Zakon o fiskalizaciji | <a href="https://www.zakon.hr/z/3960/zakon-o-fiskalizaciji" target="_blank">zakon.hr</a> |
| HR CIUS specifikacija + validator | <a href="https://porezna.gov.hr/fiskalizacija/bezgotovinski-racuni/eracun" target="_blank">porezna.gov.hr/eracun</a> |
| EN16931 (EU norma, Schematron) | <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">github.com/ConnectingEurope</a> |
| Fiskalizacija 2.0 — vodič PU | <a href="https://porezna-uprava.gov.hr/hr/vodic-kroz-fiskalizaciju-2-0-8151/8151" target="_blank">porezna-uprava.gov.hr</a> |

Kompletni popis zakona, pravilnika i izvora: [Referenca — zakonski temelj](referenca#8-zakonski-temelj)

## Licenca {#sec-licenca}
<a href="https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12" target="_blank">EUPL 1.2</a> — slobodno koristite, dijelite i prilagođavajte — ista licenca koju koristi i EU za EN16931 ekosustav.
