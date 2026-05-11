# Demo Walkthrough

A guided tour of what the skill produces. All screenshots come from the
[v1.2.0 release sample report](https://github.com/Hichamdz85/executive-market-research/releases/download/v1.2.0/khelifi-sample-report-hvac-algeria-en.pdf)
(HVAC Accessories - Algeria, English).

## The five-phase pipeline

```
   1. Intake         2. Orient         3. Officials      4. Triangulate    5. Render
+-------------+   +-------------+   +-------------+   +--------------+   +--------------+
| Product     |   | Multilingual|   | World Bank  |   | Cross-check  |   | HTML + PDF   |
| Country     | > | quick search| > | IMF / UN    | > | every number | > | Chart.js +   |
| Language    |   | (3 languages|   | Customs     |   | against >=3  |   | Playwright   |
| Focus       |   | in parallel)|   | Central bank|   | sources      |   | A4 landscape |
+-------------+   +-------------+   +-------------+   +--------------+   +--------------+
```

## What you get, page by page

### Cover page
Hero image, country flag, report title, author logo, date.

![Cover](screenshots/cover.png)

### Table of contents
Nine numbered sections with section icons and page mapping.

![TOC](screenshots/toc.png)

### Country macro overview
Eight-tile KPI dashboard with GDP, population, FX, inflation, trade balance,
EoDB rank, sovereign rating.

![Macro KPIs](screenshots/macro_kpis.png)
![Macro charts](screenshots/macro_charts.png)

### Executive summary
One-page, icon-segmented, designed so a CEO can decide from this page alone.

![Executive summary](screenshots/exec_summary.png)

### Market and imports
Demand sizing, CAGR, top exporters, value/volume bar charts - every chart
title is a finding, not a label.

![Market](screenshots/market.png)
![Imports](screenshots/imports.png)

### Regulatory deep-dive
HS codes, duties, FTAs, certifications, payment terms.

![Regulatory](screenshots/regulatory.png)

### Author back cover
Contact info and engagement offer.

![Author back cover](screenshots/author.png)

## Two output formats from one run

| Format | Use case |
|--------|----------|
| `report.html` | Interactive, shareable, embeds Chart.js for live charts |
| `report.pdf` | Print-ready A4 landscape, 35-45 pages full / 8-10 pages quick |

## Two modes, one pipeline

- **Full mode** (default): 35-45 pages, all 9 sections, full appendix.
- **Quick mode** (`--quick`): 8-10 page Executive Brief - methodology,
  macro snapshot, executive summary, market sizing, SWOT, recommendations.

Trigger Quick Mode by asking Claude:

> *"Use the executive-market-research skill in **quick mode** for [product] in [country]."*

## Try it

```bash
git clone https://github.com/Hichamdz85/executive-market-research.git
cd executive-market-research
pip install -r requirements.txt
playwright install chromium
python scripts/generate_report.py \
  --data examples/sample_engagement.json \
  --language en \
  --output ./output/
```

Open `output/report_en.html` in any browser, or send `output/report_en.pdf`
to the printer.
