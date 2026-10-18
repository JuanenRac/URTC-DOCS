# =============================================================================
# URTC-DOCS - tests/test_glance.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The 'At a glance' table: rendering, inserting, rewriting in place, checking, line endings, the command."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import make_manifest, write_repo
from urtc_docs import cli, glance

README = (
    "<p align=\"center\">banner</p>\n\n# Title\n\n---\n\n**Honesty check:** text.\n\n---\n\n"
    "## Overview\n\nBody.\n\n```text\n## not a heading\n```\n\n## Other\n\nMore.\n"
)
ENTRY = {"hardware": "simulated", "tests": {"count": 12, "command": "pytest"}}


def section(code: str = "en", **entry) -> str:
    return glance.render_section(code, make_manifest("URTC-X"), {**ENTRY, **entry})


def test_every_language_has_every_label_and_sentence():
    assert set(glance.LABELS) == set(glance.MATURITY) == set(glance.TARGETS) == set(glance.HARDWARE) == set(glance.LANGUAGE_FILES)
    for code in glance.LANGUAGE_FILES:
        assert set(glance.LABELS[code]) == set(glance.LABELS["en"]), code
        assert set(glance.MATURITY[code]) == {"scaffolding", "functional", "established", "production"}, code
        assert set(glance.TARGETS[code]) == set(glance.TARGET_KEYS), code
        assert set(glance.HARDWARE[code]) == set(glance.HARDWARE_KEYS), code
        assert all(glance.HARDWARE[code].values()) and all(glance.TARGETS[code].values()), code


def test_the_table_has_the_rows_the_facts_allow():
    text = section()
    assert text.startswith("## 📋 At a glance\n\n| | |\n|---|---|\n| Version | `0.1.0` |\n| Maturity | Established |\n| Tests | 12 (`pytest`) |\n")
    assert "| Stack | Python |" in text and "| Target | The Raspberry Pi CM5 of a HYDRA-UMC cell |" in text
    assert "Tests" not in section(tests=None)
    library = glance.render_section("en", make_manifest("X", role="library"), {"hardware": "not_run"})
    assert "| Target |" not in library
    assert "| Target | A microcontroller" in glance.render_section("en", make_manifest("X"), {"hardware": "not_run", "target": "board"})
    assert "| Target |" not in glance.render_section("en", make_manifest("X"), {"hardware": "not_run", "target": None})


def test_the_stack_comes_from_the_manifest_and_a_pipe_cannot_break_the_table():
    manifest = make_manifest("X", technologies=["A", "B|C", "D", "E", "F", "G"])
    text = glance.render_section("en", manifest, {"hardware": "not_run"})
    assert "| Stack | A / B" + chr(92) + "|C / D / E / F |" in text


def test_insert_goes_before_the_first_heading_and_is_idempotent():
    once = glance.apply_to_text(README, section())
    assert once.index("## 📋") < once.index("## Overview") and "---\n\n## 📋" in once
    assert once.count("## 📋") == 1 and glance.apply_to_text(once, section()) == once
    assert "## not a heading" in once.split("## Other")[0]


def test_a_stale_section_is_rewritten_in_place_not_duplicated():
    once = glance.apply_to_text(README, section())
    newer = glance.render_section("en", make_manifest("X", version="0.2.0"), ENTRY)
    twice = glance.apply_to_text(once, newer)
    assert "`0.2.0`" in twice and "`0.1.0`" not in twice and twice.count("## 📋") == 1


def test_crlf_files_stay_crlf_and_lf_files_stay_lf():
    crlf = README.replace("\n", "\r\n")
    out = glance.apply_to_text(crlf, section())
    assert out.count("\r\n") == out.count("\n") and glance.apply_to_text(out, section()) == out
    assert "\r" not in glance.apply_to_text(README, section())


def test_check_reports_missing_misplaced_and_stale():
    assert glance.check_text(README, section()) == ["the section is missing"]
    ok = glance.apply_to_text(README, section())
    assert glance.check_text(ok, section()) == []
    stale = glance.check_text(ok, glance.render_section("en", make_manifest("X", version="9.9.9"), ENTRY))
    assert len(stale) == 1 and "stale" in stale[0]
    misplaced = README.replace("## Overview", "## Intro\n\ntext\n\n" + section().rstrip("\n") + "\n\n## Overview", 1)
    assert any("not the first" in problem for problem in glance.check_text(misplaced, section()))


def test_the_heading_is_found_in_every_language():
    for code in glance.LANGUAGE_FILES:
        text = glance.apply_to_text(README, section(code))
        assert glance.check_text(text, section(code)) == [], code
        assert glance.apply_to_text(text, section(code)) == text, code


def test_the_data_file_only_accepts_the_closed_vocabulary(tmp_path: Path):
    def load(entry: dict):
        path = tmp_path / "glance.json"
        path.write_text(json.dumps({"repos": {"R": entry}}), encoding="utf-8")
        return glance.load_data(path)

    assert load({"hardware": "not_run"})["R"]["hardware"] == "not_run"
    for bad in ({"hardware": "great"}, {"hardware": "bench", "target": "moon"}, {"hardware": "bench", "tests": {"count": 0}}):
        with pytest.raises(glance.GlanceError):
            load(bad)


def test_the_shipped_data_file_is_valid_and_lists_this_repository():
    entries = glance.load_data(cli.GLANCE_FILE)
    assert entries["URTC-DOCS"]["hardware"] == "not_applicable"
    assert all(name.startswith("URTC") for name in entries)


def test_the_command_applies_then_checks_a_workspace(tmp_path: Path, capsys):
    repo = write_repo(tmp_path, "URTC-X")
    for filename in glance.LANGUAGE_FILES.values():
        (repo / filename).write_text(README, encoding="utf-8", newline="\n")
    data = tmp_path / "glance.json"
    data.write_text(json.dumps({"repos": {"URTC-X": ENTRY, "URTC-GONE": ENTRY}}), encoding="utf-8")
    arguments = ["--workspace", str(tmp_path), "--data", str(data)]
    assert cli.make_glance([*arguments, "--check"]) == 1
    assert cli.make_glance([*arguments, "--apply"]) == 0
    assert cli.make_glance([*arguments, "--check"]) == 0
    assert "GLANCE=PASS 1 repositories checked, 1 not found" in capsys.readouterr().out
    assert cli.make_glance([*arguments, "--check", "--require-siblings"]) == 1
    (repo / "urtc.project.json").write_text(json.dumps(make_manifest("URTC-X", version="3.0.0")), encoding="utf-8")
    assert cli.make_glance([*arguments, "--check", "--repo", "URTC-X"]) == 1
    assert cli.make_glance([*arguments, "--apply", "--repo", "URTC-X"]) == 0
    assert "`3.0.0`" in (repo / "README_jpn.md").read_text(encoding="utf-8")
    assert cli.make_glance([*arguments, "--repo", "URTC-NOPE"]) == 1
