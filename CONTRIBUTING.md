# Contributing to URTC-DOCS 📚

This repository is the memory of the URTC ecosystem: its architecture, interfaces, security baseline, capability matrix and the tools that keep them honest. Contributions that make the documents more accurate are the most useful ones.

## Technology Stack
- **Documents**: Markdown, with Mermaid diagrams.
- **Tools**: Python 3.10+, standard library only; pytest for the tests.

## Guidelines
1. **Trace every statement.** A claim about another repository must be readable in that repository's README, manifest, changelog or documents. If it cannot be traced, say so in the sentence. Never write that something works on hardware unless the repository that owns it says it was measured there.
2. **Keep the levels apart.** A unit test, a loopback test, an emulation and a bench result are different claims (see the legend of the capability matrix); a lighter one never stands in for a heavier one.
3. **Generated files are not edited by hand.** `docs/PROJECT_CATALOG.md` (between its markers), the eight READMEs, and the files in `images/` and `brand/` are written by `tools/make_catalog.py`, `tools/make_readmes.py` and `tools/make_brand.py`; change the source in `src/urtc_docs/` and regenerate.
4. **Eight languages.** Any user-facing text of a README exists in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese in `src/urtc_docs/readme_text.py`; a test refuses a missing one.
5. **Nothing private in public files.** No dates, no names of private notes, no tracking codes, no secrets, no addresses of a real installation. Run `python tools/publication_check.py` before a release.
6. **Tests.** `python -m pytest tests -q` must pass; a new tool needs tests. Use `build-test.sh` / `build-test.bat` to check without changing the version; `build.sh` / `build.bat` raise it.
