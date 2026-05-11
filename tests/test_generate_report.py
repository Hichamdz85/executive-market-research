"""Smoke-test the generation pipeline (HTML only, no PDF)."""
from __future__ import annotations
import subprocess
import sys


def _run(repo_root, tmp_path, language: str, extra=()):
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "generate_report.py"),
        "--data", str(repo_root / "examples" / "sample_engagement.json"),
        "--language", language,
        "--output", str(tmp_path),
        "--no-pdf",
        *extra,
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def test_generate_html_english(repo_root, tmp_path):
    res = _run(repo_root, tmp_path, "en")
    assert res.returncode == 0, f"stderr: {res.stderr}"
    assert (tmp_path / "report_en.html").exists()


def test_generate_html_arabic(repo_root, tmp_path):
    res = _run(repo_root, tmp_path, "ar")
    assert res.returncode == 0, f"stderr: {res.stderr}"
    assert (tmp_path / "report_ar.html").exists()


def test_generate_html_french(repo_root, tmp_path):
    res = _run(repo_root, tmp_path, "fr")
    assert res.returncode == 0, f"stderr: {res.stderr}"
    assert (tmp_path / "report_fr.html").exists()


def test_quick_mode_flag_accepted(repo_root, tmp_path):
    """The --quick flag must be accepted (Quick Mode is part of v2.0.0)."""
    res = _run(repo_root, tmp_path, "en", extra=("--quick",))
    assert res.returncode == 0, f"--quick was rejected: {res.stderr}"
