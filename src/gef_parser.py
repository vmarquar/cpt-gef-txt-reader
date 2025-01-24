"""
Author: V. Schweigl 
Creation date: 23.12.2024
License: MIT
"""
from io import BytesIO

def read_txt_file(file_path:str) -> tuple[list,str]:
    # 1) check encoding
    encoding = None
    for enc in ['windows-1252','utf-8', 'windows-1250']:
        try:    
            with open(file_path, encoding=enc) as f:
                lines = f.readlines()
                encoding = enc
                return(lines,encoding)
        except UnicodeDecodeError:
            print(f'got unicode error with {enc} , trying different encoding')

def read_byte_file(io_bytes: BytesIO) -> tuple[list,str]:
    """This helper functions reads the file content from a ioBytes files, that comes from e.g. a fastapi endpoint.

    Args:
        io_bytes (ioBytes): the uploaded file
    """
    # 1) check encoding
    encoding = None
    for enc in ['windows-1252','utf-8', 'windows-1250']:
        try:
            text_content_str = io_bytes.decode(enc)
            encoding = enc
            if ('\r\n' in text_content_str):
                lines = text_content_str.split('\r\n')
                return(lines,encoding)
            else:
                lines = text_content_str.split('\n')
                return(lines,encoding)

        except UnicodeDecodeError:
            print(f'got unicode error with {enc} , trying different encoding')

def extract_header_part(lines, header_sep = ':'):
    header = {}
    for index, line in enumerate(lines):
        if(header_sep in line):
            # all header lines contain a colon, e.g.
            # Projekt-Nummer: 20211234-123456
            # Projektname: Testprojekt ABC
            key, value = line.split(header_sep, maxsplit=1)
            key = key.rstrip().strip()
            value = value.rstrip().strip()
            try:
                value = float(value.replace(',','.'))
            except:
                value = value
            if(key):
                header[key] = value
        if(index > 50):
            # leave the loop after a maximum of 50 parameters/header lines
            break
    return(header)

def extract_alternative_header_part(lines):
    data_dict = {}
    for line in lines:
        if line.startswith('#'):
            # Remove the leading '#' and split the line by '='
            key, value = line.lstrip('#').split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle nested keys for repeated keys like COLUMNVOID, COLUMNINFO, etc.
            if key in data_dict:
                if isinstance(data_dict[key], list):
                    data_dict[key].append(value)
                else:
                    data_dict[key] = [data_dict[key], value]
            else:
                data_dict[key] = value
    
    # Further split values for each key where appropriate
    for key, value in data_dict.items():
        if isinstance(value, list):
            data_dict[key] = [parse_value(val) for val in value]
        else:
            data_dict[key] = parse_value(value)
    
    # Count header lines:
    header_lines = sum(1 for line in lines if line.startswith('#'))

    return data_dict, header_lines

def parse_value(value):
    parts = value.split(',')
    if len(parts) > 1:
        return [convert_to_number(part.strip()) for part in parts]
    else:
        return convert_to_number(value.strip())

def convert_to_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

def map_to_default_header_names(header, additional_mapping_dict={}):
    """
    This function maps the header columns to default names.
    Input:
        - header: dict of key value pairs
        - alternative_mapping_dict: alternative mapping dictionary,
            with key as header name read from the header file, maybe project specific
            value is the target value to be mapped to
            e.g. {"X":"RW", "Y": "HW", "Z":"ansatz_hoehe"}
    """
    default_mapping_dict = {
        # key: value read from header file; value: target value after mapping
        #TODO: check GEF Help Document for more!
        'Projekt-Nummer':'projekt_id',
        'Projektname':'projekt_name',
        'Versuchs-Nummer':'aufschluss_name',
        'Kundenname':'kunde',
        'Ort':'ort',
        'Datum':'datum',
        'Konus-Nummer':'konus_nummer',
        'Geländekante':'ansatz_hoehe',
        'Wasserspiegel':'gw_stand',
        'Vorbohrwerte':'vorbohrwerte',
        'E Coordinate':'RW',
        'N Coordinate':'HW',

        "Sondeerlengte":"depth",
        "Conusweerstand qc":"qc",
        "Wrijvingsweerstand fs":"fs",
        "Wrijvingsgetal Rf":"Rf",
        "Waterspanning u2":"u2",
        "Helling X":"inclination_x",
        "Helling Y":"inclination_y",
        "Gecorrigeerde diepte":"depth_corr",
        "Tijd":"time",
        "TESTID":"hole_id",
        "penetration length":"depth",
        "qc":"qc",
        "fs":"fs",
        "SampleTime":"time",
        "Rf":"Rf",
    }
    # extend the dict by additional and alternative dicts (existing keys will be overwritten!)
    mapping_dict = {**default_mapping_dict, **additional_mapping_dict}
    header_renamed = {}
    if isinstance(header, dict):
        for k in header.keys():
            try:
                header_renamed[mapping_dict[k]] = header[k]
            except KeyError:
                header_renamed[k] = header[k]

    elif isinstance(header, list):
        for k in header:
            try:
                header_renamed[mapping_dict[k]] = k
            except KeyError:
                header_renamed[k] = k

    return(header_renamed)
    
def read_measurement_headers(lines, skip_lines=0):
    _header = None
    _header_line_uncleaned = None
    _header_units = {}
    _measurements = []
    for line in lines[skip_lines:]:
        line_cleaned = ' '.join(line.strip().rstrip().split()) # remove additional whitespaces        
        if(line_cleaned != '' and _header == None and '[' not in line_cleaned):
            _header = line_cleaned.split(' ')
            _header_line_uncleaned = line
        elif(line_cleaned != '' and '[' in line_cleaned and _header_units == {}):
            start_indeces = [i for i,c in enumerate(line) if c == '[']
            for start_index in start_indeces:
                _header_col_name = _header_line_uncleaned[start_index:].split(' ',maxsplit=1)[0].strip()
                _header_col_unit = line[start_index:].split(' ',maxsplit=1)[0].strip()
                _header_units[_header_col_name] = _header_col_unit
        elif(line_cleaned != ''):
            cleaned_values = {}
            for col_i, value in enumerate(line_cleaned.split(' ')):
                if(value == 'UNDEF' or value == '-99999.000'):
                    value = None
                else:
                    try:
                        value = float(value.replace(',','.'))
                    except:
                        value = value
                cleaned_values[_header[col_i]] = value
            _measurements.append(cleaned_values)

    # add missing keys in unit dict
    [_header_units.update({h:'[-]'}) for h in _header if _header_units.get(h) == None] # caution: will update the dict inplace!
    return(_header, _header_units, _measurements)

def read_alt_measurements(txt_lines, column_names, skip_lines):
    _measurements = []

    for line in txt_lines[skip_lines:]:
        dict_per_row = {}
        line_cleaned = ' '.join(line.strip().rstrip().split())
        for col_i, value in enumerate(line_cleaned.split(' ')):
            if(value == 'UNDEF' or value == '-99999.000'):
                value = None
            else:
                try:
                    value = float(value.replace(',','.'))
                except:
                    value = value
            dict_per_row[column_names[col_i]] = value
        _measurements.append(dict_per_row)
    return(_measurements)

def read_alt_gef_file(file_path : str = None,  file_bytes : bytes = None, header_mapping_dict:dict={}):
    if(file_path is not None):
        txt_lines, encoding = read_txt_file(file_path)
    elif(file_bytes is not None):
        txt_lines, encoding = read_byte_file(file_bytes)

    # 1) Extract header
    header_dict, header_lines = extract_alternative_header_part(txt_lines)
    column_names = [c[2] for c in header_dict.get("COLUMNINFO")]
    header_units = [c[1] for c in header_dict.get("COLUMNINFO")]
    renamed_header = map_to_default_header_names(column_names)
    renamed_cols = [k for k in renamed_header.keys()]
    measurements = read_alt_measurements(txt_lines=txt_lines, column_names=renamed_cols, skip_lines=header_lines)
    if("SampleTime" in measurements[0].keys()):
        print("ok")
        pass
    return(header_dict, header_units, measurements)

def read_gef_file(file_path : str = None,  file_bytes : bytes = None, header_mapping_dict: dict = {}):
    """
    This function reads a .gef.txt file, checks encoding and maps it do a default column schema.
    It returns a list of dictionary values for each data row, that can easily imported into pandas/numpy.
    Pure python3 implementation without any dependencies, that only takes around 0.01 seconds for a normally sized .gef.txt file

    Parameters
    ----------
    file_path : str
        path to the .gef.txt file
    header_mapping_dict : dict
        Dictionary that defines the renaming of the cpt header information
        Define the dict key as header name read from the header file --> maybe project specific
        Define the dict value as the target value to be mapped to
        e.g. {"X":"RW", "Y": "HW", "Z":"ansatz_hoehe"}
    Returns
    -------
    cpt_header_data: {}
        A dictionary containing all the header information about the cpt,
        e.g. X/Y Coordinates and hole_id.
        >> the naming convention can be overwritten by providing the header_mapping_dict param.
    header_units: 
        the units of the header
    measurements: [{},{},...]
        An array of dictionaries of all cpt measurements, e.g. qc, fs, etc.
        one dictionary for one data row (usually 1cm in depth).

    """
    if(file_path is not None):
        txt_lines, encoding = read_txt_file(file_path)
    elif(file_bytes is not None):
        txt_lines, encoding = read_byte_file(file_bytes)
    cpt_header_data = extract_header_part(txt_lines)
    cpt_renamed_header = map_to_default_header_names(cpt_header_data, additional_mapping_dict=header_mapping_dict)
    column_names, header_units, measurements = read_measurement_headers(txt_lines, skip_lines=len(cpt_renamed_header))
    return(cpt_renamed_header, header_units, measurements)