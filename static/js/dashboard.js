document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".activity-card");
    const greeting = document.querySelector("main h1");

    // Add hover effect to activity cards
    cards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-15px)";
        });
        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0)";
        });
    });

    // Set dynamic greeting based on the current time
    const currentTime = new Date().getHours();
    if (currentTime < 12) {
        greeting.textContent = `Good Morning, ${greeting.textContent.split(",")[1].trim()}`;
    } else if (currentTime < 18) {
        greeting.textContent = `Good Afternoon, ${greeting.textContent.split(",")[1].trim()}`;
    } else {
        greeting.textContent = `Good Evening, ${greeting.textContent.split(",")[1].trim()}`;
    }

    // Clock and Calendar
    function updateClockAndDate() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, "0");
        const minutes = now.getMinutes().toString().padStart(2, "0");
        const seconds = now.getSeconds().toString().padStart(2, "0");
        const clock = document.getElementById("clock");
        const date = document.getElementById("date");

        clock.textContent = `${hours}:${minutes}:${seconds}`;

        const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
        date.textContent = now.toLocaleDateString(undefined, options);
    }

    setInterval(updateClockAndDate, 1000);
    updateClockAndDate(); // Initialize immediately
});
