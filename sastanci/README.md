# Sastanci

Ovaj direktorij sadrži automatski generirane sumare radnih sastanaka u kojima se pregledava dokumentacija projekta eRačun / fiskalizacija.

## Kako se sumari generiraju

Svaki sastanak ima svoj **milestone** u GitHub repozitoriju. Konvencija naziva:

```
Sastanak-YYYY-MM-DD
```

Kada se milestone **zatvori**, workflow [`meeting-summary.yml`](../.github/workflows/meeting-summary.yml) automatski:

1. pročita sve issue-e (otvorene i zatvorene) povezane s tim milestone-om,
2. pronađe sve pull request-e koji referenciraju te issue-e,
3. generira markdown datoteku `YYYY-MM-DD-sumar.md` u ovom direktoriju,
4. commita ju na `main` s porukom `docs(sastanci): sumar za ... [skip ci]`.

## Ručno pokretanje

Moguće je i ručno pokrenuti workflow preko **Actions → Generate meeting summary → Run workflow**, uz unos `milestone_number`.

## Struktura datoteke sumara

Svaki sumar sadrži:

- naslov milestone-a (npr. `Sastanak-2026-04-20`)
- datum sastanka (iz `due_on` milestone-a, ili `closed_at` ako nije postavljen)
- popis issue-a s njihovim statusom (otvoren / zatvoren + `status:` label)
- popis pull request-ova koji referenciraju te issue-e

## Napomena

Datoteke u ovom direktoriju **ne uređujte ručno** — bit će prepisane pri idućem zatvaranju istog milestone-a. Ako treba ispraviti sumar, izmijenite issue / milestone metapodatke i ponovno pokrenite workflow.
