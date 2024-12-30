document.addEventListener("DOMContentLoaded", () => {
    // Highlight new replies dynamically
    const replyList = document.querySelectorAll(".reply-list li");
    replyList.forEach((reply, index) => {
        setTimeout(() => {
            reply.style.opacity = "1";
        }, index * 100);
    });

    // Character Count for Textarea
    const textarea = document.querySelector("textarea");
    if (textarea) {
        const charCount = document.createElement("div");
        charCount.style.textAlign = "right";
        charCount.style.color = "#777";
        charCount.style.fontSize = "0.9rem";
        textarea.parentNode.insertBefore(charCount, textarea.nextSibling);

        textarea.addEventListener("input", () => {
            charCount.textContent = `${textarea.value.length} / 500 characters`;
            if (textarea.value.length > 500) {
                charCount.style.color = "red";
            } else {
                charCount.style.color = "#777";
            }
        });
    }

    // Smooth Scroll for Replies
    const replySection = document.querySelector(".reply-list");
    if (replySection) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.style.transform = "translateY(0)";
                        entry.target.style.opacity = "1";
                    }
                });
            },
            { threshold: 0.1 }
        );

        replyList.forEach((reply) => {
            reply.style.opacity = "0";
            reply.style.transform = "translateY(20px)";
            observer.observe(reply);
        });
    }
});
