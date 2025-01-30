

def generate_video_player(video_urls, video_urls_js): # Mistral
    """
    Generate HTML and JavaScript for a video player.
    """

    return f"""
<div id="videoContainer" style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <video id="videoPlayer" width="1600" height="900" controls autoplay>
        <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

<script>
    const videoUrls = [{video_urls_js}];
    let currentVideoIndex = 0;
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSource = document.getElementById("videoSource");

    // Function to preload the next video
    function preloadNextVideo() {{
        if (currentVideoIndex + 1 < videoUrls.length) {{
            const nextVideo = document.createElement('video');
            nextVideo.src = videoUrls[currentVideoIndex + 1];
            nextVideo.preload = 'auto'; // preload next video
            nextVideo.load();  // Start loading the next video
        }}
    }}

    // Function to load and play the next video
    function loadAndPlayNextVideo() {{
        currentVideoIndex++;
        if (currentVideoIndex < videoUrls.length) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();  // Reload the video player with the new source
            videoPlayer.play();  // Play the next video
            preloadNextVideo();  // Preload the next video in the background
        }}
    }}

    // Function to load and play the previous video
    function loadAndPlayPreviousVideo() {{
        currentVideoIndex--;
        if (currentVideoIndex >= 0) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();  // Reload the video player with the new source
            videoPlayer.play();  // Play the previous video
            preloadNextVideo();  // Preload the next video in the background
        }}
    }}

    // Handle video end and load the next video
    videoPlayer.onended = function() {{
        loadAndPlayNextVideo();
    }};

    // Preload the second video when the first one starts playing
    videoPlayer.onplay = function() {{
        preloadNextVideo();
    }};

    // Handle errors when loading the video
    videoPlayer.onerror = function() {{
        console.error("Error loading video:", videoPlayer.error);
        loadAndPlayNextVideo();  // Try to load the next video if there is an error
    }};

    // Handle clicks on the video to navigate to the next or previous video
    function handleVideoClick(event) {{
        const rect = videoPlayer.getBoundingClientRect();
        const x = event.clientX - rect.left; // x position within the element
        const width = rect.width;

        if (x < width / 3) {{
            // Click on the left half
            loadAndPlayPreviousVideo();
        }} else if (x > width / 1.4) {{
            // Click on the right half
            loadAndPlayNextVideo();
        }}
    }}

    // Add click event listener for normal and fullscreen modes
    videoPlayer.addEventListener('click', handleVideoClick);

    // Handle fullscreen change event
    videoPlayer.addEventListener('fullscreenchange', function() {{
        if (document.fullscreenElement) {{
            // Video is in fullscreen mode
            document.addEventListener('click', handleVideoClick);
        }} else {{
            // Video is not in fullscreen mode
            document.removeEventListener('click', handleVideoClick);
        }}
    }});

    // Handle fullscreen error event
    videoPlayer.addEventListener('fullscreenerror', function() {{
        console.error('Fullscreen mode failed');
    }});
</script>
"""


def generate_video_player_2(video_urls, video_urls_js):  # Deepseek
    """
    Generate HTML and JavaScript for a video player with next/previous navigation in fullscreen mode.
    """

    return f"""
<div id="videoContainer" style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <video id="videoPlayer" width="1600" height="900" controls autoplay>
        <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

<script>
    const videoUrls = {video_urls_js};
    let currentVideoIndex = 0;
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSource = document.getElementById("videoSource");

    // Function to preload the next video
    function preloadNextVideo() {{
        if (currentVideoIndex + 1 < videoUrls.length) {{
            const nextVideo = document.createElement('video');
            nextVideo.src = videoUrls[currentVideoIndex + 1];
            nextVideo.preload = 'auto'; // preload next video
            nextVideo.load();  // Start loading the next video
        }}
    }}

    // Function to load and play the next video
    function loadAndPlayNextVideo() {{
        currentVideoIndex++;
        if (currentVideoIndex < videoUrls.length) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();  // Reload the video player with the new source
            videoPlayer.play();  // Play the next video
            preloadNextVideo();  // Preload the next video in the background
        }}
    }}

    // Function to load and play the previous video
    function loadAndPlayPreviousVideo() {{
        currentVideoIndex--;
        if (currentVideoIndex >= 0) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();  // Reload the video player with the new source
            videoPlayer.play();  // Play the previous video
            preloadNextVideo();  // Preload the next video in the background
        }}
    }}

    // Handle video end and load the next video
    videoPlayer.onended = function() {{
        loadAndPlayNextVideo();
    }};

    // Preload the second video when the first one starts playing
    videoPlayer.onplay = function() {{
        preloadNextVideo();
    }};

    // Handle errors when loading the video
    videoPlayer.onerror = function() {{
        console.error("Error loading video:", videoPlayer.error);
        loadAndPlayNextVideo();  // Try to load the next video if there is an error
    }};

    // Handle clicks on the video to navigate to the next or previous video
    function handleVideoClick(event) {{
        const rect = videoPlayer.getBoundingClientRect();
        const x = event.clientX - rect.left; // x position within the element
        const width = rect.width;

        if (x < width / 3) {{
            // Click on the left third
            loadAndPlayPreviousVideo();
        }} else if (x > (2 * width) / 3) {{
            // Click on the right third
            loadAndPlayNextVideo();
        }}
    }}

    // Add click event listener for normal and fullscreen modes
    videoPlayer.addEventListener('click', handleVideoClick);

    // Handle fullscreen change event
    function handleFullscreenChange() {{
        if (document.fullscreenElement) {{
            // Video is in fullscreen mode
            document.addEventListener('click', handleVideoClick);
            document.addEventListener('keydown', handleKeyDown);
        }} else {{
            // Video is not in fullscreen mode
            document.removeEventListener('click', handleVideoClick);
            document.removeEventListener('keydown', handleKeyDown);
        }}
    }}

    // Handle keyboard shortcuts for navigation
    function handleKeyDown(event) {{
        switch (event.key) {{
            case 'ArrowLeft':
                loadAndPlayPreviousVideo();
                break;
            case 'ArrowRight':
                loadAndPlayNextVideo();
                break;
        }}
    }}

    // Add fullscreen change event listener
    videoPlayer.addEventListener('fullscreenchange', handleFullscreenChange);

    // Handle fullscreen error event
    videoPlayer.addEventListener('fullscreenerror', function() {{
        console.error('Fullscreen mode failed');
    }});
</script>
"""
