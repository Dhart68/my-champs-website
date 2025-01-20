def generate_video_player(video_urls, video_urls_js):
    """
    generate TML and JavaScript for a video player"""

    return f"""
<video id="videoPlayer" width="700" height="400" controls autoplay>
  <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
  Your browser does not support the video tag.
</video>

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

    // Handle video end and preload the next video
    videoPlayer.onended = function() {{
        currentVideoIndex++;
        if (currentVideoIndex < videoUrls.length) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();  // Reload the video player with the new source
            videoPlayer.play();  // Play the next video
            preloadNextVideo();  // Preload the next video in the background
        }}
    }};

    // Preload the second video when the first one starts playing
    videoPlayer.onplay = function() {{
        preloadNextVideo();
    }};
</script>

"""

def generate_video_player_2(video_urls):
    """
    Generate HTML and JavaScript for a video player with clickable zones for navigation,
    ensuring functionality in both normal and full-screen modes.

    Args:
        video_urls (list): List of video URLs to be played.

    Returns:
        str: HTML and JavaScript for the video player.
    """
    return f"""
    <div id="videoContainer" style="display: flex; justify-content: center; align-items: center; height: 100vh; position: relative;">
        <video id="videoPlayer" width="800" height="600" controls autoplay>
            <source src="{video_urls[0]}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <script>
        const videoPlayer = document.getElementById("videoPlayer");
        const videoContainer = document.getElementById("videoContainer");
        const videoList = {video_urls};
        let currentVideoIndex = 0;

        // Function to play a video based on the current index
        function playVideo(index) {{
            videoPlayer.src = videoList[index];
            videoPlayer.play();
        }}

        // Create dynamic click zones
        const leftClickArea = document.createElement("div");
        const rightClickArea = document.createElement("div");

        // Set styles dynamically for the left and right click zones
        const setClickZoneStyles = () => {{
            const rect = videoPlayer.getBoundingClientRect(); // Get video element's size and position

            // Common styles for both areas
            const baseStyles = `
                position: absolute;
                top: 0;
                height: 100%;
                cursor: pointer;
                z-index: 10;
            `;

            // Left area
            leftClickArea.style.cssText = `
                ${{baseStyles}}
                left: 0;
                width: 40%;
            `;

            // Right area
            rightClickArea.style.cssText = `
                ${{baseStyles}}
                right: 0;
                width: 40%;
            `;
        }};

        // Append click zones to the video container
        videoContainer.appendChild(leftClickArea);
        videoContainer.appendChild(rightClickArea);

        // Add event listeners to dynamically recalculate styles
        window.addEventListener("resize", setClickZoneStyles);
        document.addEventListener("fullscreenchange", setClickZoneStyles);
        setClickZoneStyles(); // Initial setup

        // Event for the right click area to play the next video
        rightClickArea.addEventListener("click", () => {{
            currentVideoIndex = (currentVideoIndex + 1) % videoList.length;
            playVideo(currentVideoIndex);
        }});

        // Event for the left click area to play the previous video
        leftClickArea.addEventListener("click", () => {{
            currentVideoIndex = (currentVideoIndex - 1 + videoList.length) % videoList.length;
            playVideo(currentVideoIndex);
        }});

        // Automatically play the next video when the current one ends
        videoPlayer.addEventListener("ended", () => {{
            currentVideoIndex = (currentVideoIndex + 1) % videoList.length;
            playVideo(currentVideoIndex);
        }});
    </script>
    """


def generate_video_player_3(video_urls):
    """
    Generate HTML and JavaScript for a video player with clickable zones for navigation,
    ensuring automatic playback and no looping.

    Args:
        video_urls (list): List of video URLs to be played.

    Returns:
        str: HTML and JavaScript for the video player.
    """
    return f"""
    <div id="videoContainer" style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <video id="videoPlayer" width="800" controls autoplay>
            <source src="{video_urls[0]}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <script>
        const videoPlayer = document.getElementById("videoPlayer");
        const videoList = {video_urls};
        let currentVideoIndex = 0;

        // Function to play a video based on the current index
        function playVideo(index) {{
            if (index >= 0 && index < videoList.length) {{
                videoPlayer.src = videoList[index];
                videoPlayer.play();
            }}
        }}



        // Add click listener to the video element
        videoPlayer.addEventListener("click", (event) => {{
            const rect = videoPlayer.getBoundingClientRect();
            const clickX = event.clientX - rect.left; // Click X relative to the video
            const videoWidth = rect.width;

            if (clickX < videoWidth * 0.3) {{
                // Left click area: Previous video
                if (currentVideoIndex > 0) {{
                    currentVideoIndex -= 1;
                    playVideo(currentVideoIndex);
                }}
            }} else if (clickX > videoWidth * 0.7) {{
                // Right click area: Next video
                if (currentVideoIndex < videoList.length - 1) {{
                    currentVideoIndex += 1;
                    playVideo(currentVideoIndex);
                }}
            }}
        }});

        // Automatically move to the next video when the current one ends
        videoPlayer.addEventListener("ended", () => {{
            if (currentVideoIndex < videoList.length - 1) {{
                currentVideoIndex += 1;
                playVideo(currentVideoIndex);
            }}
        }});
    </script>
    """

def generate_video_player_4(video_urls, video_urls_js): # Mistral
    """
    Generate HTML and JavaScript for a video player.
    """
    return f"""
<video id="videoPlayer" width="1200" height="675" controls autoplay>
  <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
  Your browser does not support the video tag.
</video>

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
    videoPlayer.addEventListener('click', function(event) {{
        const rect = videoPlayer.getBoundingClientRect();
        const x = event.clientX - rect.left; // x position within the element
        const width = rect.width;

        if (x < width / 2) {{
            // Click on the left half
            loadAndPlayPreviousVideo();
        }} else {{
            // Click on the right half
            loadAndPlayNextVideo();
        }}
    }});
</script>
"""

def generate_video_player_5(video_urls, video_urls_js): # Mistral
    """
    Generate HTML and JavaScript for a video player.
    """
    return f"""
<video id="videoPlayer" width="700" height="400" controls autoplay>
  <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
  Your browser does not support the video tag.
</video>

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

        if (x < width / 2) {{
            // Click on the left half
            loadAndPlayPreviousVideo();
        }} else {{
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
