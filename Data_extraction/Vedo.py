import os
import numpy as np
import pandas as pd
from vedo import Points, Plotter

# Folder containing CSV files
folder = "/home/scohail/Desktop/LowCast_AI-Simulation/Data_614C"

# Get list of state files
state_files = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")])

# Load the first state file to get the coordinates
first_state = pd.read_csv(state_files[0])
coordinates = first_state[['X', 'Y', 'Z']].values

# Create a Points object for visualization
points = Points(coordinates)
points.pointdata["Temperature"] = np.zeros(len(coordinates))  # Placeholder for temperature values

# Initialize the plotter
plt = Plotter(bg='white')

# Add the points to the plotter
plt.add(points)

# Function to update the points for each state
def update_state(state_file):
    data = pd.read_csv(state_file)
    temperatures = data['Temperature(K)'].values

    # Update the points with new temperature values
    points.pointdata["Temperature"] = temperatures
    points.cmap("coolwarm", "Temperature")  # Apply a colormap
    plt.render()  # Force an update to refresh the scene

# Add a callback to loop through states
current_state = 0
def loop_func(event):
    global current_state
    if current_state >= len(state_files):
        plt.timer_callback("stop")  # Stop the timer when all states are processed
        return

    update_state(state_files[current_state])
    current_state += 1

# Force the first update before the timer starts
update_state(state_files[0])
plt.render()  # Ensures visualization starts immediately

# Add the callback and start the timer
plt.add_callback("timer", loop_func)
plt.timer_callback("start", dt=4500)  # dt is the delay between frames in milliseconds

# Show the plot
plt.show("Temperature Evolution", zoom=1.25, elevation=-30, interactive=True)
