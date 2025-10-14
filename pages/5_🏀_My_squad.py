import streamlit as st
import pandas as pd
from datetime import datetime

from display_news_tickers import display_news_ticker
from get_last_scores import get_last_scores
from select_sequences import select_sequences
from video_player_module import generate_video_player

st.title("🏀 My Favorit Champs")

st.write(""" This page could displays stats for your selected players./n
         To be able to add your champs we need to have your list in advance
         to fetch information every day and provide you the best experience./n
         We have to recognize it's you, so we need you to log in to our website.""")
