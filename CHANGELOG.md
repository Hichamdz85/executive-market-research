# Changelog

All notable changes to **Executive Market Research** are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.1.0] - 2026-05-13

### Added
- `scripts/build_engagement.py` to create a research-ready engagement JSON
  from `--product`, `--country`, and `--language` inputs.
- Standalone CLI support for `--product` / `--country` in
  `scripts/generate_report.py`, while retaining `--data` rendering.
- `data.json` output on every render for downstream workflows.
- HTML escaping across rendered report content to prevent raw user input from
  being injected into templates.
- MCP mock test coverage for UN Comtrade request construction.
- CI jobs for HTML smoke tests, PDF smoke rendering, MCP smoke tests, and
  markdown link checking.
- Release workflow that builds a clean ZIP package, sample PDFs/HTML files,
  and a short demo GIF for tagged GitHub releases.
- `scripts/package_release.py` and `scripts/create_demo_gif.py` for release
  asset generation.

### Fixed
- UN Comtrade MCP tool now uses the public preview endpoint shape
  `/public/v1/preview/C/A/HS` and numeric Comtrade country codes.
- PDF rendering now falls back cleanly from Playwright to WeasyPrint and keeps
  the HTML report when PDF generation is unavailable.
- Chart data labels now load and register the Chart.js datalabels plugin.

### Changed
- README, QUICKSTART, and SKILL docs now distinguish between a research
  scaffold and a fully researched client-ready report.

## [2.0.0] - 2026-05-11

### Added
- **Production-grade upgrade** raising the maturity bar from 7.1 to 9.5 / 10.
- `QUICKSTART.md` - 3-step onboarding (Install -> Run -> Get Report).
- `tests/` - pytest suite covering YAML manifest, file presence, HTML
  templates, generation pipeline (3 languages), Quick Mode flag, and a
  brand-compliance guard (`tests/test_brand_compliance.py`) that keeps
  the methodology positioned as **Big 4 consulting firms** without
  naming any specific firm.
- `mcp-server/` - bundled MCP server exposing 4 tools (`get_country_macro`,
  `get_trade_data`, `search_market_data`, `generate_report`).
- `.claude-plugin/plugin.json` - Claude Code plugin manifest pointing at
  the skill and the MCP server.
- `presets/` - 5 sector presets (healthcare, construction, food, automotive,
  energy) with HS codes, specialised sources, interview questions, and
  key indicators.
- `CITATION.cff` - academic citation metadata.
- `docs/demo.md` - guided pipeline walkthrough with screenshots.
- Multilingual repo intro - Arabic and French sections in `README.md`.
- `--quick` flag in `scripts/generate_report.py` produces an 8-10 page
  Executive Brief by trimming 4 optional deep-dive sections.
- `pytest` and `pyyaml` added to `requirements.txt`.

### Changed
- **SKILL.md** - frontmatter compacted, version bumped to 2.0.0, added
  `languages` and `modes` fields, expanded `keywords`. Body adds a
  `## Modes` section documenting Full vs Quick.
- **`.github/workflows/ci.yml`** - replaced inline checks with a single
  `pytest` job covering all validation.

## [1.2.0] — 2026-05-10

### Added
- 📸 Real screenshots of generated reports in `docs/screenshots/`
- 🎨 Open Graph social sharing image (`docs/og-image.png`) — `1200×630px`
- 📋 `CONTRIBUTING.md` with workflow, style guide, and translation guide
- 📅 `CHANGELOG.md` with full version history (this file)
- 🐛 GitHub issue templates: `bug_report.md`, `feature_request.md`, `language_request.md`
- 💰 GitHub Sponsors `FUNDING.yml`
- 🤖 GitHub Actions CI workflow — validates skill on every push
- 📦 Real sample PDF attached to v1.2.0 release as a downloadable asset
- 🔍 Expanded `SKILL.md` description with more trigger phrases for better Claude invocation

### Changed
- README screenshot references now point to real images (no more broken `docs/preview-*.png`)
- Sample engagement JSON now references the local KH SVG logo (no more `via.placeholder.com`)
- README badges expanded — version, license, stars, language count, build status

### Fixed
- Wrong landing-page URL in v1.0.0 release notes (now `hichamdz85.github.io`, not `khelifi-consulting.github.io`)

## [1.1.0] — 2026-05-10

### Changed
- 🎨 **Brand identity** — Replaced legacy navy palette with Khelifi Consulting **charcoal (#1F1F23)** + **gold (#C9A45A)**
- Landing page redesigned with **Cormorant Garamond** serif typography (elegant, editorial)
- Color tokens in `templates/styles.css` updated globally

### Added
- KH monogram SVG (`assets/icons/logo-mark.svg`)
- Full wordmark SVG (`assets/icons/logo-khelifi.svg`)
- Geometric gold pattern SVG (`assets/icons/khelifi-pattern.svg`)
- Author / hire section on landing page

## [1.0.0] — 2026-05-10

### Added
- 🎯 Initial release — Khelifi Consulting-grade market research skill for Claude
- **9-section structure**: Methodology · Country macro · Executive summary · Market · Imports · Regulatory · Competitive · SWOT · Appendix
- **Trilingual support**: English, Arabic (full RTL), French
- **7 Golden Rules** of Khelifi Consulting research methodology in `reference/khelifi_research_playbook.md`:
  1. Triangulation (≥3 sources per number)
  2. Freshness (<18 months)
  3. Multilingual search
  4. Official sources first
  5. Benchmarking against peer countries
  6. ESG mandatory coverage
  7. Primary research simulation
- **Live web research** via Claude's web search + curated source map (UN Comtrade, World Bank, IMF, EIU, Statista, Euromonitor, BMI)
- **HTML + PDF output** via Playwright (Chart.js for charts, vector PDF)
- Country flag fetching via flagcdn.com
- 8-tile macro KPI dashboard
- SWOT 2×2 matrix + recommendations table
- 6 SVG section icons in executive-grade line art
- Sample HVAC Algeria engagement (3 generated HTML reports)
- GitHub Pages landing site
- MIT license

[Unreleased]: https://github.com/Hichamdz85/executive-market-research/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/Hichamdz85/executive-market-research/compare/v2.0.0...v2.1.0
[1.2.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.2.0
[1.1.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.1.0
[1.0.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.0.0
[2.0.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v2.0.0
