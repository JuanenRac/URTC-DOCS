# =============================================================================
# URTC-DOCS - tests/test_related.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import pytest

from urtc_docs import cli, related
from urtc_docs.readme_family import all_names

SAMPLE = "# T\n\n## 🔗 Related Projects\n\nold text\n\n- **x** - old\n\n## 📚 Documentation\n\nkeep\n"


@pytest.mark.parametrize("code", sorted(related.FILES))
def test_section_lists_the_family_and_no_claim_of_belonging(code):
    out = related.apply_to_text(SAMPLE, code, "URTC-TESTER")
    assert "old text" not in out and out.endswith("## 📚 Documentation\n\nkeep\n")
    for name in all_names():
        assert name in out
    assert out.count("**URTC-TESTER**") == 1
    assert "part of the HYDRA" not in out


def test_idempotent_and_keeps_the_line_endings():
    once = related.apply_to_text(SAMPLE.replace("\n", "\r\n"), "en", "URTC")
    assert "\r\n" in once and "\n" not in once.replace("\r\n", "")
    assert related.apply_to_text(once, "en", "URTC") == once


def test_a_readme_without_the_section_is_reported():
    with pytest.raises(ValueError):
        related.apply_to_text("# T\n\n## Other\n", "en", "URTC")


def test_check_and_apply_on_a_workspace(tmp_path):
    for name in ("URTC", "URTC-COMMON"):
        folder = tmp_path / name
        folder.mkdir()
        for filename in related.FILES.values():
            (folder / filename).write_text(SAMPLE, encoding="utf-8", newline="\n")
    base = ["--workspace", str(tmp_path), "--repo", "URTC", "--repo", "URTC-COMMON"]
    assert cli.make_related([*base, "--check"]) == 1
    assert cli.make_related([*base, "--apply"]) == 0
    assert cli.make_related([*base, "--check"]) == 0
    assert cli.make_related([*base, "--repo", "URTC-NOPE", "--check"]) == 1
