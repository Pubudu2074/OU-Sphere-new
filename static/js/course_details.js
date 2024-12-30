document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".btn");

    // Add hover effect to buttons
    buttons.forEach((btn) => {
        btn.addEventListener("mouseenter", () => {
            btn.style.transform = "scale(1.1)";
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "scale(1)";
        });
    });

    // Smooth scroll to sections
    const links = document.querySelectorAll("a[href^='#']");
    links.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            targetElement.scrollIntoView({ behavior: "smooth" });
        });
    });
});
