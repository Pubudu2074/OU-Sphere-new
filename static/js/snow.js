document.addEventListener("DOMContentLoaded", function () {
    console.log("Snow effect script loaded."); // Debug message

    // Number of snowflakes
    const snowflakeCount = 100;

    // Create a container for snowflakes
    const snowContainer = document.createElement("div");
    snowContainer.id = "snow-container";
    document.body.appendChild(snowContainer);

    console.log("Snow container added to the page."); // Debug message

    // Create and style snowflakes
    for (let i = 0; i < snowflakeCount; i++) {
        const snowflake = document.createElement("div");
        snowflake.className = "snowflake";
        snowflake.textContent = "❄"; // Snowflake symbol
        snowflake.style.left = `${Math.random() * 100}vw`; // Random horizontal position
        snowflake.style.animationDuration = `${Math.random() * 5 + 5}s`; // Random fall duration
        snowflake.style.animationDelay = `${Math.random() * 5}s`; // Random delay
        snowflake.style.fontSize = `${Math.random() * 1.5 + 0.5}rem`; // Random size
        snowflake.style.opacity = Math.random(); // Random opacity
        snowContainer.appendChild(snowflake);
    }

    console.log("Snowflakes created."); // Debug message

    // Optional cleanup when navigating away
    window.addEventListener("beforeunload", () => {
        snowContainer.remove();
        console.log("Snow container removed."); // Debug message
    });
});
