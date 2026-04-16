# Sastanci

Ovaj direktorij sadrži automatski generirane sažetke radnih sastanaka u kojima se pregledava dokumentacija projekta eRačun / fiskalizacija.

## Kako se sažeci generiraju

Svaki sastanak ima svoj **milestone** u GitHub repozitoriju. Konvencija naziva:

```
Sastanak-YYYY-MM-DD
```

Kada se milestone **zatvori**, radni tok (workflow) [`meeting-summary.yml`](../.github/workflows/meeting-summary.yml) automatski:

1. pročita sve Issue-ove (otvorene i zatvorene) povezane s tim milestone-om,
2. pronađe sve Pull Request-e koji referenciraju te Issue-ove,
3. generira markdown datoteku `YYYY-MM-DD-sazetak.md` u ovom direktoriju,
4. sprema je na `main` s porukom `docs(sastanci): sažetak za ... [skip ci]`.

## Ručno pokretanje

Moguće je i ručno pokrenuti radni tok preko **Actions → Generate meeting summary → Run workflow**, uz unos `milestone_number`.

## Struktura datoteke sažetka

Svaki sažetak sadrži:

- naslov milestone-a (npr. `Sastanak-2026-04-20`)
- datum sastanka (iz `due_on` milestone-a, ili `closed_at` ako nije postavljen)
- popis Issue-ova s njihovim statusom (otvoren / zatvoren + `status:` oznaka)
- popis Pull Request-ova koji referenciraju te Issue-ove

## Napomena

Datoteke u ovom direktoriju **ne uređujte ručno** — bit će prepisane pri idućem zatvaranju istog milestone-a. Ako treba ispraviti sažetak, izmijenite Issue / milestone metapodatke i ponovno pokrenite radni tok.
