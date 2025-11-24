# Change: Add Git Hooks Setup Function

## Why

Users currently need to manually create git hooks for version validation (as documented in EXAMPLES.md lines 393-443). This is tedious and error-prone. Automating hook installation will improve the developer experience and ensure consistent version enforcement across projects.

**UPDATE**: The implementation revealed an issue when running on the dagger-version-manager module itself. Dagger modules must have `version = "0.0.0"` in pyproject.toml (Dagger requirement), so hook validation fails incorrectly. The change now includes Dagger module detection to skip hook installation for Dagger modules.

## What Changes

- Add `setup-git-hooks` function to DaggerVersionManager class
- Auto-detect project type based on marker files (galaxy.yml, pyproject.toml, Dockerfile, Chart.yaml)
- **NEW**: Detect Dagger module projects (presence of `dagger.json` at root) and skip hook installation
- Create/update pre-commit and pre-push hooks in `.git/hooks/` directory
- Mark hooks with metadata header for version tracking (`# DAGGER-VERSION-MANAGER: v{version}`)
- Preserve existing non-dagger-version-manager hooks (won't overwrite)
- Provide clear success/error messages with project type detection results
- **NEW**: Provide informative message when skipping Dagger module projects

## Impact

- **Affected specs**: `version-management`
- **Affected code**:
  - `src/main/__init__.py` - New `setup_git_hooks` function in DaggerVersionManager class
  - Hook templates will be generated dynamically for pre-commit and pre-push
  - **NEW**: Add Dagger module detection logic before project type detection
  - **NEW**: Update README.md and EXAMPLES.md to clarify usage context
- **Breaking changes**: None (adds detection, doesn't change behavior for consumer projects)
- **New dependencies**: None (uses Python stdlib only)