# =============================================================================
# URTC-DOCS - src/urtc_docs/simulation.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A virtual ecosystem, and the nights of the comparison run over it (evidence: simulator).

The nightly comparison compares every repository of the family with the others, so on its own it can only be exercised against the real ones, over real days. This module
builds a small family in a temporary folder instead (the manifests, the shared copies and their locks, the catalogue, the version files and changelogs, a validation script per
repository) and runs a night over it with the same code the real night runs: the catalogue check, the drift and lock checks of the shared tools, the version checks of the doctor,
each repository's own validation (through a double that answers PASS or FAIL as told) and the scan for anything private.

Events can then be played between nights (a release, a manifest that moved without its source, a repository that appears or goes, a hand edit of a shared copy, a new version of
the set, a failing validation, a leak) and the report of each night says whether the night fails or only advises, exactly as the real one would. Nothing leaves the folder; there is no
clock, no network and no randomness. Standard library only.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import catalog, devtools_lock, doctor, drift, family, publication

DEFAULT_NAMES = ("URTC", "URTC-COMMON", "URTC-DEVTOOLS", "URTC-GATEWAY", "URTC-TESTER")
HUB = "URTC-DOCS"
CATALOGUE = Path("docs") / "PROJECT_CATALOG.md"
VERSION_PATTERN = r'^version\s*=\s*"(\d+\.\d+\.\d+)"'
SET_VERSION = "0.0.6"


@dataclass
class NightReport:
    """What one night found. The night FAILS on `failures`; `advisories` are reported and never fail it (the versions of the catalogue move with every release)."""

    night: int
    failures: list[str] = field(default_factory=list)
    advisories: list[str] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return bool(self.failures)


class ValidationDouble:
    """Stands in for ``tools/ci_validate.py`` of every repository: PASS unless the repository was told to fail."""

    def __init__(self) -> None:
        self.failing: set[str] = set()
        self.calls: list[str] = []

    def __call__(self, command: list[str], cwd: str = "", **_options: object) -> "subprocess.CompletedProcess[str]":
        name = Path(cwd).name
        self.calls.append(name)
        if name in self.failing:
            return subprocess.CompletedProcess(command, 1, stdout=f"CI_VALIDATION=FAIL project={name}\n", stderr="")
        return subprocess.CompletedProcess(command, 0, stdout=f"CI_VALIDATION=PASS project={name}\n", stderr="")


class VirtualEcosystem:
    def __init__(self, root: Path, names: tuple[str, ...] = DEFAULT_NAMES) -> None:
        self.root = root
        self.names = tuple(dict.fromkeys((*names, HUB)))
        self.validation = ValidationDouble()
        self.nights = 0
        self.reports: list[NightReport] = []
        for name in self.names:
            self._create(name)
        self._set_version(SET_VERSION)
        self.take_the_set()

    # ---- building ---------------------------------------------------------------
    def repo(self, name: str) -> Path:
        return self.root / name

    def _manifest(self, name: str, version: str = "0.1.0", **overrides: object) -> dict:
        manifest: dict = {
            "schema_version": "1.0", "ecosystem": "URTC", "name": name, "version": version, "role": "tool", "stack": "python",
            "technologies": ["Python"], "deployment_target": "user-pc", "maturity": "functional", "family": "Ecosystem Operations", "parent": None,
            "build": "python tools/build_test.py", "notes": "A virtual repository.",
            "native_version": {"file": "pyproject.toml", "pattern": VERSION_PATTERN},
        }
        manifest.update(overrides)
        return manifest

    def _write_manifest(self, name: str, version: str, **overrides: object) -> None:
        path = self.repo(name) / family.MANIFEST_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._manifest(name, version or "0.1.0", **overrides), indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    def _create(self, name: str) -> None:
        repo = self.repo(name)
        self._write_manifest(name, "0.1.0")
        self._write_version_files(name, "0.1.0")
        (repo / "README.md").write_text(f"# {name}\n\nA virtual repository.\n", encoding="utf-8", newline="\n")
        (repo / "tools").mkdir(exist_ok=True)
        (repo / "tools" / "ci_validate.py").write_text("print('CI_VALIDATION=PASS')\n", encoding="utf-8", newline="\n")
        (repo / ".git").mkdir(exist_ok=True)
        for relative in drift.SHARED_FILES:
            canonical = drift.template_text(relative)
            if canonical is not None:
                target = repo / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(drift.render_for(name, canonical), encoding="utf-8", newline="\n")

    def _write_version_files(self, name: str, version: str) -> None:
        repo = self.repo(name)
        (repo / "pyproject.toml").write_text(f'[project]\nname = "{name.lower()}"\nversion = "{version}"\n', encoding="utf-8", newline="\n")
        (repo / "CHANGELOG.md").write_text(f"# Changelog\n\n## [Unreleased]\n\n## [{version}] - release\n\n- Something.\n", encoding="utf-8", newline="\n")

    def manifests(self) -> list[dict]:
        return family.load_manifests(self.root)

    def regenerate_catalogue(self) -> None:
        """What tools/make_catalog.py does: the table written from the manifests."""
        path = self.repo(HUB) / CATALOGUE
        path.parent.mkdir(parents=True, exist_ok=True)
        current = path.read_text(encoding="utf-8") if path.is_file() else f"# Catalogue\n\n{catalog.BEGIN}\n{catalog.END}\n"
        path.write_text(catalog.render(current, self.manifests()), encoding="utf-8", newline="\n")

    def take_the_set(self) -> None:
        """What sync_repo_tools.py --apply does: the shared copies from the template and the lock of every repository, with the real planner."""
        items = drift.plan_sync(self.root, template_dir=drift.TEMPLATE_DIR)
        items += drift.plan_locks(self.root, items)
        items += drift.plan_locks(self.root, items)
        drift.apply_sync(items)
        self._publish_canonical()

    def _publish_canonical(self) -> None:
        """URTC-DEVTOOLS holds the canonical files (``files/``) and says which repositories must carry a lock (its registry), as the real one does."""
        for relative in drift.SHARED_FILES:
            source = drift.TEMPLATE_DIR / relative
            if source.is_file():
                target = self.repo("URTC-DEVTOOLS") / "files" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
        registry = self.repo("URTC-DEVTOOLS") / "tools" / "tooling_registry.json"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(json.dumps({"schema": 1, "expected_repositories": sorted(self.names), "files": []}, indent=2) + "\n", encoding="utf-8", newline="\n")

    def _set_version(self, version: str) -> None:
        # the version of the set is the version of the manifest of URTC-DEVTOOLS
        self._write_manifest("URTC-DEVTOOLS", version)
        self._write_version_files("URTC-DEVTOOLS", version)
        self.regenerate_catalogue()

    def version_of(self, name: str) -> str:
        return str(json.loads((self.repo(name) / family.MANIFEST_FILE).read_text(encoding="utf-8"))["version"])

    # ---- events -----------------------------------------------------------------
    def release(self, name: str, version: str) -> None:
        """A proper release: the manifest, the source file and the changelog all say the new version."""
        self._write_manifest(name, version)
        self._write_version_files(name, version)

    def move_manifest_only(self, name: str, version: str) -> None:
        """The manifest moved and the source file did not (a bump that was half done)."""
        self._write_manifest(name, version)

    def add_repository(self, name: str, **overrides: object) -> None:
        self._create(name)
        if overrides:
            self._write_manifest(name, "0.1.0", **overrides)
        self.names = tuple(dict.fromkeys((*self.names, name)))

    def remove_repository(self, name: str) -> None:
        shutil.rmtree(self.repo(name))
        self.names = tuple(n for n in self.names if n != name)

    def change_role(self, name: str, role: str) -> None:
        self._write_manifest(name, self.version_of(name), role=role)

    def hand_edit_shared(self, name: str, relative: str = "tools/build_test.py") -> None:
        path = self.repo(name) / relative
        path.write_text(path.read_text(encoding="utf-8") + "# edited by hand\n", encoding="utf-8", newline="\n")

    def delete_lock(self, name: str) -> None:
        """The lock of a repository is deleted, so that the check has nothing to compare the copies with."""
        (self.repo(name) / devtools_lock.LOCK_FILE).unlink()

    def edit_and_relock(self, name: str, relative: str = "tools/build_test.py") -> None:
        """A copy is edited by hand and the lock is written again from the files as they are, so the lock agrees with the edit."""
        self.hand_edit_shared(name, relative)
        lock_path = self.repo(name) / devtools_lock.LOCK_FILE
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"] = devtools_lock.hashes_of(self.repo(name), drift.SHARED_FILES)
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    def publish_set(self, version: str) -> None:
        """URTC-DEVTOOLS releases a new version of the set; nobody has taken it yet."""
        self._set_version(version)

    def break_validation(self, name: str) -> None:
        self.validation.failing.add(name)

    def fix_validation(self, name: str) -> None:
        self.validation.failing.discard(name)

    def leak(self, name: str, text: str = "contact: someone.private@" + "gmail" + ".com") -> None:
        path = self.repo(name) / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + f"\n{text}\n", encoding="utf-8", newline="\n")

    def unleak(self, name: str) -> None:
        (self.repo(name) / "README.md").write_text(f"# {name}\n\nA virtual repository.\n", encoding="utf-8", newline="\n")

    # ---- the night ----------------------------------------------------------------
    def night(self) -> NightReport:
        self.nights += 1
        report = NightReport(self.nights)
        repos = family.discover(self.root)
        manifests = self.manifests()
        catalogue = self.repo(HUB) / CATALOGUE

        ok, message = catalog.check_file(catalogue, manifests, structure_only=True)
        if not ok:
            report.failures.append(f"catalogue structure: {message}")
        ok, message = catalog.check_file(catalogue, manifests)
        if not ok:
            report.advisories.append(f"catalogue versions: {message}")

        found, count = drift.check_workspace(self.root, template_dir=drift.TEMPLATE_DIR)
        report.failures += [f"shared copy {item.repository}/{item.file}: {item.detail}" for item in found]
        lock_problems, _locked = devtools_lock.check_workspace(self.root, repos, drift.SHARED_FILES)
        report.failures += [f"lock {repository}: {problem}" for repository, problem in lock_problems]
        if count < 2:
            report.failures.append("fewer than two repositories were found")

        for line in doctor.check_versions(repos) + doctor.check_repositories(repos, runner=self.validation):
            if line.status == doctor.FAIL:
                report.failures.append(f"{line.group} {line.name}: {line.detail}")

        findings: list[publication.Finding] = []
        for repo in repos:
            publication.scan_text(repo.name, "README.md", (repo / "README.md").read_text(encoding="utf-8"), findings, document=True)
        report.failures += [f"private content {kind} {name} {where}: {what}" for kind, name, where, what in findings if kind == "BLOCK"]
        report.advisories += [f"private content {kind} {name} {where}: {what}" for kind, name, where, what in findings if kind != "BLOCK"]

        self.reports.append(report)
        return report

    def play(self, schedule: list[Callable[["VirtualEcosystem"], None] | None]) -> list[NightReport]:
        """One night per entry: the event (if any) happens during the day, then the night runs."""
        result = []
        for event in schedule:
            if event is not None:
                event(self)
            result.append(self.night())
        return result

