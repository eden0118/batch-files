"""Tests for FileRenamer class"""

import tempfile
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from batch_renamer.core.renamer import FileRenamer


class TestFileRenamer:
    """Test cases for FileRenamer"""

    def setup_method(self):
        """Setup test fixtures"""
        self.renamer = FileRenamer()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def teardown_method(self):
        """Cleanup test fixtures"""
        self.temp_dir.cleanup()

    def test_apply_conversion_s2t_fallback(self):
        """Test simplified to traditional conversion with fallback"""
        result = self.renamer.apply_conversion("国家", "s2t")
        assert result == "國家"

    def test_apply_conversion_replace(self):
        """Test text replacement"""
        result = self.renamer.apply_conversion(
            "hello_world",
            "replace",
            find_text="_",
            replace_text="-"
        )
        assert result == "hello-world"

    def test_apply_conversion_none(self):
        """Test no operation"""
        result = self.renamer.apply_conversion("test.txt", "none")
        assert result == "test.txt"

    def test_apply_formatting_file_with_prefix_suffix(self):
        """Test file formatting with prefix and suffix"""
        temp_file = self.temp_path / "test.txt"
        temp_file.touch()

        result = self.renamer.apply_formatting(
            temp_file,
            "test.txt",
            prefix="[",
            suffix="]",
            symbols=""
        )
        assert result == "[test].txt"

    def test_apply_formatting_remove_symbols(self):
        """Test removing symbols from filename"""
        temp_file = self.temp_path / "test@#$.txt"
        temp_file.touch()

        result = self.renamer.apply_formatting(
            temp_file,
            "test@#$.txt",
            prefix="",
            suffix="",
            symbols="@#$"
        )
        assert result == "test.txt"

    def test_scan_directory_empty(self):
        """Test scanning empty directory"""
        targets = self.renamer.scan_directory(
            self.temp_path,
            "files",
            "all",
            [],
            "none"
        )
        assert len(targets) == 0

    def test_scan_directory_with_files(self):
        """Test scanning directory with files"""
        # Create test files
        (self.temp_path / "国家.txt").touch()
        (self.temp_path / "文件.pdf").touch()

        targets = self.renamer.scan_directory(
            self.temp_path,
            "files",
            "all",
            [],
            "s2t"
        )

        assert len(targets) == 2
        # Check conversion happened
        assert any(new_name == "國家.txt" for _, new_name in targets)
        assert any(new_name == "文件.pdf" for _, new_name in targets)

    def test_scan_directory_filter_by_ext(self):
        """Test filtering by file extension"""
        # Create test files
        (self.temp_path / "file1.txt").touch()
        (self.temp_path / "file2.pdf").touch()
        (self.temp_path / "file3.txt").touch()

        targets = self.renamer.scan_directory(
            self.temp_path,
            "files",
            "ext",
            [".txt"],
            "none"
        )

        assert len(targets) == 2
        assert all(item.suffix == ".txt" for item, _ in targets)
