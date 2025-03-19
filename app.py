import streamlit as st
import plotly.express as px
import pandas as pd
import glob
import os
from joblib import load
from tensorflow.keras.models import load_model
from Modules.prediction import Prepare_data, Compute_error, Predict_temp

# Your existing functions here (Prepare_data, Compute_error, Predict_temp)
def main():
    st.set_page_config(layout="wide")
    st.title("2D Error Distribution Visualization")
    
    # Initialize session state
    if 'error_data' not in st.session_state:
        st.session_state.error_data = None
        st.session_state.current_temp = None

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        
        # Temperature slider
        temp_int = st.slider(
            "Select Temperature (°C)",
            min_value=614,
            max_value=720,
            value=614,
            step=1
        )
        
        # State number slider
        state_number = st.slider(
            "Select State Number",
            min_value=1,
            max_value=117,
            value=1,
            step=1
        )
        
        # Process button
        process_clicked = st.button("Process Error")
    
    # Processing logic
    if process_clicked:
        # Convert to Celsius for processing
        temp_int_celsius = temp_int
        
        # Only reprocess if temperature changed
        if st.session_state.current_temp != temp_int:
            with st.spinner("Processing data for new temperature..."):
                try:
                    real_data, predicted_data = Prepare_data(temp_int_celsius)
                    st.session_state.error_data = Compute_error(real_data, predicted_data)
                    st.session_state.current_temp = temp_int
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
                    st.session_state.error_data = None

    # Visualization
    if st.session_state.error_data is not None:
        st.header(f"Error Distribution - {temp_int}°C, State {state_number}")
        
        error_column = f"TempState{state_number}"
        
        try:
            fig = px.scatter(
                st.session_state.error_data,
                x="X",
                y="Y",
                color=error_column,
                color_continuous_scale="RdYlGn_r",
                labels={'color': 'Error (°C)'},
                title=f"Temperature Error Distribution",
                width=420,
                height=800
            )
            
            # Configure plot appearance
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title="Error (°C)",
                    thickness=20,
                    len=0.75
                ),
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                margin=dict(l=50, r=0, b=0, t=40)
            )


            fig_1 = fig
            fig_2 = fig

            col1, col2, col3 = st.columns(3)

            with col1:
                st.plotly_chart(fig_1, use_container_width=False, key="plot1")

            with col2:
                st.plotly_chart(fig_2, use_container_width=False, key="plot2")
            
            with col3:
                st.plotly_chart(fig, use_container_width=False, key="plot3")
            
          
        except KeyError:
            st.error(f"State {state_number} not available in processed data")
    elif process_clicked:
        st.warning("No error data available for selected parameters")

if __name__ == "__main__":
    main()