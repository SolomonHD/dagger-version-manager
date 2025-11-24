# Project Context

## Purpose

The Dagger Version Manager is a standalone, reusable Dagger module that solves the problem of maintaining consistent version numbers across multiple configuration files in software projects.

**Problem**: Many projects need to synchronize version numbers across multiple files:
- Ansible collections: `VERSION` file + `galaxy.yml`
- Python projects: `VERSION` + `pyproject.toml`
- Docker projects: `VERSION` + `Dockerfile` labels
- Kubernetes: `VERSION` + Helm `Chart.yaml`

**Solution**: A generic, installable Dagger module that:
- Uses a single source of truth (default: `VERSION` file)
- Synchronizes versions to target configuration files
- Validates version consistency
- Provides version bumping utilities (major, minor, patch)
- Supports git tagging workflows
- Works as a dependency in any project via `dagger install`

## Tech Stack

- **Dagger Python SDK** (v0.19.2+): Core functionality
- **Python 3.11+**: Implementation language
- **Semantic Versioning**: X.Y.Z version format
- **Regular Expressions**: Pattern matching for different file types

## Project Conventions

### Code Style

- **Language**: Python 3.11+
- **Async/Await**: All Dagger functions must be async
- **Type Annotations**: Use `Annotated[Type, Doc("description")]` for all parameters
- **Error Handling**: Clear, actionable error messages with helpful suggestions
- **Naming**: snake_case for functions, PascalCase for class name (`VersionManager`)
- **Docstrings**: Comprehensive docstrings for all public functions

### Architecture Patterns

- **Dagger Object Pattern**: Use `@object_type` class with `@function` methods
- **Default Parameters**: Sensible defaults for common use cases (e.g., `VERSION`, `galaxy.yml`)
- **Directory Handling**: Default to `dag.current_module().source()` when `source` parameter is None
- **File Operations**: Use `source.file().contents()` for reading, `source.with_new_file()` for writing
- **Validation First**: Validate inputs before making any changes
- **Atomic Operations**: No partial writes; complete operation or fail cleanly

### Testing Strategy

- **Unit Tests**: Test version parsing, bumping, validation logic
- **Integration Tests**: Test with real project fixtures (Ansible, Python, Docker)
- **Validation Tests**: Ensure semver format enforcement
- **Error Cases**: Test file not found, invalid format, pattern mismatch scenarios

### Git Workflow

- **No Git Operations**: Module suggests git commands but never executes them (security constraint)
- **Tag Format**: Suggest `v{version}` format for git tags (e.g., `v1.2.0`)
- **Release Workflow**: Provide complete copy-paste commands for users

## Domain Context

### Semantic Versioning (SemVer)

This module strictly enforces semantic versioning `X.Y.Z` format where:
- **X** (major): Breaking changes
- **Y** (minor): New features (backward compatible)
- **Z** (patch): Bug fixes (backward compatible)

### Version Bumping Rules

- **Major bump**: 1.2.3 → 2.0.0 (resets minor and patch to 0)
- **Minor bump**: 1.2.3 → 1.3.0 (resets patch to 0)
- **Patch bump**: 1.2.3 → 1.2.4 (increments patch only)

### File Pattern Examples

Different file types have different version line formats:
- **YAML** (galaxy.yml): `version: 1.2.0`
- **TOML** (pyproject.toml): `version = "1.2.0"`
- **Dockerfile**: `LABEL version="1.2.0"`
- **Helm Chart.yaml**: `version: 1.2.0`

The module uses regex patterns to match and replace these lines.

## Important Constraints

### Security Constraints

- **No Git Execution**: Module MUST NOT execute git commands directly
- **No File System Side Effects**: Only operate on files passed as `Directory` objects
- **Container Environment**: Must work in Dagger's containerized environment
- **No Local Dependencies**: Cannot rely on tools installed on host system

### Technical Constraints

- **Dagger Dependency**: Must be installable via `dagger install github.com/org/repo@version`
- **Python SDK Only**: No mixing with other language SDKs
- **Semver Only**: No support for CalVer, build numbers, or pre-release versions in V1
- **Single File Operations**: V1 syncs one target file per call (no batch operations)
- **Read-Only Git**: Can read VERSION file but cannot commit, tag, or push

### Usability Constraints

- **Clear Output**: All functions return human-readable strings with emojis (✅/⚠️/❌)
- **Helpful Errors**: Error messages must suggest solutions
- **Copy-Paste Ready**: Git commands must be ready to run without modification
- **Defaults for Common Cases**: Ansible collections work without any parameters

## External Dependencies

### Required

- **Dagger Engine**: v0.19.2 or higher
- **Python Runtime**: 3.11+ (provided by Dagger container)
- **dagger-io SDK**: Provided via local `sdk/` directory

### Optional (User Environments)

- **Git**: User's environment (for manual tag/push operations)
- **Target Project Files**: VERSION, galaxy.yml, pyproject.toml, etc.

## Module Installation Pattern

Users install this module in their projects:

```bash
# In their project directory
dagger install github.com/yourorg/dagger-version-manager@main

# Then call functions
dagger call version-manager sync-version
dagger call version-manager bump-version --bump-type=minor
```

## V1 Scope (Out of Scope)

**Not included in initial version:**
- Multi-file sync in single operation
- Changelog generation
- GitHub/GitLab release automation
- Pre-release versions (1.0.0-alpha.1)
- Build metadata (1.0.0+20130313144700)
- Configuration file (`.version-manager.yaml`)
- Dry-run mode
- Rollback capabilities
- Version history tracking
