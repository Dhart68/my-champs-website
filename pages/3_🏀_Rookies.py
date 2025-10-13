import streamlit as st
import pandas as pd
from datetime import datetime

from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from select_sequences import select_sequences
from video_player_module import generate_video_player

st.title("🏀 Rookies 2025")

st.write("This page displays stats for your selected players.")
