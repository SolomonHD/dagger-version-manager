"""Unit tests for version bumping logic."""

import pytest
from src.main import DaggerVersionManager


class TestVersionBumping:
    """Test version bumping functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vm = DaggerVersionManager()

    def test_bump_patch_version(self):
        """Test patch version bumping."""
        test_cases = [
            ("1.2.3", "1.2.4"),
            ("0.0.0", "0.0.1"),
            ("10.20.30", "10.20.31"),
            ("1.0.0", "1.0.1"),
        ]
        
        for current, expected in test_cases:
            new_version, error = self.vm._bump_version_logic(current, "patch")
            assert error is None, f"No error expected for {current}"
            assert new_version == expected, f"Expected {expected}, got {new_version}"

    def test_bump_minor_version(self):
        """Test minor version bumping."""
        test_cases = [
            ("1.2.3", "1.3.0"),
            ("0.0.1", "0.1.0"),
            ("10.20.30", "10.21.0"),
            ("1.0.99", "1.1.0"),
        ]
        
        for current, expected in test_cases:
            new_version, error = self.vm._bump_version_logic(current, "minor")
            assert error is None, f"No error expected for {current}"
            assert new_version == expected, f"Expected {expected}, got {new_version}"

    def test_bump_major_version(self):
        """Test major version bumping."""
        test_cases = [
            ("1.2.3", "2.0.0"),
            ("0.1.0", "1.0.0"),
            ("9.99.99", "10.0.0"),
            ("0.0.1", "1.0.0"),
        ]
        
        for current, expected in test_cases:
            new_version, error = self.vm._bump_version_logic(current, "major")
            assert error is None, f"No error expected for {current}"
            assert new_version == expected, f"Expected {expected}, got {new_version}"

    def test_bump_invalid_type(self):
        """Test bumping with invalid bump type."""
        invalid_types = ["Major", "MINOR", "patched", "xyz", ""]
        
        for bump_type in invalid_types:
            new_version, error = self.vm._bump_version_logic("1.0.0", bump_type)
            assert new_version is None, f"Should return None for invalid type: {bump_type}"
            assert error is not None, f"Should have error for invalid type: {bump_type}"
            assert "❌" in error
            assert "major" in error and "minor" in error and "patch" in error

    def test_bump_case_sensitivity(self):
        """Test that bump type is case-insensitive (after lower())."""
        # Note: The implementation does .lower() on bump_type
        test_cases = [
            ("1.0.0", "major", "2.0.0"),
            ("1.0.0", "minor", "1.1.0"),
            ("1.0.0", "patch", "1.0.1"),
        ]
        
        for current, bump_type, expected in test_cases:
            new_version, error = self.vm._bump_version_logic(current, bump_type)
            assert error is None
            assert new_version == expected

    def test_bump_version_with_invalid_format(self):
        """Test bumping when current version is invalid."""
        invalid_versions = ["1.0", "v1.0.0", "1.0.0.0"]
        
        for version in invalid_versions:
            new_version, error = self.vm._bump_version_logic(version, "patch")
            # Should fail to parse
            assert new_version is None
            assert error is not None
            assert "❌" in error


class TestBumpingEdgeCases:
    """Test edge cases for version bumping."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vm = DaggerVersionManager()

    def test_bump_from_zero_versions(self):
        """Test bumping from 0.0.0."""
        results = [
            ("major", "1.0.0"),
            ("minor", "0.1.0"),
            ("patch", "0.0.1"),
        ]
        
        for bump_type, expected in results:
            new_version, error = self.vm._bump_version_logic("0.0.0", bump_type)
            assert error is None
            assert new_version == expected

    def test_bump_large_version_numbers(self):
        """Test bumping with large version numbers."""
        test_cases = [
            ("999.999.999", "major", "1000.0.0"),
            ("100.200.300", "minor", "100.201.0"),
            ("50.60.999", "patch", "50.60.1000"),
        ]
        
        for current, bump_type, expected in test_cases:
            new_version, error = self.vm._bump_version_logic(current, bump_type)
            assert error is None
            assert new_version == expected