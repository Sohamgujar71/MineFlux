import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
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

# Define features and target variables for CO2 emissions
features_co2 = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
target_co2 = 'Total_CO2_Emissions_kg'

# Prepare the data for training
X_co2, y_co2 = df[features_co2], df[target_co2]
X_train_co2, X_test_co2, y_train_co2, y_test_co2 = train_test_split(X_co2, y_co2, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_co2 = RandomForestRegressor(random_state=42)
rf_co2.fit(X_train_co2, y_train_co2)

# Evaluate the model
y_pred_co2 = rf_co2.predict(X_test_co2)
print("CO2 Emissions Model RMSE:", mean_squared_error(y_test_co2, y_pred_co2, squared=False))

# Save the trained model
with open('rf_co2_model.pkl', 'wb') as f:
    pickle.dump(rf_co2, f)

# Save the label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
