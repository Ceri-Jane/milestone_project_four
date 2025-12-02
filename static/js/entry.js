// Filter emotion list by search text
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("emotion-search");
    const emotionSelect = document.getElementById("emotion_words");

    if (!searchInput || !emotionSelect) return;

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();

        for (let option of emotionSelect.options) {
            const text = option.textContent.toLowerCase();
            option.style.display = text.includes(query) ? "block" : "none";
        }
    });
});