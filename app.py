import streamlit as st

from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image
from nba_api.stats.static import players

st.set_page_config(layout="wide")

st.title('my-champs!')

active_players= players.get_active_players()
list_active_players = [player['full_name'] for player in active_players]


##### to do ###
# remove the error/warning message when selectbox are not filled

# Display 3 stars pictures and main stats (last game PTS, RBD, AST)

# when you click on a picture you launch the viewer with all the selectbox defined
# Add a PLUS button to add another player

# Display last scores of the day


player_picked = st.selectbox(
    "Choose your champ",
    list_active_players,
    index=None,
    placeholder="Select a player...",
)

# Function to get the stats of the 3 last games for the player picked
[last_5_games, player_id] = player_last_stats(player_picked)

# get the image of the player and display it
image_picked = get_player_image(player_id)

# Create two columns
col1, col2 = st.columns([1,6])

# Display image in the first column
with col1:
    st.image(image_picked, caption=player_picked, width=250)

# Display DataFrame in the second column
with col2:
    st.dataframe(last_5_games, hide_index=True, height=200)


### to do ###
# Add the scores

# Select a game and find location
game_id = st.selectbox(
    "Choose your game",
    last_5_games['Game_ID'],
    index=None,
    placeholder="Select a Game_ID...",
)

game_location = last_5_games[last_5_games['Game_ID']==game_id]['location'].values[0]

# Choose an option
option = st.selectbox(
    "Choose your video option",
    ['Full', 'Best'],
    index=None,
    placeholder="Select a sequences options...",
)

# Function to get the videos of the selected gamey for the player
video_event_df = get_mp4_urls(player_id, game_id, game_location, option)

video_urls = video_event_df['video'].to_list()
st.write(f'There is {len(video_urls)} sequences')

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
if st.button("Play sequences", type="primary"):
    st.components.v1.html(video_player_html, height=500)
