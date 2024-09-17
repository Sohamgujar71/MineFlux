'''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Load the data
file_path = r"D:\\sih\\emissions\\co2_final(2) - Copy.csv"
df = pd.read_csv(file_path)

# Encode categorical variables
label_encoders = {}
categorical_columns = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target variables for each emission type
features_co2 = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
features_ch4 = features_co2.copy()
features_carbon = ['Mine Name', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
features_footprint = ['Mine Name']

target_co2 = 'Total_CO2_Emissions_kg'
target_ch4 = 'Methane_Emissions_kg'
target_carbon = 'Carbon Emissions'
target_footprint = 'Carbon Footprint_kg'

# Train-test split for each model
X_co2, y_co2 = df[features_co2], df[target_co2]
X_ch4, y_ch4 = df[features_ch4], df[target_ch4]
X_carbon, y_carbon = df[features_carbon], df[target_carbon]
X_footprint, y_footprint = df[features_footprint], df[target_footprint]

X_train_co2, X_test_co2, y_train_co2, y_test_co2 = train_test_split(X_co2, y_co2, test_size=0.2, random_state=42)
X_train_ch4, X_test_ch4, y_train_ch4, y_test_ch4 = train_test_split(X_ch4, y_ch4, test_size=0.2, random_state=42)
X_train_carbon, X_test_carbon, y_train_carbon, y_test_carbon = train_test_split(X_carbon, y_carbon, test_size=0.2, random_state=42)
X_train_footprint, X_test_footprint, y_train_footprint, y_test_footprint = train_test_split(X_footprint, y_footprint, test_size=0.2, random_state=42)

# Initialize Random Forest models
rf_co2 = RandomForestRegressor(random_state=42)
rf_ch4 = RandomForestRegressor(random_state=42)
rf_carbon = RandomForestRegressor(random_state=42)
rf_footprint = RandomForestRegressor(random_state=42)

# Train the models
rf_co2.fit(X_train_co2, y_train_co2)
rf_ch4.fit(X_train_ch4, y_train_ch4)
rf_carbon.fit(X_train_carbon, y_train_carbon)
rf_footprint.fit(X_train_footprint, y_train_footprint)

# Make predictions
y_pred_co2 = rf_co2.predict(X_test_co2)
y_pred_ch4 = rf_ch4.predict(X_test_ch4)
y_pred_carbon = rf_carbon.predict(X_test_carbon)
y_pred_footprint = rf_footprint.predict(X_test_footprint)

# Evaluate the models
print("CO2 Emissions Model RMSE:", mean_squared_error(y_test_co2, y_pred_co2, squared=False))
print("CH4 Emissions Model RMSE:", mean_squared_error(y_test_ch4, y_pred_ch4, squared=False))
print("Carbon Emissions Model RMSE:", mean_squared_error(y_test_carbon, y_pred_carbon, squared=False))
print("Carbon Footprint Model RMSE:", mean_squared_error(y_test_footprint, y_pred_footprint, squared=False))

# User input function for predictions
def predict_emissions(mine_name, coal_type, mine_type, coal_production):
    mine_encoded = label_encoders['Mine Name'].transform([mine_name])[0]
    coal_encoded = label_encoders['Coal/Lignite'].transform([coal_type])[0]
    mine_type_encoded = label_encoders['Type of Mine (OC/UG/Mixed)'].transform([mine_type])[0]

    # CO2 Emissions Prediction
    co2_input = [[mine_encoded, coal_encoded, mine_type_encoded, coal_production]]
    co2_prediction = rf_co2.predict(co2_input)[0]
    
    # CH4 Emissions Prediction
    ch4_input = co2_input.copy()
    ch4_prediction = rf_ch4.predict(ch4_input)[0]
    
    # Carbon Emissions Prediction
    carbon_input = [[mine_encoded, mine_type_encoded, coal_production]]
    carbon_prediction = rf_carbon.predict(carbon_input)[0]
    
    # Carbon Footprint Prediction
    footprint_input = [[mine_encoded]]
    footprint_prediction = rf_footprint.predict(footprint_input)[0]
    
    return {
        "CO2 Emissions (kg/tonne)": co2_prediction,
        "CH4 Emissions (kg/tonne)": ch4_prediction,
        "Carbon Emissions (kg/tonne)": carbon_prediction,
        "Carbon Footprint (kgCO2e)": footprint_prediction
    }

# Example usage
print(df['Mine Name'].unique()) 
example_prediction = predict_emissions("Ningah Colliery", "Bituminous", "OC", 1000)
print(example_prediction)'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

# Load the data
file_path = r"D:\\sih\\emissions\\co2_final(2) - Copy.csv"
df = pd.read_csv(file_path)

# Encode categorical variables
label_encoders = {}
categorical_columns = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target variables for each emission type
features_co2 = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
features_ch4 = features_co2.copy()
features_carbon = ['Mine Name', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
features_footprint = ['Mine Name']

target_co2 = 'Total_CO2_Emissions_kg'
target_ch4 = 'Methane_Emissions_kg'
target_carbon = 'Carbon Emissions'
target_footprint = 'Carbon Footprint_kg'

# Train-test split for each model
X_co2, y_co2 = df[features_co2], df[target_co2]
X_ch4, y_ch4 = df[features_ch4], df[target_ch4]
X_carbon, y_carbon = df[features_carbon], df[target_carbon]
X_footprint, y_footprint = df[features_footprint], df[target_footprint]

X_train_co2, X_test_co2, y_train_co2, y_test_co2 = train_test_split(X_co2, y_co2, test_size=0.2, random_state=42)
X_train_ch4, X_test_ch4, y_train_ch4, y_test_ch4 = train_test_split(X_ch4, y_ch4, test_size=0.2, random_state=42)
X_train_carbon, X_test_carbon, y_train_carbon, y_test_carbon = train_test_split(X_carbon, y_carbon, test_size=0.2, random_state=42)
X_train_footprint, X_test_footprint, y_train_footprint, y_test_footprint = train_test_split(X_footprint, y_footprint, test_size=0.2, random_state=42)
#X_train_footprint, X_test_footprint, y_train_footprint, y_test_footprint = train_test_split(X_footprint, y_footprint, test_size=0.2, random_state=42)


# Initialize Random Forest models
rf_co2 = RandomForestRegressor(random_state=42)
rf_ch4 = RandomForestRegressor(random_state=42)
rf_carbon = RandomForestRegressor(random_state=42)
rf_footprint = RandomForestRegressor(random_state=42)

# Train the models
rf_co2.fit(X_train_co2, y_train_co2)
rf_ch4.fit(X_train_ch4, y_train_ch4)
rf_carbon.fit(X_train_carbon, y_train_carbon)
rf_footprint.fit(X_train_footprint, y_train_footprint)

# Make predictions
y_pred_co2 = rf_co2.predict(X_test_co2)
y_pred_ch4 = rf_ch4.predict(X_test_ch4)
y_pred_carbon = rf_carbon.predict(X_test_carbon)
y_pred_footprint = rf_footprint.predict(X_test_footprint)

# Evaluate the models
print("CO2 Emissions Model RMSE:", mean_squared_error(y_test_co2, y_pred_co2, squared=False))
print("CH4 Emissions Model RMSE:", mean_squared_error(y_test_ch4, y_pred_ch4, squared=False))
print("Carbon Emissions Model RMSE:", mean_squared_error(y_test_carbon, y_pred_carbon, squared=False))
print("Carbon Footprint Model RMSE:", mean_squared_error(y_test_footprint, y_pred_footprint, squared=False))

with open('rf_co2_model.pkl', 'wb') as f:
    pickle.dump(rf_co2, f)

with open('rf_ch4_model.pkl', 'wb') as f:
    pickle.dump(rf_ch4, f)

with open('rf_carbon_model.pkl', 'wb') as f:
    pickle.dump(rf_carbon, f)

with open('rf_footprint_model.pkl', 'wb') as f:
    pickle.dump(rf_footprint, f)

# Optional: Save label encoders if they are needed for future predictions
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)


# User input function for predictions
def predict_emissions(mine_name, coal_type, mine_type, coal_production):
    try:
        mine_encoded = label_encoders['Mine Name'].transform([mine_name])[0]
    except ValueError:
        # If mine name not found in training data, provide a fallback
        mine_encoded = np.median(df['Mine Name'])  # Fallback: use the median value of known mines
        
    try:
        coal_encoded = label_encoders['Coal/Lignite'].transform([coal_type])[0]
    except ValueError:
        coal_encoded = np.median(df['Coal/Lignite'])  # Fallback: use the median value of known coal types
    
    try:
        mine_type_encoded = label_encoders['Type of Mine (OC/UG/Mixed)'].transform([mine_type])[0]
    except ValueError:
        mine_type_encoded = np.median(df['Type of Mine (OC/UG/Mixed)'])  # Fallback: use the median value of known mine types

    # CO2 Emissions Prediction
    co2_input = [[mine_encoded, coal_encoded, mine_type_encoded, coal_production]]
    co2_prediction = rf_co2.predict(co2_input)[0]
    
    # CH4 Emissions Prediction
    ch4_input = co2_input.copy()
    ch4_prediction = rf_ch4.predict(ch4_input)[0]
    
    # Carbon Emissions Prediction
    carbon_input = [[mine_encoded, mine_type_encoded, coal_production]]
    carbon_prediction = rf_carbon.predict(carbon_input)[0]
    
    # Carbon Footprint Prediction
    footprint_input = [[mine_encoded]]
    footprint_prediction = rf_footprint.predict(footprint_input)[0]
    
    return {
        "CO2 Emissions (kg/tonne)": co2_prediction,
        "CH4 Emissions (kg/tonne)": ch4_prediction,
        "Carbon Emissions (kg/tonne)": carbon_prediction,
        "Carbon Footprint (kgCO2e)": footprint_prediction
    }

# Example usage
print(df['Mine Name'].unique()) 
example_prediction = predict_emissions("Ningah Colliery", "Bituminous", "OC", 1000)
print(example_prediction)
