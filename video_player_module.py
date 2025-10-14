def generate_video_player_best_computer_only(video_urls, video_urls_js):
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


# with popup for mobile
def generate_video_player(video_urls, video_urls_js):
    """
    - Desktop: original wide video player (unchanged)
    - Mobile: popup video overlay (optional fullscreen)
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

  /* Popup only for mobile */
  #popupOverlay {{
    display: none;
    position: fixed;
    z-index: 10000;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.95);
    justify-content: center;
    align-items: center;
  }}

  #popupVideo {{
    width: 100%;
    max-width: 600px;
    border-radius: 10px;
  }}

  .popupClose {{
    position: absolute;
    top: 10px;
    right: 20px;
    font-size: 28px;
    color: white;
    cursor: pointer;
  }}
</style>

<div id="videoContainer">
    <video id="videoPlayer" width="1600" height="900" controls autoplay playsinline>
        <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

<div id="rotateHint">🔁 Rotate your phone for best view</div>

<!-- Popup overlay (mobile only) -->
<div id="popupOverlay">
  <span class="popupClose" onclick="closePopup()">&times;</span>
  <video id="popupVideo" controls playsinline></video>
</div>

<script>
const videoUrls = [{video_urls_js}];
let currentVideoIndex = 0;
const videoPlayer = document.getElementById("videoPlayer");
const videoSource = document.getElementById("videoSource");
const popupOverlay = document.getElementById("popupOverlay");
const popupVideo = document.getElementById("popupVideo");
const rotateHint = document.getElementById("rotateHint");

function isMobile() {{
  return /Mobi|Android/i.test(navigator.userAgent);
}}

function showRotateHint() {{
  rotateHint.style.display = 'block';
  setTimeout(() => {{ rotateHint.style.display = 'none'; }}, 4000);
}}

function requestFullscreenLandscape() {{
  if (isMobile() && videoPlayer.requestFullscreen) {{
    videoPlayer.requestFullscreen()
      .then(() => {{
        if (screen.orientation && screen.orientation.lock) {{
          screen.orientation.lock('landscape').catch(() => showRotateHint());
        }}
      }})
      .catch(err => console.log("Fullscreen failed:", err.message));
  }}
}}

function preloadNextVideo() {{
  if (currentVideoIndex + 1 < videoUrls.length) {{
    const next = document.createElement('video');
    next.src = videoUrls[currentVideoIndex + 1];
    next.preload = 'auto';
    next.load();
  }}
}}

function loadAndPlay(index) {{
  if (index >= 0 && index < videoUrls.length) {{
    currentVideoIndex = index;
    videoSource.src = videoUrls[index];
    videoPlayer.load();
    videoPlayer.play();
    preloadNextVideo();
  }}
}}

function loadAndPlayNextVideo() {{
  loadAndPlay(currentVideoIndex + 1);
}}

function loadAndPlayPreviousVideo() {{
  loadAndPlay(currentVideoIndex - 1);
}}

videoPlayer.onplay = function() {{
  if (isMobile()) {{
    // pause inline video and open popup instead
    videoPlayer.pause();
    openPopup();
  }} else {{
    requestFullscreenLandscape();
    preloadNextVideo();
  }}
}};

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

/* Popup functions for mobile */
function openPopup() {{
  popupOverlay.style.display = "flex";
  popupVideo.src = videoUrls[currentVideoIndex];
  popupVideo.load();
  popupVideo.play();
}}

function closePopup() {{
  popupOverlay.style.display = "none";
  popupVideo.pause();
}}
</script>
"""
