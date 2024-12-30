// Ripple effect on buttons
document.querySelectorAll('.actions .btn').forEach(button => {
    button.addEventListener('click', function (e) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        this.appendChild(ripple);

        const rect = this.getBoundingClientRect();
        ripple.style.left = `${e.clientX - rect.left}px`;
        ripple.style.top = `${e.clientY - rect.top}px`;

        setTimeout(() => ripple.remove(), 600); // Remove ripple after animation
    });
});

// Search bar functionality
document.getElementById('userSearch').addEventListener('keyup', function () {
    const query = this.value.toLowerCase(); // Get search input and convert to lowercase
    const rows = document.querySelectorAll('.users-table tbody tr'); // Get all table rows

    rows.forEach(row => {
        const username = row.cells[0].innerText.toLowerCase(); // Get the username cell value
        if (username.includes(query)) {
            row.style.display = ''; // Show the row if it matches the query
        } else {
            row.style.display = 'none'; // Hide the row if it doesn't match
        }
    });
});
