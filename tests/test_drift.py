# =============================================================================
# URTC-DOCS - tests/test_drift.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared-file check: the copies may differ in the name of their repository and nothing else."""
from __future__ import annotations

import json
from pathlib import Path

from conftest import write_repo
from urtc_docs import cli, devtools_lock, drift


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


def _workspace(tmp_path: Path, copies: dict[str, str], relative: str = "tools/_x.py") -> Path:
    for name, text in copies.items():
        write_repo(tmp_path, name)
        put(tmp_path / name, relative, text)
    return tmp_path


def test_the_template_is_the_reference_when_it_is_given():
    copies = {name: "# GPL\nprint(1)\n" for name in ("URTC-A", "URTC-B", "URTC-C")}
    assert drift.compare(copies, "# GPL\nprint(1)\n") == []
    found = drift.compare(copies, "# GPL\nprint(2)\n")
    assert [item.repository for item in found] == ["URTC-A", "URTC-B", "URTC-C"]
    assert "differs from the template" in found[0].detail


def test_the_template_text_gets_the_name_of_each_repository_and_the_line_endings_of_the_copy():
    assert drift.render_for("URTC-A", "# <REPO> - x\nok\n", "\r\n") == "# URTC-A - x\r\nok\r\n"
    assert drift.make_canonical("# URTC-FLASHER - x\r\nok\r\n") == "# <REPO> - x\nok\n"


def test_a_sync_plan_lists_only_the_copies_that_differ_and_keeps_their_line_endings(tmp_path):
    template = tmp_path / "tpl"
    put(template, "tools/_x.py", "# <REPO>\nprint(1)\n")
    ws = tmp_path / "ws"
    ws.mkdir()
    _workspace(ws, {"URTC-A": "# URTC-A\nprint(1)\n", "URTC-B": "# URTC-B\r\nprint(0)\r\n"})
    items = drift.plan_sync(ws, ("tools/_x.py",), template)
    assert [item.repository for item in items] == ["URTC-B"]
    assert items[0].new_text == "# URTC-B\r\nprint(1)\r\n"
    drift.apply_sync(items)
    assert (ws / "URTC-B" / "tools" / "_x.py").read_bytes() == b"# URTC-B\r\nprint(1)\r\n"
    assert drift.plan_sync(ws, ("tools/_x.py",), template) == []


def test_the_real_template_covers_every_shared_file():
    for relative in drift.SHARED_FILES:
        assert drift.template_text(relative) is not None, relative
    assert (drift.TEMPLATE_DIR / "TEMPLATE.md").is_file()


# ---------------------------------------------------------------------------------------------------------------
# The lock: the version of the set of shared tools and the hash of each file a repository carries.
# ---------------------------------------------------------------------------------------------------------------
def _locked_workspace(tmp_path: Path, version: str = "0.0.1") -> tuple[Path, Path]:
    template = tmp_path / "tpl"
    put(template, "tools/_x.py", "# <REPO>\nprint(1)\n")
    ws = tmp_path / "ws"
    ws.mkdir()
    write_repo(ws, "URTC-DEVTOOLS", version=version)
    _workspace(ws, {"URTC-A": "# URTC-A\nprint(0)\n", "URTC-B": "# URTC-B\r\nprint(1)\r\n"})
    return ws, template


def _take_the_set(ws: Path, template: Path) -> None:
    items = drift.plan_sync(ws, ("tools/_x.py",), template)
    drift.apply_sync(items + drift.plan_locks(ws, items, ("tools/_x.py",)))


def test_the_sync_writes_a_lock_with_the_version_of_the_set_and_the_hash_of_what_the_file_becomes(tmp_path):
    ws, template = _locked_workspace(tmp_path)
    items = drift.plan_sync(ws, ("tools/_x.py",), template)
    locks = drift.plan_locks(ws, items, ("tools/_x.py",))
    assert sorted(item.repository for item in locks) == ["URTC-A", "URTC-B"]
    drift.apply_sync(items + locks)
    lock = json.loads((ws / "URTC-A" / "tools" / "devtools.lock.json").read_text(encoding="utf-8"))
    assert lock["version"] == "0.0.1" and lock["source"] == "URTC-DEVTOOLS"
    assert lock["files"] == {"tools/_x.py": devtools_lock.digest("# URTC-A\nprint(1)\n")}
    # the CRLF copy is hashed as the same text with newlines
    assert json.loads((ws / "URTC-B" / "tools" / "devtools.lock.json").read_text(encoding="utf-8"))["files"] == {"tools/_x.py": devtools_lock.digest("# URTC-B\nprint(1)\n")}
    assert drift.plan_locks(ws, drift.plan_sync(ws, ("tools/_x.py",), template), ("tools/_x.py",)) == []


def test_no_lock_is_planned_when_the_tools_repository_is_not_there_to_name_the_version(tmp_path):
    ws = tmp_path / "ws"
    ws.mkdir()
    _workspace(ws, {"URTC-A": "# URTC-A\nprint(0)\n"})
    assert drift.plan_locks(ws, [], ("tools/_x.py",)) == []


def test_the_check_finds_an_edited_copy_a_missing_file_and_a_copy_that_fell_behind(tmp_path):
    ws, template = _locked_workspace(tmp_path)
    _take_the_set(ws, template)
    repos = [ws / "URTC-A", ws / "URTC-B"]
    assert devtools_lock.check_workspace(ws, repos, ("tools/_x.py",)) == ([], 2)
    put(ws / "URTC-A", "tools/_x.py", "# URTC-A\nedited\n")
    (ws / "URTC-B" / "tools" / "_x.py").unlink()
    problems, locked = devtools_lock.check_workspace(ws, repos, ("tools/_x.py",))
    assert locked == 2
    assert ("URTC-A", "tools/_x.py: edited after the set was taken (it differs from the lock)") in problems
    assert ("URTC-B", "tools/_x.py: in the lock but missing") in problems
    (ws / "URTC-DEVTOOLS" / "urtc.project.json").write_text(json.dumps({"version": "0.0.2"}), encoding="utf-8")
    behind, _ = devtools_lock.check_workspace(ws, repos, ("tools/_x.py",))
    assert any("URTC-DEVTOOLS is at '0.0.2'" in problem for _repo, problem in behind)


def test_a_repository_without_a_lock_is_not_a_failure_yet_and_an_unreadable_lock_is(tmp_path):
    ws, _template = _locked_workspace(tmp_path)
    repos = [ws / "URTC-A", ws / "URTC-B"]
    assert devtools_lock.check_workspace(ws, repos, ("tools/_x.py",)) == ([], 0)
    put(ws / "URTC-A", "tools/devtools.lock.json", "not json")
    problems, locked = devtools_lock.check_workspace(ws, repos, ("tools/_x.py",))
    assert locked == 1 and problems and "cannot be read" in problems[0][1]


def test_the_check_command_reports_the_lock_problems(tmp_path, capsys):
    ws, template = _locked_workspace(tmp_path)
    _take_the_set(ws, template)
    put(ws / "URTC-A", "tools/devtools.lock.json", "{}")
    assert cli.check_repo_tools(["--workspace", str(ws)]) == 1
    assert "devtools.lock.json" in capsys.readouterr().err


def test_the_source_of_the_shared_files_is_urtc_devtools_when_it_is_next_to_the_repositories(tmp_path):
    assert drift.source_dir(tmp_path) == drift.TEMPLATE_DIR
    (tmp_path / "URTC-DEVTOOLS" / "files").mkdir(parents=True)
    assert drift.source_dir(tmp_path) == tmp_path / "URTC-DEVTOOLS" / "files"
