## MODIFIED Requirements

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

#### Scenario: Directory parameter defaults to caller's working directory

- **WHEN** no `source` directory is provided to any function
- **AND** the module is installed as a dependency
- **THEN** the system uses the caller's project directory as the default directory
- **AND** NOT the module's own source directory

#### Scenario: Explicit source parameter overrides default

- **WHEN** `source` directory is explicitly provided to any function
- **THEN** the system uses the provided directory
- **AND** ignores the default directory logic

### Requirement: Error Messages

The system SHALL provide clear, actionable error messages that explain what went wrong and suggest specific steps to resolve the issue.

#### Scenario: Missing VERSION file error

- **WHEN** `VERSION` file does not exist
- **AND** any function requiring the VERSION file is called
- **THEN** the system returns an error starting with `"❌"`
- **AND** the message explicitly states: `"Failed to read VERSION:"`
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