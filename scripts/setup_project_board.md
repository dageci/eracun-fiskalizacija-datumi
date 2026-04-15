# Kreiranje Project Board-a (ručni koraci)

GitHub Project Board se ne može kreirati kroz default `gh` auth scope. Potrebno je:

## Korak 1: Dodaj scope

```bash
gh auth refresh -s project
```

Ovo otvara browser, klikneš Authorize i vraća se u konzolu.

## Korak 2: Kreiraj Project (GraphQL ili web)

### Opcija A — Kroz web (najjednostavnije, 2 minute)

1. Idi na https://github.com/dageci/eracun-fiskalizacija-datumi
2. Klik na karticu **Projects**
3. Klik **New project** → odaberi **Board** template
4. Naziv: `Revizija dokumentacije`
5. Klikni **Create**

## Korak 3: Podesi stupce

Nakon kreiranja, uredi stupce:

| Stupac | Boja | Odgovara labelu |
|--------|------|-----------------|
| 🟡 Za pregled | Žuta | `status:ceka` |
| 🔵 U reviziji | Plava | `status:u-reviziji` |
| ⏸️ Čeka PU | Svijetlo plava | `status:ceka-pu` |
| 🟢 Potvrđeno | Zelena | `status:potvrdeno` |
| ⚠️ Traži izmjenu | Crvena | `status:trazi-izmjenu` |
| ⚪ Izvan revizije | Siva | `status:izvan-revizije` |
| ❌ Odbačeno | Tamna | `status:odbaceno` |

## Korak 4: Automatski dodaj Issue-ove

U Project settings → **Workflows** → uključi:

- **Auto-add to project** — filter: `is:issue repo:dageci/eracun-fiskalizacija-datumi`
- **Item added to project** — akcija: set status prema labelu

Ovo će automatski gurati nove Issue-ove u odgovarajuće stupce.

## Alternativa: GraphQL API

Ako želiš napraviti kroz CLI nakon `gh auth refresh -s project`:

```bash
# Kreiraj project
gh api graphql -f query='
mutation {
  createProjectV2(input: {
    ownerId: "USER_OR_ORG_ID",
    title: "Revizija dokumentacije"
  }) {
    projectV2 { id }
  }
}'
```

(Ovo je složenije — preporučujem Opciju A kroz web.)
