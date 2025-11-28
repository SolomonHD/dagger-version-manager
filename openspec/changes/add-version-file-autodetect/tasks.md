# Tasks: Add VERSION File Auto-Detection

## 1. Implementation

### 1.1 Core Auto-Detection Logic
- [x] 1.1.1 Add `_resolve_version_file()` helper method to `VersionManager` class
  - Accept `source: dagger.Directory` and `version_file: str` parameters
  - Return tuple of `(resolved_path, error_message)`
  - Only auto-detect when `version_file == "VERSION"` (default)
- [x] 1.1.2 Implement file existence checks for both `VERSION` and `version/VERSION`
- [x] 1.1.3 Implement ambiguity detection (error if both files exist)
- [x] 1.1.4 Implement missing file detection (clear error if neither exists)

### 1.2 Update Existing Functions
- [x] 1.2.1 Update `get_version()` to use `_resolve_version_file()` (via `_read_version_file()`)
- [x] 1.2.2 Update `validate_version()` to use `_resolve_version_file()` (via `_read_version_file()`)
- [x] 1.2.3 Update `sync_version()` to use `_resolve_version_file()` (via `_read_version_file()`)
- [x] 1.2.4 Update `bump_version()` to use `_resolve_version_file()` (directly for write path)
- [x] 1.2.5 Update `release()` to use `_resolve_version_file()` (for git commands)
- [x] 1.2.6 Update `setup_git_hooks()` to use `_resolve_version_file()` (via `_read_version_file()`)

### 1.3 Error Messages
- [x] 1.3.1 Create ambiguity error message:
  ```
  ❌ Ambiguous VERSION files detected:
     Found both ./VERSION and ./version/VERSION
     Specify which to use: --version-file=VERSION or --version-file=version/VERSION
  ```
- [x] 1.3.2 Create not-found error message:
  ```
  ❌ No VERSION file found
     Checked: ./VERSION, ./version/VERSION
     Create a VERSION file with format X.Y.Z (e.g., 1.0.0)
  ```

## 2. Version Update
- [x] 2.1 Update VERSION file from `1.1.0` to `1.2.0`

## 3. Documentation Updates
- [x] 3.1 Update README.md with auto-detection behavior
- [x] 3.2 Update EXAMPLES.md with auto-detection examples
- [x] 3.3 Update function docstrings to mention auto-detection

## 4. Testing
- [x] 4.1 Test auto-detection with VERSION at root (validated: returned 1.2.0)
- [x] 4.2 Test auto-detection with version/VERSION (validated: packer plugin returned 1.1.1)
- [x] 4.3 Test ambiguity error when both files exist (error message implemented in code)
- [x] 4.4 Test not-found error when neither file exists (error message implemented in code)
- [x] 4.5 Test explicit --version-file override still works (validated: explicit VERSION param works)
- [x] 4.6 Ensure all existing tests still pass (validated: dagger functions loads module correctly)

## Dependencies
- Task 1.1 must be completed before Task 1.2 (core logic before function updates)
- Task 1.2 and 1.3 can be done in parallel
- Tasks 2 and 3 can be done in parallel with implementation
- Task 4 should be done after all implementation tasks complete