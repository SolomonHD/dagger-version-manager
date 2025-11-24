"""Dagger Version Manager - Automated version synchronization for multi-file projects."""

import re
from datetime import datetime
from typing import Annotated, Optional

import dagger
from dagger import Doc, function, object_type


@object_type
class VersionManager:
    """
    Dagger module for managing semantic versions across multiple configuration files.
    
    Provides version synchronization, validation, bumping, and release workflows
    for projects that maintain version numbers in multiple files (e.g., VERSION + galaxy.yml).
    """

    async def _get_source(self, source: Optional[dagger.Directory] = None) -> dagger.Directory:
        """
        Get the source directory, defaulting to current module source if not provided.
        
        Args:
            source: Optional directory to use instead of current module source
            
        Returns:
            Directory object to work with
        """
        if source is None:
            return await dagger.dag.current_module().source()
        return source

    def _validate_semver(self, version: str) -> tuple[bool, str]:
        """
        Validate semantic version format (X.Y.Z).
        
        Args:
            version: Version string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        semver_pattern = r'^\d+\.\d+\.\d+$'
        if re.match(semver_pattern, version.strip()):
            return True, ""
        return False, f"❌ Invalid version format: {version.strip()} (expected X.Y.Z)"

    async def _read_version_file(
        self,
        source: dagger.Directory,
        version_file: str
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Read version from the source file.
        
        Args:
            source: Directory containing the version file
            version_file: Name of the version file
            
        Returns:
            Tuple of (version_string, error_message)
        """
        try:
            content = await source.file(version_file).contents()
            version = content.strip()
            
            is_valid, error = self._validate_semver(version)
            if not is_valid:
                return None, error
            
            return version, None
        except Exception as e:
            error_msg = (
                f"❌ Failed to read {version_file}: {str(e)}\n"
                f"   Create a {version_file} file with format X.Y.Z (e.g., 1.0.0)"
            )
            return None, error_msg

    def _extract_version_from_target(
        self,
        target_content: str,
        version_pattern: str
    ) -> Optional[str]:
        """
        Extract version from target file using regex pattern.
        
        Args:
            target_content: Content of the target file
            version_pattern: Regex pattern to match version line
            
        Returns:
            Extracted version string or None if not found
        """
        for line in target_content.split('\n'):
            if re.match(version_pattern, line):
                # Extract version number from the line
                version_match = re.search(r'\d+\.\d+\.\d+', line)
                if version_match:
                    return version_match.group(0)
        return None

    def _bump_version_logic(self, version: str, bump_type: str) -> tuple[Optional[str], Optional[str]]:
        """
        Increment version component according to semantic versioning rules.
        
        Args:
            version: Current version (X.Y.Z)
            bump_type: Type of bump (major, minor, or patch)
            
        Returns:
            Tuple of (new_version, error_message)
        """
        if bump_type not in ["major", "minor", "patch"]:
            return None, f'❌ Invalid bump_type: {bump_type} (use "major", "minor", or "patch")'
        
        try:
            major, minor, patch = map(int, version.split('.'))
            
            if bump_type == "major":
                return f"{major + 1}.0.0", None
            elif bump_type == "minor":
                return f"{major}.{minor + 1}.0", None
            else:  # patch
                return f"{major}.{minor}.{patch + 1}", None
        except Exception as e:
            return None, f"❌ Failed to parse version {version}: {str(e)}"

    @function
    async def get_version(
        self,
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing version file (defaults to current module)")
        ] = None,
        version_file: Annotated[
            str,
            Doc("Name of the version file")
        ] = "VERSION"
    ) -> str:
        """
        Read and return the current version from the version file.
        
        Args:
            source: Source directory (defaults to current module source)
            version_file: Name of the version file (default: VERSION)
            
        Returns:
            Version string or error message
            
        Example:
            dagger call get-version
            dagger call get-version --version-file=MY_VERSION
        """
        src = await self._get_source(source)
        version, error = await self._read_version_file(src, version_file)
        
        if error:
            return error
        
        return version

    @function
    async def validate_version(
        self,
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing version files (defaults to current module)")
        ] = None,
        version_file: Annotated[
            str,
            Doc("Name of the source version file")
        ] = "VERSION",
        target_file: Annotated[
            str,
            Doc("Name of the target file to validate against")
        ] = "galaxy.yml",
        version_pattern: Annotated[
            str,
            Doc("Regex pattern to match version line in target file")
        ] = r'^version:.*$'
    ) -> str:
        """
        Validate that version in source file matches version in target file.
        
        Args:
            source: Source directory (defaults to current module source)
            version_file: Name of the source version file (default: VERSION)
            target_file: Name of the target file to check (default: galaxy.yml)
            version_pattern: Regex pattern to match version line (default: r'^version:.*$')
            
        Returns:
            Validation result message
            
        Example:
            dagger call validate-version
            dagger call validate-version --target-file=pyproject.toml --version-pattern='^version\s*=\s*".*"'
        """
        src = await self._get_source(source)
        
        # Read source version
        source_version, error = await self._read_version_file(src, version_file)
        if error:
            return error
        
        # Read target file
        try:
            target_content = await src.file(target_file).contents()
        except Exception as e:
            return (
                f"❌ Failed to read {target_file}: {str(e)}\n"
                f"   Check that the file exists and path is correct"
            )
        
        # Extract target version
        target_version = self._extract_version_from_target(target_content, version_pattern)
        
        if not target_version:
            return (
                f"❌ Could not find version in {target_file} matching pattern: {version_pattern}\n"
                f"   Verify the pattern matches your file format"
            )
        
        # Compare versions
        if source_version == target_version:
            return f"✅ Version {source_version} is consistent"
        else:
            return (
                f"⚠️  Mismatch: {version_file}={source_version}, {target_file}={target_version}\n"
                f"   Run: dagger call version-manager sync-version"
            )

    @function
    async def sync_version(
        self,
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing version files (defaults to current module)")
        ] = None,
        version_file: Annotated[
            str,
            Doc("Name of the source version file")
        ] = "VERSION",
        target_file: Annotated[
            str,
            Doc("Name of the target file to update")
        ] = "galaxy.yml",
        version_pattern: Annotated[
            str,
            Doc("Regex pattern to match version line in target file")
        ] = r'^version:.*$'
    ) -> dagger.Directory:
        """
        Synchronize version from source file to target file.
        
        Reads version from source file and updates the matching line in target file
        according to the specified pattern.
        
        Args:
            source: Source directory (defaults to current module source)
            version_file: Name of the source version file (default: VERSION)
            target_file: Name of the target file to update (default: galaxy.yml)
            version_pattern: Regex pattern to match version line (default: r'^version:.*$')
            
        Returns:
            Updated directory with synced version
            
        Example:
            dagger call sync-version export --path=.
            dagger call sync-version --target-file=pyproject.toml --version-pattern='^version\s*=\s*".*"' export --path=.
        """
        src = await self._get_source(source)
        
        # Read source version
        source_version, error = await self._read_version_file(src, version_file)
        if error:
            raise Exception(error)
        
        # Read target file
        try:
            target_content = await src.file(target_file).contents()
        except Exception as e:
            raise Exception(
                f"❌ Failed to read {target_file}: {str(e)}\n"
                f"   Check that the file exists and path is correct"
            )
        
        # Update target content
        lines = target_content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if re.match(version_pattern, line):
                # Determine format based on pattern
                if 'version:' in line:
                    # YAML format
                    lines[i] = f"version: {source_version}"
                elif 'version =' in line or 'version=' in line:
                    # TOML/Python format
                    lines[i] = f'version = "{source_version}"'
                elif 'LABEL version=' in line:
                    # Dockerfile format
                    lines[i] = f'LABEL version="{source_version}"'
                else:
                    # Generic replacement
                    lines[i] = re.sub(r'\d+\.\d+\.\d+', source_version, line)
                updated = True
                break
        
        if not updated:
            raise Exception(
                f"❌ Pattern not found in {target_file}: {version_pattern}\n"
                f"   Verify the pattern matches your file format\n"
                f"   Common patterns:\n"
                f"   - YAML: r'^version:.*$'\n"
                f"   - TOML: r'^version\\s*=\\s*\".*\"$'\n"
                f"   - Dockerfile: r'LABEL version=\".*\"$'"
            )
        
        # Write updated content back
        new_content = '\n'.join(lines)
        updated_dir = src.with_new_file(target_file, new_content)
        
        return updated_dir

    @function
    async def bump_version(
        self,
        bump_type: Annotated[
            str,
            Doc("Type of version bump: major, minor, or patch")
        ],
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing version file (defaults to current module)")
        ] = None,
        version_file: Annotated[
            str,
            Doc("Name of the version file to update")
        ] = "VERSION"
    ) -> dagger.Directory:
        """
        Increment version according to semantic versioning rules.
        
        - major: X.Y.Z → (X+1).0.0
        - minor: X.Y.Z → X.(Y+1).0
        - patch: X.Y.Z → X.Y.(Z+1)
        
        Args:
            bump_type: Type of bump (major, minor, or patch)
            source: Source directory (defaults to current module source)
            version_file: Name of the version file (default: VERSION)
            
        Returns:
            Updated directory with bumped version
            
        Example:
            dagger call bump-version --bump-type=patch export --path=.
            dagger call bump-version --bump-type=minor export --path=.
            dagger call bump-version --bump-type=major export --path=.
        """
        src = await self._get_source(source)
        
        # Read current version
        current_version, error = await self._read_version_file(src, version_file)
        if error:
            raise Exception(error)
        
        # Calculate new version
        new_version, error = self._bump_version_logic(current_version, bump_type.lower())
        if error:
            raise Exception(error)
        
        # Write new version
        updated_dir = src.with_new_file(version_file, new_version)
        
        return updated_dir

    @function
    async def release(
        self,
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing version files (defaults to current module)")
        ] = None,
        version_file: Annotated[
            str,
            Doc("Name of the source version file")
        ] = "VERSION",
        target_file: Annotated[
            str,
            Doc("Name of the target file to sync")
        ] = "galaxy.yml",
        version_pattern: Annotated[
            str,
            Doc("Regex pattern to match version line in target file")
        ] = r'^version:.*$',
        tag_message: Annotated[
            Optional[str],
            Doc("Custom git tag message (defaults to 'Release X.Y.Z')")
        ] = None
    ) -> str:
        """
        Complete release workflow: sync version, validate, and generate git commands.
        
        This function orchestrates the release process by:
        1. Syncing version from source to target file
        2. Validating consistency
        3. Generating git commands for manual execution
        
        Args:
            source: Source directory (defaults to current module source)
            version_file: Name of the source version file (default: VERSION)
            target_file: Name of the target file to sync (default: galaxy.yml)
            version_pattern: Regex pattern to match version line
            tag_message: Custom git tag message (optional)
            
        Returns:
            Release instructions with git commands
            
        Example:
            dagger call release
            dagger call release --tag-message="Major release with breaking changes"
        """
        src = await self._get_source(source)
        
        # Read version
        version, error = await self._read_version_file(src, version_file)
        if error:
            return error
        
        # Sync version
        try:
            updated_src = await self.sync_version(
                source=src,
                version_file=version_file,
                target_file=target_file,
                version_pattern=version_pattern
            )
            sync_msg = f"✅ Synced {version} → {target_file}"
        except Exception as e:
            return str(e)
        
        # Validate
        validation_msg = await self.validate_version(
            source=updated_src,
            version_file=version_file,
            target_file=target_file,
            version_pattern=version_pattern
        )
        
        # Generate git commands
        tag_msg = tag_message or f"Release {version}"
        
        result = f"""🚀 Release {version} Ready

{sync_msg}
{validation_msg}

Next steps (run these commands manually):

  git add {version_file} {target_file}
  git commit -m "Release {version}"
  git tag -a v{version} -m "{tag_msg}"
  git push && git push --tags

Note: Review changes before committing!
"""
        return result

    async def _detect_project_type(
        self,
        source: dagger.Directory
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Detect project type based on marker files.
        
        Args:
            source: Directory to check for marker files
            
        Returns:
            Tuple of (project_type, target_file, version_pattern) or (None, None, None)
        """
        # Priority order: Ansible > Python > Helm > Docker
        project_types = [
            ("galaxy.yml", "Ansible Collection", "galaxy.yml", r'^version:.*$'),
            ("pyproject.toml", "Python", "pyproject.toml", r'^version\s*=\s*".*"$'),
            ("Chart.yaml", "Helm", "Chart.yaml", r'^version:.*$'),
            ("Dockerfile", "Docker", "Dockerfile", r'LABEL version=".*"$'),
        ]
        
        for marker_file, project_type, target_file, pattern in project_types:
            try:
                await source.file(marker_file).contents()
                return project_type, target_file, pattern
            except Exception:
                continue
        
        return None, None, None

    def _generate_hook_content(
        self,
        hook_type: str,
        version: str,
        target_file: str,
        version_pattern: str
    ) -> str:
        """
        Generate git hook script content.
        
        Args:
            hook_type: Type of hook (pre-commit or pre-push)
            version: Current version for metadata header
            version: Module version for metadata
            target_file: Target file for validation
            version_pattern: Regex pattern for version matching
            
        Returns:
            Hook script content
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Escape pattern for shell
        escaped_pattern = version_pattern.replace('"', '\\"')
        
        hook_content = f"""#!/bin/bash
# DAGGER-VERSION-MANAGER: v{version}
# Installed: {timestamp}
#
# This hook validates version consistency before {hook_type.replace('-', ' ')}.
# Managed by Dagger Version Manager - DO NOT EDIT MANUALLY

echo "Checking version consistency..."

if ! dagger call version-manager validate-version \\
    --target-file={target_file} \\
    --version-pattern="{escaped_pattern}" 2>&1 | grep -q "✅"; then
    echo "❌ Version mismatch detected!"
    echo "Run: dagger call version-manager sync-version export --path=."
    exit 1
fi

echo "✅ Version check passed"
exit 0
"""
        return hook_content

    async def _check_existing_hook(
        self,
        source: dagger.Directory,
        hook_path: str
    ) -> tuple[bool, bool]:
        """
        Check if hook exists and if it's managed by dagger-version-manager.
        
        Args:
            source: Directory to check
            hook_path: Path to hook file (e.g., ".git/hooks/pre-commit")
            
        Returns:
            Tuple of (exists, is_managed)
        """
        try:
            content = await source.file(hook_path).contents()
            is_managed = "# DAGGER-VERSION-MANAGER:" in content
            return True, is_managed
        except Exception:
            return False, False

    @function
    async def setup_git_hooks(
        self,
        source: Annotated[
            Optional[dagger.Directory],
            Doc("Source directory containing project files (defaults to current module)")
        ] = None
    ) -> dagger.Directory:
        """
        Install git hooks for automated version validation.
        
        This function sets up pre-commit and pre-push hooks that enforce version
        consistency across project files. The hooks are automatically configured
        based on detected project type (Ansible, Python, Docker, or Helm).
        
        The hooks will:
        - Block commits/pushes if versions are inconsistent
        - Display helpful error messages
        - Suggest sync commands to fix issues
        
        Args:
            source: Source directory (defaults to current module source)
            
        Returns:
            Updated directory with git hooks installed
            
        Raises:
            Exception: If .git directory not found or project type cannot be detected
            
        Example:
            dagger call setup-git-hooks --source=. export --path=.
        """
        src = await self._get_source(source)
        
        # Check for .git directory
        try:
            await src.directory(".git").entries()
        except Exception:
            raise Exception(
                "❌ Git repository not found (.git directory missing)\n"
                "   Initialize git first: git init"
            )
        
        # Check if this is a Dagger module project
        try:
            await src.file("dagger.json").contents()
            # This is a Dagger module - skip hook installation
            raise Exception(
                "ℹ️  Detected Dagger module project\n"
                "\n"
                "Git hooks are designed for projects that CONSUME version-manager,\n"
                "not for the version-manager module itself.\n"
                "\n"
                "For this project, manage versions manually using:\n"
                "  - VERSION file only\n"
                "  - pyproject.toml should stay at version = \"0.0.0\"\n"
                "\n"
                "No hooks installed."
            )
        except Exception as e:
            # If the exception message contains our marker, re-raise it
            if "Detected Dagger module project" in str(e):
                raise e
            # Otherwise, it's just file not found - continue with normal flow
            pass
        
        # Detect project type
        project_type, target_file, version_pattern = await self._detect_project_type(src)
        
        if not project_type:
            raise Exception(
                "❌ Could not detect project type\n"
                "   Supported marker files:\n"
                "   - galaxy.yml (Ansible Collection)\n"
                "   - pyproject.toml (Python)\n"
                "   - Chart.yaml (Helm)\n"
                "   - Dockerfile (Docker)"
            )
        
        # Get current version for metadata
        version, error = await self._read_version_file(src, "VERSION")
        if error:
            raise Exception(error)
        
        # Check existing hooks
        hooks_to_install = [
            (".git/hooks/pre-commit", "pre-commit"),
            (".git/hooks/pre-push", "pre-push")
        ]
        
        warnings = []
        updated_dir = src
        
        for hook_path, hook_type in hooks_to_install:
            exists, is_managed = await self._check_existing_hook(updated_dir, hook_path)
            
            if exists and not is_managed:
                warnings.append(
                    f"⚠️  {hook_path} exists but is not managed by dagger-version-manager\n"
                    f"   Remove it manually if you want dagger-version-manager to manage it"
                )
                continue
            
            # Generate and install hook
            hook_content = self._generate_hook_content(
                hook_type, version, target_file, version_pattern
            )
            updated_dir = updated_dir.with_new_file(hook_path, hook_content, permissions=0o755)
        
        # Build success message
        if warnings:
            warning_msg = "\n\n" + "\n".join(warnings)
        else:
            warning_msg = ""
        
        # Note: We can't actually make the export message show here, but the returned
        # directory will have the hooks with proper permissions when exported
        return updated_dir