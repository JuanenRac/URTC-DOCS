# =============================================================================
# URTC-DOCS - tests/test_related_run.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What `related.run` reports for a workspace: a repository that is not there, a README that is missing, one without the section, one out of date, and what writing does."""
from __future__ import annotations

from pathlib import Path

from urtc_docs import readmes, related

OTHER = "URTC-COMMON"


def readme_with_section(body: str = "old text") -> str:
    return f"# Title\n\n{related.HEADING}Related Projects\n\n{body}\n\n## Next\n\nkeep\n"


def make_folder(workspace: Path, name: str, text: str | None) -> Path:
    folder = workspace / name
    folder.mkdir()
    if text is not None:
        for filename in related.FILES.values():
            (folder / filename).write_bytes(text.encode("utf-8"))
    return folder


def test_the_repository_that_owns_the_section_is_never_touched(tmp_path: Path):
    problems, done = related.run(tmp_path, [readmes.NAME], write=True)
    assert (problems, done) == ([], 0)


def test_a_repository_that_is_not_in_the_workspace_is_a_problem(tmp_path: Path):
    problems, done = related.run(tmp_path, [OTHER])
    assert done == 0
    assert problems == [f"{OTHER}: not found in {tmp_path}"]


def test_a_missing_readme_is_reported_for_each_language(tmp_path: Path):
    make_folder(tmp_path, OTHER, None)
    problems, done = related.run(tmp_path, [OTHER])
    assert done == 0
    assert sorted(problems) == sorted(f"{OTHER}/{filename}: missing" for filename in related.FILES.values())


def test_a_readme_without_the_heading_is_reported_not_changed(tmp_path: Path):
    folder = make_folder(tmp_path, OTHER, "# Title\n\n## Other\n")
    problems, done = related.run(tmp_path, [OTHER], write=True)
    assert done == 0 and len(problems) == len(related.FILES)
    assert all("no Related Projects heading" in problem for problem in problems)
    assert (folder / "README.md").read_text(encoding="utf-8") == "# Title\n\n## Other\n"


def test_an_out_of_date_section_is_reported_and_only_written_on_request(tmp_path: Path):
    folder = make_folder(tmp_path, OTHER, readme_with_section())
    problems, done = related.run(tmp_path, [OTHER])
    assert done == 0 and len(problems) == len(related.FILES)
    assert all("the Related Projects section is out of date" in problem for problem in problems)
    assert "old text" in (folder / "README.md").read_text(encoding="utf-8")

    problems, done = related.run(tmp_path, [OTHER], write=True)
    assert (problems, done) == ([], len(related.FILES))
    written = (folder / "README.md").read_text(encoding="utf-8")
    assert "old text" not in written and written.endswith("## Next\n\nkeep\n")

    problems, done = related.run(tmp_path, [OTHER])
    assert (problems, done) == ([], len(related.FILES))   # now current
