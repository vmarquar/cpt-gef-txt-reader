import pytest
from .helper_functions import create_dummy_test_file, create_example_file

from gef_reader.gef_reader import (
    read_byte_file,
    convert_to_number,
    read_txt_file,
    extract_header_part,
    map_to_default_header_names,
    read_measurement_headers
)


### TEST FUNCTIONS

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

def test_read_txt_file():
    # Create a temporary file with known content and encoding
    file_content = "Line 1\nLine 2\näöüß\n"
    file_path = create_dummy_test_file(file_content, "utf-8")

    # Call the function
    lines, encoding = read_txt_file(file_path, encodings=['utf-8'])

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

def test_extract_header_part():
    example_file_content, expected_header, expected_col_names, expected_header_units, expected_measurements = create_example_file()
    lines = example_file_content.split('\n')
    header = extract_header_part(lines=lines, header_sep=':')
    assert header == expected_header, f"{header} - The extracted header does not match the expected output."

def test_map_to_default_header_names():
    example_file_content, expected_header, expected_col_names, expected_header_units, expected_measurements = create_example_file()
    header_with_default_names = map_to_default_header_names(header=expected_header)

    expected_default_keys = [
        "projekt_id",
        "projekt_name",
        "aufschluss_name",
        "kunde",
        "ort",
        "datum",
        "konus_nummer",
        "ansatz_hoehe",
        "gw_stand",
        "vorbohrwerte",
        "HW",
        "RW",
    ]
    assert all([True for k in header_with_default_names.keys() if k in expected_default_keys]) == True, "At least one of the keys is not mapped to its default naming."

def test_read_measurement_headers():
    example_file_content, expected_header, expected_col_names, expected_header_units, expected_measurements = create_example_file()
    lines = example_file_content.split('\n')
    column_names, header_units, measurements = read_measurement_headers(lines, skip_lines=len(expected_header))
    assert column_names == expected_col_names, "Error in the column names"
    assert header_units == expected_header_units, "Error in the header units"
    assert measurements == expected_measurements, "Error in the measurements"
