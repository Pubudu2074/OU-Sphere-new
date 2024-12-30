document.addEventListener("DOMContentLoaded", () => {
    console.log("Modern Study Groups JS loaded!");

    const searchInput = document.getElementById("search-bar");
    const groups = document.querySelectorAll(".group-item");

    // Search Functionality
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
        groups.forEach((group) => {
            const groupName = group.querySelector("h2").innerText.toLowerCase();
            const groupDescription = group.querySelector("p").innerText.toLowerCase();
            if (groupName.includes(query) || groupDescription.includes(query)) {
                group.style.display = "block";
                group.style.opacity = 1;
            } else {
                group.style.display = "none";
            }
        });
    });

    // Add dynamic hover effect
    groups.forEach((group) => {
        group.addEventListener("mouseenter", () => {
            group.style.transition = "all 0.3s ease";
            group.style.transform = "scale(1.05)";
        });

        group.addEventListener("mouseleave", () => {
            group.style.transform = "scale(1)";
        });
    });

    // Floating Confetti Animation
    const confettiContainer = document.createElement("div");
    confettiContainer.classList.add("confetti-container");
    document.body.appendChild(confettiContainer);

    function createConfetti() {
        const confetti = document.createElement("div");
        confetti.classList.add("confetti");
        confetti.style.left = Math.random() * 100 + "vw";
        confetti.style.animationDuration = Math.random() * 3 + 2 + "s";
        confettiContainer.appendChild(confetti);

        setTimeout(() => {
            confetti.remove();
        }, 5000);
    }

    setInterval(createConfetti, 300);
});
