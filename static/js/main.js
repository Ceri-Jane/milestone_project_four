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

    // ----------------------------------------
    // Start Regulate+ 5-day free trial (Stripe Checkout)
    // ----------------------------------------
    const startTrialBtn = document.getElementById("start-trial-btn");

    if (startTrialBtn) {
        startTrialBtn.addEventListener("click", async function () {
            const originalLabel = startTrialBtn.innerText;
            startTrialBtn.disabled = true;
            startTrialBtn.innerText = "Redirecting to Stripe…";

            try {
                const response = await fetch("/billing/start-trial/");

                // If the response isn't JSON (e.g. redirect because already subscribed),
                // just send the user back to the dashboard safely.
                const contentType = response.headers.get("content-type") || "";
                if (!contentType.includes("application/json")) {
                    window.location.href = "/dashboard/";
                    return;
                }

                const data = await response.json();

                if (data.session_url) {
                    // Redirect to Stripe Checkout
                    window.location.href = data.session_url;
                } else {
                    alert(
                        "Sorry, we couldn't start your free trial right now.\n" +
                        "Please try again in a moment."
                    );
                    startTrialBtn.disabled = false;
                    startTrialBtn.innerText = originalLabel;
                }

            } catch (error) {
                alert(
                    "Something went wrong contacting the payment server.\n" +
                    "Please check your connection and try again."
                );
                startTrialBtn.disabled = false;
                startTrialBtn.innerText = originalLabel;
            }
        });
    }

});
