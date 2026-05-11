"""HTML templates carry the placeholders the renderer expects."""
from __future__ import annotations

PLACEHOLDERS = [
    "{{PRODUCT_NAME}}", "{{COUNTRY_NAME}}", "{{REPORT_DATE}}",
    "{{AUTHOR_LOGO}}", "{{FLAG_URL}}", "{{CHART_CONFIGS}}",
]


def test_templates_have_required_placeholders(repo_root):
    for name in ("report_en.html", "report_ar.html", "report_fr.html"):
        html = (repo_root / "templates" / name).read_text(encoding="utf-8")
        missing = [p for p in PLACEHOLDERS if p not in html]
        assert not missing, f"{name} missing placeholders: {missing}"


def test_arabic_template_is_rtl(repo_root):
    html = (repo_root / "templates" / "report_ar.html").read_text(encoding="utf-8")
    lower = html.lower()
    assert 'dir="rtl"' in lower or "direction:rtl" in lower or "direction: rtl" in lower, \
        "Arabic template missing RTL declaration"


def test_templates_have_html_root(repo_root):
    for name in ("report_en.html", "report_ar.html", "report_fr.html"):
        html = (repo_root / "templates" / name).read_text(encoding="utf-8")
        assert "<html" in html.lower(), f"{name}: no <html> root element"
        assert "</html>" in html.lower(), f"{name}: no closing </html>"
