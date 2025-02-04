### Function to get the last stats of the day by scraping the page
# 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'


import requests
import pandas as pd


def get_best_players_day():
    # Download the text file
    url = 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'
    response = requests.get(url)

    # Convert text to list of lines, skipping the first 5 header lines
    lines = response.text.splitlines()[5:]

    # Read the data using pandas with fixed-width format
    df = pd.read_fwf(pd.io.common.StringIO("\n".join(lines)))

    df['MyScore'] = df['PTS']+df['AST']+df['TRB']
    Four_best_day = df.sort_values(by='MyScore', ascending=False).head(4)

    Four_best_day['Formatted_name'] = Four_best_day['NAME'].apply(lambda x: " ".join(x.split(", ")[::-1]).lower())

    return Four_best_day
