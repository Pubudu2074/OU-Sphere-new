document.addEventListener("DOMContentLoaded", function () {
    const enrollButtons = document.querySelectorAll("form .btn");
    const searchInput = document.getElementById("search-input");
    const courseItems = document.querySelectorAll("ul li");

    // Dynamic Enroll Button
    enrollButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            button.textContent = "Enrolled";
            button.style.backgroundColor = "#ffa500";
            button.style.cursor = "not-allowed";
            button.disabled = true;
        });
    });

    // Search Courses
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase();
            courseItems.forEach((item) => {
                const title = item.querySelector("h2").textContent.toLowerCase();
                const description = item.querySelector("p").textContent.toLowerCase();
                if (title.includes(query) || description.includes(query)) {
                    item.style.display = "block";
                } else {
                    item.style.display = "none";
                }
            });
        });
    }
});
