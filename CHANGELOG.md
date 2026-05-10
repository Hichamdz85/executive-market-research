# Changelog

All notable changes to **Executive Market Research** are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
- 🎨 **Brand identity** — Replaced KPMG navy palette with Khelifi Consulting **charcoal (#1F1F23)** + **gold (#C9A45A)**
- Landing page redesigned with **Cormorant Garamond** serif typography (elegant, editorial)
- Color tokens in `templates/styles.css` updated globally

### Added
- KH monogram SVG (`assets/icons/logo-mark.svg`)
- Full wordmark SVG (`assets/icons/logo-khelifi.svg`)
- Geometric gold pattern SVG (`assets/icons/khelifi-pattern.svg`)
- Author / hire section on landing page

## [1.0.0] — 2026-05-10

### Added
- 🎯 Initial release — KPMG-grade market research skill for Claude
- **9-section structure**: Methodology · Country macro · Executive summary · Market · Imports · Regulatory · Competitive · SWOT · Appendix
- **Trilingual support**: English, Arabic (full RTL), French
- **7 Golden Rules** of research methodology in `reference/kpmg_research_playbook.md`:
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
- 6 SVG section icons in KPMG-style line art
- Sample HVAC Algeria engagement (3 generated HTML reports)
- GitHub Pages landing site
- MIT license

[Unreleased]: https://github.com/Hichamdz85/executive-market-research/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.2.0
[1.1.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.1.0
[1.0.0]: https://github.com/Hichamdz85/executive-market-research/releases/tag/v1.0.0
