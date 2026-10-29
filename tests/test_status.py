# =============================================================================
# URTC-DOCS - tests/test_status.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The 'Project status' table: the one of this repository in eight languages, and the check that every repository has one."""
from __future__ import annotations

from pathlib import Path

from conftest import REPO, write_repo
from urtc_docs import cli, glance, status

README = "# Title\n\n## 📋 At a glance\n\ntable\n\n## Overview\n\nBody.\n"


def test_every_language_has_the_same_rows_and_the_same_lights():
    assert set(status.UI) == set(status.OWN_ROWS) == set(glance.LANGUAGE_FILES)
    english = [light for _, light, _ in status.OWN_ROWS["en"]]
    assert len(english) >= status.MIN_ROWS and all(light in status.LIGHTS for light in english)
    for code, rows in status.OWN_ROWS.items():
        assert [light for _, light, _ in rows] == english, code
        assert all(part and note for part, _, note in rows), code
        heading, legend, heads = status.UI[code]
        assert heading and all(light in legend for light in status.LIGHTS) and len(heads) == 3, code


def test_the_section_of_this_repository_is_a_valid_table_in_every_language():
    for code in status.UI:
        section = status.render_own(code)
        assert section.startswith("## 🚦 ") and section.endswith("\n\n")
        assert status.check_text(README + "\n" + section) == [], code
        assert len(status.lights(section)) == len(status.OWN_ROWS[code])


def test_check_says_what_is_wrong():
    good = status.render_own("en")
    assert status.check_text(README) == ["the 'Project status' section is missing"]
    assert any("not 'ok'" in p or "only a light" in p for p in status.check_text(README + good.replace("| 🟢 |", "| ok |", 1)))
    assert any("Status column must hold only a light" in p for p in status.check_text(README + good.replace("| 🟢 | The test", "| 🟢 done | The test")))
    short = "## 💡 Project status\n\nlegend\n\n| Part | Status | Note |\n| --- | :---: | --- |\n| A | 🟡 | note |\n"
    assert any("at least" in p for p in status.check_text(README + short))
    empty_note = good.replace("| 🟢 | The test suite passes in the CI, on Linux and on Windows, on every push. |", "| 🟢 |  |")
    assert any("does not have a part" in p for p in status.check_text(README + empty_note))


def test_a_status_heading_inside_a_code_block_does_not_count():
    fenced = README + "\n```text\n" + status.render_own("en") + "```\n"
    assert status.check_text(fenced) == ["the 'Project status' section is missing"]


def test_the_status_table_can_be_the_last_section_and_crlf_is_fine():
    text = (README + "\n" + status.render_own("en")).replace("\n", "\r\n")
    assert status.check_text(text) == []


def test_check_repo_compares_the_lights_of_the_translations_with_the_english_one(tmp_path: Path):
    repo = write_repo(tmp_path, "URTC-X")
    for filename in glance.LANGUAGE_FILES.values():
        (repo / filename).write_text(README + "\n" + status.render_own("en"), encoding="utf-8", newline="\n")
    assert status.check_repo(repo) == []
    changed = (repo / "README_por.md").read_text(encoding="utf-8").replace("| 🟡 |", "| 🟠 |", 1)
    (repo / "README_por.md").write_text(changed, encoding="utf-8", newline="\n")
    assert status.check_repo(repo) == ["URTC-X/README_por.md: the lights of the 'Project status' table differ from README.md"]
    (repo / "README_jpn.md").write_text(README, encoding="utf-8", newline="\n")
    assert any("README_jpn.md: the 'Project status' section is missing" in p for p in status.check_repo(repo))


def test_the_glance_command_fails_for_a_repository_without_the_table(tmp_path: Path, capsys):
    repo = write_repo(tmp_path, "URTC-X")
    for filename in glance.LANGUAGE_FILES.values():
        (repo / filename).write_text(README, encoding="utf-8", newline="\n")
    data = tmp_path / "glance.json"
    data.write_text('{"repos": {"URTC-X": {"hardware": "not_run"}}}', encoding="utf-8")
    assert cli.make_glance(["--workspace", str(tmp_path), "--data", str(data), "--apply"]) == 1
    assert "'Project status' section is missing" in capsys.readouterr().err


def test_the_readmes_of_this_repository_have_the_table():
    assert status.check_repo(REPO) == []
