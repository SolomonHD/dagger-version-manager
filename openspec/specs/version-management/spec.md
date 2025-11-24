# version-management Specification

## Purpose
TBD - created by archiving change create-version-manager-module. Update Purpose after archive.
## Requirements
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

### Requirement: Git Hooks Installation

The system SHALL provide automated installation of git hooks that enforce version consistency validation for projects that consume the version-manager module, with automatic project type detection and metadata tracking for updates. The system SHALL detect Dagger module projects and skip hook installation with an informative message, as Dagger modules have special version requirements incompatible with standard validation.

#### Scenario: Install hooks for Ansible collection

- **WHEN** a project has `galaxy.yml` file
- **AND** `.git` directory exists
- **AND** `dagger.json` does NOT exist at root (not a Dagger module)
- **AND** setup_git_hooks() is called
- **THEN** pre-commit hook is created in `.git/hooks/pre-commit`
- **AND** pre-push hook is created in `.git/hooks/pre-push`
- **AND** both hooks validate VERSION against galaxy.yml
- **AND** both hooks include metadata header `# DAGGER-VERSION-MANAGER: v{version}`
- **AND** both hooks are made executable
- **AND** success message includes project type "Ansible Collection"

#### Scenario: Install hooks for Python project

- **WHEN** a project has `pyproject.toml` file
- **AND** `.git` directory exists  
- **AND** `dagger.json` does NOT exist at root (not a Dagger module)
- **AND** setup_git_hooks() is called
- **THEN** pre-commit and pre-push hooks are created
- **AND** hooks validate VERSION against pyproject.toml with pattern `r'^version\s*=\s*".*"$'`
- **AND** success message includes project type "Python"

#### Scenario: Install hooks for Docker project

- **WHEN** a project has `Dockerfile`
- **AND** `.git` directory exists
- **AND** `dagger.json` does NOT exist at root (not a Dagger module)
- **AND** setup_git_hooks() is called
- **THEN** pre-commit and pre-push hooks are created
- **AND** hooks validate VERSION against Dockerfile with pattern `r'LABEL version=".*"$'`
- **AND** success message includes project type "Docker"

#### Scenario: Install hooks for Helm project

- **WHEN** a project has `Chart.yaml` file
- **AND** `.git` directory exists
- **AND** `dagger.json` does NOT exist at root (not a Dagger module)
- **AND** setup_git_hooks() is called
- **THEN** pre-commit and pre-push hooks are created
- **AND** hooks validate VERSION against Chart.yaml
- **AND** success message includes project type "Helm"

#### Scenario: Skip installation for Dagger module projects

- **WHEN** a project has `dagger.json` at root (is a Dagger module)
- **AND** `.git` directory exists
- **AND** setup_git_hooks() is called
- **THEN** system detects this is a Dagger module project
- **AND** NO hooks are created in `.git/hooks/`
- **AND** system returns informative message:
  - `"ℹ️  Detected Dagger module project"`
  - `""`
  - `"Git hooks are designed for projects that CONSUME version-manager,"`
  - `"not for the version-manager module itself."`
  - `""`
  - `"For this project, manage versions manually using:"`
  - `"  - VERSION file only"`
  - `"  - pyproject.toml should stay at version = \"0.0.0\""`
  - `""`
  - `"No hooks installed."`

#### Scenario: Run on dagger-version-manager itself

- **WHEN** setup_git_hooks() is run on the dagger-version-manager repository
- **AND** `dagger.json` exists at repository root
- **THEN** Dagger module detection triggers
- **AND** no hooks are installed
- **AND** command succeeds without side effects
- **AND** informative message explains why hooks were skipped

#### Scenario: Multiple project types detected (consumer project)

- **WHEN** a project has both `galaxy.yml` and `pyproject.toml`
- **AND** `dagger.json` does NOT exist at root
- **AND** setup_git_hooks() is called
- **THEN** the system defaults to Ansible project type
- **AND** hooks validate against `galaxy.yml`
- **AND** success message indicates "Ansible Collection" as primary type

#### Scenario: Dagger module with consumer project markers

- **WHEN** a project has `dagger.json` at root (Dagger module)
- **AND** also has `galaxy.yml` or other consumer project markers
- **AND** setup_git_hooks() is called
- **THEN** Dagger module detection takes precedence
- **AND** no hooks are installed
- **AND** message explains Dagger modules are excluded from hook installation

#### Scenario: Update existing dagger-version-manager hooks

- **WHEN** hooks already exist with metadata header `# DAGGER-VERSION-MANAGER: v1.0.0`
- **AND** `dagger.json` does NOT exist at root
- **AND** setup_git_hooks() is called
- **THEN** existing hooks are replaced with updated versions
- **AND** new metadata header reflects current version
- **AND** success message indicates hooks were updated

#### Scenario: Preserve existing non-dagger-version-manager hooks

- **WHEN** `.git/hooks/pre-commit` exists without dagger-version-manager metadata
- **AND** `dagger.json` does NOT exist at root
- **AND** setup_git_hooks() is called
- **THEN** existing hook is NOT modified
- **AND** system returns warning message about existing hook
- **AND** warning suggests manual inspection or removal before setup

#### Scenario: Missing .git directory

- **WHEN** `.git` directory does not exist in the project
- **AND** setup_git_hooks() is called
- **THEN** system returns error: `"❌ Git repository not found (.git directory missing)"`
- **AND** suggests initializing git with `git init`

#### Scenario: Hook validation prevents commits with version mismatch

- **WHEN** hooks are installed (consumer project, not Dagger module)
- **AND** user attempts to commit with VERSION=1.2.3 and galaxy.yml=1.0.0
- **THEN** pre-commit hook runs validation
- **AND** commit is blocked with error message
- **AND** user is directed to run sync-version command

#### Scenario: Hook validation prevents pushes with version mismatch

- **WHEN** hooks are installed (consumer project, not Dagger module)
- **AND** user attempts to push with VERSION=2.0.0 and pyproject.toml=1.9.0
- **THEN** pre-push hook runs validation
- **AND** push is blocked with error message
- **AND** user is directed to run sync-version command

#### Scenario: Success message format for consumer projects

- **WHEN** hooks are successfully installed for Ansible consumer project
- **AND** `dagger.json` does NOT exist at root
- **AND** setup_git_hooks() completes
- **THEN** output includes:
  - `"✅ Git hooks installed"`
  - `"Project type: Ansible Collection"`
  - `"Hooks installed:"`
  - `"- .git/hooks/pre-commit (validates VERSION ↔ galaxy.yml)"`
  - `"- .git/hooks/pre-push (validates VERSION ↔ galaxy.yml)"`
  - `"Hooks will prevent commits/pushes with version mismatches."`

### Requirement: Dagger Module Detection

The system SHALL detect when the project is a Dagger module (has `dagger.json` at repository root) and handle it as a special case where hook installation should be skipped.

#### Scenario: Detect dagger.json at root

- **WHEN** checking if project is a Dagger module
- **AND** `dagger.json` file exists at repository root
- **THEN** system identifies project as a Dagger module
- **AND** returns True from detection check

#### Scenario: Detect absence of dagger.json

- **WHEN** checking if project is a Dagger module
- **AND** `dagger.json` file does NOT exist at repository root  
- **THEN** system identifies project as a consumer project (not a Dagger module)
- **AND** returns False from detection check

#### Scenario: Detection runs before project type detection

- **WHEN** setup_git_hooks() is called
- **THEN** Dagger module detection runs first
- **AND** if detected, function returns early with informative message
- **AND** project type detection (`_detect_project_type`) is skipped for Dagger modules

#### Scenario: Consumer project with dagger dependency

- **WHEN** a project consumes dagger-version-manager as a dependency
- **AND** has `dagger.json` in dependencies (not at root)
- **AND** setup_git_hooks() is called
- **THEN** system does NOT treat it as a Dagger module
- **AND** hooks are installed normally based on project type
- **AND** detection only checks for `dagger.json` at the repository root level

### Requirement: Hook Metadata Tracking

The system SHALL mark installed hooks with metadata headers to enable version tracking and safe updates of dagger-version-manager managed hooks.

#### Scenario: Metadata header format

- **WHEN** hooks are created
- **THEN** first line includes: `#!/bin/bash`
- **AND** second line includes: `# DAGGER-VERSION-MANAGER: v{version}`
- **AND** third line includes: `# Installed: {ISO-8601 timestamp}`

#### Scenario: Identify managed hooks by metadata

- **WHEN** checking if hook is managed by dagger-version-manager
- **THEN** system checks for `# DAGGER-VERSION-MANAGER:` prefix in file
- **AND** hook is considered managed if marker is present
- **AND** hook is considered unmanaged if marker is absent

### Requirement: Project Type Detection

The system SHALL automatically detect project type by checking for marker configuration files and select appropriate validation parameters for generated hooks.

#### Scenario: Detection priority order

- **WHEN** multiple project types are detected
- **THEN** priority is: Ansible > Python > Helm > Docker
- **AND** most specific type is chosen for hook generation

#### Scenario: Detection mapping to validation parameters

- **WHEN** project type is Ansible (galaxy.yml found)
- **THEN** target_file is `galaxy.yml`
- **AND** version_pattern is `r'^version:.*$'`
- **WHEN** project type is Python (pyproject.toml found)
- **THEN** target_file is `pyproject.toml`
- **AND** version_pattern is `r'^version\s*=\s*".*"$'`
- **WHEN** project type is Docker (Dockerfile found)
- **THEN** target_file is `Dockerfile`
- **AND** version_pattern is `r'LABEL version=".*"$'`
- **WHEN** project type is Helm (Chart.yaml found)
- **THEN** target_file is `Chart.yaml`
- **AND** version_pattern is `r'^version:.*$'`

### Requirement: Hook Template Generation

The system SHALL generate shell script hooks that call dagger validate-version with project-specific parameters and exit with appropriate status codes.

#### Scenario: Pre-commit hook structure

- **WHEN** pre-commit hook is generated
- **THEN** hook contains shebang: `#!/bin/bash`
- **AND** hook contains metadata header
- **AND** hook contains validation command: `dagger call version-manager validate-version [params]`
- **AND** hook checks exit status and blocks commit on failure
- **AND** hook outputs error message if validation fails

#### Scenario: Pre-push hook structure

- **WHEN** pre-push hook is generated
- **THEN** hook structure matches pre-commit (same validation command)
- **AND** hook blocks push on validation failure
- **AND** both hooks use identical validation logic

#### Scenario: Hook executability

- **WHEN** hooks are written to `.git/hooks/`
- **THEN** hooks are created with executable permission (0755)
- **AND** success message reminds user hooks are executable

### Requirement: Security and Container Environment Constraints

The system SHALL operate within Dagger's containerized environment while writing hooks to the user's filesystem through the export mechanism.

#### Scenario: No direct filesystem manipulation

- **WHEN** setup_git_hooks() is called
- **THEN** system uses Dagger Directory objects
- **AND** hooks are written using `.with_new_file()` method
- **AND** changes are exported only when user adds `export --path=.`

#### Scenario: Working with .git directory

- **WHEN** checking for `.git` directory
- **THEN** system uses Directory API to check for directory existence
- **AND** does not execute shell git commands
- **AND** validation is read-only

