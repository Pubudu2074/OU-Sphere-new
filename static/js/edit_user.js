document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (event) => {
        const role = document.getElementById("role").value;

        // Validation or confirmation alert
        if (!role) {
            alert("Please select a role.");
            event.preventDefault();
        } else {
            const confirmUpdate = confirm(`Are you sure you want to update the role to "${role}"?`);
            if (!confirmUpdate) {
                event.preventDefault();
            }
        }
    });
});
