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

# Define features and target variables for Carbon emissions
features_carbon = ['Mine Name', 'Type of Mine (OC/UG/Mixed)', 'Coal/ Lignite Production (MT) (2019-2020)']
target_carbon = 'Carbon Emissions'

# Prepare the data for training
X_carbon, y_carbon = df[features_carbon], df[target_carbon]
X_train_carbon, X_test_carbon, y_train_carbon, y_test_carbon = train_test_split(X_carbon, y_carbon, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_carbon = RandomForestRegressor(random_state=42)
rf_carbon.fit(X_train_carbon, y_train_carbon)

# Evaluate the model
y_pred_carbon = rf_carbon.predict(X_test_carbon)
print("Carbon Emissions Model RMSE:", mean_squared_error(y_test_carbon, y_pred_carbon, squared=False))

# Save the trained model
with open('rf_carbon_model.pkl', 'wb') as f:
    pickle.dump(rf_carbon, f)

# Save the label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
