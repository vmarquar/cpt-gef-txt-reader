import pytest
import tempfile
from pathlib import Path

from gef_reader.gef_parser import read_byte_file, convert_to_number, parse_value, read_txt_file


# test the number conversion
@pytest.mark.parametrize("input_value, expected_output", [
    ("1.0", 1.0),
    ("1", 1),
    ("1.0E-3", 1.0E-3),
    ("1.0E+3", 1.0E+3),
    ("1.0E3", 1.0E3),
    ("1,0", "1,0")
])
def test_convert_to_number(input_value, expected_output):
    assert convert_to_number(input_value) == expected_output


def create_dummy_test_file(content: str, encoding: str) -> Path:
    """Creates a dummy test file with the specified content and encoding using tempfile.

    Args:
        content (str): The content to write to the file.
        encoding (str): The encoding to use when writing the file.

    Returns:
        Path: The path to the created temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding=encoding)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)

def test_read_txt_file():
    # Create a temporary file with known content and encoding
    file_content = "Line 1\nLine 2\näöüß\n"
    file_path = create_dummy_test_file(file_content, "utf-8")
    
    # Call the function
    lines, encoding = read_txt_file(file_path)

    # Assert the expected output
    assert lines == ["Line 1\n", "Line 2\n", "äöüß\n"], f"{lines} - The content of the lines does not match the expected output."
    assert encoding == 'utf-8' 

    # # Test with a different encoding
    # file_path = create_dummy_test_file(file_content, "windows-1252")
    # lines, encoding = read_txt_file(file_path)
    # assert lines == ["Line 1\n", "Line 2\n", "Line 3\n"]
    # assert encoding == 'windows-1252'

    # # Test with an unsupported encoding
    # file_path = create_dummy_test_file(file_content, "utf-16")
    # lines, encoding = read_txt_file(file_path)
    # assert lines == []
    # assert encoding is None

if __name__ == "__main__":
    pytest.main()