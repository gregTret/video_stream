
const searchInput = document.getElementById('searchBar');
const resultsBox = document.getElementById('results-box');


searchInput.addEventListener('input', async () => {
    const query = searchInput.value.toLowerCase().trim();
    // If input is empty, hide results
    if (query === '') {
        resultsBox.style.display = 'none';
    } else {
        // Filter movies based on the query
        const response = await fetch('/searchGeneric?q=' + query, {
            method: "GET",
        }).then((response) => response.json())
            .then((data) => {
                if (data.length > 0) {
                    resultsBox.innerHTML = data.map(movie => `<div onclick="location.href='/movie?url=${movie['video']}'"">${movie['title']}</div>`).join('');
                    resultsBox.style.display = 'block';
                } else {
                    resultsBox.style.display = 'none';
                }
            })
    }
});
