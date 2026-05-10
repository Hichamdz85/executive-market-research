<div align="center">

# Executive Market Research

### A Claude Skill that produces KPMG-grade market research reports — in PDF and interactive HTML — for any product, sector, or country.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill: Claude](https://img.shields.io/badge/Built%20for-Claude-FF7A00)](https://claude.ai)
[![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20AR%20%7C%20FR-00338D)](#languages)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

**Three languages • Live web research • Investor-grade output • Free & open source**

[Live demo](https://khelifi-consulting.github.io/executive-market-research/) · [Quick start](#quick-start) · [How it works](#how-it-works) · [Methodology](reference/kpmg_research_playbook.md)

</div>

---

## What it does

Hand it a product and a country — get back a **35–45 page consulting deliverable** that looks like KPMG, Deloitte, or McKinsey produced it. No templates to fill in, no slides to design. Claude handles the research, the analysis, the charts, and the layout.

```
You:    "Market research for HVAC accessories in Algeria, in English"
Claude: → researches the web (UN Comtrade, World Bank, IMF, ONS, EIU…)
        → triangulates every headline number from 3+ sources
        → builds a 9-section report with charts, SWOT, recommendations
        → outputs report.pdf + report.html

You:    receive the deliverable, ready to send to a board / investor / client.
```

## Why it's different

| Other "AI report" tools | This skill |
|-------------------------|-----------|
| Generic templates filled with bullet points | Real consulting structure (9 sections, KPMG-style) |
| Single-source generation | **Triangulation rule**: 3+ sources per headline number |
| English only | **English + Arabic (RTL) + French** |
| Plain HTML output | PDF + interactive HTML, fully branded |
| Hallucinated numbers | Live web research, every number cited |
| One-size-fits-all design | Country flag + macro dashboard + sector-specific imagery |

## Sample output

<table>
<tr>
<td width="33%" align="center"><b>Cover page</b><br><sub>Hero image · Country flag · Author logo</sub></td>
<td width="33%" align="center"><b>Country snapshot</b><br><sub>8 KPI dashboard · GDP & trade charts</sub></td>
<td width="33%" align="center"><b>Executive summary</b><br><sub>Icon-based segments table</sub></td>
</tr>
<tr>
<td><img src="docs/preview-cover.png" alt="Cover preview"/></td>
<td><img src="docs/preview-macro.png" alt="Macro preview"/></td>
<td><img src="docs/preview-exec.png" alt="Exec summary preview"/></td>
</tr>
<tr>
<td align="center"><b>Market sizing</b><br><sub>Value & volume bar charts</sub></td>
<td align="center"><b>Regulatory deep-dive</b><br><sub>Tariffs · FTAs · Standards</sub></td>
<td align="center"><b>Recommendations</b><br><sub>Priority · Timeline · Impact</sub></td>
</tr>
<tr>
<td><img src="docs/preview-market.png" alt="Market preview"/></td>
<td><img src="docs/preview-regulatory.png" alt="Regulatory preview"/></td>
<td><img src="docs/preview-recos.png" alt="Recommendations preview"/></td>
</tr>
</table>

> 📄 **Full sample**: [HVAC Accessories — Algeria (PDF)](examples/sample_report_en.pdf) · [HTML version](https://khelifi-consulting.github.io/executive-market-research/examples/sample_report_en.html)

## Quick start

### Option A — Use as a Claude skill (recommended)

1. Clone or download this repo into your Claude skills directory:

   ```bash
   git clone https://github.com/khelifi-consulting/executive-market-research.git \
     ~/.claude/skills/executive-market-research
   ```

2. In Claude (Code, Desktop, or API), simply ask:

   > "Use the executive-market-research skill to produce a market study for [product] in [country], in [language]."

3. Claude reads `SKILL.md`, conducts the research, and writes both `report.html` and `report.pdf` to your output folder.

### Option B — Run the generator standalone

If you already have an `engagement.json` data file, you can render directly:

```bash
pip install playwright
playwright install chromium

python scripts/generate_report.py \
  --data examples/sample_engagement.json \
  --language en \
  --output ./output/
```

You'll get `output/report_en.html` and `output/report_en.pdf`.

## Languages

| Code | Language | Direction | Fonts |
|------|----------|-----------|-------|
| `en` | English  | LTR       | Helvetica / Arial |
| `ar` | Arabic   | RTL       | Cairo / Tajawal / IBM Plex Sans Arabic |
| `fr` | Français | LTR       | Helvetica / Arial |

The full layout (header, footer, charts, tables, SWOT) flips for RTL automatically.

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│  1.  Intake the request (product, country, language, focus) │
├─────────────────────────────────────────────────────────────┤
│  2.  Live web research — KPMG 5-phase funnel                │
│       a) Quick orientation (multilingual)                   │
│       b) Official sources (World Bank, IMF, UN, national)   │
│       c) Specialised data (Statista, Euromonitor, EIU…)     │
│       d) Financial & news cross-check                       │
│       e) Academic (Google Scholar, JSTOR for niche depth)   │
├─────────────────────────────────────────────────────────────┤
│  3.  Triangulate (≥3 sources per headline number)           │
├─────────────────────────────────────────────────────────────┤
│  4.  Compose the report                                     │
│       I.   Methodology & scope                              │
│       II.  Country macro overview (with flag + KPIs)        │
│       III. Executive summary (icon-based segments)          │
│       IV.  Market review (demand-side)                      │
│       V.   Import characteristics (supply-side)             │
│       VI.  Regulatory aspects                               │
│       VII. Competitive landscape                            │
│       VIII. Conclusion + SWOT + recommendations             │
│       IX.  Appendix (sources, HS codes, glossary)           │
├─────────────────────────────────────────────────────────────┤
│  5.  Render HTML + PDF (Chart.js / Playwright)              │
└─────────────────────────────────────────────────────────────┘
```

## Research methodology

This skill enforces the **7 Golden Rules** used by Big-4 consulting firms:

1. **Triangulation** — every key number from 3+ independent sources
2. **Freshness** — prioritise data <18 months old
3. **Multilingual** — search in English + the country's local languages
4. **Official first** — government and international sources before commercial
5. **Benchmarking** — compare to 2–3 peer countries in the same sector
6. **ESG mandatory** — every report covers Environmental, Social, Governance
7. **Primary research simulation** — propose 5–10 interview questions

Read the full playbook: [reference/kpmg_research_playbook.md](reference/kpmg_research_playbook.md)

## Project structure

```
executive-market-research/
├── SKILL.md                          ← Main skill instructions
├── README.md                         ← This file
├── LICENSE
├── templates/
│   ├── report_en.html                ← English template (LTR)
│   ├── report_ar.html                ← Arabic template (RTL)
│   ├── report_fr.html                ← French template (LTR)
│   └── styles.css                    ← KPMG-style design system
├── scripts/
│   ├── generate_report.py            ← Main pipeline
│   └── fetch_assets.py               ← Country flags + section images
├── assets/
│   └── icons/                        ← SVG icons (KPMG-style line art)
├── reference/
│   ├── kpmg_research_playbook.md     ← The 7 Golden Rules + 5-phase funnel
│   ├── report_structure.md           ← 9-section breakdown
│   ├── data_sources.md               ← Authoritative source map
│   ├── research_methodology.md       ← Step-by-step research process
│   └── quality_standards.md          ← Pre-delivery checklist
├── examples/
│   ├── sample_engagement.json        ← Reference data file
│   └── sample_report_en.pdf          ← Reference output
├── landing-page/                     ← GitHub Pages source
└── docs/                             ← Preview screenshots
```

## Use cases

- **Export feasibility studies** — "Can we sell our [product] in [country]?"
- **Market entry assessments** — "Is [country] worth entering for [sector]?"
- **Competitive intelligence** — "Who are the players in [market]?"
- **Investor decks (data appendix)** — solid market sizing for fundraising
- **Government / development agency briefs** — sector studies for policy
- **Academic case studies** — country + product economic analysis
- **Quick-turn consulting** — get a 30-page first draft in minutes, polish in hours

## Frequently asked

**Q: Does this replace human consultants?**
A: No. It produces a strong first draft. A human consultant should validate triangulation, run primary interviews, and tailor the recommendations.

**Q: How long does generation take?**
A: 8–15 minutes for the research, 30 seconds for the rendering.

**Q: Can I use my own brand/logo?**
A: Yes. Edit `author_name`, `author_logo`, and the colour variables in `templates/styles.css`.

**Q: Are the numbers accurate?**
A: They come from live web research (UN Comtrade, World Bank, etc.) with triangulation. Always spot-check critical numbers before sending to a client.

**Q: Why three languages?**
A: This skill was designed in the MENA / North Africa context where reports often need to be delivered in Arabic, French, or English depending on the audience. Other languages can be added — see [Contributing](#contributing).

**Q: Can I add other languages?**
A: Yes — copy `templates/report_en.html` to `templates/report_xx.html` and translate the static labels. Send a PR.

## Contributing

PRs welcome. Areas where contributions are especially helpful:

- Additional language templates (ES, PT, DE, ZH, RU, TR, …)
- Sector-specific data source maps in `reference/data_sources.md`
- Country-specific source maps in `reference/kpmg_research_playbook.md`
- Improved chart types (geographic heatmaps, treemaps)
- Better stock photography curation in `assets/images/`

## Author

<table>
<tr>
<td width="120" valign="top">
<img src="https://via.placeholder.com/100x100/00338D/FFFFFF?text=KC" alt="Khelifi Consulting" width="100"/>
</td>
<td valign="top">

### **KHELIFI CONSULTING**

*Strategic & Marketing Research · Algeria & MENA region*

📧 **info@khelificonsulting.com**
🌐 [khelificonsulting.com](https://khelificonsulting.com)

We turn market questions into board-ready answers. Available for custom feasibility studies, market entry assessments, competitive intelligence, and bespoke research engagements across North Africa and the GCC.

If this skill helped you ship a better deliverable, ⭐ the repo and reach out — I'd love to hear what you built.

</td>
</tr>
</table>

## License

MIT — use it, fork it, sell deliverables built with it. See [LICENSE](LICENSE).

---

<div align="center">
<sub>Built with ❤️ for the global consulting community.</sub>
</div>
