# Quickstart — Executive Market Research

Three steps. Five minutes. One investor-grade market study.

## 1. Install

```bash
git clone https://github.com/Hichamdz85/executive-market-research.git \
  ~/.claude/skills/executive-market-research
pip install -r ~/.claude/skills/executive-market-research/requirements.txt
playwright install chromium
```

Or download the latest release ZIP from GitHub Releases and unzip it into
`~/.claude/skills/executive-market-research`.

## 2. Run

In Claude Code, Claude Desktop, or via the API:

> *"Use the executive-market-research skill to produce a market study for HVAC accessories in Algeria, in English."*

For an 8-page Executive Brief instead of the full 35–45 page report:

> *"Use the executive-market-research skill in **quick mode** for solar panels in Morocco, in French."*

## 3. Get the report

Outputs `report.html` (interactive) and `report.pdf` (print-ready) in `./output/`.

Standalone CLI:

```bash
python scripts/generate_report.py \
  --product "HVAC accessories" \
  --country "Algeria" \
  --language en \
  --output ./output/
```

The standalone command creates a research scaffold plus HTML/PDF output.
Before sending to a client, replace scaffold fields with cited live research.

For full documentation, methodology, and customisation:
[README.md](./README.md) - [SKILL.md](./SKILL.md) - [reference/khelifi_research_playbook.md](./reference/khelifi_research_playbook.md)
