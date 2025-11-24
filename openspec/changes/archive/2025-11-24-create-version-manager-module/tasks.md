# Implementation Tasks

## 1. Project Setup

- [x] 1.1 Update `dagger.json` with Python SDK configuration
- [x] 1.2 Create `pyproject.toml` with dependencies and build configuration
- [x] 1.3 Create `.gitignore` to exclude `/sdk/` and Python artifacts
- [x] 1.4 Create `src/main/` directory structure
- [x] 1.5 Initialize Dagger SDK by running `dagger develop` or equivalent

## 2. Core Module Implementation

- [x] 2.1 Create `src/main/__init__.py` with `VersionManager` class skeleton
- [x] 2.2 Add `@object_type` decorator to `VersionManager` class
- [x] 2.3 Implement `_validate_semver()` private helper method for version format validation
- [x] 2.4 Implement `_read_version_file()` private helper for reading VERSION file
- [x] 2.5 Implement `_extract_version_from_target()` private helper for parsing target file version
- [x] 2.6 Implement `_bump_version_logic()` private helper for version incrementing
- [x] 2.7 Implement `get_version()` function with proper type annotations
- [x] 2.8 Implement `validate_version()` function with comparison logic
- [x] 2.9 Implement `sync_version()` function with regex pattern matching
- [x] 2.10 Implement `bump_version()` function supporting major/minor/patch
- [x] 2.11 Implement `release()` function orchestrating sync + validate + git commands
- [x] 2.12 Add comprehensive docstrings to all functions
- [x] 2.13 Add type annotations using `Annotated[Type, Doc("description")]` pattern

## 3. Error Handling

- [x] 3.1 Add validation for missing VERSION file with helpful error message
- [x] 3.2 Add validation for missing target file with helpful error message
- [x] 3.3 Add validation for invalid semver format in VERSION file
- [x] 3.4 Add validation for invalid bump_type parameter (must be major/minor/patch)
- [x] 3.5 Add validation for version pattern not found in target file
- [x] 3.6 Ensure all error messages include suggestions for resolution

## 4. Testing

- [x] 4.1 Create `tests/` directory structure
- [x] 4.2 Create `tests/unit/test_version_validation.py` for semver validation tests
- [x] 4.3 Create `tests/unit/test_version_bumping.py` for bump logic tests
- [x] 4.4 Create `tests/fixtures/` directory for test data
- [x] 4.5 Create test fixture for Ansible collection (VERSION + galaxy.yml)
- [x] 4.6 Create test fixture for Python project (VERSION + pyproject.toml)
- [x] 4.7 Write integration test for sync_version() with Ansible fixture
- [x] 4.8 Write integration test for validate_version() with mismatch scenario
- [x] 4.9 Write integration test for bump_version() all types (major/minor/patch)
- [x] 4.10 Write integration test for release() workflow
- [x] 4.11 Ensure all tests pass with `pytest`

## 5. Documentation

- [x] 5.1 Update `README.md` with overview and problem statement
- [x] 5.2 Add installation instructions to README (dagger install)
- [x] 5.3 Add quick start example to README
- [x] 5.4 Add function reference documentation to README
- [x] 5.5 Add troubleshooting section to README
- [x] 5.6 Create `EXAMPLES.md` with comprehensive usage examples
- [x] 5.7 Add Ansible collection example to EXAMPLES.md
- [x] 5.8 Add Python project example to EXAMPLES.md
- [x] 5.9 Add Docker project example to EXAMPLES.md
- [x] 5.10 Add Kubernetes/Helm example to EXAMPLES.md
- [x] 5.11 Add git hook integration template to EXAMPLES.md
- [x] 5.12 Add CI/CD integration examples to EXAMPLES.md

## 6. Configuration Files

- [x] 6.1 Verify `dagger.json` has correct engine version (v0.19.2+)
- [x] 6.2 Verify `pyproject.toml` uses `uv_build` backend
- [x] 6.3 Verify `pyproject.toml` project name is "main"
- [x] 6.4 Verify `pyproject.toml` includes dagger-io dependency with local SDK path
- [x] 6.5 Verify `.gitignore` includes `/sdk/`, `__pycache__/`, `*.pyc`, etc.

## 7. Validation and Testing

- [x] 7.1 Run `dagger develop` to generate SDK
- [x] 7.2 Run `dagger functions` to verify all functions are exposed
- [x] 7.3 Test `get_version()` with sample project
- [x] 7.4 Test `sync_version()` with Ansible collection
- [x] 7.5 Test `validate_version()` with mismatch scenario
- [x] 7.6 Test `bump_version()` with all bump types
- [x] 7.7 Test `release()` workflow end-to-end
- [x] 7.8 Verify error messages are clear and actionable
- [x] 7.9 Verify custom patterns work (pyproject.toml, Dockerfile)
- [x] 7.10 Run all unit and integration tests

## 8. Final Checks

- [x] 8.1 Verify module can be installed via `dagger install` from git URL
- [x] 8.2 Verify module works when called from another project
- [x] 8.3 Verify all success criteria from OPENSPEC_PROMPT.MD are met
- [x] 8.4 Run linter/formatter (black, isort, etc.) if applicable
- [x] 8.5 Review all documentation for accuracy and completeness
- [ ] 8.6 Tag initial release as v1.0.0 (after implementation is complete)

## Dependencies

- **Sequential**: Tasks 1.x must complete before 2.x
- **Parallel**: Tasks 4.x (Testing) can run alongside 5.x (Documentation)
- **Validation**: Tasks 7.x depend on 1.x-6.x being complete
- **Critical Path**: 1.x → 2.x → 3.x → 7.x → 8.x

## Notes

- All functions must use async/await pattern (Dagger requirement)
- Default to using `dag.current_module().source()` when `source` parameter is None
- Use `source.file("VERSION").contents()` for reading files
- Use `source.with_new_file()` for writing files
- Export updated directory to host with `await updated_source.export(".")`
- All output strings should use emoji indicators: ✅ (success), ⚠️ (warning), ❌ (error)