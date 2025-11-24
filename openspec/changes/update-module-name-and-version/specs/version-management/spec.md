## MODIFIED Requirements

### Requirement: Module Installation

The system SHALL be installable as a Dagger dependency from a git repository and callable from any project that has installed it using the module name `version-manager`.

#### Scenario: Install from GitHub

- **WHEN** a user runs `dagger install github.com/org/dagger-version-manager@main`
- **THEN** the module is installed in the user's project
- **AND** functions are callable via `dagger call -m version-manager [function]`

#### Scenario: Install specific version

- **WHEN** a user runs `dagger install github.com/org/dagger-version-manager@v1.0.2`
- **THEN** the specific tagged version is installed
- **AND** functions work as documented for that version

#### Scenario: Call functions after installation

- **WHEN** the module is installed
- **AND** user runs `dagger call -m version-manager get-version`
- **THEN** the function executes successfully
- **AND** returns the version from the user's project

#### Scenario: Call functions from local development

- **WHEN** working within the dagger-version-manager repository itself
- **AND** user runs `dagger call get-version` (no `-m` flag)
- **THEN** the function executes successfully
- **AND** returns the version from the repository

#### Scenario: Call functions remotely without installation

- **WHEN** user runs `dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.2 version-manager get-version`
- **THEN** the function executes successfully without prior installation
- **AND** returns the version from the user's project

## ADDED Requirements

### Requirement: Documentation Calling Context Clarity

The system's documentation SHALL clearly distinguish between three different calling contexts for using the module, providing accurate examples for each context to prevent user confusion.

#### Scenario: Document local development context

- **WHEN** documentation describes usage within the dagger-version-manager repository
- **THEN** examples SHALL use `dagger call [function]` format
- **AND** SHALL NOT include `-m` flag or module name
- **AND** SHALL be labeled as "Local Development" context

#### Scenario: Document installed module context

- **WHEN** documentation describes usage from a consumer project that has installed the module
- **THEN** examples SHALL use `dagger call -m version-manager [function]` format
- **AND** SHALL include the module name `version-manager` from dagger.json
- **AND** SHALL be labeled as "Installed Module" context
- **AND** this SHALL be the primary context shown in Quick Start sections

#### Scenario: Document remote module context

- **WHEN** documentation describes usage without installing the module
- **THEN** examples SHALL use `dagger call -m github.com/SolomonHD/dagger-version-manager@[version] version-manager [function]` format
- **AND** SHALL include both repository URL and module name
- **AND** SHALL be labeled as "Remote Module" context
- **AND** SHALL show actual repository URL, not placeholders

#### Scenario: Quick Start defaults to installed module context

- **WHEN** user reads the Quick Start section of README.md
- **THEN** all examples SHALL use the installed module context (`-m version-manager`)
- **AND** a clear note SHALL explain which calling context is being demonstrated
- **AND** SHALL refer to additional documentation for other contexts

### Requirement: Version Number Consistency

The system SHALL maintain version number consistency across the VERSION file and all documentation references, with the VERSION file serving as the single source of truth.

#### Scenario: Version bump updates VERSION file

- **WHEN** a new release version 1.0.2 is prepared
- **THEN** the VERSION file SHALL contain `1.0.2`
- **AND** documentation references to specific versions SHALL use `v1.0.2` format for git tags
- **AND** installation examples SHALL reference `@v1.0.2` or `@main` appropriately

#### Scenario: Documentation version examples use actual version

- **WHEN** documentation provides installation or usage examples
- **THEN** examples SHALL use actual version numbers from VERSION file (e.g., `v1.0.2`)
- **AND** SHALL NOT use placeholder versions like `v1.0.0` or `vX.Y.Z`
- **AND** generic examples may use `@main` to indicate latest development version