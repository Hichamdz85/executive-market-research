#!/usr/bin/env python3
"""Executive Market Research - MCP Server.

Exposes 4 tools to any MCP-compatible client (Claude Code, Claude Desktop,
Cursor, etc.):

  - get_country_macro       Macro indicators from World Bank Open Data
  - get_trade_data          Import/export flows from UN Comtrade
  - search_market_data      Workplan + sector-preset suggestions
  - generate_report         Render the full HTML+PDF deliverable

Author: Khelifi Consulting <info@khelificonsulting.com>
License: MIT
"""
from __future__ import annotations

import datetime
import json
import subprocess
from pathlib import Path
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).resolve().parent.parent

mcp = FastMCP("executive-market-research")

# Minimal ISO2 -> UN Comtrade numeric reporter/partner code map.
# Extend in production via the official Comtrade reference table.
_ISO2_TO_COMTRADE = {
    "DZ": "12", "MA": "504", "TN": "788", "EG": "818",
    "SA": "682", "AE": "784", "QA": "634", "KW": "414",
    "BH": "48", "OM": "512", "JO": "400", "LB": "422",
    "FR": "251", "BE": "56", "DE": "276", "IT": "381",
    "ES": "724", "GB": "826", "US": "842", "CN": "156",
    "JP": "392", "TR": "792", "IN": "699", "BR": "76",
    "ZA": "710", "NG": "566", "KE": "404",
}


def _comtrade_code(value: str) -> str:
    value = str(value).strip().upper()
    if value in {"0", "WORLD", "ALL"}:
        return "0"
    if value.isdigit():
        return value
    return _ISO2_TO_COMTRADE.get(value, value)


@mcp.tool()
async def get_country_macro(iso2: str, indicators: list[str] | None = None) -> dict:
    """Fetch macroeconomic indicators from the World Bank Open Data API.

    Args:
        iso2: ISO 3166-1 alpha-2 country code (e.g. "DZ" for Algeria).
        indicators: Optional list of World Bank indicator codes. Defaults to
                    GDP current US$, population, CPI inflation %, trade % of GDP.

    Returns:
        Dict with the country code and per-indicator time series.
    """
    indicators = indicators or [
        "NY.GDP.MKTP.CD",
        "SP.POP.TOTL",
        "FP.CPI.TOTL.ZG",
        "NE.TRD.GNFS.ZS",
    ]
    out: dict[str, Any] = {"country": iso2.upper(), "indicators": {}}
    async with httpx.AsyncClient(timeout=30) as client:
        for ind in indicators:
            url = (
                f"https://api.worldbank.org/v2/country/{iso2.lower()}"
                f"/indicator/{ind}?format=json&per_page=15"
            )
            try:
                resp = await client.get(url)
                data = resp.json()
            except Exception as e:
                out["indicators"][ind] = {"error": str(e)}
                continue
            series = []
            if isinstance(data, list) and len(data) > 1 and data[1]:
                for row in data[1]:
                    if row.get("value") is not None:
                        series.append(
                            {"year": int(row["date"]), "value": row["value"]}
                        )
            out["indicators"][ind] = series
    return out


@mcp.tool()
async def get_trade_data(
    reporter_iso2: str,
    hs_code: str,
    partner_iso2: str = "0",
    years: int = 5,
    flow: str = "M",
) -> dict:
    """Fetch import/export flows from UN Comtrade public preview API.

    Args:
        reporter_iso2: ISO2 of the reporter country (e.g. "DZ").
        hs_code: HS code at 2/4/6 digits (e.g. "8419" for HVAC equipment).
        partner_iso2: Partner ISO2; "0" for World total. Default "0".
        years: Number of recent years (default 5).
        flow: "M" = imports, "X" = exports. Default "M".

    Returns:
        Dict with rows and a count, or an error.
    """
    rep = _comtrade_code(reporter_iso2)
    par = _comtrade_code(partner_iso2)
    end_year = datetime.date.today().year - 1
    periods = [str(y) for y in range(end_year - years + 1, end_year + 1)]
    url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
    base_params = {
        "reporterCode": rep,
        "partnerCode": par,
        "cmdCode": hs_code,
        "flowCode": flow,
        "maxRecords": "500",
        "includeDesc": "true",
        "breakdownMode": "classic",
    }
    rows = []
    errors = []
    async with httpx.AsyncClient(timeout=60) as client:
        for period in periods:
            params = {**base_params, "period": period}
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                errors.append({"period": period, "error": str(e), "params": params})
                continue
            for r in data.get("data", []):
                rows.append({
                    "year": r.get("refYear") or r.get("period"),
                    "reporter": r.get("reporterDesc"),
                    "partner": r.get("partnerDesc"),
                    "hs_code": r.get("cmdCode"),
                    "hs_description": r.get("cmdDesc"),
                    "value_usd": r.get("primaryValue"),
                    "qty": r.get("qty"),
                    "qty_unit": r.get("qtyUnitAbbr"),
                })
    return {
        "rows": rows,
        "count": len(rows),
        "errors": errors,
        "params": {**base_params, "periods": periods},
        "endpoint": url,
    }


@mcp.tool()
def search_market_data(
    product: str, country: str, language: str = "en", sector: str | None = None
) -> dict:
    """Compose a structured research workplan for a product+country combination.

    If a sector preset matches (or is given via `sector`), this returns the
    relevant HS codes, specialised sources, and pre-defined interview
    questions. Does NOT execute web searches itself - that is Claude's job
    when running the parent skill.
    """
    presets_dir = REPO_ROOT / "presets"
    sectors: dict[str, dict] = {}
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.json")):
            sectors[p.stem] = json.loads(p.read_text(encoding="utf-8"))
    chosen = None
    if sector and sector.lower() in sectors:
        chosen = sectors[sector.lower()]
    return {
        "product": product,
        "country": country,
        "language": language,
        "sector_chosen": sector if chosen else None,
        "sector_preset": chosen,
        "available_sector_presets": sorted(sectors.keys()),
        "research_funnel": [
            "1. Pick or extend the sector preset; lock the HS codes.",
            "2. get_country_macro(iso2) for the macro tile dashboard.",
            "3. get_trade_data(reporter_iso2, hs_code) for each HS code.",
            "4. Triangulate every headline number against >=3 sources.",
            "5. generate_report(engagement_json) to render the deliverable.",
        ],
    }


@mcp.tool()
def generate_report(
    engagement_json: str,
    language: str = "en",
    output_dir: str = "./output",
    quick: bool = False,
    no_pdf: bool = False,
) -> dict:
    """Render the executive market research deliverable (HTML + PDF).

    Args:
        engagement_json: Path to a structured engagement JSON file.
        language: en / ar / fr.
        output_dir: Output directory.
        quick: True for the 8-10 page Executive Brief.
        no_pdf: Skip PDF rendering (HTML only).
    """
    cmd = [
        "python3",
        str(REPO_ROOT / "scripts" / "generate_report.py"),
        "--data", engagement_json,
        "--language", language,
        "--output", output_dir,
    ]
    if quick:
        cmd.append("--quick")
    if no_pdf:
        cmd.append("--no-pdf")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    return {
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returncode": proc.returncode,
        "html": str(Path(output_dir) / f"report_{language}.html"),
        "pdf": None if no_pdf else str(Path(output_dir) / f"report_{language}.pdf"),
    }


if __name__ == "__main__":
    mcp.run()
