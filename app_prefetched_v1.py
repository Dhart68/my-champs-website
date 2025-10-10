# MyChamps : Each day, get their best, their worst, just select your player
# Streamlit app read local or cached NBA data (e.g. CSV or database)
# Need update_nba_data.py

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
#from get_best_players_day import get_best_players_day


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


st.set_page_config(page_title="MY CHAMPS", page_icon="📈")

st.markdown("# Best Performer of the day")
st.sidebar.header("MY CHAMPS pages")
st.write(
    """Enjoy!"""
)


# get the list of active players
active_players= players.get_active_players() # not updated
list_active_players = [player['full_name'] for player in active_players]

##### lots to do ####
# voir app.py

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
# top_10_url = 'https://www.nba.com/watch/video/mondays-top-plays-84?plsrc=nba&collection=more-to-watch'
# https://www.nba.com/watch/video/sundays-top-plays-74?plsrc=nba&collection=more-to-watch
# https://www.nba.com/watch/video/saturdays-top-plays-250125?plsrc=nba&collection=more-to-watch

#with col_01:
    #st.image('https://cdn.nba.com/manage/2025/02/Top10Plays2.4.25.png')
    #st.link_button("Top 10", top_10_url)
    #st.markdown("[![Foo](https://cdn.nba.com/manage/2025/02/Top10Plays2.4.25.png)](https://www.nba.com/watch/video/mondays-top-plays-84?plsrc=nba&collection=more-to-watch)")


## Display 4 best players of the day pictures and main stats (last game PTS, RBD, AST)
# to do : when you click on a picture you launch the viewer with all the selectbox defined
#Four_best_day = get_best_players_day() # 1 seconde

Four_best_day = pd.read_csv('data/Four_best_day.csv')

playerS_name=Four_best_day['Formatted_name'].to_list()

# Create 5 columns
colA, colB, colC, colD, colE = st.columns(5)

# for the 4 best players + one empty to fill by the user
# each column = image + nom + stats
picked_players = pd.read_csv('data/picked_players.csv')
picked_players_info = pd.read_csv('data/picked_players_info.csv')
picked_players_video_event_df = pd.read_csv("data/picked_players_video_event_df.csv")

images_picked = picked_players['img']
players_names = picked_players['player_name']

# --- 1. Create the five columns ---
col_menu, *player_cols = st.columns(5)

# --- 2. Left column: filters or player selector ---
with col_menu:
    player_picked = st.selectbox(
        label = 'Select a player',
        options = list_active_players, # to update
        index = None,
        placeholder = "Select a player...",
        label_visibility = 'collapsed'
    )
    #if player_picked:
        # Function to get the stats of the 5 last games for the player picked
        #[last_n_games, player_id] = player_last_stats(player_picked, 1) # 426333 primitive calls) in 2.618 seconds

        # get the season stats of the player
        #[picked_p, picked_p_info] = get_players_info([player_picked.lower()]) #497941 primitive calls) in 1.554 seconds
        #p_name = picked_p['player_name']
        #df0=picked_p_info[picked_p_info['Name'] == p_name[0].lower()][['JERSEY','PTS','REB','AST']]

        # get the image of the player and display it
        #image_picked = get_player_image(player_id) # 93553 primitive calls) in 0.833 seconds
        #st.image(image_picked, caption=player_caption, width=250)

        #player_caption = player_picked # add more info here from get_player_image
        #st.dataframe(df0, hide_index=True, height=20)


# --- 3. Prepare stats (loop-based) ---
player_dfs = []
for player_name in players_names:
    df_season = picked_players_info[
        picked_players_info['Name'] == player_name.lower()
    ][['PTS', 'REB', 'AST']]

    df_today = Four_best_day[
        Four_best_day['Formatted_name'] == player_name.lower()
    ][['PTS', 'TRB', 'AST']].rename(columns={'TRB': 'REB'})

    df_player = pd.concat([df_season, df_today], ignore_index=True)
    df_player.insert(0, 'Period', ['Season', 'Today'])
    player_dfs.append(df_player)

# --- 4. Display player cards ---
play_clicked = None
video_player_html = None
video_event_df = None

for i, (col, player_name, df) in enumerate(zip(player_cols, players_names, player_dfs)):
    with col:
        # --- Image + stats ---
        jersey_number = picked_players_info.loc[
            picked_players_info['Name'] == player_name.lower(), 'JERSEY'].iloc[0]
        st.image(
            images_picked[i],
            caption=f"{player_name.title()}  #  {jersey_number}",
            width=250
        )
        st.dataframe(df, hide_index=True, height=110)

        # --- Video preparation ---
        video_event_df_i = picked_players_video_event_df[
            picked_players_video_event_df['player_name'] == player_name.lower()]
        video_urls = video_event_df_i['video'].to_list()
        video_urls_js = ','.join(f'"{url}"' for url in video_urls)
        video_player_html_i = generate_video_player(video_urls, video_urls_js)

        # --- Button ---
        if st.button(
            f"Play {len(video_urls)} sequences",
            type="primary",
            key=f"play_btn_{i}_{player_name}"
        ):
            play_clicked = i
            video_player_html = video_player_html_i
            video_event_df = video_event_df_i

# --- 5. Full-width player (below all columns) ---
if play_clicked is not None:
    st.markdown("---")
    st.components.v1.html(video_player_html, height=1000)
    st.dataframe(video_event_df, hide_index=True)

# Module of data analysis
## plotly to make the chart settable
## display evolution of min per game over time
## as for babies, add mean and tendancy for player at the same position
## forecast the previous chart

# ML/AI
## to think about it
