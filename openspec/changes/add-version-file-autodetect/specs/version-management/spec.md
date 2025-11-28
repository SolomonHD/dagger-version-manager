# version-management Specification Delta

## ADDED Requirements

### Requirement: VERSION File Auto-Detection

The system SHALL automatically detect VERSION file locations when no explicit version file path is provided, checking both `VERSION` at the project root and `version/VERSION` in the version subdirectory, and SHALL return appropriate errors for ambiguous or missing file conditions.

#### Scenario: Auto-detect VERSION at project root

- **WHEN** `version_file` parameter is `"VERSION"` (default)
- **AND** only `./VERSION` exists (not `./version/VERSION`)
- **AND** any version function is called
- **THEN** the system uses `./VERSION` as the version source

#### Scenario: Auto-detect version/VERSION in subdirectory

- **WHEN** `version_file` parameter is `"VERSION"` (default)
- **AND** only `./version/VERSION` exists (not `./VERSION`)
- **AND** any version function is called
- **THEN** the system uses `./version/VERSION` as the version source

#### Scenario: Error when both VERSION files exist

- **WHEN** `version_file` parameter is `"VERSION"` (default)
- **AND** both `./VERSION` and `./version/VERSION` exist
- **AND** any version function is called
- **THEN** the system returns an error:
  - `"❌ Ambiguous VERSION files detected:"`
  - `"   Found both ./VERSION and ./version/VERSION"`
  - `"   Specify which to use: --version-file=VERSION or --version-file=version/VERSION"`

#### Scenario: Error when no VERSION file exists

- **WHEN** `version_file` parameter is `"VERSION"` (default)
- **AND** neither `./VERSION` nor `./version/VERSION` exists
- **AND** any version function is called
- **THEN** the system returns an error:
  - `"❌ No VERSION file found"`
  - `"   Checked: ./VERSION, ./version/VERSION"`
  - `"   Create a VERSION file with format X.Y.Z (e.g., 1.0.0)"`

#### Scenario: Explicit version-file overrides auto-detection

- **WHEN** `version_file` parameter is explicitly set to `"custom/path/VERSION"`
- **AND** any version function is called
- **THEN** the system uses the explicitly specified path
- **AND** does NOT perform auto-detection
- **AND** reports file-not-found error if the specified path does not exist

#### Scenario: Explicit VERSION path bypasses detection

- **WHEN** `version_file` parameter is explicitly set to `"VERSION"` with intent (same as default)
- **AND** both `./VERSION` and `./version/VERSION` exist
- **AND** user explicitly specifies `--version-file=VERSION`
- **THEN** the system uses `./VERSION` directly
- **AND** does NOT return ambiguity error
- **REASONING** Explicit specification indicates user intent and overrides auto-detection behavior

## MODIFIED Requirements

### Requirement: Version Source File Reading

The system SHALL read version numbers from a designated source file (default: `VERSION`) with automatic detection of common locations (`VERSION` at root or `version/VERSION` in subdirectory), and validate the format as semantic versioning (X.Y.Z where X, Y, and Z are non-negative integers).

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

#### Scenario: Read version from version/VERSION location

- **WHEN** only `version/VERSION` file exists with content `3.0.0`
- **AND** get_version() is called with default parameters
- **THEN** the system auto-detects the file location
- **AND** returns `"3.0.0"`