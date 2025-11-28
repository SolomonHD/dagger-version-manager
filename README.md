# Dagger Version Manager

Automated version synchronization for multi-file projects using Dagger.

## Problem Statement

Many projects maintain version numbers across multiple configuration files:
- **Ansible collections**: `VERSION` + `galaxy.yml`
- **Python projects**: `VERSION` + `pyproject.toml`
- **Docker projects**: `VERSION` + `Dockerfile` labels
- **Kubernetes**: `VERSION` + Helm `Chart.yaml`
- **Packer plugins**: `version/VERSION` + other config files

Manually keeping these in sync is tedious and error-prone. This Dagger module automates the process.

## Features

- ✅ **Version Synchronization**: Sync from single source file to target files
- ✅ **Version Validation**: Check consistency across files
- ✅ **Version Retrieval**: Get current version
- ✅ **Version Bumping**: Increment major, minor, or patch components
- ✅ **Release Workflow**: Complete release automation with git command generation
- ✅ **Flexible Patterns**: Custom regex patterns for any file format
- ✅ **Semantic Versioning**: Strict X.Y.Z format enforcement
- ✅ **Auto-Detection**: Automatically finds VERSION file at root or in `version/` subdirectory

## Installation

Install this module in your project:

```bash
dagger install github.com/SolomonHD/dagger-version-manager@main
```

Or install a specific version:

```bash
dagger install github.com/SolomonHD/dagger-version-manager@v1.2.0
```

## Quick Start

> **Important:** The `--source=.` parameter is **required** for all module functions to specify your project directory. This ensures the module always operates on the correct files.

> **Note:** These examples assume you've installed the module in your project using `dagger install`. If you're developing locally within this repository, omit the `-m version-manager` flag. For remote usage without installation, use the full GitHub URL pattern (see [EXAMPLES.md](EXAMPLES.md) for details).

### VERSION File Auto-Detection

The module automatically detects your VERSION file location:
- Checks `./VERSION` (project root) first
- Falls back to `./version/VERSION` (Packer plugin convention)
- Returns an error if both exist (you must specify which one to use)
- Returns an error if neither exists

### 1. Get Current Version

```bash
dagger call -m version-manager get-version --source=.
# Output: 1.2.3
# Works with VERSION at root OR version/VERSION
```

### 2. Sync Version to Target File

```bash
# Sync VERSION to galaxy.yml (default)
dagger call -m version-manager sync-version --source=. export --path=.

# Sync to custom file with custom pattern
dagger call -m version-manager sync-version \
  --source=. \
  --target-file=pyproject.toml \
  --version-pattern='^version\s*=\s*".*"' \
  export --path=.
```

### 3. Validate Version Consistency

```bash
dagger call -m version-manager validate-version --source=.
# Output: ✅ Version 1.2.3 is consistent
# Or: ⚠️  Mismatch: VERSION=1.2.3, galaxy.yml=1.0.0
```

### 4. Bump Version

```bash
# Bump patch: 1.2.3 → 1.2.4
dagger call -m version-manager bump-version --source=. --bump-type=patch export --path=.
```

### 5. Complete Release Workflow

```bash
dagger call -m version-manager release --source=.
```

Output:
```
🚀 Release 1.2.3 Ready

✅ Synced 1.2.3 → galaxy.yml
✅ Version 1.2.3 is consistent

Next steps (run these commands manually):

  git add VERSION galaxy.yml
  git commit -m "Release 1.2.3"
  git tag -a v1.2.3 -m "Release 1.2.3"
  git push && git push --tags

Note: Review changes before committing!
```

## Usage Contexts

The Dagger Version Manager can be called in three different ways depending on your context:

### Context A: Local Development
When working **inside** the dagger-version-manager repository:
```bash
dagger call get-version --source=.
dagger call sync-version --source=. export --path=.
```
No `-m` flag needed, but `--source=.` is still required.

### Context B: Installed Module
After installing in another project with `dagger install`:
```bash
dagger call -m version-manager get-version --source=.
dagger call -m version-manager sync-version --source=. export --path=.
```
Use `-m version-manager` (the module name from [`dagger.json`](dagger.json)) and `--source=.` to specify your project directory.

### Context C: Remote Module
Calling directly without installation:
```bash
dagger call -m github.com/SolomonHD/dagger-version-manager@v1.2.0 version-manager get-version --source=.
```
Use `-m <repo-url>@<version> <module-name>` pattern with `--source=.`.

## Documentation

For comprehensive examples, function reference, and advanced workflows (including CI/CD integration and git hooks), please see [EXAMPLES.md](EXAMPLES.md).

- [Ansible Collection Examples](EXAMPLES.md#ansible-collection)
- [Python Project Examples](EXAMPLES.md#python-project)
- [Docker Project Examples](EXAMPLES.md#docker-project)
- [Kubernetes/Helm Examples](EXAMPLES.md#kubernetes-helm-project)
- [CI/CD Integration](EXAMPLES.md#cicd-integration)
- [Git Hooks Setup](EXAMPLES.md#git-hooks-setup-automated)
- [Function Reference](EXAMPLES.md#function-reference)

## Requirements

- **Dagger Engine**: v0.19.7 or higher
- **Python**: 3.11+ (provided by Dagger container)
- **Git**: Only needed on your machine for manual tag operations

## VERSION File Locations

The module supports two standard VERSION file locations:

| Location | Project Type | Example |
|----------|-------------|---------|
| `./VERSION` | Most projects | Ansible collections, Python packages |
| `./version/VERSION` | Packer plugins | HashiCorp Packer plugins |

When both files exist, you must explicitly specify which to use:
```bash
dagger call -m version-manager get-version --source=. --version-file=VERSION
dagger call -m version-manager get-version --source=. --version-file=version/VERSION
```

## Version Format

This module strictly enforces **semantic versioning** (X.Y.Z):
- **X** (major): Breaking changes
- **Y** (minor): New features (backward compatible)
- **Z** (patch): Bug fixes (backward compatible)

**Supported:** `1.0.0`, `10.20.30`, `999.999.999`  
**Not supported:** `v1.0.0`, `1.0`, `1.0.0-alpha`, `1.0.0+build`

## Security

This module **does not execute git commands**. It only:
- Reads files from Dagger directory containers
- Writes files to Dagger directory containers
- Generates git command strings for manual execution

You maintain full control over git operations.

## License

MIT License

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/SolomonHD/dagger-version-manager/issues)
- **Documentation**: [EXAMPLES.md](EXAMPLES.md)
- **Discussions**: [GitHub Discussions](https://github.com/SolomonHD/dagger-version-manager/discussions)
