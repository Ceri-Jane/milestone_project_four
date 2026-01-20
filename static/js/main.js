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
                const response = await fetch("/api/supportive-phrase/");
                const data = await response.json();

                quoteText.innerText =
                    data.quote || "You are doing better than you think.";

                if (data.author) {
                    quoteAuthor.innerText = "— " + data.author;
                } else {
                    quoteAuthor.innerText = "";
                }

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

    /**
     * Helper: start a Stripe flow via fetch, then redirect.
     * This avoids the “extra popup” problem by:
     * - preventing default navigation on the <a>
     * - only showing an alert on true network failure
     * - if the server returns HTML (redirect/messages), we just navigate to dashboard
     */
    async function startStripeFlow({
        buttonEl,
        endpoint,
        loadingText
    }) {
        if (!buttonEl) return;

        buttonEl.addEventListener("click", async function (event) {
            // Important: stop the <a> from navigating immediately
            event.preventDefault();

            const originalLabel = buttonEl.innerText;
            buttonEl.classList.add("disabled");
            buttonEl.setAttribute("aria-disabled", "true");
            buttonEl.innerText = loadingText;

            try {
                const response = await fetch(endpoint, {
                    method: "GET",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                });

                const contentType = response.headers.get("content-type") || "";

                // If the backend chose to redirect / show messages,
                // it'll come back as HTML (NOT JSON). That’s not an error.
                if (!contentType.includes("application/json")) {
                    window.location.href = "/dashboard/";
                    return;
                }

                const data = await response.json();

                if (data.session_url) {
                    window.location.href = data.session_url;
                    return;
                }

                // JSON response but no session url → just go back and show message
                window.location.href = "/dashboard/";

            } catch (error) {
                // True network/server error only
                alert(
                    "Sorry — we couldn’t reach the payment server.\n" +
                    "Please try again in a moment."
                );

                buttonEl.classList.remove("disabled");
                buttonEl.removeAttribute("aria-disabled");
                buttonEl.innerText = originalLabel;
            }
        });
    }

    // ----------------------------------------
    // Start Regulate+ 5-day free trial (Stripe Checkout)
    // ----------------------------------------
    const startTrialBtn = document.getElementById("start-trial-btn");

    startStripeFlow({
        buttonEl: startTrialBtn,
        endpoint: "/billing/start-trial/",
        loadingText: "Redirecting to Stripe…"
    });

    // ----------------------------------------
    // Subscribe (no trial available / trial already used)
    // ----------------------------------------
    const startSubscriptionBtn = document.getElementById("start-subscription-btn");

    startStripeFlow({
        buttonEl: startSubscriptionBtn,
        endpoint: "/billing/start-subscription/",
        loadingText: "Redirecting to Stripe…"
    });

});
