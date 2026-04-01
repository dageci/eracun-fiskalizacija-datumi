---
layout: default
title: "Analiza ulaznih XML-ova"
has_toc: true
nav_order: 10
---

# Analiza 1.283 ulaznih eRačuna iz prakse

<div style="background: #fff3f3; border-left: 5px solid #e74c3c; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0;">
<strong style="color: #c0392b;">&#9888; Ovo NIJE reprezentativan uzorak</strong><br>
Analiza pokriva 1.283 ulaznih XML eRačuna od triju komitenata za razdoblje 01.01.–28.03.2026. Rezultati pokazuju trendove ali <strong>ne predstavljaju cijelo tržište</strong> — različiti posrednici i softverske kuće mogu imati različite obrasce.
</div>

### Sadržaj
{: .no_toc }

* TOC
{:toc}

---

## 1. Uzorak

| Izvor | Broj XML-ova |
|----------|:---:|
| Komitent A | 285 |
| Komitent B | 754 |
| Komitent C | 244 |
| **Ukupno** | **1.283** |

Datoteke su ulazni eRačuni (primljeni od dobavljača) preuzeti od triju komitenata za period 01.01.–28.03.2026.

---

## 2. Tipovi dokumenata i profili

| Tip dokumenta | Broj | Postotak |
|---|:---:|:---:|
| Invoice (380 i ostali) | 1.262 | 98,4% |
| CreditNote (381) | 20 | 1,6% |
| Ostalo (nečitljiv format) | 1 | 0,1% |

| Poslovni proces | Broj | Postotak |
|---|:---:|:---:|
| P1 (standardni) | 514 | 40,1% |
| P3 | 387 | 30,2% |
| P2 | 156 | 12,2% |
| P7 | 72 | 5,6% |
| P5 | 51 | 4,0% |
| Ostali (P4, P6, P9-P11, P99) | 103 | 8,0% |

---

## 3. Korištenje datumskih polja

| BT polje | Prisutno | % | Komentar |
|---|:---:|:---:|---|
| **BT-2** (IssueDate) | 1.283 | 100% | Obavezno — svi ga imaju |
| **BT-7** (TaxPointDate) | 1.059 | **82%** | Velika većina eksplicitno navodi datum porezne obveze |
| **BT-8** (DescriptionCode) | 15 | **1%** | Gotovo nitko ne koristi BT-8 |
| **BT-9** (DueDate) | 1.159 | **90%** | Od 1.172 s pozitivnim BT-115, 1.159 ima DueDate. 13 krši HR-BR-4 |
| **BT-72** (ActualDeliveryDate) | 971 | **75%** | Tri od četiri računa imaju datum isporuke |
| **BT-73** (StartDate) | 462 | 36% | Trećina ima obračunsko razdoblje |
| **BT-74** (EndDate) | 445 | 34% | Slično — ali 18 računa ima BT-73 bez BT-74 |
| **HR-BT-15** (PoNaplati) | 135 | **10%** | Svaki deseti dobavljač je na sustavu po naplati |
| **CopyIndicator=true** | 7 | 0,5% | 7 kopija (čl. 43 ispravci) |

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartPolja" height="280"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartPolja');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['BT-2\nIssueDate', 'BT-9\nDueDate', 'BT-7\nTaxPoint', 'BT-72\nDelivery', 'BT-73/74\nPeriod', 'HR-BT-15\nPoNaplati', 'BT-8\nDescrCode'],
      datasets: [{
        label: 'Prisutnost u uzorku',
        data: [100, 90, 82, 75, 36, 10, 1],
        backgroundColor: [
          '#2c3e50', '#2980b9', '#27ae60', '#16a085',
          '#8e44ad', '#e67e22', '#e74c3c'
        ],
        borderRadius: 4,
        barPercentage: 0.7
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Prisutnost datumskih polja (%)', font: { size: 14 } },
        tooltip: {
          callbacks: {
            label: function(ctx) { return ctx.raw + '% racuna'; }
          }
        }
      },
      scales: {
        x: { max: 100, ticks: { callback: function(v) { return v + '%'; } } },
        y: { ticks: { font: { size: 11 } } }
      }
    }
  });
});
</script>

### Ključni uvidi

> **82% ima BT-7** — to je pozitivno. Većina softverskih kuća razumije da je eksplicitni datum porezne obveze važan. Preostalih 18% koristi BT-2 kao default.

> **BT-8 gotovo nitko ne koristi (1%)** — od 15 računa s BT-8, 11 koristi kod 3 (redundantno = isto kao default BT-2) i 4 koristi kod 35 (datum isporuke). **Nijedan ne koristi 432 (datum plaćanja)!**

> **BT-9 (DueDate) ima 90%** — od 1.172 računa s pozitivnim BT-115, 1.159 ima DueDate (99%). Samo **13 računa** krši HR-BR-4 (pozitivan iznos bez roka plaćanja). Preostalih 111 računa ima BT-115 ≤ 0 (odobrenja, nulti iznosi) gdje DueDate nije obavezan.

---

## 4. HR-BT-15 specifičnost — potvrđena iz prakse
<div style="margin-top:-0.5rem;margin-bottom:0.5rem;"><span style="display:inline-block;background:#f39c12;color:white;font-size:0.72rem;font-weight:600;padding:0.15rem 0.55rem;border-radius:3px;cursor:help;" title="Ovo je autorovo tumačenje koje još nije službeno potvrđeno od Porezne uprave. Sadržaj treba tretirati kao prijedlog za raspravu, ne kao uputu.">Čeka potvrdu</span></div>

**135 računa ima HR-BT-15 (obračun po naplati).**

**Nijedan od tih 135 nema BT-8=432.**

Ovo je direktna potvrda iz prakse za ono što smo dokumentirali u [sekciji 3.1 na stranici Pravila](pravila#31-bt-8432-i-hr-bt-15--obračun-po-naplati-u-dva-elementa): **BT-8=432 se u praksi ne koristi** za obračun po naplati. Svi obveznici po naplati koriste samo HR-BT-15 — HR proširenje zamjenjuje EU mehanizam u potpunosti.

| Kombinacija | Očekivano | Pronađeno | Komentar |
|---|---|:---:|---|
| HR-BT-15 + BT-8=432 | Oba prisutna | **0** | Nitko ne koristi oba |
| HR-BT-15 bez BT-8=432 | Samo HR element | **135** | Svi obveznici po naplati |
| BT-8=432 bez HR-BT-15 | Nekonzistentnost — naš prijedlog [HR-BR-GECI-F01](prijedlozi-validator#f01-ako-bt-8432-zahtijevaj-hr-bt-15) bi ovo uhvatio (nije u službenom validatoru) | **0** | Nijedna pojava ovog tipa |

> **Zaključak**: Naše pitanje "treba li HR-BT-15 uopće kad postoji BT-8=432?" je u praksi odgovoreno obrnuto — **BT-8=432 uopće ne postoji u praksi**, samo HR-BT-15. EU mehanizam je potpuno zamijenjen HR proširenjem.

---

## 5. BT-7 vs BT-2 — koliko računa ima isporuku u drugom mjesecu?

| Kombinacija | Broj | % | Što to znači |
|---|:---:|:---:|---|
| BT-7 = BT-2 (isti datum) | 691 | 54% | Isporuka = izdavanje, najčešći slučaj |
| BT-7 < BT-2 (isporuka PRIJE računa) | **331** | **26%** | Isporuka u ranijem mjesecu — PDV po isporuci, ne po računu |
| BT-7 > BT-2 (isporuka NAKON računa) | 37 | 3% | Račun izdan prije isporuke (čl. 30 st. 2) ili predujam |
| Bez BT-7 (default = BT-2) | 224 | 17% | Nema eksplicitnog datuma poreza |

<div style="max-width: 380px; margin: 1.5rem auto;">
<canvas id="chartBT7" height="320"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartBT7');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['BT-7 = BT-2 (isti datum)', 'BT-7 < BT-2 (isporuka prije)', 'BT-7 > BT-2 (isporuka nakon)', 'Bez BT-7'],
      datasets: [{
        data: [691, 331, 37, 224],
        backgroundColor: ['#27ae60', '#e67e22', '#e74c3c', '#bdc3c7'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'BT-7 vs BT-2 — odnos datuma', font: { size: 14 } },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              var total = ctx.dataset.data.reduce(function(a,b){return a+b;}, 0);
              var pct = Math.round(ctx.raw / total * 100);
              return ctx.label + ': ' + ctx.raw + ' (' + pct + '%)';
            }
          }
        }
      }
    }
  });
});
</script>

> **29% računa ima isporuku u drugom mjesecu od računa.** To znači da za gotovo trećinu ulaznih računa, PDV period NIJE isti kao mjesec izdavanja računa. Ovo je upravo razlog zašto automatsko knjiženje bez provjere BT-7 ne radi — račun izdan u travnju može imati PDV u ožujku.

---

## 6. Pronađeni problemi (naši validator prijedlozi)

| Problem | Validator pravilo | Pronađeno | Primjeri |
|---|---|:---:|---|
| BT-7 + BT-8 oba prisutna | BR-CO-03 (fatal, EU) | **0** | Svi poštuju BR-CO-03 |
| BT-8=432 bez HR-BT-15 | HR-BR-GECI-F01 | **0** | — |
| BT-73 > BT-74 | HR-BR-GECI-F05 | **0** | — |
| CreditNote (381) bez BT-25 | HR-BR-GECI-F09 | **4** | 4 odobrenja bez reference na izvorni račun |
| BT-115 > 0 bez BT-9 | HR-BR-4 (službeni!) | **13** | 13 računa krši službeno pravilo — pozitivan iznos bez roka plaćanja |
| BT-73 bez BT-74 | HR-BR-GECI-W11 | **18** | 18 računa s početkom ali ne i krajem razdoblja |
| BT-74 bez BT-73 | HR-BR-GECI-W11 | **1** | 1 račun s krajem ali ne i početkom |

> **4 CreditNote-a bez BT-25** — odobrenja koja ne referenciraju izvorni račun. Primatelj ne može automatski povezati odobrenje s originalnom transakcijom. Naš prijedlog HR-BR-GECI-F09 bi ovo uhvatio.

> **13 računa krši HR-BR-4** — ovo je **službeno schematron pravilo** s `flag="fatal"` koje bi trebalo rezultirati **odbijanjem** računa. Činjenica da su ti računi prošli kroz posrednika i stigli do primatelja otvara pitanje: **provjeravaju li posrednici uopće HR CIUS schematron pravila?** Ako izdavateljev posrednik ne provjerava HR-BR-4 pri slanju, i primateljev posrednik ne provjerava pri zaprimanju — tko onda validira? Ili posrednici provjeravaju ali tretiraju `fatal` kao upozorenje umjesto odbijanja?

> **18 računa s BT-73 bez BT-74** — imaju početak obračunskog razdoblja ali ne i kraj. ERP ne može automatski razgraničiti trošak. Naš prijedlog HR-BR-GECI-W11 bi upozorio.

---

## 7. Što ovo znači za automatizaciju?

Za automatsko učitavanje ulaznih eRačuna u knjigovodstveni sustav:

1. **82% može automatski odrediti PDV period** iz BT-7 — ali preostalih 18% mora koristiti BT-2 (default), što može biti krivi mjesec ako je isporuka bila ranije

2. **29% zahtijeva provjeru** jer BT-7 ≠ BT-2 — računovođa mora odlučiti ide li PDV u mjesec računa ili mjesec isporuke

3. **10% je po naplati** (HR-BT-15) — za te račune pretporez tek po plaćanju, ne po primitku

4. **13 računa krši HR-BR-4** — pozitivan BT-115 bez DueDate. Većina (99%) poštuje pravilo

5. **7 kopija** — sustav mora prepoznati CopyIndicator i ne duplicirati knjiženje

---

*Analiza provedena 30.03.2026. na 1.283 XML datoteke. Skripta za analizu dostupna na zahtjev.*
