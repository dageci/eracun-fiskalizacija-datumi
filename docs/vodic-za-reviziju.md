---
layout: default
title: "Vodič za reviziju"
nav_order: 11
---

# Vodič za sudionike radne skupine

Ovaj vodič opisuje kako je organiziran proces pregleda i potvrde dokumentacije. Namijenjen je stručnjacima — programerima, računovođama, poreznim savjetnicima i predstavnicima Porezne uprave — koji žele doprinijeti reviziji sadržaja.

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## 1. Što je cilj procesa? {#sec-cilj-procesa}

Dokumentacija obrađuje datumska polja, porezni tretman i prijedloge za validator u Fiskalizaciji 2.0. Svaki segment (H2 ili H3 sekcija) predstavlja jedno zaokruženo tumačenje koje može biti:

- **potvrđeno** — nakon pregleda stručnjak potvrdi ispravnost,
- **ispravljeno** — nakon rasprave izmjena se primjenjuje kroz Pull Request,
- **odbačeno** — sekcija se briše ako se dokaže da je neutemeljena.

Konačni cilj jest da dokumentacija postane **jedinstveni izvor istine** koji i programeri, računovođe i Porezna uprava mogu navoditi s povjerenjem.

---

## 2. Kako je sve organizirano u GitHubu {#sec-organizacija-github}

Cijeli proces teče kroz GitHub — javno, transparentno i s trajnim audit trailom. Evo ključnih pojmova:

| Pojam | Značenje |
|-------|----------|
| **Issue** | Jedan "zahtjev za reviziju" — postoji po jedan za svaki segment dokumentacije |
| **Pull Request (PR)** | Prijedlog izmjene dokumenta — referencira Issue, nakon odobrenja se primjenjuje |
| **Label** | Oznaka na Issue-u (stranica, tip, status, prioritet) — omogućuje filtriranje |
| **Milestone** | Grupa Issueova vezana za konkretan sastanak (npr. "Sastanak 1 — 20.04.2026.") |
| **Project Board** | Kanban tablica sa stupcima koja prikazuje gdje je koji Issue |

Svaki segment dokumentacije ima **stabilni ID** u obliku `sec-xxx` koji se ne mijenja čak i kada se naslov ispravi. ID je osnova za povezivanje Issueova, PR-ova i segmenata.

---

## 3. Stanja revizije (Kanban stupci) {#sec-stanja-revizije}

Svaki segment prolazi kroz jedno od sljedećih stanja:

| Stanje | Kada ovdje | Tko djeluje |
|--------|-----------|-------------|
| 🟡 **Za pregled** | Segment postoji, nitko još nije započeo pregled | Bilo tko može započeti |
| 🔵 **U reviziji** | Aktivna rasprava u Issue-u | Sudionici rasprave |
| ⏸️ **Čeka Poreznu upravu** | Raspravljeno, čeka službeno pojašnjenje PU | Predstavnik PU |
| 🟢 **Potvrđeno** | Odobreno i primijenjeno u dokumentaciji | — |
| ⚠️ **Traži izmjenu** | Uočeno da segment treba ispraviti | Autor PR-a |
| ⚪ **Izvan revizije** | Autorski sadržaj, uvod, vodič — po defaultu ne traži reviziju | Opcionalno |
| ❌ **Odbačeno** | Odlučeno da se segment briše ili ne uključuje | — |

---

## 4. Kada koristiti Issue, a kada Discussion? {#sec-issue-vs-discussion}

GitHub nudi dva različita alata za komunikaciju: **Issues** i **Discussions**. Oba su dostupna u ovom projektu i imaju različite svrhe.

| Kriterij | **Issues** | **Discussions** |
|----------|-----------|-----------------|
| **Vezano za** | Konkretan segment (H2 / H3 s ID-em `sec-xxx`) | Opću temu, pitanje, iskustvo |
| **Životni ciklus** | Otvoren → U reviziji → Potvrđeno / Zatvoreno | Nema — rasprava teče dok god postoji interes |
| **Automatizacija** | Ulazi u Kanban ploču, mijenja badge na stranici, broji se u dashboard | Nema automatskog praćenja statusa |
| **Kada koristiti** | Traženje pregleda, ispravak, potvrda, prijedlog promjene jednog segmenta | Šira pitanja, iskustva iz prakse, prijedlozi za nove sekcije, "brain-storming" |
| **Pretraga** | Filtrirati se može po oznakama (label) — stranica, status, tip | Filtrirati se može po kategorijama |
| **Tko odgovara** | Urednik ili recenzent donosi odluku | Cijela zajednica diskutira |

### Primjeri kada koristiti **Issue** {#sec-primjeri-issue}

- *"Segment `sec-hr-bt-15` ima pogrešno tumačenje čl. 125.i — predlažem izmjenu..."*
- *"Potvrđujemo ispravnost segmenta `sec-bt-7-vs-m`"*
- *"Tablica u segmentu `sec-kada-se-koje` krivo prikazuje BT-9 za slučaj X"*
- *"Nedostaje primjer za kombinaciju BT-7 + HR-BT-15 u predujmu"*

### Primjeri kada koristiti **Discussion** {#sec-primjeri-discussion}

- *"Kako drugi ERP-ovi implementiraju storno predujma?"*
- *"Imamo li nešto za validaciju BT-25 kod storno dokumenata?"*
- *"Iskustva s MER API-jem 2.3 — što kod vas radi, što ne radi?"*
- *"Prijedlog za potpuno novu stranicu: specifičnosti za OPG-ove"*
- *"Kako Porezna uprava službeno tumači prijelaz godine kod obračuna po naplati?"*

### Što ako nisam siguran? {#sec-ako-nisam-siguran}

Pravilo palca: **ako se tvoja napomena veže za konkretan naslov sekcije**, otvori Issue. **Ako se veže za širu temu ili više segmenata istovremeno**, otvori Discussion. Ako kasnije ispadne da trebaš drugo, moderator može prebaciti Discussion u Issue (ili obratno).

Otvori ih ovdje:
- **Issues:** [github.com/dageci/eracun-fiskalizacija-datumi/issues](https://github.com/dageci/eracun-fiskalizacija-datumi/issues)
- **Discussions:** [github.com/dageci/eracun-fiskalizacija-datumi/discussions](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions)

---

## 5. Kako započeti reviziju jednog segmenta {#sec-kako-zapoceti}

### Korak 1: Pronađite segment koji vas zanima

Otvorite listu Issueova:

→ [github.com/dageci/eracun-fiskalizacija-datumi/issues](https://github.com/dageci/eracun-fiskalizacija-datumi/issues)

Filtrirati možete po:
- **Stranici** — label `stranica:pravila`, `stranica:primjeri-izdavatelj`, itd.
- **Statusu** — label `status:ceka` (još nitko nije pogledao)
- **Prioritetu** — `prioritet:visok`
- **Tipu sadržaja** — `tip:xml-primjer`, `tip:citat-zakona`

### Korak 2: Pročitajte segment u dokumentaciji

U Issue-u se nalazi poveznica na točnu sekciju dokumentacije. Klik na nju otvara stranicu pozicioniranu na odgovarajući naslov.

### Korak 3: Ostavite komentar na Issue-u

Ovdje postoje tri mogućnosti:

**A) Potvrda ispravnosti**

Ako smatrate da je sadržaj ispravan:
> *"Potvrđujemo. Sadržaj odgovara važećim propisima i praksi."*

Ako želite, dodajte kratko obrazloženje i izvor (npr. članak zakona, odluku CJEU, službenu uputu).

**B) Prijedlog izmjene**

Ako uočite pogrešku ili predlažete poboljšanje:
> *"Predlažemo izmjenu: [opis što biste promijenili]. Razlog: [tehnički/pravni/praktični]. Izvor: [poveznica na zakon, specifikaciju, odluku]."*

**C) Zahtjev za pojašnjenje**

Ako niste sigurni što autor misli:
> *"Molimo pojašnjenje: [pitanje]."*

### Korak 4: Rasprava

Ostali sudionici mogu odgovoriti, potvrditi vaše stajalište ili predložiti alternativu. Cilj je postići **konsenzus** prije bilo kakve izmjene dokumenta.

### Korak 5: Izmjena

Kada se postigne konsenzus, izmjena se primjenjuje kroz Pull Request. Autor dokumentacije ili bilo koji drugi sudionik otvara PR koji:

- referencira ovaj Issue (`Closes #42`),
- sadrži točno dogovorenu izmjenu,
- navodi sudionike rasprave i datum odluke.

PR mora biti **odobren** od odgovornog recenzenta prije nego što se spoji u glavnu verziju.

---

## 6. Kako sudjelovati u PR reviziji {#sec-pr-revizija}

Ako ste označeni kao recenzent Pull Requesta:

### Pregled promjene
- Otvorite PR na GitHubu
- Kliknite karticu **Files changed** — tamo vidite točno što se mijenja (zeleno = dodano, crveno = uklonjeno)
- Pročitajte diff rečenicu po rečenicu

### Davanje povratne informacije

Kliknite **Review changes** i odaberite jednu od tri opcije:

- **Approve** — slažem se, spremno za spajanje
- **Request changes** — potrebne su dodatne izmjene (opišite što)
- **Comment** — imam pitanja ili komentare bez blokiranja

Komentari se mogu ostaviti na konkretne linije diff-a — klik na broj linije → strelica → polje za komentar.

---

## 7. Kako otvoriti novi Issue (ako još ne postoji) {#sec-novi-issue}

Većina Issueova je već automatski generirana za postojeće segmente. Ako uočite:

- **Nedostatak sadržaja** koji bi trebao biti u dokumentaciji, ili
- **Potrebu za potpuno novom sekcijom**,

možete otvoriti novi Issue:

→ [github.com/dageci/eracun-fiskalizacija-datumi/issues/new/choose](https://github.com/dageci/eracun-fiskalizacija-datumi/issues/new/choose)

Odaberite template **"Revizija segmenta dokumentacije"** i ispunite polja.

---

## 8. Sastanci radne skupine {#sec-sastanci}

### Organizacija

Periodično se organiziraju radni sastanci (uživo ili putem video poziva) na kojima se prolazi skupina segmenata. Svaki sastanak ima **Milestone** u GitHubu (npr. `Sastanak 1 — 20.04.2026.`) s popisom Issueova za obradu.

### Prije sastanka

- Moderator dodjeljuje Issueove Milestone-u
- Sudionici mogu unaprijed ostaviti komentare na Issueove

### Tijekom sastanka

- Prolazi se Issue po Issue
- Donose se odluke koje se odmah upisuju u Issue komentare
- Za svaku izmjenu se otvara PR (moderator ili autor)

### Nakon sastanka

- GitHub Actions automatski generira **sažetak sastanka** (`sastanci/YYYY-MM-DD-sazetak.md`)
- Sažetak sadrži: sudionike, popis obrađenih Issueova, odluke, otvorene PR-ove, zadatke za sljedeći sastanak

---

## 9. Kako se AI asistenti uključuju u proces {#sec-kako-ai}

Za tehnički složenije izmjene — osobito kod Mermaid dijagrama, tablica, XML primjera ili HTML vizualizacija — sudionici mogu zatražiti pomoć autora koji se služi modernim **AI asistentima** (umjetna inteligencija specijalizirana za razvoj softvera i dokumentacije) za primjenu dogovorenih izmjena.

**Tipičan tok**:

1. U Issue-u se postigne konsenzus
2. Autor otvara AI asistenta s pristupom repozitoriju
3. Referencira Issue i opisuje dogovorenu izmjenu
4. AI primjenjuje izmjenu, sprema (commit) i otvara PR koji referencira Issue
5. Sudionici pregledavaju PR i odobravaju ili traže daljnje izmjene

Ovaj pristup je posebno koristan kada izmjena zahvaća Mermaid dijagrame ili druge vizualne elemente koje je teško editirati ručno. Krajnju odluku o prihvaćanju izmjene uvijek donose ljudi — AI je samo alat koji ubrzava mehanički dio posla.

---

## 10. Česta pitanja {#sec-fap}

### Trebam li biti programer da sudjelujem?

Ne. GitHub korisničko sučelje omogućuje komentiranje, potvrdu i otvaranje Issueova bez ikakvog programerskog znanja. Potrebno je samo:
- Besplatan GitHub račun
- Sposobnost čitanja dokumentacije i davanja stručnog mišljenja

### Trebam li instalirati nešto?

Ne. Sve se radi kroz web preglednik na github.com.

### Što ako primijetim pogrešku izvan svog stručnog područja?

Ostavite komentar na odgovarajućem Issue-u. Netko tko razumije temu će pristupiti raspravi.

### Kako mogu pratiti što se događa?

Na GitHubu kliknite **Watch** na repozitoriju i odaberite razinu obavijesti. Dobivat ćete email za svaku aktivnost ili samo za teme u kojima sudjelujete. Detalji: [Email obavijesti](github-obavijesti).

### Što ako se ne slažem s donesenom odlukom?

Otvorite novi Issue ili komentirajte postojeći. Odluke se mogu preispitati. Git povijest čuva sve prethodne verzije.

---

## 11. Dodatni resursi {#sec-resursi}

- [Dashboard napretka revizije](napredak)
- [Otvoreni Issueovi](https://github.com/dageci/eracun-fiskalizacija-datumi/issues)
- [Zatvoreni Issueovi (arhiva)](https://github.com/dageci/eracun-fiskalizacija-datumi/issues?q=is%3Aissue+is%3Aclosed)
- [Pull Requestovi](https://github.com/dageci/eracun-fiskalizacija-datumi/pulls)
- [Discussions (opće rasprave)](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions)
- [Povijest promjena (CHANGELOG)](https://github.com/dageci/eracun-fiskalizacija-datumi/blob/master/CHANGELOG.md)
- [Sažeci sastanaka](https://github.com/dageci/eracun-fiskalizacija-datumi/tree/master/sastanci)

---

**Hvala što doprinosite ovoj inicijativi.** Svaka stručna potvrda, ispravka ili pitanje doprinosi da dokumentacija postane pouzdan referentni izvor za sve koji rade s eRačunima u Hrvatskoj.
