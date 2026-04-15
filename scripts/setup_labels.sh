#!/usr/bin/env bash
# Kreira sve potrebne labels na GitHub repozitoriju
# Pokrenuti: bash scripts/setup_labels.sh
set -e

REPO="dageci/eracun-fiskalizacija-datumi"

# Funkcija za siguran create-or-update
label() {
  local name="$1"
  local color="$2"
  local desc="$3"
  gh label create "$name" --repo "$REPO" --color "$color" --description "$desc" --force
}

echo "=== Labels za stranice ==="
label "stranica:pravila"              "1f77b4" "Stranica: Pravila i mehanizmi"
label "stranica:primjeri-izdavatelj"  "2ca02c" "Stranica: Primjeri — izdavatelj"
label "stranica:primjeri-primatelj"   "17becf" "Stranica: Primjeri — primatelj"
label "stranica:referenca"            "9467bd" "Stranica: Referenca"
label "stranica:europska-usporedba"   "bcbd22" "Stranica: Europska usporedba"
label "stranica:naknadno-dospjeli"    "ff7f0e" "Stranica: Naknadno dospjeli računi"
label "stranica:prijedlozi-validator" "e377c2" "Stranica: Prijedlozi za validator"
label "stranica:indikator-kopije"     "7f7f7f" "Stranica: Indikator kopije"
label "stranica:analiza-ulaznih"      "8c564b" "Stranica: Analiza ulaznih XML-ova"
label "stranica:index"                "d62728" "Stranica: Početna"

echo ""
echo "=== Labels za status revizije ==="
label "status:ceka"              "fbca04" "Čeka pregled"
label "status:u-reviziji"        "1d76db" "U reviziji — aktivna rasprava"
label "status:ceka-pu"           "c5def5" "Čeka službeni odgovor PU"
label "status:potvrdeno"         "0e8a16" "Potvrđeno — odobreno i u dokumentaciji"
label "status:trazi-izmjenu"     "d93f0b" "Traži izmjenu — ispravak potreban"
label "status:odbaceno"          "b60205" "Odbačeno"
label "status:izvan-revizije"    "ededed" "Izvan revizije — autorski sadržaj"

echo ""
echo "=== Labels za tip sadržaja ==="
label "tip:tekst"          "f9d0c4" "Tekstualni sadržaj"
label "tip:tablica"        "fef2c0" "Tablica"
label "tip:mermaid-graf"   "c2e0c6" "Mermaid dijagram"
label "tip:xml-primjer"    "bfd4f2" "XML primjer"
label "tip:citat-zakona"   "d4c5f9" "Citat iz zakona ili specifikacije"
label "tip:slika"          "fad8c7" "Slika ili screenshot"
label "tip:autorsko"       "f0f0f0" "Autorski sadržaj — ne treba reviziju"

echo ""
echo "=== Labels za prioritet ==="
label "prioritet:kritican"  "b60205" "Kritičan — odmah"
label "prioritet:visok"     "d93f0b" "Visoki prioritet"
label "prioritet:srednji"   "fbca04" "Srednji prioritet"
label "prioritet:nizak"     "0e8a16" "Niski prioritet"

echo ""
echo "Gotovo. Pregled svih labels:"
gh label list --repo "$REPO" | head -40
