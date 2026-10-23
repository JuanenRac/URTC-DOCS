# =============================================================================
# URTC-DOCS - src/urtc_docs/doctor.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""One report on the local checkout of the ecosystem: the tools of the machine, the repositories next to this one, the copies they keep of
URTC-COMMON, the firmware they bundle, and (when asked) the newest firmware release.

Every line is PASS, FAIL, WARN (worth knowing, never a failure) or SKIP (could not be checked here, with the reason). A check that cannot
run is never printed as PASS. The exit status is non-zero when a line FAILS, and also when nothing at all could be checked.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import family

PASS, FAIL, WARN, SKIP = "PASS", "FAIL", "WARN", "SKIP"
FIRMWARE_RELEASES_URL = "https://api.github.com/repos/JuanenRac/URTC/releases?per_page=10"
#: from this version on the version has a fourth component
FOUR_PART_FROM = (0, 8, 0)
FIRMWARE_NAME = re.compile(r"^URTC_MAIN_FIRMWARE_v(\d+(?:\.\d+)+)\.bin$")

Runner = Callable[..., subprocess.CompletedProcess]


@dataclass(frozen=True)
class Line:
    group: str
    name: str
    status: str
    detail: str = ""


# ---------------------------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------------------------
def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _version_key(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", text))


def native_version(repo: Path, manifest: dict) -> str | None:
    """The version the repository keeps in its own source file, read the way the manifest says; None when it cannot be read."""
    spec = manifest.get("native_version")
    if not isinstance(spec, dict) or "file" not in spec or "pattern" not in spec:
        return None
    try:
        text = (repo / spec["file"]).read_text(encoding="utf-8", errors="replace")
        pattern = spec["pattern"]
        if isinstance(pattern, dict):
            parts: list[str] = []
            for key in ("major", "minor", "patch", "build"):
                if key not in pattern:
                    continue
                # a separate field for the fourth component only counts from the version that carries one; below it a stored 0 is a placeholder
                if key == "build" and tuple(int(part) for part in parts) < FOUR_PART_FROM:
                    continue
                match = re.search(pattern[key], text, re.MULTILINE)
                if match is None:
                    return None if key != "build" else ".".join(parts)
                parts.append(match.group(1))
            return ".".join(parts)
        match = re.search(pattern, text, re.MULTILINE)
        if match is None:
            return None
        return ".".join(group for group in match.groups() if group is not None)
    except (OSError, re.error):
        return None


def changelog_version(repo: Path) -> str | None:
    """The version of the newest entry of CHANGELOG.md."""
    try:
        text = (repo / "CHANGELOG.md").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = re.search(r"(?m)^##+\s+\[?v?(\d+(?:\.\d+){2,3})\]?", text)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------------------------------------------------
# the groups of checks
# ---------------------------------------------------------------------------------------------------------------------
def check_machine(*, which=shutil.which, has_module=lambda name: importlib.util.find_spec(name) is not None, python_version=sys.version_info) -> list[Line]:
    """The tools of this machine. A missing one is a WARN: the repositories decide what they need."""
    lines = [Line("machine", "python", PASS if python_version >= (3, 10) else FAIL, f"{python_version[0]}.{python_version[1]}.{python_version[2]}" + ("" if python_version >= (3, 10) else " (3.10 or newer is needed)"))]
    for name, hint in (("git", "installs and updates repositories"), ("node", "builds and tests URTC-WEB-STUDIO"), ("arm-none-eabi-gcc", "builds the firmware (not needed to use the tools)")):
        found = which(name)
        lines.append(Line("machine", name, PASS if found else WARN, found or f"not found: {hint}"))
    for module, hint in (("pytest", "runs the Python tests"), ("PySide6", "the Qt Quick windows"), ("serial", "SLCAN adapters (pyserial)")):
        lines.append(Line("machine", module, PASS if has_module(module) else WARN, "installed" if has_module(module) else f"not installed: {hint}"))
    return lines


def check_adapters(*, list_ports=None) -> list[Line]:
    """The serial ports that could be an SLCAN adapter. Only listed, never opened."""
    if list_ports is None:
        if importlib.util.find_spec("serial") is None:
            return [Line("machine", "serial ports", SKIP, "pyserial is not installed")]
        from serial.tools import list_ports as ports  # type: ignore[import-not-found]

        list_ports = ports.comports
    found = list(list_ports())
    if not found:
        return [Line("machine", "serial ports", WARN, "none found: no USB-CAN adapter is connected")]
    return [Line("machine", "serial ports", PASS, ", ".join(f"{getattr(port, 'device', port)}" + (f" ({port.description})" if getattr(port, "description", "") not in ("", "n/a") else "") for port in found))]


def check_versions(repos: list[Path]) -> list[Line]:
    """The manifest, the version in the source file and the newest CHANGELOG entry must name the same version."""
    lines = []
    for repo in repos:
        try:
            manifest = family.read_manifest(repo)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            lines.append(Line("versions", repo.name, FAIL, f"manifest unreadable: {exc}"))
            continue
        declared = str(manifest["version"])
        native = native_version(repo, manifest)
        logged = changelog_version(repo)
        problems = []
        if native is None:
            lines.append(Line("versions", repo.name, SKIP, f"{declared}: the version in the source file could not be read"))
            continue
        if native != declared:
            problems.append(f"source file says {native}")
        if logged is not None and logged != declared:
            problems.append(f"newest CHANGELOG entry is {logged}")
        lines.append(Line("versions", repo.name, FAIL if problems else PASS, f"manifest {declared}" + (": " + "; ".join(problems) if problems else "")))
    return lines


def check_repositories(repos: list[Path], *, python: str = sys.executable, runner: Runner = subprocess.run) -> list[Line]:
    """Each repository's own CI validation (tools/ci_validate.py)."""
    lines = []
    for repo in repos:
        script = repo / "tools" / "ci_validate.py"
        if repo.name == family.OWN_NAME:
            continue  # the checks of this repository run in their own group
        if not script.is_file():
            lines.append(Line("repositories", repo.name, SKIP, "no tools/ci_validate.py"))
            continue
        if not (repo / ".git").exists():
            lines.append(Line("repositories", repo.name, SKIP, "not a git checkout (the documentation boundary check reads git)"))
            continue
        done = runner([python, "tools/ci_validate.py"], cwd=str(repo), capture_output=True, text=True)
        token = next((line.strip() for line in reversed((done.stdout or "").splitlines()) if "CI_VALIDATION=" in line), "")
        lines.append(Line("repositories", repo.name, PASS if done.returncode == 0 else FAIL, token or f"exit code {done.returncode}"))
    return lines


def check_shared_copies(workspace: Path, repos: list[Path]) -> list[Line]:
    """Every copy of URTC-COMMON (a folder with a urtc_common.lock.json) is as locked, and has not fallen behind URTC-COMMON when that is next to us."""
    common = workspace / "URTC-COMMON"
    lines = []
    for repo in repos:
        if repo.name == "URTC-COMMON":
            continue
        for lock_path in sorted(repo.rglob("urtc_common.lock.json")):
            if any(part in {"node_modules", ".git", "dist", "build", "__pycache__"} for part in lock_path.parts):
                continue
            label = f"{repo.name}/{lock_path.parent.relative_to(repo).as_posix()}"
            try:
                lock = json.loads(lock_path.read_text(encoding="utf-8"))
                entries = lock["files"]
            except (OSError, ValueError, KeyError):
                lines.append(Line("shared copies", label, FAIL, "the lock file cannot be read"))
                continue
            problems = []
            for name, entry in entries.items():
                target = lock_path.parent / name
                if not target.is_file():
                    problems.append(f"{name} is missing")
                elif _digest(target) != entry.get("sha256"):
                    problems.append(f"{name} differs from its lock (edited by hand?)")
                elif common.is_dir():
                    origin = common / entry.get("from", "")
                    if not origin.is_file():
                        problems.append(f"{name}: {entry.get('from')} no longer exists in URTC-COMMON")
                    elif _digest(origin) != entry.get("sha256"):
                        problems.append(f"{name} is behind URTC-COMMON")
            where = "" if common.is_dir() else " (URTC-COMMON is not next to this repository: only the lock was compared)"
            lines.append(Line("shared copies", label, FAIL if problems else PASS, ("; ".join(problems) if problems else f"{len(entries)} file(s) as locked") + where))
    if not lines:
        lines.append(Line("shared copies", "all", SKIP, "no urtc_common.lock.json found"))
    return lines


def _bundled_images(folder: Path) -> dict[str, str]:
    return {item.name: _digest_binary(item) for item in sorted(folder.glob("URTC_*.bin"))} if folder.is_dir() else {}


def _digest_binary(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_firmware(workspace: Path, *, python: str = sys.executable, runner: Runner = subprocess.run) -> list[Line]:
    """The firmware that URTC-FLASHER and URTC-WEB-STUDIO carry: consistent with its manifests, and the same set in both."""
    flasher, web = workspace / "URTC-FLASHER", workspace / "URTC-WEB-STUDIO"
    lines = []
    if (flasher / "tools" / "sync_firmware.py").is_file():
        done = runner([python, "tools/sync_firmware.py", "--check"], cwd=str(flasher), capture_output=True, text=True)
        text = ((done.stdout or "") + (done.stderr or "")).strip().splitlines()
        lines.append(Line("firmware", "URTC-FLASHER firmware/", PASS if done.returncode == 0 else FAIL, text[-1] if text else f"exit code {done.returncode}"))
    else:
        lines.append(Line("firmware", "URTC-FLASHER firmware/", SKIP, "URTC-FLASHER is not next to this repository"))
    here, there = _bundled_images(flasher / "firmware"), _bundled_images(web / "public" / "firmware")
    if not here or not there:
        lines.append(Line("firmware", "FLASHER and WEB-STUDIO carry the same images", SKIP, "one of the two has no bundled images here"))
    elif here == there:
        lines.append(Line("firmware", "FLASHER and WEB-STUDIO carry the same images", PASS, f"{len(here)} image(s), identical"))
    else:
        different = sorted(set(here) ^ set(there) | {name for name in set(here) & set(there) if here[name] != there[name]})
        lines.append(Line("firmware", "FLASHER and WEB-STUDIO carry the same images", FAIL, "differ: " + ", ".join(different)))
    return lines


def newest_release_version(fetch: Callable[[str], bytes] | None = None) -> str | None:
    """The version of the newest URTC firmware release (a pre-release counts), or None."""
    def fetch_default(url: str) -> bytes:
        request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "urtc-doctor"})
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read()

    releases = json.loads((fetch or fetch_default)(FIRMWARE_RELEASES_URL))
    versions = [str(item["tag_name"]).lstrip("v") for item in releases if isinstance(item, dict) and not item.get("draft") and re.match(r"^v?\d+(\.\d+)+$", str(item.get("tag_name", "")))]
    return max(versions, key=_version_key) if versions else None


def check_release(workspace: Path, *, fetch: Callable[[str], bytes] | None = None) -> list[Line]:
    """The bundled firmware against the newest release (needs the network; only run with --online)."""
    bundled = _bundled_images(workspace / "URTC-FLASHER" / "firmware")
    versions = [m.group(1) for name in bundled if (m := FIRMWARE_NAME.match(name))]
    if not versions:
        return [Line("release", "newest firmware release", SKIP, "URTC-FLASHER has no bundled application image here")]
    have = max(versions, key=_version_key)
    try:
        newest = newest_release_version(fetch)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return [Line("release", "newest firmware release", SKIP, f"could not ask GitHub: {exc}")]
    if newest is None:
        return [Line("release", "newest firmware release", SKIP, "GitHub lists no release")]
    if _version_key(newest) > _version_key(have):
        return [Line("release", "newest firmware release", WARN, f"bundled {have}, newest release {newest}: run tools/sync_firmware.py")]
    return [Line("release", "newest firmware release", PASS, f"bundled {have}, newest release {newest}")]


def check_own(repo: Path, *, python: str = sys.executable, runner: Runner = subprocess.run, workspace: Path | None = None, siblings: bool = True) -> list[Line]:
    """The checks of this repository: its own validation and the generated documents."""
    commands = [("URTC-DOCS", ["tools/ci_validate.py"]), ("docs: readmes", ["tools/make_readmes.py", "--check"]), ("docs: brand", ["tools/make_brand.py", "--check"])]
    if siblings:
        commands += [("docs: catalogue structure", ["tools/make_catalog.py", "--check-structure", "--require-siblings"]),
                     ("docs: At a glance tables", ["tools/make_glance.py", "--check"]),
                     ("docs: claim hygiene", ["tools/check_claims.py", "--require-siblings"])]
    lines = []
    for name, command in commands:
        done = runner([python, *command], cwd=str(repo), capture_output=True, text=True)
        out = ((done.stdout or "") + (done.stderr or "")).strip().splitlines()
        token = next((line.strip() for line in reversed(out) if re.search(r"[A-Z_]+=(PASS|FAIL|SKIP|WRITTEN)", line)), "")
        lines.append(Line("docs", name, PASS if done.returncode == 0 else FAIL, token or f"exit code {done.returncode}"))
    if not siblings:
        for name in ("docs: catalogue structure", "docs: At a glance tables", "docs: claim hygiene"):
            lines.append(Line("docs", name, SKIP, "no sibling repositories to read"))
    return lines


# ---------------------------------------------------------------------------------------------------------------------
# the report
# ---------------------------------------------------------------------------------------------------------------------
def run_doctor(repo: Path, workspace: Path | None = None, *, online: bool = False, fast: bool = False, python: str = sys.executable,
               runner: Runner = subprocess.run, fetch: Callable[[str], bytes] | None = None) -> list[Line]:
    """Every group of checks. `fast` leaves out the ones that start other programs (the validations of each repository and of the documents)."""
    workspace = workspace or family.workspace_of(repo)
    repos = family.discover(workspace)
    siblings = [r for r in repos if r.name != family.OWN_NAME]
    lines = check_machine() + check_adapters()
    lines += check_versions(repos) if repos else [Line("versions", "all", SKIP, "no repository of the ecosystem next to this one")]
    lines += check_shared_copies(workspace, repos)
    lines += check_firmware(workspace, python=python, runner=runner)
    if not fast:
        lines += check_repositories(repos, python=python, runner=runner) if siblings else [Line("repositories", "all", SKIP, "no sibling repository found")]
        lines += check_own(repo, python=python, runner=runner, siblings=bool(siblings))
    if online:
        lines += check_release(workspace, fetch=fetch)
    return lines


def render(lines: list[Line]) -> tuple[str, int]:
    """The text of the report, and the exit status."""
    out, group = [], None
    for line in lines:
        if line.group != group:
            group = line.group
            out.append(f"\n[{group}]")
        out.append(f"  {line.status:<5}{line.name:<48} {line.detail}".rstrip())
    counts = {status: sum(1 for line in lines if line.status == status) for status in (PASS, FAIL, WARN, SKIP)}
    out.append("")
    out.append(f"passed {counts[PASS]}, failed {counts[FAIL]}, warnings {counts[WARN]}, skipped {counts[SKIP]}")
    if counts[FAIL]:
        out.append("URTC_DOCTOR=FAIL")
        return "\n".join(out), 1
    if counts[PASS] == 0:
        out.append("URTC_DOCTOR=FAIL nothing could be checked")
        return "\n".join(out), 1
    out.append("URTC_DOCTOR=PASS")
    return "\n".join(out), 0
