document.addEventListener("DOMContentLoaded", () => {
    const titleInput = document.getElementById("title");
    const questionInput = document.getElementById("question");

    // Add live character counter for the textarea
    const charCounter = document.createElement("div");
    charCounter.style.textAlign = "right";
    charCounter.style.fontSize = "0.9rem";
    charCounter.style.color = "#555";
    questionInput.parentNode.insertBefore(charCounter, questionInput.nextSibling);

    questionInput.addEventListener("input", () => {
        const length = questionInput.value.length;
        charCounter.textContent = `${length}/500 characters`;
        if (length > 500) {
            charCounter.style.color = "red";
        } else {
            charCounter.style.color = "#555";
        }
    });

    // Real-time input validation
    const validateInput = (input) => {
        if (input.value.trim() === "") {
            input.style.borderColor = "red";
        } else {
            input.style.borderColor = "#36CDB7";
        }
    };

    titleInput.addEventListener("input", () => validateInput(titleInput));
    questionInput.addEventListener("input", () => validateInput(questionInput));

    // Add button animation on hover
    const button = document.querySelector("form button");
    button.addEventListener("mouseover", () => {
        button.style.transform = "scale(1.1)";
        button.style.boxShadow = "0 10px 20px rgba(0, 0, 0, 0.2)";
    });

    button.addEventListener("mouseout", () => {
        button.style.transform = "scale(1)";
        button.style.boxShadow = "0 5px 10px rgba(0, 0, 0, 0.2)";
    });
});
