import pandas as pd
import glob
import os
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from joblib import load
import numpy as np  



def Prepare_data(Temp_int):
    '''
    This function is used to prepare the data for visualization
    Real_data: The real data that we have and it's temperature in celcius (int)
    Predicted_data: The 

    '''
    # Real Data Preparation

    print('Preparing the data for visualization')

    Real_Data_path = "/home/scohail/Desktop/LowCast_AI-Simulation/Data/Data_"+str(Temp_int) +'C'

    temp_int_value = Temp_int + 273
    
    print(f"Processing {Real_Data_path } with temp_int_value = {temp_int_value}")
    
    csv_files = sorted(glob.glob(os.path.join(Real_Data_path, "state*.csv")))
    
    # Initialize an empty DataFrame
    final_df = None
    
    # Process files with sequential state numbers
    for i, file in enumerate(csv_files, 1):
        # Use sequential numbering instead of original filename
        state_number = str(i)
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Filter rows where Z == -4.2632566e-15
        df_filtered = df[df["Z"] == -4.2632566e-15][["X", "Y", "Temperature(K)"]]
        
        # Rename temperature column to reflect the sequential state number
        df_filtered.rename(columns={"Temperature(K)": f"TempState{state_number}"}, inplace=True)
        
        # Add the Temp_int column
        df_filtered["Temp_int"] = temp_int_value
        
        # Merge with the final DataFrame
        if final_df is None:
            final_df = df_filtered
        else:
            final_df = pd.merge(final_df, df_filtered, on=["X", "Y", "Temp_int"], how="outer")
            
        if i % 10 == 0:  # Print progress every 10 files
            print(f"Processed {i}/{len(csv_files)} files")

    print("Real data has been prepared successfully")

    
    Real_Data = final_df
    
    print(Real_Data.head())
    # Predicted Data Preparation

    Predicted_Data = Predict_temp(Real_Data)

    print('Real and Predicted data has been prepared successfully')   

    return Real_Data, Predicted_Data
    

def Compute_error(Real_data,Predicted_data):
    '''
    This function is used to visualize the error between the real data and the predicted data for 2D approach
    '''
    print('Computing the error between the real and the predicted data')

    Error = Real_data.copy()

    Error = np.abs(Real_data.drop(['X', 'Y' , 'Temp_int'], axis=1) - Predicted_data.drop(['X', 'Y' , 'Temp_int'], axis=1))

    Error = pd.concat([Real_data[['X', 'Y', 'Temp_int']].reset_index(drop=True), Error.reset_index(drop=True)], axis=1)

    print('Error has been computed successfully')

    print(Error.head())
    
    return Error

def Predict_temp(Topredict_Data):
    '''
    This function is used to predict the temperature for a specific temperature
    '''
    print('loading the model and the scaler')

    scaler = load('/home/scohail/Desktop/LowCast_AI-Simulation/Scaler/scaler_2_1.pkl')
    model = load_model('/home/scohail/Desktop/LowCast_AI-Simulation/Models/Last_model2_5.h5')

    Transformed_Data = Topredict_Data.copy()

    Transformed_Data.iloc[:,:] = scaler.transform(Topredict_Data.iloc[:, :])

    print('Transformed data')
    print(Transformed_Data.head())

    X= Transformed_Data[['X', 'Y', 'Temp_int']]
    y = Transformed_Data.drop(['X', 'Y' , 'Temp_int'], axis=1)

    y_pred = model.predict(X)

    y_pred = pd.DataFrame(y_pred, columns = y.columns)

    print('Data has been predicted successfully')


    #Retrensform the data to the original scale
    Transform_predected_data = pd.concat([X.reset_index(drop=True), y_pred.reset_index(drop=True)], axis=1)
    Original_scale_predected_data = pd.DataFrame(scaler.inverse_transform(Transform_predected_data), columns=Transformed_Data.columns)
    print('Data has been retransformed successfully')
    print(Original_scale_predected_data.head())
    
    return Original_scale_predected_data

