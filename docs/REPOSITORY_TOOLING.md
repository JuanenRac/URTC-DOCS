<!--
=============================================================================
URTC-DOCS - Design note: packaging the shared repository tooling
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# Packaging the shared repository tooling

A design note, not a plan. Whether the structure described under "Proposal" is built is a decision that belongs to the owner of the ecosystem; nothing here is built yet.

## What is shared today

Every repository of the family carries a copy of the same small set of tools. The list is `SHARED_FILES` in `src/urtc_docs/drift.py`:

| Group | Files | What they do |
|---|---|---|
| Documentation checks | `tools/_doc_policy.py`, `tools/_readme_parity.py`, `tools/_tracked_names.py`, `tools/universal_readme_check.py` | The rules every README, changelog and tracked file name must follow, and the layout of the README. |
| Pictures | `tools/_readme_svg.py`, `tools/make_architecture.py`, `tools/make_structure.py` | The architecture and repository-structure drawings, generated from `docs/architecture.json` and `docs/structure.json`. |
| Scripts | `tools/build_test.py`, `tools/pretty_run.py`, `bump_manifest_version.py` | The non-versioning build check, the live panel of the build and test scripts, and the version bump of the manifest. |
| Workflow | `.github/workflows/dashboard-dispatch.yml` | The notice that tells the dashboard a repository changed. |

`tools/sync_repo_tools.py` copies them from the template (`template/eh3d-repo-template`) into the repositories and `tools/check_repo_tools.py` fails when a copy differs from the template, so a copy cannot drift without being noticed. The copies are identical on purpose: each repository is built and checked on its own, in CI, with nothing but its own checkout.

## What is wrong with copies

* A change to one tool is a change in about ten repositories: one commit and one CI run each.
* Some of the copies are shared with the sister ecosystems (the same tool exists in the repositories of the others), so a change made here alone would split the family into two versions of the same file. Those copies are changed in one place, in all the ecosystems, or not at all.
* Nothing says which version of the tools a repository carries: the check compares text with the template, it does not name a version.

## Options

| Option | Good | Bad |
|---|---|---|
| **Stay with copies** (today) | Each repository stands alone; CI needs no network beyond its own checkout; a copy can be read where it is used. | Every change is many commits; no version number for the set. |
| **A package installed from git** (`pip install` of a tag of a tools repository) | One place to change; a pinned tag is a version; each repository says which one it uses. | CI of every repository now needs the network and one more repository to be available; a tag of a public repository becomes part of every build; Windows and Linux runners resolve it at install time. |
| **A subtree or submodule** of a tools repository in each repository | The files stay in the checkout; the version is the commit that was pulled. | Submodules need an extra step in every clone and CI; a subtree puts the history of the tools in every repository; both are easy to get wrong and break the "one checkout is enough" rule. |
| **A package published to an index** | The usual way to share Python code. | The tools are not a library for the world: they are a convention of this family, and publishing them makes a public commitment to their interface. |

## Proposal

If the number of copies keeps growing, the least risky step is not to remove the copies but to give the set a name and a version, and to keep the check:

1. A repository of the tools (`urtc-devtools`) holds the files above, a `VERSION` and a changelog, and nothing else. It is the template of today, with a version.
2. `tools/sync_repo_tools.py` stays the way a repository takes the set, but it writes `tools/devtools.lock.json` with the version and the SHA-256 of each file, as `vendor_copy.py` already does for the shared code of URTC-COMMON. The check compares the lock with the files (a hand edit is found) and, when the tools repository is next to it, with the version (a copy that fell behind is found).
3. A repository stays buildable and checkable with its own checkout: the lock is a file in the repository, and the network is not needed to read it.
4. The copies that are shared with the sister ecosystems are moved last, together, with the owners of those repositories, because the file has to stay identical in all of them.

This keeps what works (a repository stands alone), and adds what is missing (a version for the set and a way to tell a copy that was edited from one that is behind). It needs one new repository and a change of two tools; it does not need a package index, a submodule or a network at build time.

## What exists now

The repository `URTC-DEVTOOLS` holds the files of `SHARED_FILES` under `files/`, with the version of the repository as the version of the set and its own changelog. `tools/sync_repo_tools.py` writes `tools/devtools.lock.json` (the format is in the documentation of that repository) and `tools/check_repo_tools.py` compares it with the files and with the version of the set. The template of this repository (`template/eh3d-repo-template`) is still the source the synchroniser reads; the two are compared by a test of URTC-DEVTOOLS when both are next to each other. No other repository has taken the lock yet, and the copies shared with the sister ecosystems have not moved.

## Not decided

* Whether the tools repository is public or stays inside the template repository as a folder with a version.
* Whether the lock replaces the comparison with the template or is checked next to it.
* The date at which the shared copies of the sister ecosystems are moved.
