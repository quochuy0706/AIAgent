from PrdMAgent.Libraries import *

# Create the attribute information dataframe
attribute_information = {
    "Sensor": ["PS1", "PS2", "PS3", "PS4", "PS5", "PS6", "EPS1", "FS1", "FS2", "TS1", "TS2", "TS3", "TS4", "VS1", "CE", "CP", "SE"],
    "Physical quantity": ["Pressure", "Pressure", "Pressure", "Pressure", "Pressure", "Pressure", "Motor power", "Volume flow", "Volume flow",
                          "Temperature", "Temperature", "Temperature", "Temperature", "Vibration", "Cooling efficiency (virtual)",
                          "Cooling power (virtual)", "Efficiency factor"],
    "Unit": ["bar", "bar", "bar", "bar", "bar", "bar", "W", "l/min", "l/min", "°C", "°C", "°C", "°C", "mm/s", "%", "kW", "%"],
    "Sampling rate": ["100 Hz", "100 Hz", "100 Hz", "100 Hz", "100 Hz", "100 Hz", "100 Hz", "10 Hz", "10 Hz", "1 Hz", "1 Hz", "1 Hz", "1 Hz", "1 Hz", "1 Hz", "1 Hz", "1 Hz"]
}

attr_df = pd.DataFrame(attribute_information)
export_parquet('Data/Silver', 'attribute_information', attr_df)


# Create the benchmark information dataframe
benchmark_description = {
    "Benchmark": [
        "Cooler_condition", "Cooler_condition", "Cooler_condition",
        "Valve_condition", "Valve_condition", "Valve_condition", "Valve_condition",
        "Internal_pump_leakage", "Internal_pump_leakage", "Internal_pump_leakage",
        "Hydraulic_accumulator", "Hydraulic_accumulator", "Hydraulic_accumulator", "Hydraulic_accumulator",
        "Stable_flag", "Stable_flag"
    ],
    "Value": [
        3, 20, 100,
        100, 90, 80, 73,
        0, 1, 2,
        130, 115, 100, 90,
        0, 1
    ],
    "Description": [
        "close to total failure", "reduced efficiency", "full efficiency",
        "optimal switching behavior", "small lag", "severe lag", "close to total failure",
        "no leakage", "weak leakage", "severe leakage",
        "optimal pressure", "slightly reduced pressure", "severely reduced pressure", "close to total failure",
        "conditions were stable", "static conditions might not have been reached yet"
    ]
}

benchmark_df = pd.DataFrame(benchmark_description)
export_parquet('Data/Silver', 'benchmark_df', benchmark_df)

# Create hydraulic dataframe
feature_directory_path = 'Data/Features'
all_files = [os.path.splitext(file_name)[0] for file_name in os.listdir(feature_directory_path) if os.path.isfile(os.path.join(feature_directory_path, file_name)) and file_name.endswith('.txt')]

feature_df = pd.DataFrame()

for file in all_files:
    file_path = f"{feature_directory_path}/{file}.txt"
    arr = load_hydraulic_data(file_path, 'mean')
    feature_df[file] = arr 

# Create label dataframe 
label_df = pd.read_csv('Data/Target/profile.txt', sep='\s+', header=None)
label_column = {
    0: 'Cooler_condition',
    1: 'Valve_condition',
    2: 'Internal_pump_leakage',
    3: 'Hydraulic_accumulator',
    4: 'Stable_flag'
}
label_df.rename(columns=label_column, inplace=True)

# Concat feature and label into one dataframe
hydraulic_df = pd.concat([feature_df, label_df], axis=1)
# Export to Parquet file for re-used purpose 
export_parquet('Data/Silver', 'hydraulic_df', hydraulic_df)






