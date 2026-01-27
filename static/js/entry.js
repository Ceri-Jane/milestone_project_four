document.addEventListener("DOMContentLoaded", function () {

    // ============================================================
    // EMOTION WORD SEARCH FILTER
    // ============================================================
    const searchInput = document.getElementById("emotion-search");
    const emotionList = document.getElementById("emotion-list");

    if (searchInput && emotionList) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase();

            for (let item of emotionList.querySelectorAll(".emotion-item")) {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(query) ? "flex" : "none";
            }
        });
    }

    // ============================================================
    // HUE SLIDER RANGE LABEL (matches Entry.mood bands)
    // ============================================================
    const hueInput = document.getElementById("hue");
    const hueLabel = document.getElementById("hue-range-label");

    if (hueInput && hueLabel) {

        const getBandLabel = (value) => {
            const v = Number(value);

            if (v <= 19) return "Very low";
            if (v <= 39) return "Low";
            if (v <= 59) return "Neutral";
            if (v <= 79) return "Good";
            return "Very good";
        };

        const updateHueLabel = () => {
            hueLabel.textContent = `Current range: ${getBandLabel(hueInput.value)}`;
        };

        // Set label on page load (edit page needs this)
        updateHueLabel();

        // Update live while dragging
        hueInput.addEventListener("input", updateHueLabel);
        hueInput.addEventListener("change", updateHueLabel);
    }
});
