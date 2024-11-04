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

# Create the benchmark information dataframe

benchmark_description = {
    "Benchmark": [
        "Cooler condition", "Cooler condition", "Cooler condition",
        "Valve condition", "Valve condition", "Valve condition", "Valve condition",
        "Internal pump leakage", "Internal pump leakage", "Internal pump leakage",
        "Hydraulic accumulator", "Hydraulic accumulator", "Hydraulic accumulator", "Hydraulic accumulator",
        "Stable flag", "Stable flag"
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

# Create all features dataframe

directory_path = 'Data/Features'
all_files = [os.path.splitext(file_name)[0] for file_name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file_name)) and file_name.endswith('.txt')]

feature_df = {}
for file in all_files:
    file_path = f"{directory_path}/{file}.txt"
    feature_df[f"{file}_df"] = load_hydraulic_data(file_path)

