// static/js/main.js

// Stop the hero video from looping.
// Runs when the page has loaded.
document.addEventListener("DOMContentLoaded", function () {

    // Select the hero video
    const video = document.querySelector(".video-container video");
    if (video) {
        // When the video finishes, pause it so it doesn’t replay
        video.addEventListener("ended", () => {
            video.pause();
            video.currentTime = video.duration; // Hold last frame
        });
    }

    // Auto-hide Django success messages after 3 seconds
    const alerts = document.querySelectorAll(".alert-success");

    alerts.forEach(alert => {
        // Fade out after 3 seconds
        setTimeout(() => {
            alert.classList.add("fade-out");
        }, 3000);

        // Remove the element after fade-out completes
        setTimeout(() => {
            alert.remove();
        }, 4000);
    });

    // Ask for confirmation before deleting an entry from the dashboard
    const deleteForms = document.querySelectorAll(".delete-entry-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function (event) {
            const confirmed = window.confirm(
                "Are you sure you want to delete this entry?\n\n" +
                "This will permanently remove it from your history."
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // ----------------------------------------
    // Dismissible dashboard announcements
    // ----------------------------------------
    // Behaviour:
    // - Announcement shows when user logs in
    // - User can dismiss it with the "X"
    // - It stays hidden while they remain logged in
    // - It re-appears after logout + login (because login_key changes)
    //
    // Implementation:
    // - dashboard.html sets #dashboard-announcements with data-login-key
    // - Each alert includes data-announcement-id and data-announcement-updated
    // - Store a dismissal in localStorage keyed by login + announcement + updated_at
    const announceWrap = document.getElementById("dashboard-announcements");

    if (announceWrap) {
        const loginKey = announceWrap.dataset.loginKey || "no-last-login";

        // Want the alert to come back after "a few days" even without logging out.
        // Set ttlDays = 0, if not (change as an when required).
        const ttlDays = 5;
        const ttlMs = ttlDays * 24 * 60 * 60 * 1000;

        const announceAlerts = announceWrap.querySelectorAll("[data-announcement-id]");

        announceAlerts.forEach((alertEl) => {
            const announcementId = alertEl.dataset.announcementId;
            const updatedAt = alertEl.dataset.announcementUpdated || "";

            // Include updatedAt so if admin edits an announcement, it shows again
            const storageKey =
                `regulate_announce_dismissed_${loginKey}_${announcementId}_${updatedAt}`;

            const stored = localStorage.getItem(storageKey);

            // If dismissed before, hide it (TTL optional)
            if (stored) {
                if (ttlDays > 0) {
                    const dismissedAt = parseInt(stored, 10);
                    if (!Number.isNaN(dismissedAt) && (Date.now() - dismissedAt) < ttlMs) {
                        alertEl.remove();
                        return;
                    }
                    // TTL expired → allow it to show again
                    localStorage.removeItem(storageKey);
                } else {
                    // No TTL mode: hide until next login
                    alertEl.remove();
                    return;
                }
            }

            // When Bootstrap alert is closed, store dismissal timestamp
            alertEl.addEventListener("closed.bs.alert", () => {
                localStorage.setItem(storageKey, String(Date.now()));
            });
        });
    }

    // ----------------------------------------
    // Supportive phrases (external API)
    // ----------------------------------------
    const quoteBtn = document.getElementById("generate-quote-btn");
    const quoteText = document.getElementById("supportive-quote-text");
    const quoteAuthor = document.getElementById("supportive-quote-author");

    // Only run on the dashboard where these elements exist
    if (quoteBtn && quoteText && quoteAuthor) {

        quoteBtn.addEventListener("click", async function () {

            // Loading state
            quoteBtn.disabled = true;
            const originalLabel = quoteBtn.innerText;
            quoteBtn.innerText = "Generating…";
            quoteText.innerText = "Please wait…";
            quoteAuthor.innerText = "";

            try {
                const response = await fetch("/api/supportive-phrase/", {
                    cache: "no-store",
                    headers: { "Accept": "application/json" },
                });

                const data = await response.json();

                // Support multiple possible response shapes
                const phrase =
                    data.quote ||
                    data.phrase ||
                    data.affirmation ||
                    data.message ||
                    data.text ||
                    (typeof data === "string" ? data : null);

                quoteText.innerText = phrase || "You are doing better than you think.";

                // Author is optional
                const author = data.author || data.by || data.source || "";
                quoteAuthor.innerText = author ? "— " + author : "";

            } catch (error) {
                quoteText.innerText =
                    "Could not load a phrase right now — but you still deserve kindness.";
                quoteAuthor.innerText = "";
            }

            // Reset button
            quoteBtn.disabled = false;
            quoteBtn.innerText = originalLabel;
        });
    }

});
