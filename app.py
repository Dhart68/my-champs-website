import streamlit as st

from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image

st.title('my-champs!')

player_picked = st.text_input("Player Name", "victor wembanyama")

# Function to get the stats of the day for the player
[last_3_games, player_id] = player_last_stats(player_picked)

last_game_id = last_3_games['Game_ID'][0]
last_game_location = last_3_games['location'][0]

# get the image of the player and display it
image_picked = get_player_image(player_id)
st.image(image_picked, caption=player_picked, width=250)

# Display the stats of the last 3 games
st.dataframe(last_3_games.drop(['location'], axis = 1))

# Select a game
'''
# Add a radio button to select rows
selected_index = st.radio("Select a game:", last_3_games.index, format_func=lambda i: last_3_games.loc[i, 'Game_ID'])

# Show details of the selected row
st.write("### Selected Row Details:")
st.write(last_3_games.loc[selected_index])

game_selected = last_3_games.loc[selected_index]['Game_ID']
'''
game_selected = last_game_id

# Function to get the stats of the day for the player
video_event_df = get_mp4_urls(player_id, game_selected, last_game_location, option = 'Best')

video_urls = video_event_df['video'].to_list()
# Add a video at the end of the list
#video_urls.append("https://www.youtube.com/watch?v=3Qz1GMpOtUY")

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
