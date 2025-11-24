# Implementation Tasks

## 1. Core Function Implementation
- [x] 1.1 Add `setup_git_hooks` function with proper async/await pattern
- [x] 1.2 Add parameters: `source` (Optional[Directory])
- [x] 1.3 Implement `.git` directory validation with clear error message
- [x] 1.4 Add project type detection logic (check for galaxy.yml, pyproject.toml, Dockerfile, Chart.yaml)
- [x] 1.5 Define hook templates for pre-commit and pre-push as string constants
- [x] 1.6 Implement metadata header generation with version from VERSION file
- [x] 1.7 Implement hook file creation/update logic with metadata checking
- [x] 1.8 Add Dagger module detection (check for dagger.json at root)
- [x] 1.9 Skip hook installation for Dagger modules with informative message

## 2. Hook Generation Logic
- [x] 2.1 Create pre-commit hook template with validation command
- [x] 2.2 Create pre-push hook template with validation command
- [x] 2.3 Implement project-specific validation command generation (adjust target_file and pattern)
- [x] 2.4 Make hooks executable (permissions=0o755 in with_new_file)
- [x] 2.5 Handle existing hooks without metadata (preserve them, warn user)
- [x] 2.6 Handle existing hooks with metadata (update them)

## 3. Project Type Detection
- [x] 3.1 Implement file checking for galaxy.yml (Ansible)
- [x] 3.2 Implement file checking for pyproject.toml (Python)
- [x] 3.3 Implement file checking for Dockerfile (Docker)
- [x] 3.4 Implement file checking for Chart.yaml (Helm)
- [x] 3.5 Default to Ansible if multiple types detected (priority order implemented)
- [x] 3.6 Return detected project type for output message

## 4. Output and Error Handling
- [x] 4.1 Returns Directory object (user sees success on export)
- [x] 4.2 Return error if `.git` directory not found
- [x] 4.3 Return warning if hooks exist without metadata marker (collected in warnings list)
- [x] 4.4 Hooks include behavior instructions in comments

## 5. Testing
- [x] 5.1 Manual testing confirmed project type detection works
- [x] 5.2 Manual testing confirmed hook template generation works
- [x] 5.3 Tested with actual project (Python type detected, hooks created)
- [x] 5.4 Verified hooks created with executable permissions (0755)
- [x] 5.5 Tested `.git` directory missing scenario (error raised correctly)
- [x] 5.6 Logic implemented for existing hooks preservation

## 6. Documentation
- [x] 6.1 Update README.md with setup-git-hooks function documentation
- [x] 6.2 Update EXAMPLES.md with git hooks setup examples
- [x] 6.3 Add docstring to setup_git_hooks function with usage examples