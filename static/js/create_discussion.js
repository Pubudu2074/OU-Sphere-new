// Smooth animation for the header on load
document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header h1");
    header.style.opacity = "0";
    header.style.transform = "translateY(-20px)";
    header.style.transition = "all 1s ease-out";

    setTimeout(() => {
        header.style.opacity = "1";
        header.style.transform = "translateY(0)";
    }, 200);
});

// Form validation with modern design
document.querySelector("form").addEventListener("submit", function (e) {
    const title = document.getElementById("title").value.trim();
    const question = document.getElementById("question").value.trim();

    if (!title || !question) {
        e.preventDefault();
        showError("Please fill out both the Title and Question fields!");
    }
});

// Modern error display function
function showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = message;
    errorDiv.style.position = "fixed";
    errorDiv.style.top = "20px";
    errorDiv.style.right = "20px";
    errorDiv.style.background = "#ff5252";
    errorDiv.style.color = "#fff";
    errorDiv.style.padding = "10px 20px";
    errorDiv.style.borderRadius = "8px";
    errorDiv.style.boxShadow = "0 8px 15px rgba(0, 0, 0, 0.2)";
    errorDiv.style.zIndex = "1000";
    errorDiv.style.animation = "fadeOut 4s ease forwards";

    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 4000);
}

// Fade out animation for error message
const fadeOutKeyframes = `
@keyframes fadeOut {
    0% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        opacity: 0;
    }
}
`;
const styleSheet = document.createElement("style");
styleSheet.innerText = fadeOutKeyframes;
document.head.appendChild(styleSheet);
