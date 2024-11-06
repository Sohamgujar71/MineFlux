import pandas as pd
from flask import Flask, render_template, jsonify, request
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load dataset at the start of the application
dataset = pd.read_csv('FOREST.CSV')

# Function to read CSV with specified encoding
def read_csv_with_encoding(file_path, encoding='utf-8'):
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        # Try a different encoding if the first attempt fails
        return pd.read_csv(file_path, encoding='latin1')

# Load the models and data
rf_co2 = pickle.load(open('rf_co2_model.pkl', 'rb'))
rf_ch4 = pickle.load(open('rf_ch4_model.pkl', 'rb'))
rf_carbon = pickle.load(open('rf_carbon_model.pkl', 'rb'))
rf_footprint = pickle.load(open('rf_footprint_model.pkl', 'rb'))

file_path = r"co2_final(2) - Copy.csv"
df = pd.read_csv(file_path)

label_encoders = {}
categorical_columns = ['Mine Name', 'Coal/Lignite', 'Type of Mine (OC/UG/Mixed)']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define ranges for emissions difference and corresponding pathways
pathways = {
    'High Emissions Difference': ["Implement large-scale afforestation", "Adopt advanced carbon capture technologies", "Shift to renewable energy sources"],
    'Moderate Emissions Difference': ["Increase efficiency of existing operations", "Enhance waste management practices", "Implement energy-saving technologies"],
    'Low Emissions Difference': ["Maintain current practices with minor improvements", "Promote sustainable land use", "Optimize resource utilization"]
}

# Serve the main website
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blockchain')
def blockchain():
    return render_template("blockchain.html")

@app.route('/table')
def table():
    return render_template("table.html")

@app.route('/emibox')
def emibox():
    return render_template("emibox.html")

@app.route('/carboncalculator2')
def carboncalculator2():
    return render_template("carboncalculator2.html")

@app.route('/pathways')
def pathways_view():
    return render_template("pathways.html")

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

# API endpoint to provide coal mines data for the map
@app.route('/coal_mines_data')
def coal_mines_data():
    coal_mine_df = read_csv_with_encoding('Indian Coal Mines Dataset_January 2021-1.csv')
    coal_mine_df.columns = coal_mine_df.columns.str.strip()
    data = coal_mine_df[['Mine Name', 'Latitude', 'Longitude', 'Coal/ Lignite Production (MT) (2019-2020)', 'Coal Mine Owner Name', 'Type of Mine (OC/UG/Mixed)']].to_dict(orient='records')
    return jsonify(data)

# API endpoint to search for a specific coal mine and provide suggestions
@app.route('/search_coal_mine')
def search_coal_mine():
    query = request.args.get('query', '').lower().strip()
    coal_mine_df = read_csv_with_encoding('Indian Coal Mines Dataset_January 2021-1.csv')
    coal_mine_df.columns = coal_mine_df.columns.str.strip()
    filtered_df = coal_mine_df[coal_mine_df['Mine Name'].str.lower().str.contains(query)]
    suggestions = filtered_df[['Mine Name', 'Latitude', 'Longitude', 'Coal/ Lignite Production (MT) (2019-2020)', 'Coal Mine Owner Name', 'Type of Mine (OC/UG/Mixed)']].to_dict(orient='records')
    return jsonify(suggestions)

# Prediction route for carbon emissions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        mine_name = data['mine_name']
        coal_type = data['coal_type']
        mine_type = data['mine_type']
        coal_production = float(data['coal_production'])

        try:
            mine_encoded = label_encoders['Mine Name'].transform([mine_name])[0]
        except ValueError:
            mine_encoded = np.median(df['Mine Name'])

        try:
            coal_encoded = label_encoders['Coal/Lignite'].transform([coal_type])[0]
        except ValueError:
            coal_encoded = np.median(df['Coal/Lignite'])

        try:
            mine_type_encoded = label_encoders['Type of Mine (OC/UG/Mixed)'].transform([mine_type])[0]
        except ValueError:
            mine_type_encoded = np.median(df['Type of Mine (OC/UG/Mixed)'])

        co2_input = [[mine_encoded, coal_encoded, mine_type_encoded, coal_production]]
        co2_prediction = rf_co2.predict(co2_input)[0]

        ch4_input = co2_input.copy()
        ch4_prediction = rf_ch4.predict(ch4_input)[0]

        carbon_input = [[mine_encoded, mine_type_encoded, coal_production]]
        carbon_prediction = rf_carbon.predict(carbon_input)[0]

        footprint_input = [[mine_encoded]]
        footprint_prediction = rf_footprint.predict(footprint_input)[0]

        result = {
            'CO2 Emissions (kg/tonne)': co2_prediction,
            'CH4 Emissions (kg/tonne)': ch4_prediction,
            'Carbon Emissions (kg/tonne)': carbon_prediction,
            'Carbon Footprint (kgCO2e)': footprint_prediction
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

# Route for calculating emissions and sequestration
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        user_project = request.form['project']
        user_mining_area = float(request.form['miningArea'])
        user_plantation_area = float(request.form['plantationArea'])
        user_emission_factor = float(request.form['emissionFactor'])
        user_sequestration_rate = float(request.form['sequestrationRate'])
    except ValueError:
        return jsonify({'result': 'Invalid input! Please enter valid numbers.'})

    if user_project in dataset['Project'].values:
        project_data = dataset[dataset['Project'] == user_project].iloc[0]
        dataset_mining_area = project_data['Mining Area (Sq Km)']
        dataset_plantation_area = project_data['Plantation Area (Sq Km)']
        dataset_emission_factor = project_data['Emission Factor (Tonnes CO2 per Sq Km)']
        dataset_sequestration_rate = project_data['Sequestration Rate (Tonnes CO2 per hectare per year)']
    else:
        return jsonify({'result': f"Project '{user_project}' not found in the dataset."})

    user_emissions = user_mining_area * user_emission_factor
    dataset_emissions = dataset_mining_area * dataset_emission_factor
    user_sequestration = user_plantation_area * 100 * user_sequestration_rate
    dataset_sequestration = dataset_plantation_area * 100 * dataset_sequestration_rate

    user_net_carbon_emissions = user_emissions - user_sequestration
    dataset_net_carbon_emissions = dataset_emissions - dataset_sequestration

    # Building HTML content with style
    result = """
    <table style='border: 1px solid black;'>
        <tr>
            <th>Parameter</th>
            <th>Value</th>
        </tr>
        <tr style='background-color: {};'>  <!-- Dynamic background color -->
            <td>Your Estimated Carbon Emissions:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
        <tr style='background-color: {};'>  <!-- Dynamic background color -->
            <td>Dataset Estimated Carbon Emissions for {}:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
        <tr style='background-color: {};'>  <!-- Dynamic background color -->
            <td>Your Estimated Carbon Sequestration:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
        <tr style='background-color: {};'>  <!-- Dynamic background color -->
            <td>Dataset Estimated Carbon Sequestration for {}:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
        <tr style='background-color: #ccccff;'>  <!-- Blue for net emissions -->
            <td>Your Net Carbon Emissions:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
        <tr style='background-color: #ccccff;'>  <!-- Blue for net emissions -->
            <td>Dataset Net Carbon Emissions:</td>
            <td>{:.1f} Tonnes of CO2/year</td>
        </tr>
    </table>
    """.format(
        '#ffcccc' if user_emissions > dataset_emissions else '#ccffcc',
        user_emissions,
        '#ffcccc' if user_emissions > dataset_emissions else '#ccffcc',
        user_project,
        dataset_emissions,
        '#ffcccc' if user_sequestration > dataset_sequestration else '#ccffcc',
        user_sequestration,
        '#ffcccc' if user_sequestration > dataset_sequestration else '#ccffcc',
        user_project,
        dataset_sequestration,
        user_net_carbon_emissions,
        dataset_net_carbon_emissions
    )

    # Additional sentence to indicate overall comparison
    overall_comparison = "neutral"
    if user_net_carbon_emissions > dataset_net_carbon_emissions:
        overall_comparison = "higher"
    elif user_net_carbon_emissions < dataset_net_carbon_emissions:
        overall_comparison = "lower"

    result += f"<p>Your net carbon emissions are <strong>{overall_comparison}</strong> compared to the dataset's net emissions.</p>"

    return jsonify({'result': result})

# Route for suggesting pathways based on emissions difference
@app.route('/suggest_pathways', methods=['POST'])
def suggest_pathways():
    try:
        user_emissions = float(request.form['user_emissions'])
        dataset_emissions = float(request.form['dataset_emissions'])
    except ValueError:
        return jsonify({'pathways': 'Invalid input! Please enter valid numbers.'})

    # Calculate the difference in emissions
    emission_difference = abs(user_emissions - dataset_emissions)

    # Suggest pathways based on the difference
    if emission_difference > 50:  # High difference
        suggested_pathways = pathways['High Emissions Difference']
    elif 20 < emission_difference <= 50:  # Moderate difference
        suggested_pathways = pathways['Moderate Emissions Difference']
    else:  # Low difference
        suggested_pathways = pathways['Low Emissions Difference']

    return jsonify({
  "pathways": [
    {
      "description": "Implement large-scale afforestation",
      "image": "https://cdni.iconscout.com/illustration/premium/thumb/people-plant-trees-for-earth-sustainability-8972361-7315494.png",
      "learnMoreLink": "https://eurogrant.ucoz.ru/resour/resour6.html"
    },
    {
      "description": "Adopt advanced carbon capture technologies",
      "image": "https://eurogrant.ucoz.ru/resour/image/ccs-cycle-animation.gif",
      "learnMoreLink": "https://eurogrant.ucoz.ru/resour/resour6.html"
    },
    {
      "description": "Shift to renewable energy sources",
      "image": "https://michaelsenergy.com/wp-content/uploads/2022/05/Energy-Rant-5.18.22-Blistering-Wind-and-Solar-Energy.png",
      "learnMoreLink": "https://eurogrant.ucoz.ru/resour/resour6.html"
    }
  ]
}
)

if __name__ == "__main__":
    app.run(debug=True)
