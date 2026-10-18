# =============================================================================
# URTC-DOCS - tests/test_doctor.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The doctor report: every group of checks against throw-away repositories, with the other programs and the network replaced by stand-ins."""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import namedtuple
from pathlib import Path

from conftest import write_repo

from urtc_docs import doctor
from urtc_docs.doctor import FAIL, PASS, SKIP, WARN, Line


def status(lines, name):
    return next(line.status for line in lines if line.name == name)


def detail(lines, name):
    return next(line.detail for line in lines if line.name == name)


# --- the machine ---------------------------------------------------------------------------------------------------------
def test_a_missing_tool_is_a_warning_and_an_old_python_is_a_failure():
    lines = doctor.check_machine(which=lambda name: None, has_module=lambda name: False, python_version=(3, 12, 1))
    assert status(lines, "python") == PASS
    assert {line.status for line in lines if line.name != "python"} == {WARN}
    old = doctor.check_machine(which=lambda name: "x", has_module=lambda name: True, python_version=(3, 8, 0))
    assert status(old, "python") == FAIL


def test_the_serial_ports_are_only_listed():
    Port = namedtuple("Port", "device description")
    assert status(doctor.check_adapters(list_ports=lambda: []), "serial ports") == WARN
    lines = doctor.check_adapters(list_ports=lambda: [Port("COM3", "USB Serial"), Port("COM4", "n/a")])
    assert status(lines, "serial ports") == PASS
    assert "COM3 (USB Serial)" in detail(lines, "serial ports") and "COM4" in detail(lines, "serial ports") and "n/a" not in detail(lines, "serial ports")


# --- versions ------------------------------------------------------------------------------------------------------------
def make_versioned(workspace: Path, name: str, manifest_version: str, source_version: str, changelog_version: str | None = None, **overrides) -> Path:
    repo = write_repo(workspace, name, version=manifest_version, native_version={"file": "pyproject.toml", "pattern": r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?"'}, **overrides)
    (repo / "pyproject.toml").write_text(f'[project]\nversion = "{source_version}"\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(f"# Changelog\n\n## [{changelog_version or manifest_version}] - something\n\n- a change\n", encoding="utf-8")
    return repo


def test_the_three_places_of_a_version_must_agree(tmp_path):
    good = make_versioned(tmp_path, "URTC-GOOD", "0.2.3", "0.2.3")
    source = make_versioned(tmp_path, "URTC-SOURCE", "0.2.3", "0.2.4")
    log = make_versioned(tmp_path, "URTC-LOG", "0.2.3", "0.2.3", changelog_version="0.2.4")
    lines = doctor.check_versions([good, source, log])
    assert status(lines, "URTC-GOOD") == PASS
    assert status(lines, "URTC-SOURCE") == FAIL and "source file says 0.2.4" in detail(lines, "URTC-SOURCE")
    assert status(lines, "URTC-LOG") == FAIL and "CHANGELOG entry is 0.2.4" in detail(lines, "URTC-LOG")


def test_a_four_part_version_is_read_whole(tmp_path):
    repo = make_versioned(tmp_path, "URTC-FOUR", "0.8.0.1", "0.8.0.1")
    assert status(doctor.check_versions([repo]), "URTC-FOUR") == PASS


def test_a_placeholder_build_field_below_the_four_part_versions_is_not_part_of_the_version(tmp_path):
    repo = write_repo(tmp_path, "URTC-FW", version="0.3.5", native_version={"file": "version.properties", "pattern": {"major": r"MAJOR=(\d+)", "minor": r"MINOR=(\d+)", "patch": r"PATCH=(\d+)", "build": r"BUILD=(\d+)"}})
    (repo / "version.properties").write_text("MAJOR=0\nMINOR=3\nPATCH=5\nBUILD=0\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text("## [0.3.5] - x\n", encoding="utf-8")
    assert status(doctor.check_versions([repo]), "URTC-FW") == PASS
    assert doctor.native_version(repo, json.loads((repo / "urtc.project.json").read_text(encoding="utf-8"))) == "0.3.5"


def test_a_version_that_cannot_be_read_is_skipped_not_passed(tmp_path):
    repo = write_repo(tmp_path, "URTC-ODD", version="1.0.0", native_version={"file": "missing.toml", "pattern": "x"})
    assert status(doctor.check_versions([repo]), "URTC-ODD") == SKIP


# --- the copies of URTC-COMMON -------------------------------------------------------------------------------------------
def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_copy(workspace: Path, host: str, content: str, locked: str, common_content: str | None = "v1\n") -> Path:
    repo = write_repo(workspace, host)
    folder = repo / "urtc_can"
    folder.mkdir()
    (folder / "protocol.py").write_text(content, encoding="utf-8", newline="")
    (folder / "urtc_common.lock.json").write_text(json.dumps({"format": 1, "urtc_common_version": "0.0.1", "files": {"protocol.py": {"from": "src/urtc_common/protocol.py", "sha256": sha(locked)}}}), encoding="utf-8")
    if common_content is not None:
        common = write_repo(workspace, "URTC-COMMON")
        (common / "src" / "urtc_common").mkdir(parents=True, exist_ok=True)
        (common / "src" / "urtc_common" / "protocol.py").write_text(common_content, encoding="utf-8")
    return repo


def test_a_copy_is_as_locked_and_current(tmp_path):
    host = make_copy(tmp_path, "URTC-HOST", "v1\n", "v1\n")
    lines = doctor.check_shared_copies(tmp_path, [host])
    assert status(lines, "URTC-HOST/urtc_can") == PASS


def test_a_line_ending_does_not_make_a_copy_differ(tmp_path):
    host = make_copy(tmp_path, "URTC-HOST", "v1\r\n", "v1\n")
    assert status(doctor.check_shared_copies(tmp_path, [host]), "URTC-HOST/urtc_can") == PASS


def test_a_copy_edited_by_hand_and_a_copy_that_fell_behind_both_fail(tmp_path):
    edited = make_copy(tmp_path, "URTC-EDITED", "changed\n", "v1\n")
    assert status(doctor.check_shared_copies(tmp_path, [edited]), "URTC-EDITED/urtc_can") == FAIL
    assert "edited by hand" in detail(doctor.check_shared_copies(tmp_path, [edited]), "URTC-EDITED/urtc_can")
    behind = make_copy(tmp_path, "URTC-BEHIND", "v1\n", "v1\n", common_content="v2\n")
    lines = doctor.check_shared_copies(tmp_path, [behind])
    assert status(lines, "URTC-BEHIND/urtc_can") == FAIL and "behind URTC-COMMON" in detail(lines, "URTC-BEHIND/urtc_can")


def test_without_urtc_common_only_the_lock_is_compared_and_it_says_so(tmp_path):
    host = make_copy(tmp_path, "URTC-HOST", "v1\n", "v1\n", common_content=None)
    lines = doctor.check_shared_copies(tmp_path, [host])
    assert status(lines, "URTC-HOST/urtc_can") == PASS and "only the lock was compared" in detail(lines, "URTC-HOST/urtc_can")


def test_no_copy_at_all_is_a_skip(tmp_path):
    assert doctor.check_shared_copies(tmp_path, [write_repo(tmp_path, "URTC-NONE")])[0].status == SKIP


# --- bundled firmware ----------------------------------------------------------------------------------------------------
def fake_run(code: int, out: str = ""):
    def run(command, **kwargs):
        return subprocess.CompletedProcess(command, code, stdout=out, stderr="")
    return run


def bundle(workspace: Path, flasher: dict[str, bytes], web: dict[str, bytes]) -> None:
    for repo, folder, images in (("URTC-FLASHER", "firmware", flasher), ("URTC-WEB-STUDIO", "public/firmware", web)):
        target = workspace / repo / folder
        target.mkdir(parents=True, exist_ok=True)
        for name, data in images.items():
            (target / name).write_bytes(data)
    tools = workspace / "URTC-FLASHER" / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    (tools / "sync_firmware.py").write_text("", encoding="utf-8")


def test_both_tools_carrying_the_same_images_pass_and_a_different_one_fails(tmp_path):
    bundle(tmp_path, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"a"}, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"a"})
    lines = doctor.check_firmware(tmp_path, runner=fake_run(0, "firmware/ consistent"))
    assert status(lines, "URTC-FLASHER firmware/") == PASS
    assert status(lines, "FLASHER and WEB-STUDIO carry the same images") == PASS
    bundle(tmp_path, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"a"}, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"different"})
    lines = doctor.check_firmware(tmp_path, runner=fake_run(1, "firmware/ drifted"))
    assert status(lines, "URTC-FLASHER firmware/") == FAIL
    assert status(lines, "FLASHER and WEB-STUDIO carry the same images") == FAIL
    assert "URTC_MAIN_FIRMWARE_v0.3.3.bin" in detail(lines, "FLASHER and WEB-STUDIO carry the same images")


def test_without_the_tools_the_firmware_checks_are_skipped(tmp_path):
    lines = doctor.check_firmware(tmp_path, runner=fake_run(0))
    assert {line.status for line in lines} == {SKIP}


# --- the newest release --------------------------------------------------------------------------------------------------
def releases(*tags: str, draft: bool = False) -> bytes:
    return json.dumps([{"tag_name": tag, "draft": draft} for tag in tags]).encode()


def test_a_newer_release_than_the_bundled_firmware_is_a_warning(tmp_path):
    bundle(tmp_path, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"a"}, {})
    assert status(doctor.check_release(tmp_path, fetch=lambda url: releases("v0.3.5", "v0.3.4", "v0.3.10")), "newest firmware release") == WARN
    assert status(doctor.check_release(tmp_path, fetch=lambda url: releases("v0.3.3", "v0.3.2")), "newest firmware release") == PASS
    assert status(doctor.check_release(tmp_path, fetch=lambda url: releases("v0.4.0", draft=True)), "newest firmware release") == SKIP


def test_the_version_numbers_are_compared_as_numbers(tmp_path):
    assert doctor.newest_release_version(lambda url: releases("v0.3.9", "v0.3.10", "v0.3.2")) == "0.3.10"


def test_no_network_is_a_skip_not_a_failure(tmp_path):
    bundle(tmp_path, {"URTC_MAIN_FIRMWARE_v0.3.3.bin": b"a"}, {})

    def offline(url: str) -> bytes:
        raise OSError("no route")

    lines = doctor.check_release(tmp_path, fetch=offline)
    assert lines[0].status == SKIP and "no route" in lines[0].detail


# --- the whole report ----------------------------------------------------------------------------------------------------
def test_a_report_fails_on_a_failure_and_when_nothing_could_be_checked():
    text, code = doctor.render([Line("g", "a", PASS), Line("g", "b", WARN), Line("g", "c", SKIP, "why")])
    assert code == 0 and "URTC_DOCTOR=PASS" in text and "passed 1, failed 0, warnings 1, skipped 1" in text
    text, code = doctor.render([Line("g", "a", PASS), Line("g", "b", FAIL)])
    assert code == 1 and "URTC_DOCTOR=FAIL" in text
    text, code = doctor.render([Line("g", "a", SKIP)])
    assert code == 1 and "nothing could be checked" in text


def test_the_fast_report_starts_no_other_program(workspace, tmp_path):
    started = []

    def runner(command, **kwargs):
        started.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    repo = write_repo(workspace, "URTC-DOCS")
    lines = doctor.run_doctor(repo, workspace, fast=True, runner=runner)
    assert not any("ci_validate" in " ".join(map(str, command)) for command in started)
    assert any(line.group == "versions" for line in lines)


def test_the_full_report_runs_the_validation_of_every_sibling_and_the_document_checks(workspace):
    started = []
    for sibling in ("URTC", "URTC-FLASHER", "URTC-TESTER"):
        (workspace / sibling / "tools").mkdir(exist_ok=True)
        (workspace / sibling / "tools" / "ci_validate.py").write_text("", encoding="utf-8")
        (workspace / sibling / ".git").mkdir(exist_ok=True)

    def runner(command, **kwargs):
        started.append((command, kwargs.get("cwd")))
        return subprocess.CompletedProcess(command, 0, stdout="CI_VALIDATION=PASS project=x\n", stderr="")

    repo = write_repo(workspace, "URTC-DOCS")
    lines = doctor.run_doctor(repo, workspace, runner=runner)
    validated = {Path(cwd).name for command, cwd in started if "tools/ci_validate.py" in command}
    assert {"URTC", "URTC-FLASHER", "URTC-TESTER", "URTC-DOCS"} <= validated
    assert any(line.group == "docs" and line.name == "docs: claim hygiene" for line in lines)
    assert next(line for line in lines if line.group == "repositories" and line.name == "URTC").detail == "CI_VALIDATION=PASS project=x"
