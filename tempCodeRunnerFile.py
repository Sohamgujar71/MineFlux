from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset at the start of the application
dataset = pd.read_csv('FOREST.CSV')

# Define ranges for emissions difference and corresponding pathways
pathways = {
    'High Emissions Difference': ["Implement large-scale afforestation", "Adopt advanced carbon capture technologies", "Shift to renewable energy sources"],
    'Moderate Emissions Difference': ["Increase efficiency of existing operations", "Enhance waste management practices", "Implement energy-saving technologies"],
    'Low Emissions Difference': ["Maintain current practices with minor improvements", "Promote sustainable land use", "Optimize resource utilization"]
}

@app.route('/')
def index():
    return render_template('index.html')

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

    # Extract Project Data from the dataset
    if user_project in dataset['Project'].values:
        project_data = dataset[dataset['Project'] == user_project].iloc[0]
        dataset_mining_area = project_data['Mining Area (Sq Km)']
        dataset_plantation_area = project_data['Plantation Area (Sq Km)']
        dataset_emission_factor = project_data['Emission Factor (Tonnes CO2 per Sq Km)']
        dataset_sequestration_rate = project_data['Sequestration Rate (Tonnes CO2 per hectare per year)']
    else:
        return jsonify({'result': f"Project '{user_project}' not found in the dataset."})

    # Carbon Emission Estimation
    user_emissions = user_mining_area * user_emission_factor
    dataset_emissions = dataset_mining_area * dataset_emission_factor

    # Carbon Sequestration Estimation
    user_sequestration = user_plantation_area * 100 * user_sequestration_rate
    dataset_sequestration = dataset_plantation_area * 100 * dataset_sequestration_rate

    # Comparison Results
    result = f"""
    Your Estimated Carbon Emissions: {user_emissions} Tonnes of CO2/year<br>
    Dataset Estimated Carbon Emissions for {user_project}: {dataset_emissions} Tonnes of CO2/year<br><br>
    Your Estimated Carbon Sequestration: {user_sequestration} Tonnes of CO2/year<br>
    Dataset Estimated Carbon Sequestration for {user_project}: {dataset_sequestration} Tonnes of CO2/year<br><br>
    """

    if user_emissions > dataset_emissions:
        result += "Your carbon emissions are higher than the dataset's estimated emissions.<br>"
    else:
        result += "Your carbon emissions are lower than the dataset's estimated emissions.<br>"

    if user_sequestration > dataset_sequestration:
        result += "Your carbon sequestration rate is higher than the dataset's estimated sequestration.<br>"
    else:
        result += "Your carbon sequestration rate is lower than the dataset's estimated sequestration.<br>"

    # Final Result
    user_net_carbon_emissions = user_emissions - user_sequestration
    dataset_net_carbon_emissions = dataset_emissions - dataset_sequestration

    result += f"Your Net Carbon Emissions: {user_net_carbon_emissions} Tonnes of CO2/year<br>"
    result += f"Dataset Net Carbon Emissions: {dataset_net_carbon_emissions} Tonnes of CO2/year<br>"

    return jsonify({'result': result})

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

    return jsonify({'pathways': suggested_pathways})

if __name__ == '__main__':
    app.run(debug=True)
