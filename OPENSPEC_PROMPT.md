# OpenSpec change prompt

## Context

The `dagger-version-manager` module has three issues to address:

1. **Wrong directory bug**: When installed as a dependency and called without explicit `--source` parameter, the module reads from its own directory instead of the caller's project directory
2. **Missing VERSION file handling**: Error messages exist but need verification they're clear
3. **Version bump**: Update module version from 1.0.3 to 1.1.0 and update all documentation examples

## Goal

Fix the directory resolution bug so the module correctly reads from the caller's project when used as an installed dependency, ensure clear error messages for missing VERSION files, and bump the module version with documentation updates.

## Scope

### In scope:
- Modify [`src/main/__init__.py`](src/main/__init__.py) `_get_source()` method to use correct default directory
- Review and improve error messages for missing VERSION file scenarios
- Update [`VERSION`](VERSION) file from `1.0.3` to `1.1.0`
- Update version references in [`README.md`](README.md) from `v1.0.3` to `v1.1.0`
- Update version references in [`EXAMPLES.md`](EXAMPLES.md) from `v1.0.3` to `v1.1.0`

### Out of scope:
- Changes to function signatures or parameters
- New features or functionality
- Changes to pyproject.toml (stays at `version = "0.0.0"` per Dagger module standards)
- Test file modifications beyond fixing broken assertions

## Desired behaviour

**After the fix:**

1. When a user installs the module and runs:
   ```bash
   dagger call -m version-manager get-version
   ```
   The module should read `VERSION` from **the caller's project directory**, not from the version-manager module's own directory.

2. When VERSION file is missing, display clear error:
   ```
   ❌ Failed to read VERSION: <error details>
      Create a VERSION file with format X.Y.Z (e.g., 1.0.0)
   ```

3. All documentation examples reference `v1.1.0` instead of `v1.0.3`

## Constraints & assumptions

- Assume the Dagger context provides a way to get the caller's directory (not the current module's source)
- Assume semantic versioning (X.Y.Z only, no pre-release tags)
- Assume VERSION file should contain just the version string with no prefix
- Assume pyproject.toml stays at `version = "0.0.0"` (Dagger module standard)
- Maintain backward compatibility: functions should still accept explicit `source` parameter

## Acceptance criteria

- [ ] Module correctly reads VERSION from caller's project when installed as dependency
- [ ] Clear error message when VERSION file is missing or unreadable
- [ ] VERSION file updated to `1.1.0`
- [ ] All `v1.0.3` references in README.md changed to `v1.1.0`
- [ ] All `v1.0.3` references in EXAMPLES.md changed to `v1.1.0`
- [ ] All existing functions still work with explicit `--source` parameter
- [ ] No changes to function signatures or public API