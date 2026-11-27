# =============================================================================
# URTC-DOCS - src/urtc_docs/devtools_lock.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The lock file that says which version of the shared tools a repository carries.

The shared tools are versioned as a set in the repository URTC-DEVTOOLS (the version of that repository is the version of the set). When a
repository takes the set with ``sync_repo_tools.py``, a file ``tools/devtools.lock.json`` is written next to the copies:

    {"schema": 1, "source": "URTC-DEVTOOLS", "version": "0.0.1", "files": {"tools/_doc_policy.py": "<sha256>", ...}}

The hash is that of the file as it sits in the repository (line endings read as newlines), so a hand edit changes it. ``check_repo_tools.py`` compares the lock
with the files (a copy that was edited is found) and, when URTC-DEVTOOLS is next to the repository, with the version of the set (a copy that fell behind is
found). The lock is a file of the repository: reading it needs no network and no other checkout, so each repository stays buildable on its own.

When URTC-DEVTOOLS is next to the repository, the copies are also compared with its canonical files (a hand edit whose lock was written again afterwards agrees
with its own lock and is found that way), and the repositories listed under ``expected_repositories`` in its ``tools/tooling_registry.json`` are expected to carry a
lock: one without a lock is a problem, and is only counted when ``allow_missing_lock`` is True.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

LOCK_FILE = "tools/devtools.lock.json"
SOURCE = "URTC-DEVTOOLS"
SCHEMA = 1
REGISTRY = "tools/tooling_registry.json"
# any name of a repository of the family: a header says which repository the file sits in, and the name is the one thing allowed to differ
_FAMILY_NAME = re.compile(r"(?<![A-Za-z0-9_-])URTC(?:-[A-Z0-9]+)*(?![A-Za-z0-9_])")


def digest(text: str) -> str:
    """SHA-256 of a text as it is compared: line endings as newlines, UTF-8."""
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def set_version(workspace: Path) -> str | None:
    """The version of the set: the one of the manifest of URTC-DEVTOOLS when it is next to the repositories, otherwise None."""
    manifest = workspace / SOURCE / "urtc.project.json"
    if not manifest.is_file():
        return None
    try:
        version = json.loads(manifest.read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None
    return version if isinstance(version, str) and version else None


def canonical_dir(workspace: Path) -> Path | None:
    """The canonical files of the set (``files/`` of URTC-DEVTOOLS) when that repository is next to the others."""
    path = workspace / SOURCE / "files"
    return path if path.is_dir() else None


def expected_repositories(workspace: Path) -> tuple[str, ...]:
    """The repositories that must carry a lock, from the registry of URTC-DEVTOOLS; none when it is not there or does not say."""
    path = workspace / SOURCE / REGISTRY
    if not path.is_file():
        return ()
    try:
        names = json.loads(path.read_text(encoding="utf-8")).get("expected_repositories", [])
    except (OSError, json.JSONDecodeError, AttributeError):
        return ()
    return tuple(n for n in names if isinstance(n, str)) if isinstance(names, list) else ()


def same_as_canonical(repository: str, relative: str, text: str, canonical: Path) -> bool:
    """True when a copy is the canonical file (newlines only, the name of the repository where the file says <REPO>); a canonical file that is not there counts as equal."""
    path = canonical / relative
    if not path.is_file():
        return True
    wanted = path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n")
    text = text.replace("\r\n", "\n")
    return text == wanted.replace("<REPO>", repository) or _FAMILY_NAME.sub("<REPO>", text) == _FAMILY_NAME.sub("<REPO>", wanted)


def render(version: str, hashes: dict[str, str]) -> str:
    return json.dumps({"schema": SCHEMA, "source": SOURCE, "version": version, "files": dict(sorted(hashes.items()))}, indent=2) + "\n"


def read(repo: Path) -> dict | None:
    """The lock of a repository, or None when it has none or it cannot be read."""
    path = repo / LOCK_FILE
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"unreadable": True}
    return data if isinstance(data, dict) else {"unreadable": True}


def hashes_of(repo: Path, files: tuple[str, ...], overrides: dict[str, str] | None = None) -> dict[str, str]:
    """The hash of every shared file the repository carries; ``overrides`` gives the text a file is about to get."""
    found: dict[str, str] = {}
    for relative in files:
        if overrides and relative in overrides:
            found[relative] = digest(overrides[relative])
        elif (repo / relative).is_file():
            found[relative] = digest((repo / relative).read_bytes().decode("utf-8", errors="replace"))
    return found


def check_repo(repo: Path, files: tuple[str, ...], version: str | None, canonical: Path | None = None) -> list[str]:
    """The problems of the lock of one repository (empty when it matches its files and, if the set is known, is not behind it).

    With ``canonical`` (the files of URTC-DEVTOOLS) a copy that agrees with the lock but is not the canonical file is a problem too: the lock was written again after an edit."""
    lock = read(repo)
    if lock is None:
        return []
    if lock.get("unreadable") or lock.get("schema") != SCHEMA or not isinstance(lock.get("files"), dict):
        return [f"{LOCK_FILE} cannot be read (schema {SCHEMA} expected)"]
    problems: list[str] = []
    locked: dict[str, str] = lock["files"]
    for relative, expected in sorted(locked.items()):
        path = repo / relative
        if not path.is_file():
            problems.append(f"{relative}: in the lock but missing")
        elif digest(path.read_bytes().decode("utf-8", errors="replace")) != expected:
            problems.append(f"{relative}: edited after the set was taken (it differs from the lock)")
    for relative in files:
        if (repo / relative).is_file() and relative not in locked:
            problems.append(f"{relative}: a shared file that the lock does not list")
    if version is not None and lock.get("version") != version:
        problems.append(f"the lock says set {lock.get('version')!r}, URTC-DEVTOOLS is at {version!r}: run sync_repo_tools.py --apply")
    elif canonical is not None and not problems:
        for relative in files:
            path = repo / relative
            if path.is_file() and not same_as_canonical(repo.name, relative, path.read_bytes().decode("utf-8", errors="replace"), canonical):
                problems.append(f"{relative}: edited and the lock recalculated (it differs from the canonical file of URTC-DEVTOOLS)")
    return problems


def missing_expected(workspace: Path, repos: list[Path]) -> list[str]:
    """The repositories of ``expected_repositories`` that are among ``repos`` and carry no lock."""
    expected = set(expected_repositories(workspace))
    return sorted(repo.name for repo in repos if repo.name in expected and read(repo) is None)


def check_workspace(workspace: Path, repos: list[Path], files: tuple[str, ...], allow_missing_lock: bool = False) -> tuple[list[tuple[str, str]], int]:
    """Every problem of every lock as (repository, text), and how many repositories carry a lock.

    A repository that is expected to carry a lock and has none is a problem unless ``allow_missing_lock`` is True (``missing_expected`` counts it either way)."""
    version = set_version(workspace)
    canonical = canonical_dir(workspace)
    found: list[tuple[str, str]] = []
    locked = 0
    expected = set(expected_repositories(workspace))
    for repo in repos:
        if read(repo) is None:
            if not hashes_of(repo, files) and repo.name in expected and not allow_missing_lock:
                found.append((repo.name, f"{LOCK_FILE} is missing (the repository is in expected_repositories of URTC-DEVTOOLS)"))
            # a repository that carries the shared files has to carry the lock that says which set they are: deleting it must not silence the check
            if hashes_of(repo, files):
                found.append((repo.name, f"{LOCK_FILE} is missing although the repository carries shared files (run sync_repo_tools.py --apply)"))
            continue
        locked += 1
        found += [(repo.name, problem) for problem in check_repo(repo, files, version, canonical)]
    return found, locked
