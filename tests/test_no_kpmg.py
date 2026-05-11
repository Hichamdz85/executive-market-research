"""Guarantee no KPMG / Big-4 references slip back into the tree."""
from __future__ import annotations
import re
import subprocess

PATTERN = re.compile(r"\b(kpmg|big[- ]?4|big[- ]?four)\b", re.IGNORECASE)
BINARY_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".ico", ".db", ".gif", ".svg",
               ".woff", ".woff2", ".ttf", ".otf"}


def _tracked_files(repo_root):
    res = subprocess.run(
        ["git", "ls-files"], cwd=repo_root,
        capture_output=True, text=True, check=True,
    )
    return [repo_root / line for line in res.stdout.splitlines()]


def test_no_kpmg_in_tracked_text_files(repo_root):
    hits = []
    for f in _tracked_files(repo_root):
        if not f.is_file() or f.suffix.lower() in BINARY_EXTS:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line):
                rel = f.relative_to(repo_root)
                hits.append(f"{rel}:{i}: {line[:120]}")
    assert not hits, "KPMG / Big-4 found in tracked text files:\n" + "\n".join(hits)
