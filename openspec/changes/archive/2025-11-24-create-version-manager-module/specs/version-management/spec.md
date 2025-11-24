## ADDED Requirements

### Requirement: Version Source File Reading

The system SHALL read version numbers from a designated source file (default: `VERSION`) and validate the format as semantic versioning (X.Y.Z where X, Y, and Z are non-negative integers).

#### Scenario: Read valid version from VERSION file

- **WHEN** a `VERSION` file contains `1.2.3`
- **AND** get_version() is called
- **THEN** the system returns `"1.2.3"`

#### Scenario: Read version from custom source file

- **WHEN** a custom version file `MY_VERSION` contains `2.0.5`
- **AND** get_version(version_file="MY_VERSION") is called
- **THEN** the system returns `"2.0.5"`

#### Scenario: Reject invalid version format

- **WHEN** a `VERSION` file contains `1.2` (missing patch component)
- **AND** get_version() is called
- **THEN** the system returns an error message: `"❌ Invalid version format: 1.2 (expected X.Y.Z)"`

#### Scenario: Handle missing VERSION file

- **WHEN** the `VERSION` file does not exist
- **AND** get_version() is called
- **THEN** the system returns an error message indicating the file is missing
- **AND** suggests creating the file with a valid version

### Requirement: Version Synchronization

The system SHALL synchronize the version from a source file to target configuration files by matching a configurable regex pattern and replacing the matched line with the new version in the appropriate format.

#### Scenario: Sync to Ansible galaxy.yml with default pattern

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** `galaxy.yml` contains `version: 1.0.0`
- **AND** sync_version() is called with default parameters
- **THEN** the `galaxy.yml` file is updated to `version: 1.2.3`
- **AND** the system returns `"✅ Synced 1.2.3 → galaxy.yml"`

#### Scenario: Sync to Python pyproject.toml with custom pattern

- **WHEN** `VERSION` file contains `2.1.0`
- **AND** `pyproject.toml` contains `version = "1.5.0"`
- **AND** sync_version(target_file="pyproject.toml", version_pattern=r'^version\s*=\s*".*"') is called
- **THEN** the `pyproject.toml` file is updated to `version = "2.1.0"`
- **AND** the system returns `"✅ Synced 2.1.0 → pyproject.toml"`

#### Scenario: Sync to Dockerfile with LABEL pattern

- **WHEN** `VERSION` file contains `3.0.1`
- **AND** `Dockerfile` contains `LABEL version="2.9.0"`
- **AND** sync_version(target_file="Dockerfile", version_pattern=r'LABEL version=".*"') is called
- **THEN** the `Dockerfile` is updated to `LABEL version="3.0.1"`
- **AND** the system returns `"✅ Synced 3.0.1 → Dockerfile"`

#### Scenario: Handle target file not found

- **WHEN** `VERSION` file contains `1.0.0`
- **AND** target file `missing.yml` does not exist
- **AND** sync_version(target_file="missing.yml") is called
- **THEN** the system returns an error indicating the target file is not found
- **AND** suggests checking the file path

#### Scenario: Handle pattern not found in target

- **WHEN** `VERSION` file contains `1.0.0`
- **AND** `custom.conf` does not contain any line matching the pattern
- **AND** sync_version(target_file="custom.conf", version_pattern=r'^VERSION:.*$') is called
- **THEN** the system returns an error indicating pattern not matched
- **AND** suggests verifying the pattern or target file content

### Requirement: Version Validation

The system SHALL validate that the version in the source file matches the version in target configuration files and report consistency status or mismatches with actionable guidance.

#### Scenario: Versions match

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** `galaxy.yml` contains `version: 1.2.3`
- **AND** validate_version() is called
- **THEN** the system returns `"✅ Version 1.2.3 is consistent"`

#### Scenario: Versions mismatch

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** `galaxy.yml` contains `version: 1.1.0`
- **AND** validate_version() is called
- **THEN** the system returns `"⚠️  Mismatch: VERSION=1.2.3, galaxy.yml=1.1.0"`
- **AND** suggests running `dagger call version-manager sync-version`

#### Scenario: Invalid version in source

- **WHEN** `VERSION` file contains `invalid`
- **AND** validate_version() is called
- **THEN** the system returns an error indicating invalid version format
- **AND** the validation fails

#### Scenario: Validate custom target file

- **WHEN** `VERSION` file contains `2.0.0`
- **AND** `pyproject.toml` contains `version = "2.0.0"`
- **AND** validate_version(target_file="pyproject.toml") is called
- **THEN** the system returns `"✅ Version 2.0.0 is consistent"`

### Requirement: Version Bumping

The system SHALL increment version components (major, minor, or patch) according to semantic versioning rules, where major bumps reset minor and patch to 0, minor bumps reset patch to 0, and patch bumps increment only the patch component.

#### Scenario: Bump major version

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** bump_version(bump_type="major") is called
- **THEN** the `VERSION` file is updated to `2.0.0`
- **AND** the system returns `"✅ Bumped 1.2.3 → 2.0.0"`

#### Scenario: Bump minor version

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** bump_version(bump_type="minor") is called
- **THEN** the `VERSION` file is updated to `1.3.0`
- **AND** the system returns `"✅ Bumped 1.2.3 → 1.3.0"`

#### Scenario: Bump patch version

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** bump_version(bump_type="patch") is called
- **THEN** the `VERSION` file is updated to `1.2.4`
- **AND** the system returns `"✅ Bumped 1.2.3 → 1.2.4"`

#### Scenario: Reject invalid bump type

- **WHEN** `VERSION` file contains `1.2.3`
- **AND** bump_version(bump_type="invalid") is called
- **THEN** the system returns an error message
- **AND** suggests using "major", "minor", or "patch"

#### Scenario: Bump major from 9.9.9

- **WHEN** `VERSION` file contains `9.9.9`
- **AND** bump_version(bump_type="major") is called
- **THEN** the `VERSION` file is updated to `10.0.0`
- **AND** the system returns `"✅ Bumped 9.9.9 → 10.0.0"`

### Requirement: Release Workflow

The system SHALL orchestrate a complete release workflow by syncing versions, validating consistency, and generating git tag commands with clear instructions for manual execution.

#### Scenario: Successful release workflow

- **WHEN** `VERSION` file contains `1.2.0`
- **AND** `galaxy.yml` initially contains `version: 1.1.0`
- **AND** release() is called
- **THEN** the system syncs `VERSION` to `galaxy.yml`
- **AND** validates version consistency
- **AND** returns a comprehensive message including:
  - `"🚀 Release 1.2.0 Ready"`
  - `"✅ Synced 1.2.0 → galaxy.yml"`
  - `"✅ Version 1.2.0 is consistent"`
  - Git commands: `git add VERSION galaxy.yml`
  - Git commands: `git commit -m "Release 1.2.0"`
  - Git commands: `git tag -a v1.2.0 -m "Release 1.2.0"`
  - Git commands: `git push && git push --tags`

#### Scenario: Release with custom tag message

- **WHEN** `VERSION` file contains `2.0.0`
- **AND** release(tag_message="Major release with breaking changes") is called
- **THEN** the system generates git tag command with custom message:
  - `git tag -a v2.0.0 -m "Major release with breaking changes"`

#### Scenario: Release when versions already match

- **WHEN** `VERSION` file contains `1.5.0`
- **AND** `galaxy.yml` already contains `version: 1.5.0`
- **AND** release() is called
- **THEN** the system reports no sync needed
- **AND** validates versions are consistent
- **AND** provides git commands for tagging and pushing

### Requirement: Configurable Defaults

The system SHALL provide sensible default values for common use cases while allowing full customization for different project types and file structures.

#### Scenario: Use default parameters for Ansible collection

- **WHEN** no parameters are provided to sync_version()
- **THEN** the system uses `VERSION` as source file
- **AND** uses `galaxy.yml` as target file
- **AND** uses `r'^version:.*$'` as version pattern

#### Scenario: Override all defaults

- **WHEN** sync_version(source=custom_dir, version_file="MY_VERSION", target_file="config.toml", version_pattern=r'^ver=.*$') is called
- **THEN** the system uses all provided custom values
- **AND** does not apply any default values

#### Scenario: Directory parameter defaults to current module

- **WHEN** no `source` directory is provided to any function
- **THEN** the system uses `dag.current_module().source()` as the default directory

### Requirement: Error Messages

The system SHALL provide clear, actionable error messages that explain what went wrong and suggest specific steps to resolve the issue.

#### Scenario: Missing VERSION file error

- **WHEN** `VERSION` file does not exist
- **AND** any function requiring the VERSION file is called
- **THEN** the system returns an error starting with `"❌"`
- **AND** the message explicitly states the file is missing
- **AND** suggests creating the file: `"Create a VERSION file with format X.Y.Z (e.g., 1.0.0)"`

#### Scenario: Invalid semver format error

- **WHEN** `VERSION` file contains `1.2.3.4`
- **AND** get_version() is called
- **THEN** the system returns: `"❌ Invalid version format: 1.2.3.4 (expected X.Y.Z)"`
- **AND** provides example of correct format

#### Scenario: Pattern not found error

- **WHEN** target file does not contain a line matching the pattern
- **AND** sync_version() is called
- **THEN** the system returns an error explaining pattern was not found
- **AND** suggests verifying the pattern matches the file format
- **AND** provides examples of common patterns

### Requirement: Security Constraints

The system SHALL NOT execute git operations directly and SHALL only suggest git commands for the user to run manually, ensuring the module does not require git access or permissions.

#### Scenario: Release suggests but does not execute git commands

- **WHEN** release() is called
- **THEN** the system generates git command strings
- **AND** returns those commands in output for user to copy
- **AND** does NOT execute `git add`, `git commit`, `git tag`, or `git push` commands

#### Scenario: No file system side effects outside Dagger

- **WHEN** any function modifies files
- **THEN** modifications occur only within Dagger's directory container
- **AND** changes are exported back to host only when explicitly requested
- **AND** no direct file system manipulation occurs on the host

### Requirement: Container Environment Compatibility

The system SHALL operate correctly in Dagger's containerized environment without requiring tools installed on the host system.

#### Scenario: Use only containerized Python

- **WHEN** any function is called
- **THEN** the system uses only Python standard library and dagger-io SDK
- **AND** does not depend on external command-line tools
- **AND** does not require git client in container

#### Scenario: Handle directory as Dagger object

- **WHEN** files are read or written
- **THEN** the system uses `Directory` objects from Dagger
- **AND** uses `.file().contents()` for reading
- **AND** uses `.with_new_file()` for writing

### Requirement: Module Installation

The system SHALL be installable as a Dagger dependency from a git repository and callable from any project that has installed it.

#### Scenario: Install from GitHub

- **WHEN** a user runs `dagger install github.com/org/dagger-version-manager@main`
- **THEN** the module is installed in the user's project
- **AND** functions are callable via `dagger call version-manager [function]`

#### Scenario: Install specific version

- **WHEN** a user runs `dagger install github.com/org/dagger-version-manager@v1.0.0`
- **THEN** the specific tagged version is installed
- **AND** functions work as documented for that version

#### Scenario: Call functions after installation

- **WHEN** the module is installed
- **AND** user runs `dagger call version-manager get-version`
- **THEN** the function executes successfully
- **AND** returns the version from the user's project