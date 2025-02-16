import tempfile
from pathlib import Path

### HELPER FUNCTIONS FOR AUTOMATED TESTS
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

def create_example_file() -> tuple[str, dict, list, dict, list]:
    """ This function creates the beginning of a cpt .GEF.txt file as a dummy input together with its expected parsed output.
        Returns:
        (example_header_input, expected_header_output)
    """
    example_file_content = """Projekt-Nummer: 12345678-10001
    Projektname: Testsite
    Versuchs-Nummer: CPT 01
    Kundenname: 
    Ort: Testsite
    Datum: 01.01.2022
    Konus-Nummer: S15CFIIP.S99999
    Geländekante: -100,0
    Wasserspiegel: 0,00
    Vorbohrwerte: 0,00
    N Coordinate: 0,000
    E Coordinate: 0,000
    
    Tiefe     qc        fs        u2        I         Rf        ic        Su_min    Su_max    soilfr    soilbq    soilavg   IFA       
              [MPa]     [MPa]     [MPa]     [°]       [%]                 [kPa]     [kPa]                                   [°]       
    
    0,00      0,01      0,000     0,000     1,6       0,02      2,70      0,271     0,452     4,0       5,0       4,0       UNDEF     
    0,01      0,66      0,006     0,013     1,8       0,60      1,17      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,02      1,30      0,006     0,029     1,6       0,50      0,85      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,03      1,87      0,006     0,041     1,6       0,45      0,70      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,04      2,16      0,006     0,043     1,4       0,40      0,63      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,05      2,13      0,006     0,043     1,5       0,37      0,64      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,06      2,13      0,006     0,042     1,5       0,34      0,65      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,07      2,13      0,006     0,041     1,4       0,32      0,67      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,08      2,13      0,006     0,040     1,5       0,33      0,72      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,09      2,13      0,007     0,039     1,6       0,35      0,77      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,10      2,13      0,007     0,039     1,6       0,35      0,78      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,11      2,16      0,007     0,038     1,5       0,35      0,79      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,12      2,14      0,007     0,038     1,4       0,36      0,80      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,13      2,08      0,007     0,038     1,5       0,36      0,83      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,14      1,93      0,007     0,038     1,6       0,37      0,89      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,15      1,86      0,007     0,037     1,6       0,39      0,94      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
    0,16      1,79      0,008     0,037     1,5       0,43      1,00      UNDEF     UNDEF     7,0       7,0       7,0       50,090    
    0,17      1,68      0,009     0,003     1,4       0,50      1,10      UNDEF     UNDEF     7,0       7,0       7,0       49,640    
    0,18      1,69      0,021     0,002     1,3       1,22      1,45      UNDEF     UNDEF     6,0       7,0       6,0       49,480       
    """
    expected_header_output = {
        'Projekt-Nummer': '12345678-10001',
        'Projektname': 'Testsite',
        'Versuchs-Nummer': 'CPT 01',
        'Kundenname': '',
        'Ort': 'Testsite',
        'Datum': '01.01.2022',
        'Konus-Nummer': 'S15CFIIP.S99999',
        'Geländekante': -100.0,
        'Wasserspiegel': 0.0,
        'Vorbohrwerte': 0.0,
        'N Coordinate': 0.0,
        'E Coordinate': 0.0
    }

    expected_col_names = [
        "Tiefe",
        "qc",
        "fs",
        "u2",
        "I",
        "Rf",
        "ic",
        "Su_min",
        "Su_max",
        "soilfr",
        "soilbq",
        "soilavg",
        "IFA",
    ]
    expected_header_units = {
        "qc": "[MPa]",
        "fs": "[MPa]",
        "u2": "[MPa]",
        "I": "[°]",
        "Rf": "[%]",
        "Su_min": "[kPa]",
        "Su_max": "[kPa]",
        "IFA": "[°]",
        "Tiefe": "[-]",
        "ic": "[-]",
        "soilfr": "[-]",
        "soilbq": "[-]",
        "soilavg": "[-]",
    }

    expected_measurements = [{'Tiefe': 0.0, 'qc': 0.01, 'fs': 0.0, 'u2': 0.0, 'I': 1.6, 'Rf': 0.02, 'ic': 2.7, 'Su_min': 0.271, 'Su_max': 0.452, 'soilfr': 4.0, 'soilbq': 5.0, 'soilavg': 4.0, 'IFA': None},
                            {'Tiefe': 0.01, 'qc': 0.66, 'fs': 0.006, 'u2': 0.013, 'I': 1.8, 'Rf': 0.6, 'ic': 1.17, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.02, 'qc': 1.3, 'fs': 0.006, 'u2': 0.029, 'I': 1.6, 'Rf': 0.5, 'ic': 0.85, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.03, 'qc': 1.87, 'fs': 0.006, 'u2': 0.041, 'I': 1.6, 'Rf': 0.45, 'ic': 0.7, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.04, 'qc': 2.16, 'fs': 0.006, 'u2': 0.043, 'I': 1.4, 'Rf': 0.4, 'ic': 0.63, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.05, 'qc': 2.13, 'fs': 0.006, 'u2': 0.043, 'I': 1.5, 'Rf': 0.37, 'ic': 0.64, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.06, 'qc': 2.13, 'fs': 0.006, 'u2': 0.042, 'I': 1.5, 'Rf': 0.34, 'ic': 0.65, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.07, 'qc': 2.13, 'fs': 0.006, 'u2': 0.041, 'I': 1.4, 'Rf': 0.32, 'ic': 0.67, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.08, 'qc': 2.13, 'fs': 0.006, 'u2': 0.04, 'I': 1.5, 'Rf': 0.33, 'ic': 0.72, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.09, 'qc': 2.13, 'fs': 0.007, 'u2': 0.039, 'I': 1.6, 'Rf': 0.35, 'ic': 0.77, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.1, 'qc': 2.13, 'fs': 0.007, 'u2': 0.039, 'I': 1.6, 'Rf': 0.35, 'ic': 0.78, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.11, 'qc': 2.16, 'fs': 0.007, 'u2': 0.038, 'I': 1.5, 'Rf': 0.35, 'ic': 0.79, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.12, 'qc': 2.14, 'fs': 0.007, 'u2': 0.038, 'I': 1.4, 'Rf': 0.36, 'ic': 0.8, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.13, 'qc': 2.08, 'fs': 0.007, 'u2': 0.038, 'I': 1.5, 'Rf': 0.36, 'ic': 0.83, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.14, 'qc': 1.93, 'fs': 0.007, 'u2': 0.038, 'I': 1.6, 'Rf': 0.37, 'ic': 0.89, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.15, 'qc': 1.86, 'fs': 0.007, 'u2': 0.037, 'I': 1.6, 'Rf': 0.39, 'ic': 0.94, 'Su_min': None, 'Su_max': None, 'soilfr': 0.0, 'soilbq': 0.0, 'soilavg': 0.0, 'IFA': None},
                            {'Tiefe': 0.16, 'qc': 1.79, 'fs': 0.008, 'u2': 0.037, 'I': 1.5, 'Rf': 0.43, 'ic': 1.0, 'Su_min': None, 'Su_max': None, 'soilfr': 7.0, 'soilbq': 7.0, 'soilavg': 7.0, 'IFA': 50.09},
                            {'Tiefe': 0.17, 'qc': 1.68, 'fs': 0.009, 'u2': 0.003, 'I': 1.4, 'Rf': 0.5, 'ic': 1.1, 'Su_min': None, 'Su_max': None, 'soilfr': 7.0, 'soilbq': 7.0, 'soilavg': 7.0, 'IFA': 49.64},
                            {'Tiefe': 0.18, 'qc': 1.69, 'fs': 0.021, 'u2': 0.002, 'I': 1.3, 'Rf': 1.22, 'ic': 1.45, 'Su_min': None, 'Su_max': None, 'soilfr': 6.0, 'soilbq': 7.0, 'soilavg': 6.0, 'IFA': 49.48}]

    return(example_file_content, expected_header_output, expected_col_names, expected_header_units, expected_measurements)
