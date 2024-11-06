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

# Define features and target variables for Carbon Footprint
features_footprint = ['Mine Name']
target_footprint = 'Carbon Footprint_kg'

# Prepare the data for training
X_footprint, y_footprint = df[features_footprint], df[target_footprint]
X_train_footprint, X_test_footprint, y_train_footprint, y_test_footprint = train_test_split(X_footprint, y_footprint, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_footprint = RandomForestRegressor(random_state=42)
rf_footprint.fit(X_train_footprint, y_train_footprint)

# Evaluate the model
y_pred_footprint = rf_footprint.predict(X_test_footprint)
print("Carbon Footprint Model RMSE:", mean_squared_error(y_test_footprint, y_pred_footprint, squared=False))

# Save the trained model
with open('rf_footprint_model.pkl', 'wb') as f:
    pickle.dump(rf_footprint, f)

# Save the label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
