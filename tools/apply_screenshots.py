#!/usr/bin/env python3
# =============================================================================
# URTC-DOCS - tools/apply_screenshots.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Writes the Screenshots section of the READMEs of the programs that have a window (the texts are in ``src/urtc_docs/readme_shots.py``).

    python tools/apply_screenshots.py [--base FOLDER]           # the eight README files of every program, next to this repository
    python tools/apply_screenshots.py --check [--base FOLDER]   # only reports: the section is there, equal and its images exist

The table sits between the markers ``<!-- urtc-shots -->`` and ``<!-- /urtc-shots -->``; what is outside is left as it is. A picture of the section
that an older README showed by hand (a ``<p align="center">`` block with an image of ``images/*_V1_1.png``, or the line that shows a picture of
``docs/screenshots/``) is taken out the first time. A README that has no Screenshots section yet gets one in front of Features. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from urtc_docs.readme_shots import CAPTIONS, CODES, FILES, HEADING, NOTE, SHOTS  # noqa: E402

OPEN, CLOSE = "<!-- urtc-shots -->", "<!-- /urtc-shots -->"
OLD_BLOCK = re.compile(r'<p align="center">\s*<img src="images/URTC_[A-Z_]+_V1_1\.png"[^>]*>\s*</p>\s*\n')
OLD_LINE = re.compile(r"^!\[[^\]]*\]\(docs/screenshots/[a-z]+-deck\.png\)\s*\n\s*\n?", re.MULTILINE)


def block(repo: str, code: str) -> str:
    cells = [
        f'<td width="50%" valign="top"><img src="images/screenshots/{file}.png" alt="{CAPTIONS[key][code]}" width="100%"><br><sub>{CAPTIONS[key][code]}</sub></td>'
        for file, key in SHOTS[repo]
    ]
    if len(cells) % 2:
        cells.append('<td width="50%"></td>')
    rows = "\n".join("<tr>\n" + "\n".join(cells[i:i + 2]) + "\n</tr>" for i in range(0, len(cells), 2))
    return f"{OPEN}\n{NOTE[code]}\n\n<table>\n{rows}\n</table>\n{CLOSE}\n"


def apply(text: str, repo: str, code: str) -> str:
    nl = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    new = block(repo, code)
    if OPEN in text:
        text = re.sub(re.escape(OPEN) + r".*?" + re.escape(CLOSE) + r"\n", lambda _m: new, text, count=1, flags=re.DOTALL)
    else:
        heading = re.search(r"^## 🖼️[^\n]*\n\n", text, re.MULTILINE)
        if heading:
            start, end = heading.span()
            section_end = text.find("\n## ", end)
            body = text[end:section_end if section_end >= 0 else len(text)]
            cleaned = OLD_LINE.sub("", OLD_BLOCK.sub("", body))
            text = text[:end] + new + "\n" + cleaned.lstrip("\n") + text[end + len(body):]
        else:
            features = re.search(r"^## ✨", text, re.MULTILINE)
            if not features:
                raise SystemExit(f"{repo} {code}: no place for the section (no Features heading)")
            text = text[:features.start()] + f"## 🖼️ {HEADING[code]}\n\n{new}\n" + text[features.start():]
    return text.replace("\n", nl)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=str(ROOT.parent))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    base = Path(args.base)
    problems: list[str] = []
    for repo in SHOTS:
        for code in CODES:
            path = base / repo / FILES[code]
            raw = path.read_bytes().decode("utf-8")
            if args.check:
                if block(repo, code) not in raw.replace("\r\n", "\n"):
                    problems.append(f"{repo}/{FILES[code]}: the Screenshots section is missing or differs")
                for file, _ in SHOTS[repo]:
                    if not (base / repo / "images" / "screenshots" / f"{file}.png").is_file():
                        problems.append(f"{repo}: images/screenshots/{file}.png is missing")
                continue
            result = apply(raw, repo, code)
            if result != raw:
                path.write_bytes(result.encode("utf-8"))
                print("wrote", path)
    for problem in sorted(set(problems)):
        print("PROBLEM", problem)
    if args.check:
        print("SCREENSHOTS=PASS" if not problems else "SCREENSHOTS=FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
