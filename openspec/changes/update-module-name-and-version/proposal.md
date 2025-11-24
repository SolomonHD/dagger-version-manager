# Change: Update Module Name and Bump Version to 1.0.2

## Why
The Dagger module name in `dagger.json` is currently `"dagger-version-manager"`, which requires users to call it with the verbose `dagger call -m dagger-version-manager`. The documentation uses `version-manager` in examples, creating confusion about the correct calling pattern. Additionally, we need to bump the version to 1.0.2 to reflect this change and ensure all documentation accurately shows the three different calling contexts (local development, installed module, remote module).

## What Changes
- **Update `dagger.json`**: Change module name from `"dagger-version-manager"` to `"version-manager"` for a cleaner, shorter module name
- **Bump VERSION**: Update from `1.0.1` to `1.0.2` to mark this release
- **Refactor README.md**:
  - Add clear explanation of three calling contexts at the top of Quick Start
  - Update all Quick Start examples to show **installed module** usage (context B with `-m version-manager`)
  - Optionally add a "Usage Contexts" section explaining when to use each pattern
- **Refactor EXAMPLES.md**:
  - Update local-style examples to use `-m version-manager` (installed module style)
  - Keep remote examples unchanged (they already use full GitHub URL pattern)
  - Update specific sections: Ansible Collection, Python Project, Docker Project, Kubernetes/Helm, Advanced Workflows, Git Hooks manual setup, Makefiles Integration

## Impact
- **Affected Specs**: `version-management` (documentation aspects only - no functional changes)
- **Affected Files**:
  - `dagger.json` (line 2: module name)
  - `VERSION` (bump from 1.0.1 to 1.0.2)
  - `README.md` (Quick Start section, potentially new Usage Contexts section)
  - `EXAMPLES.md` (multiple sections with local-style examples)
- **Breaking Change**: Users who installed the module with the old name will need to reinstall
- **Migration**: Users should run `dagger install github.com/SolomonHD/dagger-version-manager@v1.0.2` after this release