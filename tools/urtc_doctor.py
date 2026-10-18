#!/usr/bin/env python3
# =============================================================================
# URTC-DOCS - tools/urtc_doctor.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Thin script: the work is done by urtc_docs.cli.doctor (run it with --help)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from urtc_docs import cli  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(cli.doctor())
