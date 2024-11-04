import pandas as pd
import numpy as np
import glob
import os

def load_hydraulic_data(file_path, agg='mean'):
    try:
        # Load data from the file
        arr_data = np.genfromtxt(file_path)
        
        # Check if data was loaded successfully
        if arr_data.size == 0:
            raise ValueError("File is empty or not properly formatted.")

        # Aggregate data based on the specified aggregation function
        if agg == 'mean':
            agg_data = np.mean(arr_data, axis=1)
        elif agg == 'median':
            agg_data = np.median(arr_data, axis=1)
        else:
            raise ValueError("Invalid aggregation function. Choose 'mean' or 'median'.")

        return agg_data

    except IOError:
        print(f"Error: Could not read file {file_path}. Please check if the file exists and is accessible.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

def export_parquet(target_path, file_name,df):
    df.to_parquet(f"{target_path}/{file_name}.parquet", engine='pyarrow')