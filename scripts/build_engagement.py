#!/usr/bin/env python3
"""Build a research-ready engagement JSON from product/country inputs.

This script creates the structured data file consumed by generate_report.py.
It is intentionally conservative: when a number has not been researched, the
field says so instead of fabricating a market estimate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PRESETS = ROOT / "presets"

COUNTRY_ISO2 = {
    "algeria": "DZ",
    "morocco": "MA",
    "tunisia": "TN",
    "egypt": "EG",
    "saudi arabia": "SA",
    "united arab emirates": "AE",
    "uae": "AE",
    "qatar": "QA",
    "kuwait": "KW",
    "bahrain": "BH",
    "oman": "OM",
    "jordan": "JO",
    "lebanon": "LB",
    "france": "FR",
    "belgium": "BE",
    "germany": "DE",
    "italy": "IT",
    "spain": "ES",
    "united kingdom": "GB",
    "uk": "GB",
    "united states": "US",
    "usa": "US",
    "china": "CN",
    "japan": "JP",
    "turkey": "TR",
    "türkiye": "TR",
    "india": "IN",
    "brazil": "BR",
    "south africa": "ZA",
    "nigeria": "NG",
    "kenya": "KE",
}

SECTOR_KEYWORDS = {
    "healthcare": ["medical", "medic", "health", "hospital", "pharma", "clinic", "aesthetic", "device"],
    "construction": ["construction", "building", "cement", "steel", "hvac", "infrastructure", "real estate"],
    "food": ["food", "beverage", "agribusiness", "wheat", "rice", "sugar", "milk", "oil"],
    "automotive": ["automotive", "vehicle", "car", "truck", "ev ", "battery", "tyre", "tire"],
    "energy": ["energy", "solar", "wind", "oil", "gas", "renewable", "power", "electric"],
}

DIVIDER_IMAGES = {
    "methodology": "https://images.unsplash.com/photo-1494412651409-8963ce7935a7?auto=format&fit=crop&w=1600",
    "country": "https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=1600",
    "exec": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1600",
    "market": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600",
    "imports": "https://images.unsplash.com/photo-1494412651409-8963ce7935a7?auto=format&fit=crop&w=1600",
    "regulatory": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=1600",
    "competitive": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600",
    "conclusion": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1600",
    "appendix": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=1600",
}


def infer_country_iso2(country: str, explicit_iso2: str | None = None) -> str:
    if explicit_iso2:
        return explicit_iso2.upper()
    normalized = country.strip().lower()
    if len(normalized) == 2 and normalized.isalpha():
        return normalized.upper()
    return COUNTRY_ISO2.get(normalized, "XX")


def load_presets() -> dict[str, dict[str, Any]]:
    presets: dict[str, dict[str, Any]] = {}
    for path in sorted(PRESETS.glob("*.json")):
        presets[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return presets


def infer_sector(product: str, requested_sector: str | None, presets: dict[str, dict[str, Any]]) -> str | None:
    if requested_sector:
        key = requested_sector.lower()
        return key if key in presets else None

    text = f" {product.lower()} "
    scores: dict[str, int] = {}
    for sector, words in SECTOR_KEYWORDS.items():
        scores[sector] = sum(1 for word in words if word in text)
    best = max(scores, key=scores.get) if scores else None
    return best if best and scores[best] > 0 and best in presets else None


def _world_bank_series(iso2: str, indicator: str) -> list[dict[str, Any]]:
    if iso2 == "XX":
        return []
    query = urllib.parse.urlencode({"format": "json", "per_page": "15"})
    url = f"https://api.worldbank.org/v2/country/{iso2.lower()}/indicator/{indicator}?{query}"
    try:
        with urllib.request.urlopen(url, timeout=12) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return []
    if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
        return []
    rows = []
    for row in payload[1]:
        if row.get("value") is not None:
            rows.append({"year": int(row["date"]), "value": row["value"]})
    return sorted(rows, key=lambda item: item["year"])


def _latest(series: list[dict[str, Any]]) -> tuple[int, float] | None:
    return (series[-1]["year"], float(series[-1]["value"])) if series else None


def _compact_money(value: float) -> str:
    if abs(value) >= 1_000_000_000_000:
        return f"USD {value / 1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000:
        return f"USD {value / 1_000_000_000:.0f}B"
    if abs(value) >= 1_000_000:
        return f"USD {value / 1_000_000:.0f}M"
    return f"USD {value:,.0f}"


def _compact_number(value: float) -> str:
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    return f"{value:,.0f}"


def build_engagement(
    product: str,
    country: str,
    language: str = "en",
    country_iso2: str | None = None,
    sector: str | None = None,
    author_name: str = "Khelifi Consulting",
    author_logo: str = "../assets/icons/logo-mark.svg",
) -> dict[str, Any]:
    iso2 = infer_country_iso2(country, country_iso2)
    presets = load_presets()
    sector_key = infer_sector(product, sector, presets)
    preset = presets.get(sector_key or "", {})
    report_date = dt.date.today().strftime("%B %Y")

    gdp_series = _world_bank_series(iso2, "NY.GDP.MKTP.CD")
    population_series = _world_bank_series(iso2, "SP.POP.TOTL")
    inflation_series = _world_bank_series(iso2, "FP.CPI.TOTL.ZG")
    trade_series = _world_bank_series(iso2, "NE.TRD.GNFS.ZS")

    latest_gdp = _latest(gdp_series)
    latest_population = _latest(population_series)
    latest_inflation = _latest(inflation_series)

    hs_codes = [
        f"{item['code']} - {item['label']}"
        for item in preset.get("common_hs_codes", [])
    ]
    source_names = [
        f"{item['name']} - {item['url']}"
        for item in preset.get("specialized_sources", [])
    ]

    gdp_chart = {
        "years": [str(row["year"]) for row in gdp_series[-6:]],
        "values": [round(float(row["value"]) / 1_000_000_000, 1) for row in gdp_series[-6:]],
    } if gdp_series else {}

    return {
        "product_name": product,
        "country_name": country,
        "country_iso2": iso2,
        "report_date": report_date,
        "author_name": author_name,
        "author_logo": author_logo,
        "hero_image": DIVIDER_IMAGES["market"],
        "methodology": {
            "intro": (
                f"This engagement file is a research-ready scaffold for assessing {product} in {country}. "
                "It is designed for Claude live research: every placeholder must be replaced with cited, "
                "triangulated evidence before client delivery."
            ),
            "objectives": [
                f"Quantify demand and market size for {product} in {country}",
                "Lock HS codes and build a trade-flow view from UN Comtrade or customs data",
                "Map regulations, import duties, certification, and route-to-market constraints",
                "Produce decision-ready recommendations with uncertainty clearly disclosed",
            ],
            "scope": [
                f"Geography: {country}",
                f"Product: {product}",
                f"Language template: {language}",
                f"Sector preset: {preset.get('label', 'Not selected - general market research')}",
            ],
            "approach": "Use the Khelifi Consulting 5-phase funnel: orientation, official sources, specialist data, news/financial cross-check, and academic validation.",
            "sources": "Primary sources to prioritize: World Bank, IMF, UN Comtrade, national statistics office, customs authority, central bank, and sector-specific databases.",
            "limitations": "This generated engagement is a structured starting point. Do not treat placeholder market values as final research output.",
        },
        "macro": {
            "tagline": "Macro profile generated from public indicators where available; complete the narrative through live research.",
            "population": _compact_number(latest_population[1]) if latest_population else "Research required",
            "population_delta": str(latest_population[0]) if latest_population else "",
            "gdp": _compact_money(latest_gdp[1]) if latest_gdp else "Research required",
            "gdp_delta": str(latest_gdp[0]) if latest_gdp else "",
            "gdp_per_capita": (
                _compact_money(latest_gdp[1] / latest_population[1])
                if latest_gdp and latest_population and latest_population[1]
                else "Research required"
            ),
            "gdp_per_capita_delta": "Derived from latest GDP/population" if latest_gdp and latest_population else "",
            "inflation": f"{latest_inflation[1]:.1f}%" if latest_inflation else "Research required",
            "inflation_delta": str(latest_inflation[0]) if latest_inflation else "",
            "fx": "Research required",
            "fx_delta": "Central bank / IMF IFS",
            "trade_balance": "Research required",
            "trade_balance_delta": "Customs / IMF",
            "rating": "Research required",
            "rating_agency": "Fitch / S&P / Moody's",
            "eodb_rank": "Research required",
            "eodb_delta": "Use replacement business climate indicators where EoDB is stale",
            "finding_headline": f"{country}'s macro context must be validated before sizing {product} demand.",
            "insights": [
                "Replace this scaffold with three sourced macro implications for demand, pricing, and market access.",
                "Flag any data older than 24 months and explain how it affects confidence.",
                f"Use local-language search terms for {country} alongside English queries.",
            ],
            "gdp_series": gdp_chart,
            "trade_series": {
                "years": [str(row["year"]) for row in trade_series[-6:]],
                "imports": [round(float(row["value"]), 1) for row in trade_series[-6:]],
                "exports": [round(float(row["value"]), 1) for row in trade_series[-6:]],
            } if trade_series else {},
        },
        "executive_summary": {
            "product_def": f"Define the exact product scope for {product}, including exclusions and HS codes.",
            "demand": "Demand sizing pending live research. Use TAM/SAM/SOM, historical CAGR, and a five-year forecast.",
            "supply": "Supply analysis pending HS-level imports, domestic production, and distributor mapping.",
            "attractiveness": "Attractiveness should be scored after validating demand depth, margin potential, regulations, and competitive intensity.",
        },
        "market": {
            "finding_headline": "Market size is not yet validated - complete live research before client delivery.",
            "value_source": "To be triangulated from 3+ sources",
            "volume_source": "To be triangulated from 3+ sources",
            "insights": [
                "Identify the demand pools by customer segment and use case.",
                "Separate current market value from forecast opportunity.",
                "Disclose assumptions when direct market data is unavailable.",
            ],
            "value_series": {"years": [], "values": []},
            "volume_series": {"years": [], "values": []},
        },
        "imports": {
            "finding_headline": "Import dependency must be validated through UN Comtrade and customs data.",
            "insights": [
                "Run HS-code trade extraction for the target country and top exporting partners.",
                "Compare import value and volume to detect price/mix effects.",
                "Use mirror trade data when reporter data is missing or stale.",
            ],
            "value_series": {"years": [], "values": []},
            "volume_series": {"years": [], "values": []},
        },
        "regulatory": {
            "rows": [
                {"item": "HS code lock", "detail": "Confirm with customs broker or official tariff schedule", "source": "Customs authority"},
                {"item": "Import duty", "detail": "Research required", "source": "National tariff schedule / WTO"},
                {"item": "VAT / sales tax", "detail": "Research required", "source": "Tax authority"},
                {"item": "Certification", "detail": "Research required", "source": "Standards authority"},
            ],
            "insights": [
                "Identify the regulatory step that most affects time-to-market.",
                "Separate formal legal requirements from distributor/buyer expectations.",
            ],
        },
        "competitive": {
            "market_share_source": "To be triangulated from company filings, trade press, distributors, and interviews",
            "rows": [
                {"player": "Research required", "hq": "Local / international", "tier": "Entry / mid / premium"},
            ],
            "insights": [
                "Build a 5-10 player competitive matrix with tier, channel, and differentiation.",
                "Validate whether the premium segment is structurally underserved.",
            ],
            "market_share": {"players": [], "shares": []},
        },
        "swot": {
            "strengths": ["Large opportunity may exist if demand is fragmented and import-dependent - validate."],
            "weaknesses": ["Current scaffold lacks validated market size and competitive share data."],
            "opportunities": ["Use specialist positioning if commodity competition is intense."],
            "threats": ["Regulatory, FX, and payment constraints may change entry economics."],
        },
        "recommendations": [
            {"title": "Complete source triangulation for all headline numbers", "priority": "High", "timeline": "Immediate", "impact": "Raises confidence and reduces hallucination risk"},
            {"title": "Validate HS codes with a customs broker", "priority": "High", "timeline": "Immediate", "impact": "Prevents incorrect tariff and import-flow analysis"},
            {"title": "Interview 5-10 market participants", "priority": "Medium", "timeline": "1-2 weeks", "impact": "Validates channel economics and competitive reality"},
        ],
        "appendix": {
            "sources": [
                "World Bank Open Data - https://data.worldbank.org/",
                "IMF DataMapper / WEO - https://www.imf.org/",
                "UN Comtrade - https://comtradeplus.un.org/",
                "WTO Tariff Download Facility - https://www.wto.org/",
                *source_names,
            ],
            "hs_codes": hs_codes or ["Research required - lock HS code before trade analysis"],
            "glossary": [
                "CAGR - Compound Annual Growth Rate",
                "TAM - Total Addressable Market",
                "SAM - Serviceable Available Market",
                "SOM - Serviceable Obtainable Market",
                "HS code - Harmonised System product classification",
            ],
        },
        "divider_images": DIVIDER_IMAGES,
    }


def resolve_output_path(output: str, language: str) -> Path:
    path = Path(output)
    if path.suffix.lower() == ".json":
        return path
    return path / f"engagement_{language}.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an engagement JSON scaffold.")
    parser.add_argument("--product", required=True, help="Product, service, or sector to research")
    parser.add_argument("--country", required=True, help="Target country or region")
    parser.add_argument("--country-iso2", help="Optional ISO 3166-1 alpha-2 override")
    parser.add_argument("--language", default="en", choices=["en", "ar", "fr"])
    parser.add_argument("--sector", help="Optional preset: healthcare, construction, food, automotive, energy")
    parser.add_argument("--author-name", default="Khelifi Consulting")
    parser.add_argument("--author-logo", default="../assets/icons/logo-mark.svg")
    parser.add_argument("--output", default="./output", help="Output JSON file or directory")
    args = parser.parse_args()

    data = build_engagement(
        product=args.product,
        country=args.country,
        language=args.language,
        country_iso2=args.country_iso2,
        sector=args.sector,
        author_name=args.author_name,
        author_logo=args.author_logo,
    )
    out = resolve_output_path(args.output, args.language)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Engagement JSON written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
