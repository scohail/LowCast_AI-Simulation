import h5py
import pandas as pd
import os

# File path
file_path = "/home/scohail/Desktop/LowCast_AI-Simulation/Procast/Cube.erfh5"
output_dir = "/home/scohail/Desktop/LowCast_AI-Simulation/Data/cube"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open the HDF5 file
with h5py.File(file_path, "r") as f:
    post_group = f["post"]

    # Load the COORDINATE dataset (common for all states)
    coordinate_path = "/post/constant/entityresults/NODE/COORDINATE/erfblock/res"
    coordinates = pd.DataFrame(f[coordinate_path][()], columns=["X", "Y", "Z"])
    
    # Get all states
    singlestate_group = f["/post/singlestate"]
    state_keys = list(singlestate_group.keys())

    # Iterate through each state
    for state in state_keys:
        state_path = f"/post/singlestate/{state}/entityresults/NODE/"
        
        try:
            # Load Temperature and remove the first row
            temperature_path = f"{state_path}Temperature/ZONE1_set1/erfblock/res"
            temperature = pd.DataFrame(f[temperature_path][()], columns=["Temperature(K)"])[1:]  # Skip first row
            
            # Load Fraction Solid and remove the first row
            fraction_solid_path = f"{state_path}Fraction Solid/ZONE1_set1/erfblock/res"
            fraction_solid = pd.DataFrame(f[fraction_solid_path][()], columns=["Fraction Solid"])[1:]  # Skip first row
            
            # Reset index to align with COORDINATE dataset
            temperature.reset_index(drop=True, inplace=True)
            fraction_solid.reset_index(drop=True, inplace=True)
            coordinates_trimmed = coordinates.iloc[1:].reset_index(drop=True)

            # Concatenate COORDINATE, Temperature, and Fraction Solid
            combined_df = pd.concat([coordinates_trimmed, temperature, fraction_solid], axis=1)
            
            # Save to CSV
            output_file = os.path.join(output_dir, f"{state}.csv")
            combined_df.to_csv(output_file, index=False)
            
            print(f"Saved {output_file}")
        
        except KeyError as e:
            print(f"Skipping {state} due to missing dataset: {e}")
