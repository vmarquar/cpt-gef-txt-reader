# CPT-Parser (.gef.txt Files)
A simple pure-python implementation to parse .gef.txt files / CPT measurement data in ASCII format.
Cone penetration tests (CPT) are a very common way of doing ground surveys.

The file format .gef.txt is based on the geotechnical exchange format (GEF) defintions and is very common to represent CPT test data. This repo shows a simple and efficient way of importing this data to a python dictionary/array. This array can easily imported as a pandas Dataframe or plotted with matplotlib.


## 1) Usage / Installation
1. Copy the `gef_parser.py` file to your project
2. Inside your python project import the parser function: `from gef_parser import read_gef_file`
3. No dependencies or additional installs are needed to parse .gef.txt files

## 2) File Structure of a .gef.txt file

Header Information and beginning of the measurements of the CPT Test:
```
Projekt-Nummer: 12345678-12345
Projektname: Musterstadt, Drucksondierkampagne XYZ
Versuchs-Nummer: CPTU1
Kundenname: -
Ort: 12345 Musterstadt
Datum: 07.05.2023
Konus-Nummer: S22ABCDEF.S221234
Geländekante: 0,00
Wasserspiegel: 0,00
Vorbohrwerte: 0,00
E Coordinate: 0,000
N Coordinate: 0,000

Tiefe     qc        fs        u2        I         Rf        ic        Su_min    Su_max    soilfr    soilbq    soilavg   IFA       
          [MPa]     [MPa]     [MPa]     [°]       [%]                 [kPa]     [kPa]                                   [°]       

0,00      0,60      0,000     0,000     1,0       0,00      4,00      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
0,01      0,60      0,000     0,000     1,4       0,00      4,00      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
0,02      0,67      0,000     0,000     1,5       0,01      0,64      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
0,03      0,75      0,000     0,000     1,4       0,02      0,46      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
0,04      0,89      0,000     0,000     1,9       0,03      0,35      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
0,05      1,04      0,001     0,000     1,7       0,06      0,36      UNDEF     UNDEF     0,0       0,0       0,0       UNDEF     
```



## 3) Examples to parse .gef.txt files
> All code examples are located in `./example_usage.py` as well.

### Example 1: Parse a single file
```python
from gef_parser import read_gef_file
# Example 1: Parse a single file
file_path = './sample_cptu_file.GEF.txt'
cpt_header, measurement_columns_and_units, measurements = read_gef_file(file_path)

print(measurements)
print(cpt_header)
print(measurement_columns_and_units)
```

### Example 2: Create a pandas Dataframe from a single file
Parse a single file, create a pandas dataframe from the measurements and create a plot
```python
import pandas as pd
import matplotlib.pyplot as plt

file_path = './sample_cptu_file.GEF.txt'
cpt_header, measurement_columns_and_units, measurements = read_gef_file(file_path)

# ## Create a pandas df from it and plot qc vs. depth
df = pd.DataFrame.from_dict(measurements)

# ## Data can easily be plotted
plt.plot(df['qc'], df['Tiefe'])
plt.gca().invert_yaxis()
plt.xlabel("qc [MPa]")
plt.ylabel("Depth [m]")
plt.show()
```

### Example 3: Read multiple .gef.txt files in a folder

This example code parses all .gef.txt files in a folder and subfolders. Then it creates a big pandas data-frame of the measurement data and associated cpt header data. Finally it exports the data into a single Excel file. The two tables can easily imported into Leapfrog works for geological modelling.
```python
# Parse all *.gef.txt files in the GEF_SAMPLES folder
from glob import glob
folder_path = './GEF_SAMPLES/**/*.GEF.txt'
all_measurements = []
all_cpt_header_info = []
for file_path in glob(folder_path):
    cpt_header, measurement_columns_and_units, measurements = read_gef_file(file_path)
    measurements = [dict(item, **{'aufschluss_name':cpt_header['aufschluss_name']}) for item in measurements] # add aufschluss_name to the measurements
    all_measurements += measurements
    all_cpt_header_info.append(cpt_header)

## optionally add them to a pd.Dataframe and export it to a single excel file
import pandas as pd
header_df = pd.DataFrame.from_dict(all_cpt_header_info)
measurements_df = pd.DataFrame.from_dict(all_measurements)
excel_outpath = './CPT_Summary.xlsx'

# depending on the ampount of cpt measurement data the excel file can take some time
with pd.ExcelWriter(excel_outpath) as writer:
    header_df.to_excel(writer, sheet_name="Sheet0_cpt_header_info", index=False)
    measurements_df.to_excel(writer, sheet_name="Sheet1_cpt_measurements", index=False)

# optionally export the data into two csv files that can be imported into Leapfrog Works
header_df.to_csv('collar.csv')
measurements_df.to_csv('intervals.csv')
```

### Example 4: Read multiple .gef.txt files in a folder and create a thiessen-polygon and a delauny triangulation
This example code parses all .gef.txt files in a folder and subfolders. Then it creates a list of all input xyz coordinates and computes a delauny triangulation and thiessen/voronoi polygons. You can export the polygons into a shapefile/wkt-csv file to view it in QGIS etc.

```python
# Example 4: Create Thiessen Polygons and a Delauny triangulation from CPT xyz-Coordinates
from glob import glob
folder_path = './GEF_SAMPLES/**/*.GEF.txt'
all_measurements = []
all_cpt_header_info = []
for file_path in glob(folder_path):
    cpt_header, measurement_columns_and_units, measurements = read_gef_file(file_path)
    measurements = [dict(item, **{'aufschluss_name':cpt_header['aufschluss_name']}) for item in measurements] # add aufschluss_name to the measurements
    all_measurements += measurements
    all_cpt_header_info.append(cpt_header)

# Create Delauny and Thiessen Polygons
default_points = [(0,0,0),(5,5,0),(5,0,0), (10,3,2)]
points = [(cpt.get('RW'), cpt.get('HW')) for cpt in all_cpt_header_info if(cpt.get('RW') is not None and cpt.get('HW') is not None)]
if(len(points)==0):
    points = default_points

triangle_polygons = pytess_triangulate(points)
print(triangle_polygons)

thiessen_polygons = pytess_voronoi(points, buffer_percent=100)
print(thiessen_polygons)

print("...do some stuff with the triangulation")
```
