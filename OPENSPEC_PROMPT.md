# OpenSpec change prompt

## Context
The current `README.md` contains generic placeholders (e.g., `github.com/yourorg/...`) and is cluttered with detailed function examples that reduce readability.

## Goal
Refactor the documentation to be concise, readable, and accurate to this specific repository.

## Scope
- In scope:
  - `README.md`: Simplify content and fix installation instructions.
  - `EXAMPLES.md`: Receive detailed examples moved from the readme.
- Out of scope:
  - Functional code changes to the Dagger module.

## Desired behaviour
- **Readme Cleanup:**
  - Move "obscure", complex, or lengthy function examples from `README.md` to `EXAMPLES.md`.
  - Keep `README.md` focused on the problem statement, features, installation, and a simple "Quick Start".
  - Ensure `README.md` clearly links to `EXAMPLES.md` for advanced usage.
- **Installation Fixes:**
  - Replace generic `github.com/yourorg/...` URLs with the **actual repository URL**.
  - Determine the correct URL by inspecting the local `.git/config` (convert SSH to HTTPS if needed for public docs).
  - Ensure installation examples use the actual version found in the `VERSION` file.

## Constraints & assumptions
- Assumption: `EXAMPLES.md` is the correct destination for moved content.
- Assumption: The repository is hosted on a standard git provider (like GitHub) where the import path matches the URL structure.

## Acceptance criteria
- [ ] `README.md` is significantly shorter and easier to scan.
- [ ] Installation commands in `README.md` point to the correct repository URL (not `yourorg`).
- [ ] All examples removed from the readme are preserved in `EXAMPLES.md`.