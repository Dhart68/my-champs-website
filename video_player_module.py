def generate_video_player(video_urls, video_urls_js):
    """
    Generate a video player:
    - Large on desktop
    - Positioned at top of view (Streamlit page)
    - Fullscreen optional via native controls
    - Safe for mobile
    """
    if not video_urls:
        return "<p>No videos available for this player.</p>"

    return f"""
<style>
#videoContainer {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
    width: 100%;
}}

#videoPlayer {{
    width: 90%;       /* Large on desktop */
    max-width: 1600px;
    height: auto;
    border-radius: 8px;
}}

@media (max-width: 768px) {{
    #videoPlayer {{
        width: 100%;   /* Full width on mobile */
        height: auto;
        border-radius: 0;
    }}
}}
</style>

<div id="videoContainer">
    <video id="videoPlayer" controls autoplay playsinline>
        <source id="videoSource" src="{video_urls[0]}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

<script>
    const videoUrls = [{video_urls_js}];
    let currentVideoIndex = 0;
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSource = document.getElementById("videoSource");

    function preloadNextVideo() {{
        if (currentVideoIndex + 1 < videoUrls.length) {{
            const nextVideo = document.createElement('video');
            nextVideo.src = videoUrls[currentVideoIndex + 1];
            nextVideo.preload = 'auto';
            nextVideo.load();
        }}
    }}

    async function loadAndPlay(index) {{
        if (index < 0 || index >= videoUrls.length) return;
        currentVideoIndex = index;
        videoSource.src = videoUrls[currentVideoIndex];
        videoPlayer.load();
        try {{ await videoPlayer.play(); }}
        catch (err) {{ console.warn("Autoplay blocked:", err); }}
        preloadNextVideo();
    }}

    function loadAndPlayNextVideo() {{ loadAndPlay(currentVideoIndex + 1); }}
    function loadAndPlayPreviousVideo() {{ loadAndPlay(currentVideoIndex - 1); }}

    videoPlayer.onended = loadAndPlayNextVideo;
    videoPlayer.onerror = loadAndPlayNextVideo;

    videoPlayer.addEventListener('click', function(e) {{
        const rect = videoPlayer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        if (x < rect.width / 3) loadAndPlayPreviousVideo();
        else if (x > rect.width * 2 / 3) loadAndPlayNextVideo();
    }});
</script>
"""
