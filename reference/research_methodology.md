# Research Methodology

This document describes how to conduct the research that powers each report. Follow it sequentially for any new engagement.

## Phase 1 — Discovery (15 minutes)

Before searching anything, write a one-paragraph hypothesis:

> "I believe the [product] market in [country] is [size] USD with [direction] trajectory, driven primarily by [hypothesis]. The opportunity for [client type] is [positive/negative/mixed] because [reason]."

Now research to confirm or invalidate this hypothesis.

## Phase 2 — Macro context (30 minutes)

For the target country, gather:

1. Latest GDP (nominal USD) and 5y trend
2. Population and growth rate
3. Inflation (CPI YoY)
4. FX rate vs USD (current and 5y volatility)
5. Trade balance and major trading partners
6. Sovereign rating
7. Ease of Doing Business rank
8. If oil-dependent: oil price + production

Sources to query in this order:
1. World Bank Open Data
2. IMF DataMapper
3. Country statistical office (always check)
4. CIA World Factbook for the snapshot

## Phase 3 — Product / sector definition (20 minutes)

Lock down:

1. **HS codes** — the exact 6-digit (or 8-digit if national) codes that capture the product
   - Use the WCO HS database or country customs lookup
   - List ALL relevant codes; products often span multiple
2. **Product taxonomy** — sub-categories, technical specifications
3. **Adjacent products** — what's commonly bundled or substituted
4. **End-use sectors** — who buys this and why

Output: a one-table product definition that goes into Section IV.

## Phase 4 — Demand sizing (45 minutes)

The most important section. Don't shortcut this.

1. **Find the demand series** in volume (tons/units/liters)
   - Apparent consumption = Domestic production + Imports - Exports
   - If domestic production data is unavailable, use imports as a floor and triangulate
2. **Find the demand series in value** (USD)
3. **Calculate CAGR** correctly:
   - Historical CAGR over 5 years: `(Value_2024 / Value_2019)^(1/5) - 1`
4. **Identify forecasts**
   - Look for IMF, EIU, sector association projections
   - If none exist, project at the historical CAGR with explicit disclosure
5. **Decompose drivers**
   - Macro drivers (GDP growth, urbanization, demographic shifts)
   - Sector drivers (construction starts, housing units, healthcare spending)
   - Policy drivers (subsidy programs, infrastructure plans)

## Phase 5 — Supply analysis (45 minutes)

1. **Imports** — pull UN Comtrade for HS codes × target country, last 5 years
   - Value (USD) and volume (kg or units) — record both
   - Top 10 partner countries
   - Year-on-year changes; identify anomalies and explain
2. **Domestic production**
   - Industry association reports
   - Company filings (top 5 producers)
   - Government industrial output statistics
3. **Domestic vs import split** as % of consumption
4. **Logistics** — Incoterms norms, transit times, key ports

## Phase 6 — Regulatory deep-dive (30 minutes)

Build a regulatory table covering:

1. **Tariff** — MFN rate from country customs schedule
2. **Preferential rates** — under each relevant FTA (GAFTA, AfCFTA, EU FTA, etc.)
3. **VAT** — standard rate applied on landed cost
4. **Specific taxes** — excise, environmental, etc.
5. **Standards** — ISO certifications, country-specific marks, language labels
6. **Licenses** — import license, registration, restricted-product designations
7. **Quotas** — annual quotas, seasonal restrictions
8. **Payment terms** — what's permitted (LC, advance, open account)
9. **FX controls** — repatriation rules

For each, cite the specific regulation or government source.

## Phase 7 — Competitive landscape (30 minutes)

1. Identify top 5–10 importers / distributors (from trade press, customs broker contacts, industry directories)
2. Identify top 5 domestic producers (if applicable)
3. Profile each: HQ, founded, revenue range, products, geographic focus
4. Estimate market share where data permits (don't guess wildly)
5. Pricing tiers — entry / mid / premium with example brands
6. Distribution structure (direct, distributor-tier, tender-based)

## Phase 8 — Synthesis & recommendations (45 minutes)

1. **Score export attractiveness**:
   - Demand growth
   - Import intensity
   - Tariff barrier
   - Competition density
   - Payment risk
   Each on 1–5 scale, weight, sum.
2. **SWOT** — 3–4 items per quadrant
3. **Risk register** — top 5 risks, likelihood × impact
4. **Recommendations** — 3–7 specific actions ranked by priority and timeline

## Phase 9 — Quality control (15 minutes)

Run the quality checklist in `quality_standards.md` before delivering.

---

## Tools to use during research

- Web search (broad queries, then narrowing)
- Direct fetch of government / international body data portals
- HS code lookup (WCO, country customs)
- Currency conversion (XE, OANDA — cite the date used)
- Chart/data visualization (matplotlib, Chart.js)

## Common pitfalls

| Pitfall | Mitigation |
|---------|-----------|
| Trusting a single secondary source | Cross-check with primary (UN Comtrade, World Bank) |
| Using outdated data without flagging | State the data vintage explicitly |
| Confusing volume and value trends | Show both; sometimes value rises while volume falls (price effect) |
| Misreading mirror data direction | Mirror data is from the partner's perspective; verify direction |
| HS code misclassification | Cross-reference with description and check national subdivisions |
| FX confusion | State USD vs local currency clearly; note FX rate used |
| Ignoring informal/grey market | Acknowledge if non-official channels are material |

## Documenting your research

For each report, maintain a `research_log.md` in the engagement folder:
- What was searched
- What was found (with URLs)
- What was discarded and why
- Confidence level for each major number

This protects you and makes the report defensible.
