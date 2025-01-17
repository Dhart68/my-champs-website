import streamlit as st

from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image

'''
# my-champs front
'''

st.title('my-champs!')


st.markdown('''This is my-champs website ''')

player_picked = st.text_input("Player Name", "victor wembanyama")
st.write("The current movie title is", player_picked)

# Function to get the stats of the day for the player
[last_3_games, player_id] = player_last_stats(player_picked)

last_game_id = last_3_games['Game_ID'][0]
last_game_location = last_3_games['location'][0]

# get the image of the player and display it
image_picked = get_player_image(player_id)
st.image(image_picked, caption=player_picked, width=100)

# Display the stats of the last 3 games
st.dataframe(last_3_games.drop(['Game_ID','location'], axis = 1))

# Function to get the stats of the day for the player
video_event_df = get_mp4_urls(player_id, last_game_id, last_game_location)

video_urls = video_event_df['video'].to_list()

# Convert Python list of URLs to a JavaScript-compatible array
video_urls_js = ','.join(f'"{url}"' for url in video_urls)

# HTML and JavaScript for the smooth video transition with preloading
video_player_html = f"""
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

# Display the video player in Streamlit
st.components.v1.html(video_player_html, height=500)
