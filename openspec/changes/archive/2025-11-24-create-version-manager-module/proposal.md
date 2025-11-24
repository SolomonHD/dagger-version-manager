# Change: Create Version Manager Module

## Why

Projects frequently maintain version numbers in multiple configuration files (e.g., Ansible collections with `VERSION` and `galaxy.yml`, Python projects with `VERSION` and `pyproject.toml`). Manual synchronization is error-prone and tedious. This module provides automated, reliable version management as a reusable Dagger dependency that any project can install.

## What Changes

This creates a **new Dagger module from scratch** that provides:

- **Version Synchronization**: Read from single source file (default: `VERSION`) and sync to target files via regex patterns
- **Version Validation**: Check consistency across files with clear mismatch reporting
- **Version Retrieval**: Simple getter for current version
- **Version Bumping**: Increment major, minor, or patch components following semantic versioning rules
- **Release Workflow**: Orchestrate sync + validate + git tag command generation

The module will be installable via `dagger install` and usable in any project.

**Core Functions:**
- `sync_version()` - Sync VERSION to target file using configurable pattern
- `validate_version()` - Check version consistency across files
- `get_version()` - Return current version string
- `bump_version()` - Increment version (major|minor|patch)
- `release()` - Complete release workflow with git command suggestions

## Impact

**Affected specs:**
- `version-management` (NEW) - Core version management capability

**Affected code:**
- `src/main/__init__.py` (NEW) - Module implementation
- `dagger.json` (UPDATE) - Add SDK configuration
- `pyproject.toml` (NEW) - Python dependencies
- `.gitignore` (NEW) - Ignore generated SDK
- `README.md` (UPDATE) - Usage documentation
- `EXAMPLES.md` (NEW) - Comprehensive usage examples

**Breaking changes:** None (net-new module)

**Dependencies:**
- Dagger Engine v0.19.2+
- Python 3.11+
- dagger-io SDK (auto-generated in `sdk/`)

**Migration:** N/A (new module, no migration needed)