"""Unit tests for version validation logic."""

import pytest
from src.main import DaggerVersionManager


class TestVersionValidation:
    """Test semantic version validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vm = DaggerVersionManager()

    def test_validate_semver_valid_versions(self):
        """Test validation of valid semantic versions."""
        valid_versions = [
            "1.0.0",
            "0.0.1",
            "10.20.30",
            "999.999.999",
        ]
        
        for version in valid_versions:
            is_valid, error = self.vm._validate_semver(version)
            assert is_valid, f"Version {version} should be valid"
            assert error == "", f"No error expected for {version}"

    def test_validate_semver_invalid_versions(self):
        """Test validation of invalid semantic versions."""
        invalid_versions = [
            "1.0",           # Missing patch
            "1",             # Missing minor and patch
            "1.0.0.0",       # Too many components
            "v1.0.0",        # Has 'v' prefix
            "1.0.0-alpha",   # Has pre-release tag
            "1.0.0+build",   # Has build metadata
            "a.b.c",         # Non-numeric
            "1.0.x",         # Contains non-numeric
        ]
        
        for version in invalid_versions:
            is_valid, error = self.vm._validate_semver(version)
            assert not is_valid, f"Version {version} should be invalid"
            assert "❌" in error, f"Error message should contain ❌ for {version}"
            assert "expected X.Y.Z" in error

    def test_validate_semver_with_whitespace(self):
        """Test validation handles whitespace correctly."""
        versions_with_whitespace = [
            "  1.0.0  ",
            "\n1.0.0\n",
            "\t1.0.0\t",
        ]
        
        for version in versions_with_whitespace:
            is_valid, error = self.vm._validate_semver(version)
            assert is_valid, f"Version with whitespace should be valid: {repr(version)}"
            assert error == ""


class TestVersionExtraction:
    """Test version extraction from target files."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vm = DaggerVersionManager()

    def test_extract_version_from_yaml(self):
        """Test extracting version from YAML format."""
        content = """
name: my-collection
version: 1.2.3
author: test
"""
        pattern = r'^version:.*$'
        version = self.vm._extract_version_from_target(content, pattern)
        assert version == "1.2.3"

    def test_extract_version_from_toml(self):
        """Test extracting version from TOML format."""
        content = """
[project]
name = "my-project"
version = "2.0.5"
"""
        pattern = r'^version\s*=\s*".*"$'
        version = self.vm._extract_version_from_target(content, pattern)
        assert version == "2.0.5"

    def test_extract_version_from_dockerfile(self):
        """Test extracting version from Dockerfile."""
        content = """
FROM python:3.11
LABEL version="3.0.1"
LABEL maintainer="test"
"""
        pattern = r'LABEL version=".*"'
        version = self.vm._extract_version_from_target(content, pattern)
        assert version == "3.0.1"

    def test_extract_version_not_found(self):
        """Test extraction when pattern doesn't match."""
        content = """
name: my-collection
author: test
"""
        pattern = r'^version:.*$'
        version = self.vm._extract_version_from_target(content, pattern)
        assert version is None

    def test_extract_version_no_version_number(self):
        """Test extraction when line matches but has no version."""
        content = """
version: unknown
"""
        pattern = r'^version:.*$'
        version = self.vm._extract_version_from_target(content, pattern)
        assert version is None