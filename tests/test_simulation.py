# =============================================================================
# URTC-DOCS - tests/test_simulation.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The nights of the comparison over a virtual ecosystem (evidence: simulator): what makes a night fail, what only advises, and that every fault heals."""
from __future__ import annotations

from pathlib import Path

import pytest

from urtc_docs import drift
from urtc_docs.simulation import HUB, VirtualEcosystem


@pytest.fixture()
def eco(tmp_path: Path) -> VirtualEcosystem:
    return VirtualEcosystem(tmp_path)


def failures(report) -> str:
    return "\n".join(report.failures)


def test_a_new_ecosystem_has_a_quiet_night(eco):
    report = eco.night()
    assert report.failures == []
    assert report.advisories == []
    assert not report.failed


def test_every_repository_validates_itself_but_the_hub(eco):
    eco.night()
    assert HUB not in eco.validation.calls
    assert sorted(eco.validation.calls) == sorted(name for name in eco.names if name != HUB)


def test_a_release_that_updates_manifest_source_and_changelog_only_advises_about_the_catalogue(eco):
    eco.release("URTC-GATEWAY", "0.2.0")
    report = eco.night()
    assert not report.failed
    assert any("catalogue versions" in line for line in report.advisories)
    eco.regenerate_catalogue()
    assert eco.night().advisories == []


def test_a_manifest_that_moved_without_its_source_fails_the_night(eco):
    eco.move_manifest_only("URTC-TESTER", "0.3.0")
    report = eco.night()
    assert report.failed
    assert "versions URTC-TESTER" in failures(report)
    assert "source file says 0.1.0" in failures(report)
    eco.release("URTC-TESTER", "0.3.0")
    eco.regenerate_catalogue()
    assert eco.night().failures == []


def test_a_repository_that_appears_fails_the_structure_until_the_catalogue_is_written_again(eco):
    eco.add_repository("URTC-FLASHER")
    report = eco.night()
    assert report.failed
    assert "catalogue structure" in failures(report)
    eco.regenerate_catalogue()
    eco.take_the_set()
    assert eco.night().failures == []


def test_a_repository_that_goes_fails_the_structure_too(eco):
    eco.remove_repository("URTC-GATEWAY")
    assert "catalogue structure" in failures(eco.night())
    eco.regenerate_catalogue()
    assert eco.night().failures == []


def test_a_change_of_role_is_a_change_of_structure(eco):
    eco.change_role("URTC-TESTER", "service")
    assert "catalogue structure" in failures(eco.night())
    eco.regenerate_catalogue()
    assert eco.night().failures == []


def test_a_shared_copy_edited_by_hand_is_found_as_drift_and_as_a_lock_problem(eco):
    eco.hand_edit_shared("URTC-GATEWAY")
    text = failures(eco.night())
    assert "shared copy URTC-GATEWAY/tools/build_test.py" in text
    assert "lock URTC-GATEWAY: tools/build_test.py: edited after the set was taken" in text
    eco.take_the_set()
    assert eco.night().failures == []


def test_a_new_version_of_the_set_leaves_every_lock_behind_until_it_is_taken(eco):
    eco.publish_set("0.0.7")
    report = eco.night()
    assert report.failed
    behind = [line for line in report.failures if line.startswith("lock ") and "0.0.7" in line]
    assert len(behind) == len(eco.names)
    eco.take_the_set()
    assert eco.night().failures == []


def test_a_repository_whose_own_validation_fails_fails_the_night_and_the_others_still_run(eco):
    eco.break_validation("URTC-COMMON")
    report = eco.night()
    assert "repositories URTC-COMMON: CI_VALIDATION=FAIL" in failures(report)
    assert sorted(eco.validation.calls) == sorted(name for name in eco.names if name != HUB)
    eco.fix_validation("URTC-COMMON")
    assert eco.night().failures == []


def test_something_private_in_a_readme_blocks_the_night_and_clears_when_removed(eco):
    eco.leak("URTC")
    text = failures(eco.night())
    assert "private content BLOCK URTC README.md" in text
    eco.unleak("URTC")
    assert eco.night().failures == []


def test_several_faults_on_the_same_night_are_all_reported(eco):
    eco.hand_edit_shared("URTC")
    eco.move_manifest_only("URTC-TESTER", "0.3.0")
    eco.break_validation("URTC-GATEWAY")
    eco.leak("URTC-COMMON")
    text = failures(eco.night())
    for expected in ("shared copy URTC/", "versions URTC-TESTER", "repositories URTC-GATEWAY", "private content BLOCK URTC-COMMON"):
        assert expected in text, expected


def test_a_week_of_nights_with_a_release_a_slip_and_a_repair(eco):
    schedule = [
        None,                                                          # night 1: quiet
        lambda e: e.release("URTC-GATEWAY", "0.2.0"),                  # night 2: only the catalogue versions advise
        lambda e: e.hand_edit_shared("URTC-TESTER"),                   # night 3: drift and lock
        lambda e: e.take_the_set(),                                    # night 4: healed
        lambda e: e.move_manifest_only("URTC-COMMON", "0.5.0"),        # night 5: a bump that was half done
        lambda e: (e.release("URTC-COMMON", "0.5.0"), e.regenerate_catalogue()),  # night 6: repaired
        None,                                                          # night 7: quiet
    ]
    reports = eco.play(schedule)
    assert [report.night for report in reports] == [1, 2, 3, 4, 5, 6, 7]
    assert [report.failed for report in reports] == [False, False, True, False, True, False, False]
    assert reports[1].advisories and not reports[1].failures
    assert reports[5].advisories == [] and reports[6].advisories == []
    assert eco.reports == reports


def test_the_shared_copies_of_a_new_ecosystem_are_the_template(eco):
    found, count = drift.check_workspace(eco.root, template_dir=drift.TEMPLATE_DIR)
    assert found == []
    assert count == len(eco.names)


def test_the_validation_double_answers_pass_or_fail_as_told(eco):
    eco.break_validation("URTC")
    fail = eco.validation(["python", "tools/ci_validate.py"], cwd=str(eco.repo("URTC")))
    ok = eco.validation(["python", "tools/ci_validate.py"], cwd=str(eco.repo("URTC-COMMON")))
    assert (fail.returncode, ok.returncode) == (1, 0)
    assert "CI_VALIDATION=FAIL" in fail.stdout and "CI_VALIDATION=PASS" in ok.stdout
