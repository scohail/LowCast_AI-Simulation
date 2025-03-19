import streamlit as st
import plotly.express as px
import pandas as pd
import glob
import os
from joblib import load
from tensorflow.keras.models import load_model
from Modules.prediction import Prepare_data, Compute_error, Predict_temp
import logging
# Your existing functions here (Prepare_data, Compute_error, Predict_temp)
def main():
    st.set_page_config(layout="wide")
    st.title("2D Error Distribution Visualization")
    
    # Initialize session state
    if 'error_data' not in st.session_state:
        st.session_state.error_data = None
        st.session_state.current_temp = None
        st.session_state.real_data = None
        st.session_state.predicted_data = None

    # Sidebar controls
    with st.sidebar:



        if "page" not in st.session_state:
            st.session_state.page = "2D Error"

        Error_button = st.button("2D Error")
        prediction_button = st.button("Prediction")

        if Error_button:
            st.session_state.page = "2D Error"
        if prediction_button:
            st.session_state.page = "Predicted Simulation"



        st.header("Controls")


        if "temp_int" not in st.session_state:
            st.session_state.temp_int = 614
        if "state_number" not in st.session_state:
            st.session_state.state_number = 1
        
        # Temperature slider
        temp_int = st.slider(
            "Select Temperature (K)",
            min_value=614,
            max_value=720,
            value=614,
            step=1
        )
        st.session_state.temp_int = temp_int
        # State number slider
        state_number = st.slider(
            "Select State Number",
            min_value=1,
            max_value=117,
            value=1,
            step=1
        )
        # Process button
    
        st.session_state.state_number = state_number

        
        process_clicked = st.button("Process Error")


        if process_clicked:
            # Convert to Celsius for processing
            temp_int_celsius = temp_int
            
            # Only reprocess if temperature changed
            if st.session_state.current_temp != temp_int:
                with st.spinner("Processing data for new temperature..."):
                    try:
                        st.session_state.real_data, st.session_state.predicted_data = Prepare_data(temp_int_celsius)
                        st.session_state.error_data = Compute_error(st.session_state.real_data, st.session_state.predicted_data)
                        st.session_state.current_temp = temp_int
                        print("Data processed successfully for plotting")
                    except Exception as e:
                        st.error(f"Processing failed: {str(e)}")
                        st.session_state.error_data = None 

        
    

    if st.session_state.page == "2D Error":
        display_2D_Error_page()
    elif st.session_state.page == "Predicted Simulation":
        display_prediction_page()



def display_2D_Error_page():

    st.header("2D Error Distribution")
    if st.session_state.error_data is not None:
        st.header(f"Error Distribution - {st.session_state.temp_int}°C, State {st.session_state.state_number}")
        
        error_column = f"TempState{st.session_state.state_number}"
        
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
            fig_1 = px.scatter(
                st.session_state.real_data,
                x="X",
                y="Y",
                color=error_column,
                color_continuous_scale="RdYlGn_r",
                labels={'color': 'Temp (K)'},
                title=f"Simulation Data",
                width=420,
                height=800
            )
            fig_2 = px.scatter(
                st.session_state.predicted_data,
                x="X",
                y="Y",
                color=error_column,
                color_continuous_scale="RdYlGn_r",
                labels={'color': 'Temp (K)'},
                title=f"Predicted Data",
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
            fig_1.update_layout(    
                coloraxis_colorbar=dict(
                    title="Temp (K)",
                    thickness=20,
                    len=0.75
                ),
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                margin=dict(l=50, r=0, b=0, t=40)
            )
            fig_2.update_layout(
                coloraxis_colorbar=dict(
                    title="Temp (K)",
                    thickness=20,
                    len=0.75
                ),
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                margin=dict(l=50, r=0, b=0, t=40)
            )
            
            

            col1, col2, col3 = st.columns(3)

            with col1:
                st.plotly_chart(fig_1, use_container_width=False, key="plot1")

            with col2:
                st.plotly_chart(fig_2, use_container_width=False, key="plot2")
            
            with col3:
                st.plotly_chart(fig, use_container_width=False, key="plot3")
            
        
        except KeyError:
            st.error(f"State {st.session_state.state_number} not available in processed data")
    
    else :
        st.warning("No error data available for selected parameters")
def display_prediction_page():
    st.header("Predicted Simulation")

    if st.session_state.predicted_data is not None:
        try:
            # Convert temperature columns to Celsius
            predicted_data_celsius = st.session_state.predicted_data.copy()
            temp_columns = [col for col in predicted_data_celsius.columns if col.startswith("TempState")]
            for col in temp_columns:
                predicted_data_celsius[col] = predicted_data_celsius[col] - 273

            # Plot predicted data for the selected state
            selected_temp_column = f"TempState{st.session_state.state_number}"
            fig_predicted = px.scatter(
                predicted_data_celsius,
                x="X",
                y="Y",
                color=selected_temp_column,
                color_continuous_scale="RdYlGn_r",
                labels={'color': 'Temp (°C)'},
                title=f"Predicted Data (State {st.session_state.state_number})",
                width=420,
                height=800
            )
            fig_predicted.update_layout(
                coloraxis_colorbar=dict(
                    title="Temp (°C)",
                    thickness=20,
                    len=0.75
                ),
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                margin=dict(l=50, r=0, b=0, t=40)
            )

            # Define the temperature-to-fraction relationship
            temp_to_fraction = {
                548: 1, 551: 0.99, 560: 0.95, 566: 0.88, 569: 0.77, 570: 0.49,
                577: 0.44, 582: 0.41, 589: 0.36, 593: 0.32, 601: 0.25, 610: 0.14,
                612: 0.09, 613: 0
            }

            # Interpolate solid fraction for temperatures
            def interpolate_fraction(temp):
                if temp <= 548:
                    return 1
                elif temp >= 613:
                    return 0
                else:
                    # Perform linear interpolation
                    sorted_temps = sorted(temp_to_fraction.keys())
                    for i in range(len(sorted_temps) - 1):
                        t1, t2 = sorted_temps[i], sorted_temps[i + 1]
                        if t1 <= temp <= t2:
                            f1, f2 = temp_to_fraction[t1], temp_to_fraction[t2]
                            return f1 + (f2 - f1) * (temp - t1) / (t2 - t1)

            predicted_data_celsius['Solid Fraction'] = predicted_data_celsius[selected_temp_column].apply(interpolate_fraction)

            # Plot solid fraction
            fig_solid_fraction = px.scatter(
                predicted_data_celsius,
                x="X",
                y="Y",
                color="Solid Fraction",
                color_continuous_scale="Blues",
                labels={'color': 'Solid Fraction'},
                title=f"Solid Fraction Distribution (State {st.session_state.state_number})",
                width=420,
                height=800
            )
            fig_solid_fraction.update_layout(
                coloraxis_colorbar=dict(
                    title="Solid Fraction",
                    thickness=20,
                    len=0.75
                ),
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                margin=dict(l=50, r=0, b=0, t=40)
            )

            # Display the plots side by side
            empty_col1, col1, col2, empty_col2 = st.columns([1, 3, 3, 1])

            with col1:
                st.plotly_chart(fig_predicted, use_container_width=False, key="predicted_plot")

            with col2:
                st.plotly_chart(fig_solid_fraction, use_container_width=False, key="solid_fraction_plot")

        except Exception as e:
            st.error(f"Failed to display predicted simulation: {str(e)}")
    else:
        st.warning("No predicted data available for visualization")
    

if __name__ == "__main__":
    main()