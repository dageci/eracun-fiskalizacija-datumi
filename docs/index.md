---
layout: default
title: "eRačun Hrvatska — Datumi i porezna obveza"
---

# eRačun Hrvatska — Datumi i porezna obveza

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

### Sadržaj
{: .no_toc }

* TOC
{:toc}

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE službena uputa</strong><br>
Sve što je ovdje napisano proizlazi iz autorove analize specifikacija, zakona i prakse. Dokument je prijedlog zajednice namijenjen za raspravu. <strong>Nijedan zaključak nema službenu potvrdu Porezne uprave, radne skupine ni zakonodavca</strong> — dok tu potvrdu ne dobijemo, sadržaj treba tretirati isključivo kao polaznu točku za diskusiju, ne kao uputu za implementaciju.<br><br>
Kad pojedini primjeri i zaključci budu službeno potvrđeni ili opovrgnuti, označit ćemo ih odgovarajućim statusom: <span style="display:inline-block;background:#27ae60;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Potvrđeno</span> <span style="display:inline-block;background:#e74c3c;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Opovrgnuto</span> <span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;">Čeka potvrdu</span>
</div>

---

## Konkretan primjer: zašto ovo postoji

Obračun PDV-a po naplaćenoj naknadi (čl. 125.i) mora se označiti u eRačunu. Za to postoje **dva elementa** — `BT-8=432` iz EU norme i `HR-BT-15` iz HR proširenja — koji nose istu informaciju. Iz primjera u dokumentaciji vidljivo je da je HR-BT-15 uvijek prisutan (svojstvo obveznika), dok BT-8=432 nije uvijek primjenjiv (npr. CreditNote nema BT-8 u shemi, predujam koristi BT-7). No nigdje u specifikaciji nije eksplicitno objašnjeno moraju li se koristiti oba, samo jedan, ili je ovo nenamjerno dupliciranje.

Upravo ovakva pitanja — na koja **samo Porezna uprava ili radna skupina** mogu dati konačan odgovor — su razlog nastanka ovog dokumenta. Detaljna analiza s XML primjerima: [sekcija 3.1 — Pravila i mehanizmi](pravila#31-bt-8432-i-hr-bt-15--obračun-po-naplati-u-dva-elementa).

---

## Dokumentacija

| Stranica | Opis | Tko čita |
|----------|------|----------|
| [Pravila i mehanizmi](pravila) | BT polja, BR-CO-03, flowcharti, kodovi za BT-8, koji datum čemu služi | Svi |
| [Primjeri — izdavatelj](primjeri-izdavatelj) | 16 primjera s XML isječcima — koji element staviti za koji slučaj | Programeri, izdavatelji |
| [Primjeri — primatelj](primjeri-primatelj) | 12 primjera — pretporez, rashod, skladišna primka + pretporez detaljno (čl. 57/60, CJEU) | Računovođe, primatelji |
| [Referenca — XML, validacija, zakoni](referenca) | XML struktura, Schematron pravila, zakonski temelj | Programeri, svi |
| [Europska usporedba](europska-usporedba) | Kako PL, DE, IT, FR, BE dokumentiraju eRačun — i što HR može naučiti | Svi |
| [Prijedlozi za validator](prijedlozi-validator) | Pravila koja bi validator mogao uhvatiti na razini posrednika | Programeri, posrednici |
| [Kompletni dokument (jedna stranica)](eracun-datumi-poreza-workflow) | Sve gore navedeno u jednom dokumentu — za čitanje od početka do kraja | Svi |

## Što pokriva dokumentacija?

### Pravila i mehanizmi → [Pravila](pravila)
- **BR-CO-03** — BT-7 i BT-8 su međusobno isključivi (`flag="fatal"`)
- Flowchart dijagrami za oba režima (po izdavanju i po naplati)
- Kodovi za BT-8 (3, 35, 432) i otvoreno pitanje BT-8=432 vs HR-BT-15

### Primjeri iz prakse — po perspektivi

**Izdavatelj** → [Primjeri — izdavatelj](primjeri-izdavatelj)
- 10 primjera obračun po izdavanju (čl. 30) <span class="badge-izdavanje">Po izdavanju</span>
- 6 primjera obračun po naplati (čl. 125.i) <span class="badge-naplata">Po naplati</span>
- Usporedba svih 5 mehanizama za isti slučaj <span class="badge-usporedba">Usporedba</span>

**Primatelj** → [Primjeri — primatelj](primjeri-primatelj)
- 8 primjera po izdavanju + 4 primjera po naplati — iz kupčeve perspektive
- Za svaki primjer: pretporez, rashod, skladišna primka
- Pretporez detaljno: dva uvjeta (čl. 57 + čl. 60), rok za PDV prijavu, CJEU sudska praksa
- Vremensko razgraničenje troškova, algoritam za ERP

## Temelj dokumentacije i službeni izvori

### Zakoni i pravilnici — <a href="https://narodne-novine.nn.hr" target="_blank">Narodne novine</a> (službeni izvor)

| Propis | NN broj | Službeni tekst |
|--------|---------|----------------|
| Zakon o PDV-u | NN 73/13 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2013_06_73_1451.html" target="_blank">nn.hr — osnovni tekst</a> |
| Zakon o PDV-u — izmjene | NN 152/24 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2024_12_152_2508.html" target="_blank">nn.hr — izmjene za 2026</a> |
| Zakon o PDV-u — izmjene | NN 151/25 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2025_12_151_2262.html" target="_blank">nn.hr — dodatne izmjene</a> |
| Zakon o fiskalizaciji | NN 89/25 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2025_06_89_1233.html" target="_blank">nn.hr — novi zakon s eRačunom</a> |
| Pravilnik o PDV-u — izmjene | NN 11/26 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2026_01_11_90.html" target="_blank">nn.hr — usklađenje za 2026</a> |
| Pravilnik o fiskalizaciji | NN 153/25 | <a href="https://narodne-novine.nn.hr/clanci/sluzbeni/2025_12_153_2278.html" target="_blank">nn.hr — pravilnik uz novi zakon</a> |

> **Pročišćeni tekstovi** (neslužbeni, ali lakši za čitanje):
> <a href="https://www.zakon.hr/z/1455/zakon-o-porezu-na-dodanu-vrijednost" target="_blank">Zakon o PDV-u — zakon.hr</a> ·
> <a href="https://www.zakon.hr/z/3960/zakon-o-fiskalizaciji" target="_blank">Zakon o fiskalizaciji — zakon.hr</a>

### HR CIUS specifikacija i validator — <a href="https://porezna.gov.hr/fiskalizacija/bezgotovinski-racuni/eracun" target="_blank">Porezna uprava</a>

| Dokument | Datum | Link |
|----------|-------|------|
| Specifikacija osnovne uporabe eRačuna s proširenjima | 12.03.2026 | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/196" target="_blank">porezna.gov.hr — preuzimanje</a> |
| Validator (HR Schematron) — u primjeni od 15.03.2026 | 13.03.2026 | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/197" target="_blank">porezna.gov.hr — preuzimanje</a> |
| Primjeri eRačuna | 12.12.2025 | <a href="https://porezna.gov.hr/fiskalizacija/api/dokumenti/158" target="_blank">porezna.gov.hr — preuzimanje</a> |
| Svi dokumenti za eRačun | — | <a href="https://porezna.gov.hr/fiskalizacija/bezgotovinski-racuni/eracun" target="_blank">porezna.gov.hr/eracun</a> |

### EN16931 europska norma — <a href="https://github.com/ConnectingEurope" target="_blank">EU GitHub</a>

| Izvor | Link |
|-------|------|
| EN16931 validacijski artefakti (Schematron, XSLT) | <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">github.com/ConnectingEurope/eInvoicing-EN16931</a> |
| CEN/TC 434 tehnički odbor za eInvoicing | <a href="https://github.com/CenPC434" target="_blank">github.com/CenPC434</a> |

### Porezna uprava — vodiči i podrška

| Izvor | Link |
|-------|------|
| Fiskalizacija 2.0 / eRačun — glavna stranica | <a href="https://porezna.gov.hr/fiskalizacija/bezgotovinski-racuni" target="_blank">porezna.gov.hr</a> |
| Vodič kroz Fiskalizaciju 2.0 | <a href="https://porezna-uprava.gov.hr/hr/vodic-kroz-fiskalizaciju-2-0-8151/8151" target="_blank">porezna-uprava.gov.hr</a> |
| Pitanja i odgovori | <a href="https://porezna-uprava.gov.hr/hr/pitanja-i-odgovori-vezani-uz-zakon-o-fiskalizaciji-8031/8031" target="_blank">porezna-uprava.gov.hr</a> |
| Popis informacijskih posrednika | <a href="https://porezna-uprava.gov.hr/hr/popis-informacijskih-posrednika/8019" target="_blank">porezna-uprava.gov.hr</a> |

## Doprinos i rasprava

Ova dokumentacija je otvorena za sve — **svatko može komentirati, predložiti ispravku ili dodati primjer**. Upravo zato koristimo GitHub.

### Zašto GitHub?

- **Besplatan** — za čitanje ne treba ni registracija, za komentiranje treba samo besplatna prijava koja kreira korisnički račun (2 min registracije)
- **Transparentan** — svaka promjena je vidljiva s održavateljem i datumom, ništa se ne može tiho promijeniti
- **Verzioniran** — svaka izmjena je trajno sačuvana, moguće je vidjeti cijelu povijest dokumenta
- **Rasprave i glasanje** — <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions" target="_blank">Discussions</a> omogućuju strukturirane rasprave s emoji glasanjem (👍 👎 🤔)
- **Koriste ga institucije, tvrtke i zakonodavci diljem svijeta**:
  - <a href="https://github.com/MicrosoftDocs" target="_blank">Microsoft</a> — **cjelokupna** dokumentacija (learn.microsoft.com) je na GitHubu — 800+ repozitorija, svaki članak ima "Edit" gumb
  - <a href="https://github.com/google" target="_blank">Google</a> — Android, Kubernetes, TensorFlow i ostala dokumentacija otvorena za doprinose
  - <a href="https://github.com/ConnectingEurope/eInvoicing-EN16931" target="_blank">EU / EN16931</a> — specifikacije i schematron validatori za europski eRačun koje i mi koristimo
  - <a href="https://github.com/IRS-Public/direct-file" target="_blank">IRS (američka porezna uprava)</a> — porezni softver i <a href="https://github.com/IRS-Public/fact-graph" target="_blank">strojno čitljivi porezni zakoni</a>
  - <a href="https://github.com/DCCouncil/law-xml" target="_blank">Washington DC</a> — prvi zakonodavac koji je prihvatio izmjenu zakona od građanina kroz Pull Request

Ako niste sigurni kako GitHub funkcionira, pogledajte **<a href="/eracun-fiskalizacija-datumi/github-vodic">Vodič za GitHub</a>** — objašnjeno je korak po korak, za potpune početnike. Tu se nalaze i <a href="/eracun-fiskalizacija-datumi/github-vodic#tko-još-koristi-github-za-zakone-i-propise" target="_blank">dodatni primjeri institucija</a> koje koriste GitHub.

### Kako sudjelovati?

| Što želite? | Gdje? |
|-------------|-------|
| Postaviti pitanje ili pokrenuti raspravu | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/discussions" target="_blank">Discussions</a> |
| Prijaviti grešku u dokumentaciji | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/issues" target="_blank">Issues</a> |
| Predložiti izmjenu teksta | <a href="https://github.com/dageci/eracun-fiskalizacija-datumi/pulls" target="_blank">Pull Requests</a> |
| Glasati za prijedlog | Emoji reakcije (👍 👎) na postojećim raspravama |
| Samo čitati | Upravo ste na pravom mjestu — registracija nije potrebna |
| Dobivati obavijesti o promjenama na email | Kliknite **Watch** na <a href="https://github.com/dageci/eracun-fiskalizacija-datumi" target="_blank">GitHub repu</a> — možete odabrati sve promjene ili samo određene (npr. samo rasprave, samo izmjene dokumenta). Detaljne upute: <a href="/eracun-fiskalizacija-datumi/github-obavijesti">Vodič za obavijesti</a> |

Detaljne upute: <a href="/eracun-fiskalizacija-datumi/kako-doprinijeti">CONTRIBUTING.md</a>

## Licenca

<a href="https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12" target="_blank">EUPL 1.2</a> — slobodno koristite, dijelite i prilagođavajte — ista licenca koju koristi i EU za EN16931 ekosustav.
