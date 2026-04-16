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

### Sadržaj {#sec-sadrzaj}
{: .no_toc }

* TOC
{:toc}

---

## 1. Uzorak {#sec-uzorak}

| Izvor | Broj XML-ova |
|----------|:---:|
| Komitent A | 285 |
| Komitent B | 754 |
| Komitent C | 244 |
| **Ukupno** | **1.283** |

Datoteke su ulazni eRačuni (primljeni od dobavljača) preuzeti od triju komitenata za period 01.01.–28.03.2026.

**244 jedinstvena izdavatelja** (različite tvrtke/OIB-ovi) — uzorak pokriva širok spektar softverskih kuća i industrija.

---

## 2. Tipovi dokumenata i profili {#sec-tipovi-dokumenata-i-profili}

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

## 3. Korištenje datumskih polja {#sec-koristenje-datumskih-polja}

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

### Ključni uvidi {#sec-kljucni-uvidi}

> **82% ima BT-7** — to je pozitivno. Većina softverskih kuća razumije da je eksplicitni datum porezne obveze važan. Preostalih 18% koristi BT-2 kao default.

> **BT-8 gotovo nitko ne koristi (1%)** — od 15 računa s BT-8, 11 koristi kod 3 (redundantno = isto kao default BT-2) i 4 koristi kod 35 (datum isporuke). **Nijedan ne koristi 432 (datum plaćanja)!**

> **BT-9 (DueDate) ima 90%** — od 1.172 računa s pozitivnim BT-115, 1.159 ima DueDate (99%). Samo **13 računa** krši HR-BR-4 (pozitivan iznos bez roka plaćanja). Preostalih 111 računa ima BT-115 ≤ 0 (odobrenja, nulti iznosi) gdje DueDate nije obavezan.

### Trend po mjesecima — sazrijevanje ekosustava {#sec-trend-po-mjesecima}

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartTrend" height="300"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartTrend');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Siječanj', 'Veljača', 'Ožujak'],
      datasets: [
        { label: 'BT-7 (TaxPointDate)', data: [80, 85, 82], borderColor: '#27ae60', backgroundColor: 'rgba(39,174,96,0.1)', fill: true, tension: 0.3 },
        { label: 'BT-72 (DeliveryDate)', data: [61, 76, 85], borderColor: '#2980b9', backgroundColor: 'rgba(41,128,185,0.1)', fill: true, tension: 0.3 },
        { label: 'BT-9 (DueDate)', data: [98, 97, 99], borderColor: '#8e44ad', backgroundColor: 'rgba(142,68,173,0.1)', fill: true, tension: 0.3 }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Prisutnost polja po mjesecima (%)', font: { size: 14 } },
        tooltip: { callbacks: { label: function(ctx) { return ctx.dataset.label + ': ' + ctx.raw + '%'; } } }
      },
      scales: {
        y: { min: 50, max: 100, ticks: { callback: function(v) { return v + '%'; } } }
      }
    }
  });
});
</script>

> **BT-72 skočio s 61% na 85%** od siječnja do ožujka — softverske kuće su postupno shvatile da trebaju slati datum isporuke. BT-7 je stabilan oko 80-85%. BT-9 (DueDate) je konzistentno visok.

---

## 4. HR-BT-15 specifičnost — potvrđena iz prakse {#sec-hr-bt-15}


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

## 5. BT-7 vs BT-2 — koliko računa ima isporuku u drugom mjesecu? {#sec-bt-7-vs-m}

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

### Koliko dana BT-7 odstupa od BT-2? {#sec-koliko-dana-bt-2}

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartOffset" height="280"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartOffset');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['<-30', '-11 do -30', '-6 do -10', '-5', '-4', '-3', '-2', '-1', '0', '+1 do +5', '>+5'],
      datasets: [{
        label: 'Broj racuna',
        data: [1, 81, 82, 28, 27, 23, 37, 52, 691, 8, 29],
        backgroundColor: function(ctx) {
          var i = ctx.dataIndex;
          if (i < 8) return '#e67e22';
          if (i === 8) return '#27ae60';
          return '#e74c3c';
        },
        borderRadius: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Razlika BT-7 minus BT-2 (dani)', font: { size: 14 } },
        legend: { display: false },
        tooltip: { callbacks: { label: function(ctx) { return ctx.raw + ' racuna'; } } }
      },
      scales: {
        y: { title: { display: true, text: 'Broj racuna' } },
        x: { title: { display: true, text: 'Dani razlike (negativno = isporuka prije racuna)' } }
      }
    }
  });
});
</script>

> **Zeleno**: isti dan (691). **Narančasto**: isporuka PRIJE računa — najčešće 1-30 dana ranije (tipično: mjesečno fakturiranje za prethodni mjesec). **Crveno**: isporuka NAKON računa (predujmi, čl. 30).

### Sezonski uzorak — veljača ima najviše neslaganja {#sec-sezonski-uzorak-veljaca}

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartSeason" height="280"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartSeason');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Siječanj (355)', 'Veljača (461)', 'Ožujak (452)'],
      datasets: [
        { label: 'BT-7 = BT-2', data: [198, 248, 237], backgroundColor: '#27ae60' },
        { label: 'BT-7 < BT-2 (prije)', data: [58, 142, 131], backgroundColor: '#e67e22' },
        { label: 'BT-7 > BT-2 (nakon)', data: [28, 4, 4], backgroundColor: '#e74c3c' },
        { label: 'Bez BT-7', data: [71, 67, 80], backgroundColor: '#bdc3c7' }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'BT-7 vs BT-2 po mjesecima', font: { size: 14 } }
      },
      scales: {
        x: { stacked: true },
        y: { stacked: true, title: { display: true, text: 'Broj racuna' } }
      }
    }
  });
});
</script>

> **Siječanj ima 28 računa s BT-7 > BT-2** (isporuka nakon izdavanja) — to su vjerojatno prijelazni računi iz prosinca 2025. s TaxPointDate u siječnju. U veljači i ožujku taj broj pada na 4 — normalizacija.

---

## 6. Širi profil računa — iznosi, stavke, PDV, plaćanja {#sec-siri-profil-racuna}
### Distribucija iznosa {#sec-distribucija-iznosa}

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartAmount" height="280"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartAmount');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['<= 0','0-10','10-50','50-100','100-500','500-1K','1K-5K','5K-10K','>10K'],
      datasets: [{
        label: 'Broj racuna',
        data: [111, 79, 141, 133, 326, 161, 245, 28, 58],
        backgroundColor: '#2980b9',
        borderRadius: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Distribucija iznosa racuna (EUR)', font: { size: 14 } },
        legend: { display: false }
      },
      scales: { y: { title: { display: true, text: 'Broj racuna' } } }
    }
  });
});
</script>

> **25% računa je 100–500 EUR** — najčešći raspon. **8% ima iznos ≤ 0** (odobrenja, storna, nulti iznosi). Samo 4% prelazi 10.000 EUR.

### Broj stavki po računu {#sec-broj-stavki-po-racunu}

<div style="max-width: 600px; margin: 1.5rem auto;">
<canvas id="chartLines" height="260"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartLines');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['1', '2-3', '4-5', '6-10', '11-20', '21-50', '50+'],
      datasets: [{
        label: 'Broj racuna',
        data: [554, 419, 99, 118, 65, 23, 3],
        backgroundColor: ['#e74c3c','#e67e22','#f39c12','#27ae60','#2980b9','#8e44ad','#2c3e50'],
        borderRadius: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Broj stavki po racunu', font: { size: 14 } },
        legend: { display: false }
      },
      scales: { y: { title: { display: true, text: 'Broj racuna' } } }
    }
  });
});
</script>

> **43% računa ima samo 1 stavku**, 75% ima 1–3 stavke. Medijan je 2, prosjek 3,9. Najsloženiji račun ima **243 stavke**.

### PDV stope i kategorije {#sec-pdv-stope-i-kategorije}

<div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; margin: 1.5rem 0;">
<div style="max-width: 320px; flex: 1;">
<canvas id="chartVAT" height="280"></canvas>
</div>
<div style="max-width: 320px; flex: 1;">
<canvas id="chartVATcat" height="280"></canvas>
</div>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx1 = document.getElementById('chartVAT');
  if (ctx1) new Chart(ctx1, {
    type: 'doughnut',
    data: {
      labels: ['25%', '0% (oslobodeno)', '13%', '5%'],
      datasets: [{ data: [916, 368, 48, 24], backgroundColor: ['#2980b9','#e74c3c','#27ae60','#f39c12'], borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'PDV stope (pojavljivanja)', font: { size: 13 } },
        tooltip: { callbacks: { label: function(c) { return c.label + ': ' + c.raw; } } }
      }
    }
  });
  var ctx2 = document.getElementById('chartVATcat');
  if (ctx2) new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: ['S (standardno)', 'E (oslobodeno)', 'AE (reverse charge)', 'Z (nulta stopa)', 'O (izvan PDV)'],
      datasets: [{ data: [988, 198, 115, 53, 2], backgroundColor: ['#2980b9','#e74c3c','#8e44ad','#f39c12','#bdc3c7'], borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'PDV kategorije', font: { size: 13 } },
        tooltip: { callbacks: { label: function(c) { return c.label + ': ' + c.raw; } } }
      }
    }
  });
});
</script>

> **94% računa ima samo jednu PDV stopu**. Samo 6% kombinira više stopa na jednom računu. Kategorija **E (oslobođeno)** pojavljuje se na 198 računa — **reverse charge (AE)** na 115.

### Dan u tjednu izdavanja {#sec-dan-u-tjednu-izdavanja}

<div style="max-width: 550px; margin: 1.5rem auto;">
<canvas id="chartWeekday" height="260"></canvas>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('chartWeekday');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Pon', 'Uto', 'Sri', 'Cet', 'Pet', 'Sub', 'Ned'],
      datasets: [{
        label: 'Broj racuna',
        data: [237, 246, 217, 222, 221, 110, 29],
        backgroundColor: ['#2980b9','#2980b9','#2980b9','#2980b9','#2980b9','#e67e22','#e74c3c'],
        borderRadius: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Dan u tjednu izdavanja racuna', font: { size: 14 } },
        legend: { display: false }
      }
    }
  });
});
</script>

> **Subotom se izdaje 8% računa, nedjeljom 2%.** Radnim danima distribucija je ravnomjerna (~17-19% po danu). Vikend računi su vjerojatno automatski generirani (komunalne usluge, telekomi, SaaS pretplate).

### Način plaćanja i referencije {#sec-nacin-placanja-i-referencije}

| Podatak | Prisutno | % | Komentar |
|---------|:--------:|:-:|----------|
| Poziv na broj (BT-83) | 1.208 | **94%** | Odlično za automatizaciju plaćanja |
| Napomena na računu (BT-22) | 1.062 | **82%** | Većina dodaje tekstualnu napomenu |
| Ugovor (BT-12) | 188 | 14% | Referencija na ugovor |
| BuyerReference (BT-10) | 152 | 11% | Interna oznaka kupca |
| Narudžbenica (BT-13) | 102 | 7% | Broj narudžbenice |
| PDF prilog | 1.281 | **99%** | Gotovo svi šalju PDF vizualizaciju |
| Popust na stavci | 276 | **21%** | Svaki peti račun ima popust |
| Dokument-level popust | 6 | 0,5% | Gotovo nitko ne koristi |
| POVNAK/PP (trošak) | 21 | 1,6% | Povratna naknada ili porez na potrošnju |

> **94% računa ima poziv na broj** — to je ključno za automatsko plaćanje iz ERP-a. **99% šalje PDF** kao prilog. **21% ima popust na stavci** ali dokument-level popusti su iznimno rijetki (0,5%).

---

## 7. Pronađeni problemi (naši validator prijedlozi) {#sec-pronadeni-problemi-nasi}

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

## 8. Što ovo znači za automatizaciju? {#sec-sto-ovo-znaci}
Za automatsko učitavanje ulaznih eRačuna u knjigovodstveni sustav:

1. **82% može automatski odrediti PDV period** iz BT-7 — ali preostalih 18% mora koristiti BT-2 (default), što može biti krivi mjesec ako je isporuka bila ranije

2. **29% zahtijeva provjeru** jer BT-7 ≠ BT-2 — računovođa mora odlučiti ide li PDV u mjesec računa ili mjesec isporuke

3. **10% je po naplati** (HR-BT-15) — za te račune pretporez tek po plaćanju, ne po primitku

4. **13 računa krši HR-BR-4** — pozitivan BT-115 bez DueDate. Većina (99%) poštuje pravilo

5. **7 kopija** — sustav mora prepoznati CopyIndicator i ne duplicirati knjiženje

---

*Analiza provedena 30.03.2026. na 1.283 XML datoteke. Skripta za analizu dostupna na zahtjev.*
