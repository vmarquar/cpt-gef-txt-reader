from gef_reader.gef_parser import read_byte_file, convert_to_number, parse_value
import pytest


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

