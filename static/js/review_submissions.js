document.addEventListener('DOMContentLoaded', function () {
    // Filter submissions by student name
    const searchInput = document.getElementById('search-input');
    const rows = document.querySelectorAll('tbody tr');

    searchInput.addEventListener('input', function () {
        const searchValue = this.value.toLowerCase();
        rows.forEach(row => {
            const studentName = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
            if (studentName.includes(searchValue)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Confirmation before grading
    const gradeButtons = document.querySelectorAll('.grade-btn');
    gradeButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to grade this submission?')) {
                e.preventDefault();
            }
        });
    });

    // Confirmation before downloading
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (!confirm('Do you want to download this file?')) {
                e.preventDefault();
            }
        });
    });
});
