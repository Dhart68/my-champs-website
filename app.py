# MyChamps : Each day, get their best, their worst, just select your player


import streamlit as st
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreMatchupsV3


from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image
from video_player_module import generate_video_player
from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from get_players_info import get_players_info
from get_best_players_day import get_best_players_day


## To test the timing of the app
import cProfile
import pstats
import io
import time

def profile_function(func, *args, **kwargs):
    """Profiles a function and prints top 15 slowest calls."""
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args, **kwargs)
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15)  # top 15 slowest functions

    st.text("🕵️ Profiling Results (Top 15 slowest calls):")
    st.text(s.getvalue())
    return result


st.set_page_config(layout="wide")

# get the list of active players
active_players= players.get_active_players()
list_active_players = [player['full_name'] for player in active_players]

##### lots to do ####
# Trop lent: faire plus simple: (le 5 octobre 2025)
#               - preloader les 4 joueurs tous les jours
#                   > trouver quand a lieu le refresh des data sur nba api
#                    R: for Regular season and Playoff :
#                       > Updated within a few minutes after each game finishes (usually 5–15 minutes after the box score appears on NBA.com).
#               - ne pas donner le choix du match et des types de video
#               - loader les video des que le choix du joueur est fait
#               - lancer une video d'attente (pub?)
##
##
# 4 octobre 2025
# # If the season hasn’t started yet (like now), or you want Summer League, Preseason, In-Season Tournament, All-Star, etc., that endpoint will return nothing.
# should define parameter to look info regarding the schedule of the day by getting the date of today and then define the parameter, to avoid test in the function
# player last stat
#
# when load the page = clip to wait

# + 4 best performers + Top 10 + Dunk Party + Block Party

# Preload data from best players etc... (best option)
# - get the time of the last game to scrap the results
# - When preloaded => picture of the player is clickable and launch the video

# Cookie to recognize the user or account?

# top 10 # to do, number changing awkwardly
# to do :  Add a video at the end of the sequence
# to do: Conditional logic to handle the case where no option is selected

# to do: Wemby Block party ==> New feature select a player select BLoCK, DUNK et periode ==> Clip

# Dunk Score : 5 octobre 2025 ChatGPT : " Unfortunately, the NBA’s public stats API (and thus nba_api) does not expose a direct “dunk count” or “dunk score” field in any of its standard endpoints like playergamelog, boxscore, or shotchartdetail."

# Blocks Time : clip of all blocks of the night

## Create 2 columns for scores of the day and top 10
col_00, col_01 = st.columns([9,1], vertical_alignment="center")

# get last scores of the day
[games_date, number_of_games, scores, scores_df] = get_last_scores()

# Display the news ticker
news = [games_date, str(scores), games_date, str(scores)]

with col_00:
  display_news_ticker(news_items=news, duration=30)

# Display game score as a dataframe
# with col_00:
#    st.table(scores_df)#, hide_index=True,  height=30)

## top 10 # to do, number changing awkwardly
top_10_url = 'https://www.nba.com/watch/video/mondays-top-plays-84?plsrc=nba&collection=more-to-watch'
# https://www.nba.com/watch/video/sundays-top-plays-74?plsrc=nba&collection=more-to-watch
# https://www.nba.com/watch/video/saturdays-top-plays-250125?plsrc=nba&collection=more-to-watch

with col_01:
    #st.image('https://cdn.nba.com/manage/2025/02/Top10Plays2.4.25.png')
    #st.link_button("Top 10", top_10_url)
    st.markdown("[![Foo](https://cdn.nba.com/manage/2025/02/Top10Plays2.4.25.png)](https://www.nba.com/watch/video/mondays-top-plays-84?plsrc=nba&collection=more-to-watch)")


## Display 4 best players of the day pictures and main stats (last game PTS, RBD, AST)
# to do : when you click on a picture you launch the viewer with all the selectbox defined
Four_best_day = get_best_players_day() # 1 seconde

playerS_name=Four_best_day['Formatted_name'].to_list()

# Create 5 columns
colA, colB, colC, colD, colE = st.columns(5)

# for the 4 best players + one empty to fill by the user
# each column = image + nom + stats
[picked_players, picked_players_info] = get_players_info(playerS_name) # (1786290 primitive calls) in 7.985 seconds

images_picked = picked_players['img']
players_names = picked_players['player_name']
df1_s = picked_players_info[picked_players_info['Name'] == players_names[0].lower()][['PTS','REB','AST']]
df1_day = Four_best_day[Four_best_day['Formatted_name'] == players_names[0].lower()][['PTS','TRB','AST']]
df1 = pd.concat([df1_s,df1_day.rename(columns={'TRB':'REB'})], ignore_index=True)
df1.insert(0, 'Period', ['Season', 'Today'])


# to do : add the scores of the day in a second line
df2_s = picked_players_info[picked_players_info['Name'] == players_names[1].lower()][['PTS','REB','AST']]
df2_day = Four_best_day[Four_best_day['Formatted_name'] == players_names[1].lower()][['PTS','TRB','AST']]
df2 = pd.concat([df2_s,df2_day.rename(columns={'TRB':'REB'})], ignore_index=True)
df2.insert(0, 'Period', ['Season', 'Today'])

df3_s = picked_players_info[picked_players_info['Name'] == players_names[2].lower()][['PTS','REB','AST']]
df3_day = Four_best_day[Four_best_day['Formatted_name'] == players_names[2].lower()][['PTS','TRB','AST']]
df3 = pd.concat([df3_s,df3_day.rename(columns={'TRB':'REB'})], ignore_index=True)
df3.insert(0, 'Period', ['Season', 'Today'])

df4_s = picked_players_info[picked_players_info['Name'] == players_names[3].lower()][['PTS','REB','AST']]
df4_day = Four_best_day[Four_best_day['Formatted_name'] == players_names[3].lower()][['PTS','TRB','AST']]
df4 = pd.concat([df4_s,df4_day.rename(columns={'TRB':'REB'})], ignore_index=True)
df4.insert(0, 'Period', ['Season', 'Today'])

with colB:
    st.image(images_picked[0], caption = f"{players_names[0].title()}  #  {picked_players_info[picked_players_info['Name'] == players_names[0].lower()]['JERSEY'][0]}", width=250)
    st.dataframe(df1, hide_index=True, height=110)

with colC:
    st.image(images_picked[1], caption = f"{players_names[1].title()}  #  {picked_players_info[picked_players_info['Name'] == players_names[1].lower()]['JERSEY'][1]}", width=250)
    st.dataframe(df2, hide_index=True, height=110)

with colD:
    st.image(images_picked[2], caption = f"{players_names[2].title()}  #  {picked_players_info[picked_players_info['Name'] == players_names[2].lower()]['JERSEY'][2]}", width=250)
    st.dataframe(df3, hide_index=True, height=110)

with colE:
    st.image(images_picked[3], caption = f"{players_names[3].title()}  #  {picked_players_info[picked_players_info['Name'] == players_names[3].lower()]['JERSEY'][3]}", width=250)
    st.dataframe(df4, hide_index=True, height=110)


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

# to do: Conditional logic to handle the case where no option is selected

if player_picked:
    # Function to get the stats of the 5 last games for the player picked
    [last_n_games, player_id] = player_last_stats(player_picked, 5) # 426333 primitive calls) in 2.618 seconds

    # get the season stats of the player
    [picked_p, picked_p_info] = get_players_info([player_picked.lower()]) #497941 primitive calls) in 1.554 seconds
    p_name = picked_p['player_name']
    dfp=picked_p_info[picked_p_info['Name'] == p_name[0].lower()][['JERSEY','PTS','REB','AST']]

    # get the image of the player and display it
    image_picked = get_player_image(player_id) # 93553 primitive calls) in 0.833 seconds

    player_caption = player_picked # add more info here from get_player_image

    # Display image in the first column
    with colA:
        st.image(image_picked, caption=player_caption, width=250)
        st.dataframe(dfp, hide_index=True, height=20)

    # Display DataFrame in the second column
    with col2:
        st.dataframe(last_n_games, hide_index=True, height=210)

    # Select a game and find location
    with col1:
        game_id = st.selectbox(
            label = 'Select a Game',
            options = last_n_games['Game_ID'],
            index = None,
            placeholder = "Select a Game_ID...",
            label_visibility = 'collapsed'
        )

    if game_id:
        game_location = last_n_games[last_n_games['Game_ID']==game_id]['location'].values[0]

        # Choose an option
        with col1:
            option = st.selectbox(
                label = 'Select a sequences option',
                options = ['Full', 'Best', 'FGA', 'FGM', 'AST', 'REB', 'BLOCK'],
                index=None,
                placeholder="Select a sequences option...",
                label_visibility = 'collapsed'
            )

        # Conditional logic to handle the case where no option is selected
        if option:
            # Function to get the videos of the selected game for the player
            video_event_df = get_mp4_urls(player_id, game_id, game_location, option) # 131570 primitive calls) in 77.593 seconds pour 12 sequences// 334404 primitive calls) in 137.805 seconds pour 44 sequences

            video_urls = video_event_df['video'].to_list()

            # Add a video at the end of the list
            # video_urls.append("https://www.youtube.com/watch?v=3Qz1GMpOtUY")

            # Convert Python list of URLs to a JavaScript-compatible array
            video_urls_js = ','.join(f'"{url}"' for url in video_urls) # needed for the video player js

            # Load the video player
            video_player_html = generate_video_player(video_urls, video_urls_js) # 0 second

            # Display the video player
            go_button = 0
            with col1:
                if st.button(f"Play {len(video_urls)} sequences", type="primary"):
                   start = time.time()
                   go_button = 1

            if go_button == 1:
                st.components.v1.html(video_player_html, height=1000)
                st.dataframe(video_event_df, hide_index=True)
                end = time.time()
                print(f"Load {len(video_urls)} sequences >>> Execution time: {end - start:.4f} seconds") #0.0024 seconds

# Module of data analysis
## plotly to make the chart settable
## display evolution of min per game over time
## as for babies, add mean and tendancy for player at the same position
## forecast the previous chart

# ML/AI
## to think about it
