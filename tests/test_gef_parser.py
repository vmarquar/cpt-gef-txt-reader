import os
import pytest
from gef_parser import read_txt_file

def test_read_txt_file(tmp_path):
    # Create a temporary file with known content
    file_content = "Line 1\nLine 2\näöüß\n"
    file_path = tmp_path / "test_file.txt"
    file_path.write_text(file_content, encoding='utf-8')

    # Call the function
    lines, encoding = read_txt_file(str(file_path))

    # Assert the expected output
    assert lines == ["Line 1\n", "Line 2\n", "äöüß\n"]
    assert encoding == 'utf-8'

    # Test with a different encoding
    file_path.write_text(file_content, encoding='windows-1252')
    lines, encoding = read_txt_file(str(file_path))
    assert lines == ["Line 1\n", "Line 2\n", "Line 3\n"]
    assert encoding == 'windows-1252'

    # Test with an unsupported encoding
    file_path.write_bytes(file_content.encode('utf-16'))
    lines, encoding = read_txt_file(str(file_path))
    assert lines == []
    assert encoding is None
