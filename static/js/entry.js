document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("emotion-search");
    const emotionList = document.getElementById("emotion-list");

    if (!searchInput || !emotionList) return;

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();

        for (let item of emotionList.querySelectorAll(".emotion-item")) {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? "flex" : "none";
        }
    });
});