# =============================================================================
# URTC-DOCS - tests/test_drift.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared-file check: the copies may differ in the name of their repository and nothing else."""
from __future__ import annotations

from pathlib import Path

from conftest import write_repo
from urtc_docs import cli, drift


def put(repo: Path, relative: str, text: str) -> None:
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="")


def test_the_name_of_the_repository_and_the_line_endings_do_not_count():
    copies = {
        "URTC": "# URTC - tools/x.py\r\nprint(1)\r\n",
        "URTC-FLASHER": "# URTC-FLASHER - tools/x.py\nprint(1)\n",
        "URTC-WEB-STUDIO": "# URTC-WEB-STUDIO - tools/x.py\nprint(1)\n",
    }
    assert drift.compare(copies) == []


def test_the_repository_that_differs_from_the_others_is_named_with_its_first_changed_line():
    copies = {name: "# GPL-3.0-or-later\nprint(1)\n" for name in ("URTC-A", "URTC-B", "URTC-C")}
    copies["URTC-B"] = "# GPL-3.0\nprint(1)\n"
    found = drift.compare(copies)
    assert [item.repository for item in found] == ["URTC-B"]
    assert "GPL-3.0-or-later" in found[0].detail and "differs from URTC-A" in found[0].detail


def test_a_tie_goes_to_the_name_that_sorts_first():
    found = drift.compare({"URTC-A": "one\n", "URTC-B": "two\n"})
    assert [item.repository for item in found] == ["URTC-B"]


def test_one_copy_alone_has_nothing_to_differ_from():
    assert drift.compare({"URTC-A": "one\n"}) == []
    assert drift.compare({}) == []


def test_a_repository_without_the_file_is_left_out_of_the_comparison(tmp_path):
    for name in ("URTC-A", "URTC-B", "URTC-C"):
        write_repo(tmp_path, name)
    put(tmp_path / "URTC-A", "tools/_doc_policy.py", "same\n")
    put(tmp_path / "URTC-B", "tools/_doc_policy.py", "same\n")
    found, count = drift.check_workspace(tmp_path, ("tools/_doc_policy.py",))
    assert found == [] and count == 3


def test_the_command_fails_on_a_changed_copy_and_passes_on_equal_ones(tmp_path, capsys):
    for name in ("URTC-A", "URTC-B", "URTC-C"):
        write_repo(tmp_path, name)
        for relative in drift.SHARED_FILES:
            put(tmp_path / name, relative, f"# {name}\nsame\n")
    assert cli.check_repo_tools(["--workspace", str(tmp_path)]) == 0
    assert "REPO_TOOLS=PASS" in capsys.readouterr().out
    put(tmp_path / "URTC-C", "bump_manifest_version.py", "# URTC-C\nedited\n")
    assert cli.check_repo_tools(["--workspace", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "URTC-C/bump_manifest_version.py" in err and "REPO_TOOLS=FAIL 1" in err


def test_the_command_skips_or_fails_when_there_is_nothing_to_compare(tmp_path, capsys):
    write_repo(tmp_path, "URTC-A")
    assert cli.check_repo_tools(["--workspace", str(tmp_path)]) == 0
    assert "REPO_TOOLS=SKIP" in capsys.readouterr().out
    assert cli.check_repo_tools(["--workspace", str(tmp_path), "--require-siblings"]) == 1



def test_the_dashboard_notifier_is_one_of_the_shared_copies():
    assert ".github/workflows/dashboard-dispatch.yml" in drift.SHARED_FILES
