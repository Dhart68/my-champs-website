import streamlit as st
import pandas as pd
from datetime import datetime

from nba_api.stats.static import players
from nba_api.stats.endpoints import BoxScoreMatchupsV3


from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls
from get_player_image import get_player_image
from video_player_module import generate_video_player
from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from get_players_info import get_players_info
from select_sequences import select_sequences

st.title("🏀 Rookies 2025")

st.write("This page displays stats for your selected players.")
