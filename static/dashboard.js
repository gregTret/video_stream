const API_URL = "/dashboard";

async function fetchMovies() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Failed to fetch movies.");
        }

        const data = await response.json();
        populateTable(data);
    } catch (error) {
        console.error("Error fetching data, using fallback:", error);
    }
}

async function toggleStatus(oid) {
    const moviePayload = {
        "_id": { '$oid': oid }
    };
    try {
        const response = await fetch(`/updateRequest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(moviePayload)
        });

        if (!response.ok) {
            throw new Error("Failed to update status.");
        }
        fetchMovies();

    } catch (error) {
        console.error("Error updating status:", error);
    }
}

function populateTable(data) {
    const tableBody = document.querySelector("#data-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.message}</td>
            <td>${item.status}</td>
            <td><button class="update-status-btn" onclick="toggleStatus('${item._id.$oid}')">Update Status</button></td>
            `;

        tableBody.appendChild(row);
    });
}

function returnToHome() {
    window.location.href = '/movies';
}
function goToDashboard() {
    window.location.href = '/dashboardPage';
}


fetchMovies();

