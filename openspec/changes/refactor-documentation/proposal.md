# Change: Refactor Documentation

## Why
The current `README.md` contains generic placeholders (e.g., `github.com/yourorg/...`) and is cluttered with detailed function examples that reduce readability. Users need clear, accurate installation instructions and a scannable overview of the project.

## What Changes
- **Refactor `README.md`**:
  - Move "obscure", complex, or lengthy function examples to `EXAMPLES.md`.
  - Focus `README.md` on the problem statement, features, installation, and a simple "Quick Start".
  - Ensure `README.md` clearly links to `EXAMPLES.md` for advanced usage.
- **Fix Installation Instructions**:
  - Replace generic `github.com/yourorg/...` URLs with the actual repository URL: `github.com/SolomonHD/dagger-version-manager`.
  - Update installation examples to use the actual version found in the `VERSION` file (currently `1.0.1`).
- **Add Git Hooks Examples**:
  - Add clear examples for installing git hooks from this module into other repositories.

## Impact
- **Affected Specs**: `project-documentation` (new capability)
- **Affected Files**:
  - `README.md`
  - `EXAMPLES.md`