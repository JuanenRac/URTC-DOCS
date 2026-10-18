# =============================================================================
# URTC-DOCS - tests/test_cli_and_repository.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from conftest import write_repo

from urtc_docs import __version__, catalog, cli

REPO = Path(__file__).resolve().parents[1]


# --- the command line ---------------------------------------------------------------------------------

def run_catalog(workspace: Path, page: Path, *flags: str) -> int:
    return cli.make_catalog(["--workspace", str(workspace), "--catalog", str(page), *flags])


def test_catalog_skips_when_nothing_is_next_to_it_and_fails_when_asked_to_require(tmp_path, capsys):
    page = tmp_path / "page.md"
    page.write_text(f"{catalog.BEGIN}\n{catalog.END}\n", encoding="utf-8")
    assert run_catalog(tmp_path, page, "--check") == 0
    assert "CATALOG=SKIP" in capsys.readouterr().out          # a skip is never printed as a pass
    assert run_catalog(tmp_path, page, "--check", "--require-siblings") == 1
    assert "CATALOG=FAIL" in capsys.readouterr().err


def test_catalog_writes_then_passes_then_fails_when_a_version_moves(workspace, tmp_path, capsys):
    page = tmp_path / "page.md"
    page.write_text(f"intro\n{catalog.BEGIN}\n{catalog.END}\n", encoding="utf-8")
    assert run_catalog(workspace, page, "--check") == 1                      # empty block: stale
    capsys.readouterr()
    assert run_catalog(workspace, page) == 0
    assert "CATALOG=WRITTEN 3 repositories" in capsys.readouterr().out
    assert run_catalog(workspace, page, "--check") == 0
    assert "CATALOG=PASS" in capsys.readouterr().out
    write_repo(workspace, "URTC-FLASHER", family="Host Tools", role="api", stack="node", version="9.9.9")
    assert run_catalog(workspace, page, "--check") == 1
    assert run_catalog(workspace, page, "--check-structure") == 0           # only the version moved
    write_repo(workspace, "URTC-NEW")
    assert run_catalog(workspace, page, "--check-structure") == 1           # a repository appeared


def test_main_without_arguments_says_what_it_is(capsys):
    assert cli.main([]) == 0
    assert f"URTC-DOCS v{__version__}" in capsys.readouterr().out
    assert cli.main(["nonsense"]) == 2


def test_make_brand_and_readmes_check_this_repository(capsys):
    assert cli.make_brand(["--check"]) == 0
    assert cli.make_readmes(["--check"]) == 0
    out = capsys.readouterr().out
    assert "BRAND=PASS" in out and "READMES=PASS" in out


def test_publication_check_on_an_empty_workspace_is_a_skip(tmp_path, capsys):
    assert cli.publication_check(["--workspace", str(tmp_path)]) == 0
    assert "PUBLICATION_CHECK=SKIP" in capsys.readouterr().out


# --- this repository agrees with itself ---------------------------------------------------------------

def test_the_four_places_of_the_version_agree():
    manifest = json.loads((REPO / "urtc.project.json").read_text(encoding="utf-8"))
    pyproject_version = re.search(r'(?m)^version\s*=\s*"([^"]+)"', (REPO / "pyproject.toml").read_text(encoding="utf-8")).group(1)
    assert manifest["version"] == pyproject_version == __version__
    heading = re.search(r"(?m)^## \[(\d+\.\d+\.\d+(?:\.\d+)?)\]", (REPO / "CHANGELOG.md").read_text(encoding="utf-8"))
    assert heading and heading.group(1) == manifest["version"]


def test_the_manifest_follows_the_schema_of_the_sdk():
    manifest = json.loads((REPO / "urtc.project.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0" and manifest["ecosystem"] == "URTC"
    assert manifest["name"] == "URTC-DOCS" and re.fullmatch(r"URTC(-[A-Z0-9-]+)?", manifest["name"])
    assert manifest["role"] in {"api", "ui", "cli", "firmware", "library", "service", "tool"}
    assert manifest["deployment_target"] in {"cm5", "user-pc", "mobile", "wearable", "dev-server"}
    assert manifest["maturity"] in {"scaffolding", "functional", "established", "production"}
    assert manifest["technologies"] and len(set(manifest["technologies"])) == len(manifest["technologies"])
    assert set(manifest["native_version"]) == {"file", "pattern"}
    native = (REPO / manifest["native_version"]["file"]).read_text(encoding="utf-8")
    assert re.search(manifest["native_version"]["pattern"], native, re.MULTILINE)


def test_every_entry_of_the_changelog_is_a_dash_bullet_without_a_date():
    text = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    body = text.split("## [", 1)[1]
    for line in body.splitlines()[1:]:
        if line.strip():
            assert line.startswith("- ") or line.startswith("## ["), line
        assert not re.search(r"\b20\d\d-\d\d-\d\d\b", line)


def test_every_local_link_of_the_documents_exists():
    for path in [REPO / "README.md", *sorted((REPO / "docs").glob("*.md"))]:
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"(?i)(https?:|mailto:|#)", target):
                continue
            assert (path.parent / target.split("#")[0]).exists(), (path.name, target)


def test_the_documents_that_the_readmes_promise_exist():
    for name in ("ARCHITECTURE", "INTERFACES", "CAPABILITY_MATRIX", "SECURITY_BASELINE", "THREAT_MODEL", "FIRST_VERTICAL_SLICE", "PROJECT_CATALOG", "CAN_PROTOCOL_DUPLICATION"):
        assert (REPO / "docs" / f"{name}.md").is_file(), name


def test_the_catalogue_file_has_its_block():
    text = (REPO / "docs" / "PROJECT_CATALOG.md").read_text(encoding="utf-8")
    assert catalog.read_block(text) is not None


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash is not available")
def test_shell_scripts_have_valid_syntax():
    for script in ("tools/check_all.sh", "build.sh", "build-test.sh", "run.sh"):
        result = subprocess.run(["bash", "-n", script], capture_output=True, text=True, cwd=REPO)
        assert result.returncode == 0, (script, result.stderr)


def test_scripts_never_close_the_window_on_their_own():
    for script in ("build.sh", "build-test.sh", "run.sh"):
        text = (REPO / script).read_text(encoding="utf-8")
        assert "read -r" in text, script
    for script in ("build.bat", "build-test.bat", "run.bat"):
        assert "pause" in (REPO / script).read_text(encoding="utf-8"), script
