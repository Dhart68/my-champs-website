import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreMatchupsV3


from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image
from video_player_module import generate_video_player
from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from get_3_best_players import get_3_best_players

st.set_page_config(layout="wide")

active_players= players.get_active_players()
list_active_players = [player['full_name'] for player in active_players]


##### lots to do ####
# Cookie to recognize the user or account?

# Create 2 columns for scores and top 10
col_00, col_01 = st.columns([9,1], vertical_alignment="center")

# Display last scores of the day
[games_date, number_of_games, scores, scores_df] = get_last_scores()

# Display the news ticker
news = [games_date, str(scores), games_date, str(scores)]
with col_00:
  display_news_ticker(news_items=news, duration=30)

# Display the dataframe
#with col_00:
#    st.table(scores_df)#, hide_index=True,  height=30)

# top 10
top_10_url = 'https://www.nba.com/watch/video/fridays-top-plays-80?plsrc=nba&collection=more-to-watch'
# https://www.nba.com/watch/video/sundays-top-plays-74?plsrc=nba&collection=more-to-watch
# https://www.nba.com/watch/video/saturdays-top-plays-250125?plsrc=nba&collection=more-to-watch

with col_01:
    st.link_button("Top 10", top_10_url)

# Display 3 star players pictures and main stats (last game PTS, RBD, AST)
# when you click on a picture you launch the viewer with all the selectbox defined
playerS_name=['victor wembanyama', 'bilal coulibaly', 'moussa diabate']

# Create 4 columns
colA, colB, colC, colD, colE = st.columns(5)
# for the 3 best players + one empty to fill by the user
# each column = image + nom
[picked_players, picked_players_info] = get_3_best_players(playerS_name)
images_picked = picked_players['img']
players_names = picked_players['player_name']

with colB:
    st.image(images_picked[0], caption=players_names[0].title(), width=250)
    st.dataframe(picked_players_info[picked_players_info['Name'] == players_names[0].lower()][['PTS','REB','AST']], hide_index=True, height=60)

with colC:
    st.image(images_picked[1], caption=players_names[1].title(), width=250)

with colD:
    st.image(images_picked[2], caption=players_names[2].title(), width=250)

#with colE:


# Add a video at the end of the sequence

# Create 2 columns for menu and stats
col1, col2 = st.columns([1,6])

# Create 1 columns for video and stats
col11 = st.columns(1)

# Choose the player
with col1:
    player_picked = st.selectbox(
            label = 'Select a player',
            options = list_active_players,
            index = None,
            placeholder = "Select a player...",
            label_visibility = 'collapsed'
        )

# Conditional logic to handle the case where no option is selected
if player_picked:
    # Function to get the stats of the 3 last games for the player picked
    [last_5_games, player_id] = player_last_stats(player_picked)

    # get the image of the player and display it
    image_picked = get_player_image(player_id)

    player_caption = player_picked # add more info here from get_player_image

    # Display image in the first column
    with colA:
        st.image(image_picked, caption=player_caption, width=250)

    # Display DataFrame in the second column
    with col2:
        st.dataframe(last_5_games, hide_index=True, height=210)


    ### to do ###
    # Add the scores

    # Select a game and find location
    with col1:
        game_id = st.selectbox(
            label = 'Select a Game',
            options = last_5_games['Game_ID'],
            index = None,
            placeholder = "Select a Game_ID...",
            label_visibility = 'collapsed'
        )


    if game_id:
        game_location = last_5_games[last_5_games['Game_ID']==game_id]['location'].values[0]

        # Choose an option
        with col1:
            option = st.selectbox(
                label = 'Select a sequences option',
                options = ['Full', 'Best', 'FG', 'AST','BLOCK'],
                index=None,
                placeholder="Select a sequences option...",
                label_visibility = 'collapsed'
            )

        # Conditional logic to handle the case where no option is selected
        if option:
            # Function to get the videos of the selected game for the player
            video_event_df = get_mp4_urls(player_id, game_id, game_location, option)

            video_urls = video_event_df['video'].to_list()

            # Add a video at the end of the list
            #video_urls.append("https://www.youtube.com/watch?v=3Qz1GMpOtUY")

            # Convert Python list of URLs to a JavaScript-compatible array
            video_urls_js = ','.join(f'"{url}"' for url in video_urls) # needed for the first video player

            # Load the video player
            video_player_html = generate_video_player(video_urls, video_urls_js)


            # Display the video player in Streamlit
            go_button = 0
            with col1:
                if st.button(f"Play {len(video_urls)} sequences", type="primary"):
                   go_button = 1

            if go_button == 1:
                st.components.v1.html(video_player_html, height=1000)
                st.dataframe(video_event_df, hide_index=True)

# Module of data analysis
## plotly to make the chart settable
## display evolution of min per game over time
## as for babies, add mean and tendancy for player at the same position
## forecast the previous chart

# ML/AI
## to think about it
