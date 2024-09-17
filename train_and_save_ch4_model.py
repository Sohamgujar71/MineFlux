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

# Define features and target variables for CH4 emissions
features_ch4 = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
target_ch4 = 'Methane_Emissions_kg'

# Prepare the data for training
X_ch4, y_ch4 = df[features_ch4], df[target_ch4]
X_train_ch4, X_test_ch4, y_train_ch4, y_test_ch4 = train_test_split(X_ch4, y_ch4, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_ch4 = RandomForestRegressor(random_state=42)
rf_ch4.fit(X_train_ch4, y_train_ch4)

# Evaluate the model
y_pred_ch4 = rf_ch4.predict(X_test_ch4)
print("CH4 Emissions Model RMSE:", mean_squared_error(y_test_ch4, y_pred_ch4, squared=False))

# Save the trained model
with open('rf_ch4_model.pkl', 'wb') as f:
    pickle.dump(rf_ch4, f)

# Save the label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
