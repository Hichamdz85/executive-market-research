"""Validate SKILL.md frontmatter is well-formed and complete."""
from __future__ import annotations
import re
import pathlib
import yaml


def _frontmatter(repo_root: pathlib.Path) -> dict:
    content = (repo_root / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert m, "SKILL.md is missing YAML frontmatter"
    return yaml.safe_load(m.group(1))


def test_skill_md_exists(repo_root):
    assert (repo_root / "SKILL.md").exists()


def test_yaml_parses(repo_root):
    fm = _frontmatter(repo_root)
    assert isinstance(fm, dict), "Frontmatter is not a YAML mapping"


def test_required_fields_present(repo_root):
    fm = _frontmatter(repo_root)
    for field in ("name", "description", "license", "version", "author"):
        assert field in fm, f"Missing frontmatter field: {field}"


def test_languages_field(repo_root):
    fm = _frontmatter(repo_root)
    assert "languages" in fm, "Missing `languages` frontmatter field"
    assert set(fm["languages"]) >= {"en", "ar", "fr"}, \
        f"languages must include en, ar, fr (got {fm['languages']})"


def test_version_is_semver(repo_root):
    fm = _frontmatter(repo_root)
    assert re.match(r"^\d+\.\d+\.\d+", str(fm["version"])), \
        f"Version must be semver (got {fm['version']!r})"


def test_description_is_concise(repo_root):
    fm = _frontmatter(repo_root)
    assert len(fm["description"]) < 1500, \
        "Description should be < 1500 chars (compact YAML)"
