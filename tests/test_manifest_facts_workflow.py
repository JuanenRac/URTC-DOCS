# =============================================================================
# URTC-DOCS - tests/test_manifest_facts_workflow.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The nightly workflow of the computed facts opens its pull request with the token of the run and gets the checks started without any new secret.

GitHub does not start the checks of a branch or of a pull request that was made with the token of a workflow run; a dispatch is the exception. These are text
checks (no YAML library is needed) written so that a later edit cannot quietly give the workflow a secret, widen the permissions of the whole workflow or drop
the dispatch of the checks that lets the pull request be merged.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
FACTS = (WORKFLOWS / "manifest-facts.yml").read_text(encoding="utf-8").replace("\r\n", "\n")
CI = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8").replace("\r\n", "\n")
CODE = "\n".join(line for line in FACTS.split("\n") if not line.lstrip().startswith("#"))


def test_the_workflow_itself_only_reads_and_the_job_holds_the_write_permissions() -> None:
    top = re.search(r"(?m)^permissions:\n((?:  .*\n)+)", CODE)
    assert top is not None
    assert top.group(1).strip() == "contents: read"
    job = re.search(r"(?m)^    permissions:\n((?:      .*\n)+)", CODE)
    assert job is not None
    granted = dict(re.findall(r"(?m)^      ([a-z-]+): (read|write)", job.group(1)))
    assert granted == {"contents": "write", "pull-requests": "write", "issues": "write", "actions": "write"}


def test_no_secret_and_no_personal_token_is_used() -> None:
    assert "secrets." not in CODE
    assert "PAT" not in CODE and "DISPATCH_TOKEN" not in CODE
    assert CODE.count("GH_TOKEN: ${{ github.token }}") == 4


def test_the_pull_request_is_opened_with_the_token_of_the_run() -> None:
    assert 'gh pr create --repo "${{ github.repository }}" --head "$branch" --base main' in CODE
    assert "x-access-token:${GH_TOKEN}@github.com/${{ github.repository }}.git" in CODE


def test_the_checks_are_started_on_the_branch_after_the_push() -> None:
    push = CODE.index('git push --force "https://x-access-token')
    dispatch = CODE.index('gh workflow run ci.yml --repo "${{ github.repository }}" --ref "$branch"')
    assert push < dispatch
    assert "exit 0; fi" in CODE[:push]  # nothing is pushed or dispatched when no fact changed


def test_the_workflow_that_is_dispatched_accepts_a_dispatch() -> None:
    assert re.search(r"(?m)^  workflow_dispatch:", CI)
