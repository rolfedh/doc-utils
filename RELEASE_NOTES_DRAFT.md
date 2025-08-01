# Release Notes for v0.1.2

## 🎯 Highlights

This release focuses on improving reliability, code quality, and user experience. All CLI tools now work consistently, with better error messages and comprehensive test coverage.

## 🚀 Key Improvements

### For Users

1. **Fixed Installation Issues**
   - Resolved `ModuleNotFoundError` when running commands after installation
   - Added clear troubleshooting guide in README for common issues
   - Improved development installation instructions

2. **Enhanced Consistency**
   - All tools now support the same exclusion options (--exclude-dir, --exclude-file, --exclude-list)
   - `check-scannability` now has exclusion support like other tools

3. **Better Documentation**
   - Added comprehensive directory/file exclusion examples
   - Clear installation instructions for both PyPI and development
   - Troubleshooting section for common problems

### For Developers

1. **Code Quality**
   - Eliminated code duplication by centralizing exclusion list parsing
   - Removed dead code and unused imports
   - Better organization with test fixtures in proper location

2. **Test Coverage**
   - Added 26 new tests for comprehensive coverage
   - 100% test pass rate (47 tests total)
   - Fixed all previously failing tests

3. **Development Experience**
   - Added CLAUDE.md with project context for AI assistants
   - Improved module structure and imports
   - Better error messages and handling

## 📝 Breaking Changes

None - this release maintains full backward compatibility.

## 🔧 Installation

```bash
# From PyPI
pip install -U rolfedh-doc-utils

# For development
git clone https://github.com/rolfedh/doc-utils.git
cd doc-utils
pip install -e .
```

## 🙏 Acknowledgments

Thanks to all contributors and users who reported issues, especially the ModuleNotFoundError issue that led to several improvements in this release.