"""Brand-compliance guard: no forbidden trademarks in tracked text files.

Positions the methodology with the generic phrase 'Big 4 consulting firms'
in place of any single named firm.
"""
from __future__ import annotations
import re
import subprocess

# Forbidden tokens built at runtime so this very file stays clean of the
# string we are guarding against. The decoded value spells out the
# common four-letter big-4 firm name + the 'big-4' / 'big four' aliases.
# Only the specific four-letter trademark is forbidden. The generic
# 'Big 4 consulting firms' phrasing is the approved positioning copy and
# is intentionally allowed in tracked content.
_FORBIDDEN_TRADEMARK = bytes([107, 112, 109, 103]).decode()
PATTERN = re.compile(r"\b" + _FORBIDDEN_TRADEMARK + r"\b", re.IGNORECASE)

BINARY_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".ico", ".db", ".gif", ".svg",
               ".woff", ".woff2", ".ttf", ".otf"}


def _tracked_files(repo_root):
    res = subprocess.run(
        ["git", "ls-files"], cwd=repo_root,
        capture_output=True, text=True, check=True,
    )
    return [repo_root / line for line in res.stdout.splitlines()]


def test_no_forbidden_trademark_in_tracked_text_files(repo_root):
    """Scan every tracked text file outside tests/ for forbidden trademarks."""
    hits = []
    for f in _tracked_files(repo_root):
        if not f.is_file() or f.suffix.lower() in BINARY_EXTS:
            continue
        rel = f.relative_to(repo_root).as_posix()
        # Tests are allowed to reference the guarded terms internally.
        if rel.startswith("tests/"):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line):
                hits.append(f"{rel}:{i}: {line[:120]}")
    assert not hits, \
        "Forbidden trademark found in tracked text files:\n" + "\n".join(hits)
