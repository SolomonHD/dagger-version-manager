# Change: Add VERSION File Auto-Detection

## Why

The dagger-version-manager module currently requires users to specify `--version-file=version/VERSION` for projects that follow the Packer plugin convention of storing VERSION in a `version/` subdirectory. This creates friction for users who must remember the exact location.

By auto-detecting common VERSION file locations, the module becomes more user-friendly while maintaining backward compatibility for projects with explicit paths.

## What Changes

- **ADDED**: Auto-detection logic for VERSION file locations
  - Check both `VERSION` (root) and `version/VERSION`
  - Error if both files exist (ambiguity)
  - Use whichever file is found if only one exists
  - Clear error if neither file exists
- **MODIFIED**: `_read_version_file` helper to support auto-detection when default value is used
- Version bump to 1.2.0 for this feature release
- Documentation updates in README.md and EXAMPLES.md

## Impact

- **Affected specs**: `version-management`
- **Affected code**: 
  - `src/main/__init__.py` - new `_resolve_version_file()` method
  - All functions using `version_file` parameter (`get_version`, `validate_version`, `sync_version`, `bump_version`, `release`, `setup_git_hooks`)
- **Backward compatibility**: Fully maintained - explicit `--version-file` parameter always takes precedence

## Constraints

- Auto-detection only applies when `version_file` uses its default value (`"VERSION"`)
- Only two locations are supported: `VERSION` and `version/VERSION`
- Semantic versioning (X.Y.Z) format requirement unchanged
- The default parameter value remains `"VERSION"` in function signatures (for documentation purposes)