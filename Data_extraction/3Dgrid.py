import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("/home/scohail/Desktop/Script ProCAST to Excel/teste/state000000000001.csv")
df['Temperature(K)'] = pd.to_numeric(df['Temperature(K)'], errors='coerce')

# Plotly 3D Scatter
fig = px.scatter_3d(df, x='X', y='Y', z='Z', color='Temperature(K)', opacity=0.7)

# Save as HTML and open in a browser
fig.write_html("3d_plot.html")
print("Plot saved as '3d_plot.html'. Open it in a browser.")
