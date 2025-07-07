document.getElementById('queryForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const query = document.getElementById('query').value;
    
    fetch('/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // TASK: extract the fields from the returned data object and set the values of the form fields
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
