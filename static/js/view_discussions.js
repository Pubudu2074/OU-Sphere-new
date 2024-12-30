document.getElementById('searchBar').addEventListener('keyup', function () {
    const query = this.value.toLowerCase();
    const items = document.querySelectorAll('.discussion-item');

    items.forEach(item => {
        const title = item.querySelector('h2').innerText.toLowerCase();
        const question = item.querySelector('p').innerText.toLowerCase();

        if (title.includes(query) || question.includes(query)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
