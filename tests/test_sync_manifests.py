# =============================================================================
# URTC-DOCS - tests/test_sync_manifests.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load_tool():
    spec = importlib.util.spec_from_file_location("sync_manifests", REPO / "tools" / "sync_manifests.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_repo(root: Path, name: str, manifest: dict, files: dict[str, str]) -> Path:
    path = root / name
    path.mkdir()
    (path / "urtc.project.json").write_text(json.dumps({"name": name, "version": "1.2.3", "maturity": "functional", **manifest}), encoding="utf-8")
    for rel, text in files.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(text, encoding="utf-8")
    return path


NATIVE = {"native_version": {"file": "pyproject.toml", "pattern": r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"'}}


def codes(root: Path) -> set[str]:
    tool = load_tool()
    return {code for level, code, _ in tool.inspect(tool.Repo(root, "WORKTREE"), None)["findings"] if level == tool.HARD}


def test_agreeing_repository_has_no_contradiction(tmp_path):
    repo = make_repo(tmp_path, "URTC-X", {**NATIVE, "evidence": "host-test"},
                     {"pyproject.toml": 'version = "1.2.3"\n', "CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n\n## [1.2.3]\n- a\n", "tests/test_a.py": "def test_a(): pass\n"})
    assert codes(repo) == set()


def test_native_version_and_changelog_head_must_follow_the_manifest(tmp_path):
    repo = make_repo(tmp_path, "URTC-X", NATIVE, {"pyproject.toml": 'version = "1.2.4"\n', "CHANGELOG.md": "# Changelog\n\n## [1.2.4]\n- a\n"})
    assert codes(repo) == {"NATIVE_VERSION", "CHANGELOG_HEAD"}


def test_four_components_equal_three_when_the_last_is_zero(tmp_path):
    tool = load_tool()
    assert tool.same("0.4.5.0", "0.4.5")
    assert not tool.same("0.4.5.1", "0.4.5")
    assert tool.same("0.3.5.2", "0.3.5", three=True)


def test_simulator_evidence_needs_a_simulation_in_ci_and_tests(tmp_path):
    bare = make_repo(tmp_path, "URTC-A", {**NATIVE, "evidence": "simulator"}, {"pyproject.toml": 'version = "1.2.3"\n', ".github/workflows/ci.yml": "jobs:\n  t:\n    steps:\n      - run: pytest\n"})
    assert codes(bare) == {"SIMULATOR_NO_CI_JOB", "EVIDENCE_NO_TESTS"}
    sim = make_repo(tmp_path, "URTC-B", {**NATIVE, "evidence": "simulator"},
                    {"pyproject.toml": 'version = "1.2.3"\n', ".github/workflows/ci.yml": "jobs:\n  t:\n    steps:\n      - name: Run against the simulated bench\n        run: pytest\n", "tests/test_a.py": "def test_a(): pass\n"})
    assert codes(sim) == set()


def test_a_human_judgement_is_never_written(tmp_path):
    tool = load_tool()
    repo = make_repo(tmp_path, "URTC-X", {**NATIVE, "evidence": "field", "maturity": "established"}, {"pyproject.toml": 'version = "1.3.0"\n'})
    result = tool.inspect(tool.Repo(repo, "WORKTREE"), None)
    tool.MANIFEST = "urtc.project.json"
    written = tool.apply_changes([result], tmp_path)
    manifest = json.loads((repo / "urtc.project.json").read_text(encoding="utf-8"))
    assert written and manifest["version"] == "1.3.0"
    assert manifest["evidence"] == "field" and manifest["maturity"] == "established"
    assert "HUMAN_RECORD_MISSING" in {code for _, code, _ in result["findings"]}   # a person has to keep the record of a bench or field test


def test_apply_never_lowers_a_version(tmp_path):
    tool = load_tool()
    repo = make_repo(tmp_path, "URTC-X", NATIVE, {"pyproject.toml": 'version = "1.0.0"\n'})
    result = tool.inspect(tool.Repo(repo, "WORKTREE"), None)
    assert tool.apply_changes([result], tmp_path) == []
    assert json.loads((repo / "urtc.project.json").read_text(encoding="utf-8"))["version"] == "1.2.3"


def test_waivers_hide_only_the_listed_codes(tmp_path):
    tool = load_tool()
    repo = make_repo(tmp_path, "URTC-X", {**NATIVE, "evidence": "host-test"}, {"pyproject.toml": 'version = "1.2.3"\n'})
    assert tool.run_in_ci(repo) and "EVIDENCE_NO_TESTS" in tool.run_in_ci(repo)[0]
    (repo / "data").mkdir()
    (repo / "data" / "manifest_waivers.json").write_text(json.dumps({"URTC-X": ["EVIDENCE_NO_TESTS"]}), encoding="utf-8")
    assert tool.run_in_ci(repo) == []


def test_release_cache_and_call_budget(tmp_path, monkeypatch):
    tool = load_tool()
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="v1.0.0\n", stderr="")

    monkeypatch.setattr(tool.subprocess, "run", fake_run)
    gh = tool.Gh("Owner", 2, tmp_path / "cache.json", 3600)
    assert gh.release("A") == "v1.0.0" and gh.release("A") == "v1.0.0"       # second answer comes from the cache
    assert gh.ci("A") == "v1.0.0"
    assert gh.release("B") == "budget" and len(calls) == 2                    # the budget stops the calls
