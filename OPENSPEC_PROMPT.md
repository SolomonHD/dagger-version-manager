# OpenSpec change prompt

## Context
The Dagger module name in `dagger.json` is currently `"dagger-version-manager"`, which requires users to call it with `dagger call -m dagger-version-manager` when using it from another project. The documentation, however, shows examples using `version-manager`, creating confusion.

## Goal
Change the module name to `version-manager` (shorter, cleaner) and fix all documentation to correctly show how to call the module in different contexts (local development vs. installed module vs. remote module).

## Scope
- In scope:
  - `dagger.json`: Change module name from `"dagger-version-manager"` to `"version-manager"`
  - `README.md`: Update examples to clarify calling patterns for different contexts
  - `EXAMPLES.md`: Fix all examples to use correct `-m` flag patterns
- Out of scope:
  - Functional code changes to Python module
  - Changes to VERSION file or other configuration

## Desired behaviour

### 1. Module Name Change
- In `dagger.json` line 2: Change `"name": "dagger-version-manager"` to `"name": "version-manager"`

### 2. Documentation Calling Patterns
The documentation should clearly distinguish between three contexts:

**A. Local Development (working IN the dagger-version-manager repo):**
```bash
dagger call get-version
dagger call sync-version export --path=.
```
No `-m` flag needed, no module name needed.

**B. Installed Module (using from ANOTHER project after `dagger install`):**
```bash
dagger call -m version-manager get-version
dagger call -m version-manager sync-version export --path=.
```
Use `-m version-manager` (the module name from dagger.json).

**C. Remote Module (calling without installing):**
```bash
dagger call -m github.com/SolomonHD/dagger-version-manager@v1.0.1 version-manager get-version
```
Use `-m <repo-url>@<version> <module-name>` (both source and module name).

### 3. README.md Updates
- The "Quick Start" section should be rewritten to show **installed module** examples (context B), since this is the most common use case for documentation readers.
- Add a clear note at the top of Quick Start explaining the context.
- Change all examples from `dagger call version-manager ...` to `dagger call -m version-manager ...`

### 4. EXAMPLES.md Updates  
- All local-style examples (without `-m` flag) should be updated to installed module style (with `-m version-manager`)
- Remote examples are already correct (they show the full pattern with repository URL and module name)
- Examples in these sections need updating:
  - Ansible Collection (lines 34-51)
  - Python Project (lines 94-108)
  - Docker Project (lines 147-161)
  - Kubernetes/Helm (lines 209-220)
  - All examples in Advanced Workflows section (lines 590-743)
  - Git Hooks manual setup (lines 547, 573)
  - Makefiles Integration (lines 703-724)

## Constraints & assumptions
- Assumption: Users most commonly install the module and use it from other projects (context B above)
- Assumption: Remote calling examples (with full GitHub URL) are already correct and don't need changes
- Constraint: The repository name stays `dagger-version-manager` (only the module name in dagger.json changes)
- Constraint: CI/CD examples that use remote calling (lines 278-373 in EXAMPLES.md) are already correct

## Acceptance criteria
- [ ] `dagger.json` has `"name": "version-manager"` instead of `"dagger-version-manager"`
- [ ] README.md Quick Start section uses `-m version-manager` in all examples
- [ ] README.md has a clear note explaining the calling context (installed module usage)
- [ ] EXAMPLES.md local-style examples all updated to use `-m version-manager`
- [ ] Remote examples (with full GitHub URL) remain unchanged
- [ ] All three calling contexts are documented clearly somewhere (could be in README under a "Usage Contexts" section)