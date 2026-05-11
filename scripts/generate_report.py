#!/usr/bin/env python3
"""
Executive Market Research — Report Generator
=============================================

Renders an executive-grade market research report (HTML + PDF) from a
JSON data file describing the engagement.

Usage:
    python generate_report.py \
        --data ./engagement.json \
        --language en \
        --output ./output/

Or programmatically:
    from generate_report import ReportGenerator
    gen = ReportGenerator(data, language='en')
    gen.write_html('output/report.html')
    gen.write_pdf('output/report.pdf')

Author: Khelifi Consulting
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Engagement:
    product_name: str
    country_name: str
    country_iso2: str
    report_date: str
    author_name: str
    author_logo: str
    hero_image: str = ""
    methodology: dict = field(default_factory=dict)
    macro: dict = field(default_factory=dict)
    executive_summary: dict = field(default_factory=dict)
    market: dict = field(default_factory=dict)
    imports: dict = field(default_factory=dict)
    regulatory: dict = field(default_factory=dict)
    competitive: dict = field(default_factory=dict)
    swot: dict = field(default_factory=dict)
    recommendations: list = field(default_factory=list)
    appendix: dict = field(default_factory=dict)
    divider_images: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str | Path) -> "Engagement":
        with open(path, "r", encoding="utf-8") as fh:
            return cls(**json.load(fh))


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

def list_to_li(items: list[str]) -> str:
    return "\n".join(f"<li>{x}</li>" for x in items)


def kv_pair(label: str, value: str, delta: str = "") -> dict:
    return {"label": label, "value": value, "delta": delta}


def regulatory_rows(rows: list[dict]) -> str:
    return "\n".join(
        f"<tr><td>{r.get('item','')}</td><td>{r.get('detail','')}</td>"
        f"<td>{r.get('source','')}</td></tr>"
        for r in rows
    )


def competitive_rows(rows: list[dict]) -> str:
    return "\n".join(
        f"<tr><td>{r.get('player','')}</td><td>{r.get('hq','')}</td>"
        f"<td>{r.get('tier','')}</td></tr>"
        for r in rows
    )


def recommendations_rows(rows: list[dict]) -> str:
    out = []
    for i, r in enumerate(rows, start=1):
        prio_class = {
            "High": "priority-high",
            "Med": "priority-med",
            "Medium": "priority-med",
            "Low": "priority-low",
        }.get(r.get("priority", ""), "")
        out.append(
            f"<tr><td>{i}</td><td>{r.get('title','')}</td>"
            f"<td class='{prio_class}'>{r.get('priority','')}</td>"
            f"<td>{r.get('timeline','')}</td>"
            f"<td>{r.get('impact','')}</td></tr>"
        )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Chart configs (Chart.js JSON injected as inline JS)
# ---------------------------------------------------------------------------

CHART_TEMPLATE = """
new Chart(document.getElementById('{cid}'), {{
  type: '{ctype}',
  data: {{
    labels: {labels},
    datasets: [{{
      label: '{dlabel}',
      data: {data},
      backgroundColor: {bg},
      borderColor: chartTheme.primary,
      borderWidth: 1
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: false }},
      datalabels: {{ display: true }}
    }},
    scales: {{
      y: {{ beginAtZero: true, grid: {{ color: '#E0E0E0' }} }},
      x: {{ grid: {{ display: false }} }}
    }}
  }}
}});
"""


def make_chart(cid: str, ctype: str, labels: list, data: list, dlabel: str = "") -> str:
    bg = "chartTheme.primary"
    if ctype == "pie" or ctype == "doughnut":
        bg = "[chartTheme.primary, chartTheme.secondary, chartTheme.accent, chartTheme.c3, chartTheme.c4, chartTheme.c5]"
    return CHART_TEMPLATE.format(
        cid=cid, ctype=ctype, labels=json.dumps(labels),
        data=json.dumps(data), dlabel=dlabel, bg=bg,
    )


def build_chart_block(eng: Engagement) -> str:
    blocks = []
    macro = eng.macro
    if macro.get("gdp_series"):
        blocks.append(make_chart(
            "chart-gdp", "bar",
            macro["gdp_series"]["years"], macro["gdp_series"]["values"],
            "Nominal GDP (USD bn)",
        ))
    if macro.get("trade_series"):
        ts = macro["trade_series"]
        blocks.append(f"""
new Chart(document.getElementById('chart-trade'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(ts['years'])},
    datasets: [
      {{ label: 'Imports', data: {json.dumps(ts['imports'])}, backgroundColor: chartTheme.primary }},
      {{ label: 'Exports', data: {json.dumps(ts['exports'])}, backgroundColor: chartTheme.secondary }}
    ]
  }},
  options: {{ responsive:true, maintainAspectRatio:false,
    scales:{{ y:{{ beginAtZero:true }} }} }}
}});
""")
    if eng.market.get("value_series"):
        v = eng.market["value_series"]
        blocks.append(make_chart("chart-market-value", "bar", v["years"], v["values"], "Value (USD mn)"))
    if eng.market.get("volume_series"):
        v = eng.market["volume_series"]
        blocks.append(make_chart("chart-market-volume", "bar", v["years"], v["values"], "Volume ('000 tons)"))
    if eng.imports.get("value_series"):
        v = eng.imports["value_series"]
        blocks.append(make_chart("chart-import-value", "bar", v["years"], v["values"], "Import value (USD mn)"))
    if eng.imports.get("volume_series"):
        v = eng.imports["volume_series"]
        blocks.append(make_chart("chart-import-volume", "bar", v["years"], v["values"], "Import volume ('000 tons)"))
    if eng.competitive.get("market_share"):
        ms = eng.competitive["market_share"]
        blocks.append(make_chart("chart-market-share", "doughnut", ms["players"], ms["shares"], "Market share"))
    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    def __init__(self, engagement: Engagement, language: str = "en"):
        if language not in {"en", "ar", "fr"}:
            raise ValueError(f"Unsupported language: {language}")
        self.engagement = engagement
        self.language = language
        self.template_path = TEMPLATES / f"report_{language}.html"

    def render(self) -> str:
        eng = self.engagement
        with open(self.template_path, "r", encoding="utf-8") as fh:
            html = fh.read()

        flag_url = f"https://flagcdn.com/{eng.country_iso2.lower()}.svg"

        substitutions = {
            "{{REPORT_TITLE}}": f"{eng.product_name} — {eng.country_name}",
            "{{PRODUCT_NAME}}": eng.product_name,
            "{{COUNTRY_NAME}}": eng.country_name,
            "{{REPORT_DATE}}": eng.report_date,
            "{{AUTHOR_NAME}}": eng.author_name,
            "{{AUTHOR_LOGO}}": eng.author_logo,
            "{{HERO_IMAGE}}": eng.hero_image or eng.divider_images.get("market", ""),
            "{{FLAG_URL}}": flag_url,
            "{{FLAG_URL_LARGE}}": flag_url,
            "{{COUNTRY_TAGLINE}}": eng.macro.get("tagline", ""),
            # Methodology
            "{{METHODOLOGY_INTRO}}": eng.methodology.get("intro", ""),
            "{{METHODOLOGY_OBJECTIVES}}": list_to_li(eng.methodology.get("objectives", [])),
            "{{METHODOLOGY_SCOPE}}": list_to_li(eng.methodology.get("scope", [])),
            "{{METHODOLOGY_APPROACH}}": eng.methodology.get("approach", ""),
            "{{METHODOLOGY_SOURCES}}": eng.methodology.get("sources", ""),
            "{{METHODOLOGY_LIMITATIONS}}": eng.methodology.get("limitations", ""),
            # Macro KPIs
            "{{KPI_POPULATION}}": eng.macro.get("population", "—"),
            "{{KPI_POPULATION_DELTA}}": eng.macro.get("population_delta", ""),
            "{{KPI_GDP}}": eng.macro.get("gdp", "—"),
            "{{KPI_GDP_DELTA}}": eng.macro.get("gdp_delta", ""),
            "{{KPI_GDP_PC}}": eng.macro.get("gdp_per_capita", "—"),
            "{{KPI_GDP_PC_DELTA}}": eng.macro.get("gdp_per_capita_delta", ""),
            "{{KPI_INFLATION}}": eng.macro.get("inflation", "—"),
            "{{KPI_INFLATION_DELTA}}": eng.macro.get("inflation_delta", ""),
            "{{KPI_FX}}": eng.macro.get("fx", "—"),
            "{{KPI_FX_DELTA}}": eng.macro.get("fx_delta", ""),
            "{{KPI_TRADE_BAL}}": eng.macro.get("trade_balance", "—"),
            "{{KPI_TRADE_BAL_DELTA}}": eng.macro.get("trade_balance_delta", ""),
            "{{KPI_RATING}}": eng.macro.get("rating", "—"),
            "{{KPI_RATING_AGENCY}}": eng.macro.get("rating_agency", ""),
            "{{KPI_EODB}}": eng.macro.get("eodb_rank", "—"),
            "{{KPI_EODB_DELTA}}": eng.macro.get("eodb_delta", ""),
            "{{MACRO_FINDING_HEADLINE}}": eng.macro.get("finding_headline", ""),
            "{{MACRO_INSIGHTS}}": list_to_li(eng.macro.get("insights", [])),
            # Executive summary
            "{{EXEC_PRODUCT_DEF}}": eng.executive_summary.get("product_def", ""),
            "{{EXEC_DEMAND}}": eng.executive_summary.get("demand", ""),
            "{{EXEC_SUPPLY}}": eng.executive_summary.get("supply", ""),
            "{{EXEC_ATTRACTIVENESS}}": eng.executive_summary.get("attractiveness", ""),
            # Market
            "{{MARKET_FINDING_HEADLINE}}": eng.market.get("finding_headline", ""),
            "{{MARKET_VALUE_SOURCE}}": eng.market.get("value_source", ""),
            "{{MARKET_VOLUME_SOURCE}}": eng.market.get("volume_source", ""),
            "{{MARKET_INSIGHTS}}": list_to_li(eng.market.get("insights", [])),
            # Imports
            "{{IMPORTS_FINDING_HEADLINE}}": eng.imports.get("finding_headline", ""),
            "{{IMPORTS_INSIGHTS}}": list_to_li(eng.imports.get("insights", [])),
            # Regulatory
            "{{REGULATORY_TABLE}}": regulatory_rows(eng.regulatory.get("rows", [])),
            "{{REGULATORY_INSIGHTS}}": list_to_li(eng.regulatory.get("insights", [])),
            # Competitive
            "{{COMPETITIVE_TABLE}}": competitive_rows(eng.competitive.get("rows", [])),
            "{{COMPETITIVE_INSIGHTS}}": list_to_li(eng.competitive.get("insights", [])),
            "{{MARKET_SHARE_SOURCE}}": eng.competitive.get("market_share_source", ""),
            # SWOT
            "{{SWOT_STRENGTHS}}": list_to_li(eng.swot.get("strengths", [])),
            "{{SWOT_WEAKNESSES}}": list_to_li(eng.swot.get("weaknesses", [])),
            "{{SWOT_OPPORTUNITIES}}": list_to_li(eng.swot.get("opportunities", [])),
            "{{SWOT_THREATS}}": list_to_li(eng.swot.get("threats", [])),
            # Recommendations
            "{{RECOMMENDATIONS_TABLE}}": recommendations_rows(eng.recommendations),
            # Appendix
            "{{APPENDIX_SOURCES}}": list_to_li(eng.appendix.get("sources", [])),
            "{{APPENDIX_HS_CODES}}": list_to_li(eng.appendix.get("hs_codes", [])),
            "{{APPENDIX_GLOSSARY}}": list_to_li(eng.appendix.get("glossary", [])),
            # Divider images
            "{{DIVIDER_IMAGE_METHODOLOGY}}": eng.divider_images.get("methodology", ""),
            "{{DIVIDER_IMAGE_COUNTRY}}": eng.divider_images.get("country", ""),
            "{{DIVIDER_IMAGE_EXEC}}": eng.divider_images.get("exec", ""),
            "{{DIVIDER_IMAGE_MARKET}}": eng.divider_images.get("market", ""),
            "{{DIVIDER_IMAGE_IMPORTS}}": eng.divider_images.get("imports", ""),
            "{{DIVIDER_IMAGE_REGULATORY}}": eng.divider_images.get("regulatory", ""),
            "{{DIVIDER_IMAGE_COMPETITIVE}}": eng.divider_images.get("competitive", ""),
            "{{DIVIDER_IMAGE_CONCLUSION}}": eng.divider_images.get("conclusion", ""),
            "{{DIVIDER_IMAGE_APPENDIX}}": eng.divider_images.get("appendix", ""),
            # Charts
            "{{CHART_CONFIGS}}": build_chart_block(eng),
        }

        for placeholder, value in substitutions.items():
            html = html.replace(placeholder, str(value))

        # Strip any unused placeholders so output stays clean
        html = re.sub(r"\{\{[A-Z_]+\}\}", "", html)
        return html

    def write_html(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered = self.render()
        # Inline the CSS so the HTML is fully self-contained
        css_path = TEMPLATES / "styles.css"
        if css_path.exists():
            css = css_path.read_text(encoding="utf-8")
            rendered = rendered.replace(
                '<link rel="stylesheet" href="styles.css">',
                f"<style>\n{css}\n</style>",
            )
        path.write_text(rendered, encoding="utf-8")
        return path

    def write_pdf(self, html_path: str | Path, pdf_path: str | Path) -> Path:
        """Convert the rendered HTML file to PDF.

        Tries Playwright first (best fidelity), falls back to WeasyPrint.
        """
        html_path = Path(html_path).resolve()
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            from playwright.sync_api import sync_playwright  # type: ignore
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(html_path.as_uri(), wait_until="networkidle")
                page.pdf(
                    path=str(pdf_path),
                    format="A4", landscape=True,
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                )
                browser.close()
            return pdf_path
        except ImportError:
            pass

        try:
            from weasyprint import HTML  # type: ignore
            HTML(str(html_path)).write_pdf(str(pdf_path))
            return pdf_path
        except ImportError as e:
            raise RuntimeError(
                "Neither Playwright nor WeasyPrint is installed. "
                "Install one: `pip install playwright && playwright install chromium` "
                "or `pip install weasyprint`."
            ) from e


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate executive market research report.")
    parser.add_argument("--data", required=True, help="Path to engagement JSON file")
    parser.add_argument("--language", default="en", choices=["en", "ar", "fr"], help="Report language")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--quick", action="store_true", help="Quick mode (Executive Brief, 8-10 pages)")
    args = parser.parse_args()

    # Quick mode marker - propagated to the engagement so templates and
    # downstream tooling can react. Trimming sections is the responsibility
    # of the calling pipeline (Claude composes a smaller engagement.json).
    quick_mode = bool(args.quick)

    eng = Engagement.from_json(args.data)
    if quick_mode:
        # Quick Mode: trim optional deep-dive sections at runtime so the
        # full pipeline still works against any engagement JSON.
        eng.imports = {}
        eng.regulatory = {}
        eng.competitive = {}
        eng.appendix = {}
        print('[quick mode] Executive Brief - 4 deep-dive sections trimmed')
    gen = ReportGenerator(eng, language=args.language)

    out = Path(args.output)
    html_path = gen.write_html(out / f"report_{args.language}.html")
    print(f"✓ HTML written: {html_path}")

    if not args.no_pdf:
        try:
            pdf_path = gen.write_pdf(html_path, out / f"report_{args.language}.pdf")
            print(f"✓ PDF written: {pdf_path}")
        except RuntimeError as e:
            print(f"⚠ PDF generation skipped: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
