import streamlit as st
import pandas as pd
from datetime import datetime


from video_player_module import generate_video_player
from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from select_sequences import select_sequences

st.title("🏀 Frenchies")

### French players
my_champs_french = [
    "Wembanyama, Victor",
    "Gobert, Rudy",
    "Batum, Nicolas",
    "Yabusele, Guerschon",
    "Coulibaly, Bilal",
    "Dieng, Ousmane",
    "Luwawu-Cabarrot, Timothé",
    "Sarr, Olivier",
    "Risacher, Zaccharie",
    "Sarr, Alex",
    "Sarr, Olivier",
    "Essengue, Noa",
    "Rupert, Rayan",
    "Cissoko, Sidy",
    "Beringer, Joan",
    "Diawara, Mohamed",
    "Dadiet, Pacome",
    "Raynaud, Maxime",
    "Traoré, Nolan",
    "Penda, Noah"

]

my_champs_french_converted = [" ".join(name.split(", ")[::-1]).lower() for name in my_champs_french]

st.write("This page displays stats for french players of that list {my_champs_french_converted}")

# Get today local files ---
input_file_1 = f"data/best_players_day.csv"
df_not_best_performers = pd.read_csv(input_file_1).iloc[5:].reset_index(drop=True)
french_players_day = df_not_best_performers[df_not_best_performers['NAME'].isin(my_champs_french)]

# Get today local files ---
input_file_2 = f"data/picked_players.csv"
picked_players = pd.read_csv(input_file_2).iloc[5:].reset_index(drop=True)

picked_french_players = picked_players[picked_players['player_name'].isin(my_champs_french_converted)]

input_file_3 = f"data/picked_players_info.csv"
picked_players_info = pd.read_csv(input_file_3).iloc[5:].reset_index(drop=True)

french_players_info = picked_players_info[picked_players_info['Name'].isin(my_champs_french_converted)]

input_file_4 = f"data/picked_players_video_event_df.csv"
picked_players_video_event_df = pd.read_csv(input_file_4)
picked_players_video_event_df = picked_players_video_event_df.dropna(subset=['video']).reset_index(drop=True)
supertars_video_event_df = picked_players_video_event_df[picked_players_video_event_df['player_name'].isin(my_champs_french_converted)]


# For 5 french players not in the best performer of the day
# each column = image + nom + stats

playerS_name= french_players_day['Formatted_name'].to_list()
images_picked = picked_french_players['img']
players_names = picked_french_players['player_name']

# ---  Create the five columns ---
player_cols = st.columns(5)

# ---  Prepare stats (loop-based) ---
player_dfs = []

for player_name in players_names:
    # Filter data
    df_season = french_players_info[
        french_players_info['Name'] == player_name.lower()
    ][['PTS', 'REB', 'AST']]

    df_today = french_players_day[
        french_players_day['Formatted_name'] == player_name.lower()
    ][['PTS', 'TRB', 'AST']].rename(columns={'TRB': 'REB'})

    # Combine
    df_player = pd.concat([df_season, df_today], ignore_index=True)

    # Create Period column dynamically based on number of rows
    periods = ['Season', 'Today'][:len(df_player)]
    df_player.insert(0, 'Period', periods)

    player_dfs.append(df_player)

# --- Precompute sequences for each player and each option ---

options = ["Full", "Best", "FGA", "FGM", "AST", "REB", "BLOCK"]
video_options_dict = {}

for player_name in players_names:
    player_videos = {}
    game_location = picked_french_players.loc[picked_french_players["player_name"] == player_name.lower(), "location"].iloc[0]
    player_id = picked_french_players.loc[picked_french_players["player_name"] == player_name.lower(), "player_id"].iloc[0]

    for opt in options:
        df_opt = select_sequences(supertars_video_event_df, player_id, game_location, opt)
        player_videos[opt] = df_opt

    video_options_dict[player_name.lower()] = player_videos

# ---  Display player cards ---

play_clicked = None
video_player_html = None
video_event_df = None

# Use st.session_state to store which button was clicked and which video set should be displayed.
# Initialize state
if "selected_player" not in st.session_state:
    st.session_state["selected_player"] = None
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None

# Loop over players
for i, (col, player_name, df) in enumerate(zip(player_cols, players_names, player_dfs)):
    with col:
        # --- Image + stats ---
        mask = picked_players_info['Name'].str.lower() == player_name.lower()
        if mask.any():
            if picked_players_info.loc[mask, 'DRAFT_YEAR'].iloc[0] == "Undrafted":
                draft_year = "Undrafted"
                draft_round = 'U'
                draft_number = 'U'
            else:
                jersey_number = picked_players_info.loc[mask, 'JERSEY'].iloc[0]
                draft_year = picked_players_info.loc[mask, 'DRAFT_YEAR'].iloc[0]
                draft_round = picked_players_info.loc[mask, 'DRAFT_ROUND'].iloc[0]
                draft_number = picked_players_info.loc[mask, 'DRAFT_NUMBER'].iloc[0]

        else:
            jersey_number = "?"

        # Use HTML code to center the image
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="{images_picked.iloc[i]}" width="250"><br>
                <strong>{player_name.title()}  # {jersey_number}</strong><br>
                Draft: {draft_year} — R: {draft_round}, Pick {draft_number}
            </div>
            """,
            unsafe_allow_html=True
            )

        st.dataframe(df, hide_index=True, height=110)

        # Buttons for options
        if st.button(f"Full - {len(video_options_dict[player_name]["Full"]['video'])} sequences", key=f"full_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "Full"

        if st.button(f"Best - {len(video_options_dict[player_name]["Best"]['video'])} sequences", key=f"best_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "Best"

        if st.button(f"FGA - {len(video_options_dict[player_name]["FGA"]['video'])} sequences", key=f"fga_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "FGA"

        if st.button(f"FGM - {len(video_options_dict[player_name]["FGM"]['video'])} sequences", key=f"fgm_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "FGM"

        if st.button(f"AST - {len(video_options_dict[player_name]["AST"]['video'])} sequences", key=f"ast_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "AST"

        if st.button(f"REB - {len(video_options_dict[player_name]["REB"]['video'])} sequences", key=f"rbd_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "REB"

        if st.button(f"BLOCK - {len(video_options_dict[player_name]["BLOCK"]['video'])} sequences", key=f"block_{i}", width="stretch"):
            st.session_state["selected_player"] = player_name
            st.session_state["selected_option"] = "BLOCK"

# --- Below all players ---
if st.session_state["selected_player"]:
    player = st.session_state["selected_player"]
    option = st.session_state["selected_option"]

    # Get URLs directly from your dictionary
    video_urls = video_options_dict[player][option]['video'].to_list()

    # Prepare JS and HTML player
    video_urls_js = ','.join(f'"{url}"' for url in video_urls)
    video_player_html_i = generate_video_player(video_urls, video_urls_js)

    st.markdown(f"### 🎥 {player.title()} – {option} sequences")
    st.components.v1.html(video_player_html_i, height=800)
