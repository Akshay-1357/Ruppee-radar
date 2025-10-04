document.getElementById('incomeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/income', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            // After successful POST, fetch updated income data
            return fetch('/income_data')
                .then(res => res.json())
                .then(data => {
                    const tbody = document.getElementById('incomeTableBody');
                    tbody.innerHTML = '';
                    data.forEach(inc => {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${inc.source}</td><td>${inc.amount}</td><td>${inc.date}</td>`;
                        tbody.appendChild(row);
                    });
                    // Clear form inputs after update
                    form.reset();
                });
        } else {
            console.error('Failed to add income');
        }
    })
    .catch(error => console.error('Error:', error));
});