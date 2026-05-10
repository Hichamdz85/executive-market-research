# Contributing to Executive Market Research

Thank you for considering a contribution. This skill is built by [Khelifi Consulting](https://khelificonsulting.com) and made open to the community under the MIT license.

## Ways to contribute

| Area | Examples | Difficulty |
|------|----------|-----------|
| 🌍 **New language templates** | Spanish, Portuguese, German, Turkish, Chinese | ⭐ |
| 📊 **New data source maps** | Add country/sector sources to `reference/data_sources.md` | ⭐ |
| 🎨 **New chart types** | Treemap, geographic heatmap, waterfall | ⭐⭐ |
| 🖼️ **Better stock imagery** | Curated section-divider images | ⭐ |
| 🐛 **Bug fixes** | Open an issue first | ⭐⭐ |
| ✨ **Feature ideas** | Discuss in an issue before PR | ⭐⭐ |
| 📚 **Documentation** | Improve `reference/*.md` files | ⭐ |
| 🧪 **Test cases** | Sample engagement JSONs for different sectors | ⭐ |

## Workflow

1. **Open an issue first** for anything bigger than a typo. This avoids duplicate work.
2. **Fork** the repo and create a topic branch: `git checkout -b feat/spanish-template`
3. **Make changes** with clear commit messages following conventional commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation only
   - `style:` formatting, no code change
   - `refactor:` code change that neither fixes a bug nor adds a feature
4. **Test locally**:
   ```bash
   python scripts/generate_report.py \
     --data examples/sample_engagement.json \
     --language en \
     --output ./test-output/
   ```
5. **Open a PR** with a clear description. Reference the issue number.

## Adding a new language template

1. Copy `templates/report_en.html` to `templates/report_xx.html` (where `xx` is the ISO 639-1 code)
2. Translate all the static strings (section headings, labels, footers)
3. If the language is RTL (Hebrew, Urdu, Persian, etc.), update `<html lang="xx" dir="rtl">` and ensure CSS RTL support works
4. Update `scripts/generate_report.py` — add `xx` to the `language` choices in argparse
5. Update `README.md` languages table
6. Add a sample translated paragraph to `landing-page/index.html` under "Languages"

## Adding a new sector data source

Edit `reference/data_sources.md` and add under the "Sector-specific sources" heading. Format:

```markdown
### My Sector
- **Source name** — https://example.com — what it provides
- **Another source** — https://example.com — coverage notes
```

PRs that add country-specific sources for under-served markets (sub-Saharan Africa, Central Asia, Pacific Islands) are especially welcome.

## Style guide

- **Python**: PEP 8, 4-space indent, type hints where reasonable
- **HTML/CSS**: 2-space indent, lowercase tag names
- **Markdown**: GitHub-flavoured, blank line before/after lists & headers
- **Commits**: imperative mood, ≤72 chars subject line

## Reporting bugs

Use the **Bug report** issue template. Include:
- Operating system
- Python version
- Exact command run
- Full error trace
- Expected vs. actual behaviour

## Reporting security issues

Do **not** open a public issue for security vulnerabilities. Email **info@khelificonsulting.com** with details. We'll respond within 48 hours.

## Code of conduct

Be kind. Disagree on substance, not on people. Every contributor — regardless of experience, language, or background — is welcome.

## License

By contributing, you agree your contributions will be licensed under the MIT license.

---

Maintainer: **Khelifi Consulting** · info@khelificonsulting.com
