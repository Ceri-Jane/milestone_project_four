// Stop the hero video from looping.
// Runs when the page has loaded.
document.addEventListener("DOMContentLoaded", function () {

    // Select the hero video
    const video = document.querySelector(".video-container video");
    if (!video) return;

    // When the video finishes, pause it so it doesn’t replay
    video.addEventListener("ended", () => {
        video.pause();
        video.currentTime = video.duration; // Hold last frame
    });
});
