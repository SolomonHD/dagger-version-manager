## MODIFIED Requirements

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

## ADDED Requirements

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