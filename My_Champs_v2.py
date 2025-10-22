import streamlit as st
import pandas as pd
from datetime import datetime

from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from select_sequences import select_sequences
from video_player_module import generate_video_player
from player_last_stats import player_last_stats

st.set_page_config(page_title="MY CHAMPS", page_icon="🏀", layout="wide")
st.title("MY CHAMPS")

# --- SESSION INIT ---
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "video_html" not in st.session_state:
    st.session_state.video_html = None


# --- CACHE HEAVY OPS ---
@st.cache_data(show_spinner=False)
def load_csvs():
    best = pd.read_csv("data/best_players_day.csv").head(6)
    picked = pd.read_csv("data/picked_players.csv").head(6).reset_index(drop=True)
    info = pd.read_csv("data/picked_players_info.csv").head(6)
    video_df = pd.read_csv("data/picked_players_video_event_df.csv").dropna(subset=["video"]).reset_index(drop=True)
    return best, picked, info, video_df


@st.cache_data(show_spinner=False)
def prepare_video_options(players_names, picked_players, picked_players_video_event_df):
    options = ["Full", "Best", "FGA", "FGM", "AST", "REB", "BLOCK"]
    video_options_dict = {}

    for player_name in players_names:
        player_videos = {}
        game_location = picked_players.loc[picked_players["player_name"] == player_name.lower(), "location"].iloc[0]
        player_id = picked_players.loc[picked_players["player_name"] == player_name.lower(), "player_id"].iloc[0]

        for opt in options:
            df_opt = select_sequences(picked_players_video_event_df, player_id, game_location, opt)
            player_videos[opt] = df_opt

        video_options_dict[player_name.lower()] = player_videos

    return video_options_dict


# --- LOAD DATA (CACHED) ---
best_players_day, picked_players, picked_players_info, picked_players_video_event_df = load_csvs()

today = datetime.today().strftime("%Y-%m-%d")
if today != best_players_day['DATE'][0]:
    st.warning(f"Old data ({best_players_day['DATE'][0]}) - Please update")

# --- DISPLAY TICKER ---
col_00, col_01 = st.columns([9, 1], vertical_alignment="center")
games_date, number_of_games, scores, scores_df = get_last_scores()
with col_00:
    display_news_ticker([games_date, str(scores)], duration=30)

# --- PREPARE PLAYER DATA ---
players_names = picked_players["player_name"].tolist()
images_picked = picked_players["img"]

video_options_dict = prepare_video_options(players_names, picked_players, picked_players_video_event_df)

# --- DISPLAY PLAYER CARDS ---
player_cols = st.columns(5)

for i, (col, player_name) in enumerate(zip(player_cols, players_names)):
    with col:
        image_player = images_picked.iloc[i] if images_picked.iloc[i] else "data/Picture1.png"
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{image_player}" width="250"><br>
                <strong>{player_name.title()}</strong>
            </div>
        """, unsafe_allow_html=True)

        # Buttons that store player + option
        for opt in ["Full", "Best", "FGA", "FGM", "AST", "REB", "BLOCK"]:
            label = f"{opt} - {len(video_options_dict[player_name][opt]['video'])} seq"
            if st.button(label, key=f"{opt}_{i}"):
                st.session_state.selected_player = player_name
                st.session_state.selected_option = opt
                st.session_state.video_html = None  # reset to rebuild later


# --- VIDEO PLAYER ---
if st.session_state.selected_player:
    player = st.session_state.selected_player
    option = st.session_state.selected_option

    if st.session_state.video_html is None:
        [last_n_games, player_id] = player_last_stats(player, 5)
        video_urls = video_options_dict[player][option]["video"].tolist()
        video_urls_js = ",".join(f'"{url}"' for url in video_urls)
        st.session_state.video_html = generate_video_player(video_urls, video_urls_js)
        st.session_state.last_n_games = last_n_games

    st.markdown(f"### 🎥 {player.title()} – {option} sequences")
    st.components.v1.html(st.session_state.video_html, height=800)

    st.markdown(f"### Last 5 games statistics : {player.title()}")
    st.dataframe(st.session_state.last_n_games, hide_index=True, height=210)
