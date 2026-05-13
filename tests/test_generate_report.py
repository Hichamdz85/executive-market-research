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


def test_generate_from_product_country_cli(repo_root, tmp_path):
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "generate_report.py"),
        "--product", "Solar panels",
        "--country", "XX",
        "--language", "en",
        "--output", str(tmp_path),
        "--no-pdf",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, f"stderr: {res.stderr}"
    assert (tmp_path / "engagement_en.json").exists()
    assert (tmp_path / "data.json").exists()
    assert (tmp_path / "report_en.html").exists()


def test_html_escapes_engagement_values(repo_root, tmp_path):
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "generate_report.py"),
        "--product", "<script>alert(1)</script>",
        "--country", "XX",
        "--language", "en",
        "--output", str(tmp_path),
        "--no-pdf",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, f"stderr: {res.stderr}"
    html = (tmp_path / "report_en.html").read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
