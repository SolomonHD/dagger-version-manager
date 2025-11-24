# Dagger Version Manager - Examples & Reference

Comprehensive usage examples, function reference, and troubleshooting guide.

## Table of Contents

- [Ansible Collection](#ansible-collection)
- [Python Project](#python-project)
- [Docker Project](#docker-project)
- [Kubernetes/Helm](#kubernetes-helm-project)
- [CI/CD Integration](#cicd-integration)
- [Git Hooks](#git-hooks-setup-automated)
- [Advanced Workflows](#advanced-workflows)
- [Function Reference](#function-reference)
- [Troubleshooting](#troubleshooting)

---

## Ansible Collection

### Project Structure

```
my-collection/
├── VERSION          # 1.2.3
├── galaxy.yml       # version: 1.0.0 (out of sync)
├── plugins/
└── roles/
```

### Sync and Release

```bash
# 1. Check current version
dagger call -m version-manager get-version
# Output: 1.2.3

# 2. Validate consistency
dagger call -m version-manager validate-version
# Output: ⚠️  Mismatch: VERSION=1.2.3, galaxy.yml=1.0.0

# 3. Sync version to galaxy.yml
dagger call -m version-manager sync-version export --path=.
# Updates galaxy.yml to version: 1.2.3

# 4. Validate again
dagger call -m version-manager validate-version
# Output: ✅ Version 1.2.3 is consistent

# 5. Complete release
dagger call -m version-manager release
```

### Bump and Release Workflow

```bash
# Bump patch version
dagger call -m version-manager bump-version --bump-type=patch export --path=.
# VERSION: 1.2.3 → 1.2.4

# Sync to galaxy.yml
dagger call -m version-manager sync-version export --path=.

# Run release workflow
dagger call -m version-manager release

# Follow the generated git commands
git add VERSION galaxy.yml
git commit -m "Release 1.2.4"
git tag -a v1.2.4 -m "Release 1.2.4"
git push && git push --tags
```

---

## Python Project

### Project Structure

```
my-package/
├── VERSION              # 2.0.5
├── pyproject.toml       # version = "1.5.0" (out of sync)
├── src/
└── tests/
```

### Custom Pattern for pyproject.toml

```bash
# Set up custom pattern
PATTERN='^version\s*=\s*".*"'

# 1. Check current version
dagger call -m version-manager get-version
# Output: 2.0.5

# 2. Sync to pyproject.toml
dagger call -m version-manager sync-version \
  --target-file=pyproject.toml \
  --version-pattern="$PATTERN" \
  export --path=.

# 3. Validate
dagger call -m version-manager validate-version \
  --target-file=pyproject.toml \
  --version-pattern="$PATTERN"
# Output: ✅ Version 2.0.5 is consistent
```

### Complete Python Release

```bash
# Bump minor version for new features
dagger call -m version-manager bump-version --bump-type=minor export --path=.
# VERSION: 2.0.5 → 2.1.0

# Sync to pyproject.toml
dagger call -m version-manager sync-version \
  --target-file=pyproject.toml \
  --version-pattern='^version\s*=\s*".*"' \
  export --path=.

# Run release with custom message
dagger call -m version-manager release \
  --target-file=pyproject.toml \
  --version-pattern='^version\s*=\s*".*"' \
  --tag-message="Add new feature: async support"
```

---

## Docker Project

### Project Structure

```
my-app/
├── VERSION          # 3.0.1
├── Dockerfile       # LABEL version="2.9.0" (out of sync)
├── src/
└── docker-compose.yml
```

### Sync Dockerfile Version

```bash
# Custom pattern for Dockerfile LABEL
PATTERN='LABEL version=".*"'

# Sync VERSION to Dockerfile
dagger call -m version-manager sync-version \
  --target-file=Dockerfile \
  --version-pattern="$PATTERN" \
  export --path=.

# Validate
dagger call -m version-manager validate-version \
  --target-file=Dockerfile \
  --version-pattern="$PATTERN"
# Output: ✅ Version 3.0.1 is consistent
```

### Docker Release Workflow

```bash
# Bump patch for bug fix
dagger call -m version-manager bump-version --bump-type=patch export --path=.
# VERSION: 3.0.1 → 3.0.2

# Sync to Dockerfile
dagger call -m version-manager sync-version \
  --target-file=Dockerfile \
  --version-pattern='LABEL version=".*"' \
  export --path=.

# Build and tag Docker image
docker build -t myapp:3.0.2 .
docker build -t myapp:latest .

# Create git tag
git add VERSION Dockerfile
git commit -m "Release 3.0.2"
git tag -a v3.0.2 -m "Release 3.0.2"
git push && git push --tags

# Push Docker images
docker push myapp:3.0.2
docker push myapp:latest
```

---

## Kubernetes / Helm Project

### Project Structure

```
my-chart/
├── VERSION          # 1.5.0
├── Chart.yaml       # version: 1.4.0 (out of sync)
├── values.yaml
└── templates/
```

### Helm Chart Versioning

```bash
# Helm Chart.yaml uses YAML format like Ansible
# Default pattern works!

# Sync to Chart.yaml
dagger call -m version-manager sync-version \
  --target-file=Chart.yaml \
  export --path=.

# Validate
dagger call -m version-manager validate-version \
  --target-file=Chart.yaml
# Output: ✅ Version 1.5.0 is consistent
```

### Helm Release Workflow

```bash
# Bump version for new features
dagger call -m version-manager bump-version --bump-type=minor export --path=.
# VERSION: 1.5.0 → 1.6.0

# Sync to Chart.yaml
dagger call -m version-manager sync-version \
  --target-file=Chart.yaml \
  export --path=.

# Package and publish
helm package .
helm repo index .

# Git release
git add VERSION Chart.yaml
git commit -m "Release 1.6.0"
git tag -a v1.6.0 -m "Release 1.6.0"
git push && git push --tags
```

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches:
      - main
    paths:
      - 'VERSION'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Dagger
        run: |
          curl -fsSL https://dl.dagger.io/dagger/install.sh | sh
          sudo mv bin/dagger /usr/local/bin/
      
      - name: Get version
        id: version
        run: |
          VERSION=$(dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager get-version)
          echo "version=$VERSION" >> $GITHUB_OUTPUT
      
      - name: Validate version consistency
        run: |
          dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager validate-version
      
      - name: Sync version to all files
        run: |
          dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager sync-version export --path=.
          dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager sync-version \
            --target-file=pyproject.toml \
            --version-pattern='^version\s*=\s*".*"' \
            export --path=.
      
      - name: Create git tag
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add VERSION galaxy.yml pyproject.toml
          git commit -m "Release ${{ steps.version.outputs.version }}" || true
          git tag -a v${{ steps.version.outputs.version }} \
            -m "Release ${{ steps.version.outputs.version }}"
          git push --follow-tags
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
release:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add curl bash
    - curl -fsSL https://dl.dagger.io/dagger/install.sh | sh
    - mv bin/dagger /usr/local/bin/
  script:
    - VERSION=$(dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager get-version)
    - echo "Releasing version $VERSION"
    - dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager validate-version
    - dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager sync-version export --path=.
    - |
      git config user.name "gitlab-ci"
      git config user.email "gitlab-ci@gitlab.com"
      git add VERSION galaxy.yml
      git commit -m "Release $VERSION"
      git tag -a v$VERSION -m "Release $VERSION"
      git push --follow-tags
  only:
    - main
  when: manual
```

### Jenkins Pipeline

Create `Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Install Dagger') {
            steps {
                sh '''
                    curl -fsSL https://dl.dagger.io/dagger/install.sh | sh
                    sudo mv bin/dagger /usr/local/bin/
                '''
            }
        }
        
        stage('Get Version') {
            steps {
                script {
                    env.VERSION = sh(
                        script: 'dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager get-version',
                        returnStdout: true
                    ).trim()
                    echo "Version: ${env.VERSION}"
                }
            }
        }
        
        stage('Validate') {
            steps {
                sh 'dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager validate-version'
            }
        }
        
        stage('Sync Version') {
            steps {
                sh 'dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager sync-version export --path=.'
            }
        }
        
        stage('Create Release') {
            steps {
                sh """
                    git config user.name "Jenkins"
                    git config user.email "jenkins@example.com"
                    git add VERSION galaxy.yml
                    git commit -m "Release ${env.VERSION}"
                    git tag -a v${env.VERSION} -m "Release ${env.VERSION}"
                    git push --follow-tags
                """
            }
        }
    }
}
```

---

## Git Hooks Setup (Automated)

### Quick Setup (Remote Module)

To install hooks in any project without cloning this repo:

```bash
dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 \
  setup-git-hooks --source=. export --path=.
```

### Quick Setup (Local Module)

If you have the module locally:

```bash
# Automatically detect project type and install hooks
dagger call setup-git-hooks --source=. export --path=.
```

This will:
1. Detect your project type (Ansible, Python, Docker, or Helm)
2. Create pre-commit and pre-push hooks in `.git/hooks/`
3. Configure validation commands for your project type
4. Set proper executable permissions

### Project Type Detection

The function automatically detects your project type:

```bash
# Ansible Collection (galaxy.yml present)
cd my-ansible-collection/
dagger call setup-git-hooks --source=. export --path=.
# Creates hooks validating VERSION ↔ galaxy.yml

# Python Project (pyproject.toml present)
cd my-python-package/
dagger call setup-git-hooks --source=. export --path=.
# Creates hooks validating VERSION ↔ pyproject.toml

# Docker Project (Dockerfile present)
cd my-docker-app/
dagger call setup-git-hooks --source=. export --path=.
# Creates hooks validating VERSION ↔ Dockerfile

# Helm Chart (Chart.yaml present)
cd my-helm-chart/
dagger call setup-git-hooks --source=. export --path=.
# Creates hooks validating VERSION ↔ Chart.yaml
```

### Verifying Installation

Check that hooks were created:

```bash
ls -la .git/hooks/ | grep -E "pre-commit|pre-push"
# Output:
# -rwxr-xr-x 1 user user  579 Nov 24 15:17 pre-commit
# -rwxr-xr-x 1 user user  577 Nov 24 15:17 pre-push
```

View hook content:

```bash
head .git/hooks/pre-commit
# Output:
# #!/bin/bash
# # DAGGER-VERSION-MANAGER: v1.0.1
# # Installed: 2025-11-24T20:17:01.345087Z
# #
# # This hook validates version consistency before pre commit.
# # Managed by Dagger Version Manager - DO NOT EDIT MANUALLY
```

### Testing Hooks

Test the pre-commit hook:

```bash
# Create version mismatch
echo "1.2.3" > VERSION
# galaxy.yml still has version: 1.0.0

# Try to commit
git add VERSION
git commit -m "Update version"
# Output:
# Checking version consistency...
# ❌ Version mismatch detected!
# Run: dagger call version-manager sync-version export --path=.
```

Fix and retry:

```bash
# Sync versions
dagger call version-manager sync-version export --path=.

# Now commit succeeds
git add VERSION galaxy.yml
git commit -m "Release 1.2.3"
# Output:
# Checking version consistency...
# ✅ Version check passed
# [main abc1234] Release 1.2.3
```

### Hook Behavior

**Pre-commit Hook:**
- Runs before `git commit`
- Validates version consistency
- Blocks commit if versions don't match
- Provides sync command to fix issues

**Pre-push Hook:**
- Runs before `git push`
- Same validation as pre-commit
- Prevents pushing inconsistent versions
- Last line of defense before publishing

### Updating Hooks

Re-run setup to update existing hooks:

```bash
# Hooks are tracked by metadata marker
# Running setup again will update them
dagger call setup-git-hooks --source=. export --path=.
```

The function will:
- Update hooks that have `# DAGGER-VERSION-MANAGER:` marker
- Preserve hooks without the marker (won't overwrite)
- Update metadata with new version and timestamp

---

## Git Hooks Integration (Manual)

### Pre-commit Hook (Manual Setup)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Validate version consistency before commit
echo "Checking version consistency..."

if ! dagger call -m version-manager validate-version 2>&1 | grep -q "✅"; then
    echo "❌ Version mismatch detected!"
    echo "Run: dagger call -m version-manager sync-version export --path=."
    exit 1
fi

echo "✅ Version check passed"
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Pre-push Hook

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash

# Check if VERSION file changed
if git diff --name-only HEAD @{u} 2>/dev/null | grep -q "^VERSION$"; then
    echo "VERSION file changed, running validation..."
    
    if ! dagger call -m version-manager validate-version 2>&1 | grep -q "✅"; then
        echo "❌ Version mismatch detected!"
        echo "Versions must be synchronized before pushing."
        exit 1
    fi
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-push
```

---

## Advanced Workflows

### Multi-File Sync

Sync version to multiple files in sequence:

```bash
#!/bin/bash

VERSION=$(dagger call -m version-manager get-version)
echo "Syncing version $VERSION to all files..."

# Sync to Ansible galaxy.yml
dagger call -m version-manager sync-version \
  --target-file=galaxy.yml \
  export --path=.

# Sync to Python pyproject.toml
dagger call -m version-manager sync-version \
  --target-file=pyproject.toml \
  --version-pattern='^version\s*=\s*".*"' \
  export --path=.

# Sync to Helm Chart.yaml
dagger call -m version-manager sync-version \
  --target-file=Chart.yaml \
  export --path=.

# Sync to Dockerfile
dagger call -m version-manager sync-version \
  --target-file=Dockerfile \
  --version-pattern='LABEL version=".*"' \
  export --path=.

echo "✅ All files synced to version $VERSION"
```

### Automated Patch Releases

Script for automated patch releases with CI:

```bash
#!/bin/bash
set -e

echo "Starting automated patch release..."

# Bump patch version
dagger call -m version-manager bump-version --bump-type=patch export --path=.

# Get new version
NEW_VERSION=$(dagger call -m version-manager get-version)
echo "New version: $NEW_VERSION"

# Sync to all target files
dagger call -m version-manager sync-version export --path=.

# Validate
if ! dagger call -m version-manager validate-version | grep -q "✅"; then
    echo "❌ Validation failed!"
    exit 1
fi

# Create git release
git add VERSION galaxy.yml
git commit -m "Automated patch release $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Automated patch release $NEW_VERSION"
git push && git push --tags

echo "✅ Release $NEW_VERSION complete!"
```

### Version Comparison Script

```bash
#!/bin/bash

# Compare versions across multiple files
echo "Version Consistency Report"
echo "=========================="

VERSION_FILE=$(dagger call -m version-manager get-version)
echo "VERSION file:      $VERSION_FILE"

# Check galaxy.yml
GALAXY=$(grep "^version:" galaxy.yml | awk '{print $2}')
echo "galaxy.yml:        $GALAXY"

# Check pyproject.toml
PYPROJECT=$(grep "^version = " pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
echo "pyproject.toml:    $PYPROJECT"

# Check all match
if [ "$VERSION_FILE" = "$GALAXY" ] && [ "$VERSION_FILE" = "$PYPROJECT" ]; then
    echo ""
    echo "✅ All versions match: $VERSION_FILE"
    exit 0
else
    echo ""
    echo "❌ Version mismatch detected!"
    echo "Run: dagger call -m version-manager sync-version export --path=."
    exit 1
fi
```

### Makefiles Integration

Create `Makefile`:

```makefile
.PHONY: version validate sync bump-patch bump-minor bump-major release

version:
	@dagger call -m version-manager get-version

validate:
	@dagger call -m version-manager validate-version

sync:
	@dagger call -m version-manager sync-version export --path=.

bump-patch:
	@dagger call -m version-manager bump-version --bump-type=patch export --path=.
	@$(MAKE) sync

bump-minor:
	@dagger call -m version-manager bump-version --bump-type=minor export --path=.
	@$(MAKE) sync

bump-major:
	@dagger call -m version-manager bump-version --bump-type=major export --path=.
	@$(MAKE) sync

release:
	@dagger call -m version-manager release

help:
	@echo "Dagger Version Manager Make Targets:"
	@echo "  version      - Show current version"
	@echo "  validate     - Validate version consistency"
	@echo "  sync         - Sync VERSION to target files"
	@echo "  bump-patch   - Bump patch version and sync"
	@echo "  bump-minor   - Bump minor version and sync"
	@echo "  bump-major   - Bump major version and sync"
	@echo "  release      - Complete release workflow"
```

Usage:
```bash
make version
make validate
make bump-patch
make release
```

---

## Function Reference

### `get-version`

Read the current version from the version file.

**Parameters:**
- `--source` (optional): Source directory (defaults to current module)
- `--version-file` (optional): Version file name (default: `VERSION`)

**Example:**
```bash
dagger call version-manager get-version
dagger call version-manager get-version --version-file=MY_VERSION
```

### `validate-version`

Check if version in source file matches target file.

**Parameters:**
- `--source` (optional): Source directory
- `--version-file` (optional): Source version file (default: `VERSION`)
- `--target-file` (optional): Target file to check (default: `galaxy.yml`)
- `--version-pattern` (optional): Regex pattern to match version line (default: `r'^version:.*$'`)

**Example:**
```bash
dagger call version-manager validate-version
dagger call version-manager validate-version \
  --target-file=pyproject.toml \
  --version-pattern='^version\s*=\s*".*"'
```

### `sync-version`

Synchronize version from source to target file.

**Parameters:**
- `--source` (optional): Source directory
- `--version-file` (optional): Source version file (default: `VERSION`)
- `--target-file` (optional): Target file to update (default: `galaxy.yml`)
- `--version-pattern` (optional): Regex pattern to match version line (default: `r'^version:.*$'`)

**Example:**
```bash
dagger call version-manager sync-version export --path=.
dagger call version-manager sync-version \
  --target-file=Dockerfile \
  --version-pattern='LABEL version=".*"' \
  export --path=.
```

**Note:** Must use `export --path=.` to write changes back to your filesystem.

### `bump-version`

Increment version according to semantic versioning rules.

**Parameters:**
- `--bump-type` (required): Type of bump: `major`, `minor`, or `patch`
- `--source` (optional): Source directory
- `--version-file` (optional): Version file to update (default: `VERSION`)

**Examples:**
```bash
# Patch: 1.2.3 → 1.2.4
dagger call version-manager bump-version --bump-type=patch export --path=.

# Minor: 1.2.3 → 1.3.0
dagger call version-manager bump-version --bump-type=minor export --path=.

# Major: 1.2.3 → 2.0.0
dagger call version-manager bump-version --bump-type=major export --path=.
```

**Note:** Must use `export --path=.` to write changes back to your filesystem.

### `setup-git-hooks`

Install git hooks for automated version validation.

**Parameters:**
- `--source` (optional): Source directory (defaults to current module)

**Example:**
```bash
dagger call setup-git-hooks --source=. export --path=.
```

**How it works:**
1. Detects project type (Ansible, Python, Docker, or Helm) based on marker files
2. Creates pre-commit and pre-push hooks in `.git/hooks/`
3. Configures hooks with appropriate validation commands for your project type
4. Hooks will block commits/pushes if versions are inconsistent

**Project Type Detection:**
- **Ansible Collection**: Looks for `galaxy.yml`
- **Python**: Looks for `pyproject.toml`
- **Helm**: Looks for `Chart.yaml`
- **Docker**: Looks for `Dockerfile`

**Hook Behavior:**
- Hooks run validation before commit/push operations
- Display error messages if versions don't match
- Suggest sync commands to fix mismatches
- Exit with non-zero status to block the operation

**Note:** Hooks are marked with metadata headers (`# DAGGER-VERSION-MANAGER: v{version}`) for tracking and safe updates. Existing hooks without this marker are preserved and not overwritten.

### `release`

Complete release workflow with git command generation.

**Parameters:**
- `--source` (optional): Source directory
- `--version-file` (optional): Source version file (default: `VERSION`)
- `--target-file` (optional): Target file to sync (default: `galaxy.yml`)
- `--version-pattern` (optional): Regex pattern
- `--tag-message` (optional): Custom git tag message

**Example:**
```bash
dagger call version-manager release
dagger call version-manager release \
  --tag-message="Major release with breaking changes"
```

---

## Tips and Best Practices

### 1. Always Validate After Manual Edits

```bash
# After editing VERSION file
dagger call version-manager validate-version
dagger call version-manager sync-version export --path=.
```

### 2. Use Release Function for Tags

The `release` function generates correct git commands:
```bash
dagger call version-manager release
# Copy and execute the provided git commands
```

### 3. Custom VERSION File Location

```bash
# If your VERSION file is named differently
dagger call version-manager get-version --version-file=MY_VERSION
```

### 4. Test Patterns First

```bash
# Test your custom pattern with validate
dagger call version-manager validate-version \
  --target-file=myfile.conf \
  --version-pattern='^APP_VERSION=.*$'
```

### 5. Chain Operations in Scripts

```bash
# Complete workflow in one script
dagger call version-manager bump-version --bump-type=minor export --path=. && \
dagger call version-manager sync-version export --path=. && \
dagger call version-manager validate-version
```

---

## Troubleshooting

### Error: "Failed to read VERSION"

**Cause:** VERSION file doesn't exist or isn't in the expected location.

**Solution:** Create a VERSION file in your project root:
```bash
echo "1.0.0" > VERSION
```

### Error: "Invalid version format"

**Cause:** Version doesn't follow semantic versioning (X.Y.Z).

**Solution:** Ensure VERSION file contains exactly three numeric components:
```bash
# ✅ Valid
1.0.0
10.20.30

# ❌ Invalid
1.0
v1.0.0
1.0.0-alpha
```

### Error: "Pattern not found in target file"

**Cause:** The regex pattern doesn't match any line in the target file.

**Solution:** Verify the pattern matches your file format. Common patterns:
- YAML: `r'^version:.*$'`
- TOML: `r'^version\s*=\s*".*"$'`
- Dockerfile: `r'LABEL version=".*"$'`

### Warning: "Mismatch: VERSION=X, target=Y"

**Cause:** Version files are out of sync.

**Solution:** Run sync to update:
```bash
dagger call version-manager sync-version export --path=.
```

### Pattern Not Matching

If you get pattern errors, inspect your file:

```bash
# Show line that should match
grep -n "version" myfile.yml

# Test with simpler pattern first
dagger call version-manager validate-version \
  --version-pattern='version'
```

### Multiple Version Lines

If file has multiple version lines, the pattern matches the first occurrence:

```yaml
# In Chart.yaml
apiVersion: v2
version: 1.0.0        # This line will be matched
appVersion: "1.0"     # This line is ignored
```

### Files Not Exporting

Always use `export --path=.` to write changes:

```bash
# ❌ Wrong - changes stay in container
dagger call version-manager sync-version

# ✅ Correct - changes written to filesystem
dagger call version-manager sync-version export --path=.