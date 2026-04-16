---
layout: default
title: "Napredak revizije"
nav_order: 13
---

# Napredak revizije dokumentacije

Ova stranica prikazuje stanje stručne revizije dokumentacije u realnom vremenu. Podaci se automatski ažuriraju svaki put kada se promijeni stanje bilo kojeg Issue-a na GitHubu.

**Zadnje ažuriranje:** {{ site.data.review_status.last_updated | default: "—" }}

---

## Ukupni napredak {#sec-ukupni-napredak}

Napredak se računa iz **145 segmenata za reviziju** (45 autorskih segmenata nije uključeno u postotak).

<div style="max-width: 720px; margin: 1.5rem auto;">
  <div id="progress-bar-total" style="background:#ecf0f1; border-radius: 8px; height: 32px; overflow: hidden; display: flex;">
    <div id="bar-potvrdeno" style="background:#27ae60; height: 100%; transition: width 0.5s;"></div>
    <div id="bar-u-reviziji" style="background:#1d76db; height: 100%; transition: width 0.5s;"></div>
    <div id="bar-ceka-pu" style="background:#5dade2; height: 100%; transition: width 0.5s;"></div>
    <div id="bar-trazi-izmjenu" style="background:#d93f0b; height: 100%; transition: width 0.5s;"></div>
    <div id="bar-ceka" style="background:#f39c12; height: 100%; transition: width 0.5s;"></div>
  </div>
  <div id="progress-legend" style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.75rem; font-size: 0.85rem;"></div>
</div>

<div id="main-stats" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin: 2rem 0;"></div>

---

## Po stranicama {#sec-po-stranicama}

<div style="max-width: 800px; margin: 1.5rem auto;">
<canvas id="chartPoStranicama" height="320"></canvas>
</div>

---

## Raspored po stanjima {#sec-po-stanjima}

<div style="max-width: 500px; margin: 1.5rem auto;">
<canvas id="chartPoStanju" height="300"></canvas>
</div>

---

## Kako se stanja mijenjaju {#sec-kako-stanja}

| Stanje | Značenje |
|--------|----------|
| 🟡 **Za pregled** | Segment još nije pregledan od strane stručnjaka |
| 🔵 **U reviziji** | Aktivna rasprava na GitHub Issue-u |
| ⏸️ **Čeka Poreznu upravu** | Raspravljeno, čeka službeni odgovor PU |
| ⚠️ **Traži izmjenu** | Potrebna je ispravka prije potvrde |
| 🟢 **Potvrđeno** | Odobreno i primijenjeno u dokumentaciji |
| ⚪ **Izvan revizije** | Autorski sadržaj — po defaultu ne traži reviziju |
| ❌ **Odbačeno** | Segment se ne uključuje u konačnu verziju |

Detaljnije: [Vodič za reviziju](vodic-za-reviziju).

---

<script id="review-data" type="application/json">
{{ site.data.review_status | jsonify }}
</script>

<script>
(function() {
  var dataEl = document.getElementById('review-data');
  if (!dataEl) return;
  var data;
  try {
    data = JSON.parse(dataEl.textContent || dataEl.innerText);
  } catch (e) {
    console.error('Ne mogu parsirati review_status.json', e);
    return;
  }

  var s = data.summary || {};
  var total = (s.za_reviziju || 145);

  var pct = function(n) { return total > 0 ? Math.round(n / total * 100) : 0; };

  // Progress bar
  var widths = {
    'bar-potvrdeno':     pct(s.potvrdeno || 0),
    'bar-u-reviziji':    pct(s.u_reviziji || 0),
    'bar-ceka-pu':       pct(s.ceka_pu || 0),
    'bar-trazi-izmjenu': pct(s.trazi_izmjenu || 0),
    'bar-ceka':          pct(s.ceka || 0)
  };
  Object.keys(widths).forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.style.width = widths[id] + '%';
  });

  // Legend
  var legendItems = [
    { color: '#27ae60', label: 'Potvrđeno', count: s.potvrdeno || 0 },
    { color: '#1d76db', label: 'U reviziji', count: s.u_reviziji || 0 },
    { color: '#5dade2', label: 'Čeka PU', count: s.ceka_pu || 0 },
    { color: '#d93f0b', label: 'Traži izmjenu', count: s.trazi_izmjenu || 0 },
    { color: '#f39c12', label: 'Za pregled', count: s.ceka || 0 }
  ];
  var legendHTML = legendItems.map(function(item) {
    return '<div style="display:flex;align-items:center;gap:0.4rem;">' +
           '<span style="width:12px;height:12px;background:' + item.color + ';border-radius:2px;display:inline-block;"></span>' +
           item.label + ': <strong>' + item.count + '</strong>' +
           '</div>';
  }).join('');
  var legend = document.getElementById('progress-legend');
  if (legend) legend.innerHTML = legendHTML;

  // Main stats cards
  var cardStyle = 'background:rgba(41,128,185,0.08);border:1px solid rgba(41,128,185,0.2);border-radius:8px;padding:1rem 1.5rem;text-align:center;min-width:140px;';
  var cards = [
    { num: (s.potvrdeno || 0), label: 'Potvrđeno', color: '#27ae60' },
    { num: (s.ceka || 0), label: 'Čeka pregled', color: '#f39c12' },
    { num: pct(s.potvrdeno || 0) + '%', label: 'Dovršeno', color: '#2980b9' },
    { num: total, label: 'Za reviziju', color: '#7f8c8d' },
    { num: (s.izvan_revizije || 0), label: 'Izvan revizije', color: '#94a3b8' }
  ];
  var cardsHTML = cards.map(function(c) {
    return '<div style="' + cardStyle + '">' +
           '<div style="font-size:2rem;font-weight:800;color:' + c.color + ';line-height:1;">' + c.num + '</div>' +
           '<div style="font-size:0.8rem;color:#7f8c8d;margin-top:0.3rem;text-transform:uppercase;letter-spacing:0.5px;">' + c.label + '</div>' +
           '</div>';
  }).join('');
  var mainStats = document.getElementById('main-stats');
  if (mainStats) mainStats.innerHTML = cardsHTML;

  // Chart: Po stranicama
  var emptyBucket = function() { return { potvrdeno: 0, u_reviziji: 0, ceka_pu: 0, trazi_izmjenu: 0, ceka: 0, izvan_revizije: 0, odbaceno: 0 }; };
  var stranice = {};
  (data.segments || []).forEach(function(seg) {
    if (!stranice[seg.stranica]) stranice[seg.stranica] = emptyBucket();
    var st = seg.status || 'ceka';
    if (stranice[seg.stranica][st] !== undefined) stranice[seg.stranica][st]++;
  });
  // Default page list in case segments empty
  var allPages = ['pravila','primjeri-izdavatelj','primjeri-primatelj','referenca','europska-usporedba','naknadno-dospjeli-racuni','prijedlozi-validator','indikator-kopije','analiza-ulaznih','index','vodic-za-reviziju','github-vodic','github-obavijesti','kako-doprinijeti'];
  allPages.forEach(function(p) {
    if (!stranice[p]) stranice[p] = emptyBucket();
  });
  // Sort pages: those with any segments first, then alphabetically
  var pageLabels = Object.keys(stranice).sort(function(a, b) {
    var sumA = Object.values(stranice[a]).reduce(function(x,y){return x+y;}, 0);
    var sumB = Object.values(stranice[b]).reduce(function(x,y){return x+y;}, 0);
    if (sumA === 0 && sumB === 0) return a.localeCompare(b);
    if (sumA === 0) return 1;
    if (sumB === 0) return -1;
    return b - a;
  });
  var ctx1 = document.getElementById('chartPoStranicama');
  if (ctx1 && typeof Chart !== 'undefined') {
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: pageLabels,
        datasets: [
          { label: 'Potvrđeno', data: pageLabels.map(function(p){return stranice[p].potvrdeno;}), backgroundColor: '#27ae60' },
          { label: 'U reviziji', data: pageLabels.map(function(p){return stranice[p].u_reviziji;}), backgroundColor: '#1d76db' },
          { label: 'Čeka PU', data: pageLabels.map(function(p){return stranice[p].ceka_pu;}), backgroundColor: '#5dade2' },
          { label: 'Traži izmjenu', data: pageLabels.map(function(p){return stranice[p].trazi_izmjenu;}), backgroundColor: '#d93f0b' },
          { label: 'Za pregled', data: pageLabels.map(function(p){return stranice[p].ceka;}), backgroundColor: '#f39c12' },
          { label: 'Izvan revizije', data: pageLabels.map(function(p){return stranice[p].izvan_revizije;}), backgroundColor: '#94a3b8' },
          { label: 'Odbačeno', data: pageLabels.map(function(p){return stranice[p].odbaceno;}), backgroundColor: '#b60205' }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { position: 'top', labels: { font: { size: 11 }, padding: 10, usePointStyle: true } }, title: { display: false } },
        scales: {
          x: { stacked: true, title: { display: true, text: 'Broj segmenata' } },
          y: { stacked: true, ticks: { font: { size: 11 } } }
        }
      }
    });
  }

  // Chart: Po stanjima (donut) — svih 7 stanja
  var ctx2 = document.getElementById('chartPoStanju');
  if (ctx2 && typeof Chart !== 'undefined') {
    new Chart(ctx2, {
      type: 'doughnut',
      data: {
        labels: ['Potvrđeno', 'U reviziji', 'Čeka PU', 'Traži izmjenu', 'Za pregled', 'Izvan revizije', 'Odbačeno'],
        datasets: [{
          data: [
            s.potvrdeno || 0,
            s.u_reviziji || 0,
            s.ceka_pu || 0,
            s.trazi_izmjenu || 0,
            s.ceka || 0,
            s.izvan_revizije || 0,
            s.odbaceno || 0
          ],
          backgroundColor: ['#27ae60', '#1d76db', '#5dade2', '#d93f0b', '#f39c12', '#94a3b8', '#b60205'],
          borderWidth: 2, borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 10, usePointStyle: true } },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                var total = ctx.dataset.data.reduce(function(a,b){return a+b;}, 0);
                var pct = total > 0 ? Math.round(ctx.raw / total * 100) : 0;
                return ctx.label + ': ' + ctx.raw + ' (' + pct + '%)';
              }
            }
          }
        }
      }
    });
  }
})();
</script>
