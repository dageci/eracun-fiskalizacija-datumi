# Kako dobivati obavijesti o promjenama na email

Možete postaviti da vas GitHub automatski obavještava emailom kad se nešto promijeni u ovom projektu — nova rasprava, izmjena dokumenta, novi prijedlog ili komentar. I možete odabrati **samo ono što vas zanima**.

## Preduvjet: besplatna prijava na GitHub

Za obavijesti trebate GitHub korisnički račun. Prijava je besplatna i traje 2 minute: [github.com/signup](https://github.com/signup)

---

## Korak 1: Otvorite repo i kliknite Watch

1. Idite na **[github.com/dageci/eracun-fiskalizacija-datumi](https://github.com/dageci/eracun-fiskalizacija-datumi)**
2. U gornjem desnom kutu vidjet ćete gumb **Watch** (s ikonom oka)
3. Kliknite na njega — otvori se padajući izbornik

## Korak 2: Odaberite razinu obavijesti

GitHub nudi 4 opcije:

### Opcija 1: Participating and @mentions (zadano)
> Dobivate obavijesti samo ako:
> - Sudjelujete u raspravi (napisali ste komentar)
> - Netko vas označi (@vaše-ime)
>
> **Za koga**: Ako želite mir i dobivati obavijesti samo kad vas se tiče.

### Opcija 2: All Activity
> Dobivate obavijesti za **sve** — svaka nova rasprava, svaki komentar, svaka izmjena dokumenta, svaki pull request.
>
> **Za koga**: Ako želite biti u toku sa svime što se događa u projektu.

### Opcija 3: Custom
> **Najkorisnija opcija** — odabirete točno što vas zanima. Kliknite "Custom" i označite:
>
> | Opcija | Što dobivate | Primjer |
> |--------|-------------|---------|
> | **Issues** | Obavijest kad netko prijavi grešku ili komentira prijavu | "Greška u Primjeru D.2 — krivi članak zakona" |
> | **Pull requests** | Obavijest kad netko predloži izmjenu dokumenta | "Dodan primjer za avansni račun s predujmom u EUR" |
> | **Releases** | Obavijest kad se objavi nova verzija | "Verzija 2.0 — dodani svi primjeri za kontinuirane usluge" |
> | **Discussions** | Obavijest kad netko pokrene ili komentira raspravu | "Pitanje: Kako tretirati BT-7 kod povrata robe?" |
> | **Security alerts** | Obavijesti o sigurnosnim problemima | (rijetko za dokumentacijski projekt) |
>
> **Preporuka za ovaj projekt**: Označite **Discussions** i **Pull requests** — to su dvije najvažnije aktivnosti.

### Opcija 4: Ignore
> Ne dobivate nikakve obavijesti, čak ni kad vas netko označi.
>
> **Za koga**: Ako ne želite nikakve obavijesti iz ovog projekta.

---

## Primjeri: Što odabrati ovisno o vašoj ulozi

### "Ja sam knjigovođa, zanima me samo kad se promijeni sadržaj dokumenta"
→ Odaberite **Custom** → označite samo **Pull requests**

Dobit ćete email kad netko predloži izmjenu teksta (npr. ispravak članka zakona, novi primjer). Nećete dobivati obavijesti o raspravama i komentarima.

### "Ja sam ERP programer, želim pratiti rasprave o implementaciji"
→ Odaberite **Custom** → označite **Discussions** i **Pull requests**

Dobit ćete email za svaku novu raspravu (pitanja, prijedlozi) i za svaku predloženu izmjenu dokumenta.

### "Želim znati sve što se događa"
→ Odaberite **All Activity**

Dobit ćete email za svaku aktivnost — nove rasprave, komentari, izmjene, prijave grešaka.

### "Zanima me samo kad izađe nova verzija dokumenta"
→ Odaberite **Custom** → označite samo **Releases**

Dobit ćete email samo kad autor objavi novu verziju (npr. nakon veće revizije ili potvrde od Porezne uprave).

---

## Kako promijeniti ili isključiti obavijesti naknadno

1. Idite na **[github.com/dageci/eracun-fiskalizacija-datumi](https://github.com/dageci/eracun-fiskalizacija-datumi)**
2. Kliknite **Watch** (gumb u gornjem desnom kutu)
3. Promijenite opciju ili odaberite **Ignore** za isključivanje

Možete i centralno upravljati svim obavijestima na: **[github.com/settings/notifications](https://github.com/settings/notifications)**

---

## Kako filtrirati obavijesti u email klijentu

Ako dobivate previše emailova, možete ih filtrirati u svom email programu:

### Gmail
1. Otvorite email od GitHub notifikacije
2. Kliknite tri točkice → "Filter messages like this"
3. Dodajte pravilo: `from:notifications@github.com` i `subject:dageci/eracun-fiskalizacija-datumi`
4. Odaberite akciju: automatski označi labelom "eRačun" ili premjesti u folder

### Outlook
1. Desni klik na email → "Rules" → "Create Rule"
2. Uvjet: From = `notifications@github.com`, Subject contains = `eracun-fiskalizacija-datumi`
3. Akcija: premjesti u folder "eRačun"

### Općenito
GitHub obavijesti dolaze s adrese `notifications@github.com` i u subject liniji uvijek sadrže `dageci/eracun-fiskalizacija-datumi`. To možete koristiti za filtriranje u bilo kojem email klijentu.

---

## Kako pratiti samo jednu raspravu (bez praćenja cijelog projekta)

Ako vas zanima samo jedna konkretna rasprava:

1. Otvorite tu raspravu (Discussion ili Issue)
2. U desnom sidebaru kliknite **Subscribe** (ikona zvonca)
3. Dobit ćete obavijesti samo za tu jednu raspravu

Ovo radi neovisno o Watch postavkama na razini projekta.

---

*Imate pitanje o obavijestima? Otvorite [Discussion](https://github.com/dageci/eracun-fiskalizacija-datumi/discussions) — rado ćemo pomoći.*
