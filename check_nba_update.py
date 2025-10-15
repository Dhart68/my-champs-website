import requests
from datetime import datetime
from pathlib import Path
import pandas as pd


## A REVOIR ####################


# load last file saved
saved_day_df = pd.read_csv("data/all_players_day.csv")

# Get last file online
url = 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'
response = requests.get(url)

# Convert text to list of lines, skipping the first 5 header lines
lines = response.text.splitlines()[5:]

# header
header_line = lines[0] #
Col_names = header_line.split()

## For name longer than 20 char I have to add this lines of code to calculate the widths of each column (pd.read_fwf limit to 20 chars)
# Find the starting position of each column name
start_positions = {}
current_position = 0
for col_name in Col_names:
    start_positions[col_name] = header_line.find(col_name, current_position)
    current_position = start_positions[col_name] + len(col_name)

list_start = list(start_positions.values())

widths_list = []
for i in range(len(list_start)-1):
    widths_list.append((list_start[i+1])-(list_start[i]))

widths_list.append(3)

# data
data = response.text.splitlines()[6:]
# Read the data using pandas with fixed-width format
df_day = pd.read_fwf(pd.io.common.StringIO("\n".join(data)), names = Col_names, widths = widths_list) # specify the size of the col


# Compare
if df_day.equals(saved_day_df):
    print("✅ Data up to date!")

else:
    print("Data need update")
