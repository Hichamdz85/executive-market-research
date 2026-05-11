# Quickstart — Executive Market Research

Three steps. Five minutes. One investor-grade market study.

## 1. Install

```bash
git clone https://github.com/Hichamdz85/executive-market-research.git \
  ~/.claude/skills/executive-market-research
pip install -r ~/.claude/skills/executive-market-research/requirements.txt
playwright install chromium
```

## 2. Run

In Claude Code, Claude Desktop, or via the API:

> *"Use the executive-market-research skill to produce a market study for HVAC accessories in Algeria, in English."*

For an 8-page Executive Brief instead of the full 35–45 page report:

> *"Use the executive-market-research skill in **quick mode** for solar panels in Morocco, in French."*

## 3. Get the report

Outputs `report.html` (interactive) and `report.pdf` (print-ready) in `./output/`.

For full documentation, methodology, and customisation:
[README.md](./README.md) - [SKILL.md](./SKILL.md) - [reference/khelifi_research_playbook.md](./reference/khelifi_research_playbook.md)
