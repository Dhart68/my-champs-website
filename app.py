import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreMatchupsV3


from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image
from video_player_module import generate_video_player_5
from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores


st.set_page_config(layout="wide")

active_players= players.get_active_players()
list_active_players = [player['full_name'] for player in active_players]


##### lots to do ####
# CSS

# Display 3 star players pictures and main stats (last game PTS, RBD, AST)
# when you click on a picture you launch the viewer with all the selectbox defined

# Add a PLUS button to add another player

# Display last scores of the day
# https://cdn.nba.com/static/json/staticData/EliasGameStats/00/day_scores.txt
# Example news items
[games_date, scores_day] = get_last_scores()

news = [games_date, str(scores_day), games_date, str(scores_day)]

# Display the news ticker
display_news_ticker(news_items=news, duration=40)

# Add a video at the end of the sequence

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Choose the player
with col1:
    player_picked = st.selectbox(
    "Choose your champ",
    list_active_players,
    index=None,
    placeholder="Select a player...",
    )

# Conditional logic to handle the case where no option is selected
if player_picked:
    # Function to get the stats of the 3 last games for the player picked
    [last_5_games, player_id] = player_last_stats(player_picked)

    # get the image of the player and display it
    image_picked = get_player_image(player_id)

    player_caption = player_picked # add more info here from get_player_image

    # Create two columns
    col4, col5 = st.columns([1,6])

    # Display image in the first column
    with col4:
        st.image(image_picked, caption=player_caption, width=250)

    # Display DataFrame in the second column
    with col5:
        st.dataframe(last_5_games, hide_index=True, height=210)


    ### to do ###
    # Add the scores

    # Select a game and find location
    with col2:
        game_id = st.selectbox(
            "Choose your game",
            last_5_games['Game_ID'],
            index=None,
            placeholder="Select a Game_ID...",
        )


    if game_id:
        game_location = last_5_games[last_5_games['Game_ID']==game_id]['location'].values[0]

        # Choose an option
        with col3:
            option = st.selectbox(
                "Choose your video option",
                ['Full', 'Best'],
                index=None,
                placeholder="Select a sequences options...",
            )

        # Conditional logic to handle the case where no option is selected
        if option:
            # Function to get the videos of the selected game for the player
            video_event_df = get_mp4_urls(player_id, game_id, game_location, option)

            video_urls = video_event_df['video'].to_list()
            st.write(f'There is {len(video_urls)} sequences')

            # Add a video at the end of the list
            #video_urls.append("https://www.youtube.com/watch?v=3Qz1GMpOtUY")

            # Convert Python list of URLs to a JavaScript-compatible array
            video_urls_js = ','.join(f'"{url}"' for url in video_urls) # needed for the first video player

            # Load the video player
            video_player_html = generate_video_player_5(video_urls, video_urls_js)
            #video_player_html = generate_video_player_3(video_urls)

            # Display the video player in Streamlit
            if st.button("Play sequences", type="primary"):
                st.components.v1.html(video_player_html, height=500)


# Module of data analysis
## plotly to make the chart settable
## display evolution of min per game over time
## as for babies, add mean and tendancy for player at the same position
## forecast the previous chart

# ML/AI
## to think about it
