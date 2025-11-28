# OpenSpec change prompt

## Context

The `dagger-version-manager` module currently only looks for a `VERSION` file at the project root. However, some projects (like Packer plugins) use `version/VERSION` instead. Users must manually specify `--version-file=version/VERSION` for these projects.

## Goal

Add auto-detection to check both `VERSION` and `version/VERSION` locations when no explicit `--version-file` is provided. If both files exist, return an error to prevent ambiguity.

## Scope

### In scope:
- Modify [`src/main/__init__.py`](src/main/__init__.py) to add VERSION file auto-detection logic
- Check both `VERSION` (root) and `version/VERSION` locations
- Error if both files exist (ambiguity)
- Use whichever file is found if only one exists
- Update VERSION file to `1.2.0` for this release
- Update documentation (README.md, EXAMPLES.md) with new behavior

### Out of scope:
- Changes to function signatures (keep backward compatibility)
- Support for additional version file locations beyond these two
- Changes to pyproject.toml version (stays at `0.0.0` per Dagger module standards)

## Desired behavior

**Detection logic (when `--version-file` not explicitly provided):**

1. Check if `VERSION` exists at project root
2. Check if `version/VERSION` exists
3. If both exist → Return error with message asking user to specify which one
4. If only one exists → Use that file
5. If neither exists → Return error with helpful message

**Example outputs:**

When both files exist:
```
❌ Ambiguous VERSION files detected:
   Found both ./VERSION and ./version/VERSION
   Specify which to use: --version-file=VERSION or --version-file=version/VERSION
```

When neither exists:
```
❌ No VERSION file found
   Checked: ./VERSION, ./version/VERSION
   Create a VERSION file with format X.Y.Z (e.g., 1.0.0)
```

When one exists (success case):
```
1.2.3
```

## Constraints & assumptions

- Maintain full backward compatibility: explicit `--version-file` always takes precedence
- Auto-detection only applies when `version_file` parameter uses its default value
- The default value remains `"VERSION"` in the function signature (for documentation)
- Semantic versioning (X.Y.Z) format requirement unchanged

## Acceptance criteria

- [ ] Auto-detects `VERSION` at project root
- [ ] Auto-detects `version/VERSION` as fallback
- [ ] Returns error if both `VERSION` and `version/VERSION` exist
- [ ] Returns clear error if neither file exists
- [ ] Explicit `--version-file` parameter overrides auto-detection
- [ ] All existing tests pass
- [ ] VERSION file updated to `1.2.0`
- [ ] Documentation updated with auto-detection behavior