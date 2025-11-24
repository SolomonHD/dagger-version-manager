# Change: Fix source directory resolution and bump version to 1.1.0

## Why

When the `dagger-version-manager` module is installed as a dependency in another project and called without an explicit `--source` parameter, it incorrectly reads from its own module directory instead of the caller's project directory. This breaks the intended behavior where it should operate on the consuming project's files. Additionally, the module version needs to be bumped to 1.1.0 to reflect these fixes, and all documentation examples need updating.

## What Changes

- Fix `_get_source()` method in [`src/main/__init__.py`](../../src/main/__init__.py:20-32) to use caller's directory instead of module's own source
- Verify error messages for missing VERSION file are clear and actionable
- Update [`VERSION`](../../VERSION) file from `1.0.3` to `1.1.0`
- Update all `v1.0.3` version references in [`README.md`](../../README.md) to `v1.1.0`
- Update all `v1.0.3` version references in [`EXAMPLES.md`](../../EXAMPLES.md) to `v1.1.0`

## Impact

- Affected specs: `version-management`
- Affected code: [`src/main/__init__.py`](../../src/main/__init__.py), [`VERSION`](../../VERSION), [`README.md`](../../README.md), [`EXAMPLES.md`](../../EXAMPLES.md)
- **BREAKING**: None - this fix restores the intended behavior
- Users who installed the module will now correctly operate on their project files
- Backward compatibility maintained: explicit `--source` parameter still works as before