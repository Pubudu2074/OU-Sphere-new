document.addEventListener("DOMContentLoaded", () => {
    // Fade-in Animation for Discussions
    const discussions = document.querySelectorAll(".discussion-list li");
    discussions.forEach((item, index) => {
        item.style.opacity = "0";
        item.style.transition = `all 0.5s ease ${index * 0.1}s`;
        setTimeout(() => {
            item.style.opacity = "1";
        }, index * 100);
    });

    // Delete Confirmation
    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            const confirmed = confirm("Are you sure you want to delete this discussion?");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Search Functionality
    const searchInput = document.getElementById("search-bar");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase();
            const discussions = document.querySelectorAll(".discussion-list li");
            discussions.forEach(item => {
                const title = item.querySelector("h2").innerText.toLowerCase();
                const content = item.querySelector("p").innerText.toLowerCase();
                if (title.includes(query) || content.includes(query)) {
                    item.style.display = "block";
                } else {
                    item.style.display = "none";
                }
            });
        });
    }
});
