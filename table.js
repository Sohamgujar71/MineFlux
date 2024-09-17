const minesData = {
    "last-day": {
        CO2: [
            { rank: 1, mine: "Jambad UG", emission: 189 },
            { rank: 2, mine: "Narsumuda", emission: 173 },
            { rank: 3, mine: "DHEMOMAIN PIT", emission: 171 },
            { rank: 4, mine: "NORTH SEARSOLE", emission: 168 },
            { rank: 5, mine: "PATMOHONA", emission: 165 }
        ],
        CH4: [
            { rank: 1, mine: "KHOTADIH OC", emission: 200 },
            { rank: 2, mine: "SONEPUR BAZARI PROJECT", emission: 195 },
            { rank: 3, mine: "BEJDIH", emission: 190 },
            { rank: 4, mine: "CHITRA EAST", emission: 185 },
            { rank: 5, mine: "SALANPUR", emission: 180 }
        ]
    },
    "last-week": {
        CO2: [
            { rank: 1, mine: "Jambad UG", emission: 1 },
            { rank: 2, mine: "Narsumuda", emission: 2 },
            { rank: 3, mine: "DHEMOMAIN PIT", emission: 3 },
            { rank: 4, mine: "NORTH SEARSOLE", emission: 4 },
            { rank: 5, mine: "PATMOHONA", emission: 5 }
        ],
        CH4: [
            { rank: 1, mine: "Jambad UG", emission: 16},
            { rank: 2, mine: "Narsumuda", emission: 25},
            { rank: 3, mine: "DHEMOMAIN PIT", emission: 38},
            { rank: 4, mine: "NORTH SEARSOLE", emission: 42},
            { rank: 5, mine: "PATMOHONA", emission: 59}
        ]
    },
    "last-month": {
        CO2: [
            { rank: 1, mine: "KHOTADIH OC", emission: 200 },
            { rank: 2, mine: "SONEPUR BAZARI PROJECT", emission: 195 },
            { rank: 3, mine: "BEJDIH", emission: 190 },
            { rank: 4, mine: "CHITRA EAST", emission: 185 },
            { rank: 5, mine: "SALANPUR", emission: 180 }
        ],
        CH4: [
            { rank: 1, mine: "Jambad UG", emission: 189 },
            { rank: 2, mine: "Narsumuda", emission: 173 },
            { rank: 3, mine: "DHEMOMAIN PIT", emission: 171 },
            { rank: 4, mine: "NORTH SEARSOLE", emission: 168 },
            { rank: 5, mine: "PATMOHONA", emission: 165 }
        ]
    }
};

function updateData() {
    const timeRange = document.getElementById('time-range').value;
    const emissionType = document.getElementById('emission-type').value;

    const minesList = document.getElementById('mine-list');
    minesList.innerHTML = '';

    const data = minesData[timeRange][emissionType];

    data.forEach(mine => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="rank">${mine.rank}</td>
            <td>${mine.mine}</td>
            <td>${mine.emission}</td>
        `;
        minesList.appendChild(row);
    });
}

// Initial data population
updateData();
