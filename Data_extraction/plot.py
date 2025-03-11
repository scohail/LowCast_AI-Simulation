import dash
import dash_cytoscape as cyto
import h5py
import dash_html_components as html

def add_nodes_edges(hdf5_obj, nodes, edges, parent=None, depth=0, max_depth=6):
    """Recursively adds nodes and edges to the list, with labels based on content."""
    if depth >= max_depth:
        return

    for key in hdf5_obj:
        node_name = f"{parent}/{key}" if parent else key
        
        # Define the label for the node, based on content. 
        label = key
        if isinstance(hdf5_obj[key], h5py.Group):
            label += " (Group)"
        elif isinstance(hdf5_obj[key], h5py.Dataset):
            label += f" (Dataset, Shape: {hdf5_obj[key].shape})"
        
        nodes.append({"data": {"id": node_name, "label": label}})

        if parent:
            edges.append({"data": {"source": parent, "target": node_name}})

        if isinstance(hdf5_obj[key], h5py.Group):  
            add_nodes_edges(hdf5_obj[key], nodes, edges, node_name, depth + 1, max_depth)

# Load HDF5 file
file_path = "/home/scohail/Desktop/Script ProCAST to Excel/th-CorpsBrocheMoule1BPv4-sym.erfh5"  # Update with your file path
nodes = []
edges = []

with h5py.File(file_path, "r") as f:
    add_nodes_edges(f, nodes, edges)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=nodes + edges,
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '3000px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',  # Set label to the node's label
                    'font-size': '2px',  # Adjust font size here
                    'font-family': 'Arial',  # Optional: change the font family
                    'color': 'black',  # Optional: change the label color
                    'text-valign': 'center',  # Vertically center the label
                    'text-halign': 'center',  # Horizontally center the label
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 2,  # Set edge width
                    'line-color': '#ccc'  # Optional: change edge color
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
