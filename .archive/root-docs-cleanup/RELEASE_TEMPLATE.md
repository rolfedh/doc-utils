# Git Tag and Release Templates

## Git Tag Message

```bash
git tag -a v0.1.2 -m "Release v0.1.2: Improved reliability and test coverage

- Fixed ModuleNotFoundError installation issues
- Added comprehensive test coverage (100% pass rate)
- Eliminated code duplication in exclusion parsing
- Added exclusion support to check-scannability
- Improved documentation and troubleshooting guides"
```

## GitHub Release Title
`v0.1.2 - Reliability and Quality Improvements`

## GitHub Release Description

### What's Changed

**🐛 Bug Fixes**
- Fixed `ModuleNotFoundError` when running CLI commands (#1)
- Resolved test failures due to substring matching issues

**✨ New Features**
- Added `--exclude-dir`, `--exclude-file`, and `--exclude-list` options to `check-scannability`
- Centralized exclusion list parsing with new `parse_exclude_list_file()` function

**📚 Documentation**
- Added troubleshooting section for common installation issues
- Enhanced README with directory/file exclusion examples
- Created CLAUDE.md for AI-assisted development

**🧪 Testing**
- Increased test coverage from 38 to 47 tests
- Achieved 100% test pass rate
- Added comprehensive tests for file utilities and CLI entry points

**🔧 Code Quality**
- Removed code duplication across CLI tools
- Cleaned up dead code and unused imports
- Reorganized test fixtures for better structure

### Installation

```bash
pip install -U rolfedh-doc-utils
```

**Full Changelog**: https://github.com/rolfedh/doc-utils/compare/v0.1.1...v0.1.2

---

## Version Bump Checklist

Before releasing:
1. [ ] Update version in `pyproject.toml` to `0.1.2`
2. [ ] Update CHANGELOG.md with release date
3. [ ] Run full test suite: `python -m pytest tests/`
4. [ ] Commit changes: `git commit -am "Prepare release v0.1.2"`
5. [ ] Create and push tag: `git tag -a v0.1.2 -m "..."`
6. [ ] Push tag: `git push origin v0.1.2`
7. [ ] Create GitHub release with above description
8. [ ] Verify PyPI deployment (should happen automatically via GitHub Action)