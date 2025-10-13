def generate_video_player(video_urls, video_urls_js):
    """
    Generate responsive HTML + JS video player.
    - On desktop: centered video (1600x900)
    - On mobile: fullscreen in landscape (if allowed)
    - Graceful fallback if autorotation is blocked
    """

    if not video_urls:
        return "<p>No videos available for this player.</p>"

    return f"""
<style>
  #videoContainer {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }}

  video {{
    max-width: 100%;
    height: auto;
    border-radius: 12px;
  }}

  /* Overlay message */
  #rotateHint {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 16px;
    z-index: 9999;
    display: none;
    text-align: center;
  }}
</style>

<div id="videoContainer">
    <video id="videoPlayer" width="1600" height="900" controls autoplay playsinline>
        <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

<div id="rotateHint">🔁 Rotate your phone for best view</div>

<script>
    const videoUrls = [{video_urls_js}];
    let currentVideoIndex = 0;
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSource = document.getElementById("videoSource");
    const rotateHint = document.getElementById("rotateHint");

    function isMobile() {{
        return /Mobi|Android/i.test(navigator.userAgent);
    }}

    // Show a non-blocking overlay message
    function showRotateHint() {{
        rotateHint.style.display = 'block';
        setTimeout(() => {{
            rotateHint.style.display = 'none';
        }}, 4000);
    }}

    // Request fullscreen & try to lock orientation
    function requestFullscreenLandscape() {{
        if (isMobile() && videoPlayer.requestFullscreen) {{
            videoPlayer.requestFullscreen()
                .then(() => {{
                    if (screen.orientation && screen.orientation.lock) {{
                        screen.orientation.lock('landscape').catch(err => {{
                            console.log("Orientation lock not allowed:", err.message);
                            showRotateHint();
                        }});
                    }}
                }})
                .catch(err => {{
                    console.log("Fullscreen request failed:", err.message);
                }});
        }}
    }}

    // Auto-trigger when video starts playing
    videoPlayer.onplay = function() {{
        requestFullscreenLandscape();
        preloadNextVideo();
    }};

    function preloadNextVideo() {{
        if (currentVideoIndex + 1 < videoUrls.length) {{
            const nextVideo = document.createElement('video');
            nextVideo.src = videoUrls[currentVideoIndex + 1];
            nextVideo.preload = 'auto';
            nextVideo.load();
        }}
    }}

    function loadAndPlayNextVideo() {{
        currentVideoIndex++;
        if (currentVideoIndex < videoUrls.length) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();
            videoPlayer.play();
            preloadNextVideo();
        }}
    }}

    function loadAndPlayPreviousVideo() {{
        currentVideoIndex--;
        if (currentVideoIndex >= 0) {{
            videoSource.src = videoUrls[currentVideoIndex];
            videoPlayer.load();
            videoPlayer.play();
            preloadNextVideo();
        }}
    }}

    videoPlayer.onended = loadAndPlayNextVideo;

    videoPlayer.onerror = function() {{
        console.error("Error loading video:", videoPlayer.error);
        loadAndPlayNextVideo();
    }};

    function handleVideoClick(event) {{
        const rect = videoPlayer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const width = rect.width;

        if (x < width / 3) {{
            loadAndPlayPreviousVideo();
        }} else if (x > width / 1.4) {{
            loadAndPlayNextVideo();
        }}
    }}

    videoPlayer.addEventListener('click', handleVideoClick);
</script>
"""
