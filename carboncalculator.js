document.getElementById('emission-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get form values
    const mine_name = document.getElementById('mine_name').value;
    const coal_type = document.getElementById('coal_type').value;
    const mine_type = document.getElementById('mine_type').value;
    const coal_production = document.getElementById('coal_production').value;

    // Prepare data for API call
    const data = {
        mine_name: mine_name,
        coal_type: coal_type,
        mine_type: mine_type,
        coal_production: parseFloat(coal_production)
    };

    // Make API request to the backend
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Create a table for results
        const resultTable = `
            <table class="result-table">
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>CO<sub>2</sub> Emissions</td>
                    <td>${result['CO2 Emissions (kg/tonne)']} kg/tonne</td>
                </tr>
                <tr>
                    <td>CH<sub>4</sub> Emissions</td>
                    <td>${result['CH4 Emissions (kg/tonne)']} kg/tonne</td>
                </tr>
                <tr>
                    <td>Carbon Emissions</td>
                    <td>${result['Carbon Emissions (kg/tonne)']} kg/tonne</td>
                </tr>
                <tr>
                    <td>Carbon Footprint</td>
                    <td>${result['Carbon Footprint (kgCO2e)']} kgCO2e</td>
                </tr>
            </table>
        `;
        
        document.getElementById('results').innerHTML = resultTable;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
