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
    const deleteForms = document.querySelectorAll(".entry-delete-form");

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
});
