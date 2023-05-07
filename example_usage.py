from gef_parser import read_gef_file


if __name__ == '__main__':

    # Example 1: Parse a single file
    file_path = './sample_cptu_file.GEF.txt'
    cpt_header, measurement_columns_and_units, measurements = read_gef_file(file_path)
    
    print(measurements)
    print(cpt_header)
    print(measurement_columns_and_units)





    # Example 2: Parse a single file and create a pandas dataframe from the measurements
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





    # Example 3: Read all .gef.txt files in a folder and create a big pandas df of the measurement data
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