document.addEventListener("DOMContentLoaded", function () {
    const mineSearchInput = document.getElementById("mine-search");
    const suggestionsList = document.getElementById("suggestions");

    // Hardcoded mine data
    const minesData = {
        "Ningah Colliery": {
            "carbon_emissions": 32,
            "status": "Moderate",
            "last_update": "2024-08-22 10:00:00"
        },
        "Singrauli Coal Mine": {
            "carbon_emissions": 15,
            "status": "Low",
            "last_update": "2024-08-22 10:00:00"
        },
        "Jharia Coalfield": {
            "carbon_emissions": 75,
            "status": "High",
            "last_update": "2024-08-22 10:00:00"
        }
    };

    // Show suggestions based on input
    mineSearchInput.addEventListener("input", function () {
        const query = mineSearchInput.value.toLowerCase();
        suggestionsList.innerHTML = "";  // Clear previous suggestions

        Object.keys(minesData).forEach(mine => {
            if (mine.toLowerCase().includes(query) && query.length > 0) {
                const suggestionItem = document.createElement("li");
                suggestionItem.textContent = mine;
                suggestionItem.addEventListener("click", function () {
                    mineSearchInput.value = mine;
                    suggestionsList.innerHTML = "";  // Clear suggestions
                    displayMineData(mine);  // Display the mine data when an item is clicked
                });
                suggestionsList.appendChild(suggestionItem);
            }
        });
    });

    // Function to display mine data
    function displayMineData(mineName) {
        const data = minesData[mineName];
        if (data) {
            // Update mine-name and emissions data
            document.getElementById('mine-name').innerText = mineName;
            document.getElementById('carbon-emissions').innerText = data.carbon_emissions;
            document.getElementById('last-update').innerText = `Last Update: ${data.last_update}`;
            document.getElementById('status-text').innerText = data.status;

            // Set the color based on status
            let statusColor;
            if (data.status === 'Good') {
                statusColor = '#4CAF50'; // Green
            } else if (data.status === 'Moderate') {
                statusColor = '#FFA500'; // Orange
            } else if (data.status === 'High') {
                statusColor = '#FF0000'; // Red
            }
            document.getElementById('status-text').style.backgroundColor = statusColor;
            document.getElementById('carbon-emissions').style.color = statusColor;

            // Adjust the width of the progress bar based on emissions
            const progressFill = document.getElementById('progress-fill');
            const fillWidth = data.carbon_emissions * 3.5;  // Adjust for a 350px width progress bar
            progressFill.style.width = `${fillWidth}px`;
        } else {
            alert('Mine not found.');
        }
    }

    // Attach the displayMineData function to the search button
    document.getElementById('search-button').addEventListener('click', function () {
        const mineName = mineSearchInput.value;
        displayMineData(mineName);
    });
});
