"""All files required by the v2.0.0 contract are present on disk."""
from __future__ import annotations

REQUIRED = [
    # core
    "SKILL.md", "README.md", "QUICKSTART.md", "CHANGELOG.md",
    "CONTRIBUTING.md", "LICENSE", "CITATION.cff", "requirements.txt",
    # plugin manifest
    ".claude-plugin/plugin.json",
    # templates
    "templates/report_en.html", "templates/report_ar.html",
    "templates/report_fr.html", "templates/styles.css",
    # scripts
    "scripts/generate_report.py", "scripts/fetch_assets.py",
    # reference (note renamed playbook)
    "reference/khelifi_research_playbook.md",
    "reference/report_structure.md",
    "reference/data_sources.md",
    "reference/quality_standards.md",
    "reference/research_methodology.md",
    # examples
    "examples/sample_engagement.json",
    # mcp server
    "mcp-server/server.py", "mcp-server/README.md",
    "mcp-server/requirements.txt",
    # sector presets
    "presets/healthcare.json", "presets/construction.json",
    "presets/food.json", "presets/automotive.json", "presets/energy.json",
    # docs
    "docs/demo.md",
]


def test_required_files_exist(repo_root):
    missing = [p for p in REQUIRED if not (repo_root / p).exists()]
    assert not missing, f"Missing required files:\n  - " + "\n  - ".join(missing)


def test_old_playbook_was_renamed(repo_root):
    assert not (repo_root / "reference" / "kpmg_research_playbook.md").exists(), \
        "Old kpmg_research_playbook.md must be deleted; use khelifi_research_playbook.md"
