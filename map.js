var map = L.map('map').setView([22.5937, 78.9629], 5); // Default view centered on India
var markers = [];
var mineMarker;

// Initialize map with OpenStreetMap tiles
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


// Function to add markers to the map
function addMarkers(coalMines) {
    coalMines.forEach(mine => {
        var marker = L.marker([mine['Latitude'], mine['Longitude']], { icon: L.icon({ iconUrl: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png' }) })
            .bindTooltip(`<strong>${mine['Mine Name']}</strong><br>
                          Production: ${mine['Coal/ Lignite Production (MT) (2019-2020)']} MT<br>
                          Owner: ${mine['Coal Mine Owner Name']}<br>
                          Type of Mine: ${mine['Type of Mine (OC/UG/Mixed)']}`, { permanent: false, direction: 'top' })
            .addTo(map);

        markers.push({ marker: marker, name: mine['Mine Name'], data: mine });
    });
}

// Load all coal mine data and add markers
fetch('/coal_mines_data')
    .then(response => response.json())
    .then(data => {
        console.log('Coal mines data:', data); // Debugging line
        addMarkers(data);
    })
    .catch(error => console.log('Error loading coal mine data:', error));

// Handle search and change marker color
document.getElementById('searchButton').addEventListener('click', function () {
    var query = document.getElementById('coalMineInput').value;
    fetchSearchResults(query);
});

// Function to fetch search results
function fetchSearchResults(query) {
    fetch(`/search_coal_mine?query=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log('Search results:', data); // Debugging line
            if (data.length > 0) {
                updateMapWithSearchResult(data[0]);
            } else {
                alert('No results found');
            }
        })
        .catch(error => console.log('Error fetching search results:', error));
}

// Function to update map with search results
function updateMapWithSearchResult(selectedMine) {
    const lat = selectedMine['Latitude'];
    const lng = selectedMine['Longitude'];
    const mineName = selectedMine['Mine Name'];

    // Reset all markers to blue
    markers.forEach(item => {
        item.marker.setIcon(L.icon({ iconUrl: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png' }));
        item.marker.closePopup(); // Close any open popups
    });

    // Find the marker for the selected mine and change color to red
    const targetMarker = markers.find(item => item.name === mineName);
    if (targetMarker) {
        targetMarker.marker.setIcon(L.icon({ iconUrl: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png' }));
        targetMarker.marker.openPopup(); // Open the popup for the selected marker

        map.setView([lat, lng], 12); // Zoom in to the selected mine location
    }
}

// Handle autocomplete suggestions
document.getElementById('coalMineInput').addEventListener('input', function () {
    var query = this.value;

    if (query.length > 2) {
        fetch(`/search_coal_mine?query=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log('Suggestions data:', data); // Debugging line
                const suggestions = document.getElementById('suggestions');
                suggestions.innerHTML = '';

                data.forEach(mine => {
                    const div = document.createElement('div');
                    div.classList.add('autocomplete-suggestion');
                    div.textContent = mine['Mine Name'];
                    div.setAttribute('data-lat', mine['Latitude']);
                    div.setAttribute('data-lng', mine['Longitude']);
                    div.addEventListener('click', function () {
                        const lat = this.getAttribute('data-lat');
                        const lng = this.getAttribute('data-lng');
                        const mineName = this.textContent;

                        updateMapWithSearchResult({ 'Latitude': lat, 'Longitude': lng, 'Mine Name': mineName });

                        // Clear suggestions
                        suggestions.innerHTML = '';
                        document.getElementById('coalMineInput').value = mineName;
                    });
                    suggestions.appendChild(div);
                });
            })
            .catch(error => console.log('Error fetching suggestions:', error));
    } else {
        document.getElementById('suggestions').innerHTML = '';
    }
});
