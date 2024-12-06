import os
from PyTaskHelper.file_utils import find_duplicate_files

def test_find_duplicate_files(tmp_path):
    # Create duplicate files
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("Hello")
    file2.write_text("Hello")
    
    duplicates = find_duplicate_files(tmp_path)
    assert len(duplicates) == 1
