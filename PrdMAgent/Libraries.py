import pandas as pd
import glob
import os

def load_hydraulic_data(file_path):
    # Load data from a single file with whitespace delimiter and no header
    df = pd.read_csv(file_path, sep='\s+', header=None)
    # Determine the number of columns in the file
    num_columns = df.shape[1]
    # Assign column names based on the number of columns
    df.columns = list(range(1, num_columns + 1))
    # Add a column for load cycle ID
    df['CycleID'] = range(1, df.shape[0] + 1)
    # Reorder columns to place "CycleID" as the first column
    df = df[['CycleID'] + list(range(1, num_columns + 1))]
    return df
